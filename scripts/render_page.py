#!/usr/bin/env python3
"""Render a manual page (or one figure on it) to PNG so an agent can view it with the Read tool.

Usage:
  python scripts/render_page.py OM-023          # whole page  -> .cache/renders/OM-023.png
  python scripts/render_page.py OM-023 f1       # figure crop -> .cache/renders/OM-023-f1.png (sharper, fewer tokens)
  python scripts/render_page.py DL-078          # Data List page
  python scripts/render_page.py OM-014 --box 10,20,60,45   # zoom: x0,y0,x1,y1 in % of the page

Needs PyMuPDF. If the current interpreter lacks it, re-runs itself with the repo's .venv Python.
"""
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / ".cache" / "renders"
PDFS = {"OM": "DGX-670_owners_manual_En_D0.pdf", "RM": "DGX-670_reference_manual_En_B0.pdf",
        "DL": "dgx670_en_dl_b0.pdf"}
LONG_EDGE = 1560  # px; larger images are downscaled by the model anyway

try:
    import pymupdf
except ImportError:
    for venv_py in (ROOT / ".venv" / "Scripts" / "python.exe", ROOT / ".venv" / "bin" / "python"):
        if venv_py.exists() and Path(sys.executable).resolve() != venv_py.resolve():
            sys.exit(subprocess.call([str(venv_py), __file__, *sys.argv[1:]]))
    sys.exit("PyMuPDF missing: run  pip install -r requirements.txt  then retry.")


def figure_box(page_id, fig):
    """Figure bbox in page fractions, from the page file's figure_boxes frontmatter."""
    text = (ROOT / "kb" / "pages" / page_id[:2] / f"{page_id}.md").read_text(encoding="utf-8")
    m = re.search(rf"\b{fig} x(\d+)-(\d+)% y(\d+)-(\d+)%", text)
    if not m:
        sys.exit(f"{fig} not found in figure_boxes of {page_id}")
    x0, x1, y0, y1 = (int(v) / 100 for v in m.groups())
    px, py = 0.07, 0.04  # callout circles/leader lines usually sit just outside the image bbox
    return max(0, x0 - px), max(0, y0 - py), min(1, x1 + px), min(1, y1 + py)


def main():
    args = sys.argv[1:]
    box = None
    if "--box" in args:
        i = args.index("--box")
        box = tuple(int(v) / 100 for v in args[i + 1].split(","))
        del args[i:i + 2]
    if len(args) not in (1, 2) or not re.fullmatch(r"(OM|RM|DL)-\d{3}", args[0]) or (box and len(box) != 4):
        sys.exit(__doc__)
    page_id, fig = args[0], (args[1] if len(args) == 2 else None)
    doc = pymupdf.open(ROOT / "dgx_source_docs" / PDFS[page_id[:2]])
    page = doc[int(page_id[3:]) - 1]
    W, H = page.rect.width, page.rect.height
    clip, suffix = page.rect, ""
    if fig or box:
        fx0, fy0, fx1, fy1 = box or figure_box(page_id, fig)
        clip = pymupdf.Rect(fx0 * W, fy0 * H, fx1 * W, fy1 * H)
        suffix = f"-{fig}" if fig else "-box" + "_".join(str(round(v * 100)) for v in box)
    zoom = min(LONG_EDGE / max(clip.width, clip.height), 8)
    OUT.mkdir(parents=True, exist_ok=True)
    out = OUT / f"{page_id}{suffix}.png"
    page.get_pixmap(matrix=pymupdf.Matrix(zoom, zoom), clip=clip).save(out)
    print(os.path.relpath(out, ROOT).replace("\\", "/"))


if __name__ == "__main__":
    main()
