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

1. **Verified FAQ + guides** — `Grep` `faq/INDEX.md` and `kb/guides/` for the topic. A match is a strong starting
   point, but still confirm its citations say that (read the cited page) before answering. FAQ entries whose
   `status:` says UNVERIFIED are cited drafts the user hasn't tested yet.
2. **Translate the wording** — `Grep -i` `kb/maps/GLOSSARY.md` for the user's words → manual terms.
3. **Map terms to pages** — `Grep -i` the manual terms in:
   - `kb/maps/TERMS.md` (printed indexes → page IDs)
   - `kb/maps/MENU_PATHS.md` ("how do I get to X" → exact button path + page)
   - `kb/maps/BUTTONS.md` (a panel button → pages that mention it most)
   - `kb/maps/TOC.md` (chapter/section → page range; also the OM ↔ RM chapter join)
   - `kb/datalist/INDEX.md` (briefs of all 18 Data List tables: voices, styles, songs, drum kits, effects,
     Parameter Chart = what is saved where, Direct Access Chart, MIDI…) → which CSV can answer
4. **Backstop** — only if the maps found nothing: `Grep -i` `kb/pages` for distinctive words.
5. **Lab tier, then external tier** — if the manuals leave a gap, `Grep -i` `kb/lab/INDEX.md` and then
   `kb/external/INDEX.md` (include both in the step-1 batch). Lab findings were tested on the user's own DGX-670 (e.g.
   Voice file internals: `kb/lab/voice-file-format.md` + `voice_file_fields.csv`); external ones come from online
   research. Use them only for the gap; see §6 and §6b.

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
- Lab findings go **after** the manual-backed answer, under `**Lab-tested on your DGX-670 (not from the manuals):**`,
  each claim cited `[LAB <slug>#L<n>]` with its status (confirmed / likely / hypothesis / unknown). Don't present a
  `likely` or `hypothesis` finding as fact.
- External research goes **after** the manual-backed answer, under `**External research (not from the manuals):**`,
  each claim cited `[EXT <slug>#E<n>]` with its source type (forum/Reddit/official…). A `nothing-found` entry is
  reported as "Nothing found online as of <date> [EXT <slug>]".

## 6. External research (online) — only when asked, or when a gap matters and nothing is cached
1. Check `kb/external/INDEX.md` first. Reuse an entry; re-research only if it's `nothing-found` and old, or asked.
2. Search in one batch of parallel `WebSearch` calls (DGX-670 name variants; Reddit; psrtutorial.com; Yamaha
   Musicians Forum; YouTube; Yamaha support/FAQ; then sibling models on the same engine, labelled as such).
   `WebFetch` only the most promising 1–3 pages, with a prompt asking for the specific facts.
3. Write `kb/external/<slug>.md` exactly as in `kb/external/README.md` (manual baseline cited, one `**[En]**` per
   claim with URL, source type, which model it's about, trust). Record negatives with the date.
4. `python scripts/register.py external <slug>`, then commit `kb: external <slug>` and push.

## 6b. Lab findings (first-hand tests on the user's DGX-670)
1. When the user reports a test (screenshots, files the keyboard saved, what loaded/sounded), or you analyse files they
   saved, update the matching `kb/lab/<slug>.md` (or create one) exactly as in `kb/lab/README.md`: one `**[Ln]**`
   paragraph per finding with `Status:` and evidence, a dated experiment-log line, and the remaining open questions.
2. Upgrade a status only with new evidence (e.g. `likely` → `confirmed` when the display shows the value).
3. Voice files: decode/diff with `python scripts/voicefile.py decode|diff …`; keep `voice_file_fields.csv` in step.
4. `python scripts/register.py lab <slug>`, then commit `kb: lab <slug> …` and push.

## 7. Grow the knowledge base (then commit + push only kb/ and faq/)
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
