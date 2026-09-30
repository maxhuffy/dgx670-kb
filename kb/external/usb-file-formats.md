# What are the DGX-670's USB file formats (Voice, Registration, Playlist), and can they be edited on a PC?
topic: DGX-670 USB file formats (.vce Voice, .rgt Registration Bank, .tsv Playlist) and editing them on a computer
status: partial
researched: 2026-09-30
manual_gap: The manuals say which data can be saved as files and give only a few formats: backup ".bup" [OM p.33], Songs as SMF format 0 [OM p.68], audio WAV 44.1 kHz/16-bit [OM p.72], text ".txt" up to 60 KB [RM p.47], Styles in SFF GE [OM p.49]. They give no extension or internal format for Voice, Registration Bank or Playlist files.
queries: "DGX-670 file extensions registration bank user voice playlist file format USB"; "Yamaha registration file format RGT reverse engineered editor PC tool PSR Genos"; "Yamaha playlist .tsv file edit text editor registration playlist Genos PSR-SX DGX-670"; "Yamaha Registration Manager YRM 5.3 DGX-670 playlist tsv voice settings edit registration button features"; "DGX-670 edit voice file computer VCE sequencer Cakewalk sysex voice set"; "sandsoftwaresound VCE user voice file Standard MIDI File in disguise Yamaha arranger"; "Yamaha RGT registration bank file binary format reverse engineered open source tool github Genos PSR-SX registration parser"
summary: Voice files (.vce) are Standard MIDI Files holding parameter settings; Playlists (.tsv) are plain tab-separated text that link .rgt files by path. Registration Banks (.rgt) are proprietary binary with no public spec, but the Windows tool Yamaha Registration Manager (v5.3+) reads/edits/writes them for the DGX-670. No encryption reported for any of them.

## Manual baseline
- The File Selection display has three locations: Preset, User (internal) and USB1 [OM p.24]. Files can be saved,
  renamed, copied, moved and deleted there; nothing can be saved to Preset [OM p.26].
- Voice Set edits are saved as a file to the User drive or a USB flash drive [RM p.12].
- Registration Memory: the four buttons are saved together as one Registration Memory Bank file [OM p.80]. The
  Registration Sequence is saved as part of the Bank file [RM p.64].
- A Playlist file stores Records, which are links that call up a Registration Memory Bank file (and optionally a
  specific Registration number) [OM p.80, OM p.86, RM p.65].
- Setup Files: System Setup, MIDI Setup and User Effect files [RM p.90]. The microphone setting file can only be saved
  to the User drive; to put it on USB, save a User Effect file [RM p.59].
- Full backup: everything on the User drive (except protected Songs) plus settings, as one ".bup" file [OM p.33].
  Protected Songs cannot be copied or moved to USB [OM p.29].
- Other file types: Songs saved as SMF format 0 [OM p.68]; WAV audio 44.1 kHz/16-bit stereo [OM p.72, OM p.75];
  ".txt" text files up to 60 KB for the Text display [RM p.47]; Styles in SFF GE format [OM p.49].

## Findings
**[E1]** On the DGX-670, Registration Bank files use the ".rgt" extension, Playlist files ".tsv" and Voice files ".vce". Yamaha's bonus DGX-670 Playlist pack contains 1,100 .rgt files linked from 16 .tsv Playlists sorted by genre, copied to the root of a USB drive. Source: PSR Tutorial forum, DGX-670 threads (seen via search excerpts only; the site blocks direct fetches). https://forum.psrtutorial.com/index.php?msg=521269 and https://forum.psrtutorial.com/index.php?msg=473614. Type: forum. Applies to: DGX-670. Trust: medium (several consistent excerpts, not read in full).

**[E2]** A Playlist ".tsv" is a plain text file. Opened in Notepad, each Record is a line that includes the path of its .rgt file, e.g. "I:/PSR-SX900 Playlist/Ballroom/Amapola.rgt". Users make a USB Playlist work from internal memory by replacing "I:/" with "C:/REGIST/" in a text editor. Source: PSR Tutorial forum (search excerpt). https://forum.psrtutorial.com/index.php?msg=514430. Type: forum. Applies to: PSR-SX900 (same Playlist system as the DGX-670). Trust: medium (the drive letters may differ on the DGX-670; untested).

**[E3]** "tsv" stands for Tab Separated Values, so Playlist files can be edited in a spreadsheet such as Excel. The same article lists "rgt" as the Registration file extension and says Voice files' "Data format is MIDI". Source: The Unofficial YAMAHA Keyboard Resource Site (Jørgen Sørensen), "Yamaha File Extensions". http://www.jososoft.dk/yamaha/articles/software_12.htm. Type: third-party doc. Applies to: Yamaha arrangers in general. Trust: medium-high (long-standing reference site).

**[E4]** User Voice files (.vce and related extensions: liv, swv, clv, mgv, sar, org, drm…) are "Standard MIDI Files (SMF) in disguise". Rename to ".mid" and a DAW can import them. Source: YamahaMusicians forum, "Voices, not Expansion but just from USB", user pjd, 2025-04-14. https://yamahamusicians.com/forum/threads/voices-not-expansion-but-just-from-usb.22647/post-134612. Type: forum. Applies to: Yamaha arrangers (family). Trust: high (matches [E5] and [E3]).

**[E5]** A Voice file stores parameter information only, no audio. It is an edit of an existing preset Voice. Voice files "can be created from any MIDI or style file; and modified in software", e.g. Michael Bedesem's MIDI Player II and MixMaster. Source: The Unofficial YAMAHA Keyboard Resource Site, "Voice File Format". http://jososoft.dk/yamaha/articles/voices.htm. Type: third-party doc. Applies to: Yamaha arrangers in general. Trust: medium-high (not DGX-670-specific).

**[E6]** Voice files contain only the Voice Edit settings for a Voice that must already exist on the keyboard; they override the internal Voice programming. Source: same YamahaMusicians thread, users BogdanH and pjd, 2025-04-14. https://yamahamusicians.com/forum/threads/voices-not-expansion-but-just-from-usb.22647/post-134612. Type: forum. Applies to: Yamaha arrangers (family). Trust: high.

**[E7]** The internal structure of .rgt files is proprietary to Yamaha and is binary. No public specification was found. Source: FILExt, "RGT File Extension". https://filext.com/file-extension/RGT. Type: third-party doc. Applies to: Yamaha arrangers in general. Trust: medium (a generic file-extension site, but consistent with the lack of any published spec).

**[E8]** Yamaha Registration Manager (YRM), a free Windows program by Murray Best, builds new Registration Banks, edits the settings in registration buttons, copies Style/Voice settings between banks, converts banks between models, and batch-processes and searches them. Source: PSR Tutorial, "Registration Manager Features" (search excerpt). https://psrtutorial.com/util/best.html. Type: third-party doc. Applies to: many Yamaha arrangers. Trust: medium-high (not read in full; the site blocks direct fetches).

**[E9]** YRM is compatible with the DGX-670 from version 5.3, with all its functions available. The DGX-670 has only 4 registrations per bank, versus 8 or 10 on PSR-S/SX, Tyros and Genos. Source: PSR Tutorial forum (search excerpt). https://forum.psrtutorial.com/index.php?msg=528845. Type: forum. Applies to: DGX-670. Trust: medium-high (the 4-per-bank detail matches [OM p.80]).

**[E10]** YRM works on files, not on the keyboard's internal memory: changes "can't be saved directly on the Genos", only to the USB drive. With the keyboard connected by USB and MIDI receive on, YRM can audition registration changes live ("MIDI Sampling"). Source: YamahaMusicians forum, YRM thread, Murray Best, 2025-01-07. https://yamahamusicians.com/forum/viewtopic.php?p=129624. Type: forum (tool author). Applies to: Genos (DGX-670 support for this feature not confirmed). Trust: high for Genos.

**[E11]** An older tool, Kim Winther's PSR Registration Memory Editor, edits .rgt files on a PC (bank names, icons, style names, tempo, multipad and song names…) for PSR-3000, PSR-S900/S910 and Tyros 1–3. This shows hobbyists have decoded parts of the .rgt format. Source: PSR Tutorial, Kim Winther utilities page (search excerpt). https://psrtutorial.com/util/winther.html. Type: third-party doc. Applies to: older models only. Trust: medium.

## Not found
- A byte-level specification of the .rgt format for any model, or an open-source .rgt parser (GitHub, PyPI) — as of 2026-09-30.
- Any report of encryption or checksums in .vce, .rgt, .tsv or .bup files — neither confirmed nor ruled out.
- The .bup backup format and the Setup File formats (System/MIDI/User Effect): no community documentation found.
- A DGX-670-specific breakdown of which MIDI/SysEx events a .vce file contains (none online; since worked out
  first-hand, see [LAB voice-file-format]).
- Any way to write to the internal User drive from a computer; every tool found works on files on a USB drive.
- PSR Tutorial pages could only be seen through search excerpts (the site returns a Cloudflare challenge to fetches).

## Practical takeaway
- Manual-backed: Voices, Registration Banks, Playlists, Songs, Styles, Setup Files, WAV, text and a full backup can
  all live on a USB drive. Selecting them from the USB1 location, or copying them to the User drive, is done on the
  panel [OM p.24, OM p.29, OM p.33, RM p.90].
- External, not from the manuals:
  - Playlists (.tsv) are plain text and can be written by any program [EXT usb-file-formats#E2, #E3].
  - Voices (.vce) are MIDI files, so a program can read and likely write them [EXT usb-file-formats#E4, #E5]. The
    community GM/XG Voice files for the DGX-670 show generated .vce files do load [EXT synth-waveform-voice-choice#E2].
  - Registration Banks (.rgt) have no public spec, but YRM reads and writes DGX-670 banks [EXT usb-file-formats#E8, #E9].
  - Every route found goes through files on USB; the keyboard still has to load or copy them (panel presses).
- Lab-tested on the user's DGX-670 (not from the manuals): generated .vce files load and play; the full field map
  is in `kb/lab/voice-file-format.md` [LAB voice-file-format#L4, #L12].
