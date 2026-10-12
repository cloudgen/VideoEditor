**file**: docs/requirements/requirement-runtime-prerequisites.md
**Status**: Active (Version 1.1.6)
**Area**: runtime
**Key**: `requirement-runtime-prerequisites`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

Declare the host and Python runtime prerequisites required to run VideoJoin. This product does not implement a privileged installer. This file is the documentation and validation SSOT for what must already be present, together with the ChronicleLogger floor also owned by `requirement-python-packaging`.

### 1.1 Human-facing

**In one sentence:** You need Python, ChronicleLogger, OpenCV from pip, and FFmpeg on your PATH before a join or an edit encode can finish. The text menu also needs the interpreter module `_curses`, and a missing module is caught with `try`. `video-editor setup` installs the declared pip libraries. On Windows it also tries curses and FFmpeg.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | Person about to join two videos | FFmpeg is already installed by you, not by pip |
| The other role | pip | Installs VideoJoin and ChronicleLogger. It does not install FFmpeg |
| Not this file | The menu picture and the concat command | TUI and pipeline requirements |

| Includes | Excludes |
|----------|----------|
| FFmpeg on PATH, required for `join` and for an edit encode. OpenCV from pip for the duration probe | A claim that pip installs FFmpeg |
| ChronicleLogger `>=1.3.1`, required | Calling that library optional |
| The text menu’s `curses` import inside `try` / `except ImportError`, so a missing `_curses` does not raise | Declaring `_curses` or `windows-curses` in `pyproject.toml` |
| Typed verb `setup`: `python -m pip install` of the declared floors, as this user | A root install, `sudo`, or a downloaded script |
| On Windows, `setup` may `python -m pip install windows-curses` when `import curses` fails, and may run the FFmpeg winget command below | Installing GTK 4 or GStreamer from `setup`. Printing `pacman` |

| Surface | What you open | What for |
|---------|---------------|----------|
| PATH | `ffmpeg` | Concat and the fallback re-encode |
| pip | ChronicleLogger | Status file |
| About page | Runtime-tools line | Names FFmpeg. Does not probe PATH (`requirement-python-about`) |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Install the Python package | You get VideoJoin and the status library. | `python -m pip install VideoJoin` |
| Prepare a join | FFmpeg must already be on PATH. The menu may open before that check. | `ffmpeg -version` |
| Start with the library missing | The console prints the pip next step and returns non-zero. | `video-join` |
| Prepare this Python | `setup` installs the declared pip libraries. On Windows it also tries curses and FFmpeg. | `video-editor setup` |

## 2. Core Rules (Mandatory)

### 2.1 Scope

1. **MUST** document every external tool required at runtime.
2. **MUST NOT** claim the product auto-installs system packages via root or sudo.
3. **MUST** separate pip-installable Python dependencies from system binaries.

### 2.2 Required runtime components

| Component | Kind | Required for | Install surface |
|-----------|------|--------------|-----------------|
| CPython | interpreter | package import and the CLI | OS, pyenv, or the system Python. This product does not require you to install pyenv |
| ChronicleLogger `>=1.3.1` | pip package | the one status logger | `pyproject.toml` / `python -m pip`. Required, not optional |
| `curses` (`_curses`) | interpreter module | the text menu | `try` / `except ImportError` around `import curses`. Not a pip package |
| FFmpeg (`ffmpeg` on PATH) | system binary | stream-copy concat and the re-encode fallback | the operator’s own install. Not pip |

### 2.3 Validation

4. **MUST** fail with an actionable message when `join` runs and `ffmpeg` is missing.
5. The front board **MAY** open when `ffmpeg` is missing. About reports whether it is on PATH. About does not install it.
6. **MUST** document that FFmpeg is not installed by `pip install VideoJoin`.
7. **MUST** document the input formats as the domain format set.
8. If `ChronicleLogger` cannot be imported, `def main` **MUST** print the pip next step and return non-zero (`requirement-python-cli-logging`). That line is console text. The library is required.
9. The text menu depends on the interpreter module `curses`, whose extension is `_curses`. That module **MUST NOT** be declared in `pyproject.toml`. `windows-curses` **MUST NOT** be added to `pyproject.toml`. Every load-time `import curses` in `src/VideoEditor/tui.py`, `src/VideoEditor/menu_painter.py`, and `src/VideoEditor/menu_model.py` **MUST** sit inside `try` / `except ImportError`. That `try` is how a missing `_curses` avoids the import error. The exception **MUST NOT** leave package import. `about`, `version`, `help`, and `hello` **MUST** still run. Opening the text menu **MUST** fail closed as `requirement-python-tui` states. The handler **MUST NOT** install a package.

### 2.3a Verb `setup`

9a. `setup` is a typed verb (`requirement-python-cli-interface`). It **MUST NOT** open the text menu and **MUST NOT** open the window. It is not a numbered menu row. Class `HostSetup` in `src/VideoEditor/host_setup.py` owns the argument lists and `run`. `cli.py` **MUST NOT** build those lists.
9b. `setup` **MUST** run `sys.executable -m pip install` of `ChronicleLogger>=1.3.1` and `opencv-python-headless>=5.0.0.93` as the current user. The child’s stdin **MUST** be closed. The command **MUST NOT** use `sudo` and **MUST NOT** use `curl`.
9c. On Windows (`os.name == "nt"`, or `sys.platform` starts with `win`, or the environment variable `OS` starts with `windows`), when `import curses` fails, `setup` **MUST** run `sys.executable -m pip install windows-curses` and then import `curses` again. On any other host, `setup` **MUST NOT** install `windows-curses`. `pyproject.toml` **MUST NOT** list `windows-curses`. The load-time handler in rule 9 **MUST NOT** install it.
9d. On Windows, when `ffmpeg` is absent from `PATH` and `winget` is on `PATH`, `setup` **MUST** run `winget install -e --id Gyan.FFmpeg --accept-package-agreements --accept-source-agreements --disable-interactivity`. When that start raises `OSError`, including access denied on a WindowsApps alias, `setup` **MUST** retry once as `cmd.exe /d /c` plus those same arguments. When `winget` is absent, or both starts raise `OSError`, `setup` **MUST** print `On Windows, run:` and that winget command, and **MUST NOT** raise. On any other host, `setup` **MUST NOT** call `winget`. A missing `ffmpeg` there **MUST** print `Install FFmpeg and ensure ffmpeg is available.`
9e. `setup` **MUST NOT** install GTK 4 or GStreamer. It **MUST** print the window-library lines from `AboutPage` and the sentence `setup does not install GTK 4 or GStreamer.` That operator report **MUST** appear once. The logger **MAY** record `setup finished with code` and **MUST NOT** be the second copy of the report on the console. The report **MUST NOT** contain `pacman`, `msys2`, `mingw-w64`, `UCRT64`, or `curl`.
9f. The process exit code **MUST** be the pip exit code. That is the declared-floor install, and on Windows the `windows-curses` install when that install ran and returned non-zero. A missing or refused `ffmpeg` **MUST NOT** by itself make the exit non-zero when pip returned 0.
9g. Invocation sample:

```text
video-editor setup
```

### 2.4 Privilege

10. **MUST NOT** require root to satisfy runtime prerequisites for normal use.
11. Type 1 elevation is out of scope.

### 2.5 Implementation Notes (this project)

| Item | Value |
|------|--------|
| **Python package install** | `python -m pip install VideoJoin`, or `python -m pip install -e .` from a checkout |
| **Declared pip dependency (law)** | `ChronicleLogger>=1.3.1` and `opencv-python-headless>=5.0.0.93`, both required |
| **Live manifest** | `pyproject.toml` lists those two floors. It does not list `windows-curses` |
| **System binary** | `ffmpeg` on PATH, required for `join` |
| **Verb `setup`** | `video-editor setup`. Pip of the two floors as this user. On Windows, `windows-curses` only when `import curses` fails, then the winget command in rule 9d |
| **Auto install command** | `setup` is the operator command. It does not use root. pip does not install FFmpeg. `setup` does not install GTK 4 or GStreamer |
| **Platform notes** | Linux primary. macOS and Windows when FFmpeg and CPython are available. Windows CPython may ship `curses` without `_curses`. The import uses `try`. The picture window still needs `DISPLAY` and the host GTK 4 and GStreamer packages |
| **Text-menu module** | `_curses` is not a `pyproject.toml` dependency. `import curses` in `tui.py`, `menu_painter.py`, and `menu_model.py` is inside `try` / `except ImportError`. `setup` on Windows may pip-install `windows-curses` when that import fails |
| **Product version** | 1.0.0 |
| **Startup check** | FFmpeg is checked when `join` runs (`shutil.which` and `ffmpeg -version`). It is not a gate on the front board |
| **User docs** | Root `README.md` names `video-editor setup` and states FFmpeg is a system prerequisite. The picture window still needs `DISPLAY` |

### 2.6 Why This Requirement Exists (CIAO)

- **Principle 1 – Caution**: FFmpeg may be missing. The join says so.
- **Principle 10 – Least privilege**: No root installer.
- **Principle 2 – Intentional**: The pip library and the system binary are different rows.

## Under command line for normal user only

On Termux, Git Bash, Windows cmd, or the same class, the normal user installs the pip package and supplies FFmpeg. **This requirement:** do not use administrator privilege, `sudo`, `apt`, or a dedicated system user to install ChronicleLogger or FFmpeg from inside VideoJoin. Do not pipe a downloaded script into a shell. Type 1 and Type 2 are unused on Termux, Git Bash, and Windows cmd. Git Bash and Windows cmd do not call Termux `pkg`.

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** Document the missing tool before the join fails.
- **Intentional:** pip does not install FFmpeg. ChronicleLogger is required.
- **Anti-fragile:** Join works wherever `ffmpeg` is already on PATH.
- **Over-protect:** No silent root install.

## 4. Protection Rule (Sacred)

**Future AI assistants, Grok, or maintainers MUST NOT**:

1. Claim FFmpeg is installed by `pip install VideoJoin`.
2. Add a root package-manager install from this product.
3. Drop FFmpeg from the table while `join` still depends on it.
4. Store secrets in this file.
5. Drop the OpenCV duration dependency while edit still probes duration with it.
6. Call ChronicleLogger optional, or hide the manifest lag.
7. Leave a bare module-level `import curses` in `tui.py`, `menu_painter.py`, or `menu_model.py`.
8. Add `_curses` or `windows-curses` to `pyproject.toml` in place of the `try`, or make the load-time handler install a package.
9. Remove verb `setup`, or make `setup` use `sudo`, `curl`, or a package-manager line for GTK 4.

**Violating this rule is a critical honesty regression.**

## 5. Acceptance criteria

| ID | Criterion |
|----|-----------|
| AC-1 | FFmpeg is listed as a system binary |
| AC-2 | ChronicleLogger is a required pip dependency at `>=1.3.1`. The live manifest lag is stated |
| AC-3 | No root auto-install claim |
| AC-4 | Missing FFmpeg on `join` produces an actionable message |
| AC-5 | Missing ChronicleLogger produces the pip next step and a non-zero return |
| AC-6 | Load-time `import curses` uses `try` / `except ImportError`. A missing `_curses` does not leave package import. `_curses` and `windows-curses` are absent from `pyproject.toml` |
| AC-7 | `video-editor setup` installs the two declared floors with `sys.executable -m pip` and does not use sudo or curl. On Windows it may install `windows-curses` when the import fails, and it tries the FFmpeg winget command in rule 9d. It does not install GTK 4 or GStreamer. The report does not contain `pacman` |

## 6. Related requirements (peer keys only)

| Key | Relationship |
|-----|----------------|
| `requirement-python-packaging` | Floor owner for the pip dependency. `_curses` stays off that list |
| `requirement-python-tui` | Text menu. The missing-module sentence after the `try` |
| `requirement-python-cli-logging` | Construct. Missing-import sentence. `HostSetup.ensure_geteuid()` before that import |
| `requirement-python-cli-interface` | Verb `setup` is named there. This file owns the steps |
| `requirement-python-oop` | Class `HostSetup` |
| `requirement-video-ffmpeg-pipeline` | Uses FFmpeg |
| `requirement-python-error-handling` | Missing-tool messages |
| `requirement-domain-videoeditor` | About reports FFmpeg |
| `docs/requirements/index.md` | Registry |

## Design-time verification

| TP family / ID | Suite | Status | Note |
|----------------|-------|--------|------|
| **TP-PRE-01** | `tests/test_prerequisites.py` | todo | Host `ffmpeg`, or an actionable miss on `join` |
| **TP-PRE-02** | `tests/test_prerequisites.py` | todo | ChronicleLogger imports. Law floor is `>=1.3.1` |
| **TP-ERR-01** | `tests/test_errors.py` | todo | Peer: missing FFmpeg on `join` |
| **TP-SETUP-01** | `tests/test_setup.py` | have | Peer: `os.geteuid` bind. Primary owner is `requirement-python-cli-logging` |
| **TP-SETUP-02** | `tests/test_setup.py` | have | `setup` installs the declared floors. Windows adds `windows-curses` when the import fails and names `Gyan.FFmpeg`. A refused winget stays a printed command. GTK 4 is not installed |

**Matrix:** `docs/reviews/requirement-test-matrix.md`
**Map:** `docs/reviews/test-plan.md`

## Terminologies

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
| 2026-08-09 | Active 1.0.0 | Initial runtime prerequisites law for VideoJoin |
| 2026-10-04 | Active 1.1.0 | ChronicleLogger `>=1.3.1` is required. Live manifest still `>=1.2.3`. FFmpeg stays a system binary. The front board may open without it |
| 2026-10-04 | Active 1.1.1 | Product version **1.0.4**. Manifest floor is `ChronicleLogger>=1.3.1` |
| 2026-10-04 | Active 1.1.2 | The about page names FFmpeg and does not probe PATH. Product version **1.0.5** |
| 2026-10-10 | Active 1.1.3 | The text menu depends on `_curses`. The import uses `try` / `except ImportError`. A missing module does not leave package import. `_curses` is not a pip dependency |
| 2026-10-10 | Active 1.1.4 | Verb `setup` installs the declared pip floors. On Windows it may install `windows-curses` when `import curses` fails, and it tries `winget install -e --id Gyan.FFmpeg`. `pyproject.toml` stays without `windows-curses`. `setup` does not install GTK 4 or GStreamer. The operator report is printed once. `TP-SETUP-02` is have |
| 2026-10-11 | Active 1.1.5 | Live product version is **2.0.0**. `setup` still does not install GTK 4 or GStreamer |
| 2026-10-12 | Active 1.1.6 | Distribution name is VideoEditor. Console script is `video-editor`. Current release string is **1.0.0**. |

---

**Last Updated**: 2026-10-12
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
