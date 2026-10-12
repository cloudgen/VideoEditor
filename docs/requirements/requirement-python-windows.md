**file**: docs/requirements/requirement-python-windows.md
**Status**: Active (Version 1.0.2)
**Area**: python
**Key**: `requirement-python-windows`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

This file is the Windows host contract for a Python program that also runs on Linux. It decides how that host is recognized, which front door is supported there, and which changes are forbidden. The environment-verb steps, the about-page sentences, the picture-window open rule, the status-logger bind, and the pip manifest stay on their owners. This file points at those owners. It does not restate their procedures.

### 1.1 Human-facing

**In one sentence:** On Windows you run `video-editor` from Command Prompt or Git Bash as yourself; the text menu and the typed verbs are the supported door, and the picture window stays the existing X11 window.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | The person at Windows Command Prompt, PowerShell, or Git Bash | `video-editor help` |
| The other role | The interpreter on that host | `python -m VideoEditor` |
| Not this file | The encode steps, the menu picture, and the about-page wording | Peer requirements in section 6 |

| Includes | Excludes |
|----------|----------|
| How a Windows host is recognized | A second copy of the `setup` command list |
| The text menu and typed verbs as the supported door when no X11 display is set | A native Windows picture window |
| The rule that a missing window library leaves the X11 window file in place | An installer, a package-manager command, or a downloaded script on the about page |
| Normal-user privilege on Git Bash and Windows cmd | Administrator privilege, a dedicated system account, or Termux `pkg` on those shells |

| Surface | What you open | What for |
|---------|---------------|----------|
| `video-editor` | Console script on a terminal | Text menu when `DISPLAY` is unset |
| `video-editor tui` | Same script | Text menu, including when a display is set |
| `video-editor setup` | Same script | Prepare this Python. Steps stay on `requirement-runtime-prerequisites` |
| `video-editor about` | Same script | Window-library check. Sentences stay on `requirement-python-about` |
| `src/VideoEditor/gui.py` | Picture window | Opens only when `DISPLAY` is set and the host libraries import |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Start on Windows with no X11 display | You get the text menu on a terminal, or help when there is no terminal. The picture-window file is still in the package. | `video-editor` |
| Ask what this Python can import | The about page names GTK 4 and GStreamer and does not install them. A miss on Windows tells you to open the text menu. | `video-editor about` |
| Prepare libraries | `setup` installs the declared pip libraries as you. On Windows it may also try the curses module and FFmpeg. It does not install the window libraries. | `video-editor setup` |
| Open the picture window | The same X11 window used on Linux. It needs `DISPLAY` and the host GTK 4 and GStreamer packages. | `video-editor` on a terminal where `DISPLAY` is set |

## 2. Core Rules (Mandatory)

1. **Detect.** The program **MUST** treat the host as Windows when `os.name` is `nt`, when `sys.platform` starts with `win`, or when the environment variable `OS` starts with `windows` (compared without case). Git Bash around Windows Python still counts when the interpreter reports one of those signals. Detect **MUST** run before any code assumes `os.geteuid` or a successful `import curses`.

2. **Supported door.** On that host, with no X11 `DISPLAY`, the supported door is the text menu on a terminal and the typed verbs. `WAYLAND_DISPLAY` alone **MUST NOT** open the picture window. No terminal and no verb **MUST** print help and return 0. Those routes stay on `requirement-python-cli-interface` and `requirement-python-tui`.

3. **Picture window.** When the product has a picture window, that window **MUST** remain the existing X11 window. It opens only when `DISPLAY` is non-empty, standard input and output are a terminal, and the host window libraries import. An empty `DISPLAY`, a refused X server, or a missing library **MUST** leave the window module on disk. This requirement **MUST NOT** replace that window with a native Windows window.

4. **Missing window library.** Operator text for that miss **MUST** name the text menu as the next step and **MUST** state that the check does not install the libraries. It **MUST NOT** print `pacman`, `msys2`, `mingw-w64`, `UCRT64`, or `curl | sh`. It **MUST NOT** run an installer, open a socket, or use sudo. The sentences stay on `requirement-python-about`.

5. **Curses.** The pip manifest **MUST NOT** list `windows-curses` or `_curses`. Each load-time `import curses` **MUST** sit in `try` / `except ImportError`, so a missing module does not stop verbs that do not open the text menu. Opening the text menu **MUST** fail closed and name the missing module. The environment verb **MAY** install `windows-curses` on a Windows host only when that import fails. The load-time handler **MUST NOT** install it. The import rule and the verb step stay on `requirement-python-tui`, `requirement-python-packaging`, and `requirement-runtime-prerequisites`.

6. **Status logger.** Before the status-logger import, an interpreter with no `os.geteuid` **MUST** receive a bind that returns a non-zero id, so the log folder stays with this user. An interpreter that already has `os.geteuid` **MUST** keep that function. The library **MUST NOT** be edited. The bind stays on `requirement-python-cli-logging`.

7. **Environment verb.** The verb that prepares the interpreter installs the declared pip libraries as the current user. On Windows it may also try the curses module and FFmpeg. A refused host-package command **MUST** be printed with the command and the error. It **MUST NOT** raise out of the report, and it **MUST NOT** be replaced by a downloaded installer script. The verb **MUST NOT** install the picture-window libraries. The command bodies stay on `requirement-runtime-prerequisites`. The verb name stays on `requirement-python-cli-interface`.

8. **Shells.** Git Bash and Windows cmd **MUST NOT** invoke Termux `pkg`. They **MUST NOT** grow in-tool `sudo`, an `apt` or `dnf` wrap, an `/etc` destination, or a dedicated system account. A Windows virtual environment is activated with the `Scripts` activate script (`venv\Scripts\activate`).

9. **No frozen machine.** Core rules and Implementation Notes **MUST NOT** record a session login, a home directory, a LAN address, or a live `DISPLAY` value such as `:0`.

10. **Point, do not copy.** This file **MUST NOT** become a second owner of the environment-verb argv, the about-page lines, the window-open procedure, or the logger construct.

### 2.1 Implementation Notes (this project)

| Fact | Value |
|------|--------|
| Product | VideoEditor. Console script `video-editor`. Module `python -m VideoEditor`. Product version **1.0.0**. This requirement does not bump that version |
| Home | `https://github.com/cloudgen/VideoEditor` |
| Detect | `HostSetup.windows_host` in `src/VideoEditor/host_setup.py` and `AboutPage._windows_host` in `src/VideoEditor/about_page.py` use rule 1 |
| Picture window | Class `Gui` in `src/VideoEditor/gui.py`. `Cli.opens_window` in `src/VideoEditor/cli.py` requires a non-empty `DISPLAY`, a terminal, and no verb. `Gui.open` sets `GDK_BACKEND` to `x11` |
| Text menu | `requirement-python-tui`. Verb `tui` opens it even when `DISPLAY` is set |
| About | `requirement-python-about`. Windows miss text and the “does not install” line stay there. Proof `TP-ABOUT-17` |
| Logger bind | `HostSetup.ensure_geteuid` runs in `def main` before `from ChronicleLogger import ChronicleLogger`. Proof `TP-SETUP-01`. Owner `requirement-python-cli-logging` |
| Declared pip floors | `ChronicleLogger>=1.3.1` and `opencv-python-headless>=5.0.0.93` in `pyproject.toml`. `windows-curses` is absent there |
| Verb `setup` | Named on `requirement-python-cli-interface`. Steps on `requirement-runtime-prerequisites`. Proof `TP-SETUP-02`. Last report line states that setup does not install GTK 4 or GStreamer |
| FFmpeg | Host binary. The Windows attempt and a refused command stay on `requirement-runtime-prerequisites`. A refusal is printed. It does not hide the rest of the report |
| Window libraries | GTK 4 and GStreamer are host packages. They are not pip dependencies. PyPI packages that do not provide `gi.repository.Gtk` and `gi.repository.Gst` are not a substitute for that import |
| Tested picture-window path | Linux, when `DISPLAY` is set and those host libraries import. Windows without `DISPLAY` uses the text menu and the typed verbs |
| Virtual environment | On Windows, `venv\Scripts\activate` |

### 2.2 Why This Requirement Exists (Direct CIAO Alignment)

- **CIAO Principle 1 – Caution** (https://github.com/cloudgen/ciao): Windows Python has no `os.geteuid` and may lack `_curses`. Both are handled before they stop `about`, `version`, `help`, and `hello`.
- **CIAO Principle 2 – Intentional**: One host contract records the decisions that were already fixed in peer law, so a later edit does not treat an empty `DISPLAY` as a removed window.
- **CIAO Principle 5 – SSOT**: Command text stays on the peer that already owns it.
- **CIAO Principle 9 – Privilege layers**: Git Bash and Windows cmd stay at normal user privilege.
- **CIAO Principle 21 – Dual policies**: Core rules stay free of this product’s paths. Implementation Notes name VideoEditor.

## Under command line for normal user only

On Termux, Git Bash, Windows cmd, or the same class, VideoEditor runs as the person who started it. **This requirement:** Windows cmd and Git Bash are that class. Do not use administrator privilege, `sudo`, `apt`, `dnf`, or a dedicated system account. Do not pipe a downloaded script into a shell. Administrator privilege and dedicated system user privilege are unused on those shells. Git Bash and Windows cmd do not call Termux `pkg`. `video-editor setup` uses `python -m pip` as this user. The about page does not install packages.

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** Detect the host from the interpreter. Catch a missing `curses` import. Bind a missing `geteuid` before the logger import.
- **Intentional:** The X11 window file stays. The Windows door is the text menu and the typed verbs until `DISPLAY` and the host libraries are present.
- **Anti-fragile:** A refused FFmpeg install is a printed command and error. The process still finishes the rest of the report.
- **Over-protect:** Do not delete `src/VideoEditor/gui.py`, do not retarget it to a native Windows toolkit, and do not add `windows-curses` to `pyproject.toml`.
- **Principle 5:** One owner for each procedure. This file points.
- **Principle 10:** The person at the keyboard is the only account this program uses on Windows.

## 4. Protection Rule (Sacred)

**Future AI assistants or maintainers MUST NOT:**

1. Delete `src/VideoEditor/gui.py` or describe an empty `DISPLAY` as a removed picture window.
2. Replace the X11 window with a native Windows window unless the user explicitly orders that redesign.
3. Open the picture window from `WAYLAND_DISPLAY` alone, or when `DISPLAY` is empty.
4. Print `pacman`, `msys2`, `mingw-w64`, or `UCRT64` as the Windows next step for a missing window library.
5. Make `about` or `setup` install GTK 4 or GStreamer, run sudo, open a socket, or run `curl | sh`.
6. Add `windows-curses` or `_curses` to `pyproject.toml`.
7. Let a missing `_curses` or a missing `os.geteuid` abort package import or `about` / `version` / `help` / `hello`.
8. Edit the ChronicleLogger library to add `geteuid`.
9. Turn a refused FFmpeg install into an uncaught exception, or replace that report with a downloaded installer.
10. Invoke Termux `pkg` because Git Bash or Windows cmd was detected.
11. Copy the `setup` argv, the about-page sentences, or the window-open procedure into this file as a second owner.
12. Freeze a session login, a home directory, a LAN address, or a live display id in this file.
13. Bump product version **1.1.0** only because this requirement was added.

**Violating any of these is a critical regression.**

## 5. Acceptance criteria

| ID | Criterion |
|----|-----------|
| AC-1 | Windows detect matches rule 1 in `HostSetup.windows_host` and `AboutPage._windows_host` |
| AC-2 | Empty `DISPLAY` does not remove `src/VideoEditor/gui.py`. The picture window still requires `DISPLAY` |
| AC-3 | `pyproject.toml` has no `windows-curses` entry |
| AC-4 | Peer proofs `TP-SETUP-01`, `TP-SETUP-02`, `TP-ABOUT-17`, and `TP-TUI-11` stay on their owners |
| AC-5 | This file does not restate the winget argument list or the about-page sentence list |
| AC-6 | Registered in `docs/requirements/index.md` with Area `python`. The class residual OS cell points here |

## 6. Related requirements (peer keys only)

| Key | Relationship |
|-----|----------------|
| `requirement-class-software-dev` | Residual OS cell points here |
| `requirement-runtime-prerequisites` | Verb `setup` steps, including Windows curses and FFmpeg. Primary owner of `TP-SETUP-02` |
| `requirement-python-cli-interface` | Verb `setup` is named there. It does not open the text menu or the window |
| `requirement-python-about` | GTK 4 and GStreamer check. Windows miss text. Primary owner of `TP-ABOUT-17` |
| `requirement-python-gui` | X11 window. Empty `DISPLAY` returns before toolkit load |
| `requirement-python-tui` | Text menu. Load-time `import curses` uses `try`. Primary owner of `TP-TUI-11` |
| `requirement-python-cli-logging` | `HostSetup.ensure_geteuid` before the ChronicleLogger import. Primary owner of `TP-SETUP-01` |
| `requirement-python-packaging` | Declared pip floors. `windows-curses` stays out of the manifest |
| `requirement-python-oop` | Class `HostSetup` and class `Gui` |
| `docs/requirements/index.md` | Registry |

## Design-time verification

| TP family / ID | Suite | Status | Note |
|----------------|-------|--------|------|
| **TP-WIN-01** | `tests/test_windows.py` | todo | Windows detect, and an empty `DISPLAY` leaves the X11 window module in the package. Not written with this requirement |
| **TP-SETUP-01** | `tests/test_setup.py` | have | Peer. Primary owner `requirement-python-cli-logging` |
| **TP-SETUP-02** | `tests/test_setup.py` | have | Peer. Primary owner `requirement-runtime-prerequisites` |
| **TP-ABOUT-17** | `tests/test_about.py` | have | Peer. Primary owner `requirement-python-about` |
| **TP-TUI-11** | `tests/test_tui.py` | have | Peer. Primary owner `requirement-python-tui` |

**Matrix:** `docs/reviews/requirement-test-matrix.md`
**Map:** `docs/reviews/test-plan.md`

## Terminologies

### command-line-for-normal-user-only

**Definition:** A command line for normal user only is a POSIX-like shell environment whose privilege ceiling is Type 0 (normal user privilege). Typical instances: Termux, Git Bash, and Windows cmd (Windows Command Prompt / Windows command-line). There is no usable root/`sudo` host mutate and no dedicated system account for this login. When the ship unit detects this class (or detects Termux, Git Bash, or Windows cmd), it MUST NOT implement or enable admin privilege (Type 1) or dedicated system user privilege (Type 2): no in-tool `sudo`, no `apt`/`dnf` wrap, no `/etc` dest, no `useradd`, no dedicated-account switch.

**Human daily-life explanation:** A command line for normal user only is a keyboard that only has your keys. Termux on a phone, Git Bash on Windows, and Windows cmd / Command Prompt are this kind of room: you can tidy your own drawer; you cannot borrow the building site key or put on a dedicated-operator badge.

**Daily-life example:** On Termux you run `pkg` as yourself. On Git Bash you run `git` as yourself. On Windows cmd you type as yourself. None of those rooms should grow a `sudo apt` or a hidden system-user switch.

### windows-cmd

**Definition:** Windows cmd is an instance of command line for normal user only — the Windows-native console family: Command Prompt (`cmd.exe`) and the same Windows command-line (including PowerShell when it is not Git Bash / Cygwin / WSL). Typical detect: `OS` is `Windows_NT`, or `ComSpec` / `COMSPEC` names `cmd.exe`, after excluding Git Bash (`MSYSTEM` / MINGW / MSYS), Cygwin (`uname` `CYGWIN*`), and WSL (`WSL_DISTRO_NAME` or `uname` `Linux`). On detect, Type 1 (admin privilege) and Type 2 (dedicated system user privilege) stay unused. Windows cmd has no Termux `pkg` and no Unix `sudo` / `apt`.

**Human daily-life explanation:** Windows cmd is a Windows drawer that only opens with your keys. It is the ordinary Command Prompt / Windows command-line — not a Linux superintendent desk and not Git Bash.

**Daily-life example:** You type commands in Command Prompt or PowerShell as yourself. The program must not grow `sudo apt` or a dedicated system-user switch because you opened Windows cmd.

### git-bash

**Definition:** Git Bash is an instance of command line for normal user only — the MSYS/MINGW POSIX shell shipped with Git for Windows. Primary detect: directory `/c/` or `/c` exists (Windows `C:` as Git Bash mounts it; default drive `/c/`). Secondary: `MSYSTEM` is `MINGW*` / `MSYS*` / `UCRT*` / `CLANG*`, or `uname -s` is `MINGW*` / `MSYS*`. Exclude WSL (`WSL_DISTRO_NAME`). On detect, Type 1 (admin privilege) and Type 2 (dedicated system user privilege) stay unused. Git Bash has no Termux `pkg`. Volatile scratch is the Git Bash temp folder.

**Human daily-life explanation:** Git Bash is a Windows drawer that only opens with your keys. It looks like a Unix shell; it is not a Linux superintendent desk.

**Daily-life example:** You run `git` and this program as yourself. The program must not grow `sudo apt` or a dedicated system-user switch because you opened Git Bash.

### Python GUI window

**Definition:** Python GUI window is a claimed picture window on a Python CLI. The window imports a host toolkit in this interpreter. The operator page reports that import. A failed import is the text `not available`. On Windows, a miss names the text-screen verb the specialized requirement already claims and states that the page does not install the toolkit. The page does not print `pacman`, `msys2`, `mingw-w64`, or `UCRT64`, and it does not run a package manager or an installer. The specialized requirement names the toolkit and the open rule. This term does not mint a GUI law mold and does not attach every CLI verb to the window.

**Human daily-life explanation:** A python-gui-window is the shop’s picture counter. The card on the wall says whether today’s tools are in this drawer. When the drawer is empty, the card points you back to the written counter you already know. The card does not send you to a second shop to run a foreign package command.

**Daily-life example:** You ask what the picture counter needs. The card says the tools are missing and tells you to use the written counter. It does not hand you a command for a different shop’s package shelf.

### Proper project version bump

**Definition:** A proper project version bump is a user-ordered semver increase of the product ship version that is strictly newer than the previous local ship version, applied in the same change on every in-scope surface. When `pyproject.toml` exists, `[project].name` is the app and package name and `[project].version` equals the import-package `__version__`, the ship-unit version, the README Version badge, and the current CHANGELOG heading. A bump is not a side effect of editing a requirement, a skill, or a glossary file. Agents must not invent a second version literal beside the one the user ordered.

**Human daily-life explanation:** A proper project version bump is printing one newer edition number on every copy of the book in the same sitting, because someone asked for a new edition. Editing a workshop note does not print a new edition by itself. When the catalog card exists, the name on the card is the product name and the number on the card is the same number as the title page.

**Daily-life example:** The kitchen card says name `pancake-timer` and edition `1.2.0`. The title page, the cover sticker, and the change list all say `1.2.0`. The next ordered edition is `1.2.1` on all of those surfaces together. A note in the workshop drawer does not become `1.2.1` on its own.

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-10-11 | Active 1.0.0 | Windows host contract. Points at the existing owners for `setup`, about, the X11 window, the logger bind, and the pip manifest. `TP-WIN-01` is todo. Product version stays **1.1.0** |
| 2026-10-11 | Active 1.0.1 | The live product-version cell is **2.0.0**. This file does not cause that bump. Rule 13 still forbids bumping **1.1.0** only because this requirement was added |
| 2026-10-12 | Active 1.0.2 | Distribution name is VideoEditor. Console script is `video-editor`. Current release string is **1.0.0**. |

---

**Last Updated**: 2026-10-12
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
