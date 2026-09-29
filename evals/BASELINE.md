# Eval run 2026-09-29 13:27 (model: newest result per question)

**Passed 10/10** · mean score 1.00 · total $2.57 · $0.257/question · avg 186,839 in / 2,782 out tokens

| Question | Category | Pass | Expected cited | Cost | Tokens in/out | Turns | Tool calls | Secs |
|---|---|---|---|---|---|---|---|---|
| menu-acmp-default | menu-path | ✅ | ✓ | $0.258 | 205,723/2,524 | 11 | 0 | 50 |
| menu-split-point | menu-path | ✅ | ✓ | $0.242 | 160,046/2,617 | 11 | 10 | 27 |
| xref-metronome | cross-manual | ✅ | ✓ ✓ | $0.298 | 247,161/3,733 | 14 | 0 | 38 |
| xref-style-creator | cross-manual | ✅ | ✓ ✓ | $0.230 | 116,039/3,095 | 9 | 0 | 31 |
| fig-main-display-registration | figure | ✅ | ✓ ✓ | $0.205 | 116,851/1,744 | 8 | 7 | 19 |
| fig-rear-panel-order | figure | ✅ | ✓ ✓ | $0.235 | 119,040/2,410 | 8 | 7 | 31 |
| datalist-direct-access | data-list | ✅ | ✓ | $0.232 | 234,942/1,649 | 10 | 9 | 21 |
| general-auto-power-off | general | ✅ | ✓ | $0.287 | 209,365/3,325 | 13 | 0 | 34 |
| neg-adapter-cable-weight | undocumented | ✅ | ND ✓ | $0.262 | 162,520/2,678 | 11 | 0 | 28 |
| neg-vst-plugins | undocumented | ✅ | ND ✓ | $0.324 | 296,709/4,052 | 14 | 0 | 40 |

## Answers (review against `notes`)

### menu-acmp-default — PASS
**Q:** How do I make the ACMP button be off by default when I turn the keyboard on?

**Expected:** [MENU] → Cursor buttons [▲][▼][◀][▶] Style Setting, [ENTER] → TAB [◀][▶] Setting2 → Cursor button [▲] 1 ACMP On/Off Default [OM p.50].

**Cited:** OM-050, RM-023, RM-024

Change the **ACMP On/Off Default** setting to Off. It controls whether the [ACMP] button is on or off at power-on [RM p.24]. The factory default is on [OM p.50].

Steps:
1. Press [MENU], then use Cursor buttons [▲][▼][◀][▶] to select **Style Setting** and press [ENTER] [OM p.50].
2. Use TAB [◀][▶] to open the **Setting2** tab [OM p.50].
3. Use Cursor button [▲] to go to page **1**, which holds "OTS Link Timing, Intro/Ending, Synchro Stop, ACMP On/Off" [OM p.50, RM p.24].
4. Use the **[7▲▼]/[8▲▼]** buttons to set **ACMP On/Off Default** to Off [RM p.24]. The [1▲▼]–[8▲▼] buttons under each setting change its value [RM p.23].

The full menu path as printed: [MENU] → Cursor buttons [▲][▼][◀][▶] Style Setting, [ENTER] → TAB [◀][▶] Setting2 → Cursor button [▲] 1 ACMP On/Off Default [OM p.50].

Notes:
- Some Styles have no rhythm unless [ACMP] is on. With one of those, turn [ACMP] on by hand [OM p.50].
- With [ACMP] off, [SYNC START] starts the Style on any key you press. With it on, the Style starts when you play a chord with your left hand. This applies unless Chord Fingering is AI Full Keyboard or Full Keyboard [OM p.50].
- Synchro Stop, on the same Setting2 page, only works while [ACMP] is on [RM p.24].

Sources: OM p.50 · RM p.23 · RM p.24

<details><summary>Tool trace</summary>


</details>

### menu-split-point — PASS
**Q:** How do I change where the keyboard splits between my left-hand and right-hand sounds?

**Expected:** Split Point procedure in 'Changing the Split Points' [OM p.58] (default F#2 per OM p.38).

**Cited:** OM-038, OM-057, OM-058, OM-059

The setting you want is the **Left Split Point**. It divides the keyboard into the Left part (your left-hand sound) and the Main/Layer parts (your right-hand sound). By default it is at F#2 [OM p.58], [OM p.38].

Steps:
1. Press [MENU], use the Cursor buttons [▲][▼][◀][▶] to select Split Point/Chord Fingering, and press [ENTER]. Then press TAB [◀] to open Split Point [OM p.58].
2. Set the split key in one of two ways [OM p.58]:
   - Press the **[6▲▼]** buttons ("Left"), or
   - Hold one of the **[7▲▼]** (KBD) buttons and press the key where you want the split.

Notes:
- **Two split points:** The keyboard has two. The **Left Split Point** separates the left-hand and right-hand sounds. The **Style Split Point** marks off the Chord section used for Style playback. Both start at F#2, but you can set them separately [OM p.58].
  - [4▲▼]/[5▲▼] "Style" sets only the Style Split Point [OM p.58].
  - [8▲▼] "Style + Left" moves both to the same key, either with the Data dial or by holding [8▲▼] (KBD) and pressing a key [OM p.58].
- **Lower limit:** The Left Split Point can't be set lower than the Style Split Point [OM p.58]. If you want to move the left-hand split lower while using Styles, use [8▲▼] "Style + Left", or lower the Style Split Point first.
- **Turn on the Left part:** The split only takes effect when the Left part is on. Turn it on with the PART ON/OFF buttons. When it's off, the Main and Layer parts use the whole keyboard [OM p.38].
- **Related setting:** The same Split Point screen is where you move the Chord Detection Area from the left-hand section (Lower) to the right-hand section (Upper). This lets you play bass with your left hand and control Style chords with your right [OM p.57], [OM p.59]. The Reference Manual has the details [OM p.57].

Sources: OM p.38 · OM p.57 · OM p.58 · OM p.59

If you confirm this is right, I can save it as a verified FAQ entry.

<details><summary>Tool trace</summary>

- `main: Grep {"pattern": "split", "path": "C:\\Users\\maxhu\\Desktop\\Yamaha DGX 670 PDFs and Text\\faq\\INDEX.md", "-i": true, "output_mode": "content"}`
- `main: Grep {"pattern": "split|left.?hand|right.?hand", "path": "C:\\Users\\maxhu\\Desktop\\Yamaha DGX 670 PDFs and Text\\kb\\maps\\GLOSSARY.md", "-i": `
- `main: Grep {"pattern": "split", "path": "C:\\Users\\maxhu\\Desktop\\Yamaha DGX 670 PDFs and Text\\kb\\maps\\TERMS.md", "-i": true, "output_mode": "cont`
- `main: Grep {"pattern": "split", "path": "C:\\Users\\maxhu\\Desktop\\Yamaha DGX 670 PDFs and Text\\kb\\maps\\MENU_PATHS.md", "-i": true, "output_mode": `
- `main: Grep {"pattern": "split|SPLIT", "path": "C:\\Users\\maxhu\\Desktop\\Yamaha DGX 670 PDFs and Text\\kb\\maps\\BUTTONS.md", "-i": true, "output_mode`
- `main: Grep {"pattern": "split", "path": "C:\\Users\\maxhu\\Desktop\\Yamaha DGX 670 PDFs and Text\\kb\\maps\\TOC.md", "-i": true, "output_mode": "conten`
- `main: Read {"file_path": "C:\\Users\\maxhu\\Desktop\\Yamaha DGX 670 PDFs and Text\\kb\\pages\\OM\\OM-058.md"}`
- `main: Read {"file_path": "C:\\Users\\maxhu\\Desktop\\Yamaha DGX 670 PDFs and Text\\kb\\pages\\OM\\OM-059.md"}`
- `main: Read {"file_path": "C:\\Users\\maxhu\\Desktop\\Yamaha DGX 670 PDFs and Text\\kb\\pages\\OM\\OM-057.md"}`
- `main: Read {"file_path": "C:\\Users\\maxhu\\Desktop\\Yamaha DGX 670 PDFs and Text\\kb\\pages\\OM\\OM-038.md"}`

</details>

### xref-metronome — PASS
**Q:** How do I change the metronome's time signature and turn the bell on the first beat on or off?

**Expected:** Path via [MENU] → Metronome Setting [OM p.44]; Metronome page: [3▲▼]–[5▲▼] Sound (bell accent), [6▲▼]/[7▲▼] Time Signature [RM p.5].

**Cited:** OM-044, RM-005

Both settings are on the same screen, the "1 Metronome" page of Metronome Setting. Time Signature sets the meter, and the Sound setting controls whether a bell accent plays on the first beat of each measure [RM p.5].

Steps:
1. Press [MENU] → Cursor buttons [▲][▼][◀][▶] Metronome Setting, [ENTER] [RM p.5]
2. Use the Cursor buttons [▲][▼] to pick the page. You want page **1 Metronome**, which the Owner's Manual reaches with Cursor button [▲] [RM p.5] [OM p.44]
3. **Time Signature:** use [6▲▼]/[7▲▼] to set the time signature of the metronome sound [RM p.5]
4. **Bell on the first beat:** use [3▲▼]–[5▲▼] (Sound). This "determines whether a bell accent is sounded or not at the first beat of each measure" [RM p.5]
5. Volume is on the same page, under [2▲▼] [RM p.5]

Notes:
- The [METRONOME] button starts and stops the metronome. You set its tempo the same way as a Style's tempo [OM p.44]
- The Tap Tempo page on the same screen sets the sound and volume you hear when you tap [TEMPO/TAP]. It's separate from the metronome's bell [RM p.5]
- The page text doesn't give the exact option names for Sound or the available time signatures. They're probably in the screen image [FIG RM-005-f1], which hasn't been described yet. I can get it described if you want the exact labels.

Sources: RM p.5 · OM p.44

**Knowledge-base update:** I added a glossary row that maps "bell / accent on beat 1 / downbeat click" to Metronome Settings → Sound (`kb/maps/GLOSSARY.md`). **I didn't commit or push it**, for two reasons: the file already had changes that weren't committed before this session, and committing now would include them too; and my git commands were denied. Once you've looked at those earlier changes, you can commit with `git add kb/maps/GLOSSARY.md && git commit -m "kb: glossary bell accent" && git push`.

<details><summary>Tool trace</summary>


</details>

### xref-style-creator — PASS
**Q:** Can I create my own Style from scratch, and where do I start?

**Expected:** Style Creator: [MENU] → Cursor buttons [▲][▼][◀][▶] Style Creator, [ENTER] [OM p.59]; full procedure in RM Ch3 'Creating/Editing Styles (Style Creator)' [RM p.26+].

**Cited:** OM-059, RM-026, RM-027, RM-028, RM-032

You can build your own Style from scratch. The Style Creator has a **New Style** option that gives you a blank Style to record into [RM p.26]. Each Style is made of Sections (Intro, Main, Fill In, Ending, and so on), and each Section has eight channels called "Source Patterns." You record or copy each channel separately [RM p.26].

Steps:
1. Select a Style to use as the basis for the new one [RM p.26]. The manual's general advice is to pick the preset Style closest to what you want [RM p.26].
2. Open the Style Creator: [MENU] → Cursor buttons [▲][▼][◀][▶] Style Creator, [ENTER] [RM p.26] [OM p.59]. A message asks whether you want to edit the selected Style or create a new one [RM p.26].
3. **To start from scratch**, press one of the [7▲▼]/[8▲▼] (New Style) buttons. This creates a blank Style named "NewStyle" [RM p.26]. The [5▲▼]/[6▲▼] (Current Style) buttons edit the selected Style instead [RM p.26].
4. On the Basic page, pick a Section. If the Rec Channel window is showing, press [EXIT] first. Then use Cursor [▲] to select "1 Section" and the [3▲▼]/[4▲▼] (Section) buttons to choose one [RM p.26].
5. **Set the time signature first.** Select "2 Tempo/Time Signature" with Cursor [▲][▼], then set Tempo with [3▲▼]/[4▲▼] and Time Signature with [5▲▼]/[6▲▼] [RM p.27]. Changing the Time Signature later clears the data from all sections [RM p.27]. You can also set the Section's length with [5▲▼]/[6▲▼] (Pattern Length), then press [ENTER] to apply it [RM p.27].
6. Create the Source Pattern for each channel [RM p.27]:
   - **Realtime Recording** (TAB [◀][▶] Basic): record by playing the keyboard [RM p.27] [OM p.59]. Details are on RM p.28.
   - **Style Assembly** (TAB [◀][▶] Assembly): copy patterns from preset Styles or Styles you've made [RM p.27] [OM p.59]. Details are on RM p.32.
7. Edit what you recorded (optional) [RM p.27]:
   - **Groove** tab: rhythmic feel [OM p.59]. **Channel** tab: quantizing, velocity and similar edits [RM p.27] [OM p.59].
   - **Parameter** tab: Style File Format (SFF) settings [RM p.27] [OM p.59].
   - **Drum Setup** (Basic → Cursor [▼] 3 Drum Setup): change individual drum sounds [RM p.27] [OM p.59].
8. Repeat steps 4–7 for each Section you want [RM p.27].
9. **Save** with one of the [8▲▼] (Save) buttons on any page [RM p.27]. The Owner's Manual's "Basic Operations" section covers the save process [RM p.27].

Notes:
- ⚠ **Save before you switch Styles or turn off the power.** Either one erases an unsaved Style [RM p.27].
- Fill In A–D, Intro 1–4 and Ending 1–4 can be picked on the display even though they have no panel buttons [RM p.26].
- The pages I read don't say whether a blank "NewStyle" keeps anything from the Style you selected in step 1.

Sources: RM p.26 · RM p.27 · OM p.59

If you want the details for step 6, I can pull up how Realtime Recording works (RM p.28) or Style Assembly (RM p.32). No knowledge-base update was needed for this one.

<details><summary>Tool trace</summary>


</details>

### fig-main-display-registration — PASS
**Q:** Where on the Main display is the Registration Memory Bank name shown?

**Expected:** Callout (5) on the Main display figure [OM p.23]; location must come from the figure description [FIG OM-023-f1] — verify against the PDF page.

**Cited:** OM-023, OM-023-f1, RM-063

The Bank name appears in item (5) of the Main display, a full-width dark-grey bar near the top of the screen [OM p.23] [FIG OM-023-f1]. The bar sits just below the thin status row and just above the Main Voice panel [FIG OM-023-f1].

**Layout of the Registration bar (5):** [FIG OM-023-f1]
- **Left side:** the label "Regist". Next to it is the current Registration number and name (for example "1 : New Regist"). The **Bank name** (for example "NewBank") is on the line beneath that.
- **Right side:** the Registration number row "1 2 3 4 1 2 3 4", with the current number highlighted.
- **Lower-right corner:** a small "F" box.

**What the bar shows:** [OM p.23]
- The currently selected Registration Memory Bank name and the current Registration number (page 81).
- When Registration Sequence is on, the programmed numbers.
- When Freeze is on (page 83), an "F" in the right corner.

**Opening the Bank's file list:** From the Main display, use the Cursor buttons [▲][▼][◀][▶] to select the Registration Memory Bank item, then press [ENTER]. This opens its File Selection display (page 24). [OM p.23]

**Notes:** The only things above the Registration bar are the status indicators: (6) Tempo, (7) Bar/Beat, (8) Mic and (9) Transpose [FIG OM-023-f1]. Items (7)–(9) are explained on the next page [OM p.23]. Registration Sequence is covered in Chapter 7 of the Reference Manual [OM p.23] [RM p.63].

Sources: OM p.23 · FIG OM-023-f1 · RM p.63

I didn't change the knowledge base: the figure description was already saved and your wording matched the manual's terms. If this answer is right, say so and I'll save it as an FAQ entry.

<details><summary>Tool trace</summary>

- `main: Grep {"pattern": "registration|bank", "path": "C:\\Users\\maxhu\\Desktop\\Yamaha DGX 670 PDFs and Text\\faq\\INDEX.md", "-i": true, "output_mode"`
- `main: Grep {"pattern": "registration|bank|main display|home screen", "path": "C:\\Users\\maxhu\\Desktop\\Yamaha DGX 670 PDFs and Text\\kb\\maps\\GLOSSA`
- `main: Grep {"pattern": "registration memory|main display|bank name", "path": "C:\\Users\\maxhu\\Desktop\\Yamaha DGX 670 PDFs and Text\\kb\\maps\\TERMS.`
- `main: Grep {"pattern": "registration|main display", "path": "C:\\Users\\maxhu\\Desktop\\Yamaha DGX 670 PDFs and Text\\kb\\maps\\TOC.md", "-i": true, "o`
- `main: Grep {"pattern": "registration|main display", "path": "C:\\Users\\maxhu\\Desktop\\Yamaha DGX 670 PDFs and Text\\kb\\maps\\MENU_PATHS.md", "-i": t`
- `main: Read {"file_path": "C:\\Users\\maxhu\\Desktop\\Yamaha DGX 670 PDFs and Text\\kb\\pages\\OM\\OM-023.md"}`
- `main: Read {"file_path": "C:\\Users\\maxhu\\Desktop\\Yamaha DGX 670 PDFs and Text\\kb\\figures\\OM-023.md"}`

</details>

### fig-rear-panel-order — PASS
**Q:** Looking at the rear panel, which connector is at the far left and which is at the far right?

**Expected:** Rear panel figure with callouts (1)–(7) [OM p.14, FIG OM-014-f1]; positions come only from the figure — verify against the PDF page.

**Cited:** OM-014, OM-014-f1

In the manual's rear-panel drawing, the **[USB TO HOST] terminal** is at the far left and the **DC IN jack** (the AC adaptor socket) is at the far right. [OM p.14] [FIG OM-014-f1]

Full order as drawn, left to right [OM p.14] [FIG OM-014-f1]:
1. [USB TO HOST] terminal: connects to a computer or smart device
2. [AUX PEDAL] jack: the included footswitch or separately sold foot pedals
3. [PEDAL UNIT] jack: a separately sold pedal unit
4. (wide gap)
5. [MIC INPUT] jack: a microphone
6. [AUX IN] jack: an external audio device, such as a portable player
7. [PHONES/OUTPUT] jack: headphones or external speakers
8. DC IN jack: the AC adaptor. It sits in its own small box, separate from the others.

Notes:
- The drawing shows the panel face-on, but neither the figure nor its text says whether its left side is your left when you sit at the keys. So this is the left-to-right order as the manual draws it. If you look at the back of the instrument from behind, the order could be the other way round. [FIG OM-014-f1]
- The printed callout order "(7) (1) (2) … (6)" in the page text comes from how the PDF text was extracted, not from the layout. In the drawing, (7) DC IN is on the far right. [FIG OM-014-f1]
- Before connecting anything, turn off the power on all equipment and set all volume levels to minimum (0). [OM p.14]

Sources: OM p.14 · FIG OM-014-f1

<details><summary>Tool trace</summary>

- `main: Grep {"pattern": "rear|panel|connector|jack|terminal", "path": "C:\\Users\\maxhu\\Desktop\\Yamaha DGX 670 PDFs and Text\\faq\\INDEX.md", "-i": tr`
- `main: Grep {"pattern": "rear|back panel|connector|jack|port", "path": "C:\\Users\\maxhu\\Desktop\\Yamaha DGX 670 PDFs and Text\\kb\\maps\\GLOSSARY.md",`
- `main: Grep {"pattern": "rear panel|panel controls|terminals|connector", "path": "C:\\Users\\maxhu\\Desktop\\Yamaha DGX 670 PDFs and Text\\kb\\maps\\TER`
- `main: Grep {"pattern": "rear|panel controls|terminal|connect", "path": "C:\\Users\\maxhu\\Desktop\\Yamaha DGX 670 PDFs and Text\\kb\\maps\\TOC.md", "-i`
- `main: Read {"file_path": "C:\\Users\\maxhu\\Desktop\\Yamaha DGX 670 PDFs and Text\\kb\\pages\\OM\\OM-014.md"}`
- `main: Read {"file_path": "C:\\Users\\maxhu\\Desktop\\Yamaha DGX 670 PDFs and Text\\kb\\pages\\OM\\OM-015.md"}`
- `main: Read {"file_path": "C:\\Users\\maxhu\\Desktop\\Yamaha DGX 670 PDFs and Text\\kb\\figures\\OM-014.md"}`

</details>

### datalist-direct-access — PASS
**Q:** If I press the DIRECT ACCESS button and then the MIXER/EQ button, which display comes up?

**Expected:** OM p.22 defers to the Direct Access Chart in the Data List [DL p.78]; answer is the chart row for [MIXER/EQ].

**Cited:** DL-078, OM-022

It opens the **Mixer** display on its **Volume/Pan (Panel)** page [DL p.78]. That's the Direct Access Chart's entry for [MIXER/EQ], and it sets no sub-page or item beyond that [DL p.78].

Steps:
1. Press [DIRECT ACCESS]. A message appears asking you to press the button you want [OM p.22].
2. Press [MIXER/EQ]. The display for that button comes up right away [OM p.22]. For [MIXER/EQ], that is Mixer › Volume/Pan (Panel) [DL p.78].

Notes:
- Pressing [DIRECT ACCESS] then [CHANNEL ON/OFF] opens the same Mixer › Volume/Pan (Panel) display [DL p.78].
- The full list of Direct Access shortcuts is in the Direct Access Chart in the Data List [OM p.22] [DL p.78].

Sources: OM p.22 · DL p.78

<details><summary>Tool trace</summary>

- `main: Grep {"pattern": "(?i)direct access", "path": "C:\\Users\\maxhu\\Desktop\\Yamaha DGX 670 PDFs and Text\\faq", "output_mode": "content"}`
- `main: Grep {"pattern": "(?i)direct access", "path": "C:\\Users\\maxhu\\Desktop\\Yamaha DGX 670 PDFs and Text\\kb\\datalist\\INDEX.md", "output_mode": "`
- `main: Grep {"pattern": "(?i)direct access", "path": "C:\\Users\\maxhu\\Desktop\\Yamaha DGX 670 PDFs and Text\\kb\\maps", "output_mode": "content"}`
- `main: Grep {"pattern": "(?i)mixer", "path": "C:\\Users\\maxhu\\Desktop\\Yamaha DGX 670 PDFs and Text\\kb\\datalist\\csv", "glob": "*direct*", "output_m`
- `main: Read {"file_path": "C:\\Users\\maxhu\\Desktop\\Yamaha DGX 670 PDFs and Text\\kb\\pages\\OM\\OM-022.md"}`
- `main: Grep {"pattern": "(?i)direct.access|DL.?0?78|mixer", "path": "C:\\Users\\maxhu\\Desktop\\Yamaha DGX 670 PDFs and Text\\kb\\datalist\\ISSUES.md", `
- `main: Read {"file_path": "C:\\Users\\maxhu\\Desktop\\Yamaha DGX 670 PDFs and Text\\kb\\datalist\\csv\\direct_access.csv", "limit": 3}`
- `main: Read {"file_path": "C:\\Users\\maxhu\\Desktop\\Yamaha DGX 670 PDFs and Text\\kb\\datalist\\pages\\DL-078.md"}`
- `main: Read {"file_path": "C:\\Users\\maxhu\\Desktop\\Yamaha DGX 670 PDFs and Text\\kb\\datalist\\INDEX.md", "offset": 72, "limit": 11}`

</details>

### general-auto-power-off — PASS
**Q:** My keyboard keeps turning itself off. Why, and how do I stop that?

**Expected:** Auto Power Off: default time, how to change it, and the simple disable method [OM p.17].

**Cited:** OM-017, OM-018, OM-103, RM-090

The keyboard is almost certainly being turned off by its **Auto Power Off** function. The Owner's Manual troubleshooting section describes this: "The power is automatically turned off. This is normal and due to the Auto Power Off function." [OM p.103] It switches the keyboard off if you don't use it for a set time, which is **15 minutes by default** [OM p.17].

**To turn it off permanently (in the menu):**
1. Press [MENU], then use the Cursor buttons [▲][▼][◀][▶] to select **System**, and press [ENTER] [OM p.18].
2. Press TAB [◀] to open the **Common** tab [OM p.18].
3. Use the [1▲▼]/[2▲▼] buttons to set **Auto Power Off** to **Disabled**. You can also pick a longer time here instead of disabling it [OM p.18].
4. Press [EXIT] to go back [OM p.18].

**Quick method (at startup):**
- Hold down the lowest key on the keyboard while you turn the power on. A message appears briefly, then the keyboard starts with Auto Power Off disabled [OM p.17].

**Notes:**
- **Save your work.** If the keyboard switches off by itself, anything you haven't saved with the Save operation is lost [OM p.17].
- Even in standby, a small amount of power still flows to the keyboard. Unplug it if you won't use it for a long time or during electrical storms [OM p.17].
- The manuals don't list the other time options. They also don't say whether the quick method lasts beyond that one startup. Use the menu setting if you want a permanent change.

Sources: OM p.17 · OM p.18 · OM p.103 (RM p.90 just points back to "Starting Up" in the Owner's Manual)

I didn't change the knowledge base. The glossary already links "shuts off by itself" to Auto Power Off. If this answer is correct, say "save it" and I'll add it as a verified FAQ entry.

<details><summary>Tool trace</summary>


</details>

### neg-adapter-cable-weight — PASS
**Q:** What is the weight of the power adapter cable?

**Expected:** Not documented. Closest: Specifications (instrument weight 21.4 kg, power adaptor info) [OM p.106–107].

**Cited:** OM-007, OM-016, OM-106, OM-107

**Not documented in the DGX-670 manuals.** The only weight in the specifications is the keyboard's own. No weight is given for the AC adaptor, its power cord, or the DC cable. [OM p.106], [OM p.107]

**Closest documented:**
- **Instrument weight:** 21.4 kg (47 lb, 3 oz). Dimensions are 1,397 mm × 445 mm × 151 mm. [OM p.106]
- **Power supply model:** AC Adaptor PA-300C. Power consumption is 14.5 W with the PA-300C, and standby consumption is 0.3 W. [OM p.107]
- **The power parts:** the AC adaptor and a separate power cord. The cord goes from the wall outlet to the adaptor, and the adaptor's DC plug goes into the keyboard's DC IN jack. [OM p.16]
- **Included in the box:** the AC adaptor and power cord, though they "May not be included depending on your area." The PA-300C is also sold separately. [OM p.7], [OM p.107]
- **Warning:** "Use the specified AC adaptor (page 107) only. Using the wrong AC adaptor can result in damage to the instrument or overheating." [OM p.16]

The manual doesn't say whether the 21.4 kg includes the adaptor, so I haven't assumed either way.

Sources: OM p.7 · OM p.16 · OM p.106 · OM p.107

---
**Knowledge base:** "power adapter" isn't in the glossary; the manuals spell it "AC adaptor". I didn't add the row because `kb/maps/GLOSSARY.md` already has uncommitted changes from before this session. I couldn't view that diff (the git command was denied), and committing now would include those changes. If you commit or discard them first, I'll add this row and push it:
`| power adapter, power brick, charger, power cable | AC adaptor; PA-300C; power cord; DC IN |`

<details><summary>Tool trace</summary>


</details>

### neg-vst-plugins — PASS
**Q:** Can I install third-party VST plugins on the DGX-670?

**Expected:** Not documented. Closest: computer connection via [USB TO HOST] [OM p.92] / Connections chapter.

**Cited:** OM-092, OM-093

**Not documented in the DGX-670 manuals.** The manuals never mention VST, plugins, or installing any software onto the instrument.

**Closest documented:**
- **Connecting to a computer:** A computer plugged into the [USB TO HOST] terminal can exchange MIDI data and audio data with the instrument. [OM p.92]
- **USB Audio Interface function:** Over the same USB connection, the instrument can send and receive digital audio with a computer or smart device. This lets you play audio back at higher quality than through [AUX IN], and record your playing as audio in recording or music production software. [OM p.93]
- **Using a DAW:** If you use a DAW (digital audio workstation) with the instrument, set Audio Loopback to off, or a loud sound may occur. [OM p.92] The path is [MENU] → Cursor buttons [▲][▼][◀][▶] Utility, [ENTER] → TAB [◀] Config1 → Cursor buttons [▲][▼] 2 Audio Loopback. [OM p.93]
- **Driver on the computer side:** On Windows, the Yamaha Steinberg USB Driver should be installed on the computer to send or receive audio. [OM p.93] This is the only installation the manuals describe, and it goes on the computer, not the keyboard.

For more detail, the manuals point to the "Computer-related Operations" document on Yamaha's website. That document is not in this knowledge base. [OM p.92] [OM p.93]

Sources: OM p.92 · OM p.93

---

I added a row to `kb/maps/GLOSSARY.md` so "VST / plugins / software instruments" points to these pages next time. I couldn't commit or push it because the git command was denied. The change is still in your working tree, together with a glossary edit that was already uncommitted before this session and that I didn't review. To commit both:

```
git add kb/maps/GLOSSARY.md && git commit -m "kb: glossary VST/plugins" && git push
```

<details><summary>Tool trace</summary>


</details>

