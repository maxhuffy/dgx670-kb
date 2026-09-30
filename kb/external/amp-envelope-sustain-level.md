# Can I set the Sustain Level of a Voice's envelope on the DGX-670?
topic: Amp envelope on the DGX-670: no Sustain Level parameter (Attack/Decay/Release only)
status: found
researched: 2026-09-30
manual_gap: RM p.15 edits Attack, Decay and Release. Its EG diagram shows a "Sustain Level", but no parameter sets it [FIG RM-015-f2 figure text]. The MIDI tables list the same three EG times as offsets [DL p.60, p.65].
queries: "Yamaha PSR OR DGX voice set EG sustain level not editable attack decay release only"; "XG part parameters EG attack decay release no sustain level parameter Yamaha XG specification"
summary: Confirmed: the XG-style part envelope has Attack/Decay/Release offsets only. The sustain level is fixed by each Voice's preset. Workaround: long Decay (or pick a Voice that already holds), plus a compressor for evenness.

## Manual baseline
- **Voice Set EG** [RM p.15]:
  - Attack: "how quickly the sound reaches its maximum level";
  - Decay: "how quickly the sound reaches its sustain level (a slightly lower level than maximum)";
  - Release: decay to silence after key-off.
- The MIDI tables show these as relative offsets (−64…0…+63) of the Voice's own settings:
  - NRPN EG Attack Time / Decay Time / Release [DL p.60];
  - SysEx Multi Part EG ATTACK / DECAY / RELEASE TIME [DL p.65].

  No sustain-level parameter appears in either table.
- Per-key drum parameters (EG Attack Rate, Decay1/Decay2 Rate) exist only for Song-part drum kits [DL p.68], so
  they don't help.

## Findings
**[E1]** The XG Multi Part envelope parameters are EG ATTACK TIME (08 nn 1A), EG DECAY TIME (1B) and EG RELEASE TIME (1C), each −64…0…+63 around the Voice's default. The XG spec has no sustain-level parameter. Attack and Release can also be sent as CC73/CC72. Source: STUDIO4ALL, "Yamaha XG Part Setup". http://www.studio4all.de/htmle/main92.html Type: third-party doc (XG reference site). Applies to: XG in general; the addresses match the DGX-670 table [DL p.65]. Trust: high.

**[E2]** Sound On Sound: XG gives "full control over the envelope time constants". Its one main EG drives both amp and filter [EXT filter-envelope#E1]. Source: Sound On Sound, Mike Senior, "Creative Synthesis With Yamaha XG (Part 1)", April 2004. https://www.soundonsound.com/techniques/creative-synthesis-yamaha-xg-part1 Type: third-party doc. Applies to: XG. Trust: medium.

## Not found
- As of 2026-09-30, no DGX-670 forum/Reddit post discusses the missing sustain level or a workaround.
- One search-engine summary claimed the DGX-670 has "EG Decay 1 / Decay 2". That **contradicts** RM p.15
  (Attack/Decay/Release), so it was discarded.

## Practical takeaway
- **Sustained lead:** choose a Voice that already holds at full level. Then set EG Decay to a high value (slow decay)
  so the level stays near the peak for held notes. Keep Attack low and Release fairly low [RM p.15].
- **Even level:** a compressor evens out the level. CompMelody or CompMed are available as DSP Types [DL p.28].
  Comp+Dist1 puts compression before distortion [DL p.30].
- Master Compressor also works, but on the whole instrument [RM p.73].
