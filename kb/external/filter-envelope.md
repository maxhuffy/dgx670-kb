# Is there a filter envelope (contour) on the DGX-670, or a way to fake one?
topic: Filter envelope / filter contour (MG-1 style) on the DGX-670 and workarounds
status: partial
researched: 2026-09-30
manual_gap: RM p.15 says the EG "determine[s] how the level of the sound changes in time" and gives no filter-envelope amount. The filter can be moved only by the Modulation controls (Modulation → Filter, LFO FMOD) [RM p.14] or by effects such as DynFilter / TouchWah [DL p.28, p.32].
queries: "DGX-670 OR PSR-SX600 OR PSR-SX700 filter envelope synth voice set filter sweep"; "Yamaha XG filter EG OR EG affects filter shared envelope attack decay brightness sweep"; plus the filter-slope searches
summary: No separate filter envelope. In the related XG architecture one EG drives both filter and amp (Sound On Sound), so EG Attack/Decay changes may also sweep the filter (untested on the DGX). Best documented workaround: the DynFilter effect (tier 1).

## Manual baseline
- **Voice EG:** Attack / Decay / Release, described as shaping the level [RM p.15]. The Voice Set has no
  filter-EG-depth parameter [RM p.13–16].
- **Filter modulation available:**
  - Controller page → Modulation **Filter** (a Modulation pedal moves the cutoff) and **LFO FMOD** (filter wobble)
    [RM p.14]. Modulation is a continuous pedal function needing an FC3A or LP-1B/LP-1WH [RM p.76–77].
  - Pitch Bend can also move the filter: the SysEx "BEND LOW PASS FILTER CONTROL" is received by Song parts and by
    Main/Layer/Left [DL p.65]. How to send it from the panel is not documented.
- **Level-following filter effects (tier 1):**
  - **DynFilter**: cutoff moved by the input level, with Attack 0.3–227 ms, Release 2.6–2171.4 ms, Direction
    Up/Down, Threshold, and LPF(24dB) available [DL p.32, p.43].
  - **TouchWah1** / **TcWah+Dist1**: a Touch Wah, the latter with distortion after it [DL p.28–29].

## Findings
**[E1]** In the XG voice architecture, the low-pass filter "is modulated from the main envelope generator, which also controls the amplifier output level". The author calls this shared EG one of XG's main sound-design limitations. His example: raising resonance and the main EG attack makes harmonics "surface" slowly, i.e. the filter follows the EG. Source: Sound On Sound, Mike Senior, "Creative Synthesis With Yamaha XG (Part 1)", April 2004. https://www.soundonsound.com/techniques/creative-synthesis-yamaha-xg-part1 Type: third-party doc. Applies to: XG tone generators, not tested on the DGX-670. The DGX exposes the same XG EG/filter offsets [DL p.60, p.65]. Trust: medium.

**[E2]** The DGX-670's internals are said to be closely based on the PSR-SX600; the two share about 80% of features. So PSR-SX600 synth-programming tips are the most likely to carry over. Source: Jeremy See, "Compare: Yamaha's Best Prosumer Keyboards Compared — DGX-670 vs PSR-SX600". https://www.jeremysee.info/post/compare-yamaha-s-best-prosumer-keyboards-compared-dgx-670-vs-psr-sx600 Type: third-party review. Applies to: DGX-670 vs PSR-SX600. Trust: medium (a reviewer's comparison, not a Yamaha statement).

**[E3]** Yamaha's Dynamic Filter moves its cutoff "in response to the incoming signal", scaled by Sensitivity. See [EXT filter-slope-24db#E3]. Source: YamahaSynth community, Bad Mister (Yamaha), 2018-01-19. https://yamahasynth.com/community/postid/27018/ Type: official (staff forum post, MONTAGE). Applies to: an effect of the same name on another model. Trust: medium-high.

## Not found
As of 2026-09-30, nothing found that:
- documents or tests a filter-EG amount on the DGX-670 or PSR-SX600;
- shows a DGX-670 user building a filter sweep / contour;
- confirms whether Voice Set EG Attack/Decay also move the filter on the DGX (as on XG, [E1]).

## Practical takeaway
- **Try the shared-EG behaviour:** raise Harmonic Content, then lengthen EG Attack or shorten Decay, and listen for
  the filter moving along with the volume [RM p.15]. Whether it does is external [E1] and untested.
- **Per-note "contour" (tier 1 + by ear):** DSP Type **DynFilter**, LPF(24dB), Direction Up. Use a fast Attack Time
  and a Release Time of a few hundred ms. Raise Sensitivity until each note's attack opens the filter, then it closes
  as the level settles [DL p.43]. The exact behaviour of each parameter is not documented, so tune by ear.
- **Manual sweeps:** set a continuous pedal (FC3A / LP-1 right pedal) to Modulation, with Modulation → Filter depth
  in the Voice Set [RM p.14, p.76–77].
