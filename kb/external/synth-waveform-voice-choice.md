# Can I choose a saw/pulse/square waveform, or get more raw synth-lead Voices, on the DGX-670?
topic: Choosing a saw/pulse/square source for synth leads; hidden GM/XG synth-lead Voices; loading new waveforms
status: found
researched: 2026-09-30
manual_gap: The manuals have no waveform/oscillator setting and don't describe any Voice's sound. The Data List gives names and numbers only [DL p.3–12]. GM/XG/GM2 compatibility is listed "for Song playback" [OM p.106].
queries: "DGX-670 synth lead voice sawtooth square analog Moog sound"; "reddit DGX-670 synth voices best lead"; "DGX-670 expansion voices load custom samples waveform not supported"; "DGX-670 Expansion Manager not compatible NAND flash wave data internal voices"
summary: No waveform choice and no expansion packs. But the hidden GM/XG synth leads (SawtoothLead1/2, PulseSaw, SawPulseLead, DoublSawLead, SquareLead1/2, LM Square…) can be played via community-made User Voice files loaded from USB.

## Manual baseline
- Voice editing has no oscillator or waveform parameters. The Voice Set pages are Common, Controller, Sound, Effect/EQ
  and Harmony [RM p.13–16].
- The panel spec is 601 Voices + 29 Drum/SFX Kits [OM p.106]. That count equals the Data List's Main + Legacy +
  MegaVoice sections. The **GM & XG** (480) and **GM2** (265) sections are extra [DL p.7–12; `kb/datalist/INDEX.md`].
- The spec lists "Compatibility (for Song playback) XG, GS, GM, GM2" [OM p.106].
- Synth-lead names in the GM & XG / GM2 sections include SquareLead1–2, LM Square, SawtoothLead1–2, ThickSaw,
  DynamicSaw, DigitalSaw, BigLead, HeavySynth, WaspySynth, PulseSaw, Dr.Lead, SeqAnalog, CharangLead, DistortedLd
  [DL p.9], and SawPulseLead and DoublSawLead [DL p.12]. Their MSB/LSB/PC numbers are in `voices.csv`.

## Findings
**[E1]** Yamaha Customer Support says the GM/XG Voices are for Song playback only and "cannot be played from the DGX itself". This differs from the DGX-650/660. Source: keyboardforums.com thread "DGX-670 GM & XG Voices", John Harjo (Yamaha Customer Support), 2022-12-20. https://www.keyboardforums.com/threads/dgx-670-gm-xg-voices.34185/ Type: official (Yamaha staff on a forum). Applies to: DGX-670. Trust: high (it matches the "for Song playback" spec line [OM p.106]).

**[E2]** Workaround: a user extracted **all GM, XG and GM2 Voices as DGX-670 User Voice files**. The download is "GM, XG, and GM2 Voices (DGX-670).zip", 360 KB, attached to post #18. You copy them to a USB stick and load them as user Voices, which makes them playable from the keyboard. Source: same thread, user "Δικαιοπολις", 2023-05-07. https://www.keyboardforums.com/threads/dgx-670-gm-xg-voices.34185/ Type: forum. Applies to: DGX-670. Trust: medium (several users say it works; not tested here; the attachment may need a forum login).

**[E3]** You can also play the GM/XG Voices without files: from a DAW or MIDI device, send Bank Select MSB/LSB + Program Change to the DGX over USB. Source: same thread (the Yamaha answer and discussion). https://www.keyboardforums.com/threads/dgx-670-gm-xg-voices.34185/ Type: forum/official. Applies to: DGX-670. Trust: high (consistent with the MIDI numbers in [DL p.7–12]).

**[E4]** The DGX-670 is **not** compatible with Yamaha Expansion Manager packs, so no new samples or waveforms can be added. The reason given: the internal wave memory (NAND flash) and tone generator are fully used by the built-in Voices. Editing existing Voices and saving them is possible. Source: PSR Tutorial forum, "Expansion Packs for DGX-670". https://forum.psrtutorial.com/index.php?topic=62281.0 Type: forum (the wording reads like a Yamaha answer). Applies to: DGX-670. Trust: medium-high (seen only through search excerpts; the site returned 403 to direct fetch).

## Not found
- Any description of the waveform or sample content behind individual DGX-670 synth Voices (official or community).
  Names are the only hint.
- Any DGX-670-specific Reddit discussion of the best synth leads (as of 2026-09-30).

## Practical takeaway
- On the panel: audition the Main/Legacy synth leads [DL p.5–6].
- For more raw saw/square/pulse sources (external, not from the manuals):
  - load the community GM/XG User Voice files [EXT synth-waveform-voice-choice#E2], or
  - drive the DGX from a DAW with the GM/XG numbers [EXT synth-waveform-voice-choice#E3].
- Candidates from the names: SawtoothLead1/2, PulseSaw, SawPulseLead, DoublSawLead, SquareLead1/2, LM Square
  [DL p.9, p.12].
- Once loaded as User Voices, the normal Voice Set editing should apply (not verified).
