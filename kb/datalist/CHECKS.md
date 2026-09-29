# Data List build checks

Automated checks run by `scripts/build_datalist.py` on every build.

| Result | Check | Expected | Got |
|---|---|---|---|
| ok | Piano Room piano types listed (CFX Grand … SweetDX) | 6 | 6 |
| ok | Main+Legacy+MegaVoice voices excl. kits = 601 (OM p.106 spec) | 601 | 601 |
| ok | Main+Legacy+MegaVoice Drum/SFX kits = 29 (OM p.106 spec) | 29 | 29 |
| ok | voices of type VRM (OM p.106 spec) | 9 | 9 |
| ok | voices of type S.Art! (OM p.106 spec) | 49 | 49 |
| ok | voices of type Natural! (OM p.106 spec) | 11 | 11 |
| ok | voices of type Sweet! (OM p.106 spec) | 26 | 26 |
| ok | voices of type Cool! (OM p.106 spec) | 53 | 53 |
| ok | voices of type Live! (OM p.106 spec) | 68 | 68 |
| ok | voices of type MegaVoice (OM p.106 spec) | 23 | 23 |
| ok | every voice has numeric MSB/LSB/PC | 0 | 0 |
| ok | songs listed (50 Popular + 50 Classics) | 100 | 100 |
| ok | styles = 263 (OM p.106 spec) | 263 | 263 |
| ok | Reverb Block: effect type No. 1..59 complete, no gaps | no gaps | no gaps |
| ok | Chorus Block: effect type No. 1..107 complete, no gaps | no gaps | no gaps |
| ok | Variation/Insertion Block: effect type No. 1..297 complete, no gaps | no gaps | no gaps |
| ok | drum/SFX kits in Drum/Key list = 29 (OM p.106 spec) | 29 | 29 |
| ok | every kit's MSB-LSB-PC also appears as a Drum/SFX voice in voices.csv | [] | [] |
| ok | drum note numbers within 13..91 | yes | yes |
| ok | light-grey cells really equal StandardKit1 sound | 0 | 0 |
| ok | parameter chart file columns hold only ○/×/– marks | 0 | 0 |
| ok | every effect parameter list has a name | 0 | 0 |
| ok | every Parameter List named in effect_types.csv exists in effect_params.csv | [] | [] |
| ok | every Effect Data Assign table has a 'Table #n' label | 0 | 0 |
| ok | each value table's Data column is contiguous with no duplicates | [] | [] |
| ok | every value table referenced by effect_params.csv exists | [] | [] |
| ok | number base table covers decimal 0..127 exactly once | yes | yes |
| ok | MegaVoice Map covers all 23 MegaVoices of voices.csv | 23 | 23 |
| ok | MegaVoice Map voices all exist in voices.csv | [] | [] |
| ok | MIDI Data Format tables yield rows for every layout | all > 0 | all > 0 |
| ok | MIDI rows extracted (sanity: > 300) | yes | yes |
| ok | every CSV has a brief in scripts/datalist_briefs.md | [] | [] |
