**file**: docs/requirements/requirement-python-gui.md
**Status**: Active (Version 1.6.0)
**Area**: python
**Key**: `requirement-python-gui`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-protect)

## 1. Purpose

This file is the X11 window for VideoTools. A bare start on an interactive terminal opens this window when `DISPLAY` is set. The verb `tui` opens the text menu in `requirement-python-tui` and does not change that menu. Typed verbs stay on `requirement-python-cli-interface`.

The window has two groups. One is visible and the other is hidden. Edit is the first group. Join is the second group. A project-root line sits under the header. join and edit are tabs on the left of the group. Each group splits left and right. Edit puts Input Video, Edit Controls, and Looping Options on the left, and Output & Result on the right. Join puts the two sources on the left and the same output column on the right. A process bar sits on the bottom of the window.

### 1.1 Human-facing

**In one sentence:** On a terminal with an X11 display, `video-tools` opens a window with a project-root line, an edit source player, a resulting-video player, three join players, and a process bar, and `video-tools tui` opens the text menu.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | Person at a local X session or an `ssh -X` session | `video-tools` |
| The other role | Class `Gui` | `src/VideoTools/gui.py` |
| Not this file | The curses frame, the FFmpeg graph, and the typed `join` questions | TUI, pipeline, and CLI requirements |

| Includes | Excludes |
|----------|----------|
| Edit group and Join group, one visible at a time. Project-root line. Process bar | A second text-menu painter inside the window |
| Input Video, Edit Controls, Looping Options, Output & Result, Resulting Video | A timeline multi-track editor |
| MP4 player, `MM:SS.CC` elapsed time, Start, Pause, Stop, jump, Go To, Mark start, Mark end | Both Boomerang and Repeat on at once |
| Join players for both sources and the generated file. Edit player for the generated file. Each has the elapsed time bar and Play and Stop | A second encode control on those buttons |
| Two join file buttons that browse the host where the process runs | File-operand flags on the `join` verb |

## 2. Core Rules (Mandatory)

1. Class `Gui` in `src/VideoTools/gui.py` owns this window. `Cli` constructs it and calls `open`. `cli.py` does not build widgets.
2. A bare start opens this window when stdin and stdout are terminals and `DISPLAY` is non-empty. That covers a local X session, XWayland when `DISPLAY` is set, and `ssh -X`. The GDK backend is X11. `WAYLAND_DISPLAY` alone does not open the window.
3. When that X server refuses the connection, or GTK 4 cannot be imported, the process exits non-zero and the next step is `video-tools tui`. It does not draw a partial window and it does not hang.
4. A bare start with `DISPLAY` unset opens the text menu. A bare start with no terminal prints help and returns 0. `video-tools tui` on a terminal opens the text menu even when `DISPLAY` is set. `tui` with no terminal exits non-zero. `tui` is not a numbered row.
5. `join`, `edit`, `list-videos`, `list-mp4`, `help`, `about`, `hello`, `version`, the pip verbs, `--json`, and a complete edit job stay on their current paths and do not open this window.
6. The menu in the window shows join, edit, system-log, language, self-management, and Exit. Those labels have no row number. The text menu keeps **1**, **2**, **3**, **4**, **8**, and **9**. Self-management opens **82**–**87**. Row **81** stays omitted. `help` and `tui` stay off this menu. A framed project-root line sits under the header. It shows a folder icon, the translated label Project Root, and the absolute current working directory. The directory is selectable and is not translated. join and edit sit in a strip directly above the stack. That strip shares the stack’s left edge and width. The label for the visible video group is highlighted, and that highlight meets the top edge of the group. system-log, language, and self-management hide both video groups and clear that highlight. Leaving a group pauses the players on that group. A process bar sits on the bottom of the window.
7. The Edit left side is an Input Video card, then Edit Controls and Looping Options side by side. Input Video has the format token `MP4:`, one **Select file** button, the player, and the time bar. Edit Controls has Start, Pause, Stop, a jump field whose placeholder is `00:00.00`, Go To, the cut Start and End, Mark start, Mark end, and Percent. Elapsed time sits on the left of the bar as `MM:SS.CC` (minutes at least two digits and free to grow, seconds `00`–`59`, centiseconds). Percent is a scale and a spin from 20–200 and defaults to 100. The two stay equal. Looping Options is three switches: Boomerang, Repeat, and None. Exactly one is on. The window starts on None. Turning one on clears the others. Turning the last one off returns to None. Boomerang appends the reverse. Repeat appends the clip so it plays twice. The Edit right side is an Output & Result card: **Run**, the output path, the result line, Generated, and a Resulting Video card. That player has the elapsed time bar and Play and Stop. When Run starts, that player is cleared and Play, Stop, and the time bar are disabled. When Run finishes and the output file is on disk, the player loads that file and those controls are enabled. When Run finishes without that file, the player stays cleared and those controls stay disabled. Play and Stop do not start or kill FFmpeg.
8. Mark start and Mark end store the player position into the cut start and cut end. Run uses those values with the existing encoder. The output filename keeps the one-decimal pattern. The OpenCV duration is the bound. A reversed mark or an end past that duration does not start FFmpeg.
9. The Join left side has Video 1 above Video 2. Each is a titled card with a path and a **Select file** button. The chooser accepts `.mp4`, `.mov`, `.mkv`, `.avi`, and `.m4v`. The same path cannot be chosen twice. The chooser lists files on the computer that runs `video-tools`, including the remote host under `ssh -X`. Under each source path is a player with the elapsed time bar and Play and Stop. The Join right side is the same Output & Result column as Edit, plus the output name. The default name is `{stem1} + {stem2}.mp4`. The write line names the current working directory and that file. **Run** calls `Join.run`. The Resulting Video player is the third player, with the same bar and Play and Stop. When Run starts, that generated player is cleared and Play, Stop, and the time bar are disabled. The two source players stay loaded. When Run finishes and the output file is on disk, the generated player loads that file and those controls are enabled. When Run finishes without that file, the generated player stays cleared and those controls stay disabled. Join has three players. Play and Stop do not start or kill the concat.
10. A long encode runs off the GTK main loop. Before that work starts, the generated player for the running group is cleared and its controls are disabled. The process bar and the visible result show `please wait for time consuming process`. That sentence is not translated. The bar fraction is 0 while the sentence is showing. The bar is not a live FFmpeg ticker. When the work finishes and the output file is on disk, the player loads that file, its controls are enabled, and the bar reads Process 100% at fraction 1. When the work finishes without that file, the player stays cleared, those controls stay disabled, and the bar returns to Process 0% at fraction 0. Idle, including a capture taken before Run, is Process 0%. Stop on the player does not kill an encode that has already started. Close waits until that encode finishes and keeps the wait sentence on the bar. The thread create and start lines go through the one ChronicleLogger with `component` `Gui`.
11. The window may open when FFmpeg or the GStreamer playback plugins are missing. Playback controls stay disabled when the player cannot be created. Run still fails closed before FFmpeg is spawned. GTK 4 and GStreamer are host packages, not pip dependencies.
12. Language strings for the menu and for the window controls come from `MenuLanguage`. A language pick redraws the open window, including an icon button, without dropping the icon. The window translates button names and captions: Select file, Start, Pause, Stop, Play, Go To, Mark start, Mark end, the cut Start and End, Percent, Tail, None, Boomerang, Repeat, Run, Output, Output name, Generated, Video 1, Video 2, Project Root, Input Video, Edit Controls, Looping Options, Output & Result, Resulting Video, Process, View, Clear, Yes, and No, plus the short sentences the window itself writes. English Go To is the current English word. The other codes keep their existing go-to words. The elapsed clock, the directory on the project-root line, the product name, the version, the format token MP4, and the About page stay as they are. The widget paints `MP4:` from that token. The text-menu path word stays Path. Leaf command tokens stay the English tokens. The wait sentence stays `please wait for time consuming process`. Join command lines, pip output, and FFmpeg sentences stay English. Pip rows call `SelfManage` and do not use sudo. Self-uninstall asks before it runs. Log view and clear use `SystemLog` and its folder fence.
13. Actor / role / subject / approver: **considered**. No dest machine. No approver.

### 2.1 Implementation Notes (this project)

| Item | Value |
|------|--------|
| **Class** | `Gui` in `src/VideoTools/gui.py` |
| **Open** | `video-tools` on a terminal with `DISPLAY` set |
| **Text menu** | `video-tools tui` |
| **Groups** | Edit visible hides Join. Join visible hides Edit |
| **Project root** | Folder icon, translated Project Root, absolute current working directory |
| **Process bar** | Idle and a finish without a file: Process 0%. Busy: the untranslated wait sentence. A file on disk: Process 100% |
| **Looping** | Three switches. Exactly one on. Default None |
| **Player** | GTK 4 `MediaFile` / `Video`, GStreamer, X11 backend |
| **Elapsed** | `MM:SS.CC` on the left of the time bar |
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

## 5. Acceptance criteria

| ID | Criterion |
|----|-----------|
| AC-1 | Bare start with `DISPLAY` and a terminal opens this window and does not run pip |
| AC-2 | `video-tools tui` opens the existing text menu |
| AC-3 | Edit and Join are separate groups. Each puts the source or sources on the left and the output on the right |
| AC-4 | The elapsed label is `MM:SS.CC`, and Mark start / Mark end fill the cut bounds |
| AC-5 | Join offers two file buttons and refuses the same path twice |
| AC-6 | Join shows three players (video 1, video 2, generated), each with an elapsed time bar and Play and Stop |
| AC-7 | Edit shows a generated-file player with an elapsed time bar and Play and Stop |
| AC-8 | Run clears and disables that group’s generated player first. A finished file refreshes and enables it. A finish without that file leaves it cleared and disabled |
| AC-9 | The project-root line starts with the translated Project Root label and names the current working directory. The directory is not translated |
| AC-10 | Exactly one looping switch is on. The window starts on None. Turning the last switch off returns to None |
| AC-11 | Idle is Process 0% at fraction 0. A busy run shows `please wait for time consuming process`. A finished file on disk is Process 100% at fraction 1 |

## 6. Related requirements (peer keys only)

| Key | Relationship |
|-----|----------------|
| `requirement-python-cli-interface` | Bare start, the `tui` verb, and the other verbs |
| `requirement-python-tui` | Text menu opened by `tui` and by a bare start with no `DISPLAY` |
| `requirement-domain-videotools` | Join and edit steps |
| `requirement-python-oop` | Class `Gui` |
| `requirement-video-ffmpeg-pipeline` | Encode and publish |
| `requirement-python-cli-language` | Menu words and the language leaf |

### 6.1 Window screen

The window explains seven parts. Each part says what it is, where it sits, and the display style.

| Part | What it is | Where it sits | Display style |
|------|------------|---------------|---------------|
| Navigation | Header actions and the two group tabs | Header bar, start side, for system-log, language, self-management, and Exit. join and edit are tabs on the left edge of the group | Icon and words for the four header actions. Plain words for join and edit. The visible group’s tab is highlighted and meets the top of the group. system-log, language, and self-management clear that highlight |
| Status | The window title and the process bar when the window is idle or a run has finished | Title centered in the header. Process bar full width on the bottom | Title is the product name, a space, and the package version. Idle and a finish without a file: Process 0%, fraction 0. A finish with the file on disk: Process 100%, fraction 1. The percent words follow the language |
| Major input | The source and the edit settings | Left column of the visible group | Edit: Input Video, then Edit Controls beside Looping Options. Input Video holds `MP4:`, Select file, the source player, and the elapsed scale. Edit Controls holds Start, Pause, Stop, the jump field, Go To, the cut bounds, Mark start, Mark end, and the percent scale with its spin. Looping Options holds the three switches. Join: Video 1 above Video 2. Each card holds a path, Select file, and a player |
| Major output | The output path and the resulting player | Right column of the visible group | Titled Output & Result. Run is the suggested action and spans the width. Then the output line, the result line, Generated, and a titled Resulting Video player |
| Path display | The folder this process is using | A frame under the header, above the tabs | Folder icon, the translated Project Root label, a colon, and the absolute current working directory. The directory is selectable and is not translated. This line has no clock |
| System-time display | The player clock | Left and right of each elapsed scale | `MM:SS.CC`. The jump placeholder is `00:00.00`. This window does not show `HH:MM:SS` |
| Time-consuming process | The wait while an encode runs | The process bar and the visible result label | Fraction 0 and the untranslated sentence `please wait for time consuming process`. Close while busy keeps that sentence and does not close |

**Components list.** Navigation is the header and the join and edit tabs. Status is the title and the process bar when idle or finished. Major input is Input Video, Edit Controls, and Looping Options, or Video 1 and Video 2. Major output is Output & Result and Resulting Video. Path display is the project-root line. System-time display is each player clock. The time-consuming process message is the wait sentence on the bar and the result label while a run is busy.

**Style guide.** The table above is the style for each part. Cards are titled frames. The process bar is not a live FFmpeg ticker.

**Storyboard.** Each row names a capture already on disk. The operator flow is Edit, then Join, then the language list, then self-management. Caption cells stay on `requirement-python-readme`.

| Order | Action that opens the capture | Capture |
|------:|--------------------------------|---------|
| 1 | Open the window in Traditional Chinese with Edit visible, one MP4 loaded, and Run not pressed | `screenshots/gui-edit.png` |
| 2 | Show Join with both sources loaded and Run not pressed | `screenshots/gui-join.png` |
| 3 | Open the language list | `screenshots/gui-language.png` |
| 4 | Open self-management | `screenshots/gui-self-management.png` |

## Terminologies

### Python GUI window

**Definition:** Python GUI window is a claimed picture window on a Python CLI. The window imports a host toolkit in this interpreter. The operator page reports that import. A failed import is the text `not available`. On Windows, a miss names the text-screen verb the specialized requirement already claims and states that the page does not install the toolkit. The page does not print `pacman`, `msys2`, `mingw-w64`, or `UCRT64`, and it does not run a package manager or an installer. The specialized requirement names the toolkit and the open rule. This term does not mint a GUI law mold and does not attach every CLI verb to the window.

**Human daily-life explanation:** A python-gui-window is the shop’s picture counter. The card on the wall says whether today’s tools are in this drawer. When the drawer is empty, the card points you back to the written counter you already know. The card does not send you to a second shop to run a foreign package command.

**Daily-life example:** You ask what the picture counter needs. The card says the tools are missing and tells you to use the written counter. It does not hand you a command for a different shop’s package shelf.

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
