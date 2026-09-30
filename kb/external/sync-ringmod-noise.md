# Does the DGX-670 have oscillator hard sync, ring modulation ("Bell Tone") or a noise source?
topic: Oscillator hard sync, ring modulation and noise on the DGX-670 (MG-1-style features)
status: partial
researched: 2026-09-30
manual_gap: The manuals have no oscillator section, so no sync or noise generator [RM p.13–16]. The Data List **does** list RingMod, DynRingMod and Lo-Fi insertion effects [DL p.32, p.43–44], which the earlier Motion City Soundtrack answer overlooked.
queries: "DGX-670 OR PSR-SX ring modulator effect RingMod synth sound"; "Yamaha arranger keyboard oscillator sync synth lead workaround PSR DGX hard sync sound"; plus the topic-1 searches for noise/synth Voices
summary: Ring mod exists as an effect (RingMod, DynRingMod: tier 1, Data List). Noise only as sampled noise Voices (GM/XG, reachable via community files) or the Lo-Fi effect. Hard sync: nothing found online.

## Manual baseline
- **Ring modulation (tier 1):**
  - **RingMod**: "An effect that modifies the pitch by applying amplitude modulation to the frequency of the input".
    Parameters: Osc Frequency Coarse/Fine, LFO Wave (Triangle/Sine), LFO Depth, LFO Frequency, HPF and LPF Cutoff,
    Dry/Wet, EQ Low/High [DL p.32, p.44].
  - **DynRingMod**: "Dynamically controlled Ring Modulator". Parameters: Sensitivity, Attack/Release Time, Release
    Curve, Direction Up/Down, Dyna Threshold Level, Dyna Level Offset, HPF/LPF, Dry/Wet, EQ [DL p.32, p.43].
  - Both are Legacy Variation/Insertion types, so they can be a Voice's DSP Type (DSP1–5) [DL p.32, p.43–44; RM p.16].
- **Noise-ish:** the **Lo-Fi** effect "Degrades the audio quality of the input signal". Parameters: Sampling
  Frequency 44.1 kHz–345 Hz, Word Length, Output Gain, LPF Cutoff/Resonance, Filter Type
  (Thru/PowerBass/Radio/Tel/Clean/Low), Bit Assign, Emphasis [DL p.32, p.43]. It adds digital grit, not a noise
  source.
- Sampled noise Voices exist only in the GM & XG / GM2 sections: BreathNoise, CuttingNoise1–2, BurstNoise [DL p.10,
  p.12]. These sections are for Song playback [OM p.106].
- **Hard sync:** no parameter or effect in the manuals or Data List.

## Findings
**[E1]** The GM/XG/GM2 Voices, including the noise Voices, can be made playable from the keyboard by loading community-extracted User Voice files from USB. You could then **Layer** a noise Voice quietly under a lead, similar to the MG-1 noise mix. See [EXT synth-waveform-voice-choice#E2]. Source: keyboardforums.com, "DGX-670 GM & XG Voices", user Δικαιοπολις, 2023-05-07. https://www.keyboardforums.com/threads/dgx-670-gm-xg-voices.34185/ Type: forum. Applies to: DGX-670. Trust: medium (not tested here).

**[E2]** Hard sync resets one oscillator's phase from another oscillator. It is a sound-generation feature, so no insertion effect can recreate it; only a sampled Voice that already contains sync can. Source: Perfect Circuit, "Synthesizer Basics: What is Oscillator Sync?". https://www.perfectcircuit.com/signal/what-is-oscillator-sync Type: third-party doc. Applies to: general. Trust: high (standard synthesis explanation).

## Not found
As of 2026-09-30, no DGX-670 (or PSR) forum/Reddit post was found that:
- uses RingMod/DynRingMod on a synth lead,
- recreates hard sync, or
- names a DGX Voice sampled with sync.

No Voice name contains "Sync" [DL p.3–12].

## Practical takeaway
- **Bell Tone-like clang:** set a Voice's DSP Type to **RingMod**, keep Dry/Wet mostly dry and tune Osc Frequency by
  ear [DL p.44; RM p.16]. Caveat: one DSP per part, so RingMod and your drive can't both be on one part [RM p.68–69].
  Use Layer for the second effect.
- **Noise:** load the GM noise Voices and Layer one quietly (external [E1]), or use Lo-Fi for grit [DL p.43].
- **Sync:** not available (external [E2]); choose a bright, buzzy sampled lead instead.
