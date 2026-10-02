#!/usr/bin/env python3
"""Decode, diff and edit DGX-670 Voice files (.vce, .sar, .liv, ... = Standard MIDI Files). Stdlib only.

Format, field map and panel-value rules: kb/lab/voice-file-format.md and kb/lab/voice_file_fields.csv.

Usage:
  python scripts/voicefile.py decode <file> [<file> ...]   # every event, labelled from the Data List CSVs
  python scripts/voicefile.py diff   <file_a> <file_b>       # only the events that differ

Editing (from Python):
  from voicefile import VoiceFile
  v = VoiceFile.load("SawLead.T248.vce")
  v.xg(0x08, 0x05, 0x00)          # Mono/Poly -> Mono
  v.cc(74, 64 + 16)               # Brightness +16 (Sound page: panel = file - 64)
  v.splice_dsp(VoiceFile.load("SmoothLead.T333.vce"))   # take a donor's whole DSP block
  v.save("SL Mono.T248.vce")      # the display name is the file name; keep the .Tnnn.ext suffix
"""
import csv
import difflib
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
CSV = Path(__file__).resolve().parents[1] / "kb" / "datalist" / "csv"

XG_PREFIX = bytes([0x43, 0x10, 0x4C])
YAMAHA_PREFIX = bytes([0x43, 0x73, 0x01])
CC_NAMES = {0: "Bank MSB", 32: "Bank LSB", 99: "NRPN MSB", 98: "NRPN LSB", 6: "Data Entry MSB", 38: "Data Entry LSB",
            5: "Portamento Time", 71: "Harmonic Content", 72: "Release", 73: "Attack", 74: "Brightness",
            91: "Reverb Depth", 93: "Chorus Depth"}
NRPN_NAMES = {0x08: "Vibrato Speed", 0x09: "Vibrato Depth", 0x0A: "Vibrato Delay", 0x64: "EG Decay", 0x66: "EG Release"}
YAMAHA_NAMES = {(0x50, 8, 0, 4): "Volume", (0x50, 8, 0, 5): "Part Octave Main/Layer", (0x50, 8, 3, 6): "Part Octave Left",
                (0x50, 8, 0, 8): "DSP On/Off", (0x50, 4, 0, 5): "Harmony Volume", (0x51, 4, 0, 0): "Harmony Type",
                (0x51, 0, 1, 0): "Pedal function", (0x51, 8, 0, 0x11): "DSP panel ID",
                (0x51, 8, 0, 0x12): "DSP panel ID"}


def _xg_names():
    names = {}
    with (CSV / "midi_parameter_change.csv").open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            low = r["Address (H) low"].split()
            if low:
                names.setdefault((r["Address (H) high"].strip(), low[0]), r["Parameter"].replace("\n", " ").strip())
    return names


XG_NAMES = _xg_names()


def _vlq(b, i):
    v = 0
    while True:
        c = b[i]
        i += 1
        v = (v << 7) | (c & 0x7F)
        if not c & 0x80:
            return v, i


class VoiceFile:
    """A Voice file as header + list of [delta, raw_event_bytes] (raw bytes include status / F0 / FF)."""

    def __init__(self, header, events):
        self.header, self.events = header, events

    @classmethod
    def load(cls, path):
        b = Path(path).read_bytes()
        if b[:4] != b"MThd":
            raise ValueError(f"{path}: not a Standard MIDI File")
        i = 8 + int.from_bytes(b[4:8], "big")
        events = []
        while i < len(b):
            j, end = i + 8, i + 8 + int.from_bytes(b[i + 4:i + 8], "big")
            status = None
            while j < end:
                dt, j = _vlq(b, j)
                start = j
                if b[j] == 0xFF:
                    ln, k = _vlq(b, j + 2)
                    j = k + ln
                elif b[j] in (0xF0, 0xF7):
                    ln, k = _vlq(b, j + 1)
                    j = k + ln
                else:
                    if b[j] & 0x80:
                        status = b[j]
                        j += 1
                    j += 1 if (status & 0xF0) in (0xC0, 0xD0) else 2
                    raw = b[start:j] if b[start] & 0x80 else bytes([status]) + b[start:j]
                    events.append([dt, raw])
                    continue
                events.append([dt, b[start:j]])
            i = end
        return cls(b[:8 + int.from_bytes(b[4:8], "big")], events)

    def to_bytes(self):
        track = b""
        for dt, raw in self.events:
            if dt > 127:
                raise ValueError("delta times above 127 are not supported")
            track += bytes([dt]) + raw
        return self.header + b"MTrk" + len(track).to_bytes(4, "big") + track

    def save(self, path):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        Path(path).write_bytes(self.to_bytes())

    def copy(self):
        return VoiceFile(self.header, [list(e) for e in self.events])

    # --- finding / editing -------------------------------------------------------------------
    def _find(self, pred, what):
        idx = [i for i, (_, r) in enumerate(self.events) if pred(r)]
        if len(idx) != 1:
            raise KeyError(f"{what}: expected 1 event, found {len(idx)}")
        return idx[0]

    def xg(self, high, low, *values, mid=0x00):
        """Set XG parameter `F0 len 43 10 4C high mid low values F7` (e.g. Multi Part 08 00 lo, insertion 03 00 lo)."""
        key = XG_PREFIX + bytes([high, mid, low])
        i = self._find(lambda r: r[0] == 0xF0 and r[2:8] == key, f"XG {high:02X} {mid:02X} {low:02X}")
        r = self.events[i][1]
        if len(r) != 9 + len(values):
            raise ValueError(f"XG {high:02X} {mid:02X} {low:02X} holds {len(r) - 9} byte(s), got {len(values)}")
        self.events[i][1] = r[:8] + bytes(values) + b"\xF7"

    def yamaha(self, sub, a, b, c, value):
        """Set Yamaha-specific `F0 len 43 73 01 sub a b c value F7` (single-value forms only)."""
        key = YAMAHA_PREFIX + bytes([sub, a, b, c])
        i = self._find(lambda r: r[0] == 0xF0 and r[2:9] == key, f"Yamaha {sub:02X} {a:02X} {b:02X} {c:02X}")
        r = self.events[i][1]
        if len(r) != 11:
            raise ValueError("multi-byte Yamaha message; edit events directly")
        self.events[i][1] = r[:9] + bytes([value]) + b"\xF7"

    def cc(self, number, value):
        i = self._find(lambda r: r[0] == 0xB0 and r[1] == number, f"CC{number}")
        self.events[i][1] = bytes([0xB0, number, value])

    def nrpn(self, lsb, value, msb=0x01):
        """Set the Data Entry MSB that follows NRPN msb/lsb (e.g. 01/64 = EG Decay)."""
        ev = self.events
        for i in range(len(ev) - 2):
            if ev[i][1] == bytes([0xB0, 0x63, msb]) and ev[i + 1][1] == bytes([0xB0, 0x62, lsb]):
                ev[i + 2][1] = bytes([0xB0, 0x06, value])
                return
        raise KeyError(f"NRPN {msb:02X}/{lsb:02X}")

    def voice(self, msb, lsb, pc_number):
        """Retarget the base Voice; pc_number is the Voice List's PC# (1-128)."""
        self.cc(0, msb)
        self.cc(32, lsb)
        i = self._find(lambda r: r[0] == 0xC0, "Program Change")
        self.events[i][1] = bytes([0xC0, pc_number - 1])

    def _dsp_span(self):
        s = self._find(lambda r: r[0] == 0xF0 and r[2:8] == XG_PREFIX + bytes([3, 0, 0]), "DSP type")
        e = max(i for i, (_, r) in enumerate(self.events)
                if r[0] == 0xF0 and r[2:9] == YAMAHA_PREFIX + bytes([0x51, 8, 0, 0x12]))
        return s, e

    def splice_dsp(self, donor):
        """Replace this file's DSP block (XG 03 00 00 .. Yamaha 51 08 00 12) with the donor's."""
        s, e = self._dsp_span()
        ds, de = donor._dsp_span()
        self.events[s:e + 1] = [list(x) for x in donor.events[ds:de + 1]]


# --- labelling -------------------------------------------------------------------------------
def label(raw):
    hx = raw.hex(" ").upper()
    if raw[0] == 0xFF:
        return f"META {hx}"
    if raw[0] & 0xF0 == 0xB0:
        return f"CC   {hx:12} {CC_NAMES.get(raw[1], f'CC{raw[1]}')} = {raw[2]}"
    if raw[0] & 0xF0 == 0xC0:
        return f"PC   {hx:12} Program = {raw[1]} (PC# {raw[1] + 1})"
    if raw[0] == 0xF0 and raw[2:5] == XG_PREFIX:
        hi, mid, lo = raw[5], raw[6], raw[7]
        name = XG_NAMES.get((f"{hi:02X}", f"{lo:02X}"), "?")
        return f"XG   {hi:02X} {mid:02X} {lo:02X} = {raw[8:-1].hex(' ').upper():6} {name}"
    if raw[0] == 0xF0 and raw[2:5] == YAMAHA_PREFIX:
        name = YAMAHA_NAMES.get(tuple(raw[5:9]), "?")
        return f"YAM  {raw[5:-1].hex(' ').upper():30} {name} (Yamaha-specific; see kb/lab)"
    return f"??   {hx}"


def decode_lines(path):
    v = VoiceFile.load(path)
    lines, nrpn = [], None
    for _, raw in v.events:
        text = label(raw)
        if raw[:2] == bytes([0xB0, 0x62]):
            nrpn = raw[2]
        elif raw[:2] == bytes([0xB0, 0x06]) and nrpn in NRPN_NAMES:
            text += f"   <- NRPN 01/{nrpn:02X} {NRPN_NAMES[nrpn]}"
        lines.append(text)
    return lines


if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "decode":
        for p in sys.argv[2:]:
            print(f"== {p}")
            print("\n".join(decode_lines(p)))
    elif len(sys.argv) == 4 and sys.argv[1] == "diff":
        a, b = decode_lines(sys.argv[2]), decode_lines(sys.argv[3])
        for line in difflib.unified_diff(a, b, sys.argv[2], sys.argv[3], n=0, lineterm=""):
            print(line)
    else:
        print(__doc__)
        sys.exit(2)
