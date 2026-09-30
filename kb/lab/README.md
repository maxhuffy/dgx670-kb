# Lab findings: format and rules

This folder holds **first-hand findings from the user's own DGX-670**: file analysis of data the instrument saved,
files generated here and loaded on the instrument, and what its display showed (screenshots). It covers things the
manuals don't document and nobody online has published (e.g. the internals of Voice files).

Trust tier (between the manuals and `kb/external/`):
- The manuals (OM/RM/DL) still win. If a lab finding seems to contradict a manual page, report both, cited.
- Lab findings beat `kb/external/` for DGX-670 behaviour, because they were observed on this instrument.
- Cite as `[LAB <slug>#L<n>]` and label "(lab-tested on the user's DGX-670, not from the manuals)".
- Every finding carries a **status**:
  - `confirmed`: observed on the instrument (display, sound or load behaviour), or proven by a one-change file diff.
  - `likely`: consistent with all evidence and the Data List tables, but not yet seen on the instrument.
  - `hypothesis`: an educated guess from patterns; test before relying on it.
  - `unknown`: seen in the data, meaning not worked out.
- Never upgrade a status without new evidence. Record the date and the evidence (file names, screenshots) for each.

## File: `kb/lab/<slug>.md`
```
# <Topic>
topic: <one line, used in INDEX.md>
status: <overall: confirmed | partial | hypothesis>
tested: YYYY-MM-DD (last update)
evidence: <where the raw evidence lives (local, untracked folders), e.g. initial_dgx_voices_saved_to_usb/>
summary: <one line, used in INDEX.md>

## Manual baseline
<cited manual/Data List facts that frame the topic>

## Findings
**[L1]** <claim>. Status: confirmed | likely | hypothesis | unknown. Evidence: <files / screenshots / test>.

## Experiment log
<dated: what was generated/tested, what the user observed>

## Open questions
<what to test next, and how>
```

Machine-readable companions (CSV) sit next to the entry, e.g. `voice_file_fields.csv`.
Evidence folders (`initial_dgx_voices_saved_to_usb/`, `settings_screenshots/`, `generated_voices/`) are local and
untracked; findings must be understandable without them.
