# UNVERIFIED: How can pedals step through Registrations during a song (custom order, next/previous, more than 4 via a second Bank)?
question: UNVERIFIED: How can pedals step through Registrations during a song (custom order like 1 2 1 3 1 4, next/previous pedals, continuing into a second Bank)?
citations: [RM p.63–64], [FIG RM-064-f1], [DL p.53], [RM p.76–78], [OM p.15], [OM p.83], [OM p.86]
status: UNVERIFIED. Saved at the user's request; the user has not yet tested it on the instrument. Treat it as a cited draft and re-check the pages. The open questions below still need hands-on testing.
saved: 2026-09-29

## The feature: Registration Sequence
- Recalls the four setups "in any order you specify" using TAB [◀][▶] on the Main display, or pedals [RM p.63].
- Program the order left to right using REGISTRATION MEMORY [1]–[4] + [4▲▼] (Insert). Edit with [3▲▼] Replace and
  [5▲▼] Delete [RM p.64].
- The same number can repeat: the example screen shows the sequence "1 2 3 4 1", so 1 2 1 3 1 4 is possible. The
  screen shows 32 slots; no maximum length is printed [FIG RM-064-f1].
- Path: [MENU] → Cursor buttons [▲][▼][◀][▶] Regist Sequence/Freeze, [ENTER] → TAB [◀] Registration Sequence
  [RM p.63].
- Separate Prev and Next pedals via [8▲▼] (Pedal); each can be AUX, Right, Center or Left [RM p.63].
- A pedal set here (other than Off) overrides that pedal's Controller → Pedal function [RM p.63].
- Sequence End (per Bank) [RM p.64]:
  - Stop: "next" does nothing.
  - Top: the sequence restarts.
  - Next Bank: goes to the start of the next Bank in the same folder.
- Turn it on with [1▲▼] (Seq.). Save with [EXIT] → [7▲▼] (Yes), or the sequence is lost when you select another Bank
  [RM p.64].

## What is stored where [DL p.53]
- Stored in the Bank file: Sequence Data and Sequence End ("One sequence data per Regist Bank file").
- Global (Backup/System Setup, not per Bank): Sequence On/Off and the Prev/Next pedal choice.

## Suggested gig setup (pedal unit + AUX)
- Pedals: Right = sustain (Half Pedal) [OM p.15]; Left = Regist Prev; Center = Regist Next; AUX = spare, e.g. Layer Part
  On/Off or Style Start/Stop [RM p.77–78].
- One-Bank songs: program the order, End = Stop.
- Two-Bank songs: put both Banks next to each other in the same folder; Bank A End = Next Bank, Bank B End = Stop.
- Between songs: select the next Playlist Record [OM p.86]. Alternative: keep the whole set in one folder in order and
  chain it with Next Bank.
- Backups by hand:
  - TAB [◀][▶] follows the sequence [RM p.63].
  - REGISTRATION MEMORY [1]–[4] jumps directly [OM p.83].
- Freeze keeps chosen items (e.g. the Style) from changing on recall [OM p.83].

## Open questions (not in the manuals; test on the instrument)
1. Does Prev cross back into the previous Bank after a Next Bank jump?
2. What order decides "next Bank in the same folder"? Probably display/name order, so name files "05a", "05b"
   (this is an assumption).
3. Where does the sequence start when a Playlist Record loads a Bank with Load Regist Memory set?
4. Can a pedal step through Playlist Records? None is listed in the pedal functions [RM p.76–78], so it looks like no.
