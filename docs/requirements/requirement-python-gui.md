**file**: docs/requirements/requirement-python-gui.md
**Status**: Active (Version 1.5.0)
**Area**: python
**Key**: `requirement-python-gui`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-protect)

## 1. Purpose

This file is the X11 window for VideoTools. A bare start on an interactive terminal opens this window when `DISPLAY` is set. The verb `tui` opens the text menu in `requirement-python-tui` and does not change that menu. Typed verbs stay on `requirement-python-cli-interface`.

The window has two groups. One is visible and the other is hidden. Edit is the first group. Join is the second group. Each group splits left and right. The left side is the source or sources and the settings. The right side is the output.

### 1.1 Human-facing

**In one sentence:** On a terminal with an X11 display, `video-tools` opens a window with an edit source player, a generated-file player, and three join players, and `video-tools tui` opens the text menu.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | Person at a local X session or an `ssh -X` session | `video-tools` |
| The other role | Class `Gui` | `src/VideoTools/gui.py` |
| Not this file | The curses frame, the FFmpeg graph, and the typed `join` questions | TUI, pipeline, and CLI requirements |

| Includes | Excludes |
|----------|----------|
| Edit group and Join group, one visible at a time | A second text-menu painter inside the window |
| MP4 player, `MM:SS.CC` elapsed time, Start, Pause, Stop, jump, Mark start, Mark end | A timeline multi-track editor |
| Join players for both sources and the generated file. Edit player for the generated file. Each has the elapsed time bar and Play and Stop | A second encode control on those buttons |
| Two join file buttons that browse the host where the process runs | File-operand flags on the `join` verb |

## 2. Core Rules (Mandatory)

1. Class `Gui` in `src/VideoTools/gui.py` owns this window. `Cli` constructs it and calls `open`. `cli.py` does not build widgets.
2. A bare start opens this window when stdin and stdout are terminals and `DISPLAY` is non-empty. That covers a local X session, XWayland when `DISPLAY` is set, and `ssh -X`. The GDK backend is X11. `WAYLAND_DISPLAY` alone does not open the window.
3. When that X server refuses the connection, or GTK 4 cannot be imported, the process exits non-zero and the next step is `video-tools tui`. It does not draw a partial window and it does not hang.
4. A bare start with `DISPLAY` unset opens the text menu. A bare start with no terminal prints help and returns 0. `video-tools tui` on a terminal opens the text menu even when `DISPLAY` is set. `tui` with no terminal exits non-zero. `tui` is not a numbered row.
5. `join`, `edit`, `list-videos`, `list-mp4`, `help`, `about`, `hello`, `version`, the pip verbs, `--json`, and a complete edit job stay on their current paths and do not open this window.
6. The menu in the window shows join, edit, system-log, language, self-management, and Exit. Those labels have no row number. The text menu keeps **1**, **2**, **3**, **4**, **8**, and **9**. Self-management opens **82**–**87**. Row **81** stays omitted. `help` and `tui` stay off this menu. join and edit sit in a strip directly above the stack. That strip shares the stack’s left edge and width. The label for the visible video group is highlighted, and that highlight meets the top edge of the group. system-log, language, and self-management hide both video groups and clear that highlight. Leaving a group pauses the players on that group.
7. The Edit left side has one MP4 **Select file** button, the player, the time bar, Start, Pause, Stop, a jump field, Mark start, and Mark end. Elapsed time sits on the left of the bar as `MM:SS.CC` (minutes at least two digits and free to grow, seconds `00`–`59`, centiseconds). Percent is 20–200 and defaults to 100. The tail is one choice of None, Boomerang, or Repeat, and it defaults to None. Boomerang appends the reverse. Repeat appends the clip so it plays twice. The Edit right side shows the output path and **Run**. It also has a player for the generated file, labeled Generated, with that elapsed time bar and Play and Stop. When Run starts, that player is cleared and Play, Stop, and the time bar are disabled. When Run finishes and the output file is on disk, the player loads that file and those controls are enabled. When Run finishes without that file, the player stays cleared and those controls stay disabled. Play and Stop do not start or kill FFmpeg.
8. Mark start and Mark end store the player position into the cut start and cut end. Run uses those values with the existing encoder. The output filename keeps the one-decimal pattern. The OpenCV duration is the bound. A reversed mark or an end past that duration does not start FFmpeg.
9. The Join left side has Video 1 above Video 2. Each has a path and a **Select file** button. The chooser accepts `.mp4`, `.mov`, `.mkv`, `.avi`, and `.m4v`. The same path cannot be chosen twice. The chooser lists files on the computer that runs `video-tools`, including the remote host under `ssh -X`. Under each source path is a player with the elapsed time bar and Play and Stop. The Join right side shows the output name, default `{stem1} + {stem2}.mp4`, the full path in the current working directory, and **Run**. Run calls `Join.run`. The right side also has a third player, labeled Generated, with the same bar and Play and Stop. When Run starts, that generated player is cleared and Play, Stop, and the time bar are disabled. The two source players stay loaded. When Run finishes and the output file is on disk, the generated player loads that file and those controls are enabled. When Run finishes without that file, the generated player stays cleared and those controls stay disabled. Join has three players. Play and Stop do not start or kill the concat.
10. A long encode runs off the GTK main loop. Before that work starts, the generated player for the running group is cleared and its controls are disabled. The visible result shows `please wait for time consuming process`. When the work finishes, that player loads the output file when the file is on disk and then enables its controls. Stop on the player does not kill an encode that has already started. Close waits until that encode finishes. The thread create and start lines go through the one ChronicleLogger with `component` `Gui`.
11. The window may open when FFmpeg or the GStreamer playback plugins are missing. Playback controls stay disabled when the player cannot be created. Run still fails closed before FFmpeg is spawned. GTK 4 and GStreamer are host packages, not pip dependencies.
12. Language strings for the menu and for the window controls come from `MenuLanguage`. A language pick redraws the open window. The window translates button names and captions: Select file, Start, Pause, Stop, Play, Go, Mark start, Mark end, the cut Start and End, Percent, Tail, None, Boomerang, Repeat, Run, Output, Output name, Generated, Video 1, Video 2, View, Clear, Yes, and No, plus the short sentences the window itself writes. The elapsed clock, the folder path, the product name, the version, the format token MP4, and the About page stay as they are. Leaf command tokens stay the English tokens. The wait sentence stays `please wait for time consuming process`. Join command lines, pip output, and FFmpeg sentences stay English. Pip rows call `SelfManage` and do not use sudo. Self-uninstall asks before it runs. Log view and clear use `SystemLog` and its folder fence.
13. Actor / role / subject / approver: **considered**. No dest machine. No approver.

### 2.1 Implementation Notes (this project)

| Item | Value |
|------|--------|
| **Class** | `Gui` in `src/VideoTools/gui.py` |
| **Open** | `video-tools` on a terminal with `DISPLAY` set |
| **Text menu** | `video-tools tui` |
| **Groups** | Edit visible hides Join. Join visible hides Edit |
| **Player** | GTK 4 `MediaFile` / `Video`, GStreamer, X11 backend |
| **Elapsed** | `MM:SS.CC` on the left of the time bar |
| **Join players** | Three: video 1, video 2, generated. Elapsed bar, Play, Stop |
| **Edit generated** | One player on the right side. Elapsed bar, Play, Stop |
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
- Translate the elapsed clock, the folder path, the About page, or the wait sentence `please wait for time consuming process`.

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

## 6. Related requirements (peer keys only)

| Key | Relationship |
|-----|----------------|
| `requirement-python-cli-interface` | Bare start, the `tui` verb, and the other verbs |
| `requirement-python-tui` | Text menu opened by `tui` and by a bare start with no `DISPLAY` |
| `requirement-domain-videotools` | Join and edit steps |
| `requirement-python-oop` | Class `Gui` |
| `requirement-video-ffmpeg-pipeline` | Encode and publish |
| `requirement-python-cli-language` | Menu words and the language leaf |

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-10-10 | Active 1.0.0 | X11 window with edit and join groups. `tui` keeps the text menu |
| 2026-10-10 | Active 1.1.0 | Join has three players. Edit has a generated-file player. Elapsed bar, Play, Stop |
| 2026-10-10 | Active 1.2.0 | Edit and Join each split left and right. Sources stay on the left. Output stays on the right |
| 2026-10-10 | Active 1.3.0 | Window controls follow the menu language. The clock, the folder path, and About stay as they are |
| 2026-10-10 | Active 1.4.0 | The window’s top menu shows the names and omits the row numbers |
| 2026-10-10 | Active 1.5.0 | Run clears and disables the generated player first, then refreshes and enables it when the output file is on disk |
