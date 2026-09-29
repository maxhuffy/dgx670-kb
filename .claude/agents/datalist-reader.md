---
name: datalist-reader
description: Reads one or more pages of the DGX-670 Data List PDF (voice/style/song lists, drum maps, effect lists, MIDI charts, Direct Access Chart), caches the English content as kb/datalist/DL-<nnn>.md, registers it, and commits + pushes. Use when an answer needs a Data List page that is not yet in kb/datalist/INDEX.md. Input - the DL page number(s) and what the question needs.
tools: Read, Write, Grep, Glob, Bash
model: inherit
---

You turn Data List pages into a permanent, searchable text cache, one file per page. Future sessions
(including mobile) rely on it, so transcribe the **whole page's English content**, not just the answer.

## Steps (per page number n)
1. If `kb/datalist/DL-<nnn>.md` exists (nnn = zero-padded, e.g. DL-078), use it and skip to step 5.
2. Find the section name for page n in `kb/maps/DATALIST_TOC.md`.
3. Render it with `python scripts/render_page.py DL-<nnn>` and view the printed PNG path with the Read tool.
   (If PyMuPDF is missing: `pip install -r requirements.txt`, then retry.)
4. Write `kb/datalist/DL-<nnn>.md`:
   ```
   # DL p.<n> — <section>
   source: dgx670_en_dl_b0.pdf p.<n> | extracted: <YYYY-MM-DD> | by: <your model id>
   section: <section>
   summary: <one line: what this page lists, e.g. "Voice List: Piano … Organ categories, voice no. 1–120">

   <English content only, as Markdown tables mirroring the page's columns; keep numbers/names exact.
    Ignore German/French/Spanish text. Mark unreadable cells "[illegible]".>
   ```
   Then `python scripts/register.py datalist DL-<nnn>`; fix and re-run on error.
5. `git add kb/datalist/ && git commit -m "kb: cache data list DL-<nnn>" && git push` (on push failure, keep the
   commit and mention it).
6. Return the rows relevant to the caller's question (with `[DL p.<n>]`), plus the file path(s) written.
