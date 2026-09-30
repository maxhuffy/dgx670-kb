# Externally Researched Topics

Online research (forums, Reddit, Yamaha support pages, videos, third-party docs) on gaps the DGX-670 manuals
leave open. **Lower trust than the manuals**: cite as `[EXT <slug>#E<n>]` and label "(external, not from the
manuals)". `nothing-found` rows are dated so they can be re-checked later. Format and rules: `README.md`.

| Topic | File | Status | Researched | Summary |
|---|---|---|---|---|
| Amp envelope on the DGX-670: no Sustain Level parameter (Attack/Decay/Release only) | [amp-envelope-sustain-level](amp-envelope-sustain-level.md) | found | 2026-09-30 | Confirmed: the XG-style part envelope has Attack/Decay/Release offsets only. The sustain level is fixed by each Voice's preset. Workaround: long Decay (or pick a Voice that already holds), plus a compressor for evenness. |
| Bass amplifier / bass cabinet simulation (e.g. Ampeg SVT + 8×10) on the DGX-670 | [bass-amp-simulation](bass-amp-simulation.md) | nothing-found | 2026-09-30 | Nothing found online (as of 2026-09-30) about a bass-amp model on the DGX-670 or its PSR-SX600 sibling. Closest documented: amp sims with Stack cabinets plus EQ. |
| Filter envelope / filter contour (MG-1 style) on the DGX-670 and workarounds | [filter-envelope](filter-envelope.md) | partial | 2026-09-30 | No separate filter envelope. In the related XG architecture one EG drives both filter and amp (Sound On Sound), so EG Attack/Decay changes may also sweep the filter (untested on the DGX). Best documented workaround: the DynFilter effect (tier 1). |
| Voice filter slope (Brightness/Harmonic Content) and a true 24 dB/oct resonant low-pass on the DGX-670 | [filter-slope-24db](filter-slope-24db.md) | partial | 2026-09-30 | The Voice filter's slope is not published anywhere found (manuals, Yamaha XG docs, forums). A real LPF(24dB) with Resonance exists as the DynFilter insertion effect (tier 1, Data List). |
| Oscillator hard sync, ring modulation and noise on the DGX-670 (MG-1-style features) | [sync-ringmod-noise](sync-ringmod-noise.md) | partial | 2026-09-30 | Ring mod exists as an effect (RingMod, DynRingMod: tier 1, Data List). Noise only as sampled noise Voices (GM/XG, reachable via community files) or the Lo-Fi effect. Hard sync: nothing found online. |
| Choosing a saw/pulse/square source for synth leads; hidden GM/XG synth-lead Voices; loading new waveforms | [synth-waveform-voice-choice](synth-waveform-voice-choice.md) | found | 2026-09-30 | No waveform choice and no expansion packs. But the hidden GM/XG synth leads (SawtoothLead1/2, PulseSaw, SawPulseLead, DoublSawLead, SquareLead1/2, LM Square…) can be played via community-made User Voice files loaded from USB. |
