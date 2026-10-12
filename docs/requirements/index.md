# Requirements index

**Product:** VideoEditor (Python CLI — text menu, X11 window when `DISPLAY` is set, join two local videos, and cut, speed, or boomerang an MP4)
**Workspace state:** Specialized product law (left genesis); **software-development** class; **pip/local package** install (not shell online Type O). Bootstrapped from VideoJoin. Edit steps added from VideoSpeed. Neither sibling tree is this product.
**Product version:** **1.0.0** (align `pyproject.toml`, `__init__.__version__`, root `README.md` Version badge)
**Updated:** 2026-10-12

| ID / key | Title | Area | Status | Path | Updated |
|----------|-------|------|--------|------|---------|
| requirement-class-software-dev | Software-development class law + residual stack (Python, setuptools). Git surface `cloudgen/VideoEditor`. OS family points at `requirement-python-windows` | class | Active | `requirement-class-software-dev.md` | 2026-10-12 |
| requirement-domain-videoeditor | Domain surface SSOT (join J-01..J-06 and edit E-01..E-08; help; about) | domain | Active | `requirement-domain-videoeditor.md` | 2026-10-12 |
| requirement-domain-videojoin | Former join-only domain file | domain | Superseded | `requirement-domain-videojoin.md` | 2026-10-12 |
| requirement-python-about | About page: identity, window libraries, host check, star box. Homepage `cloudgen/VideoEditor`. Sample package **1.0.0**. About date `2026-10-12` | python | Active | `requirement-python-about.md` | 2026-10-12 |
| requirement-video-ffmpeg-pipeline | FFmpeg ops SSOT (join stream-copy → re-encode; edit cut → speed → one tail of none, boomerang, or repeat; unique temps; shutil.move publish) | video | Active | `requirement-video-ffmpeg-pipeline.md` | 2026-10-12 |
| requirement-python-cli-interface | CLI entry, combined verbs including `setup`, edit flags, `--json`, empty-argv menu on a terminal and help off a terminal. Product version **1.0.0** | python | Active | `requirement-python-cli-interface.md` | 2026-10-12 |
| requirement-python-cli-logging | ChronicleLogger construct in `def main`. `HostSetup.ensure_geteuid()` runs before that import. Current version string **1.0.0** | python | Active | `requirement-python-cli-logging.md` | 2026-10-12 |
| requirement-python-tui | Text menu: join, edit, system-log, language, self-management, Exit. Path word is selected by the language requirement. Default is `Path`. Menu columns are display columns. Verb `tui` opens this menu. `import curses` uses `try` so a missing `_curses` does not stop about | python | Active | `requirement-python-tui.md` | 2026-10-12 |
| requirement-python-gui | X11 window: project root, Input Video, Edit Controls, Looping Options, Output & Result, process bar. Canvas `#d3d3d3`. Source and output cards `#ffffff`. The output total updates when a file is regenerated. Each elapsed bar is a 56 px thumbnail track with hover, click, and drag. Edit source player, edit generated player, three join players. Bare start when `DISPLAY` is set. `tui` keeps the text menu | python | Active | `requirement-python-gui.md` | 2026-10-12 |
| requirement-python-cli-language | Menu language: front row 4, codes 41–53, leaf `~/.local/VideoEditor/language`. Window controls use the same codes, including Project Root and Process. `language` is not an argv verb | python | Active | `requirement-python-cli-language.md` | 2026-10-12 |
| requirement-python-oop | Class map, including `HostSetup` for verb `setup` | python | Active | `requirement-python-oop.md` | 2026-10-12 |
| requirement-python-coding-style | Python style; temps; **shutil.move** publish; end state is the class map | python | Active | `requirement-python-coding-style.md` | 2026-10-12 |
| requirement-python-packaging | `pyproject.toml` / version 1.0.0 / console scripts; ChronicleLogger and OpenCV floors. Homepage `cloudgen/VideoEditor`. `_curses` and `windows-curses` stay out of the manifest | python | Active | `requirement-python-packaging.md` | 2026-10-12 |
| requirement-python-project-structure | Repository and `src/VideoEditor` layout. Live `__version__` cell **1.0.0** | python | Active | `requirement-python-project-structure.md` | 2026-10-12 |
| requirement-python-readme | Root user document: sections, badges, four X11 window captures, related projects. Home `cloudgen/VideoEditor`. Package **1.0.0** | python | Active | `requirement-python-readme.md` | 2026-10-12 |
| requirement-python-error-handling | Fail-closed errors; source-safe cleanup; console sentences stay | python | Active | `requirement-python-error-handling.md` | 2026-10-12 |
| requirement-runtime-prerequisites | Host FFmpeg + required ChronicleLogger; verb `setup` installs the declared pip floors. On Windows it tries curses and FFmpeg. No root auto-install. Text menu `_curses` import uses `try`. Product version **1.0.0** | runtime | Active | `requirement-runtime-prerequisites.md` | 2026-10-12 |
| requirement-python-windows | Windows host contract: text menu and typed verbs; picture window stays the X11 window; missing window libraries name `video-editor tui`; `windows-curses` stays out of the manifest | python | Active | `requirement-python-windows.md` | 2026-10-12 |

## Intentionally absent (by design)

| Surface | Status on VideoEditor |
|---------|----------------------|
| Shell online install / `SCRIPT_URL` / Type O empty-argv install-ensure / `curl\|sh` | **Absent** |
| Shell local `install` / `uninstall` / shell self-update | **Absent** (pip package) |
| Type 1 sudoers / root elevation allowlist | **Absent** |
| Automatic companion `.sha256` channel integrity law | **Absent** |
| OpenCV duration probe | **Present**. Pip dependency `opencv-python-headless>=5.0.0.93` on `requirement-python-packaging` and `requirement-runtime-prerequisites`. No separate dependency-management file |
| Second Active `requirement-domain-*` | **Forbidden** while `requirement-domain-videoeditor` is Active |
| Front row 2, cut / speed / boomerang or repeat, `list-mp4` | **Present**. Row **2** is `edit`. The tail is none, boomerang, or repeat. `list-mp4` is typed, not a front row. Join stays row **1** and current-folder only |
| `requirement-python-dependency-management` | **Absent** as its own file. ChronicleLogger floor and the OpenCV pin live on packaging + runtime |
| `requirement-python-version` | **Absent**. Version SSOT is the `__version__` string `1.0.0` |
| `requirement-python-json-output` | **Absent** as its own file. `--json` is owned by `requirement-python-cli-interface` |
| `requirement-python-graceful-exit` | **Absent**. Control-C is not confirmed law. Row 9 Exit returns 0 with no confirm. No SIGINT handler is claimed |
| `requirement-python-interactive-vs-noninteractive` | **Absent** as its own file. Terminal versus script routing is `requirement-python-cli-interface` |
| `requirement-python-pyenv`, `requirement-python-conda`, `requirement-python-oop-architecture` | **Absent**. Host-check path reads for pyenv and conda stay on `requirement-python-about`. Class homes are `requirement-python-oop`. `build.sh` is maintainer tooling on `requirement-python-project-structure` |
| Actor-role requirement file | **Absent**. Class residual is no dest approver |
| Native Windows picture window | **Absent**. Windows host contract is `requirement-python-windows`. The picture window stays the X11 window in `requirement-python-gui` |

**Install mode:** **pip / local package**. Primary console script `video-editor`. Aliases `video-join` and `video-speed` call `VideoEditor.cli:main`. Not a shell installer.

**Pip lifecycle:** claimed. Rows 84–87 and the typed verbs `version-check`, `self-update`, `self-install`, and `self-uninstall` are `requirement-python-cli-interface` and `requirement-python-tui`. They use `python -m pip`. They are not a shell channel. Empty argv does not run them. Verb `setup` is `requirement-python-cli-interface` and `requirement-runtime-prerequisites`. It installs the declared pip floors. On Windows it tries curses and FFmpeg. It does not install GTK 4 or GStreamer.

**Logger:** required (`ChronicleLogger>=1.3.1` in law and in `pyproject.toml`). `def main` in `src/VideoEditor/cli.py` writes `ChronicleLogger(...)`.

**Rules for agents:**

1. Treat Active rows above as the **live product-law inventory** for VideoEditor. The Superseded domain row is history.
2. **Do not invent** additional `requirement-*.md` paths — verify on disk and add a registry row in the same change when creating one.
3. Product source comments cite **only** these live requirement files.
4. This versioned surface lists **requirement rows only**.
5. Keep Status and Path in sync with each file’s header when status changes.
6. **Class gate:** software-development requires exactly one Active `requirement-class-software-dev.md` (this registry includes it).
7. **Domain SSOT:** exactly one Active domain file (`requirement-domain-videoeditor`).
8. **Do not introduce** a shell installer or Type 1 elevation without an explicit user order and a registry update.
9. **Do not** treat pip rows 84–87 as a reason to add a shell installer. **Do not** mark those pip rows absent.

When adding a requirement: append a row, create the file under `docs/requirements/`, keep Status in sync with the file header.
