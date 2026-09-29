#!/usr/bin/env python3
"""Build the Data List knowledge base (kb/datalist/) from dgx670_en_dl_b0.pdf.

Every table becomes a tidy CSV (one self-contained fact per row, merged cells filled down, symbols
spelled out). The first columns of every CSV are `dl_page,table`, pointing back to the PDF page and the
table's position on it. Deterministic: same PDF in -> byte-identical files out.

Generated:  kb/datalist/csv/*.csv, kb/datalist/pages/DL-nnn.md, kb/datalist/INDEX.md, kb/datalist/CHECKS.md
Inputs it respects: scripts/datalist_briefs.md (hand-written table briefs), kb/datalist/ISSUES.md (never touched)

Usage:  python scripts/build_datalist.py            # build
        python scripts/build_datalist.py --dump 47  # debug: print the raw cell grid of DL page 47
"""
import collections
import csv
import io
import re
import sys
from pathlib import Path

import pymupdf

from kbcommon import KB, ROOT

sys.stdout.reconfigure(encoding="utf-8")

PDF = ROOT / "dgx_source_docs" / "dgx670_en_dl_b0.pdf"
PDF_NAME = PDF.name
OUT = KB / "datalist"
BRIEFS = ROOT / "scripts" / "datalist_briefs.md"

# Symbol fonts -> text. Calibrated against page renders (DL p.15, 21, 47, 79) and printed legends.
FONT_MAPS = [  # order matters: Wingdings2 before Wingdings
    ("Wingdings2", {"": "○", "": "×", "\x02": "○", "\x03": "×", "": " "}),
    ("Wingdings", {"": "●", "": "○", "": "→"}),
    ("MWspecial", {"U": "▲", "D": "▼", "L": "◀", "R": "▶", "K": "❚❚"}),
]
TEXT_FLAGS = pymupdf.TEXTFLAGS_DICT & ~pymupdf.TEXT_PRESERVE_LIGATURES


def map_text(font, text):
    base = font.split("+")[-1]
    for prefix, table in FONT_MAPS:
        if base.startswith(prefix):
            return "".join(table.get(c, c) for c in text)
    return text


def tidy(s):
    s = s.replace(" ", " ")
    s = re.sub(r"([A-G]) ♯", r"\1♯", s)       # "C ♯-1" -> "C♯-1"
    s = re.sub(r"[ \t]+", " ", s)
    return s.strip()


class Page:
    """A Data List page with font-mapped spans, for cell-level text lookup."""

    def __init__(self, doc, n):
        self.n = n
        self.page = doc[n - 1]
        self.spans = []  # (Rect, text, line_key)
        for b in self.page.get_text("dict", flags=TEXT_FLAGS)["blocks"]:
            for li, l in enumerate(b.get("lines", [])):
                for s in l["spans"]:
                    if s["text"]:
                        rot = l["dir"][1] < -0.5  # text rotated 90° (reads bottom→top), e.g. MegaVoice Map
                        self.spans.append((pymupdf.Rect(s["bbox"]), map_text(s["font"], s["text"]), rot))
        self._tables = None

    @property
    def tables(self):
        """Detected tables in reading order (left column top→bottom, then right column)."""
        if self._tables is None:
            mid = self.page.rect.width / 2
            tabs = self.page.find_tables().tables
            col = lambda t: 1 if t.bbox[0] >= mid - 10 else 0
            self._tables = sorted(tabs, key=lambda t: (col(t), round(t.bbox[1])))
        return self._tables

    def lines_in(self, rect):
        """Text lines (top→bottom) of spans whose centre lies in rect; spans on a line joined left→right."""
        hits = [h for h in self.spans if rect.contains(pymupdf.Point((h[0].x0 + h[0].x1) / 2, (h[0].y0 + h[0].y1) / 2))]
        return [t for _, t in self.positioned_lines(rect, hits)]

    def positioned_lines(self, rect, hits=None):
        """[(y, text)] for a rect. Spans separated by a visible gap are joined with a space."""
        if hits is None:
            hits = [h for h in self.spans if rect.contains(pymupdf.Point((h[0].x0 + h[0].x1) / 2, (h[0].y0 + h[0].y1) / 2))]
        rotated = bool(hits) and all(len(h) > 2 and h[2] for h in hits)
        # Normal text: lines stack along y, words run along x. Rotated text: lines stack along x,
        # words run bottom→top (so order by -y).
        across = (lambda r: r.x0) if rotated else (lambda r: r.y0)
        along = (lambda r: -r.y1) if rotated else (lambda r: r.x0)
        hits = sorted(hits, key=lambda h: (round(across(h[0])), along(h[0])))
        lines = []
        for r, t, *_ in hits:
            if lines and abs(lines[-1][0] - across(r)) < 3:
                lines[-1][1].append((r, t))
            else:
                lines.append([across(r), [(r, t)]])
        out = []
        for y, parts in lines:
            parts.sort(key=lambda p: along(p[0]))
            txt = parts[0][1]
            for (pr, pt), (r, t) in zip(parts, parts[1:]):
                dist = (pr.y0 - r.y1) if rotated else (r.x0 - pr.x1)
                gap = dist > 1.5 and not pt.endswith(" ") and not t.startswith(" ")
                txt += (" " if gap else "") + t
            txt = tidy(txt)
            if txt:
                out.append((y, txt))
        return out

    def line_rows(self, tb, row, split_first=None):
        """One output row per visual text line inside a ruled table row (for cells holding stacked lists).
        split_first: x offset; text in column 0 left of it goes to an extra leading 'label' column."""
        xs = sorted({round(c[0]) for r in tb.rows for c in r.cells if c} | {round(tb.bbox[2])})
        y0, y1 = row.bbox[1], row.bbox[3]
        cols = [self.positioned_lines(pymupdf.Rect(xs[i], y0, xs[i + 1], y1)) for i in range(len(xs) - 1)]
        if split_first is not None:
            left = self.positioned_lines(pymupdf.Rect(xs[0], y0, xs[0] + split_first, y1))
            right = self.positioned_lines(pymupdf.Rect(xs[0] + split_first, y0, xs[1], y1))
            cols = [left, right] + cols[1:]
        ys = []
        for c in cols:
            for y, _ in c:
                if not any(abs(y - v) < 3 for v in ys):
                    ys.append(y)
        ys.sort()
        return [[next((t for yy, t in c if abs(yy - y) < 3), "") for c in cols] for y in ys]

    def cell(self, rect):
        return tidy(" ".join(self.lines_in(pymupdf.Rect(rect)))) if rect else None

    def grid(self, tb, resolve=True):
        """Rows of cell texts. Slots covered by a merged cell take that cell's text (resolve=True) or None."""
        raw = [[self.cell(c) for c in row.cells] for row in tb.rows]
        if not resolve:
            return raw
        owners = [(pymupdf.Rect(c), self.cell(c)) for row in tb.rows for c in row.cells if c]
        xs = sorted({round(c[0]) for row in tb.rows for c in row.cells if c} | {round(tb.bbox[2])})
        out = []
        for r, row in enumerate(tb.rows):
            vals = []
            for c, cell in enumerate(row.cells):
                if cell is not None:
                    vals.append(raw[r][c])
                    continue
                x0, x1 = (xs[c], xs[c + 1]) if c + 1 < len(xs) else (xs[-1] - 2, xs[-1])
                # A row's bbox can be several visual rows tall when other columns merge downward;
                # its own shortest cell gives the true band.
                y1 = min((c[3] for c in row.cells if c), default=row.bbox[3])
                vals.append(owner_text(owners, pymupdf.Rect(x0, row.bbox[1], x1, y1)))
            out.append(vals)
        return out

    def fill_at(self, x, y):
        """Fill color (rounded RGB) of the smallest filled shape under a point, or None."""
        if not hasattr(self, "_fills"):
            self._fills = [(d["rect"], tuple(round(v, 2) for v in d["fill"]))
                           for d in self.page.get_drawings() if d.get("fill")]
        under = [(r.get_area(), f) for r, f in self._fills if r.contains(pymupdf.Point(x, y))]
        return min(under)[1] if under else None

    def text_below(self, tb):
        """Lines between the table and the page footer (footnotes/legends)."""
        r = pymupdf.Rect(0, tb.bbox[3], self.page.rect.width, self.page.rect.height)
        return [l for l in self.lines_in(r) if not re.match(r"DGX-670 Data List", l) and " / " not in l]

    def text_above(self, tb, height=30, min_width=0):
        """Lines just above a table. min_width widens narrow tables whose caption is wider than the grid."""
        x0, y0, x1, _ = tb.bbox
        return " / ".join(self.lines_in(pymupdf.Rect(x0 - 2, y0 - height, max(x1, x0 + min_width), y0)))


# --- Output model ----------------------------------------------------------------------

class Table:
    """One CSV. May gather rows from several PDF tables/pages; rows always start with dl_page, table."""

    def __init__(self, key, title, columns):
        self.key, self.title, self.columns = key, title, ["dl_page", "table"] + columns
        self.rows = []
        self.sources = collections.OrderedDict()  # (page, table_no) -> row count

    def add(self, page, table_no, values):
        values = ["" if v is None else v for v in values]
        assert len(values) == len(self.columns) - 2, (self.key, page, values)
        self.rows.append([page, table_no] + values)
        self.sources[(page, table_no)] = self.sources.get((page, table_no), 0) + 1

    @property
    def pages(self):
        return sorted({p for p, _ in self.sources})

    def csv_text(self):
        buf = io.StringIO()
        w = csv.writer(buf, lineterminator="\n")
        w.writerow(self.columns)
        w.writerows(self.rows)
        return buf.getvalue()


TABLES = collections.OrderedDict()
PAGE_NOTES = collections.defaultdict(list)  # page -> extra notes for the page file
CHECKS = []  # (name, expected, actual)
SOURCE_NOTES = []  # inconsistencies that are in the PDF itself (not extraction errors)


def table(key, title, columns):
    TABLES[key] = Table(key, title, columns)
    return TABLES[key]


def check(name, expected, actual):
    CHECKS.append((name, expected, actual))


def is_header(row, *labels):
    return any(c in labels for c in row if c)


# --- Family: simple ruled lists ------------------------------------------------------------

def extract_piano_types(doc):
    t = table("piano_types", "Piano Types in the Piano Room", ["voice_name"])
    pg = Page(doc, 2)
    lines = [l for l in pg.lines_in(pg.page.rect) if l]
    names = lines[lines.index("Voice Name") + 1:]
    for name in names:
        if re.fullmatch(r"\d+", name) or "Data List" in name or " / " in name:
            continue
        t.add(2, 1, [name])
    check("Piano Room piano types listed (CFX Grand … SweetDX)", 6, len(t.rows))


def extract_voices(doc):
    t = table("voices", "Voice List", ["section", "category", "voice_name", "msb", "lsb", "pc", "voice_type"])
    section = "Main"
    for n in range(3, 13):
        pg = Page(doc, n)
        for i, tb in enumerate(pg.tables, 1):
            above = pg.text_above(tb)
            if above.startswith("Category:"):
                section = above.split(":", 1)[1].strip()
            for row in pg.grid(tb):
                if is_header(row, "Category", "Sub Category", "MSB", "Voice Name"):
                    continue
                t.add(n, i, [section] + row)
    by_section = collections.Counter(r[2] for r in t.rows)
    # The spec's "601 Voices + 29 Drum/SFX Kits" = the panel sections Main + Legacy + MegaVoice
    # (GM & XG and GM2 are extra compatibility sets, not counted in the spec).
    panel = [r for r in t.rows if r[2] in ("Main", "Legacy", "MegaVoice")]
    kits = [r for r in panel if re.search(r"Drums|SFX", r[8])]
    check("Main+Legacy+MegaVoice voices excl. kits = 601 (OM p.106 spec)", 601, len(panel) - len(kits))
    check("Main+Legacy+MegaVoice Drum/SFX kits = 29 (OM p.106 spec)", 29, len(kits))
    types = collections.Counter(r[8] for r in panel)
    for vt, n in (("VRM", 9), ("S.Art!", 49), ("Natural!", 11), ("Sweet!", 26), ("Cool!", 53), ("Live!", 68),
                  ("MegaVoice", 23)):
        check(f"voices of type {vt} (OM p.106 spec)", n, types[vt])
    bad = [r for r in t.rows if not (r[5].isdigit() and r[6].isdigit() and r[7].isdigit())]
    check("every voice has numeric MSB/LSB/PC", 0, len(bad))


def extract_songs(doc):
    t = table("songs", "Song List", ["collection", "category", "title", "composer", "lyricist", "lyric_data"])
    for n in (21, 22):
        pg = Page(doc, n)
        band = pg.page.get_textbox(pymupdf.Rect(0, 40, pg.page.rect.width, 80))
        collection = next((l.strip() for l in band.splitlines() if re.match(r"\d+ \w", l.strip())), "")
        for i, tb in enumerate(pg.tables, 1):
            for row in pg.grid(tb):
                if is_header(row, "Category"):
                    continue
                if len(row) == 3:
                    row = row + ["", ""]
                t.add(n, i, [collection] + row)
    check("songs listed (50 Popular + 50 Classics)", 100, len(t.rows))


def extract_styles(doc):
    t = table("styles", "Style List", ["category", "style_name", "unison", "adaptive"])
    for n in (23, 24):
        pg = Page(doc, n)
        for i, tb in enumerate(pg.tables, 1):
            for row in pg.grid(tb):
                if not is_header(row, "Category", "Style Name"):
                    t.add(n, i, row)
    check("styles = 263 (OM p.106 spec)", 263, len(t.rows))


def extract_effect_types(doc):
    t = table("effect_types", "Effect Type List",
              ["block", "no", "category", "type_name", "description", "msb", "lsb", "parameter_list"])
    block = ""
    for n in range(25, 33):
        pg = Page(doc, n)
        for i, tb in enumerate(pg.tables, 1):
            above = pg.text_above(tb)
            if "Block" in above:
                block = next(s for s in above.split(" / ") if "Block" in s)
            for row in pg.grid(tb):
                if not is_header(row, "No.", "Type Name"):
                    t.add(n, i, [block] + row)
    for blk, rows in itertools_groupby(t.rows, lambda r: r[2]):
        nums = [int(r[3]) for r in rows if r[3].isdigit()]
        gaps = sorted(set(range(1, max(nums) + 1)) - set(nums)) if nums else ["no numbers"]
        check(f"{blk}: effect type No. 1..{max(nums or [0])} complete, no gaps", "no gaps", f"gaps {gaps}" if gaps else "no gaps")


def itertools_groupby(rows, key):
    groups = collections.OrderedDict()
    for r in rows:
        groups.setdefault(key(r), []).append(r)
    return groups.items()


def extract_direct_access(doc):
    t = table("direct_access", "Direct Access Chart",
              ["group", "control", "function_1", "function_2", "function_3", "function_4"])
    pg = Page(doc, 78)
    for i, tb in enumerate(pg.tables, 1):
        for row in pg.grid(tb):
            if row[0] and row[0].startswith("Operation"):
                continue
            if row[0] == row[1]:
                row[1] = ""  # one button cell spans the group and control columns
            t.add(78, i, row)


# --- Family: symbol grids -----------------------------------------------------------------

LIGHT, DARK = (0.8, 0.8, 0.8), (0.6, 0.6, 0.6)  # drum list: "Same as Standard Kit 1" / "No Sound" (legend)


def extract_drum_kits(doc):
    t = table("drum_kits", "Drum/Key Assignment List",
              ["kit", "msb", "lsb", "pc", "drum_tutor", "note_no", "midi_note", "keyboard_note", "sound",
               "alt_group", "key_off", "status"])
    std = {}
    kits_seen, silent = [], collections.Counter()
    for n in range(15, 21):
        pg = Page(doc, n)
        tb = pg.tables[0]
        grid = pg.grid(tb)
        PAGE_NOTES[n] += ["Legend swatches (graphics, decoded from the page render): light grey cell = Same as "
                          "Standard Kit 1; dark grey cell = No Sound."] + pg.text_below(tb)
        kit_cols = range(3, len(grid[0]), 3)
        for r in range(4, len(grid)):
            row = grid[r]
            note_no, midi_note, key_note = row[0], row[1], row[2]
            for c in kit_cols:
                kit = grid[0][c]
                if r == 4:
                    kits_seen.append(kit)
                msb, lsb, pc = grid[1][c].split("-")
                cell = tb.rows[r].cells[c]
                fill = pg.fill_at((cell[0] + cell[2]) / 2, (cell[1] + cell[3]) / 2) if cell else None
                sound, alt, off = row[c], row[c + 1], row[c + 2]
                if kit == "StandardKit1":
                    std[note_no] = (sound, alt, off)
                if fill == DARK or (not sound and fill != LIGHT):
                    silent[kit] += 1
                    continue
                if fill == LIGHT:
                    status = "same as StandardKit1"
                    if not sound:
                        sound, alt, off = std.get(note_no, ("", "", ""))
                else:
                    status = "kit-specific"
                t.add(n, 1, [kit, msb, lsb, pc, "yes" if grid[2][c] == "○" else "", note_no, midi_note, key_note,
                             sound, alt, "yes" if off == "●" else "", status])
    check("drum/SFX kits in Drum/Key list = 29 (OM p.106 spec)", 29, len(kits_seen))
    voice_by_num = {(r[5], r[6], r[7]): r[4] for r in TABLES["voices"].rows if re.search(r"Drums|SFX", r[8])}
    kits = {(r[2], r[3], r[4], r[5]) for r in t.rows}
    missing = sorted(k[0] for k in kits if k[1:] not in voice_by_num)
    check("every kit's MSB-LSB-PC also appears as a Drum/SFX voice in voices.csv", "[]", str(missing))
    for name, *num in sorted(kits):
        vname = voice_by_num.get(tuple(num))
        if vname and vname != name:
            SOURCE_NOTES.append(f"Kit {'-'.join(num)} is printed as \"{vname}\" in the Voice List but "
                                f"\"{name}\" in the Drum/Key Assignment List (same kit).")
    notes = [r[7] for r in t.rows]
    check("drum note numbers within 13..91", "yes", "yes" if all(13 <= int(x) <= 91 for x in notes) else "no")
    same_diff = [r for r in t.rows if r[13] == "same as StandardKit1" and std.get(r[7], ("",))[0] != r[10]]
    check("light-grey cells really equal StandardKit1 sound", 0, len(same_diff))


def extract_parameter_chart(doc):
    cols = ["backup_restore", "setup_files_system_setup", "setup_files_midi_setup", "setup_files_user_effect",
            "voice_set", "voice_set_filter_group", "midi_song_file", "song_creator_setup_group", "style_file",
            "style_ots", "registration_memory", "registration_memory_freeze_group", "parameter_lock_group", "note"]
    t = table("parameter_chart", "Parameter Chart", ["group", "subgroup", "parameter"] + cols)
    group = subgroup = ""
    for n in range(47, 57):
        pg = Page(doc, n)
        tb = pg.tables[0]
        grid = pg.grid(tb)
        PAGE_NOTES[n] += pg.text_below(tb)
        for r, row in enumerate(grid):
            if row[0] == "Parameter":
                continue
            vals = [v for v in row[:-1] if v]
            if vals and len(set(vals)) == 1 and len(vals) >= 10:  # full-width group bar
                cell = tb.rows[r].cells[0] or tb.bbox
                fill = pg.fill_at(cell[0] + 3, (tb.rows[r].bbox[1] + tb.rows[r].bbox[3]) / 2)
                if fill == (0.0, 0.0, 0.0):
                    group, subgroup = vals[0], ""
                else:
                    subgroup = vals[0]
                continue
            t.add(n, 1, [group, subgroup] + row)
    bad = [r for r in t.rows if not all(v in ("○", "×", "–", "") or v.startswith("○") for v in r[5:9])]
    check("parameter chart file columns hold only ○/×/– marks", 0, len(bad))


def extract_midi_impl_chart(doc):
    t = table("midi_impl_chart", "MIDI Implementation Chart",
              ["block", "function", "transmitted", "recognized", "remarks"])
    pg = Page(doc, 79)
    tb = pg.tables[0]
    for row in tb.rows[2:]:
        lines = pg.line_rows(tb, row)
        if lines and lines[0][0].startswith("Notes:"):
            PAGE_NOTES[79] += [" ".join(v for v in l if v) for l in lines]
            continue
        block = " ".join(l[0] for l in lines if l[0])
        if not block:  # legend lines under the chart (Mode 1–4, ○ : Yes, × : No)
            PAGE_NOTES[79] += [" ".join(v for v in l if v) for l in lines]
            continue
        for l in lines:
            t.add(79, 1, [block] + l)
    PAGE_NOTES[79].insert(0, "Chart header: Yamaha [ Portable Grand ] Model DGX-670 MIDI Implementation Chart, "
                             "Date: 1-April-2020, Version: 1.0")


# --- Family: stacked lists and lookup tables ----------------------------------------------

def column_stream(pg):
    """Per page column: outside-table text lines and tables, merged in y order -> [(kind, y, payload)]."""
    mid = pg.page.rect.width / 2
    stream = []
    for x0, x1 in ((0, mid), (mid, pg.page.rect.width)):
        col_tabs = [tb for tb in pg.tables if x0 - 10 <= tb.bbox[0] < x1 - 10]
        inside = lambda r: any(pymupdf.Rect(tb.bbox).contains(r) for tb in pg.tables)
        spans = [h for h in pg.spans if x0 <= h[0].x0 < x1 and not inside(h[0])
                 and 40 < h[0].y0 < pg.page.rect.height - 40]
        items = [("line", y, t) for y, t in pg.positioned_lines(None, spans)]
        items += [("table", tb.bbox[1], tb) for tb in col_tabs]
        stream += sorted(items, key=lambda it: it[1])
    return stream


def extract_effect_params(doc):
    t = table("effect_params", "Effect Parameter List",
              ["parameter_list", "blocks", "no", "parameter", "display", "min", "max", "value_table", "control_ac1"])
    names = []
    for n in range(33, 45):
        pg = Page(doc, n)
        name = blocks = ""
        tno = 0
        for kind, _, item in column_stream(pg):
            if kind == "line":
                if item.startswith("Block:"):
                    blocks = item.split(":", 1)[1].strip()
                elif item.startswith("Note:") and "No parameters" in item:
                    t.add(n, 0, [name, blocks, "", "(no parameters)", "", "", "", "", ""])
                    names.append(name)
                elif item.startswith(("•", "(*")) or "par" in item.lower() and "efectos" in item.lower():
                    PAGE_NOTES[n].append(item) if item.startswith(("•", "(*")) else None
                elif re.fullmatch(r"[A-Z0-9][A-Z0-9 &/+.\-]*", item):
                    name, blocks = item, ""
                continue
            tno += 1
            names.append(name)
            last_no = last_param = ""
            for line in pg.line_rows(item, item.rows[1]):
                no, param, disp, lo, hi, vt, ctl = line
                if no and not param and not disp:
                    continue  # unused parameter slot
                if not no and disp:  # continuation line: alternative range for the same parameter
                    no, param = last_no, last_param
                last_no, last_param = no, param
                t.add(n, tno, [name, blocks, no, param, disp, lo, hi, vt, "yes" if ctl == "●" else ""])
    check("every effect parameter list has a name", 0, sum(1 for x in names if not x))
    used = {r[9] for r in TABLES["effect_types"].rows}
    missing = sorted(used - set(names) - {""})
    check("every Parameter List named in effect_types.csv exists in effect_params.csv", "[]", str(missing))


def extract_effect_data_tables(doc):
    t = table("effect_data_tables", "Effect Data Assign Table", ["value_table", "title", "data", "value"])
    seen = []
    for n in (45, 46):
        pg = Page(doc, n)
        for i, tb in enumerate(pg.tables, 1):
            above = pg.text_above(tb, 25, min_width=115).split(" / ")
            k = next((j for j, a in enumerate(above) if a.startswith("Table #")), None)
            tno = above[k] if k is not None else ""
            title = " / ".join(above[k + 1:]) if k is not None else ""
            seen.append(tno)
            for row in pg.grid(tb):
                if row[0] == "Data":
                    continue
                # Rows are strict Data/Value pairs. Pair tokens in x order rather than trusting detected
                # cell borders, which drift on some tables (e.g. Table #14 put "68" in a Value cell).
                text = " ".join(c for c in row if c)
                pairs = re.findall(r"(\d+) (\S+(?: \([^)]*\))?)", text)  # value may carry "(20k)" etc.
                if " ".join(f"{d} {v}" for d, v in pairs) != text:
                    check(f"{tno} row parses as Data/Value pairs (DL p.{n})", "clean pairs", text)
                for d, v in pairs:
                    t.add(n, i, [tno, title, d, v])
    check("every Effect Data Assign table has a 'Table #n' label", 0, seen.count(""))
    gaps = []
    for tno in seen:
        data = sorted(int(r[4]) for r in t.rows if r[2] == tno)
        if data != list(range(data[0], data[0] + len(data))):
            gaps.append(tno)
    check("each value table's Data column is contiguous with no duplicates", "[]", str(gaps))
    refs = {r[9] for r in TABLES["effect_params"].rows if r[9]}
    check("every value table referenced by effect_params.csv exists", "[]", str(sorted(refs - set(seen))))


def extract_number_bases(doc):
    t = table("number_bases", "Decimal / Hexadecimal / Binary conversion (MIDI Data Format)",
              ["decimal", "hexadecimal", "binary"])
    pg = Page(doc, 57)
    tb = pg.tables[0]
    for row in pg.grid(tb):
        for c in range(0, len(row), 4):
            if row[c].isdigit():
                t.add(57, 1, row[c:c + 3])
    ok = sorted(int(r[2]) for r in t.rows) == list(range(128))
    check("number base table covers decimal 0..127 exactly once", "yes", "yes" if ok else "no")


# --- Family: irregular (rotated) grid -------------------------------------------------------

def extract_megavoice_map(doc):
    """DL p.13–14 are printed rotated 90°: in PDF coordinates each table row is one velocity layer (or
    key range) and each voice occupies a column pair (velocity range, sound)."""
    t = table("megavoice_map", "MegaVoice Map",
              ["voice_name", "element", "msb", "lsb", "pc", "key_range", "velocity", "sound"])
    mega = {(r[5], r[6], r[7]): r[4] for r in TABLES["voices"].rows if r[2] == "MegaVoice"}
    found = set()
    for n in (13, 14):
        pg = Page(doc, n)
        tb = pg.tables[0]
        grid = pg.grid(tb)
        label = {}
        for row in grid:
            for key, pat in (("Voice", r"^Voice Name$"), ("PC", r"PC#"), ("LSB", r"^LSB$"), ("MSB", r"^MSB$")):
                if re.search(pat, row[0]):
                    label[key] = row
        layers = [row for row in grid if row[0].startswith(("C8", "C6", "Velocity"))]
        pairs = list(range(1, len(grid[0]) - 1, 2))
        prev_num, element_idx = None, 0
        for c in pairs:
            num = (label["MSB"][c], label["LSB"][c], label["PC"][c])
            if not all(x.isdigit() for x in num):
                continue
            element_idx = element_idx + 1 if num == prev_num else 0
            prev_num = num
            printed = label["Voice"][c]
            elements = re.findall(r"Element\d\([^)]*\)", printed)
            element = elements[element_idx] if elements else ""
            name = mega.get(num, printed)
            found.add(num)
            seen = set()
            for row in layers:
                vel, sound = row[c], row[c + 1]
                if elements and row[0].startswith(("C8", "C6")):
                    if element_idx:
                        continue
                    vel, sound = row[c], row[c + 2]  # one cell pair spans both elements
                    if (row[0], vel, sound) in seen:
                        continue
                    seen.add((row[0], vel, sound))
                    t.add(n, 1, [name, "both elements"] + list(num) + [row[0], vel, sound])
                    continue
                if not vel and not sound:
                    continue
                key = "B5 and lower" if row[0].startswith("Velocity") else row[0]
                if (key, vel, sound) in seen:
                    continue  # merged cell repeated over several layer rows
                seen.add((key, vel, sound))
                t.add(n, 1, [name, element] + list(num) + [key, vel, sound])
    check("MegaVoice Map covers all 23 MegaVoices of voices.csv", 23, len(found & set(mega)))
    check("MegaVoice Map voices all exist in voices.csv", "[]", str(sorted(found - set(mega))))


# --- Family: MIDI Data Format (wide tables with multi-level headers) -----------------------------

MIDI_KINDS = [  # first header cell -> csv key, title
    ("MIDI Events", "midi_channel_messages", "MIDI Data Format: Channel Messages"),
    ("NRPN", "midi_nrpn_rpn", "MIDI Data Format: NRPN / RPN"),
    ("Address (H)", "midi_parameter_change", "MIDI Data Format: MIDI Parameter Change Tables"),
    ("MIDI Event", "midi_sysex_messages", "MIDI Data Format: System Exclusive Messages"),
    ("Data Format", "song_sysex_and_meta", "Song System Exclusive Message List / Song Meta Event List"),
]
SONG_SUBHEADS = {"Guide", "Score", "Style", "Yamaha Meta Event", "Yamaha XF Meta Event"}
SECTION_RE = re.compile(r"^(MIDI CHANNEL MESSAGE.*|NRPN \(.*|RPN \(.*|MIDI Parameter Change Table.*|"
                        r"System Exclusive Messages.*|Song .*List.*|[A-Z][a-z]+( [A-Za-z]+)?)$")


# Unique column names, calibrated from the printed two-level header (render of DL p.61). Header text
# alone can't be used: labels like "Song", "Style" and "Address (H)" repeat across columns.
MIDI_FLAGS = ["Voice › Regular/Drum/Natural", "Voice › Mic", "MIDI Reception › Song",
              "MIDI Reception › Main/Layer/Left", "MIDI Reception › Keyboard", "MIDI Reception › Style",
              "MIDI Reception › Extra", "MIDI Transmission › Main/Layer/Left", "MIDI Transmission › Style",
              "MIDI Transmission › Song", "MIDI Transmission › Upper Lower", "PLAY › PLAY", "PLAY › REW",
              "REC › From panel (Main/Layer/Left)"]
MIDI_LEAD = {
    "midi_channel_messages": ["MIDI Event", "Status byte", "1st Data byte", "1st Data byte (Hex)", "1st Data parameter",
                              "2nd Data byte", "2nd Data byte (Hex)", "2nd Data parameter"],
    "midi_nrpn_rpn": ["NRPN/RPN MSB", "NRPN/RPN LSB", "Data Entry MSB", "Data Entry LSB", "Parameter", "Data Range"],
    "midi_parameter_change": ["Address (H) high", "Address (H) mid", "Address (H) low", "Size (H)", "Data (H)",
                              "Parameter", "Description", "XG Default (H)"],
    "midi_sysex_messages": ["MIDI Event", "Data Format"],
    "song_sysex_and_meta": ["Data Format", "Parameter", "Description", "Note"],
}


def midi_column_names(key, ncols):
    lead = MIDI_LEAD[key]
    flags = ncols - len(lead)
    assert flags in (0, 11, 14), (key, ncols)
    return lead + MIDI_FLAGS[:flags]


def owner_text(cells, slot):
    """Text of the cell covering most of a slot (first-hit point tests picked neighbouring rows' cells)."""
    slot = pymupdf.Rect(slot.x0 + 1, slot.y0 + 1, slot.x1 - 1, slot.y1 - 1)
    best = max(((rect & slot).get_area(), t) for rect, t in cells) if cells else (0, "")
    return best[1] if best[0] > 0 else ""


def column_xs(tb):
    return sorted({round(c[0]) for r in tb.rows for c in r.cells if c} | {round(tb.bbox[2])})


def grid_on(pg, tb, xs):
    """Cell texts sampled at another table's column centres: merged cells spread over every column they cover."""
    cells = [(pymupdf.Rect(c), pg.cell(c)) for r in tb.rows for c in r.cells if c]
    return [[owner_text(cells, pymupdf.Rect(a, row.bbox[1], b, row.bbox[3])) for a, b in zip(xs, xs[1:])]
            for row in tb.rows]


def extract_midi(doc):
    collected = collections.OrderedDict((k, []) for _, k, _ in MIDI_KINDS)  # key -> [(page, tno, dict)]
    columns = collections.OrderedDict((k, []) for _, k, _ in MIDI_KINDS)
    current = None  # (key, names, xs)
    section = ""
    fill = {}
    song_sub, prev_song_page = "", None
    for n in range(58, 78):
        pg = Page(doc, n)
        table_boxes = [pymupdf.Rect(tb.bbox) for tb in pg.tables]
        outside = [h for h in pg.spans if not any(b.contains(h[0]) for b in table_boxes)
                   and 40 < h[0].y0 < pg.page.rect.height - 40]
        for tno, tb in enumerate(sorted(pg.tables, key=lambda t: t.bbox[1]), 1):
            above = [l for l in pg.text_above(tb, 40).split(" / ") if l]
            heads = [l for l in above if re.match(r"(MIDI CHANNEL MESSAGE|NRPN \(|RPN \(|MIDI Parameter Change "
                                                    r"Table|System Exclusive Messages)", l)]
            if heads:
                section = heads[-1]
            grid = pg.grid(tb)
            kind = next(((key, title) for first, key, title in MIDI_KINDS if grid[0][0] == first
                         or (len(grid) > 1 and grid[1][0] == first)), None)
            if kind:
                h = 0
                while h < len(grid) and (grid[h][0] in [f for f, _, _ in MIDI_KINDS] + ["MSB"]
                                         or grid[h][0].startswith("[MIDI]")):
                    h += 1
                names = midi_column_names(kind[0], len(grid[0]))
                current = (kind[0], names, column_xs(tb))
                rows = grid[h:]
            elif current and len(grid[0]) != len(current[1]):
                rows = grid_on(pg, tb, current[2])  # header-less continuation with merged flag columns
            elif current:
                rows = grid
            else:
                continue
            key, names, _ = current
            if key == "song_sysex_and_meta":
                sub = next((l for l in reversed(above) if l in SONG_SUBHEADS), None)
                song_sub = sub or (song_sub if n == prev_song_page else "")
                prev_song_page = n
                base = "Song Meta Event List" if n == 77 else "Song System Exclusive Message List"
                section = f"{base} › {song_sub}" if song_sub else base
            for c in names:
                if c not in columns[key]:
                    columns[key].append(c)
            if section != fill.get("_section"):
                fill = {"_section": section}  # address bytes carry across continuation tables of a section
            for row in rows:
                if not any(row):
                    continue
                d = dict(zip(names, row))
                if key == "midi_parameter_change":  # blank high/mid address = same as the row above
                    for c in names[:2]:
                        d[c] = d[c] or fill.get(c, "")
                        fill[c] = d[c]
                collected[key].append((n, tno, section, d))
        notes = [t for _, t in pg.positioned_lines(None, outside)]
        PAGE_NOTES[n] += [l for l in notes if " / " not in l and not l.startswith("DGX-670 Data List")]
    for _, key, title in MIDI_KINDS:
        t = table(key, title, ["section"] + columns[key])
        for n, tno, sec, d in collected[key]:
            t.add(n, tno, [sec] + [d.get(c, "") for c in columns[key]])
    total = sum(len(v) for v in collected.values())
    check("MIDI Data Format tables yield rows for every layout", "all > 0",
          "all > 0" if all(collected.values()) else str({k: len(v) for k, v in collected.items()}))
    check("MIDI rows extracted (sanity: > 300)", "yes", "yes" if total > 300 else f"only {total}")


def dump(n):
    doc = pymupdf.open(PDF)
    pg = Page(doc, n)
    for i, tb in enumerate(pg.tables):
        print(f"--- table {i + 1} bbox={[round(v) for v in tb.bbox]} {tb.row_count}x{tb.col_count} above={pg.text_above(tb)!r}")
        for r in pg.grid(tb):
            print("   ", " | ".join("∅" if c is None else c[:26] for c in r))


if __name__ == "__main__" and "--dump" in sys.argv:
    for a in sys.argv[sys.argv.index("--dump") + 1:]:
        dump(int(a))
    sys.exit()


# --- Main -----------------------------------------------------------------------------

EXTRACTORS = [extract_piano_types, extract_voices, extract_songs, extract_styles, extract_effect_types,
              extract_direct_access, extract_drum_kits, extract_parameter_chart, extract_midi_impl_chart,
              extract_effect_params, extract_effect_data_tables, extract_number_bases,
              extract_megavoice_map, extract_midi]


# Visual verification actually performed (page renders compared row-by-row against the CSV).
VERIFIED = {
    "voices": "DL p.3 rows 1–25 compared to render; Main+Legacy+MegaVoice counts match OM p.106 spec exactly",
    "songs": "DL p.21 heading and first rows compared to render",
    "drum_kits": "DL p.15 and p.20 compared to render; shading legend decoded (light grey = Same as Standard Kit 1, "
                 "dark grey = No Sound)",
    "megavoice_map": "DL p.13 compared to render (rotated table, 12StringGuitar elements)",
    "effect_params": "DL p.33 (REAL REVERB, REVERB1) compared to render",
    "effect_data_tables": "DL p.46 compared to render (Tables #14, #17, #18, #20, #22, #28)",
    "parameter_chart": "DL p.47 compared to render; ○/× glyphs decoded from it",
    "midi_impl_chart": "DL p.79 compared to render; ○/× legend printed on the chart",
    "midi_parameter_change": "DL p.61 header and p.64 continuation tables compared to render",
    "direct_access": "two independent methods agree on all 59 rows: this text extraction and an earlier image "
                     "transcription of DL p.78",
}


def write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists() or path.read_text(encoding="utf-8") != content:
        path.write_text(content, encoding="utf-8", newline="\n")


def load_briefs():
    if not BRIEFS.exists():
        return {}
    text = BRIEFS.read_text(encoding="utf-8")
    return {m.group(1): m.group(2).strip() for m in re.finditer(r"^## (\w+)\n(.*?)(?=^## |\Z)", text, re.M | re.S)}


def page_range(pages):
    return f"p.{pages[0]}" + (f"–{pages[-1]}" if pages[-1] != pages[0] else "")


def page_titles(doc):
    """English section title per page, from the running footer ("Voice List / Voice-Liste / …")."""
    titles = {}
    for n in range(1, doc.page_count + 1):
        pg = Page(doc, n)
        band = pymupdf.Rect(0, pg.page.rect.height - 40, pg.page.rect.width, pg.page.rect.height)
        foot = [l for l in pg.lines_in(band) if " / " in l]
        titles[n] = foot[0].split(" / ")[0].strip() if foot else ""
    return titles


def render_pages(doc, titles):
    by_page = collections.defaultdict(list)
    for t in TABLES.values():
        for (pg, tno), count in t.sources.items():
            by_page[pg].append((t, tno, count))
    for n in range(2, doc.page_count + 1):
        lines = [
            "---", f"id: DL-{n:03d}", f"doc: Data List ({PDF_NAME})", f"page: {n}", f"section: {titles[n]}",
            f"csv: [{', '.join(sorted({t.key for t, _, _ in by_page[n]}))}]", "---",
            f"# DL p.{n} — {titles[n]}", "",
            f"Source: `dgx_source_docs/{PDF_NAME}` page {n}. View it: `python scripts/render_page.py DL-{n:03d}`. "
            f"Cite as [DL p.{n}].", "", "## Data on this page",
        ]
        for t, tno, count in by_page[n]:
            pos = "text outside a ruled table" if tno == 0 else f"table {tno} on the page"
            lines.append(f"- `kb/datalist/csv/{t.key}.csv` — {t.title}: {count} rows ({pos}; filter `dl_page={n}`)")
        if not by_page[n]:
            lines.append("- (no tabular data)")
        notes = list(dict.fromkeys(x for x in PAGE_NOTES.get(n, []) if x.strip()))
        if notes:
            lines += ["", "## Notes and legends printed on this page (verbatim)"] + [f"- {x}" for x in notes]
        write(OUT / "pages" / f"DL-{n:03d}.md", "\n".join(lines) + "\n")


def render_index(briefs):
    failed = [c for c in CHECKS if str(c[1]) != str(c[2])]
    lines = [
        "# Data List — Table Index",
        "",
        f"Every table in `dgx_source_docs/{PDF_NAME}` (79 pages) as a CSV in `csv/`, with a brief for search.",
        "Generated by `scripts/build_datalist.py`. Briefs come from `scripts/datalist_briefs.md`.",
        "",
        "## How to use",
        "- Search these briefs to find which table can answer a question, then `grep -i` the CSV. The first",
        "  line of each CSV is its header.",
        "- Every CSV row starts with `dl_page,table`. Cite it as [DL p.<dl_page>]. `pages/DL-nnn.md` holds each page's",
        "  printed notes and legends. `python scripts/render_page.py DL-nnn` shows the original page.",
        "- Conventions: merged cells are repeated on every row they cover. Symbols are kept as printed (○ ● × – ▲▼◀▶).",
        "  ○ = yes/available, × = no, ● = see that table's legend, – = not applicable.",
        "- Suspected errors: check the page render, then log them in `ISSUES.md` (hand-maintained).",
        f"- Build checks: {len(CHECKS) - len(failed)}/{len(CHECKS)} passed (see `CHECKS.md`).",
        "",
        "## Tables",
    ]
    for t in TABLES.values():
        lines += [
            "", f"### {t.key} — {t.title} (DL {page_range(t.pages)})",
            f"- File: `csv/{t.key}.csv` · {len(t.rows)} rows · columns: {', '.join(t.columns[2:])}",
            "- Verification: automated checks"
            + (f"; visual: {VERIFIED[t.key]}" if t.key in VERIFIED else " only (no visual spot-check)"),
            "", briefs.get(t.key, "_(brief missing)_"),
        ]
    if SOURCE_NOTES:
        lines += ["", "## Source notes (inconsistencies in the PDF itself, not extraction errors)"]
        lines += [f"- {x}" for x in SOURCE_NOTES]
    return "\n".join(lines) + "\n"


def render_checks():
    lines = ["# Data List build checks", "", "Automated checks run by `scripts/build_datalist.py` on every build.", "",
             "| Result | Check | Expected | Got |", "|---|---|---|---|"]
    for name, exp, act in CHECKS:
        lines.append(f"| {'ok' if str(exp) == str(act) else 'FAIL'} | {name} | {exp} | {act} |".replace("\n", " "))
    return "\n".join(lines) + "\n"


ISSUES_SEED = """# Data List issues

Suspected discrepancies between a CSV and its PDF page. Hand-maintained; the build never overwrites this file.
Add a row with: date, CSV + row, DL page, what the page actually shows, status.

| Date | CSV / row | DL page | Finding | Status |
|---|---|---|---|---|
"""


def main():
    doc = pymupdf.open(PDF)
    for fn in EXTRACTORS:
        fn(doc)
    SOURCE_NOTES.append("Effect Data Assign value tables are numbered up to #40, but only 22 are printed "
                        "(#1–9, 11–14, 17–20, 22, 28, 29, 39, 40). Every table the Effect Parameter List "
                        "references is among them.")
    briefs = load_briefs()
    check("every CSV has a brief in scripts/datalist_briefs.md", "[]", str([k for k in TABLES if k not in briefs]))
    for t in TABLES.values():
        write(OUT / "csv" / f"{t.key}.csv", t.csv_text())
    render_pages(doc, page_titles(doc))
    write(OUT / "INDEX.md", render_index(briefs))
    write(OUT / "CHECKS.md", render_checks())
    if not (OUT / "ISSUES.md").exists():
        write(OUT / "ISSUES.md", ISSUES_SEED)
    failed = [c for c in CHECKS if str(c[1]) != str(c[2])]
    for name, exp, act in failed:
        print(f"  FAIL {name}: expected {exp}, got {act}")
    print(f"datalist: {len(TABLES)} tables | {sum(len(t.rows) for t in TABLES.values())} rows | "
          f"checks {len(CHECKS) - len(failed)}/{len(CHECKS)} passed")
    return not failed


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
