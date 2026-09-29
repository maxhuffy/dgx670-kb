# Data List table briefs

Hand-written, search-oriented descriptions of every Data List CSV, made by reading each CSV together with its
PDF pages. `scripts/build_datalist.py` merges them into `kb/datalist/INDEX.md`. Keep one `## <csv key>`
section per CSV; the build fails its check if one is missing. They live here rather than under kb/ so that
searches don't hit each brief twice.

## piano_types
The 6 piano and electric-piano Voices selectable as the piano type in Piano Room: CFX Grand, PopGrand, HonkyTonk,
SuitcaseEP, VintageEP, SweetDX. One row per selectable piano type. Answers "which pianos / piano sounds can I pick
in Piano Room". Piano Room itself is covered in [OM p.35–37].

## voices
The complete Voice List: every Voice (instrument sound) with its category, Voice name, Bank Select MSB/LSB and Program
Change number (PC# 1–128), and Voice Type. Voice Types: VRM, S.Art! (Super Articulation), Natural!, Sweet!, Cool!, Live!,
MegaVoice, Drums / Live!Drums, SFX / Live!SFX, Regular. `section` groups the list:
- **Main** is the panel Voice categories: Piano & E.Piano, Organ & Accordion, Guitar & Bass, Strings & Choir,
  Brass & Woodwind, Perc. & Drums, Synth & Pad.
- **Legacy** and **MegaVoice** are further built-in sets, with sub-categories.
- **GM & XG** (480) and **GM2** (265) are General MIDI / XG compatibility sounds.

Main + Legacy + MegaVoice = 601 Voices + 29 Drum/SFX Kits, exactly the spec count [OM p.106]. The same name can appear
more than once with different numbers and types (e.g. CFX Grand is VRM 108-0-1 and Natural! 0-122-1).

Answers: a Voice's MSB/LSB/PC (to select it via MIDI from a computer/DAW or a Song), which category a Voice is in,
which Voices are VRM / Super Articulation / Live!, how many Voices of a type exist.

## songs
The 100 preset Songs (internal MIDI songs). "50 Popular" has categories Let's Play, Sing-a-long and Follow Lights;
"50 Classics" has Arrangements, Duets and Original Compositions. Columns: title, composer, and (50 Popular only)
lyricist and lyric data (○ = the Song contains lyric data, shown on the Lyrics display). Answers "is song X built in",
"which preset songs have lyrics", "who composed preset song X". Songs chapter: [OM p.60].

## styles
All 263 Styles (auto-accompaniment rhythms), in 8 categories: Pop & Rock, Ballad, Dance & R&B, Country & Blues,
Standards & Jazz, Entertainment, Latin & World, PIANIST. The `unison` and `adaptive` columns show which Styles support
Unison (the Unison & Accent feature [OM p.54]) and Adaptive Style [OM p.51] ("-" = not supported). Answers "which
Styles support Unison / Adaptive", "what category is Style X in", "how many jazz/latin Styles".

## effect_types
All 463 effect types (DSP / reverb / chorus / variation / insertion effect algorithms): Reverb Block (59), Chorus Block
(107), Variation/Insertion Block (297). Each row has number, category (e.g. Reverb, Delay, Modulation, Distortion,
EQ & Comp, Misc, Legacy), type name, a one-line description of the sound, the effect-type MSB/LSB (used in MIDI/XG
effect-type messages), and the Parameter List name that defines its editable parameters (see `effect_params`).
Answers "what does effect type X sound like", "which reverb/delay/distortion types exist", "what are its MIDI numbers".

## effect_params
The Effect Parameter List: for each effect algorithm's parameter list (REAL REVERB, REVERB1…, DELAY LCR, ROTARY SPEAKER,
DISTORTION, COMPRESSOR, RING MODULATOR, ISOLATOR, etc.), the blocks that can use it (Reverb, Chorus, Variation, DSP1–5)
and each parameter's number (1–16), name, display range, min/max data values, and the value table (`Table #n` →
`effect_data_tables`) that converts data to real units. `control_ac1 = yes` (● on the page) means the parameter can
be controlled from AC1 (assignable controller 1); that only affects insertion-type effects. Display values marked (*1)
apply in the Reverb Block and (*2) in the Chorus/Variation/Insertion blocks. Unused parameter numbers are omitted, and
lists printed with "No parameters" have one "(no parameters)" row. Answers "what parameters does effect X have and
what are their ranges".

## effect_data_tables
The Effect Data Assign Table: 22 lookup tables ("Table #1"…"Table #40") that map an effect parameter's data value
(0–127) to its real value: Reverb Time [s], Delay Time [ms], EQ Frequency [Hz], Room Size, LFO Frequency [Hz],
Modulation/Flanger delay offset, Dyna and Compressor attack/release times [ms], Compressor Ratio, Wah Release Time,
Rotary speaker slow/fast speed [rpm], LO-FI sampling frequency, Ring Mod oscillator frequency. One row per data→value
pair. Answers "what does data value N mean for parameter X".

## number_bases
The decimal / hexadecimal / binary conversion table for values 0–127 that opens the MIDI Data Format section. One row
per value. A convenience table for reading the hex values in the MIDI tables.

## megavoice_map
How the 23 MegaVoices switch playing techniques by velocity and key range: guitars (NylonGuitar, SteelGuitar,
HiStringGuitar, 12StringGuitar with its two elements, CleanGuitar, SolidGuitar1/2, SingleCoilGuitar, OverdriveGuitar,
DistortionGuitar, JazzGuitar), basses (AcousticBass, ElectricBass, VintageRound, VintageFlat, PickBass, VintagePick,
FretlessBass), SmallStrings, LargeStrings, Brass, Trumpet and TenorSax. Each row is one voice + key range (B5 and lower /
C6 and higher / C8 and higher) + velocity range → sound. Sounds include open soft/med/hard, mute, dead, hammer, slide,
harmonics, slap, strum noise, fret noise, SE, spiccato, tremolo, glissando, fall, shake, growl, breath noise and valve
noise. Answers "how do I get the slide / harmonics / strum noise on a MegaVoice guitar" (play at that velocity or in
that key range).

## drum_kits
The Drum/Key Assignment List: which drum, percussion or sound-effect sound each key plays in each of the 29 Drum/SFX
kits (StandardKit1/2, HitKit, RoomKit, RockKit(Legacy), ElectroKit, AnalogKit, DanceKit, JazzKit, BrushKit, SymphonyKit,
HipHopKit, BreakKit, AnalogT8Kit, AnalogT9Kit, HouseKit, StudioKit, PowerKit1/2, AcousticKit, RockKit, RealDrumKit,
SFX Kit1/2, NoisesKit, PopLatinKit 1, TurkishKit, CubanKit, ArabicKit). One row per kit × key that sounds, with:
- MIDI note number (13–91), MIDI note name and keyboard note name (the keyboard note is one octave above the MIDI
  note name, e.g. note 13 = C♯-1 MIDI = C♯0 keyboard);
- `alt_group` (*1 Alternate Group: playing any instrument in a numbered group stops the others in the same group,
  e.g. open/closed hi-hat);
- `key_off` (*2: yes = the sound stops the instant the key is released);
- `drum_tutor` (yes = the kit supports the Drum Tutor function);
- `status`: "same as StandardKit1" (light-grey on the page) or kit-specific.

Keys marked "No Sound" (dark grey) are omitted. Answers "which key is the cowbell / crash / hand clap in kit X",
"what does key C3 play in the JazzKit".

## parameter_chart
The Parameter Chart: for about 460 settings (panel switches, Voice/Style/Song parameters, Mixer, Effect, Mic, Piano Room,
and every Menu function such as Split Point, Chord Fingering, Registration Sequence, Freeze, Pedal, Master/Scale Tune,
MIDI, Wireless LAN, Bluetooth) it shows where each setting is saved or recalled:
- Backup/Restore;
- Setup Files (System Setup, MIDI Setup, User Effect);
- Voice Set (and its Voice Set Filter group);
- MIDI Song file (and its Song Creator Setup group);
- Style file and OTS (One Touch Setting);
- Registration Memory (and its Memory/Freeze group);
- Parameter Lock group.

○ = included/saved, × = not, – = not applicable; values like "○ (On)" are as printed. `group`/`subgroup` are the
chart's section bars. Answers "is setting X stored in Registration Memory / a backup file / the Voice Set",
"which Freeze or Parameter Lock group covers X", "is X kept after power off (Backup)".
Registration Memory: [OM p.80]. Voice Set: [RM p.12].

## direct_access
The Direct Access Chart: which display opens when you press [DIRECT ACCESS] and then another button, wheel or pedal.
That includes STYLE CONTROL and SONG buttons, [TEMPO/TAP], [METRONOME], TRANSPOSE, [MENU], [MIXER/EQ],
[CHANNEL ON/OFF], [MIC SETTING], [USB AUDIO], [VOICE EFFECT], PART ON/OFF, [PLAYLIST], [PIANO ROOM],
REGISTRATION MEMORY, [PITCH BEND], [AUX PEDAL] and the [PEDAL UNIT] pedals. `function_1`–`function_4` are the
display path as printed (display › tab/page › sub-page › item, e.g. Menu › Metronome Setting › – › 2 Tap Tempo). A
blank `control` means the button in `group` is itself the control. Answers "what shortcut opens setting X" and "what
does DIRECT ACCESS + button do". Direct Access: [OM p.22].

## midi_impl_chart
The standard MIDI Implementation Chart (Model DGX-670, Version 1.0, 1-April-2020): what the instrument transmits and
recognizes. Covers basic channels (1–16), mode (3), note numbers (0–127), velocity (note on/off), aftertouch (key/channel),
pitch bend (recognized range 0–24 semitones), each control change number (bank select, data entry, sustain and
sound controllers, portamento, effect depth, RPN/NRPN…), program change, system exclusive, system common and real time
(clock, commands) and aux messages (all sound off, reset all controllers, local on/off, all notes off, active sense).
○ = Yes, × = No. Answers "does the DGX-670 send/receive aftertouch / MIDI clock / program change / CC nn".

## midi_channel_messages
MIDI Data Format, channel messages: Key On/Off, Control Change (each controller number), Mode messages, Program Change,
Channel and Polyphonic Aftertouch, Pitch Bend, Realtime messages. Each row has the status byte, 1st/2nd data bytes with
their meaning, then ○/×/● per part for:
- Voice (Regular/Drum/Natural, Mic);
- MIDI reception (Song, Main/Layer/Left, Keyboard, Style, Extra parts);
- MIDI transmission (Main/Layer/Left, Style, Song, Upper/Lower);
- internal sequencer PLAY/REW/REC.

● = transmitted via panel operations and keyboard/controller performances; ○ = available. Answers "which CC numbers
are received or transmitted, and by which parts".

## midi_nrpn_rpn
MIDI Data Format: NRPN (Non Registered Parameter Numbers) and RPN (Registered Parameter Numbers) with MSB/LSB, Data Entry
MSB/LSB and data range. NRPN covers vibrato rate/depth/delay, low pass filter cutoff/resonance, EQ bass/treble
gain/frequency, EG attack/decay/release, and per-drum-instrument parameters (pitch, level, pan, reverb/chorus/variation
send, filter, EG, EQ). RPN covers pitch bend sensitivity, fine tune, coarse tune, etc. Includes the same ○/×/●
reception/transmission columns as midi_channel_messages. Drum NRPNs (MSB 14H–35H) are accepted only on a channel set to
a Drum Voice.

## midi_parameter_change
MIDI Data Format: the MIDI Parameter Change Tables (XG-style system exclusive parameter address map). One row per
parameter: address high/mid/low (hex), size, data range, parameter name, description and XG default, plus the
reception/transmission columns. Sections: XG SYSTEM (master tune, master volume, transpose…), SYSTEM INFORMATION,
EFFECT1 (reverb/chorus/variation type and parameters), MULTI EQ, EFFECT2 (insertion effects), MULTI PART (per-part
bank/program, receive switches, filter, EG, EQ, controller offsets), A/D PART (microphone/input), DRUM SETUP. Blank
high/mid address bytes on the page mean "same as the row above" and are filled in. For developers and advanced MIDI users.

## midi_sysex_messages
MIDI Data Format: System Exclusive messages with their hex data format and reception/transmission support:
- Universal Real Time: Master Volume, Master Fine/Coarse Tuning, Reverb/Chorus Parameter, Channel Pressure and
  Controller destination, Key-Based Instrument Control.
- Universal Non-Real Time: GM1/GM2 System On, General MIDI System Off, Scale/Octave Tuning.
- Style: Section Control, Tempo Control, Chord Control.
- XG: Parameter Changes, Bulk Dump, Parameter/Dump Request.
- Scale Tuning, Internal/External Clock, Display open/close, MIDI Master Tuning.

SysEx is not received or transmitted when the MIDI settings "System Exclusive Message - Receive/Transmit" are off.

## song_sysex_and_meta
The Song System Exclusive Message List and Song Meta Event List: data embedded in Song (MIDI) files that the instrument
reads. SysEx covers Guide Mode, and Score display settings (Left/Right part indication, Lyrics/Chord/Note Name
indication, size, part channels, quantize, note name), and Style settings (Style Split Point, Style No., Section
Control). Meta events (Yamaha and Yamaha XF) cover Lyrics, Set Tempo, Beat, Key Signature, Score Start Bar, Keyboard
Voice, Chord Name, Phrase Mark/Max and Guide Track Flag. Each row gives the data format, parameter, description and
note. Answers "how does a MIDI file control the score/lyrics/guide display".
