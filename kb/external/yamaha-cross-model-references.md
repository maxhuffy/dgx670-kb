# What external Yamaha references explain the DGX-670's Voices, DSP effects and parameters?
topic: Cross-model Yamaha references (PSR-SX600, XG/MU128, Synthesizer Parameter Manual, Motif/MOX) and community sources for understanding DGX-670 Voices, DSP effect types and effect parameters
status: partial
researched: 2026-10-02
manual_gap: The Data List gives Voice names/numbers only [DL p.3–12], one-line effect-type descriptions [DL p.25–32] and effect parameter names/ranges with no explanation of what each parameter does [DL p.33–44]. The manuals never say which other Yamaha models share the DGX-670's sounds or effects.
queries: "Yamaha XG specification PDF effect type descriptions V DISTORTION AMP SIMULATOR parameter description"; "Yamaha Synthesizer Parameter Manual effect parameters Edge Presence Speaker Type"; "PSR-SX600 data list PDF voice list effect type list"; "github Yamaha XG voice list csv OR json MSB LSB program effect types dataset"; "DGX-670 all voices demo YouTube"; "Yamaha MU128 OR MU2000 owner's manual effect type list descriptions"; "MOTIF XF OR MOXF Synthesizer Parameter Manual effect type descriptions"; "DGX-670 PSR-SX600 same voices same sound engine"; "sandsoftwaresound Yamaha arranger DSP effects"; "Yamaha arranger voice descriptions Cool! Sweet! Live!"; "psrtutorial Yamaha effects explained DSP"; "PSR-SX600 all voices demo"; "Yamaha XG Guidebook pdf effects explained"; "DGX670 same sound library PSR-SX600"
summary: Best absorbable source: Yamaha's own effect-parameter explanations (MU128 XG Data List + Synthesizer Parameter Manual), now indexed per DGX parameter in effect_param_glossary.csv (179/194 names matched). The PSR-SX600 Data List is near-identical to the DGX's (same sound library per forum + our name comparison), so SX600 material applies. No per-Voice descriptions or systematic all-Voice demos were found.

## Manual baseline
- Effect types have one-line descriptions, e.g. Overdrive "Adds mild distortion to the sound", VDistCrunch "Distortion
  which simulates the sound of a vintage tube, fuzz effect, etc." [DL p.28–30].
- Effect parameter lists give names, display ranges and data values only, e.g. V DISTORTION: Overdrive, Device, Speaker
  Type, Presence, Output Level, Dry/Wet [DL p.37]; STEREO AMP SIMULATOR: Drive, Amp Type, LPF Cutoff Frequency, Output
  Level, Dry/Wet, Edge [DL p.38]. Nothing explains what a parameter does, except "Edge (Clip Curve) 0–127 (mild –
  sharp)" [DL p.38].
- Voice types (VRM, S.Art!, MegaVoice, Live!, Cool!, Sweet!, Natural!) are explained in the Reference Manual
  [RM p.4]; individual Voices are not described.

## Findings
**[E1]** A forum user states "The DGX670 is the same sound library as PSRsx600/PSRs770"; the differences named are features (no MIDI event edit page, 4 instead of 8 registrations). Source: YamahaMusicians forum, "DGX 670 in 2026?", amwilburn, post #11, 2026-06-29. https://yamahamusicians.com/forum/threads/dgx-670-in-2026.24287/post-148617. Type: forum. Applies to: DGX-670 vs PSR-SX600/PSR-S770. Trust: medium-high (supported by [E2]).

**[E2]** The official PSR-SX600 Data List (77 pages) matches the DGX-670 Data List closely. Name comparison done here on 2026-10-02 against `kb/datalist/csv/`: 593 of the DGX's 630 panel Voices/kits appear by name (the misses are mainly VRM pianos and some organ/"SW" Voices), 316 of 322 effect-type names (the misses are the six Piano-room reverbs Pf…/Piano…), 84 of 85 effect parameter lists, and 153 of 159 effect descriptions word-for-word. So SX600 material (reviews, demos, forum threads) is very likely to apply, but the SX600 Data List adds no new descriptions. Source: Yamaha, PSR-SX600 Data List (EN, B0, 10/2020). https://usa.yamaha.com/files/download/other_assets/8/1346928/psrsx600_en_dl_b0.pdf. Type: official (other model). Applies to: PSR-SX600. Trust: high (official document; comparison reproducible).

**[E3]** The MU128 "Sound List & MIDI Data" (XG tone generator) has an "Explanation of effect parameters" table (PDF pages 22–23): each parameter name, the XG effect types that use it, and a one-line explanation, e.g. Edge (Clip Curve) "Curve of distortion characteristics (sharp(127) distorts suddenly, mild(0) distorts gradually)", Delay Mix "Mixing amount of delay sound", High Damp "Attenuation of the high frequency range". The DGX's effect parameter names largely come from this XG lineage. Source: Yamaha, MU128 Sound List & MIDI Data (MU128E2.pdf). https://usa.yamaha.com/files/download/other_assets/1/318081/MU128E2.pdf. Type: official (other model). Applies to: XG effects (ancestors of the DGX's). Trust: high for meaning; ranges may differ from the DGX.

**[E4]** Yamaha's Synthesizer Parameter Manual (MONTAGE/MODX edition, EN c0, 90 pages) has an alphabetical Effect Parameters glossary (PDF pages ~66–89, about 400 entries including effect-type descriptions), e.g. Presence "For Amp Simulator effects this parameter controls high frequencies", Device "Selects the device for changing how to distort the sound", Overdrive "Determines the degree and character of the distortion effect", Edge "Sets the curve that determines how the sound is distorted". Source: Yamaha, Synthesizer Parameter Manual. https://usa.yamaha.com/files/download/other_assets/1/812531/synthesizer_en_pm_c0.pdf. Type: official (other models). Applies to: Yamaha AWM2/FM-X synths; shared effect terminology. Trust: high for meaning; not proof that the DGX implementation is identical.

**[E5]** An older edition of the Synthesizer Parameter Manual (AWM2 synths, EN a0, 74 pages; glossary on PDF pages ~48–65) adds some older-style names, e.g. Speaker Type "Selects the type of speaker simulation". Source: Yamaha. https://usa.yamaha.com/files/download/other_assets/7/323557/synth_en_pm_a0.pdf. Type: official (other models). Applies to: Motif-era synths. Trust: high for meaning.

**[E6]** Combined, [E3]–[E5] explain 179 of the DGX's 194 effect parameter names (146 exact name matches, 33 via an alias list for wording differences such as "Lch Delay Time" = "Lch Delay", "Feedback High Dump" = "High Damp"). The per-parameter index with definitions, source and PDF page is `kb/external/effect_param_glossary.csv` (built 2026-10-02). Unmatched: Ambience, Coarse, Connect Mode, Delay Ctrl, High/Low/Mid Gain Offset, Horn, Middle, Offset, On/Off SW, Rotor SW, Threshold Offset, Time, Woofer. Source: [E3]–[E5] (same URLs). https://usa.yamaha.com/files/download/other_assets/1/318081/MU128E2.pdf. Type: official (other models), indexed here. Applies to: DGX-670 parameter names. Trust: high for meaning; "alias" rows are this KB's mapping.

**[E7]** The MOTIF XF Data List has the same parameter tables for V Distortion (Overdrive 0–100%, Device Transistor/Vintage Tube/Distortion 1/Distortion 2/Fuzz, Speaker Type Flat/Stack/Combo/Twin/Radio/Megaphone), but shows Presence as −10…+10 for data 0–20 (the DGX Data List shows 0–20 [DL p.37]). It gives no parameter explanations. Source: Yamaha, MOTIF XF Data List (EN C0), PDF pages ~98–100. https://usa.yamaha.com/files/download/other_assets/3/325083/motifxf_en_dl_c0.pdf. Type: official (other model). Applies to: MOTIF XF. Trust: high (display difference may be model-specific).

**[E8]** Paul Drongowski maps PSR effect types to MOX/Motif algorithms: MOX "AmpSim 1" = PSR "V_DIST CRUNC" (MSB 98 / LSB 18) and also "V_DIST WARM"; MOX "AmpSim2" = PSR "AMP SIM2"; MOX "CompDistDly" ≈ PSR "V_DST H+DLY". His PSR translations of MOX electric-piano amp settings use Device Vintage Tube, Speaker Stack, Presence +10, low Overdrive (2–15 %). Source: Sand, software and sound, "Crunchin' da drums" (2015-08-18) and "PSR effects for electric piano (Part 1)" (2015-11-30). https://sandsoftwaresound.net/psr-effects-electric-piano-1/ and https://sandsoftwaresound.net/crunchin-da-drums/. Type: third-party doc (expert blog). Applies to: PSR-S950 / MOX (same effect families as the DGX). Trust: medium-high.

**[E9]** A Yamaha synth-forum regular recommends the SPX2000 effects-processor manual for detailed descriptions of effects used in MONTAGE/MODX, noting parameter counts and ranges can differ. Not downloaded or checked here. Source: Yamaha Synth forum, "Lots of detailed info on Montage M/Montage/MODX effects in SPX2000 manual", Pete, 2024-11-23. https://yamahasynth.com/community/montage-series-synthesizers/lots-of-detailed-info-on-montage-m-montage-modx-effects-in-spx2000-manual. Type: forum. Applies to: Yamaha effect algorithms generally. Trust: medium (pointer only).

**[E10]** GitHub repository ltgcgo/midi-db (CC-BY-SA-4.0) holds TSV/JSON maps of XG bank/program numbers for MU-series and PLG boards; no arranger (PSR/DGX/Tyros/Genos) data and no voice or effect descriptions. Source: GitHub. https://github.com/ltgcgo/midi-db. Type: third-party doc. Applies to: XG devices. Trust: medium; low value here (the DGX's own numbers are already in `voices.csv`).

**[E11]** demodb.org's DGX-670 page streams the main demo and the 100 preset Songs only; no per-Voice or per-effect audio. Source: demodb.org. https://demodb.org/en/yamaha/dgx/dgx-670. Type: third-party doc. Applies to: DGX-670. Trust: high (checked page).

**[E12]** A Yamaha guitar-effects-processor Effect List (EffectList_E.pdf) describes amp-model parameters (Gain, Treble, Presence "Adjusts level of extremely high frequencies", speaker simulator cabinets) for a different product family; useful vocabulary only. Source: Yamaha. https://usa.yamaha.com/files/download/other_assets/1/319541/EffectList_E.pdf. Type: official (other product). Applies to: Yamaha guitar processors. Trust: low relevance (different implementation).

## Not found
- Per-Voice descriptions (what each named Voice sounds like) for the DGX-670, PSR-SX600 or related models — as of
  2026-10-02. Names, numbers and Voice-type labels are all that is published.
- Systematic "every Voice" audio/video demos for the DGX-670 or PSR-SX600 (search tools returned none; a manual
  YouTube search may still find some).
- A machine-readable (CSV/JSON) list of arranger Voices or DSP types with descriptions (GitHub, PyPI).
- PSR Tutorial articles could not be read directly (the site blocks automated fetches); only search excerpts were seen.

## Practical takeaway
- To learn what an effect parameter does: look the DGX name up in `kb/external/effect_param_glossary.csv` (external,
  not from the manuals) [EXT yamaha-cross-model-references#E6]; ranges and values always come from the Data List.
- Treat PSR-SX600 reviews, demos and forum threads as applying to the DGX-670 for shared Voices/effects
  [EXT yamaha-cross-model-references#E1, #E2].
- For guitar-amp style tones, the V Distortion settings that MOX's "AmpSim 1" uses on PSRs (Vintage Tube + Stack,
  Presence up) are a documented starting point [EXT yamaha-cross-model-references#E8].
- Which factory Voices already use amp/distortion DSPs (lab-tested, not from the manuals): `kb/lab/preset_voice_map.csv`.
