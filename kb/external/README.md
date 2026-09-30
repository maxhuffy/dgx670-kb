# Externally researched topics: format and rules

This folder holds **online research** on questions the DGX-670 manuals don't answer, or answer only partly. Sources
include Yamaha support/FAQ pages, forums (e.g. PSR Tutorial, Yamaha Musicians Forum), Reddit, YouTube and
third-party docs. It is a **second trust tier**:

- The manuals (OM/RM/DL) always win. If an external claim conflicts with a manual page, say so and cite both.
- Every external claim in an answer is labelled **(external, not from the manuals)** and cited `[EXT <slug>#E<n>]`,
  e.g. `[EXT filter-envelope#E2]`. The finding line in the file carries the URL.
- Negative results are kept too. `status: nothing-found` plus the `researched:` date says "nothing found online as of
  that date", so later sessions don't repeat the same searches unless the entry is old or the user asks.

## File: `kb/external/<slug>.md`
```
# <Topic as a question or short title>
topic: <one line, used in INDEX.md>
status: found | partial | nothing-found
researched: YYYY-MM-DD
manual_gap: <what the manuals say / don't say, cited, e.g. "RM p.15 lists Attack/Decay/Release only">
queries: "<search 1>"; "<search 2>"; …
summary: <one line answer, used in INDEX.md>

## Manual baseline
<cited facts from kb/ that frame the gap: [RM p.15], [DL p.37] …>

## Findings
**[E1]** <claim, in your own words, short quote if useful>. Source: <site>, <author/thread title>, <post date if shown>.
<URL>. Type: official | forum | reddit | video | third-party doc. Applies to: DGX-670 | same engine/family (name it) |
general. Trust: high | medium | low (why).

**[E2]** …

## Not found
<what was looked for and not found, as of the researched date>

## Practical takeaway
<how this changes what the user can do on the DGX-670; keep manual-backed and external parts clearly separated>
```

Rules for findings:
- One claim per `[En]`. Always include the URL and the source type; say whether it's about the DGX-670 itself or a
  related model (e.g. PSR-E/PSR-SX/Genos/Clavinova), because related-model claims may not carry over.
- Don't paste long copyrighted text; paraphrase, quote at most a sentence.
- Never upgrade an external claim to a fact. "A forum user reports…" stays that way until the user tests it.

## Registering
`python scripts/register.py external <slug>` validates the fields (a URL on every finding, a `## Manual baseline`
section, a valid status/date) and updates `INDEX.md`. `scripts/check_kb.py` re-checks every entry. Then commit
`kb/external/…` with `kb: external <slug>` and push.
