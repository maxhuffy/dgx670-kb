# Lab Findings (tested on the user's DGX-670)

First-hand findings: analysis of files the instrument saved, generated files loaded on it, and what its display
showed. Trust tier between the manuals and `external/`: cite as `[LAB <slug>#L<n>]`, label "(lab-tested on the
user's DGX-670, not from the manuals)", and respect each finding's status (confirmed / likely / hypothesis /
unknown). Format and rules: `README.md`.

| Topic | File | Status | Tested | Summary |
|---|---|---|---|---|
| Internal format of DGX-670 Voice (Voice Set) files, panel-value mapping, and generating edited Voices on a computer | [voice-file-format](voice-file-format.md) · [voice_file_fields.csv](voice_file_fields.csv) | partial | 2026-10-01 | A Voice file is a ~670-byte Standard MIDI File of XG parameter messages (part 0, insertion effect 0) plus ~12 Yamaha-specific messages; no checksum, no encryption, name = filename. Files generated on a PC load and play; panel values map to file values by simple rules (confirmed from screenshots). Field map: voice_file_fields.csv. |
