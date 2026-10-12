**file**: docs/requirements/requirement-python-gui.md
**Status**: Active (Version 1.6.5)
**Area**: python
**Key**: `requirement-python-gui`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-protect)

## 1. Purpose

This file is the X11 window for VideoEditor. A bare start on an interactive terminal opens this window when `DISPLAY` is set. The verb `tui` opens the text menu in `requirement-python-tui` and does not change that menu. Typed verbs stay on `requirement-python-cli-interface`.

The window has two groups. One is visible and the other is hidden. Edit is the first group. Join is the second group. A project-root line sits under the header. join and edit are tabs on the left of the group. Each group splits left and right. Edit puts Input Video, Edit Controls, and Looping Options on the left, and Output & Result on the right. Join puts the two sources on the left and the same output column on the right. A process bar sits on the bottom of the window. The window and the content column use light gray `#d3d3d3`. Each source card and each output card uses white `#ffffff`, including the video area and the controls on that card. The header bar and the process bar keep their theme colors. Each elapsed bar is a timeline thumbnail preview: a strip of scaled frames, a scrubber handle, a hover timestamp, and click or drag to move the picture.

### 1.1 Human-facing

**In one sentence:** On a terminal with an X11 display, `video-editor` opens a window with a project-root line, an edit source player, a resulting-video player, three join players, and a process bar, and `video-editor tui` opens the text menu.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | Person at a local X session or an `ssh -X` session | `video-editor` |
| The other role | Class `Gui` | `src/VideoEditor/gui.py` |
| Not this file | The curses frame, the FFmpeg graph, and the typed `join` questions | TUI, pipeline, and CLI requirements |

| Includes | Excludes |
|----------|----------|
| Edit group and Join group, one visible at a time. Project-root line. Process bar | A second text-menu painter inside the window |
| Window and content-column background `#d3d3d3`. Source and output cards, including video and controls, background `#ffffff` | The canvas color on a source or output card. White on the header bar or the process bar |
| Input Video, Edit Controls, Looping Options, Output & Result, Resulting Video. One thumbnail track per elapsed bar | A timeline editor with more than one track on the same player |
| MP4 player, `MM:SS.CC` elapsed time, Start, Pause, Stop, jump, Go To, Mark start, Mark end | Both Boomerang and Repeat on at once |
| Join players for both sources and the generated file. Edit player for the generated file. Each has the elapsed time bar and Play and Stop. Each elapsed bar is a thumbnail track with a scrubber handle | A second encode control on those buttons. A multi-track timeline editor |
| Two join file buttons that browse the host where the process runs | File-operand flags on the `join` verb |

## 2. Core Rules (Mandatory)

1. Class `Gui` in `src/VideoEditor/gui.py` owns this window. `Cli` constructs it and calls `open`. `cli.py` does not build widgets.
2. A bare start opens this window when stdin and stdout are terminals and `DISPLAY` is non-empty. That covers a local X session, XWayland when `DISPLAY` is set, and `ssh -X`. The GDK backend is X11. `WAYLAND_DISPLAY` alone does not open the window.
3. When that X server refuses the connection, or GTK 4 cannot be imported, the process exits non-zero and the next step is `video-editor tui`. It does not draw a partial window and it does not hang.
4. A bare start with `DISPLAY` unset opens the text menu. A bare start with no terminal prints help and returns 0. `video-editor tui` on a terminal opens the text menu even when `DISPLAY` is set. `tui` with no terminal exits non-zero. `tui` is not a numbered row.
5. `join`, `edit`, `list-videos`, `list-mp4`, `help`, `about`, `hello`, `version`, the pip verbs, `--json`, and a complete edit job stay on their current paths and do not open this window.
6. The menu in the window shows join, edit, system-log, language, self-management, and Exit. Those labels have no row number. The text menu keeps **1**, **2**, **3**, **4**, **8**, and **9**. Self-management opens **82**–**87**. Row **81** stays omitted. `help` and `tui` stay off this menu. A framed project-root line sits under the header. It shows a folder icon, the translated label Project Root, and the absolute current working directory. The directory is selectable and is not translated. join and edit sit in a strip directly above the stack. That strip shares the stack’s left edge and width. The label for the visible video group is highlighted, and that highlight meets the top edge of the group. system-log, language, and self-management hide both video groups and clear that highlight. Leaving a group pauses the players on that group. A process bar sits on the bottom of the window.
7. The Edit left side is an Input Video card, then Edit Controls and Looping Options side by side. Input Video has the format token `MP4:`, one **Select file** button, the player, and the time bar. That time bar, and every player time bar, is the timeline thumbnail preview in rule 14. Edit Controls has Start, Pause, Stop, a jump field whose placeholder is `00:00.00`, Go To, the cut Start and End, Mark start, Mark end, and Percent. Elapsed time sits on the left of the bar as `MM:SS.CC` (minutes at least two digits and free to grow, seconds `00`–`59`, centiseconds). Percent is a scale and a spin from 20–200 and defaults to 100. The two stay equal. Looping Options is three switches: Boomerang, Repeat, and None. Exactly one is on. The window starts on None. Turning one on clears the others. Turning the last one off returns to None. Boomerang appends the reverse. Repeat appends the clip so it plays twice. The Edit right side is an Output & Result card: **Run**, the output path, the result line, Generated, and a Resulting Video card. That player has the elapsed time bar and Play and Stop. When Run starts, that player is cleared and Play, Stop, and the time bar are disabled. When Run finishes and the output file is on disk, the player loads that file and those controls are enabled. When Run finishes without that file, the player stays cleared and those controls stay disabled. Play and Stop do not start or kill FFmpeg.
8. Mark start and Mark end store the player position into the cut start and cut end. Run uses those values with the existing encoder. The output filename keeps the one-decimal pattern. The OpenCV duration is the bound. A reversed mark or an end past that duration does not start FFmpeg.
9. The Join left side has Video 1 above Video 2. Each is a titled card with a path and a **Select file** button. The chooser accepts `.mp4`, `.mov`, `.mkv`, `.avi`, and `.m4v`. The same path cannot be chosen twice. The chooser lists files on the computer that runs `video-editor`, including the remote host under `ssh -X`. Under each source path is a player with the elapsed time bar and Play and Stop. The Join right side is the same Output & Result column as Edit, plus the output name. The default name is `{stem1} + {stem2}.mp4`. The write line names the current working directory and that file. **Run** calls `Join.run`. The Resulting Video player is the third player, with the same bar and Play and Stop. When Run starts, that generated player is cleared and Play, Stop, and the time bar are disabled. The two source players stay loaded. When Run finishes and the output file is on disk, the generated player loads that file and those controls are enabled. When Run finishes without that file, the generated player stays cleared and those controls stay disabled. Join has three players. Play and Stop do not start or kill the concat.
10. A long encode runs off the GTK main loop. Before that work starts, the generated player for the running group is cleared and its controls are disabled. The process bar and the visible result show `please wait for time consuming process`. That sentence is not translated. The bar fraction is 0 while the sentence is showing. The bar is not a live FFmpeg ticker. When the work finishes and the output file is on disk, the player loads that file, its controls are enabled, the output total shows that file’s duration, and the bar reads Process 100% at fraction 1. A later run that writes a different duration replaces that total. When the work finishes without that file, the player stays cleared, those controls stay disabled, the output total returns to `00:00.00`, and the bar returns to Process 0% at fraction 0. Idle, including a capture taken before Run, is Process 0%. Stop on the player does not kill an encode that has already started. Close waits until that encode finishes and keeps the wait sentence on the bar. The thread create and start lines go through the one ChronicleLogger with `component` `Gui`.
11. The window may open when FFmpeg or the GStreamer playback plugins are missing. Playback controls stay disabled when the player cannot be created. Run still fails closed before FFmpeg is spawned. GTK 4 and GStreamer are host packages, not pip dependencies.
12. Language strings for the menu and for the window controls come from `MenuLanguage`. A language pick redraws the open window, including an icon button, without dropping the icon. The window translates button names and captions: Select file, Start, Pause, Stop, Play, Go To, Mark start, Mark end, the cut Start and End, Percent, Tail, None, Boomerang, Repeat, Run, Output, Output name, Generated, Video 1, Video 2, Project Root, Input Video, Edit Controls, Looping Options, Output & Result, Resulting Video, Process, View, Clear, Yes, and No, plus the short sentences the window itself writes. English Go To is the current English word. The other codes keep their existing go-to words. The elapsed clock, the directory on the project-root line, the product name, the version, the format token MP4, and the About page stay as they are. The widget paints `MP4:` from that token. The text-menu path word stays Path. Leaf command tokens stay the English tokens. The wait sentence stays `please wait for time consuming process`. Join command lines, pip output, and FFmpeg sentences stay English. Pip rows call `SelfManage` and do not use sudo. Self-uninstall asks before it runs. Log view and clear use `SystemLog` and its folder fence.
13. Actor / role / subject / approver: **considered**. No dest machine. No approver.
14. Each elapsed bar on the edit source and on every player is a timeline thumbnail preview. The thumbnail track is a strip of scaled frames spanning that file, in place of a plain trough. The scrubber handle sits on the strip. The thumbnail track height is 56 pixels, inside the 48 to 64 pixel band. The edit source picture is requested at 200 pixels tall, so the thumbnail trail height proportion on that card is 56 divided by 200. Each other player picture is requested at 180 pixels tall, so the proportion there is 56 divided by 180. Both stay below one half. Hovering the strip shows the time under the pointer as `MM:SS.CC` and does not move playback or the handle. A click jumps playback to that time and moves the handle. Dragging the handle updates the picture while the pointer moves. The label on the left of the strip is the current time and uses the same clock. Frames are read on a background thread, so opening a file does not freeze the window. The sample interval is 2 seconds when the file is shorter than 2 minutes and 5 seconds otherwise. The strip does not contain every frame. A finished strip is stored in the system temporary directory and reused when the same path, size, and modification time are opened again. A cleared player drops its strip from the bar. Building the strip does not show `please wait for time consuming process`.

### 2.1 Implementation Notes (this project)

| Item | Value |
|------|--------|
| **Class** | `Gui` in `src/VideoEditor/gui.py` |
| **Open** | `video-editor` on a terminal with `DISPLAY` set |
| **Text menu** | `video-editor tui` |
| **Groups** | Edit visible hides Join. Join visible hides Edit |
| **Project root** | Folder icon, translated Project Root, absolute current working directory |
| **Process bar** | Idle and a finish without a file: Process 0%. Busy: the untranslated wait sentence. A file on disk: Process 100% |
| **Looping** | Three switches. Exactly one on. Default None |
| **Player** | GTK 4 `MediaFile` / `Video`, GStreamer, X11 backend |
| **Elapsed** | `MM:SS.CC` on the left of the time bar |
| **Thumbnail track** | Height 56 px. Source picture 200 px (proportion 56/200). Other players 180 px (proportion 56/180). Sample every 2 s, or every 5 s when the file is at least 2 minutes. Cache leaf `videoeditor-timeline-thumbs` under the system temporary directory |
| **Join players** | Three: video 1, video 2, generated. Elapsed bar, Play, Stop |
| **Edit generated** | One player on the right side, inside Resulting Video. Elapsed bar, Play, Stop |
| **Join files** | Two host file choosers on the left. Output name on the right, in the current directory |
| **Edit output** | On the right side, existing encoder name |
| **Privilege** | normal user |

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** A refused X server exits. A reversed mark does not encode.
- **Intentional:** Edit and Join are two groups. The text menu stays on `tui`.
- **Anti-fragile:** A missing player still leaves the file buttons and the typed commands usable.
- **Over-protect:** The file chooser reads the host that runs FFmpeg.

## 4. Protection Rule (Sacred)

**Future AI assistants or maintainers MUST NOT:**

- Open this window for a typed verb other than the bare start described above.
- Change the curses frame because this window exists.
- Add file-operand flags to the `join` verb.
- Let the two join buttons accept the same path.
- Browse the `ssh -X` client filesystem for a path the remote FFmpeg cannot open.
- Kill an encode from a player Stop button, or start an encode from Play.
- Drop a join source player, the join generated player, or the edit generated player.
- Leave the previous generated picture enabled while a new edit or join run is in progress.
- Put row **81** on this menu, or put `help` or `tui` on a numbered row.
- Print a row number on the window’s top menu.
- Leave the window control labels in English after a non-English menu language is selected.
- Translate the elapsed clock, the directory on the project-root line, the About page, or the wait sentence `please wait for time consuming process`.
- Turn Boomerang and Repeat on together, or leave every looping switch off.
- Paint a live FFmpeg percent on the process bar. Idle is Process 0%. A finished file on disk is Process 100%.
- Drop the icon when a language pick redraws an icon button.
- Paint the header bar, a card, a player, or the process bar with the canvas color `#d3d3d3`.
- Leave a source card or an output card on the canvas color. Those cards, including the video area and the controls on the card, use white `#ffffff`.
- Paint the header bar or the process bar white.
- Seek, or move the scrubber handle, on hover.
- Extract every frame into the thumbnail track, or build that strip on the window thread.
- Make the thumbnail track taller than 64 pixels or shorter than 48 pixels.
- Show `please wait for time consuming process` because a thumbnail strip is loading.

## 5. Acceptance criteria

| ID | Criterion |
|----|-----------|
| AC-1 | Bare start with `DISPLAY` and a terminal opens this window and does not run pip |
| AC-2 | `video-editor tui` opens the existing text menu |
| AC-3 | Edit and Join are separate groups. Each puts the source or sources on the left and the output on the right |
| AC-4 | The elapsed label is `MM:SS.CC`, and Mark start / Mark end fill the cut bounds |
| AC-5 | Join offers two file buttons and refuses the same path twice |
| AC-6 | Join shows three players (video 1, video 2, generated), each with an elapsed time bar and Play and Stop |
| AC-7 | Edit shows a generated-file player with an elapsed time bar and Play and Stop |
| AC-8 | Run clears and disables that group’s generated player first. A finished file refreshes and enables it and sets the output total to that file’s duration. A later file with a different duration replaces that total. A finish without that file leaves the player cleared and disabled and the total at `00:00.00` |
| AC-9 | The project-root line starts with the translated Project Root label and names the current working directory. The directory is not translated |
| AC-10 | Exactly one looping switch is on. The window starts on None. Turning the last switch off returns to None |
| AC-11 | Idle is Process 0% at fraction 0. A busy run shows `please wait for time consuming process`. A finished file on disk is Process 100% at fraction 1 |
| AC-12 | The window and the content column use background `#d3d3d3` |
| AC-13 | Each source card and each output card, including its video area and the controls on that card, uses background `#ffffff` |
| AC-14 | Each elapsed bar is a thumbnail track 56 px tall with a scrubber handle. Hover shows `MM:SS.CC` and does not seek. Click and drag seek and update the picture. Frames are sampled every 2 or 5 seconds on a background thread and cached in the system temporary directory |

## 6. Related requirements (peer keys only)

| Key | Relationship |
|-----|----------------|
| `requirement-python-cli-interface` | Bare start, the `tui` verb, and the other verbs |
| `requirement-python-tui` | Text menu opened by `tui` and by a bare start with no `DISPLAY` |
| `requirement-domain-videoeditor` | Join and edit steps |
| `requirement-python-oop` | Class `Gui` |
| `requirement-video-ffmpeg-pipeline` | Encode and publish |
| `requirement-python-cli-language` | Menu words and the language leaf |

### 6.1 Window screen

The window explains seven parts. Each part says what it is, where it sits, and the display style.

| Part | What it is | Where it sits | Display style |
|------|------------|---------------|---------------|
| Navigation | Header actions and the two group tabs | Header bar, start side, for system-log, language, self-management, and Exit. join and edit are tabs on the left edge of the group | Icon and words for the four header actions. Plain words for join and edit. The visible group’s tab is highlighted and meets the top of the group. system-log, language, and self-management clear that highlight |
| Status | The window title and the process bar when the window is idle or a run has finished | Title centered in the header. Process bar full width on the bottom | Title is the product name, a space, and the package version. Idle and a finish without a file: Process 0%, fraction 0. A finish with the file on disk: Process 100%, fraction 1. The percent words follow the language |
| Major input | The source and the edit settings | Left column of the visible group | White `#ffffff` cards. Edit: Input Video, then Edit Controls beside Looping Options. Input Video holds `MP4:`, Select file, the source player, and the elapsed thumbnail track. Edit Controls holds Start, Pause, Stop, the jump field, Go To, the cut bounds, Mark start, Mark end, and the percent scale with its spin. The percent scale is not a thumbnail track. Looping Options holds the three switches. Join: Video 1 above Video 2. Each card holds a path, Select file, and a player. The video area on the card is white |
| Major output | The output path and the resulting player | Right column of the visible group | White `#ffffff` cards. Titled Output & Result. Run is the suggested action and spans the width. Then the output line, the result line, Generated, and a titled Resulting Video player. The resulting video area is white |
| Path display | The folder this process is using | A frame under the header, above the tabs | Folder icon, the translated Project Root label, a colon, and the absolute current working directory. The directory is selectable and is not translated. This line has no clock |
| System-time display | The player clock and the thumbnail track | Left label, thumbnail track, and right label on each elapsed bar | `MM:SS.CC`. The jump placeholder is `00:00.00`. This window does not show `HH:MM:SS`. The output player’s total is the duration of the generated file and changes when that file is regenerated. The track is 56 px tall. Hover shows the time under the pointer and does not seek. The left label is the current time |
| Time-consuming process | The wait while an encode runs | The process bar and the visible result label | Fraction 0 and the untranslated sentence `please wait for time consuming process`. Close while busy keeps that sentence and does not close |

**Components list.** Navigation is the header and the join and edit tabs. Status is the title and the process bar when idle or finished. Major input is Input Video, Edit Controls, and Looping Options, or Video 1 and Video 2. Major output is Output & Result and Resulting Video. Path display is the project-root line. System-time display is each player clock. The time-consuming process message is the wait sentence on the bar and the result label while a run is busy.

**Style guide.** The table above is the style for each part. Cards are titled frames. The process bar is not a live FFmpeg ticker. The window and the content column are light gray `#d3d3d3`. Source cards and output cards are white `#ffffff`, including the video area and the controls on the card. The header bar and the process bar keep their theme colors. Buttons keep their theme colors, including Run as the suggested action. Each elapsed bar’s thumbnail track is 56 pixels tall, with the scrubber handle on the strip. The percent scale stays a plain scale.

**Storyboard.** Each row names a capture already on disk. The operator flow is Edit, then Join, then the language list, then self-management. Caption cells stay on `requirement-python-readme`.

| Order | Action that opens the capture | Capture |
|------:|--------------------------------|---------|
| 1 | Open the window in Traditional Chinese with Edit visible, one MP4 loaded, and Run not pressed | `screenshots/gui-edit.png` |
| 2 | Show Join with both sources loaded and Run not pressed | `screenshots/gui-join.png` |
| 3 | Open the language list | `screenshots/gui-language.png` |
| 4 | Open self-management | `screenshots/gui-self-management.png` |

The four captures are the current window: light gray canvas, white cards, thumbnail strips on loaded players, title VideoEditor 1.0.0, and a Traditional Chinese header.

## Terminologies

### Python GUI window

**Definition:** Python GUI window is a claimed picture window on a Python CLI. The window imports a host toolkit in this interpreter. The operator page reports that import. A failed import is the text `not available`. On Windows, a miss names the text-screen verb the specialized requirement already claims and states that the page does not install the toolkit. The page does not print `pacman`, `msys2`, `mingw-w64`, or `UCRT64`, and it does not run a package manager or an installer. The specialized requirement names the toolkit and the open rule. This term does not mint a GUI law mold and does not attach every CLI verb to the window.

**Human daily-life explanation:** A python-gui-window is the shop’s picture counter. The card on the wall says whether today’s tools are in this drawer. When the drawer is empty, the card points you back to the written counter you already know. The card does not send you to a second shop to run a foreign package command.

**Daily-life example:** You ask what the picture counter needs. The card says the tools are missing and tells you to use the written counter. It does not hand you a command for a different shop’s package shelf.

### Timeline thumbnail preview

**Definition:** A timeline thumbnail preview is the filmstrip scrubber on one video’s duration. It is a thumbnail track of scaled frames that spans that duration, with a scrubber handle on top of the strip. A pointer UI interaction on the strip shows a timestamp, jumps playback, or drags the handle so the main picture follows. Frames are extracted on a background worker so the window thread does not freeze when a file is opened. The finished strip is cached in the system temporary directory and reused when the same file, size, and modification time are opened again. A long file is sampled on a regular interval of 2 to 5 seconds. The strip does not extract every frame. This term does not mint a GUI law mold. The specialized requirement names the toolkit, the height, and which bars carry the strip.

**Human daily-life explanation:** A timeline thumbnail preview is a row of tiny photos along the edge of a film reel. You can see the story without playing the whole reel. Pointing at a photo names the moment. Pressing it jumps the projector. Sliding the marker moves the projector as you go. The photos are printed in the back room, saved in a scrap drawer, and reprinted only when the reel itself has changed. A long reel is photographed every few seconds, not on every sprocket hole.

**Daily-life example:** You drop a reel on the counter. A strip of small frames appears under the picture. You point near the middle and the card says 01:23.45. You press, and the picture jumps there. You drag the marker and the picture keeps up. Opening the same reel again uses the strip already in the scrap drawer.

### Scrubber handle

**Definition:** A scrubber handle is the playhead drawn on a thumbnail track. It marks the current time. Dragging it moves playback and updates the main picture while the pointer moves. A click elsewhere on the strip moves this handle to that time. The handle is not the strip of frames, and it is not a hover tip.

**Human daily-life explanation:** A scrubber handle is the clip you slide along a ruler. The clip sits on the row of tiny photos and shows where the reel is. Sliding the clip moves the picture. Pressing another spot on the ruler picks the clip up and sets it down there.

**Daily-life example:** The reel is at the start. You drag the clip toward the right and the picture changes as the clip moves. You then press a photo further along, and the clip jumps to that photo.

### Thumbnail track

**Definition:** A thumbnail track is the continuous strip of scaled video frames that replaces or covers the plain slider trough for one duration. The strip runs from the start of that video to the end. It has a fixed thumbnail track height. It is not the scrubber handle, and it is not the main picture.

**Human daily-life explanation:** A thumbnail track is the row of small photos that stands in for a blank ruler. Each photo is a moment from the reel, in order, from the first moment to the last. The row is short. The big picture stays above it.

**Daily-life example:** Instead of a gray line under the picture, you see a ribbon of frames. The left end is the opening shot. The right end is the last shot. The ribbon does not grow into a second full picture.

### Thumbnail track height

**Definition:** Thumbnail track height is the fixed pixel height of a thumbnail track. A compact editing timeline uses a short band, commonly 48 to 64 pixels, so the strip stays detailed without becoming a second picture. The height does not follow the video’s own pixel height. It is not the thumbnail track height proportion.

**Human daily-life explanation:** Thumbnail track height is how tall the row of tiny photos is, in a fixed size. The row stays short, about the height of a fingertip on a ruler, whether the reel is a postcard or a poster. It does not grow when the picture is tall.

**Daily-life example:** The ribbon under the picture is always the same short height. A wide landscape and a tall portrait both get that same short ribbon. The ribbon is not a second poster.

### Thumbnail track height proportion

**Definition:** Thumbnail track height proportion is the thumbnail track height divided by the video picture height on the same screen. The ratio stays well below 1 so the strip is a ruler under the picture and not a second full preview. It is not the pixel height itself.

**Human daily-life explanation:** Thumbnail track height proportion is how the short photo ribbon compares with the big picture above it. You divide the ribbon’s height by the picture’s height. A small result means the ribbon is a strip, not another poster. People also call that comparison the thumbnail trail height proportion.

**Daily-life example:** The picture on the card is tall. The ribbon under it is a fraction of that height. You can still read the frames, and the ribbon does not compete with the picture.

### UI hover state

**Definition:** A UI hover state is the pointer resting on a control without a press. The control may show extra information. It does not activate. On a timeline thumbnail preview, the extra information is the timestamp under the pointer, in the same clock the bar already uses. Hover does not seek and does not move the scrubber handle.

**Human daily-life explanation:** A UI hover state is your finger hovering over a photo on the ribbon without pressing. A small card names the moment under your finger. The projector does not jump, and the clip on the ruler stays where it was.

**Daily-life example:** You rest a finger over the middle of the ribbon. A card says 01:23.45. The picture on the screen stays on the frame it was already showing. You lift your finger and the card goes away.

### UI click to seek

**Definition:** UI click to seek is a press on a duration strip that jumps playback to the time under the pointer and moves the scrubber handle to that time. The main picture shows that moment. A hover is not this press. A drag is the handle moving while the button stays down, and the picture follows during that move.

**Human daily-life explanation:** UI click to seek is pressing one photo on the ribbon so the projector jumps to that moment. The clip on the ruler moves there too. Resting a finger on the photo only names the moment. Holding and sliding is a different move, and the picture follows the slide.

**Daily-life example:** The reel is at the start. You press a photo near the end. The picture jumps to that photo and the clip sits on it. Earlier, resting on that photo only showed the time.

### UI interaction

**Definition:** A UI interaction is a pointer act on a control: rest, press, or drag. On a timeline thumbnail preview, the rest is a UI hover state and does not seek. The press is UI click to seek. The drag moves the scrubber handle and updates the main picture while the pointer moves. This term is the family. It is not one of those acts alone, and it is not the window’s toolkit check.

**Human daily-life explanation:** A UI interaction is what your hand does to a control: hover, tap, or slide. On the photo ribbon, a hover names the moment, a tap jumps the projector, and a slide keeps the projector with your finger. The three are one family, and they are not the same move.

**Daily-life example:** You hover and read 01:23.45 while the picture stays put. You tap and the picture jumps. You then hold and slide, and the picture follows the clip until you let go.

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-10-10 | Active 1.0.0 | X11 window with edit and join groups. `tui` keeps the text menu |
| 2026-10-10 | Active 1.1.0 | Join has three players. Edit has a generated-file player. Elapsed bar, Play, Stop |
| 2026-10-10 | Active 1.2.0 | Edit and Join each split left and right. Sources stay on the left. Output stays on the right |
| 2026-10-10 | Active 1.3.0 | Window controls follow the menu language. The clock, the folder path, and About stay as they are |
| 2026-10-10 | Active 1.4.0 | The window’s top menu shows the names and omits the row numbers |
| 2026-10-10 | Active 1.5.0 | Run clears and disables the generated player first, then refreshes and enables it when the output file is on disk |
| 2026-10-11 | Active 1.6.0 | Project-root line, Input Video, Edit Controls, Looping Options, Output & Result, Resulting Video, and a process bar. Looping is three exclusive switches and starts on None. English Go is Go To. The four captures on disk are the storyboard |
| 2026-10-11 | Active 1.6.1 | The window and the content column are light gray `#d3d3d3`. The four captures still show the earlier canvas |
| 2026-10-11 | Active 1.6.2 | Source cards and output cards are white `#ffffff`, including the video area and the controls on the card. The four captures still show the earlier canvas |
| 2026-10-11 | Active 1.6.3 | The output player’s total is replaced with the duration of each regenerated file |
| 2026-10-12 | Active 1.6.4 | Each elapsed bar is a timeline thumbnail preview. The four captures still show the earlier canvas |
| 2026-10-12 | Active 1.6.5 | Distribution name is VideoEditor. Console script is `video-editor`. Current release string is **1.0.0**. |
