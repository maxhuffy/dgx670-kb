"""Batch 3: synth lead through guitar amp/cabinet DSPs (G*), and guitar Voices with their tails removed (B*).

Parameter numbers/ranges: kb/datalist/csv/effect_params.csv [DL p.37-38]; file layout: kb/lab/voice_file_fields.csv.
Run from the repo root:  python generated_voices/batch3_recipe.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from voicefile import VoiceFile  # noqa: E402

LIB = ROOT / "initial_dgx_voices_saved_to_usb"
OUT = ROOT / "generated_voices" / "batch3"
GTR = LIB / "Guitar & Bass"

SL3 = VoiceFile.load(ROOT / "generated_voices" / "batch1" / "SL3 OD Hot.T248.vce")  # SawLead + Step 2 + St.Overdrive
CRUNCH_SA = VoiceFile.load(GTR / "CrunchGuitar.T333.sar")      # DSP: StAmpCrunch (Stereo Amp Simulator 75/30)
HEAVY_SA = VoiceFile.load(GTR / "HeavyRockGuitar.T245.sar")    # DSP: StAmpSim4  (Stereo Amp Simulator 75/24)
CRUNCH_REG = VoiceFile.load(GTR / "CrunchGuitar.T245.vce")     # DSP: VDistH+TDly1 (V Dist Tempo Delay 103/0)
BLUES = VoiceFile.load(GTR / "BluesGuitar.T245.clv")           # DSP: VDistHd+Dly (V Distortion Delay 98/1)

AMP = {"Off": 0, "Stack": 1, "Combo": 2, "Tube": 3}                                   # Amp Type [DL p.38]
DEVICE = {"Transistor": 0, "Vintage Tube": 1, "Dist1": 2, "Dist2": 3, "Fuzz": 4}      # Device [DL p.37]
SPEAKER = {"Flat": 0, "Stack": 1, "Combo": 2, "Twin": 3, "Radio": 4, "Megaphone": 5}  # Speaker Type [DL p.37]


def no_tail(v):
    v.cc(91, 0)   # Reverb Depth 0
    v.cc(93, 0)   # Chorus Depth 0


def synth_with(donor, **dsp):
    """SL3 synth settings, Reverb/Chorus 0, the donor's whole DSP block, then DSP parameter edits (address: value)."""
    v = SL3.copy()
    no_tail(v)
    v.splice_dsp(donor)
    v.yamaha(0x50, 8, 0, 8, 0x7F)  # DSP On
    for addr, val in dsp.items():
        v.xg(0x03, int(addr[1:], 16), val)
    return v


made = []


def save(v, name):
    v.save(OUT / name)
    made.append(name)


# --- G: SawLead synth through amp / cabinet simulation ------------------------------------
# Stereo Amp Simulator: a02 Drive, a03 Amp Type, a04 LPF (Table #3), a05 Output, a0B Dry/Wet, a20 Edge.
save(synth_with(CRUNCH_SA, a02=90, a03=AMP["Tube"], a04=48, a20=80), "G1 AmpTube.T248.vce")     # S3B drive + S3C 5 kHz
save(synth_with(CRUNCH_SA, a02=90, a03=AMP["Stack"], a04=48, a20=110), "G2 AmpStack.T248.vce")  # + S3E edge, Stack amp
save(synth_with(HEAVY_SA), "G3 AmpCombo.T248.vce")   # HeavyRockGuitar's amp as-is: Combo, Drive 100, Edge 106, 4 kHz
# V Dist Tempo Delay with Delay Mix 0 = V Distortion with a speaker cabinet and no echo:
# a02 Overdrive %, a03 Device, a04 Speaker, a05 Presence, a06 Output %, a0B Dry/Wet, a20 Delay Mix.
vt = dict(a02=70, a03=DEVICE["Vintage Tube"], a04=SPEAKER["Stack"], a05=8, a0B=127, a20=0)
save(synth_with(CRUNCH_REG, **vt), "G4 VTubeStack.T248.vce")       # the recipe's "VDistCrunch" idea
g5 = synth_with(CRUNCH_REG, **vt)
g5.nrpn(0x64, 0x30)                                                  # EG Decay -16 (fades like a plucked string)
save(g5, "G5 VTube Pluck.T248.vce")
save(synth_with(CRUNCH_REG, **dict(vt, a03=DEVICE["Dist2"], a04=SPEAKER["Combo"])), "G6 VDist2Combo.T248.vce")

# --- B: guitar Voices you liked, with every tail source removed ---------------------------
b = BLUES.copy(); no_tail(b); b.xg(0x03, 0x20, 0)                 # Delay Mix 0 (V Distortion Delay param 11)
save(b, "B1 Blues Dry.T245.clv")
b = CRUNCH_REG.copy(); no_tail(b); b.xg(0x03, 0x20, 0)            # Delay Mix 0 (V Dist Tempo Delay param 11)
save(b, "B2 Crunch Dry.T245.vce")
b = CRUNCH_SA.copy(); no_tail(b)                                   # S.Art CrunchGuitar: amp sim, no delay
save(b, "B3 CrunchSA Dry.T333.sar")
b.xg(0x03, 0x02, 50)                                               # Drive 14 -> 50 (sample is already crunchy)
save(b, "B4 CrunchSA Hot.T333.sar")
b = HEAVY_SA.copy(); no_tail(b)
save(b, "B5 HeavySA Dry.T245.sar")

print("\n".join(made))
