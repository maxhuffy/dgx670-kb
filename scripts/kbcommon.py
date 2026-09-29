"""Shared helpers (stdlib only, so they also run in cloud sessions without PyMuPDF)."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KB = ROOT / "kb"
MARKER_RE = re.compile(r"\[FIG ([A-Z]{2}-\d{3})-(f\d+)(?: — [^\]]*)?\]")
FIG_SECTION_RE = re.compile(r"^## (f\d+) — (.+?)\s*$", re.M)
SUMMARY_RE = re.compile(r"^summary:\s*(.+?)\s*$", re.M)


def figure_file(page_id):
    return KB / "figures" / f"{page_id}.md"


def cached_figure_titles(page_id):
    """{'f1': 'title', ...} from kb/figures/<page_id>.md, or None if not cached."""
    f = figure_file(page_id)
    if not f.exists():
        return None
    return dict(FIG_SECTION_RE.findall(f.read_text(encoding="utf-8")))


def mark_figures(text, page_id, titles):
    """Rewrite [FIG ...] markers so cached figures carry their title and a pointer."""
    def sub(m):
        fid = m.group(2)
        t = titles.get(fid)
        if not t:
            return f"[FIG {m.group(1)}-{fid}]"
        return f"[FIG {m.group(1)}-{fid} — {t}; see kb/figures/{page_id}.md#{fid}]"
    return MARKER_RE.sub(sub, text)


def page_path(page_id):
    return KB / "pages" / page_id[:2] / f"{page_id}.md"
