#!/usr/bin/env python3
"""Build the DGX-670 knowledge base (kb/) from the source PDFs.

Deterministic: the same PDFs always produce byte-identical generated files.
Generated:  kb/pages/**, kb/maps/{TOC,TERMS,BUTTONS,MENU_PATHS,DATALIST_TOC}.md, kb/INDEX.md
Read-only inputs it respects (never overwritten): kb/figures/*.md, kb/datalist/*,
kb/maps/GLOSSARY.md, faq/*. Cached figure titles are folded back into page markers.

Usage:  python scripts/build_kb.py
"""
import collections
import re
import sys
from pathlib import Path

import pymupdf

from kbcommon import KB, ROOT, cached_figure_titles, mark_figures

sys.stdout.reconfigure(encoding="utf-8")

SRC = ROOT / "dgx_source_docs"

DOCS = {
    "OM": dict(
        file="DGX-670_owners_manual_En_D0.pdf",
        title="Owner's Manual",
        roles={"cover": [1], "front-matter": range(2, 10), "overview": range(10, 12),
               "index": range(109, 111), "legal": range(111, 121)},
        index_pages=range(109, 111),
    ),
    "RM": dict(
        file="DGX-670_reference_manual_En_B0.pdf",
        title="Reference Manual",
        roles={"cover": [1], "toc": [2], "index": range(92, 94)},
        index_pages=range(92, 94),
    ),
}
DL_FILE = "dgx670_en_dl_b0.pdf"
# Pages with these roles never get figure descriptions (marketing, legal, etc.).
NO_FIGURE_ROLES = {"cover", "front-matter", "overview", "toc", "index", "legal"}
CHAPTERS = ["Piano Room", "Voices", "Styles", "Songs", "USB Audio Player/Recorder", "Microphone",
            "Registration Memory/Playlist", "Mixer", "Connections", "Menu"]

# --- Symbol fonts -> text. Calibrated once against Yamaha's supplied text export. ---
CIRCLE = {**{str(i): i for i in range(1, 10)}, ")": 10, "!": 11, "@": 12, "#": 13, "$": 14,
          "%": 15, "^": 16, "&": 17, "*": 18, "(": 19, **{c: 20 + i for i, c in enumerate("ABCDEF")}}
FONT_MAPS = [  # order matters: Wingdings3 before Wingdings
    ("MWspecial", {"U": "▲", "D": "▼", "L": "◀", "R": "▶", "K": "❚❚", "I": "●", "J": "■", "P": "⏻"}),
    ("ELEMARKplus", {"E": "◀", "F": "▶", "G": "◀◀", "H": "▶▶", "K": "❚❚"}),
    ("Wingdings3", {"": "▲", "": "▼", "": "→", "": "→"}),
    ("Wingdings", {"": "→", "": "■", "": "●"}),
]
TEXT_FLAGS = (pymupdf.TEXTFLAGS_DICT | pymupdf.TEXT_DEHYPHENATE) & ~pymupdf.TEXT_PRESERVE_LIGATURES


def map_span(font, text):
    base = font.split("+")[-1]
    if base.startswith("CircleNumberInv"):
        return "".join(f"({CIRCLE[c]})" if c in CIRCLE else c for c in text)
    for prefix, table in FONT_MAPS:
        if base.startswith(prefix):
            return "".join(table.get(c, c) for c in text)
    return text


def tidy(s):
    s = re.sub(r"[\x00-\x08\x0b-\x1f]", "", s)
    s = re.sub(r"\[(\d+)\s+([▲▼])", r"[\1\2", s)  # "[2 ▲▼]" -> "[2▲▼]"
    s = re.sub(r"[ \t ]+", " ", s)
    return s.strip()


# --- Page extraction ---------------------------------------------------------------

def body_size(doc):
    sizes = collections.Counter()
    for page in doc:
        for b in page.get_text("dict", flags=TEXT_FLAGS)["blocks"]:
            for l in b.get("lines", []):
                for s in l["spans"]:
                    sizes[round(s["size"], 1)] += len(s["text"])
    return sizes.most_common(1)[0][0]


def in_margin(bbox, W, H):
    x0, y0, x1, y1 = bbox
    return y0 > H * 0.935 or x0 > W * 0.93 or x1 < W * 0.07


SYMBOL_FONT = re.compile(r"MWspecial|Wingdings|CircleNumber|ELEMARK|^Symbol|SonataPoint")
NEW_ITEM = re.compile(r"^(•|■|●|\(\d+\)|\d+\)|NOTE\b|NOTICE\b)")


def edge_font(spans, last):
    """Font at the start/end of a line, ignoring symbol fonts and whitespace-only spans."""
    for s in (reversed(spans) if last else spans):
        f = s["font"].split("+")[-1]
        if s["text"].strip() and not SYMBOL_FONT.search(f):
            return f
    return None


def block_text(block, body):
    """Join wrapped lines; break where the font changes across the line boundary or a new item starts."""
    segs = []  # [text, size, heading, last_font]
    for line in block["lines"]:
        spans = [s for s in line["spans"] if s["text"]]
        if not spans:
            continue
        text = "".join(map_span(s["font"], s["text"]) for s in spans)
        dom = max(spans, key=lambda s: len(s["text"].strip()))
        size = round(dom["size"])
        heading = dom["size"] >= body * 1.25 and len(re.findall(r"[A-Za-z]", text)) >= 3
        first = edge_font(spans, last=False)
        continues = segs and (segs[-1][0].rstrip().endswith("→") or (
            segs[-1][1] == size and not NEW_ITEM.match(text.strip())
            and (first is None or segs[-1][3] is None or first == segs[-1][3])))
        if continues:
            segs[-1][0] += " " + text
            segs[-1][3] = edge_font(spans, last=True) or segs[-1][3]
        else:
            segs.append([text, size, heading, edge_font(spans, last=True)])
    out = []
    for text, _, heading, _ in segs:
        t = tidy(text)
        if not t:
            continue
        if out and re.fullmatch(r"\d{1,2}", out[-1]):  # big step number on its own line
            out[-1] = f"{out[-1]}. {t}"
            continue
        out.append(("## " + t) if heading and len(t) < 90 else t)
    return "\n".join(out)


def text_coverage(rect, text_bboxes):
    area = rect.get_area() or 1
    return sum((rect & pymupdf.Rect(b)).get_area() for b in text_bboxes) / area


def find_figures(page, blocks, W, H):
    text_bboxes = [b["bbox"] for b in blocks if b["type"] == 0]
    figs = [pymupdf.Rect(b["bbox"]) for b in blocks
            if b["type"] == 1 and pymupdf.Rect(b["bbox"]).get_area() > 1500]
    for r in page.cluster_drawings():
        banner = r.width > 0.6 * W and r.height < 0.12 * H  # decorative title bars / rules
        if r.width > 60 and r.height > 40 and not banner and text_coverage(r, text_bboxes) < 0.35 \
                and not any(r.intersects(f) for f in figs):
            figs.append(r)
    return [f for f in figs if not in_margin(tuple(f), W, H)]


def order_items(items, W):
    """Reading order. items: (bbox, kind, payload). Two-column pages read left then right."""
    mid = W / 2

    def col(b):
        if b[2] <= mid + 12:
            return 0
        if b[0] >= mid - 12:
            return 1
        return -1

    def ykey(it):
        return (round(it[0][1] / 4), it[0][0])

    chars = collections.Counter()
    for b, kind, payload in items:
        if kind == "text":
            chars[col(b)] += len(payload)
    if not (chars[0] > 200 and chars[1] > 200):
        return sorted(items, key=ykey)
    out, band = [], []

    def flush():
        band.sort(key=lambda it: (col(it[0]),) + ykey(it))
        out.extend(band)
        band.clear()

    for it in sorted(items, key=ykey):
        if col(it[0]) == -1:
            flush()
            out.append(it)
        else:
            band.append(it)
    flush()
    return out


def role_of(cfg, pno):
    for role, pages in cfg["roles"].items():
        if pno in pages:
            return role
    return "content"


def chapter_label(title):
    short = title.split(" – ")[0].strip()
    if short in CHAPTERS:
        return f"Ch{CHAPTERS.index(short) + 1} {short}"
    return title


def sections_for(toc, pno):
    """Breadcrumb from bookmarks: chapter › subsection(s) active on this page."""
    l1 = [t for t in toc if t[0] == 1 and t[2] <= pno]
    if not l1:
        return ""
    starting = [t for t in l1 if t[2] == pno]
    chap = starting if len(starting) > 1 else [l1[-1]]
    crumb = "; ".join(chapter_label(t[1]) for t in chap)
    last = chap[-1]
    idx = toc.index(last)
    subs = []
    for t in toc[idx + 1:]:
        if t[0] == 1:
            break
        if t[0] == 2 and t[2] <= pno:
            subs.append(t)
    here = [t for t in subs if t[2] == pno]
    pick = here if here else subs[-1:]
    if pick:
        crumb += " › " + "; ".join(t[1] for t in pick)
    return crumb


def extract_doc(key, cfg):
    doc = pymupdf.open(SRC / cfg["file"])
    body = body_size(doc)
    toc = [t[:3] for t in doc.get_toc()]
    pages = []
    for page in doc:
        pno = page.number + 1
        W, H = page.rect.width, page.rect.height
        blocks = page.get_text("dict", flags=TEXT_FLAGS)["blocks"]
        fig_rects = find_figures(page, blocks, W, H)
        labels = collections.defaultdict(list)  # text sitting inside a figure (callouts, key names)
        items = []
        for b in blocks:
            if b["type"] != 0 or in_margin(b["bbox"], W, H):
                continue
            t = block_text(b, body)
            if not t:
                continue
            r = pymupdf.Rect(b["bbox"])
            host = None if t.startswith("## ") else next(
                (i for i, f in enumerate(fig_rects) if (r & f).get_area() >= 0.8 * (r.get_area() or 1)), None)
            if host is None:
                items.append((b["bbox"], "text", t))
            else:
                labels[host].append((b["bbox"], "text", t.replace("\n", " ")))
        for i, f in enumerate(fig_rects):
            items.append((tuple(f), "fig", i))
        parts, figs, boxes = [], [], []
        for bbox, kind, payload in order_items(items, W):
            if kind == "fig":
                fid = f"{key}-{pno:03d}-f{len(figs) + 1}"
                figs.append(fid)
                x0, y0, x1, y1 = (round(100 * v / d) for v, d in zip(bbox, (W, H, W, H)))
                boxes.append(f"f{len(figs)} x{x0}-{x1}% y{y0}-{y1}%")
                lab = " ".join(t for _, _, t in order_items(labels[payload], W))
                parts.append(f"[FIG {fid}]" + (f"\nFigure text: {lab}" if lab else ""))
            else:
                parts.append(payload)
        links = set()
        for l in page.get_links():
            if l["kind"] in (pymupdf.LINK_GOTO, pymupdf.LINK_NAMED) and l.get("page", -1) >= 0:
                if l["page"] + 1 != pno:
                    links.add(l["page"] + 1)
        text = "\n\n".join(parts)
        refers = [d for d, pat in (("OM", r"Owner[’']s Manual"), ("RM", r"Reference Manual"), ("DL", r"Data List"))
                  if d != key and re.search(pat, text)]
        pages.append(dict(key=key, pno=pno, id=f"{key}-{pno:03d}", text=text, figs=figs, boxes=boxes,
                          links=sorted(links), refers=refers, role=role_of(cfg, pno),
                          section=sections_for(toc, pno)))
    return pages, toc, doc.page_count


# --- Page rendering ----------------------------------------------------------------

def render_page(p, cfg, links_in):
    titles = cached_figure_titles(p["id"])
    text = p["text"]
    if titles is not None:
        text = mark_figures(text, p["id"], titles)
    if not p["figs"]:
        cache = "n/a"
    elif titles is not None:
        cache = "done"
    elif p["role"] in NO_FIGURE_ROLES:
        cache = "skip"
    else:
        cache = "none"
    fmt = lambda xs: "[" + ", ".join(xs) + "]"
    leaf = p["section"].split(" › ")[-1] if p["section"] else cfg["title"]
    fm = [
        "---",
        f"id: {p['id']}",
        f"doc: {cfg['title']} ({cfg['file']})",
        f"page: {p['pno']}",
        f"section: {p['section']}",
        f"role: {p['role']}",
        f"links_out: {fmt(f'{p['key']}-{n:03d}' for n in p['links'])}",
        f"links_in: {fmt(links_in)}",
        f"refers_to: {fmt(p['refers'])}",
        f"figures: {fmt(p['figs'])}",
        f"figure_boxes: {fmt(p['boxes'])}",
        f"figure_cache: {cache}",
        "---",
    ]
    return "\n".join(fm) + f"\n# {p['key']} p.{p['pno']} — {leaf}\n\n{text}\n"


# --- Maps ---------------------------------------------------------------------------

def pid(key, n):
    return f"{key}-{n:03d}"


def toc_map(tocs, counts):
    lines = ["# Table of Contents Map", "",
             "Generated from the PDF bookmarks. Page IDs map to `kb/pages/<DOC>/<ID>.md`.",
             "Each Reference Manual chapter expands on the Owner's Manual chapter with the same number (RM p.2).", "",
             "## Chapter join (Owner's Manual ↔ Reference Manual)", "",
             "| Ch | Chapter | Owner's Manual | Reference Manual |", "|---|---|---|---|"]
    ranges = {}
    for key, toc in tocs.items():
        l1 = [t for t in toc if t[0] == 1]
        for i, t in enumerate(l1):
            short = t[1].split(" – ")[0].strip()
            if short in CHAPTERS:
                end = max(t[2], (l1[i + 1][2] - 1) if i + 1 < len(l1) else counts[key])
                ranges[(key, short)] = (t[2], end)
    for n, ch in enumerate(CHAPTERS, 1):
        cells = []
        for key in ("OM", "RM"):
            r = ranges.get((key, ch))
            cells.append((f"{key} p.{r[0]}" + (f"–{r[1]}" if r[1] > r[0] else "")) if r else "—")
        lines.append(f"| {n} | {ch} | {cells[0]} | {cells[1]} |")
    for key, toc in tocs.items():
        lines += ["", f"## {DOCS[key]['title']}", ""]
        for i, (lvl, title, start) in enumerate(toc):
            nxt = next((t[2] for t in toc[i + 1:] if t[0] <= lvl), counts[key] + 1)
            end = max(start, nxt - 1)
            rng = f"p.{start}" if end == start else f"p.{start}–{end}"
            lines.append(f"{'  ' * (lvl - 1)}- {title} — {key} {rng} → `{pid(key, start)}`")
    return "\n".join(lines) + "\n"


def parse_index_pages(key, cfg):
    doc = pymupdf.open(SRC / cfg["file"])
    entries = []
    for pno in cfg["index_pages"]:
        page = doc[pno - 1]
        W, H = page.rect.width, page.rect.height
        items = []
        for b in page.get_text("dict", flags=TEXT_FLAGS)["blocks"]:
            if b["type"] != 0 or in_margin(b["bbox"], W, H):
                continue
            for l in b["lines"]:
                t = tidy("".join(map_span(s["font"], s["text"]) for s in l["spans"]))
                if t:
                    items.append((l["bbox"], "text", t))
        pending = ""
        for _, _, t in order_items(items, W):
            m = re.match(r"^(.*?)\s*(?:\.\s*){2,}\s*([\d,\s–-]+)$", t)
            if m:
                term = tidy((pending + " " + m.group(1)).strip())
                nums = [int(x) for x in re.findall(r"\d+", m.group(2))]
                entries.append((term, nums))
                pending = ""
            elif len(t) > 1 and t not in ("Index", "Numerics") and not re.fullmatch(r"[A-Z]", t):
                pending = (pending + " " + t).strip()
    return entries


def terms_map():
    merged = collections.defaultdict(lambda: {"OM": [], "RM": []})
    for key, cfg in DOCS.items():
        for term, nums in parse_index_pages(key, cfg):
            merged[term][key] += nums
    lines = ["# Terms Map (printed indexes)", "",
             "Parsed from the printed indexes: Owner's Manual pp.109–110 and Reference Manual pp.92–93.",
             "Use this to jump from a manual term to its pages. For everyday wording, check `GLOSSARY.md` first.", "",
             "| Term | Owner's Manual | Reference Manual |", "|---|---|---|"]
    for term in sorted(merged, key=lambda s: (s.lower(), s)):
        cells = [", ".join(pid(k, n) for n in sorted(set(merged[term][k]))) or "—" for k in ("OM", "RM")]
        lines.append(f"| {term.replace('|', '/')} | {cells[0]} | {cells[1]} |")
    return "\n".join(lines) + "\n", len(merged)


BUTTON_RE = re.compile(r"\[([A-Z][A-Z0-9/&+.\- ]*[A-Za-z0-9+\-.])\]")


def buttons_map(pages):
    hits = collections.defaultdict(collections.Counter)
    for p in pages:
        if p["role"] != "content":
            continue
        for m in BUTTON_RE.finditer(p["text"]):
            name = m.group(1)
            if name.startswith("FIG ") or len(name) < 2:
                continue
            hits[name][p["id"]] += 1
    lines = ["# Panel Buttons Map", "",
             "Every bracketed panel control mentioned on a content page → pages, most mentions first (top 12).", "",
             "| Button | Mentions | Pages |", "|---|---|---|"]
    for name in sorted(hits, key=lambda s: (s.lower(), s)):
        c = hits[name]
        top = sorted(c.items(), key=lambda kv: (-kv[1], kv[0]))[:12]
        lines.append(f"| [{name}] | {sum(c.values())} | " + ", ".join(f"{k} ({v})" for k, v in top) + " |")
    return "\n".join(lines) + "\n", len(hits)


def extract_paths(text):
    paths = []
    for line in text.split("\n"):
        pos = 0
        while True:
            a = line.find("→", pos)
            if a < 0:
                break
            start = line.rfind("[", 0, a)
            # walk back to the first "[BUTTON]" that begins the chain
            while start > 0:
                prev = line.rfind("[", 0, start)
                seg = line[prev:start]
                if prev >= 0 and "→" in line[prev:start] and not re.search(r"[.;:]\s", seg):
                    start = prev
                else:
                    break
            if start < 0:
                pos = a + 1
                continue
            end, depth, i = len(line), 0, a
            last_arrow = a
            while i < len(line):
                ch = line[i]
                if ch == "[":
                    depth += 1
                elif ch == "]":
                    depth = max(0, depth - 1)
                elif ch == "→":
                    last_arrow = i
                elif depth == 0 and ch in ".;" and (i + 1 == len(line) or line[i + 1] == " ") and i > last_arrow:
                    end = i
                    break
                i += 1
            path = line[start:end].strip().rstrip(",")
            if path.count("→") >= 1:
                paths.append(path)
            pos = end
    return paths


def dest_name(path):
    """Human name of where a path ends: last step minus button tokens and trailing prose."""
    for seg in reversed([x for x in path.split("→") if x.strip()]):
        seg = re.split(r",? and then|, and |\(page|\(→", seg)[0]
        seg = re.sub(r"\[[^\]]*\]|\bCursor buttons?\b|\bTAB\b|\bbuttons?\b|\bor\b|[()]", " ", seg)
        seg = tidy(re.sub(r"^[\d\s–-]*", "", seg.strip())).strip(" ,.–-/")
        if seg:
            return seg
    return "(button step)"


def menu_paths_map(pages):
    seen = collections.OrderedDict()
    for p in pages:
        if p["role"] != "content":
            continue
        for path in extract_paths(p["text"]):
            dest = dest_name(path)
            seen.setdefault((dest.lower(), path), (dest, path, set()))[2].add(p["id"])
    rows = sorted(seen.values(), key=lambda r: (r[0].lower(), r[1]))
    lines = ["# Menu / Navigation Paths Map", "",
             "Every button → display navigation path printed in the manuals, sorted by destination.",
             "Symbols: ▲▼◀▶ = cursor/display buttons, [1▲▼] = numbered display buttons, → = next step.", "",
             "| Destination | Path | Pages |", "|---|---|---|"]
    for dest, path, ids in rows:
        lines.append(f"| {dest.replace('|', '/')} | {path.replace('|', '/')} | {', '.join(sorted(ids))} |")
    return "\n".join(lines) + "\n", len(rows)


def datalist_toc():
    doc = pymupdf.open(SRC / DL_FILE)
    page = doc[0]
    W = page.rect.width
    items = []
    for b in page.get_text("dict", flags=TEXT_FLAGS)["blocks"]:
        if b["type"] != 0:
            continue
        for l in b["lines"]:
            t = tidy("".join(s["text"] for s in l["spans"]))
            if t:
                items.append((l["bbox"], "text", t))
    entries, group = [], []
    for _, _, t in order_items(items, W):
        group.append(t)
        m = re.search(r"\.{3,}\s*(\d+)$", t)
        if m:
            entries.append((group[-4].rstrip(" /").strip(), int(m.group(1))))  # EN is 1st of 4 languages
            group = []
    entries.sort(key=lambda e: e[1])
    lines = ["# Data List — Table of Contents", "",
             f"From page 1 of `dgx_source_docs/{DL_FILE}` ({doc.page_count} pages, 4 languages; English column first).",
             "Every table is extracted to CSV: search the briefs in `kb/datalist/INDEX.md`, then grep `kb/datalist/csv/`.", "",
             "| Section | DL pages |", "|---|---|"]
    for i, (title, start) in enumerate(entries):
        end = entries[i + 1][1] - 1 if i + 1 < len(entries) else doc.page_count
        end = max(start, end)
        lines.append(f"| {title} | p.{start}" + (f"–{end}" if end > start else "") + " |")
    return "\n".join(lines) + "\n", len(entries)


def index_md(stats):
    return f"""# DGX-670 Knowledge Base — Start Here

Source of truth: the PDFs in `dgx_source_docs/`. Everything in `kb/` is derived from them or cached from them.

## Where to look (in this order)
1. `../faq/INDEX.md` — answers the user already verified.
2. `maps/GLOSSARY.md` — everyday words → the manual's terms.
3. `maps/TERMS.md` — printed-index terms → page IDs ({stats['terms']} terms).
4. `maps/BUTTONS.md` — panel button → pages ({stats['buttons']} buttons).
5. `maps/MENU_PATHS.md` — "how do I get to setting X" → exact button path ({stats['paths']} paths).
6. `maps/TOC.md` — bookmark tree + Owner's ↔ Reference Manual chapter join.
7. `pages/OM/OM-nnn.md`, `pages/RM/RM-nnn.md` — one file per PDF page (OM {stats['OM']} pages, RM {stats['RM']} pages).
8. `figures/INDEX.md` — figures already described (cache).
9. `datalist/INDEX.md` — every Data List table (voices, styles, songs, drum kits, effects, Parameter Chart,
   Direct Access Chart, MIDI) as CSV, with a searchable brief each. `maps/DATALIST_TOC.md` — its page ranges.
10. `guides/` — cited cheat sheets that pull one topic together across OM/RM/DL (e.g. `voice-editing-cheat-sheet.md`).

## Page file conventions
- Frontmatter: `section` (bookmark breadcrumb), `role`, `links_out`/`links_in` (clickable PDF cross-references),
  `refers_to` (other manuals mentioned), `figures`, `figure_cache` (`none` = not yet described, `done`, `skip`, `n/a`).
- `[FIG RM-031-f1]` marks where a figure sits. Once described it reads `[FIG RM-031-f1 — <title>; see kb/figures/RM-031.md#f1]`.
- Symbols: ▲▼◀▶ cursor/display buttons · [1▲▼] numbered display buttons · → navigation step ·
  (n) numbered callout · ⏻ power · ▶/❚❚ play/pause · ● record · ■ stop.
- Citation IDs: `OM-050` = Owner's Manual printed page 50 = PDF page 50 (identical numbering; same for RM).
"""


# --- Main ---------------------------------------------------------------------------

def write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists() or path.read_text(encoding="utf-8") != content:
        path.write_text(content, encoding="utf-8", newline="\n")


def seed(path, content):
    if not path.exists():
        write(path, content)


def main():
    all_pages, tocs, counts = [], {}, {}
    for key, cfg in DOCS.items():
        pages, toc, n = extract_doc(key, cfg)
        all_pages += pages
        tocs[key], counts[key] = toc, n
    links_in = collections.defaultdict(set)
    for p in all_pages:
        for n in p["links"]:
            links_in[pid(p["key"], n)].add(p["id"])
    for p in all_pages:
        cfg = DOCS[p["key"]]
        write(KB / "pages" / p["key"] / f"{p['id']}.md", render_page(p, cfg, sorted(links_in[p["id"]])))

    write(KB / "maps" / "TOC.md", toc_map(tocs, counts))
    terms, n_terms = terms_map()
    write(KB / "maps" / "TERMS.md", terms)
    buttons, n_buttons = buttons_map(all_pages)
    write(KB / "maps" / "BUTTONS.md", buttons)
    paths, n_paths = menu_paths_map(all_pages)
    write(KB / "maps" / "MENU_PATHS.md", paths)
    dl, n_dl = datalist_toc()
    write(KB / "maps" / "DATALIST_TOC.md", dl)
    write(KB / "INDEX.md", index_md(dict(terms=n_terms, buttons=n_buttons, paths=n_paths, **counts)))

    seed(KB / "figures" / "INDEX.md",
         "# Figure Cache Index\n\nPages whose figures have been described. One row per page; details in `<PAGE-ID>.md`.\n\n"
         "| Page | Figures | Summary |\n|---|---|---|\n")
    seed(ROOT / "faq" / "INDEX.md",
         "# Verified FAQ\n\nAnswers the user confirmed as correct. One row per entry; details in `faq/<slug>.md`.\n\n"
         "| Question | File | Citations |\n|---|---|---|\n")

    figs = collections.Counter(p["key"] for p in all_pages for _ in p["figs"])
    unmapped = sum(len(re.findall(r"[-�]", p["text"])) for p in all_pages)
    print(f"pages: OM {counts['OM']}, RM {counts['RM']} | figures: OM {figs['OM']}, RM {figs['RM']} | "
          f"links: {sum(len(p['links']) for p in all_pages)} | terms {n_terms}, buttons {n_buttons}, "
          f"paths {n_paths}, DL sections {n_dl} | unmapped glyphs: {unmapped}")


if __name__ == "__main__":
    main()
    import build_datalist  # Data List tables -> kb/datalist/ (same source-of-truth rules)
    sys.exit(0 if build_datalist.main() else 1)
