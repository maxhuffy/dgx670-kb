# What makes the BWV 565 Toccata opening sound as it does on a pipe organ, and how keyboards emulate it
topic: Pipe-organ sound of Bach's Toccata in D minor (BWV 565) opening, and emulating organo pleno + church acoustics on a digital keyboard / the DGX-670
status: partial
researched: 2026-10-04
manual_gap: The manuals describe no Voice's sound and give no registration advice; the Data List names the organ Voices [DL p.3, p.8] and the effect types/parameters [DL p.25–33], and the RM describes Layer, Part Octave and historical Scale Tunes [RM p.10–13].
queries: "Bach Toccata in D minor BWV 565 opening registration organo pleno mixtures reeds 16'"; "Toccata and Fugue D minor opening mordent octaves diminished seventh chord pedal D acoustics cathedral reverb"; "how to make pipe organ sound on digital keyboard synth Toccata D minor octave layer reverb no velocity"; "Yamaha PSR DGX Toccata and Fugue best organ voice settings Notre Dame church organ reverb"; "pipe organ tone characteristics flue pipe chiff attack steady sustain"; "organ plenum 16' pedal reed 32' Toccata D minor opening registration"; "digital organ realism reverb decay cathedral, sample release, wind, why sampled pipe organ sounds fake"
summary: The opening is an octave-doubled flourish (the doubling itself imitates a 16' stop) falling to a diminished-7th chord over a low pedal D, played on organo pleno (principal chorus 8-4-2 + mixtures, reed/16' in the pedal) in a 4–7 s room. Keyboards get closest with a velocity-free church-organ Voice, a sub-octave or reed layer, extra brightness and a long hall reverb. Generated test Voices: generated_voices/bwv565.

## Manual baseline
- Pipe-organ-type preset Voices: FullOrgan, HymnOrgan, ChapelOrgan1/2 (all PC# 20, the GM "Church Organ" program), plus
  Tibia/VoxHumana/Trumpet theatre-organ Voices [DL p.3]; the GM & XG list adds ChurchOrgan1–3, NotreDame and OrganFlute
  [DL p.8], which are for Song playback per the spec [OM p.106] (see [EXT synth-waveform-voice-choice#E1, #E2]).
- Two Voices can be layered (Main + Layer) [OM p.38]; Part Octave shifts a Voice Set by octaves for Main/Layer or Left
  [RM p.13]; Voice Setting → Tune → Octave sets each part's octave [RM p.11].
- Touch Response can be turned off per part, with a fixed Touch Off Level [OM p.43].
- Reverb block types include RealLrgHall and PfCathedral ("acoustics of a cathedral") [DL p.25]; the DSP slot can hold
  Hall1–5 (REVERB1) with Reverb Time 0.3–30 s, Initial Delay, LPF, High Damp and Dry/Wet [DL p.28, p.33, p.45]. The
  Reverb block type is chosen in the Mixer's Effect page [RM p.68–70].
- Scale Tune offers Mean-Tone and "Werckmeister, Kirnberger", the latter described as used extensively in Bach's
  time [RM p.10–11].

## Findings
**[E1]** The opening is a single-voice flourish high on the keyboard, doubled at the octave and ornamented with a lower mordent, with fermata pauses (Adagio); it spirals down to a diminished-seventh chord over a tonic pedal (D) that resolves to D major. Source: Wikipedia, "Toccata and Fugue in D minor, BWV 565". https://en.wikipedia.org/wiki/Toccata_and_Fugue_in_D_minor,_BWV_565 Type: third-party doc. Applies to: general. Trust: high (well-sourced article, matches the score).

**[E2]** Bach probably used the octave doubling to create the effect of a 16-foot register, because the Arnstadt organ's manuals lacked a 16' stop. Source: Netherlands Bach Society, BWV 565 page. https://www.bachvereniging.nl/en/bwv/bwv-565/ Type: third-party doc (specialist ensemble). Applies to: general. Trust: high.

**[E3]** Organo pleno, the usual registration for Bach's free works, is the full principal chorus: principals at 8', 4', 2', 2⅔' plus mixtures (high harmonics on every note), with a 16' reed such as a Posaune in the pedal. Avoid 16' in the manuals when the texture is fast, for clarity. Source: organduo.lt, "Building organo pleno". https://www.organduo.lt/buildingorganopleno.html Type: third-party doc (organists' teaching blog). Applies to: general. Trust: medium-high.

**[E4]** A full 16'/32' registration in fast Toccata passagework makes a low rumble that masks the brilliance of the higher pipes. The opening flourishes need brilliance and "chiff" more than heavy reeds. Source: Modartt (Pianoteq) forum, "Toccata and Fugue new registration, more stops, also in pedal". https://forum.modartt.com/viewtopic.php?id=8427 Type: forum. Applies to: general (Pianoteq organ). Trust: medium (seen through search excerpts, not read in full).

**[E5]** A flue pipe's attack transient ("chiff") comes from the edge tone, and its steady sound is very stable (no decay while the key is held). Real pipe tone is only quasi-periodic, and that variation is part of why it sounds alive. Source: Colin Pykett, "How the Flue Pipe Speaks", and US patent 4905562 (search excerpts). https://colinpykett.org.uk/how_the_flue_pipe_speaks.htm Type: third-party doc. Applies to: general. Trust: medium-high.

**[E6]** Olivier Latry's Bach recording at Notre-Dame de Paris deals with about seven seconds of reverberation. Source: Classical Music Sentinel review of "Bach to the Future". https://www.classicalmusicsentinel.com/KEEP/bach-latry.html Type: third-party doc (review). Applies to: general. Trust: medium.

**[E7]** On a Yamaha synth, a big church-organ sound comes from layering and octave doubling (above and below) plus church/cathedral reverb; "the most important stop on the organ is the room". Source: Yamaha Synth forum, "unbelievable church pipe organ sounds on the MX". https://yamahasynth.com/community/mx-series-synthesizers/unbelievable-church-pipe-organ-sounds-on-the-mx Type: forum. Applies to: Yamaha MX (Motif-family AWM2, not the DGX engine). Trust: medium.

**[E8]** Sampled organs sound fake mostly because of short static loops, identical notes every time, little or no wind modelling, and missing release transients (real high-end sets add release samples and random pipe fluctuation). Source: Hauptwerk forum, "Open letter to sample set producers". https://forum.hauptwerk.com/viewtopic.php?p=123171 Type: forum. Applies to: general. Trust: medium.

**[E9]** Digital organs also suffer from intermodulation when many voices go through few loudspeaker channels, and from audible joins between the held loop and the release transient. Source: Colin Pykett, "Digital Organs Today". https://colinpykett.org.uk/digitalorganstoday.htm Type: third-party doc. Applies to: general. Trust: medium-high.

**[E10]** Yamaha sells a "Church Organ" Voice & Style expansion pack (classic organ Voices with natural hall response) for PSR/Genos arrangers. Source: Yamaha US shop. https://shop.usa.yamaha.com/en/p/downloadables/sound-expansion-library/voice-style-expansion-packs/church-organ-20 Type: official. Applies to: PSR-SX/Genos, not the DGX-670 (no expansion packs, [EXT synth-waveform-voice-choice]). Trust: high.

## Not found
- No DGX-670-specific (or PSR-SX600-specific) settings for BWV 565 or for cathedral organ sounds, as of 2026-10-04.
- Which soundfont MuseScore used for the user's reference playback (not checked; the page was not fetched).
- The Hauptwerk BWV 565 registration thread (Bovenkerk) returned HTTP 403.

## Practical takeaway
- Manual-backed: start from FullOrgan / ChapelOrgan1 / HymnOrgan [DL p.3]. Add a Layer Voice an octave down (16') or a
  reed [OM p.38, RM p.13], pick the longest hall/cathedral Reverb type [DL p.25, RM p.69], optionally Scale Tune
  "Werckmeister, Kirnberger" [RM p.10–11].
- External: the octave doubling already *is* the 16' imitation [E2], so a sub-octave layer is optional colour, not a
  requirement. Brightness (mixtures) and the room (4–7 s) matter most [E3, E6, E7]. Keep the low end clean [E4].
- Lab: six test Voices built from these ideas: `generated_voices/bwv565/` (log in [LAB voice-file-format]).
