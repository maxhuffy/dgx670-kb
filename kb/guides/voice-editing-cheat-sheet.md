# DGX-670 Voice Editing Cheat Sheet

Every setting you can change at the Voice level: what it does, where it lives, what it's saved with, and which
Voice types it works with. Compiled from the Owner's Manual (OM), Reference Manual (RM) and Data List (DL). Every
claim carries a citation. Where the manuals are silent, the table says **"not stated"** instead of guessing.

> Compiled 2026-09-29 from `kb/` (the source PDFs). Tables in the Data List are in `kb/datalist/csv/`.

---

## 0. Legend

| Mark | Meaning |
|---|---|
| ✅ | Available / works for this Voice type |
| ⛔ | Not available, locked, or ignored for this Voice type (the manual says so) |
| ⚠️ | Available, but the manual warns the result may be unexpected, or it only works under a condition |
| ❔ | The manuals don't say either way |

**Voice-type columns** used throughout:

| Column | Covers | Count (panel sets) |
|---|---|---|
| **Regular+** | Regular, Natural!, Live!, Cool!, Sweet! Voices (no special editing rules unless noted) | 520 (= 601 non-kit − 9 VRM − 49 S.Art! − 23 Mega) |
| **VRM** | VRM piano Voices | 9 |
| **S.Art!** | Super Articulation Voices | 49 |
| **Kit** | Drums, Live!Drums, SFX, Live!SFX kits | 29 |
| **Mega** | MegaVoices | 23 |

Counts are the Main + Legacy + MegaVoice sections of the Voice List. They match the spec "601 Voices + 29 Drum/SFX
Kits" [OM p.106; DL p.3–12]. The GM & XG (480) and GM2 (265) sections are extra compatibility sounds [DL p.7–12].

---

## 1. The Voice types

| Type | What it is | Special editing rules |
|---|---|---|
| **VRM** (Virtual Resonance Modeling) | Pianos that model the string and soundboard resonance of a real acoustic piano. The resonance reacts to your key and damper-pedal timing [OM p.41]. VRM is on by default [OM p.41]. | Its own global settings page (§5). Reverb/Chorus Depth are **locked** in the Voice Set (§4.4) [RM p.16]. |
| **S.Art!** (Super Articulation) | Voices that change articulation according to how you play. For example, a legato sax passage sounds as if played in one breath, and a firm legato guitar interval slides [OM p.42]. | Automatic pedal articulations, no Mono Type, and warnings about edits (§6). |
| **Natural!** | "High quality sounds on many specialist sampling techniques", especially pianos and keyboards [RM p.4] | A Portamento pedal "does not affect certain Natural! Voices" [RM p.77] |
| **Live!** | Stereo-sampled, including the ambience of the recording room [RM p.4] | none stated |
| **Cool!** | Electric instruments built with voicing and DSP effect programming [RM p.4] | none stated |
| **Sweet!** | Acoustic instruments with the player's sampled vibrato [RM p.4] | none stated |
| **Drums / Live!Drums, SFX / Live!SFX** (kits) | A different drum, percussion or effect sound on each key [RM p.4]. Key maps: `drum_kits.csv` [DL p.15–20]. | No Transpose, no Master Tune, no Mono Type (§7) |
| **MegaVoice** | "Designed for use in Styles and Songs, not for live performance". Velocity ranges select different playing techniques [RM p.4]. Maps: `megavoice_map.csv` [DL p.13–14]. | Warnings about edits (§7) |
| **Regular** | Every Voice not in the types above. It's the label the Voice List uses [DL p.3–12]. | none stated |

The type appears above the Voice name on the Voice Selection display and the Main display [OM p.40, p.42]. The type of
every Voice is in `voices.csv` (column `voice_type`) [DL p.3–12].

---

## 2. Where Voice settings live, and what saves them

The DGX-670 layers settings on top of each other. Knowing the layers explains most of the surprises.

| Layer | What it holds | Where you edit it |
|---|---|---|
| **Voice Set** (per Voice, saved as a file) | Common, Controller, Sound, Effect/EQ and Harmony pages (§4) | Voice Selection display → [5▼] (Voice Set) [RM p.12] |
| **Per-part panel settings** | Mixer levels, filter, effect depths and EQ per part; Mono/Poly, DSP on/off; part Tuning/Octave | [MIXER/EQ], [VOICE EFFECT], Menu → Voice Setting → Tune [RM p.11, p.66–71; OM p.46] |
| **VRM / piano settings** (global for all VRM parts) | VRM on/off, resonance depths, VRM Reverb/Chorus, Key Off Sampling | Menu → Voice Setting → Piano [RM p.6] |
| **Instrument-wide** | Touch Response, Pitch Bend Range, pedal functions, Transpose, Master Tune, Scale Tune, effect **types**, Master EQ, Master Compressor | Menu (Controller, Master Tune/Scale Tune), TRANSPOSE buttons, Mixer [OM p.43–45; RM p.10, p.68–73] |

**What gets saved where** (from the Parameter Chart; ○ = saved, × = not) [DL p.47–54]:

| Setting | Voice Set | Registration Memory | Backup |
|---|---|---|---|
| Voice Set pages: Common, Controller (Modulation), Sound, Effect/EQ incl. **DSP Type**, Harmony | ○ | ○ | ○ |
| Center/Left pedal function (Controller page) | ○ | ○ | ○ |
| Part Octave, Portamento Time (Tune tab) | ○ | ○ | ○ |
| Part **Tuning** (Tune tab) | **×** | ○ | ○ |
| Keyboard Harmony **On/Off**, Left Hold On/Off | **×** | ○ | ○ |
| Effect **Type** of each block (Reverb, Chorus, DSP1–5) | **×** | ○ | ○ |
| Edited Reverb/Chorus/DSP1 **parameters** | × | **×** | ○ |
| Edited DSP2–5 parameters | × | ○ | ○ |
| VRM Reverb / Chorus depth (Piano tab) | × | ○ | ○ |
| **VRM on/off, Damper/String Resonance, Key Off Sampling** | **×** | **×** | ○ |
| Voice Set Filter switches | × | × | ○ |

**Takeaways:**
- A Voice Set stores **how much** reverb and chorus the Voice sends (Depth), **not which** reverb or chorus type is
  used. Those types are instrument-wide Mixer settings [RM p.68–69; DL p.47, p.51].
- A Voice Set **does** store its own DSP Type [DL p.47].
- The VRM resonance settings follow neither the Voice nor the Registration. Only a backup keeps them [DL p.54].

---

## 3. Creating and saving your own Voice (Voice Set)

1. Select the Voice to start from.
2. On the Voice Selection display, press [5▼] (Voice Set). If it isn't shown, press [8▼] (Close) first [RM p.12].
3. Use TAB [◀][▶] to choose a page (Common / Controller / Sound / Effect/EQ / Harmony), Cursor [▲][▼] to choose an
   item, and [1▲▼]–[7▲▼] to edit it [RM p.12].
4. **[8▲] (Compare)** switches between the edited and original sound so you can A/B them [RM p.12].
5. **[8▼] (Save)** saves it as a file to the User drive (internal memory) or a USB flash drive [RM p.12].
   - **Unsaved edits are lost** if you select another Voice or turn the power off [RM p.12].
6. **Voice Set Filter** (Menu → Voice Setting → TAB [▶] Voice Set Filter):
   - For each part, choose which groups a Voice brings with it when selected: 1 Voice (Common + Sound pages), 2 Effect
     (Effect/EQ 1–2), 3 EQ, 4 Keyboard Harmony, 5 Pedal (Controller page) [RM p.17].
   - Example: set **Effect = Off** to keep your current effect while changing Voices [RM p.17].

"The available parameters differ depending on the Voice" [RM p.13]. So a parameter can be missing for a particular
Voice even where this sheet shows ✅.

---

## 4. Master matrix: every Voice Set parameter

> For **S.Art!** and **MegaVoice**, the manuals warn that changing Voice Set parameters, Keyboard Harmony or Transpose
> "may" give "unexpected or undesired sounds" [OM p.42; RM p.4]. That warning applies to every ✅ in those two columns.
> It's marked ⚠️ only where there's an extra, specific rule.

### 4.1 Common page [RM p.13–14]

| Parameter | What it does | Regular+ | VRM | S.Art! | Kit | Mega |
|---|---|---|---|---|---|---|
| **Volume** | Volume of this Voice | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Touch Sense – Depth** | How strongly the level follows your playing strength. 64 = normal, 127 = twice, 0 = no velocity response | ✅ | ✅ | ⚠️ articulation depends on velocity | ✅ | ⚠️ technique switches by velocity |
| **Touch Sense – Offset** | Shifts all received velocities up or down. 64 = normal, >64 louder/harder, <64 softer | ✅ | ✅ | ⚠️ | ✅ | ⚠️ |
| **Part Octave** | Shifts this Voice by octaves. "Main/Layer" value applies when it's used as Main or Layer, "Left" value when used as Left | ✅ | ✅ | ⚠️ range-dependent | ❔ | ⚠️ range-dependent |
| **Mono/Poly** | Mono = one note at a time (last-note priority), good for lead lines. Poly = chords [RM p.13; OM p.46] | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Mono Type** (Normal / Legato / Crossfade) | How notes played legato behave in Mono. **Normal:** the next note starts after the previous one stops. **Legato:** the previous note's sound continues and only the pitch changes. **Crossfade:** the sound fades smoothly into the next note | ✅ | ✅ | ⛔ acts as Normal | ⛔ acts as Normal | ✅ |
| **Portamento Time** | Glide time between notes. 0 = none. Only works in **Mono** [RM p.14; p.11] | ✅ | ✅ | ✅ | ❔ | ✅ |
| **Portamento Type** | **Fixed Rate:** constant glide speed, so wider intervals take longer. **Fixed Time:** constant glide duration regardless of interval [RM p.14] | ✅ | ✅ | ✅ | ❔ | ✅ |

### 4.2 Controller page [RM p.14]

| Parameter | What it does | Regular+ | VRM | S.Art! | Kit | Mega |
|---|---|---|---|---|---|---|
| **Center Pedal / Left Pedal – Function** | Function of the pedal unit's Center/Left pedal while this Voice is selected (any function from RM p.76–78) | ✅ | ✅ | ⚠️ switches to articulation automatically when S.Art! is Main (§6) | ✅ | ✅ |
| **… – Main / Layer / Left, etc.** | Whether the pedal function applies to each part, plus depth-type details | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Modulation – Filter** | How far a **Modulation** pedal moves the filter cutoff | ✅ | ✅ | ✅ | ❔ | ✅ |
| **Modulation – Amplitude** | How far it changes volume | ✅ | ✅ | ✅ | ❔ | ✅ |
| **Modulation – LFO PMOD** | How much vibrato (pitch wobble) it adds | ✅ | ✅ | ✅ | ❔ | ✅ |
| **Modulation – LFO FMOD** | How much wah (filter wobble) it adds | ✅ | ✅ | ✅ | ❔ | ✅ |
| **Modulation – LFO AMOD** | How much tremolo (volume wobble) it adds | ✅ | ✅ | ✅ | ❔ | ✅ |

The Modulation depths only matter when a pedal is set to **Modulation**. That's a continuous function needing an FC3A
or LP-1B/LP-1WH, not a footswitch [RM p.76–77]. Center/Left pedal assignments stick across Voice changes only if
**Switch with Main Voice = Off** [RM p.76].

### 4.3 Sound page [RM p.15]

| Parameter | What it does | Regular+ | VRM | S.Art! | Kit | Mega |
|---|---|---|---|---|---|---|
| **Filter – Brightness** | Filter **cutoff frequency**: which frequencies pass. Higher = brighter, lower = darker/mellower | ✅ | ✅ | ✅ | ❔ | ✅ |
| **Filter – Harmonic Content** | **Resonance**: emphasis right at the cutoff frequency. Higher = sharper, more "synthy" peak | ✅ | ✅ | ✅ | ❔ | ✅ |
| **EG – Attack** | How fast the sound reaches full level after key-on. Lower = faster | ✅ | ✅ | ✅ | ❔ | ✅ |
| **EG – Decay** | How fast it falls from peak to the sustain level. Lower = faster | ✅ | ✅ | ✅ | ❔ | ✅ |
| **EG – Release** | How fast it fades to silence after key-off. Lower = faster | ✅ | ✅ | ✅ | ❔ | ✅ |
| **Vibrato – Depth** | Vibrato intensity (Sweet! Voices already contain the player's sampled vibrato [RM p.4]) | ✅ | ✅ | ✅ | ❔ | ✅ |
| **Vibrato – Speed** | Vibrato rate | ✅ | ✅ | ✅ | ❔ | ✅ |
| **Vibrato – Delay** | Time before the vibrato starts after key-on | ✅ | ✅ | ✅ | ❔ | ✅ |

**Brightness in plain terms:** it's a tone knob working on a low-pass filter. The per-part **Brightness** and
**Harmonic Content** in the Mixer's Filter page are the same two controls for the current part [RM p.67]. Both are
saved in the Voice Set [DL p.50].

**EG:** the Envelope Generator shapes the level over time. The manual's examples are the quick attack and decay of
percussion, or the long release of a sustained piano [RM p.15].

### 4.4 Effect/EQ page [RM p.16]

| Parameter | What it does | Regular+ | VRM | S.Art! | Kit | Mega |
|---|---|---|---|---|---|---|
| **Reverb Depth** | How much of this Voice goes to the (instrument-wide) Reverb block | ✅ | ⛔ **cannot be changed**; use the Piano tab (§5) | ✅ | ✅ | ✅ |
| **Chorus Depth** | How much goes to the (instrument-wide) Chorus block | ✅ | ⛔ **cannot be changed**; use the Piano tab (§5) | ✅ | ✅ | ✅ |
| **DSP On/Off** | Turns this Voice's insertion effect on or off. The same switch as [VOICE EFFECT] → DSP per part [OM p.46] | ✅ | ✅ | ✅ | ✅ | ✅ |
| **DSP Depth** | Wet amount of the insertion effect | ✅ | ✅ | ✅ | ✅ | ✅ |
| **DSP Type – Category / Type** | Chooses the insertion effect (§9 lists what's available) | ✅ | ✅ | ⚠️ some S.Art! effects are built into the samples (see §6) | ✅ | ✅ |
| **DSP Type – Detail** | Edits that effect's parameters. The parameter set differs by effect type [RM p.16]. Parameter lists: `effect_params.csv` [DL p.33–44] | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Vibe Rotor** (On/Off) | Only shown when the DSP Type is **Vibe Rotor** (a vibraphone effect [DL p.27, p.32]). Sets whether the rotor starts on or off when the Voice is selected | ⚠️ only with that DSP type | ⚠️ | ⚠️ | ⚠️ | ⚠️ |
| **EQ – Low / High: Frequency & Gain** | Two-band tone control for this Voice: boost or cut lows and highs at a chosen frequency [RM p.16, p.71] | ✅ | ✅ | ✅ | ✅ | ✅ |

### 4.5 Harmony page [RM p.16; RM p.7–9]

The same settings as Keyboard Harmony, stored with the Voice and recalled automatically when you select it. Before
editing, **make sure the Main part is on** (PART ON/OFF [MAIN]) [RM p.16].

| Parameter | What it does | Regular+ | VRM | S.Art! | Kit | Mega |
|---|---|---|---|---|---|---|
| **Type – Harmony category** | Adds harmony notes to the right hand following the left-hand chord. Types run from "Standard Duet 1" to "Strum"; "1+5" and "Octave" ignore the chord. **Multi Assign** spreads simultaneous notes alternately over Main and Layer (both must be on) [RM p.8] | ✅ | ✅ | ⚠️ | ❔ | ⚠️ |
| **Type – Echo category** (Echo / Tremolo / Trill) | Repeats right-hand notes in time with the tempo. **Trill** needs two held notes and alternates them. Works regardless of [ACMP] or the Left part [RM p.8] | ✅ | ✅ | ⚠️ | ❔ | ⚠️ |
| **Volume** | Level of the generated notes (not Multi Assign) [RM p.9] | ✅ | ✅ | ✅ | ❔ | ✅ |
| **Assign** (Auto / Multi / Main / Layer) | Which part sounds the harmony or echo notes [RM p.9] | ✅ | ✅ | ✅ | ❔ | ✅ |
| **Speed** | Rate of Echo/Tremolo/Trill (only for those types) [RM p.9] | ✅ | ✅ | ✅ | ❔ | ✅ |
| **Chord Note Only** | Harmony only on right-hand notes that belong to the left-hand chord (Harmony types) [RM p.9] | ✅ | ✅ | ✅ | ❔ | ✅ |
| **Minimum Velocity** | Harmony sounds only when you play harder than this, so you can accent phrases [RM p.9] | ✅ | ✅ | ✅ | ❔ | ✅ |

**"Echo" is two different things on this keyboard:**
1. **Keyboard Harmony Echo:** extra note repeats in tempo [RM p.8].
2. **Echo / Delay effect types:** audio echoes produced by the effect processor [DL p.26, p.28] (see §9).

Keyboard Harmony On/Off itself is **not** stored in the Voice Set. It's stored in Registration Memory [DL p.47].
Using the Harmony types with the Style stopped needs Stop ACMP ≠ Disabled [RM p.8].

---

## 5. VRM-only settings (Menu → Voice Setting → TAB [◀] Piano) [RM p.6]

Page 1 VRM applies "commonly to all parts (Main/Layer/Left) for which VRM Voices are selected" [RM p.6].

| Setting | What it does | Applies to | Saved in |
|---|---|---|---|
| **VRM** On/Off | The resonance-modeling effect itself (default On) [OM p.41] | VRM Voices | Backup only [DL p.54] |
| **Damper Resonance** | Depth of the VRM resonance heard **when the damper pedal is pressed** | VRM Voices | Backup only |
| **String Resonance** | Depth of the VRM resonance heard **when playing the keys** | VRM Voices | Backup only |
| **Reverb** | Reverb depth for VRM Voices. This replaces the locked Voice Set Reverb Depth [RM p.16] | VRM Voices | Registration + Backup |
| **Chorus** | Chorus depth for VRM Voices | VRM Voices | Registration + Backup |
| **Key Off Sampling** (page 2) | Volume of the subtle sound when a key is released | Named pianos only: CFX Grand, PopGrand, StudioGrand, OctavePiano1, OctavePiano2, RockPiano, AmbientPiano, CocktailPiano [RM p.6]. Whether it also covers Natural! Voices with the same names is **not stated**. | Backup only |

**Related VRM behaviors:**
- The right damper pedal "activates the VRM" on VRM Voices [OM p.15].
- **Scale Tune:** if a VRM Voice is Main, all VRM resonance follows the Main part's scale. If Main is not a VRM Voice,
  the other VRM Voices' resonance uses Equal temperament [RM p.11].
- **Piano Reset:** hold [PIANO ROOM] for 2+ seconds, then [7▲▼] (Reset). This gives CFX Grand across the whole
  keyboard with piano-appropriate settings [OM p.41].

---

## 6. S.Art!-specific behavior

| Topic | What happens | Source |
|---|---|---|
| Articulation by playing | Legato, velocity and interval choices trigger realistic transitions: sax single-breath legato, guitar slides | [OM p.42] |
| **Info** window | [6▼] (Info) on the Voice Selection display shows how to play that Voice | [OM p.42] |
| Center/Left pedals | With an S.Art! Voice as **Main**, the Center/Left pedals switch automatically to articulation effects (breath or key noise on sax, fret noise or body taps on guitar) | [OM p.42] |
| **Articulation 1 / 2** pedal functions | Trigger the Voice's pedal-assigned articulation effect, set per part | [RM p.76] |
| Keeping your own pedal functions | Set **Switch with Main Voice = Off** (Controller → Setting) | [OM p.42; RM p.76] |
| Rotary/organ-type effects | S.Art! Voices "contain the effect as part of the wave data", so use Articulation 1/2, not Organ Rotary Slow/Fast | [RM p.77] |
| Modulation pedal | "Various effects can be added to the Super Articulation Voice" with a Modulation pedal (FC3A / pedal unit) | [RM p.77] |
| **Mono Type** | ⛔ Not available (behaves as Normal) | [RM p.13] |
| Edits, Harmony, Transpose | ⚠️ "May" produce unexpected sounds, because the sound depends on range, velocity and touch | [OM p.42] |
| Compatibility | Songs and Styles using S.Art! Voices only play correctly on models that have them | [OM p.42] |

---

## 7. Other type-specific rules

| Voice type | Rule | Source |
|---|---|---|
| **Kits** (Drums/SFX) | Transpose does not affect them | [OM p.44] |
| Kits | Master Tune does not affect keyboard parts played with Drum/SFX kits | [RM p.10] |
| Kits | Mono Type unavailable (acts as Normal) | [RM p.13] |
| Kits | **Drum Kit Tutor** ([4▼] on compatible kits) shows each key's instrument. Full key maps with Alternate Group and Key Off: `drum_kits.csv` | [OM p.40; DL p.15–20] |
| **MegaVoice** | Meant for Styles/Songs, not live playing. Velocity ranges pick different techniques. Harmony, Transpose or Voice Set changes may sound wrong | [RM p.4] |
| MegaVoice | Full velocity/key-range technique map: `megavoice_map.csv` | [DL p.13–14] |
| **Natural!** | A **Portamento** pedal function does not affect certain Natural! Voices | [RM p.77] |
| Any | The **Soft** pedal is "effective only for certain appropriate Voices" | [RM p.76] |
| Any | The **Organ Rotary Slow/Fast** pedal only works when an organ effect such as RotarySp1 is applied | [RM p.77] |

---

## 8. Voice-related settings outside the Voice Set

| Setting | What it does | Scope | Saved in | Source |
|---|---|---|---|---|
| [VOICE EFFECT] → **DSP** (per part) | Insertion effect on/off for Main/Layer/Left | Per part | Voice Set, Registration | [OM p.46; DL p.47] |
| [VOICE EFFECT] → **Mono/Poly** (per part) | Mono (last-note priority) or Poly | Per part | Voice Set, Registration | [OM p.46; DL p.47] |
| [VOICE EFFECT] → **Keyboard Harmony** On/Off + Type | Turns Harmony/Echo on; Type opens its settings | Right hand | On/Off: Registration only; settings: Voice Set | [OM p.46; DL p.47–48] |
| [VOICE EFFECT] → **Left Hold** | Holds the Left Voice after release ("H" shows on the Main display) | Left part | Registration only | [OM p.46; DL p.47] |
| Voice Setting → Tune → **Tuning** | Fine pitch per part | Per part | Registration only | [RM p.11; DL p.54] |
| Voice Setting → Tune → **Octave** | Octave shift per part | Per part | Voice Set, Registration | [RM p.11; DL p.54] |
| Voice Setting → Tune → **Portamento Time** | Glide time per part (Mono parts) | Per part | Voice Set, Registration | [RM p.11; DL p.54] |
| Controller → **Touch Response** – Touch | Hard2 / Hard1 / Medium / Soft1 / Soft2 curve. Doesn't change key weight | Instrument | Backup + System Setup (not Registration) | [OM p.43; DL p.53] |
| Controller → Touch Response – **Touch Off Level**, per-part on/off | Fixed velocity for parts with touch off; touch on/off for Main/Layer/Left | Instrument / per part | Registration | [OM p.43; DL p.53] |
| Controller → **Pitch Bend Range** | Maximum [PITCH BEND] range, set per part | Per part | Registration | [OM p.45; DL p.53] |
| **Mixer** (Panel part): Volume, Pan, Brightness, Harmonic Content, Reverb/Chorus/DSP depth, EQ High/Low | The same per-part controls as the Voice Set pages, adjusted live | Per part | Voice Set, Registration | [RM p.66–71; DL p.50–51] |
| **Transpose** (Master/Keyboard/Song) | Semitone shift ±12 (not kits) | Instrument | Registration | [OM p.44; DL p.50] |
| **Master Tune** | 440.0 Hz in 0.2 Hz steps | Instrument | Backup + System Setup (not Registration) | [RM p.10; DL p.53] |
| **Scale Tune** | Equal, Pure Major/Minor, Pythagorean, Mean-Tone, Werckmeister/Kirnberger, Arabic1/2; Base Note; per-note cents; per part | Instrument / per part | Registration if Scale Tune is ticked | [RM p.10–11] |
| **Master EQ** | 5-band final EQ: Normal/Light/Heavy/Mellow/Bright + User 1–30 | Whole output | Backup (Type also System Setup); not Registration | [RM p.71–72; DL p.51] |
| **Master Compressor** | Natural/Rich/Punchy/Electronic/Loud + User 1–30; Compression (threshold), Texture (ratio), Output | Whole output | Backup (On/Off + Type also System Setup); not Registration | [RM p.73; DL p.51] |

---

## 9. Effects: what you can add, and where

### 9.1 The seven effect blocks [RM p.68–69]

| Block | Applies to | How it works | Types to choose from |
|---|---|---|---|
| **Reverb** | All parts | **One** type for the whole instrument; each part sets its send level (Depth); one Return level | Reverb Block list (59) |
| **Chorus** | All parts | **One** type for the whole instrument (it can also be a reverb, delay, etc.); per-part send, one Return | Chorus Block list (107) |
| **DSP1** | Style and Song only | System (shared) or Insertion on one Style/Song channel | Variation/Insertion list |
| **DSP2–DSP5** | Main, Layer, Left, Song ch 1–16, Mic (Mic: **DSP5 only**) | **Insertion**: each block processes one chosen part, and each can have a different type | Variation/Insertion list (297) |

**Key limits:**
- There are only **four** insertion blocks (DSP2–5) for your keyboard parts, song channels and the mic.
- A Song or Style that needs DSP2–5 **reassigns them automatically** [RM p.69].
- Reverb and Chorus **types** are shared by everything. A Voice can only change how much it sends [RM p.68].
- A Voice Set's **DSP Type** is its insertion effect [RM p.16; DL p.47].
- Edited effect parameters can be saved as **User Effects** (Detail → [8▲▼] Save), then picked from each block's
  **User** category [RM p.70].
- Mixer path to choose a block's type: [MIXER/EQ] → Effect page → [ENTER] → Block / Part / Category / Type → [8▲▼]
  (Detail) [RM p.69–70].

### 9.2 Signal flow (short version; details in §9.6)
Keyboard part → **Part EQ** → **insertion DSP2–5** (if one is assigned to that part) → **VRM** (VRM switch) →
dry signal plus sends to **Chorus** and **Reverb** → sum → **Master Compressor** → **Master EQ** → output
[FIG RM-074-f2].

### 9.3 Effect types by block (Data List, DL p.25–32)

**Reverb Block** (59) [DL p.25]:
- **Reverb** (29): RealLrgHall, RealMedHall, RealBrtHall, BasicHall, LightHall, BalladHall, PianoHall, Hall1–5,
  VocalHall1–2, PfRecitHall, PfCncertHall, PfCathedral, RealRoom, RealPwrRoom, AcousticRoom, DrumsRoom, PfChamber,
  Stage1, PianoClub, RealLrgPlate, RealMedPlate, RealRtlPlate, Plate1, PianoPlate
- **Legacy** (29): older halls, rooms, stages and plates
- **NoEffect**

**Chorus Block** (107) [DL p.26–27]:
- **Modulation** (16): Chorus1–2, Symphonic1, Flanger1, TempoFlanger, Phaser1, TempoPhaser1, EP Phaser1,
  DualRotBrt, DualRotWarm, RotarySp1, Tremolo1, EP Tremolo, TempoTremolo, AutoPan1, TempoAtPan1
- **Reverb** (9): Hall1–5, AcousticRoom, DrumsRoom, Stage1, Plate1
- **Delay** (7): TempoDelay1–2, TempoEcho, TempoCross1–4
- **Legacy** (74), including VibeRotor
- **NoEffect**

**Variation/Insertion Block** (297), the list the DSP blocks draw from [DL p.28–32]:
- **Reverb** (9): Hall1–5, AcousticRoom, DrumsRoom, Stage1, Plate1
- **Delay** (13): DelayLCR1–2, DelayLR, Echo, CrossDelay1–2, TempoDelay1–2, TempoEcho, TempoCross1–4
- **Distortion** (25): MltDistSolo, MltDistBasic, MltOD Chorus, MltCrunchWah, MltOldDelay, MltVintgEcho, SmallStDist,
  SmallStOD, SmallStVintg, SmallStHeavy, BCmbClassic, BCmbTopBst, BCmbCustom, BCmbHeavy, BLegndBlues, BLegndHvy1–2,
  BLegndClean, BLegndDtCln, VDistCrunch, VDistBlues, StAmpSolid, StAmpCrunch, StAmpBlues, VDistHd+Dly
- **EQ & Comp** (6): CompMed, CompHeavy, CompMelody, CompBass, EQ Telephone, 3BandEQ
- **Modulation** (24): Chorus1–2, Symphonic1, Flanger1, VFlanger, TempoFlanger, Phaser1, TempoPhaser1, EP Phaser1,
  AutoWah1, AtWah+Dist1, TempoAutoWah, TouchWah1, TcWah+Dist1, PedalWah, PWah+Dist, DualRotBrt, DualRotWarm,
  RotarySp1, Tremolo1, EP Tremolo, TempoTremolo, AutoPan1, TempoAtPan1
- **Misc** (6): LoopFX1–2, Lo-FiDrum1–4
- **Legacy** (212): older algorithms, e.g. REVERB1, CHORUS, V DISTORTION, TOUCH WAH2, STEREO AMP SIMULATOR, KARAOKE,
  GATE REVERB, EARLY REFLECTION, HARMONIC ENHANCER, ENSEMBLE DETUNE, PITCH CHANGE1, ROTARY SPEAKER1, VIBE VIBRATE
- **NoEffect**, **Thru**

The full list (number, description, MSB/LSB, parameter list) is in `kb/datalist/csv/effect_types.csv`, and each
type's editable parameters with ranges are in `effect_params.csv` [DL p.33–44]. Which categories the Voice Set's DSP
Type menu actually offers is **not stated**. The DSP blocks use the Variation/Insertion types (the parameter lists
name their blocks "Variation, DSP1–5") [DL p.33–44].

**Not available:**
- No DSP types beyond the lists above (plus your User Effects) [RM p.70; DL p.25–32].
- Reverb and Chorus can't be different types per Voice [RM p.68].
- At most four insertion effects at once (DSP2–5) [RM p.68–69].
- Effect parameters marked "control from AC1" (76 of them) [DL p.33]: the manuals don't describe any AC1 controller or
  how to operate one on the DGX-670, so treat that as **not stated**.

### 9.4 What the effect words mean (the Data List's own descriptions)

| Term | Meaning | Example types |
|---|---|---|
| **Reverb** | The ambience of a room or hall ("warm ambience of … a concert hall or jazz club") [RM p.69]. Hall = large space, Room = small, Plate = the sound of a classic plate reverb unit, Stage = "suitable for a solo instrument" [DL p.25] | RealLrgHall, RealRoom, RealLrgPlate, Stage1 |
| **Chorus** | Thickens the sound "as if several parts are being played simultaneously" [RM p.69] | Chorus1 "rich, warm chorusing"; Symphonic1 adds more modulation stages [DL p.26] |
| **Delay / Echo** | Delayed repeats of the sound. LCR = left/center/right repeats; Echo = L/R repeats with separate feedback; Cross = feedback crossed between sides; Tempo… = synced to the tempo [DL p.26, p.28] | DelayLCR1, Echo, CrossDelay1, TempoDelay1 |
| **Flanger** | "A sound similar to that of a jet airplane" [DL p.26] | Flanger1, VFlanger (analog-style) |
| **Phaser** | "Cyclically modulates the phase" [DL p.26] | Phaser1, EP Phaser1 (for electric piano) |
| **Tremolo** | Volume (and pitch) pulsing [DL p.26] | Tremolo1, EP Tremolo, TempoTremolo |
| **Auto Pan** | Automatically moves the sound left, right, front and back [DL p.26] | AutoPan1 |
| **Rotary speaker** | Simulates an organ's rotating speaker [DL p.26]. Speed can be switched by pedal (Organ Rotary Slow/Fast) [RM p.77] | RotarySp1, DualRotBrt/Warm |
| **Wah** | A sweeping filter. **Auto** = sweeps on its own; **Touch** = follows how hard you play; **Pedal** = follows the "Pedal Control" parameter [DL p.28–29] | AutoWah1, TouchWah1, PedalWah |
| **Distortion / Amp sim** | Guitar overdrive, fuzz, and amp models (British combo, vintage tube, stereo amp) [DL p.28] | MltDistSolo, BCmbClassic, VDistCrunch, StAmpSolid |
| **Compressor** | Evens out loud and soft playing [RM p.73]. Voice-level versions: CompMed/Heavy/Melody/Bass [DL p.28] | CompMed |
| **EQ** | Boosts or cuts frequency bands [RM p.71]. EQ Telephone cuts lows and highs like a phone line [DL p.28] | 3BandEQ, EQ Telephone |
| **Lo-Fi** | "Degrades the audio quality of the input signal" [DL p.29] | LoopFX1, Lo-FiDrum1 |
| **Vibe Rotor** | "Vibraphone effect" [DL p.27]. It has its own Vibe Rotor on/off in the Voice Set and a pedal function [RM p.16, p.77] | VibeRotor (Legacy) |

### 9.5 Filter vs EQ vs Brightness
- **Brightness / Harmonic Content** (Voice Set Sound page, and the Mixer Filter page): the Voice's **filter**, i.e.
  cutoff and resonance. It changes the timbre at the source [RM p.15, p.67].
- **Part EQ Low/High** (Voice Set Effect/EQ page, and the Mixer EQ page): two bands boosted or cut after the sound is
  made [RM p.16, p.71].
- **Master EQ**: a 5-band EQ on the whole instrument's output [RM p.71–72].

### 9.6 Signal flow (Block Diagram, RM p.74)

As drawn in the Mixer block diagram (full description: `kb/figures/RM-074.md`) [FIG RM-074-f2]:

1. **Part EQ:** MAIN, LAYER, LEFT, every Song channel and every Style part first pass through their own PART EQ.
   The mic goes through MIC EFFECT (Vocal/Talk) instead.
2. **Insertion effects:** DSP2, DSP3, DSP4 and DSP5 in sequence. DSP2–4 can sit on the keyboard parts or Song
   channels. DSP5 can also take the MIC ("MAIN, LAYER, LEFT, SONG CH1~16, MIC").
3. **DSP1 as insertion** (Connection = Insertion): only on Song/Style rows.
4. **VRM:** each keyboard, Song and Style row has a "VRM Sw" feeding the VRM block. VRM's output becomes its own
   send row into Chorus and Reverb. That fits VRM Voices having their Reverb/Chorus set on the Piano tab
   rather than the Voice Set (§5), though the figure itself doesn't state the link.
5. **Sends:** CHORUS DEPTH and REVERB DEPTH knobs on every row (including the VRM row and the mic) feed the
   **SYSTEM EFFECT** blocks (Chorus, Reverb). DSP1 DEPTH (Connection = System) is fed only from the VRM, Song and
   Style rows. It is **not** fed from Main/Layer/Left.
6. **Returns:** CHORUS / REVERB / VARIATION (DSP1) RETURN LEVEL are summed with the dry signal of all rows.
7. **Master:** MASTER COMPRESSOR → MASTER EQ → OUTPUT. **AUDIO** (USB audio) and **AUX IN** join *after* the Master
   EQ. That's why Master EQ/Compressor don't affect them [RM p.71, p.73].

The diagram draws no separate "Filter" block. The Voice filter (Brightness/Harmonic Content) is part of the Voice
itself [RM p.15, p.67].

---

## 10. Quick recipes (all steps cited above)
- **Brighter or darker:** Voice Set → Sound → Brightness up or down; Harmonic Content for a resonant edge [RM p.15].
- **Pad that swells in:** Sound → EG Attack up, Release up [RM p.15].
- **Lead line with glide:** Common → Mono, Portamento Time > 0, Portamento Type to taste. Mono Type Legato for
  seamless changes (not on S.Art!/kits) [RM p.13–14].
- **More room on a piano:**
  - VRM piano: Menu → Voice Setting → Piano → Reverb [RM p.6].
  - Other Voices: Voice Set → Effect/EQ → Reverb Depth [RM p.16].
  - Changing the reverb **type** is a Mixer setting, and it affects everything [RM p.68–69].
- **Guitar amp tone on a Voice:** Effect/EQ → DSP Type → Distortion category → e.g. BCmbClassic; adjust with Detail
  [RM p.16; DL p.28].
- **Keep an effect while browsing Voices:** Voice Set Filter → Effect Off for that part [RM p.17].
- **Save it:** [8▼] (Save) to the User drive or USB. Put it in Registration Memory if you want the per-part extras too
  [RM p.12; OM p.81].

---
Sources: OM p.15, p.40–47, p.81, p.106 · RM p.4, p.6–17, p.66–77 · DL p.3–53
