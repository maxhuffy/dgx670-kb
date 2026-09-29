---
name: dgx
description: Answer any question about the Yamaha DGX-670 keyboard (buttons, menus, settings, Styles, Voices, Songs, recording, connections, specs, troubleshooting) from the cited knowledge base in kb/. Use for every DGX-670 question, whether or not /dgx is typed.
argument-hint: <question about the DGX-670>
---

# Answering a DGX-670 question

Question: $ARGUMENTS

Goal: a correct answer where **every claim is cited to a page**, using as few reads as possible.
Never answer from memory. "Not documented" beats a guess.

## 1. Look up (cheap → expensive)
**Token economy:** every turn re-sends the whole context, so batch. Run steps 1–3 as **one message of
parallel `Grep` calls** (FAQ index, GLOSSARY, TERMS, MENU_PATHS, BUTTONS, TOC, and the Data List briefs in
`kb/datalist/INDEX.md` with your best-guess terms), then read all candidate pages / grep candidate CSVs in
**one parallel batch**. Aim for ≤ 4 turns before answering.

1. **Verified FAQ** — `Grep` `faq/INDEX.md` for the topic. A match is a strong starting point, but still
   confirm its citations still say that (read the cited page) before answering.
2. **Translate the wording** — `Grep -i` `kb/maps/GLOSSARY.md` for the user's words → manual terms.
3. **Map terms to pages** — `Grep -i` the manual terms in:
   - `kb/maps/TERMS.md` (printed indexes → page IDs)
   - `kb/maps/MENU_PATHS.md` ("how do I get to X" → exact button path + page)
   - `kb/maps/BUTTONS.md` (a panel button → pages that mention it most)
   - `kb/maps/TOC.md` (chapter/section → page range; also the OM ↔ RM chapter join)
   - `kb/datalist/INDEX.md` (briefs of all 18 Data List tables: voices, styles, songs, drum kits, effects,
     Parameter Chart = what is saved where, Direct Access Chart, MIDI…) → which CSV can answer
4. **Backstop** — only if the maps found nothing: `Grep -i` `kb/pages` for distinctive words.

## 2. Read
- Read the candidate page files (`kb/pages/OM/OM-058.md` etc.) **in full** — usually 1–4 pages is enough.
- Follow `links_out` one hop when the page defers ("page 56"). When a page says "refer to the Reference
  Manual", use the TOC chapter join to find the RM pages. `refers_to: [DL]` → step 4.
- Stop reading once every part of the question is covered.

## 3. Figures (only when the answer depends on what a figure shows)
- Figure marker already has a title (`[FIG RM-005-f1 — …; see kb/figures/RM-005.md#f1]`) → read that file. Free.
- Page has `figure_cache: none` → delegate to the **figure-describer** agent with the page ID and what the
  question needs. Do **not** open the PDF yourself (keeps image tokens out of this conversation).
- `figure_cache: skip` (cover/marketing/legal/index pages) → don't describe; answer from text.

## 4. Data List (lists, numbers, charts — and extra context the manuals don't give)
- Every Data List table is a CSV in `kb/datalist/csv/`, described in `kb/datalist/INDEX.md`. `Grep -i` the CSV
  for the value (e.g. a voice/style/kit name); read line 1 for the header. Each row starts `dl_page,table` →
  cite `[DL p.<dl_page>]`. Page legends/footnotes: `kb/datalist/pages/DL-nnn.md`.
- Use it even when the manuals don't mention it, if a table adds precise facts (voice numbers, which Styles
  support Unison/Adaptive, what a setting is saved with, which key plays which drum…).
- Check `kb/datalist/ISSUES.md` for known discrepancies. If a row looks wrong/missing, or the user doubts it,
  delegate to the **datalist-verifier** agent (it compares with the page image and logs the result).

## 5. Answer format
```
<Direct answer in 1–3 sentences> [OM p.58]

Steps:
1. Press [MENU] → Cursor buttons [▲][▼][◀][▶] … [OM p.58]
2. … [RM p.24]

Notes: <caveats / related settings, cited>
Sources: OM p.58 · RM p.24 · FIG RM-005-f1 · DL p.23
```
- Cite every factual sentence. Quote menu paths exactly as the page prints them.
- Symbols: ▲▼◀▶ cursor/display buttons; [1▲▼] numbered display buttons; → next step; (n) numbered callout.
- Undocumented: `**Not documented in the DGX-670 manuals.**` then `**Closest documented:**` + cited items
  (omit that part if nothing is close). Never fill the gap from general knowledge.
- Conflicting pages (e.g. OM vs RM): show both, cited, and say which is more specific.

## 6. Grow the knowledge base (then commit + push only kb/ and faq/)
- **Glossary gap**: the user's wording needed a term not in GLOSSARY → add a row (alphabetical), commit
  `kb: glossary <term>`.
- **Verified FAQ**: only when the user confirms the answer is right / asks to save it. Write `faq/<slug>.md`:
  ```
  # <Question as asked>
  question: <question>
  citations: [OM p.58], [RM p.24]
  verified: <YYYY-MM-DD>

  <the confirmed answer, with inline citations>
  ```
  Then `python scripts/register.py faq <slug>` and commit `faq: <slug>`.
- Commit/push command: `git add <changed kb/ and faq/ paths> && git commit -m "<msg>" && git push`.
