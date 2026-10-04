"""Decode DGX-670 voice files (.vce etc. = SMF) and label events from the kb Data List CSVs."""
import csv, sys, os

KB = r"C:\Users\maxhu\Desktop\Yamaha DGX 670 PDFs and Text\kb\datalist\csv"


def load_xg():
    m = {}
    for r in csv.DictReader(open(os.path.join(KB, "midi_parameter_change.csv"), encoding="utf-8")):
        hi, mid, lo = r["Address (H) high"].strip(), r["Address (H) mid"].strip(), r["Address (H) low"].strip()
        name = r["Parameter"].replace("\n", " ").strip()
        # first low address only (multi-byte rows like "00 01 02 03")
        lo0 = lo.split()[0] if lo else ""
        m.setdefault((hi, lo0), name)
    return m


XG = load_xg()


def xg_name(hi, mid, lo):
    h = "%02X" % hi
    l = "%02X" % lo
    if h == "08":
        return XG.get(("08", l), "?")
    if h == "0A":
        return XG.get(("0A", l), "?")
    if h == "03":
        return XG.get(("03", l), "?")
    if h == "02":
        return XG.get(("02", l), "?")
    return "?"


def vlq(b, i):
    v = 0
    while True:
        c = b[i]; i += 1
        v = (v << 7) | (c & 0x7F)
        if not c & 0x80:
            return v, i


def events(path):
    b = open(path, "rb").read()
    assert b[:4] == b"MThd"
    hl = int.from_bytes(b[4:8], "big")
    i = 8 + hl
    out = []
    while i < len(b):
        tag, ln = b[i:i + 4], int.from_bytes(b[i + 4:i + 8], "big")
        j, end = i + 8, i + 8 + ln
        run = None
        while j < end:
            start = j
            dt, j = vlq(b, j)
            st = b[j]
            if st == 0xFF:
                t = b[j + 1]; l, k = vlq(b, j + 2); data = b[k:k + l]; j = k + l
                out.append((start, dt, "meta", bytes([t]) + data))
            elif st in (0xF0, 0xF7):
                l, k = vlq(b, j + 1); data = b[k:k + l]; j = k + l
                out.append((start, dt, "sysex", data))
            else:
                if st & 0x80:
                    run = st; j += 1
                n = 1 if (run & 0xF0) in (0xC0, 0xD0) else 2
                out.append((start, dt, "chan", bytes([run]) + b[j:j + n])); j += n
        i = end
    return out


def label(ev):
    off, dt, kind, d = ev
    hx = d.hex(" ").upper()
    if kind == "meta":
        return f"META {hx}"
    if kind == "chan":
        s = d[0] & 0xF0
        if s == 0xB0:
            names = {0: "Bank MSB", 32: "Bank LSB", 99: "NRPN MSB", 98: "NRPN LSB", 6: "Data Entry MSB", 38: "Data Entry LSB",
                     73: "CC73 Attack", 71: "CC71 Harmonic Content", 74: "CC74 Brightness", 5: "CC5 Portamento Time",
                     91: "CC91 Reverb send", 93: "CC93 Chorus send", 7: "CC7 Volume", 72: "CC72 Release", 75: "CC75 Decay"}
            return f"CC  {hx:12} {names.get(d[1], 'CC%d' % d[1])} = {d[2]}"
        if s == 0xC0:
            return f"PC  {hx:12} Program = {d[1]} (PC# {d[1] + 1})"
        return f"CH  {hx}"
    # sysex (d excludes F0, includes F7)
    if d[:3] == bytes([0x43, 0x10, 0x4C]):
        hi, mid, lo = d[3], d[4], d[5]
        val = d[6:-1]
        return f"XG  {hi:02X} {mid:02X} {lo:02X} = {val.hex(' ').upper():6} {xg_name(hi, mid, lo)}"
    if d[:3] == bytes([0x43, 0x73, 0x01]):
        return f"YAM {hx}   (Clavinova-ID; not in DL tables)"
    return f"SX  {hx}"


if __name__ == "__main__":
    for p in sys.argv[1:]:
        print("=" * 8, os.path.basename(p))
        for ev in events(p):
            print(f"{ev[0]:4d} {label(ev)}")
