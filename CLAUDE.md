# DGX-670 Knowledge Base

A cited, growing knowledge base for the **Yamaha DGX-670** keyboard, built from the PDFs in `dgx_source_docs/`
(Owner's Manual = OM, Reference Manual = RM, Data List = DL). Every DGX-670 question is answered with the
`/dgx` skill (`.claude/skills/dgx/SKILL.md`) — use it even when not invoked by name.

## Hard rules
- **Answer only from `kb/` (or the PDFs through the cache workflow). Never from memory or general knowledge**
  unless the user explicitly asks, and then label it "(general knowledge, not from the manuals)".
- **Cite every claim**: `[OM p.50]`, `[RM p.31]`, `[DL p.23]`, figures as `[FIG RM-005-f1]`. Page numbers are the
  printed page numbers, which equal the PDF page numbers.
- If the manuals don't cover it: say **"Not documented in the DGX-670 manuals."**, then **"Closest documented:"**
  with cited related material, if any exists.
- Start from the maps (`kb/INDEX.md`), not from bulk-reading pages. Read only the pages you need.
- Never search or cite the supplied text folders `dgx_source_docs/*_text/` (build-time calibration only, gitignored).

## Layout
- `kb/INDEX.md` — entry point. `kb/maps/` — GLOSSARY, TERMS, BUTTONS, MENU_PATHS, TOC, DATALIST_TOC.
- `kb/pages/{OM,RM}/<ID>.md` — one file per PDF page (generated; `ID` like `OM-050`).
- `kb/figures/` — cached figure descriptions. `kb/datalist/` — cached Data List pages. `faq/` — verified answers.
- `scripts/build_kb.py` (needs `pip install -r requirements.txt`) regenerates pages + maps from the PDFs;
  `scripts/register.py` and `scripts/check_kb.py` are stdlib-only and run anywhere.

## Living cache (expensive work is done once)
- Figure needed and page has `figure_cache: none` → delegate to the **figure-describer** agent.
- Data List needed and page not in `kb/datalist/INDEX.md` → delegate to the **datalist-reader** agent.
- User confirms an answer ("correct", "save it") → write a FAQ entry (see skill).
- Wording that didn't map to a manual term → add a row to `kb/maps/GLOSSARY.md`.
- Hand-editing generated files is only allowed via `scripts/register.py` (it keeps markers/indexes consistent).

## Git (pre-authorized by the user)
After any cache update, commit **only** `kb/` and `faq/` paths and push immediately:
`git add kb/... faq/... && git commit -m "kb: <what>" && git push`. If push fails (offline/no remote), keep the
local commit and say so. Changes to anything else (scripts, CLAUDE.md, .claude/) need the user's go-ahead.
