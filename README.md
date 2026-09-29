# DGX-670 Knowledge Base

A cited knowledge base for the Yamaha DGX-670 that grows as you use it, plus a Claude Code agent setup
that answers from it. The PDFs in `dgx_source_docs/` are the source of truth. The build turns them into
one Markdown file per page and a set of lookup maps. Every answer cites pages like `[OM p.58]`, so you can
check any claim in seconds.

## Ask a question
| Where | How |
|---|---|
| VS Code / terminal | Open this folder in Claude Code and ask, or type `/dgx <question>` |
| Phone, quick Q&A | Claude app → Project **DGX-670 Expert** (reads `kb/` and `faq/` synced from GitHub; tap **Sync** after pushes) |
| Phone, full agent | Claude app → Code → this repo (can process new figures and Data List pages, and saves them back) |

## How it gets smarter
Expensive work is done once and committed:
- **Figures:** the figure-describer agent looks at the whole page, describes every figure on it, and saves the result to `kb/figures/`.
- **Data List pages:** the datalist-reader agent saves them to `kb/datalist/`.
- **Answers you confirm:** saved to `faq/`.
- **New wording:** added to `kb/maps/GLOSSARY.md`.

Agents commit and push only `kb/` and `faq/`.

## Maintenance
```bash
python -m venv .venv && .venv/Scripts/pip install -r requirements.txt   # once (PyMuPDF)
.venv/Scripts/python scripts/build_kb.py   # rebuild pages + maps from the PDFs (deterministic; keeps caches)
python scripts/check_kb.py                 # consistency checks (stdlib only)
python evals/run_evals.py                  # 10 test questions: citation accuracy + cost per answer
```
Replacing a PDF with a newer revision: update the file name in `scripts/build_kb.py` (`DOCS`), rebuild,
and review `git diff kb/`. The page roles and index page ranges in `DOCS` may also need updating.

See `CLAUDE.md` for the agent rules and layout, and `.claude/skills/dgx/SKILL.md` for how answers are looked up.
