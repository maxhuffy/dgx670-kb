# What is the slope of the DGX-670 Voice filter, and can I get a Moog-style 24 dB/oct resonant low-pass?
topic: Voice filter slope (Brightness/Harmonic Content) and a true 24 dB/oct resonant low-pass on the DGX-670
status: partial
researched: 2026-09-30
manual_gap: RM p.15 describes Brightness (cutoff) and Harmonic Content (resonance) without a slope. The Data List **does** offer a 24 dB low-pass as an effect: DynFilter, Filter Type LPF(24dB) [DL p.32, p.43].
queries: "Yamaha AWM2 tone generator filter slope 12dB 24dB PSR DGX voice brightness harmonic content resonance"; "Yamaha XG filter cutoff resonance NRPN 12dB low pass filter type XG tone generator"; "XG tone generator voice low pass filter 12dB/oct OR 24dB/oct slope MU80 MU100 resonance"
summary: The Voice filter's slope is not published anywhere found (manuals, Yamaha XG docs, forums). A real LPF(24dB) with Resonance exists as the DynFilter insertion effect (tier 1, Data List).

## Manual baseline
- **Voice filter:** Brightness = "the cutoff frequency or effective frequency range of the filter" and Harmonic
  Content = "the emphasis given to the cutoff frequency (resonance)" [RM p.15]. No slope is given.
- These are offsets from the Voice's preset (−64…0…+63), per the MIDI tables:
  - NRPN "Low Pass Filter Cutoff Frequency" / "Resonance" [DL p.60];
  - SysEx Multi Part "FILTER CUTOFF FREQUENCY −64…0…+63" / "FILTER RESONANCE" [DL p.65].
- **DynFilter effect (tier 1):** "Dynamically controlled filter" [DL p.32]. Parameters [DL p.43]:
  - Filter Type LPF(12dB) / LPF(18dB) / **LPF(24dB)** / HPF / BPF / BEF;
  - Resonance −16…0…+111;
  - Sensitivity, Dyna Level Offset, Attack Time 0.3–227 ms, Release Time 2.6–2171.4 ms, Release Curve;
  - Direction Up/Down, Dyna Threshold Level, Dry/Wet, EQ Low/High.

  It's a Legacy Variation/Insertion type, so it can be a Voice's DSP Type [DL p.32; RM p.16].

## Findings
**[E1]** In Yamaha's XG voice architecture, a sampled waveform goes through a low-pass filter (Cutoff Frequency + Resonance) and an amplifier. The filter "is modulated from the main envelope generator". The article gives no slope. Source: Sound On Sound, Mike Senior, "Creative Synthesis With Yamaha XG (Part 1)", April 2004. https://www.soundonsound.com/techniques/creative-synthesis-yamaha-xg-part1 Type: third-party doc (magazine). Applies to: XG tone generators (the DGX-670 uses the same XG parameters [DL p.60, p.65]; its internal engine isn't described). Trust: medium.

**[E2]** Yamaha's MU100 XG documentation lists filter cutoff/resonance parameters but no slope. Source: Yamaha, "MU100 Tone Generator Sound List & MIDI Data". https://usa.yamaha.com/files/download/other_assets/9/318079/MU100E2.pdf Type: official (another model). Applies to: related XG model. Trust: high for "not stated".

**[E3]** How Yamaha's "Dynamic Filter" works (Yamaha staff): the cutoff moves "in response to the incoming signal", with **Sensitivity** setting how much. On the MONTAGE, a side-chain can use another Part as the trigger. Source: YamahaSynth community, "Dynamic Filter? Control Filter?", Bad Mister (Yamaha), 2018-01-19. https://yamahasynth.com/community/postid/27018/ Type: official (Yamaha staff on forum). Applies to: MONTAGE effect of the same name. The DGX-670 DynFilter has no side-chain parameter [DL p.43]. Trust: medium-high.

## Not found
As of 2026-09-30, nothing found (official, forum, Reddit) giving the slope of the Voice filter on the DGX-670, PSR or
XG models, and no DGX-670 user report on using DynFilter.

## Practical takeaway
- For a guaranteed 24 dB/oct resonant low-pass, set the lead Voice's DSP Type to **DynFilter**, Filter Type
  **LPF(24dB)**, and add Resonance to taste [DL p.43; RM p.16].
- For a static filter, keep Sensitivity low; how low Sensitivity behaves isn't documented, so try it by ear.
- It uses the part's one insertion DSP, so drive has to go elsewhere, e.g. on a Layer part [RM p.68–69].
- Brightness/Harmonic Content still work on top of it [RM p.15].
