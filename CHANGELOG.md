# CHANGELOG

All notable changes to **VideoEditor** are documented here.
Version SSOT: `pyproject.toml` `[project].version` and `src/VideoEditor/__init__.py` `__version__`.

## [1.0.0] - 2026-10-12

### Added

- Each elapsed bar on the X11 window is a timeline of thumbnail frames. Hover, click, and drag seek within that clip. The output player's total time updates when a regenerated file is loaded.

### Changed

- The distribution name is VideoEditor. The console script is `video-editor`. The module is `python -m VideoEditor`. Aliases `video-join` and `video-speed` stay. The language leaf is `~/.local/VideoEditor/language`. `VIDEOEDITOR_LANG` overrides that leaf for one process and does not write it.
- Product version is **1.0.0**. `pyproject.toml`, `__version__`, the README Version badge, this section, and the current SECURITY row use that string.
- Public home is `https://github.com/cloudgen/VideoEditor` (`git@github.com:cloudgen/VideoEditor.git`).
- The four pictures in `screenshots/` are captures of this window. The title is VideoEditor 1.0.0. The header on those captures is Traditional Chinese. Run has not been pressed, so the process bar reads 處理 0%.

## [2.0.0] - 2026-10-11

### Added

- The X11 window shows a project-root line under the header. The label follows the menu language. The directory is the current working directory and is not translated.
- Edit groups the source as Input Video, the transport and cut as Edit Controls, and the tail as Looping Options. Join keeps Video 1 above Video 2. Both groups put Output & Result and Resulting Video on the right.
- Looping Options uses one switch each for None, Boomerang, and Repeat. Exactly one is on. The window starts on None. Turning the last switch off returns to None. `--repeat` and `--boomerang` together still fail closed.
- A process bar sits on the bottom of the window. Idle and a finish without a file read Process 0%. While a run is busy the bar shows `please wait for time consuming process`. A finish with the output file on disk reads Process 100%.
- English Go on the window is Go To. The other twelve languages keep their existing go-to words.

### Changed

- Product version is **2.0.0**. `pyproject.toml`, `__version__`, the README Version badge, this section, and the current SECURITY row use that string.
- The four pictures in `screenshots/` are captures of this window. The header on those captures is Traditional Chinese. Run has not been pressed, so the process bar reads 處理 0%.

## [1.1.0] - 2026-10-10

### Added

- `video-editor setup` installs `ChronicleLogger>=1.3.1` and `opencv-python-headless>=5.0.0.93` for this Python. On Windows it also tries the curses module and FFmpeg. It does not install GTK 4 or GStreamer, and it does not use administrator privilege.
- Before ChronicleLogger starts, a Python that has no `os.geteuid` receives a stand-in that returns `1`. `help`, `about`, `version`, and `hello` can start on that interpreter. The ChronicleLogger library itself is unchanged.
- A Python that cannot import `curses` still loads the package. `about`, `version`, `help`, and `hello` still run. Opening the text menu says this Python does not provide the curses module and does not print a traceback.
- `about` names GTK 4 and GStreamer and reports whether this Python can import them. On Windows, a missing library names `video-editor tui`. The page does not install packages and does not print a package-manager command.
- Run clears and disables the generated player before the encode starts. When the run finishes and the output file is on disk, that player loads the file and its controls are enabled.
- Window labels follow the menu language: buttons, Start, Stop, Percent, Tail, None, Boomerang, Repeat, Output, Generated, and the other controls on the window. The clock, the folder path, and the About page stay in their current form. The wait sentence stays `please wait for time consuming process`.
- The window’s top menu shows join, edit, system-log, language, self-management, and Exit.
- Menu rows 1 join and 2 edit sit on the video group. They share that group’s left edge and width. The row for the group on screen is highlighted, and the highlight meets the top of the group.
- Edit tail is none, boomerang, or repeat. The window offers those three choices and starts on none. The text menu asks the same question. `--repeat` appends the forward clip so it plays twice. `--boomerang` still appends the reverse. The two flags together fail closed. A repeat output name ends in `_REPEAT`.
- X11 window for a bare `video-editor` when `DISPLAY` is set. Edit and Join are two groups. Each group puts the source or sources on the left and the output on the right. Edit has an MP4 player, an `MM:SS.CC` time bar, and Start, Pause, Stop, jump, Mark start, and Mark end. Join stacks Video 1 above Video 2 and has two file buttons.
- Join shows three players: both source files and the generated file. Edit shows a player for the generated file. Each of those players has an `MM:SS.CC` elapsed time bar and Play and Stop. Play and Stop do not start or stop an encode.
- Verb `tui` opens the existing text menu, including when `DISPLAY` is set.
- Product law records the Windows host contract. The text menu and the typed verbs are the Windows door. The picture window stays the X11 window. `setup`, `about`, and the logger bind stay on their existing owners.

### Changed

- Public home is `https://github.com/cloudgen/VideoEditor` (`git@github.com:cloudgen/VideoEditor.git`). The user document pictures are the X11 window: edit, join, language, and self-management.

## [1.0.5] - 2026-10-04

### Changed

- `about` shows one page: product identity, a host check of this computer, and a star box. The page stays English. It does not probe `ffmpeg` and it does not print a pip install line.
- Self-management row 83 reads "version, FFmpeg, and this computer."
- Version is **1.0.5**. `ChronicleLogger>=1.3.1` is unchanged.
- Product README Screenshots links every picture in `screenshots/` with an absolute `https` URL. Menu pictures captured before the about page still show **1.0.4**.

## [1.0.4] - 2026-10-04

### Added

- Text menu on a terminal when `video-join` is started with no arguments. Front rows are join (1), system-log (3), language (4), self-management (8), and Exit (9). system-log lists view-log (31), clear-log (32), log-folder (33), and Back (0). language lists English through Ελληνικά (41–53) and Back (0). self-management lists version (82), about (83), version-check (84), self-update (85), self-uninstall (86), self-install (87), and Back (0).
- Menu language file `~/.local/VideoJoin/language`. `VIDEOJOIN_LANG` overrides that file for one process and does not write it. `language` is not a command-line verb.
- Typed verbs `help`, `version`, `about`, `hello`, `join`, `list-videos`, `self-install`, `version-check`, `self-update`, and `self-uninstall`.
- `ChronicleLogger` is constructed in `main` and required at `ChronicleLogger>=1.3.1`.
- Product README shows the main menu, the system-log board, the language board, and the self-management board.
- Product README PyPI version badge (`pypi.org/project/VideoJoin`).

### Changed

- Empty argv on a terminal opens that menu and does not start the join questions. With no terminal, empty argv prints help and returns 0.
- Quick Installation documents **`pip install VideoJoin`**. This tree is **1.0.4**. A registry probe on 2026-08-19 reported **1.0.3**. Checkout `pip install -e .` stays the local path.
- Join still prefers stream copy, then re-encode, and still publishes with `shutil.move`.

---

## [1.0.3] - 2026-08-09

### Added

- Same-FS staging helpers (`staging_dir_for`, `make_temp_path`) and **`promote_file` → `shutil.move`** for publishing intermediates.
- Unique temp concat list and media intermediates (no fixed cwd-only `filelist.txt` strategy).
- Product requirements set (class, domain, pipeline, CLI, coding-style, packaging, structure, errors, runtime).
- Promote gate checklist **`CL-PYTHON-SHUTIL-MOVE-PUBLISH`** (blank + filled run).

### Changed

- Join pipeline: stream-copy to temp → promote; on failure re-encode to temp → promote.
- Package public surface: `__version__` and `main` only (no phantom `ChronicleLogger` re-export from `.cli`).
- Product README rewritten for install/usage honesty (local package primary; FFmpeg system dep).

### Fixed

- Fail-closed re-encode path: non-zero FFmpeg or missing intermediate no longer prints success.
- Reject final output path equal to either source path.

### Security

- Still user-level only; no Type 1 elevation. FFmpeg invoked with argument lists (no shell string interpolation of free-form filters).

---

## [1.0.2] - prior

### Added

- Interactive two-file join with FFmpeg stream-copy and re-encode fallback.
- Package layout under `src/VideoJoin/` with console script `video-join`.

### Notes

- Earlier packaging claims may have listed broad Python support and optional Cython tooling; runtime join does not require Cython.

---

Update this file when shipping version bumps; keep body complete (no hollow TBD sections for claimed releases).
