#!/usr/bin/env python3
"""Consistency checks for the knowledge base. Stdlib only. Exit code 1 on any failure.

Usage:  python scripts/check_kb.py
"""
import re
import sys

from kbcommon import KB, ROOT, cached_figure_titles
from register import ROW_KEY_RE

sys.stdout.reconfigure(encoding="utf-8")

# Figure markers counted in Yamaha's supplied text export (build-time calibration reference).
REFERENCE_FIGURES = {"OM": 144, "RM": 104}
FIGURE_TOLERANCE = 0.25
BAD_CHARS = re.compile(r"[-�\x00-\x08\x0b-\x1f]")

errors = []


def fail(msg):
    errors.append(msg)


def fm(text, name):
    m = re.search(rf"^{name}: ?(.*)$", text, re.M)
    return m.group(1).strip() if m else None


def ids(value):
    return re.findall(r"[A-Z]{2}-\d{3}(?:-f\d+)?", value or "")


def index_keys(index_file):
    return {m.group(1) for m in ROW_KEY_RE.finditer(index_file.read_text(encoding="utf-8"))}


pages = {p.stem: p.read_text(encoding="utf-8") for p in sorted((KB / "pages").glob("*/*.md"))}
if not pages:
    fail("no page files under kb/pages — run scripts/build_kb.py")

fig_count = {"OM": 0, "RM": 0}
for pid, text in pages.items():
    if BAD_CHARS.search(text):
        fail(f"{pid}: unmapped glyph/control char {BAD_CHARS.search(text).group(0)!r}")
    role = fm(text, "role")
    if role == "content" and not fm(text, "section"):
        fail(f"{pid}: content page without a section")
    for ref in ids(fm(text, "links_out")) + ids(fm(text, "links_in")):
        if ref not in pages:
            fail(f"{pid}: link to missing page {ref}")
    figs = ids(fm(text, "figures"))
    fig_count[pid[:2]] += len(figs)
    markers = re.findall(r"\[FIG ([A-Z]{2}-\d{3}-f\d+)", text)
    if sorted(markers) != sorted(figs):
        fail(f"{pid}: figure markers {markers} != frontmatter {figs}")
    cache = fm(text, "figure_cache")
    titles = cached_figure_titles(pid)
    if (cache == "done") != (titles is not None):
        fail(f"{pid}: figure_cache={cache} but kb/figures/{pid}.md {'exists' if titles is not None else 'missing'}")
    if titles is not None:
        missing = [f for f in figs if f.split("-")[-1] not in titles]
        if missing:
            fail(f"{pid}: kb/figures/{pid}.md lacks sections for {missing}")
        for f in figs:
            if f"[FIG {f} — " not in text and f.split("-")[-1] in titles:
                fail(f"{pid}: marker {f} not updated with its cached title (run scripts/register.py figure {pid})")

for doc, ref in REFERENCE_FIGURES.items():
    if abs(fig_count[doc] - ref) > ref * FIGURE_TOLERANCE:
        fail(f"{doc}: detected {fig_count[doc]} figures vs reference {ref} (>{FIGURE_TOLERANCE:.0%} off)")

# Cache indexes <-> files
for folder, pattern in ((KB / "figures", "[A-Z][A-Z]-[0-9][0-9][0-9].md"),
                        (KB / "datalist", "DL-[0-9][0-9][0-9].md"),
                        (ROOT / "faq", "*.md")):
    index = folder / "INDEX.md"
    if not index.exists():
        fail(f"missing {index.relative_to(ROOT)}")
        continue
    files = {p.stem for p in folder.glob(pattern) if p.name != "INDEX.md"}
    rows = index_keys(index)
    for k in sorted(files - rows):
        fail(f"{folder.name}/{k}.md is not in {folder.name}/INDEX.md (run scripts/register.py)")
    for k in sorted(rows - files):
        fail(f"{folder.name}/INDEX.md lists {k} but the file is missing")

for f in sorted((ROOT / "faq").glob("*.md")):
    if f.name != "INDEX.md" and not re.search(r"\[(OM|RM|DL) p\.\d+", f.read_text(encoding="utf-8")):
        fail(f"faq/{f.name}: no citation")

for name in ("INDEX.md", "maps/TOC.md", "maps/TERMS.md", "maps/BUTTONS.md", "maps/MENU_PATHS.md",
             "maps/DATALIST_TOC.md", "maps/GLOSSARY.md"):
    if not (KB / name).exists():
        fail(f"missing kb/{name}")

cached = sum(1 for t in pages.values() if fm(t, "figure_cache") == "done")
pending = sum(1 for t in pages.values() if fm(t, "figure_cache") == "none")
print(f"pages {len(pages)} | figures OM {fig_count['OM']} (ref {REFERENCE_FIGURES['OM']}), "
      f"RM {fig_count['RM']} (ref {REFERENCE_FIGURES['RM']}) | figure pages cached {cached}, pending {pending}")
if errors:
    print(f"FAILED ({len(errors)}):")
    for e in errors[:50]:
        print("  -", e)
    sys.exit(1)
print("OK")
