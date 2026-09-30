# Is there a bass-amp (Ampeg SVT + 8×10 style) simulation on the DGX-670?
topic: Bass amplifier / bass cabinet simulation (e.g. Ampeg SVT + 8×10) on the DGX-670
status: nothing-found
researched: 2026-09-30
manual_gap: The Data List's amp simulators are guitar-oriented: British combo/stack, Amp Sim / Stereo Amp Sim with Amp Type Off/Stack/Combo, V Distortion speakers, Small Stereo Dist speakers [DL p.28–30, p.37–38]. The only bass-labelled effect is CompBass, a compressor [DL p.28].
queries: "DGX-670 bass amp simulator effect bass guitar amp DSP"; "Yamaha PSR-SX600 OR Genos DSP effects bass amp simulator Ampeg OR SVT style effect list"
summary: Nothing found online (as of 2026-09-30) about a bass-amp model on the DGX-670 or its PSR-SX600 sibling. Closest documented: amp sims with Stack cabinets plus EQ.

## Manual baseline
- The amp and distortion effects are guitar-oriented [DL p.28, p.30]:
  - "British combo amp simulator" (BCmb…);
  - "British stack amp simulator" (BLegnd…);
  - "Stereo amp simulator" (StAmp…);
  - "A simulation of a guitar amp" (AmpSim1/2).
- Cabinet-like choices:
  - AMP SIMULATOR1 / STEREO AMP SIMULATOR: Amp Type Off/Stack/Combo [DL p.38].
  - V DISTORTION: Speaker Type Flat/Stack/Combo/Radio/Megaphone; Device Transistor/Vintage Tube/Dist1/Dist2/Fuzz
    [DL p.37].
  - SMALL STEREO DIST: Speaker Type Off/Stack/Twin/Oldies/Modern/Mean/Small/Dip1/Dip2/Light, Dist EQ presets
    [DL p.37].
- **CompBass**: "Compressor for the Bass part" (multi-band) [DL p.28].

## Findings
_None._ No source found describes a bass-amp simulation on the DGX-670 or PSR-SX600. A review lists the DGX's
amp-simulator types, but they're the same guitar ones as the Data List. Pages checked:
- https://www.pianodreamers.com/yamaha-dgx670-review/ (review)
- Yamaha PSR-SX600 product and news pages (official, no bass-amp model named)

## Not found
As of 2026-09-30, nothing found for:
- a bass-amp model on the DGX-670 or PSR-SX600;
- anyone approximating an SVT/8×10 on these instruments;
- the frequency response of the "Stack" speaker types.

## Practical takeaway
- **Closest documented:** DSP Type **VDistCrunch** with Device = Vintage Tube and Speaker Type = Stack, or
  **StAmpCrunch** with Amp Type = Stack [DL p.28, p.37–38]. Use the effect's LPF Cutoff and the part EQ to shape it
  [DL p.38; RM p.16].
- **Starting points (general knowledge, not from the manuals or any found source):**
  - lower the LPF Cutoff (about 4–6 kHz) and add low-mid body with the part's EQ Low, to suggest a big bass cabinet;
  - keep drive moderate, since a clean boost into a driven amp is more "crunch" than fuzz.
