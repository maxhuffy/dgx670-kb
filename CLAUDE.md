# DGX-670 Knowledge Base

A cited, growing knowledge base for the **Yamaha DGX-670** keyboard, built from the PDFs in `dgx_source_docs/`
(Owner's Manual = OM, Reference Manual = RM, Data List = DL). Every DGX-670 question is answered with the
`/dgx` skill (`.claude/skills/dgx/SKILL.md`) — use it even when not invoked by name.

## Hard rules
- **Answer only from `kb/` (or the PDFs through the cache workflow). Never from memory or general knowledge**
  unless the user explicitly asks, and then label it "(general knowledge, not from the manuals)".
- **Three trust tiers.** The manuals (`kb/pages`, `kb/datalist`, `kb/figures`, `faq/`) are tier 1. `kb/lab/`
  (first-hand tests on the user's own DGX-670: file analysis, generated files loaded on it, display screenshots) is
  tier 2: label it "(lab-tested on the user's DGX-670, not from the manuals)", cite `[LAB <slug>#L<n>]`, and pass on
  each finding's status (confirmed / likely / hypothesis / unknown). `kb/external/` (online research) is tier 3: use it
  only to fill gaps, label it "(external, not from the manuals)", cite `[EXT <slug>#E<n>]`. Neither lower tier may
  override a manual page; lab beats external on how this instrument actually behaves.
- **Cite every claim**: `[OM p.50]`, `[RM p.31]`, `[DL p.23]`, figures as `[FIG RM-005-f1]`. Page numbers are the
  printed page numbers, which equal the PDF page numbers.
- If the manuals don't cover it: say **"Not documented in the DGX-670 manuals."**, then **"Closest documented:"**
  with cited related material, if any exists. Then, if `kb/lab/` covers it, **"Lab-tested:"** with `[LAB …]`
  citations and statuses. Then, if `kb/external/` covers it, **"External research:"** with `[EXT …]` citations (or its
  dated "nothing found online").
- Start from the maps (`kb/INDEX.md`), not from bulk-reading pages. Read only the pages you need.
- Never search or cite the supplied text folders `dgx_source_docs/*_text/` (build-time calibration only, gitignored).

## Layout
- `kb/INDEX.md` — entry point. `kb/maps/` — GLOSSARY, TERMS, BUTTONS, MENU_PATHS, TOC, DATALIST_TOC.
- `kb/pages/{OM,RM}/<ID>.md` — one file per PDF page (generated; `ID` like `OM-050`).
- `kb/datalist/` — every Data List table as CSV (`csv/`, each row starts `dl_page,table`), searchable briefs in
  `INDEX.md`, per-page legends in `pages/DL-nnn.md`, build checks in `CHECKS.md`, known discrepancies in `ISSUES.md`.
- `kb/figures/` — cached figure descriptions. `faq/` — verified answers. `kb/guides/` — cited cheat sheets.
- `kb/lab/` — lab findings tested on the user's DGX-670, with machine-readable companions such as
  `voice_file_fields.csv` (format: `kb/lab/README.md`, index: `INDEX.md`). Raw evidence lives in local untracked
  folders (`initial_dgx_voices_saved_to_usb/`, `settings_screenshots/`, `generated_voices/`).
- `kb/external/` — externally researched topics (format: `kb/external/README.md`, index: `INDEX.md`).
- `scripts/build_kb.py` (needs `pip install -r requirements.txt`) regenerates pages, maps and the Data List CSVs
  (`build_datalist.py`, briefs from `scripts/datalist_briefs.md`); `register.py`, `check_kb.py` are stdlib-only.
- `scripts/voicefile.py` (stdlib-only) decodes, diffs and edits DGX-670 Voice files (.vce etc.), labelling fields from
  the Data List CSVs; see `kb/lab/voice-file-format.md` for the format and the panel-value rules.

## Living cache (expensive work is done once)
- Figure needed and page has `figure_cache: none` → delegate to the **figure-describer** agent.
- A Data List CSV row looks wrong/missing or is doubted → delegate to the **datalist-verifier** agent (logs to ISSUES.md).
- User confirms an answer ("correct", "save it") → write a FAQ entry (see skill).
- User asks for online research, or a gap matters and `kb/external/` has nothing (or only an old `nothing-found`)
  → research it (WebSearch/WebFetch), write `kb/external/<slug>.md` per its README, even when nothing is found, then
  `python scripts/register.py external <slug>`.
- User reports a test on the instrument (screenshots, files it saved, what loaded or how it sounded) → update or create
  `kb/lab/<slug>.md` per its README (upgrade a finding's status only with new evidence, log the experiment), then
  `python scripts/register.py lab <slug>`.
- Wording that didn't map to a manual term → add a row to `kb/maps/GLOSSARY.md`.
- Hand-editing generated files is only allowed via `scripts/register.py` (it keeps markers/indexes consistent).

## Git (pre-authorized by the user)
After any cache update, commit **only** `kb/` and `faq/` paths and push immediately:
`git add kb/... faq/... && git commit -m "kb: <what>" && git push`. If push fails (offline/no remote), keep the
local commit and say so. Changes to anything else (scripts, CLAUDE.md, .claude/) need the user's go-ahead.
