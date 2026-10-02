# DGX-670 Voice files (.vce and related): internal format, and generating new Voices on a PC
topic: Internal format of DGX-670 Voice (Voice Set) files, panel-value mapping, and generating edited Voices on a computer
status: partial
tested: 2026-10-01
evidence: initial_dgx_voices_saved_to_usb/ (all 630 preset Voices + kits copied from the Preset tab, plus CFX Grand M/NM test pair in NewFolder/); settings_screenshots/ (Voice Set pages of SL0 and SL3, SL3 DSP Detail); generated_voices/batch1, batch2 and tools/ (vce.py decoder, gen.py generator)
summary: A Voice file is a ~670-byte Standard MIDI File of XG parameter messages (part 0, insertion effect 0) plus ~12 Yamaha-specific messages; no checksum, no encryption, name = filename. Files generated on a PC load and play; panel values map to file values by simple rules (confirmed from screenshots). Field map: voice_file_fields.csv.

## Manual baseline
- Voice Set edits are saved as a file to the User drive or a USB flash drive [RM p.12]. The Voice Set pages are
  Common, Controller, Sound, Effect/EQ and Harmony [RM p.13–16].
- The Parameter Chart lists what a Voice Set stores: Voice, Volume, Touch Sense, Part Octave, Mono/Poly, Mono Type,
  Portamento, Modulation, Filter, EG, Vibrato, Reverb/Chorus Depth, DSP On/Off, DSP Depth, DSP Type, EQ, Harmony,
  pedal functions [DL p.47–49, DL p.53–54]. It has no row for the DSP Detail values.
- Files can be copied from the Preset tab (folders too, with [8▼] All) to USB [OM p.29].
- The XG parameter addresses, NRPNs and effect type numbers used inside the files are the Data List's MIDI tables
  [DL p.58–68] and effect lists [DL p.25–45].
- External background: Yamaha arranger Voice files are Standard MIDI Files [EXT usb-file-formats#E4, #E5].

## Findings
**[L1]** Copying the Preset Voice folders to USB (OM p.29 procedure) produces one file per Voice: 630 files = the 601
Voices + 29 Drum/SFX kits of the panel spec. Every file's Bank MSB/LSB + Program matches a Main/Legacy/MegaVoice row of
`voices.csv`. Status: confirmed. Evidence: initial_dgx_voices_saved_to_usb/ (user copied the whole library in minutes).

**[L2]** The file extension is the Voice Type from the Voice List: vce = Regular (362), liv = Live! (68), clv = Cool!
(53), sar = S.Art! (49), swv = Sweet! (26), mgv = MegaVoice (23), drm = Drums (12), nlv = Natural! (11), ldr =
Live!Drums (10), vrm = VRM (9), sfx = SFX (4), lsf = Live!SFX (3). Status: confirmed (630/630). Evidence: library.

**[L3]** File names are `<Name>.T<nnn>.<ext>` (e.g. `SawLead.T248.vce`). The name shown on the display is the file
name; no name is stored inside the file. The meaning of `T<nnn>` is unknown; keeping the donor's value works.
Status: confirmed (renamed files show their new names). Evidence: SL0/SL3 screenshots.

**[L4]** Container: Standard MIDI File, format 0, one track, 96 ticks per quarter note; 4/4 time-signature and
120 bpm tempo meta events; every event 5 ticks apart; all channel messages on MIDI channel 1. Files are ~650–700
bytes and contain 61–64 events in 12 structural variants. No checksum and no encryption. Status: confirmed.
Evidence: all 632 files parse; the re-serialised SawLead is byte-identical to the original.

**[L5]** Contents: (a) the base Voice as Bank Select MSB/LSB + Program Change; (b) channel CCs and XG NRPNs for
Attack, Decay, Release, Brightness, Harmonic Content, Vibrato, Portamento, Reverb/Chorus Depth [DL p.58, DL p.60];
(c) XG Multi Part parameter changes for **part 0** (Mono/Poly, Touch Sense, Modulation, part EQ) [DL p.65–66];
(d) XG insertion effect **0** type + all its parameters = the Voice's DSP [DL p.64]; (e) about 12 Yamaha-specific
messages (`F0 43 73 01 50/51 …`) not in the Data List (Volume, Part Octave, DSP On/Off, Harmony, pedals, two
DSP-related IDs). Field-by-field map with statuses: `voice_file_fields.csv`. Status: confirmed (structure).

**[L6]** Mono/Poly is XG `08 00 05` (00 = Mono, 01 = Poly). Status: confirmed. Evidence: the user's CFX Grand
NM vs M files (only Mono/Poly changed on the panel) differ in exactly this one byte.

**[L7]** Panel ↔ file value rules, confirmed on the Voice Set display (SL0 = unmodified SawLead, SL3 = generated):
- Sound page (Brightness, Harmonic Content, Attack, Decay, Release, Vibrato Depth/Speed/Delay): panel = file − 64.
- Common page (Volume, Touch Sense Depth/Offset, Portamento Time): panel = file value.
- Part Octave (Main/Layer and Left): panel = file − 64.
- Controller page (Modulation Filter/Amplitude, LFO PMOD/FMOD/AMOD): panel = file value.
- Effect/EQ page: Reverb/Chorus Depth = file value; DSP Depth = insertion parameter 10 (Dry/Wet) = file value;
  EQ frequencies via Table #3 [DL p.45]; EQ gains dB = file − 64.
Status: confirmed for every field changed in SL3 (Touch Sense Depth, Mono, Portamento, Attack, Decay, Release,
Vibrato Depth, Brightness, Harmonic Content, Reverb Depth, DSP Type, DSP Depth); defaults-only for the rest.
Evidence: settings_screenshots/ (10 images, 2026-09-30).

**[L8]** DSP Type is the XG insertion effect type MSB/LSB from `effect_types.csv` (Variation/Insertion block): SawLead
= 1/18 "Hall 4", generated SL3 = 74/8 "Stereo Overdrive", both shown so on the panel. Status: confirmed.

**[L9]** The Voice file carries the DSP **Detail** values (insertion parameters 1–16) even though the Parameter Chart
has no Detail row [DL p.47]. Parameter names/ranges come from `effect_params.csv` (e.g. Stereo Distortion list:
Drive, EQ Low Freq/Gain, LPF Cutoff, Output Level, EQ Mid Freq/Gain/Width, Dry/Wet, Edge [DL p.37]). Status: likely:
present in every file, and variants differing only in Drive/Edge/Mid Gain sound different. **Update 2026-10-01:
confirmed.** SL3's Detail display shows all ten Stereo Overdrive values exactly as written: Drive 70, EQ Low 315 Hz /
0 dB, LPF 7.0 kHz, Output Level 105, EQ Mid 1.0 kHz / +8 dB / Width 1.0, Dry/Wet D<W36, Edge 80. Conversions:
plain 0–127 parameters = file value; frequencies via Table #3 [DL p.45]; gains dB = file − 64; EQ Mid Width =
file ÷ 10; Dry/Wet 64 = D=W, above 64 = D<W(file − 64), below 64 = D(64 − file)>W. Status: confirmed.
Evidence: settings_screenshots/sl3_effect_eq_details_1.png, _2.png.

**[L10]** Two Yamaha-specific fields (`51 08 00 11` and `51 08 00 12`) track the DSP type but are not a unique ID per
type. Safe method: when changing the DSP type, copy the whole DSP block (XG `03 00 00` through `51 08 00 12`) from a
preset file that already uses the target type ("donor"), then edit parameters. Donors used: SmoothLead (Stereo
Overdrive 74/8), WazzoSaw (DynFilter 109/0). Status: confirmed that donor-spliced files load and show the right DSP
type (SL3). Whether changing only the XG type (no donor) works: untested.

**[L11]** Changing only Bank/Program retargets a file to another base Voice (SQ5: SawLead file → SquareLead
0/112/81). Status: confirmed that it loads and plays (user played it, 2026-09-30); the panel display of the base Voice
was not checked.

**[L12]** Generated files load from the USB1 tab and play; no Save on the keyboard is needed to audition them.
Status: confirmed (batch 1, all six files).

**[L13]** Mono Type is XG `0A 00 02` (Portamento Mono Legato): 00 = Normal, 01 = Legato. Status: confirmed. Evidence:
the user's clone of SL0 saved with Mono + Legato ("SL0 Copy CHANGD", 2026-10-01) differs from SL0 in exactly Mono/Poly
(01 → 00) and this byte (00 → 01), apart from the pedal message in [L15].

**[L14]** DSP On/Off is the Yamaha-specific `50 08 00 08`: 7F = On, 00 = Off. Status: confirmed. Evidence: SL0/SL3
(7F) show On; SL1 Dry (00) shows Off (2026-10-01).

**[L15]** Pedal settings are Yamaha-specific `51 00 01 00 08 1p ff 00 mm …`: p = 1 Center Pedal, p = 0 Left Pedal;
ff = function (05 = Modulation, 02 = Soft, one example each); mm = part checkmarks (bits 1 = Main, 2 = Layer,
4 = Left). SawLead's preset file has only the Center Pedal message (Modulation, Main + Layer); when the keyboard
saved the clone it also wrote the Left Pedal message (Soft, all three parts), which matches what the Controller
page shows for SL0. The file grows to 689 bytes as a result. Status: likely (layout fits both messages and the
display; only two function codes seen). Evidence: SL0 Copy CHANGD vs SL0; settings_screenshots/sl0_controller.png.

**[L16]** Files saved by the keyboard carry the date 2019-12-31 (the instrument does not stamp the real date).
Status: confirmed (all preset copies and the user's clone). Evidence: file listings.

## Experiment log
- 2026-09-30, CFX Grand NM/M (user-made): one-byte difference = Mono/Poly [L6].
- 2026-09-30, batch 1 (SawLead template, `generated_voices/batch1/`): SL0 Copy (byte-identical control), SL1 Dry
  (recipe Step 2 settings + DSP off), SL2 OD (Step 2 + Stereo Overdrive: Drive 40, Edge 40, LPF 7.0 kHz, Mid 1.0 kHz
  +5 dB), SL3 OD Hot (Drive 70, Edge 80, Mid +8 dB), SL4 DynFlt (Step 2 + DynFilter LPF 24 dB), SQ5 OD (SL2 on
  SquareLead). Step 2 = Mono, Portamento 0, Touch Sense Depth 16, Attack −64, Decay +48, Release −16, Vibrato Depth
  −64, Brightness +16, Harmonic Content +16, Reverb 16, Chorus 0. Result: all loaded; user found SL3 closest to the
  target (a distorted, crunchy synth lead), SL2 OK, the others too "electric"/"chiptune". User: Reverb Depth 16 was
  far too high, about 6 better.
- 2026-09-30, batch 2 (`generated_voices/batch2/`, not yet tested): SL3 + Reverb 6, each with one change: Drive 90;
  LPF 5.0 kHz; Mid 800 Hz +10 dB width 0.5; Edge 110; Dry/Wet 127.

- 2026-10-01, follow-up checks: SL1 Effect/EQ shows DSP Off [L14]; SL3 DSP Detail shows all ten values as written
  [L9]; user's clone "SL0 Copy CHANGD" (Mono + Legato) settles Mono Type [L13] and shows the pedal message layout
  [L15].

## Open questions
- Retarget display [L11]: does SQ5 show SquareLead as its Voice?
- Portamento Time type (`0A 00 03`, 00 = Fixed Rate): the other option's value is untested.
- DSP type swap without a donor [L10]; Harmony and pedal encodings; the `T<nnn>` suffix; 2-byte DSP parameters
  (addresses 30–42) used by types that need MSB, e.g. V Distortion.
