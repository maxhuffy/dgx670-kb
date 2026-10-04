"""Generate DGX-670 test Voice files from a preset template (batch 1: SawLead recipe)."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import vce

LIB = r"C:\Users\maxhu\Desktop\Yamaha DGX 670 PDFs and Text\initial_dgx_voices_saved_to_usb"
OUT = r"C:\Users\maxhu\Desktop\Yamaha DGX 670 PDFs and Text\generated_voices\batch1"


def load(rel):
    """Return (header_bytes, [(delta, raw_event_bytes_without_delta)])."""
    p = os.path.join(LIB, rel)
    b = open(p, "rb").read()
    hdr = b[:14]
    evs = []
    for off, dt, kind, d in vce.events(p):
        if kind == "meta":
            raw = bytes([0xFF, d[0], len(d) - 1]) + d[1:]
        elif kind == "sysex":
            raw = bytes([0xF0, len(d)]) + d
        else:
            raw = d
        evs.append([dt, raw])
    return hdr, evs


def save(name, hdr, evs):
    trk = b""
    for dt, raw in evs:
        assert dt < 128
        trk += bytes([dt]) + raw
    data = hdr + b"MTrk" + len(trk).to_bytes(4, "big") + trk
    os.makedirs(OUT, exist_ok=True)
    open(os.path.join(OUT, name), "wb").write(data)
    return os.path.join(OUT, name)


def find(evs, pred):
    idx = [i for i, (dt, r) in enumerate(evs) if pred(r)]
    assert len(idx) == 1, (idx, pred)
    return idx[0]


def xg(evs, hi, lo, *vals):
    """Set XG parameter (43 10 4C hi 00 lo ...)."""
    key = bytes([0x43, 0x10, 0x4C, hi, 0x00, lo])
    i = find(evs, lambda r: r[0] == 0xF0 and r[2:8] == key)
    r = evs[i][1]
    assert len(r) == 9 + len(vals), r.hex(" ")
    evs[i][1] = r[:8] + bytes(vals) + b"\xF7"


def yam(evs, sub, a, b_, c, val):
    """Set Yamaha 43 73 01 <sub> a b c <val>."""
    key = bytes([0x43, 0x73, 0x01, sub, a, b_, c])
    i = find(evs, lambda r: r[0] == 0xF0 and r[2:9] == key)
    r = evs[i][1]
    evs[i][1] = r[:9] + bytes([val]) + b"\xF7"


def cc(evs, num, val):
    i = find(evs, lambda r: r[0] == 0xB0 and r[1] == num)
    evs[i][1] = bytes([0xB0, num, val])


def nrpn(evs, lsb, val):
    """Set the Data Entry MSB following NRPN MSB 01 / LSB lsb."""
    for i in range(len(evs) - 2):
        if evs[i][1] == bytes([0xB0, 0x63, 0x01]) and evs[i + 1][1] == bytes([0xB0, 0x62, lsb]):
            assert evs[i + 2][1][:2] == bytes([0xB0, 0x06])
            evs[i + 2][1] = bytes([0xB0, 0x06, val])
            return
    raise KeyError(lsb)


def voice(evs, msb, lsb, pc):
    cc(evs, 0, msb); cc(evs, 32, lsb)
    i = find(evs, lambda r: r[0] == 0xC0)
    evs[i][1] = bytes([0xC0, pc])


def dsp_block(evs):
    s = find(evs, lambda r: r[0] == 0xF0 and r[2:8] == bytes([0x43, 0x10, 0x4C, 0x03, 0x00, 0x00]))
    e = find(evs, lambda r: r[0] == 0xF0 and r[2:9] == bytes([0x43, 0x73, 0x01, 0x51, 0x08, 0x00, 0x12]))
    return s, e


def splice_dsp(evs, donor_evs):
    s, e = dsp_block(evs)
    ds, de = dsp_block(donor_evs)
    evs[s:e + 1] = [list(x) for x in donor_evs[ds:de + 1]]


def step2(evs):
    """Recipe Step 2 (Common/Sound/Effect pages)."""
    xg(evs, 0x08, 0x05, 0x00)   # Mono/Poly -> Mono (confirmed by CFX M/NM test)
    cc(evs, 5, 0)                # Portamento Time 0
    xg(evs, 0x08, 0x0C, 0x10)   # Touch Sense (Velocity Sense) Depth low (16)
    cc(evs, 73, 0x00)            # EG Attack minimum
    nrpn(evs, 0x64, 0x70)        # EG Decay: slow (+48)
    nrpn(evs, 0x66, 0x30)        # EG Release: shorter (-16)
    nrpn(evs, 0x09, 0x00)        # Vibrato Depth minimum
    cc(evs, 74, 0x50)            # Brightness up (+16)
    cc(evs, 71, 0x50)            # Harmonic Content moderately up (+16)
    cc(evs, 91, 0x10)            # Reverb depth low
    cc(evs, 93, 0x00)            # Chorus depth 0


if __name__ == "__main__":
    SAW = r"Legacy\Synth\SawLead.T248.vce"
    hdr, base = load(SAW)
    _, smooth = load(r"Legacy\E.Guitar\SmoothLead.T333.vce")   # StOverdrive donor
    _, wazzo = load(r"Guitar & Bass\WazzoSaw.T248.vce")        # DynFilter donor
    made = []

    # 0: control - byte-identical re-serialisation of SawLead
    made.append(save("SL0 Copy.T248.vce", hdr, [list(x) for x in base]))

    # 1: Step 2 settings, DSP switched OFF (tests hypothesis: Yamaha 50 08 00 08 = DSP on/off)
    e = [list(x) for x in base]; step2(e); yam(e, 0x50, 0x08, 0x00, 0x08, 0x00)
    made.append(save("SL1 Dry.T248.vce", hdr, e))

    # 2: Step 2 + StOverdrive (donor SmoothLead), recipe starting values
    e = [list(x) for x in base]; step2(e); splice_dsp(e, smooth); yam(e, 0x50, 0x08, 0x00, 0x08, 0x7F)
    xg(e, 0x03, 0x02, 40)    # P1 Drive 40
    xg(e, 0x03, 0x04, 64)    # P3 EQ Low Gain 0 dB
    xg(e, 0x03, 0x05, 51)    # P4 LPF Cutoff 7.0 kHz (Table #3)
    xg(e, 0x03, 0x08, 34)    # P7 EQ Mid Freq 1.0 kHz (Table #3)
    xg(e, 0x03, 0x09, 69)    # P8 EQ Mid Gain +5 dB
    xg(e, 0x03, 0x20, 40)    # P11 Edge: mild (40 of 127)
    made.append(save("SL2 OD.T248.vce", hdr, e))

    # 3: same as 2 but hotter drive / sharper edge
    e2 = [list(x) for x in e]
    xg(e2, 0x03, 0x02, 70); xg(e2, 0x03, 0x20, 80); xg(e2, 0x03, 0x09, 72)
    made.append(save("SL3 OD Hot.T248.vce", hdr, e2))

    # 4: Step 2 + DynFilter (donor WazzoSaw): LPF 24 dB, Up, fast attack, ~370 ms release, full wet
    e = [list(x) for x in base]; step2(e); splice_dsp(e, wazzo); yam(e, 0x50, 0x08, 0x00, 0x08, 0x7F)
    xg(e, 0x03, 0x02, 2)     # P1 Filter Type LPF(24dB)
    xg(e, 0x03, 0x03, 90)    # P2 Sensitivity (donor 80) up
    xg(e, 0x03, 0x05, 56)    # P4 Resonance +40
    xg(e, 0x03, 0x06, 5)     # P5 Attack 5.4 ms (Table #13)
    xg(e, 0x03, 0x07, 64)    # P6 Release 369 ms (Table #14)
    xg(e, 0x03, 0x09, 0)     # P8 Direction Up (0)
    xg(e, 0x03, 0x0B, 127)   # P10 Dry/Wet fully wet
    made.append(save("SL4 DynFlt.T248.vce", hdr, e))

    # 5: retarget test - variant 2 settings on SquareLead (MSB 0 / LSB 112 / PC#81 -> program 80) [DL p.6]
    e = [list(x) for x in base]; step2(e); splice_dsp(e, smooth); yam(e, 0x50, 0x08, 0x00, 0x08, 0x7F)
    xg(e, 0x03, 0x02, 40); xg(e, 0x03, 0x04, 64); xg(e, 0x03, 0x05, 51); xg(e, 0x03, 0x08, 34)
    xg(e, 0x03, 0x09, 69); xg(e, 0x03, 0x20, 40)
    voice(e, 0, 112, 80)
    made.append(save("SQ5 OD.T248.vce", hdr, e))

    for m in made:
        print(m, os.path.getsize(m))
