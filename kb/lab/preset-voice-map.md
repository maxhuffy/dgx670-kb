# Default DSP and mix settings of every DGX-670 preset Voice
topic: Default DSP effect type, reverb/chorus depth and mono/poly of all 630 preset Voices and kits, decoded from their Voice files
status: confirmed
tested: 2026-10-02
evidence: initial_dgx_voices_saved_to_usb/ (630 preset Voice files copied from the Preset tab); decoded with scripts/voicefile.py
files: preset_voice_map.csv
summary: One row per preset Voice/kit with its default DSP type (named via effect_types.csv), DSP on/off and depth, reverb/chorus depth, mono/poly and volume. 58 Voices use distortion/amp DSPs, including three synth leads (TechGlide, ClubLead, CryingLead); delay-type DSPs and reverb 19–28 are the usual sources of sound after key release.

## Manual baseline
- Each Voice brings its own DSP (insertion effect) type; DSP Type and DSP On/Off are stored with the Voice Set
  [DL p.47]. The Data List names the effect types and their MSB/LSB [DL p.25–32] but does not say which Voice uses
  which effect.
- Voice names, categories, MSB/LSB/PC and Voice types: [DL p.3–12] (`kb/datalist/csv/voices.csv`).

## Findings
**[L1]** `preset_voice_map.csv` lists all 630 preset Voices/kits with: name, section, category, Voice type, MSB/LSB/PC,
preset file, DSP on/off, DSP type name, DSP category, DSP algorithm (parameter list), DSP MSB/LSB, DSP depth
(Dry/Wet), Reverb Depth, Chorus Depth, mono/poly, Volume. Every file's effect type is found in the Data List's
Variation/Insertion list. Status: confirmed (decoded from the instrument's own files; field meanings per
[LAB voice-file-format#L5–L14]).

**[L2]** Most common default DSP algorithms: REVERB1 (105 Voices), TEMPO DELAY (97), CHORUS (56), TEMPO CROSS DELAY (51),
HARMONIC ENHANCER (42), ENSEMBLE DETUNE (29), CROSS DELAY (25), ECHO (23), TREMOLO (23), 3BAND EQ (20), STEREO AMP
SIMULATOR (20). Status: confirmed.

**[L3]** 58 Voices use a distortion or amp-type DSP (V Distortion, V Dist (Tempo) Delay, Comp Dist (Tempo) Delay,
Stereo Amp Simulator, Amp Simulator 1/2, British Combo/Legend, Stereo/plain Distortion, Auto Wah Distortion). Besides
guitars, organs and saxes, three are synth leads: **TechGlide** (Legacy Synth; Cmp+OD+TDly2 = compressor + overdrive +
tempo delay; mono; Reverb 3), **ClubLead** (Synth & Pad; AmpSim2 = Amp Simulator 2; mono; Reverb 15) and
**CryingLead** (Synth & Pad; AtWah+Dist1 = auto wah + distortion; Reverb 9, Chorus 17). Status: confirmed (filter the
CSV on `dsp_algorithm`).

**[L4]** Sources of sound after key release in the presets: Reverb Depth is typically 12–28 on guitar Voices (up to 38
on the MegaVoice DistortionGuitar), and many guitar DSPs include a delay (V DISTORTION DELAY, V DIST TEMPO DELAY,
COMP DIST TEMPO DELAY). Setting Reverb/Chorus Depth to 0 and the DSP's Delay Mix to 0 removes these
[LAB voice-file-format, batch 3]. Status: confirmed for the decoded values; likely for the audible result (batch 3's
tail-free guitars were tested, but the user did not comment on the tails specifically).

## Experiment log
- 2026-10-02: built from the 630-file preset library with `scripts/voicefile.py` while looking for factory Voices that
  combine a synth sound with guitar-amp style processing.

## Open questions
- Do TechGlide / ClubLead / CryingLead come closer to the target "crunchy guitar-like synth" riff than batch 3's G4?
- Per-Voice sound descriptions do not exist in the manuals or online [EXT yamaha-cross-model-references]; tags could
  be added here from the user's listening notes.
