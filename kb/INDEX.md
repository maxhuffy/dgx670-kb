# DGX-670 Knowledge Base — Start Here

Source of truth: the PDFs in `dgx_source_docs/`. Everything in `kb/` is derived from them or cached from them.

## Where to look (in this order)
1. `../faq/INDEX.md` — answers the user already verified.
2. `maps/GLOSSARY.md` — everyday words → the manual's terms.
3. `maps/TERMS.md` — printed-index terms → page IDs (228 terms).
4. `maps/BUTTONS.md` — panel button → pages (50 buttons).
5. `maps/MENU_PATHS.md` — "how do I get to setting X" → exact button path (71 paths).
6. `maps/TOC.md` — bookmark tree + Owner's ↔ Reference Manual chapter join.
7. `pages/OM/OM-nnn.md`, `pages/RM/RM-nnn.md` — one file per PDF page (OM 120 pages, RM 93 pages).
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
