**file**: docs/requirements/requirement-python-cli-interface.md
**Status**: Active (Version 1.1.5)
**Area**: python
**Key**: `requirement-python-cli-interface`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

Define the official command-line entry points, empty-argv behavior, and typed verbs for the VideoJoin Python package.

The text-menu picture is `requirement-python-tui`. Join steps and formats are `requirement-domain-videoeditor`. The about page is `requirement-python-about`. The domain sentence stays on the domain file. The logger construct is `requirement-python-cli-logging`. Class homes are `requirement-python-oop`. Concat order is `requirement-video-ffmpeg-pipeline`.

`def main` writes `ChronicleLogger(...)` and then constructs `Cli`. The argument parser runs after that construct and after the debug block. The running `src/VideoEditor/cli.py` still starts the prompt session. The allowed end state is this file. This pass does not change `src/`.

### 1.1 Human-facing

**In one sentence:** `video-editor` with no words opens the numbered menu on a terminal, and with no terminal it prints help and stops. `video-join` and `video-speed` call the same entry.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | Person at the keyboard or in a script | `video-join` or `video-join join` |
| The other role | The menu picture and the join facts | `requirement-python-tui`, `requirement-domain-videoeditor` |
| Not this file | How the frame is drawn, and how FFmpeg concatenates | TUI and pipeline requirements |

| Includes | Excludes |
|----------|----------|
| Console script, module entry, typed verbs, empty-argv menu or help | A shell installer on empty argv. File-operand flags for join |
| `join`, `list-videos`, `edit`, and `list-mp4` as typed verbs, also owned by the domain file | A numbered row for `list-videos`, `list-mp4`, or `help`. `hello` stays a verb and is not a front row |
| Pip verbs `version-check`, `self-update`, `self-install`, `self-uninstall`, also owned by the text menu | `sudo` pip, or a downloaded script piped into a shell |

| Surface | What you open | What for |
|---------|---------------|----------|
| `video-join` on a terminal | Front board | Menu. Does not start the join questions |
| `video-join` with no terminal | Help text | Exit 0 |
| `video-join join` on a terminal | Join questions | First index, second index, output name |
| `video-join help` | Help text | Verb list. Does not draw the menu |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Start on a terminal | The front board opens. Pip does not run. | `video-join` |
| Start in a script | Help text, exit 0. | `video-join` |
| Join two videos | On a terminal, the questions use the bottom box. With no terminal, the program stops and tells you to use a terminal. | `video-join join` |
| List files | Names in this folder. Nothing is joined. | `video-join list-videos` |
| Check or change the install | Pip runs only when you ask. Empty argv does not. | `video-join version-check` |

## 2. Core Rules (Mandatory)

### 2.1 Entry points

1. **MUST** expose console script `video-editor` pointing at `VideoEditor.cli:main`, and aliases `video-join` and `video-speed` pointing at the same entry (declared in packaging SSOT).
2. **MUST** support module execution: `python -m VideoEditor`.
3. **MUST** keep `def main` in `src/VideoEditor/cli.py` as the single runtime entry. `main` writes `ChronicleLogger(...)` before it constructs `Cli` (`requirement-python-cli-logging`, `requirement-python-oop`).
4. **MUST NOT** require root or sudo to run the CLI.

### 2.2 Empty argv

5. On a terminal, bare invocation with `DISPLAY` set **MUST** open the window in `requirement-python-gui`. It **MUST NOT** open the text menu, **MUST NOT** start the join questions or the edit questions, and **MUST NOT** run pip. On a terminal, bare invocation with `DISPLAY` unset **MUST** open the front board in `requirement-python-tui`. It **MUST NOT** start those questions and **MUST NOT** run pip.
6. When stdout is not a terminal, bare invocation **MUST** print help and return 0. It **MUST NOT** draw the text screen, **MUST NOT** open the window, and **MUST NOT** wait.
7. **MUST NOT** default empty argv to a shell-channel install or to self-update.

### 2.3 Typed verbs

8. `ArgumentParser.parse_args` **MUST** run after `ChronicleLogger(...)` and after the debug block.
9. The typed verbs are `help`, `version`, `about`, `hello`, `tui`, `join`, `list-videos`, `edit`, `list-mp4`, `self-install`, `version-check`, `self-update`, `self-uninstall`, and `setup`. Each one is operational. **MUST NOT** add a verb whose only purpose is a test. `tui` on a terminal **MUST** open the text menu in `requirement-python-tui`, including when `DISPLAY` is set. `tui` is not a numbered row. `setup` **MUST NOT** open the text menu and **MUST NOT** open the window. `setup` is not a numbered row. The environment steps stay on `requirement-runtime-prerequisites`. `language` is not a typed verb. Menu row 4 owns it (`requirement-python-cli-language`). **MUST NOT** add `language` to `PRODUCT_VERBS`. Exit is menu row 9 and is not an argv verb.
10. **MUST NOT** invent file-operand flags for `join`. Direct `join` with no terminal exits non-zero and tells the operator to use a terminal. Edit **MAY** use `--file`, `--folder`, `--start`, `--end`, `--percent`, `--boomerang`, and `--repeat`. Those flags do not apply to join. `--boomerang` and `--repeat` together **MUST** fail closed before FFmpeg runs.
11. On a terminal, `join` **MUST** start the join questions on the text screen (rules 16–23). `list-videos` **MUST** list eligible videos and **MUST NOT** join. `edit` without a complete `--file`, `--start`, and `--end` **MUST** ask folder, then file, on the text screen. `list-mp4` lists MP4 files and **MUST NOT** encode. `about` **MUST** open the about page.
12. With no terminal, `list-videos` **MUST** print the eligible names and return 0. `about` **MUST** print the about page and return 0. Neither draws the text screen.
13. `help`, `hello`, and `setup` **MUST NOT** draw the text screen. `help` returns 0. `hello` prints `Hello from VideoEditor <version>.` using `__version__`, then the next step `video-editor help`, and returns 0. `setup` returns the code from `requirement-runtime-prerequisites`.
14. `version` **MUST** print `__version__` and **MUST NOT** call pip and **MUST NOT** draw the text screen.
15. `version-check`, `self-update`, `self-install`, and `self-uninstall` **MUST NOT** open the text screen. The commands are:

| Verb | Command |
|------|---------|
| `version-check` | `python -m pip index versions VideoJoin` |
| `self-update` | `python -m pip install --upgrade VideoJoin` |
| `self-install` | `python -m pip install VideoJoin` |
| `self-uninstall` | `python -m pip uninstall -y VideoJoin` only when `--force` is also present |

`self-uninstall` without `--force` **MUST** print the next step and return non-zero. The package stays installed. These commands **MUST NOT** use `sudo` and **MUST NOT** use `curl`. Empty argv **MUST NOT** run `self-install` or `self-update`.

Every typed verb is named again by its topic owner. Help text is not that second mention.

| Verb | Second mention |
|------|----------------|
| `help`, `hello`, `version` | This file for `help` and `hello`. `version` is also row 82 on `requirement-python-tui` |
| `tui` | `requirement-python-gui` and `requirement-python-tui`. It opens the text menu |
| `about` | `requirement-python-about` and row 83. The domain sentence stays on pillar D of `requirement-domain-videoeditor` |
| `join`, `list-videos`, `edit`, `list-mp4` | `requirement-domain-videoeditor` |
| `self-install`, `version-check`, `self-update`, `self-uninstall` | Rows 84–87 on `requirement-python-tui` |
| `setup` | `requirement-runtime-prerequisites`. It installs the declared pip libraries. On Windows it also tries curses and ffmpeg |

`language` is not in this table. The second mention of that ban is `requirement-python-cli-language`.

Complete invocation samples:

```text
video-join
video-join help
video-join hello
video-join version
video-join about
video-join join
video-join list-videos
video-join self-install
video-join version-check
video-join self-update
video-join self-uninstall --force
video-editor setup
python -m VideoEditor
```

### 2.4 Join questions

These rules are the `join` verb. The text screen draws them (`requirement-python-tui`). The domain file owns the step catalog. They are not what empty argv does.

16. **MUST** scan the current working directory for eligible video files (domain format set).
17. **MUST** list discoverable videos with 1-based indices, sorted case-insensitively by name.
18. When fewer than two eligible videos are found, **MUST** fail closed with a clear message and **MUST NOT** run FFmpeg. A direct `video-join join` exits non-zero. An already open front board stays open.
19. **MUST** ask for the first video index, then the second index from the remaining set (first choice excluded).
20. **MUST** ask again on a non-numeric or out-of-range selection. **MUST NOT** proceed with an invalid index.
21. **MUST** ask for the output filename. Empty means the documented default.
22. **MUST** show the chosen pair and the output path before running FFmpeg.
23. **MUST** show a clear success or failure outcome after the join attempt.

There is no folder question. Esc on the text screen returns to the front board and does not join.

### 2.5 Flags

24. The parser accepts the verbs in rule 9. `help` is also available as `--help`.
25. `--json` **MUST** be accepted. It **MUST NOT** open the text menu. With no verb and no `--file`, `--start`, `--end`, `--folder`, `--percent`, `--boomerang`, or `--repeat`, help goes to stderr and one JSON object is emitted, and the process returns 0. `edit --json` without a complete job still runs the edit JSON walk when stdin is a terminal. `--percent`, `--boomerang`, or `--repeat` alone, including with `--json`, **MUST** fail closed and **MUST NOT** be treated as JSON help. `--boomerang` and `--repeat` together **MUST** fail closed.
26. **MUST NOT** add `--debug`. Debug status is the environment gate on `requirement-python-cli-logging`. `--verbose` **MAY** be accepted. It **MUST NOT** force the console log mirror onto a text screen or onto `--json`.
27. **MUST NOT** add file-operand flags for the two join inputs or the join output. Edit flags are rule 10. A complete no-verb job (`--file`, `--start`, and `--end`) **MUST** encode and **MUST NOT** open the menu. `--percent` defaults to 100 on that job.

### 2.6 Output behavior

28. Join progress and failures **MUST** be visible to the operator. On the text screen they are drawn in the menu region. Off the text screen they are console lines.
29. Durable status **MUST** go through ChronicleLogger once `main` has constructed it (`requirement-python-cli-logging`). The console failure sentence remains required.
30. `--json` is the machine output for an edit job and for bare JSON help. It **MUST NOT** replace the join questions with a second output family. Join still uses the text screen on a terminal and a non-zero stop with no terminal.

### 2.7 FFmpeg gate

31. The front board **MUST** be allowed to open when `ffmpeg` is missing.
32. `join` **MUST** fail closed with an actionable message when `ffmpeg` is missing, before FFmpeg is spawned (`requirement-runtime-prerequisites`).
33. The about page names FFmpeg on the static runtime-tools line (`requirement-python-about`). It does not probe `PATH` and it does not install FFmpeg. `join` still fails closed when `ffmpeg` is missing.

### 2.8 Implementation Notes (this project)

| Item | Value |
|------|--------|
| **Console scripts** | `video-editor`, `video-join`, and `video-speed` = `VideoEditor.cli:main` |
| **Module entry** | `src/VideoEditor/__main__.py` → `main()` |
| **CLI module** | `src/VideoEditor/cli.py` defines `Cli` and `def main` |
| **Empty argv, terminal** | Front board. No join questions. No edit questions. No pip |
| **Empty argv, no terminal** | Help text. Return 0 |
| **Parser** | After ChronicleLogger and the debug block |
| **Quiet / JSON** | A text screen or `--json` sets the logger quiet. `--verbose` does not undo that |
| **Privilege** | user-level only |
| **Product version** | `1.0.0` |
| **User docs** | Root `README.md` Usage must match this contract when the behavior ships. This pass does not edit that README |

### 2.9 Why This Requirement Exists (CIAO)

- **Principle 2 – Intentional**: Entry, empty argv, and each typed verb are explicit.
- **Principle 16 – Interactive awareness**: A terminal opens the menu. No terminal prints help and returns 0.
- **Principle 5 – SSOT**: Verb names live here and on the topic owner. The picture lives on the TUI requirement.
- **Principle 10 – Least privilege**: Pip verbs do not use sudo.

## Under command line for normal user only

On Termux, Git Bash, Windows cmd, or the same class, the person runs `video-join` as the normal user. **This requirement:** do not use administrator privilege, `sudo`, `apt`, or a dedicated system user to start the program or to run the pip verbs. Do not pipe a downloaded script into a shell. Type 1 and Type 2 are unused on Termux, Git Bash, and Windows cmd. Git Bash and Windows cmd do not call Termux `pkg`.

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** Fewer than two videos does not encode. Invalid index asks again. Join with no terminal exits non-zero.
- **Intentional:** Empty argv is the menu on a terminal and help off a terminal.
- **Anti-fragile:** Module entry and the console script both call `main`.
- **Over-protect:** Empty argv does not install, update, or start the join questions.

## 4. Protection Rule (Sacred)

**Future AI assistants, Grok, or maintainers MUST NOT**:

1. Change empty argv into a shell-channel install.
2. Make empty argv start the join questions or run pip.
3. Make empty argv off a terminal exit non-zero. That path prints help and returns 0.
4. Remove the console script or the module entry without a packaging and docs update.
5. Require root to run a normal join.
6. Allow the same file as both inputs without a domain-law change.
7. Add file-operand flags to `join`, or add `--debug`. Edit flags and `--json` stay the rules in §2.
8. Treat help text as the second mention of a verb.
9. Add `language` as an argv verb. Row 4 is the menu language.

**Violating this rule is a critical CLI regression.**

## 5. Acceptance criteria

| ID | Criterion |
|----|-----------|
| AC-1 | `video-editor`, `video-join`, and `video-speed` are declared in packaging and call `VideoEditor.cli:main` |
| AC-2 | `python -m VideoEditor` reaches `main` |
| AC-3 | Empty argv on a terminal with `DISPLAY` set opens the window. With `DISPLAY` unset it opens the front board. It does not join and does not run pip |
| AC-4 | Empty argv with no terminal prints help and returns 0 |
| AC-5 | Direct `join` with no terminal exits non-zero |
| AC-6 | Fewer than two videos does not encode. An invalid index asks again |
| AC-7 | Pip verbs match the command table and do not use sudo or curl |
| AC-8 | `setup` is a typed verb. It does not open the text menu or the window. Its second mention is `requirement-runtime-prerequisites` |

## 6. Related requirements (peer keys only)

| Key | Relationship |
|-----|----------------|
| `requirement-python-tui` | Menu picture and numbered rows. Verb `tui` |
| `requirement-python-gui` | X11 window for a bare start when `DISPLAY` is set |
| `requirement-python-cli-language` | `language` is not an argv verb. Menu row 4 |
| `requirement-domain-videoeditor` | Join steps, edit steps, both lists, and the about domain sentence |
| `requirement-python-about` | The about page |
| `requirement-python-cli-logging` | Construct before the parser |
| `requirement-python-oop` | `Cli` and `def main` |
| `requirement-video-ffmpeg-pipeline` | Concat after the questions |
| `requirement-python-packaging` | Console script name |
| `requirement-python-error-handling` | Fail messaging |
| `requirement-runtime-prerequisites` | FFmpeg check on join |
| `docs/requirements/index.md` | Registry |

## Design-time verification

| TP family / ID | Suite | Status | Note |
|----------------|-------|--------|------|
| **TP-CLI-01** | `tests/test_cli.py` | todo | Empty argv on a tty opens the front board |
| **TP-CLI-02** | `tests/test_cli.py` | todo | Invalid index on `join` asks again and does not encode |
| **TP-CLI-03** | `tests/test_cli.py` | todo | Fewer than two eligible videos → message, no encode |
| **TP-CLI-04** | `tests/test_cli.py` | optional | Empty argv off a tty prints help and returns 0 |
| **TP-TUI-07** | `tests/test_tui.py` | todo | Direct `join` off a tty exits non-zero |
| **TP-SETUP-02** | `tests/test_setup.py` | have | `setup` stays off the text menu and the window. Windows runs the declared pip install, then `windows-curses` when curses cannot be imported, then the FFmpeg winget command. Primary owner of the steps is `requirement-runtime-prerequisites` |

**Matrix:** `docs/reviews/requirement-test-matrix.md`
**Map:** `docs/reviews/test-plan.md`

## Terminologies

### Proper project version bump

**Definition:** A proper project version bump is a user-ordered semver increase of the product ship version that is strictly newer than the previous local ship version, applied in the same change on every in-scope surface. When `pyproject.toml` exists, `[project].name` is the app and package name and `[project].version` equals the import-package `__version__`, the ship-unit version, the README Version badge, and the current CHANGELOG heading. A bump is not a side effect of editing a requirement, a skill, or a glossary file. Agents must not invent a second version literal beside the one the user ordered.

**Human daily-life explanation:** A proper project version bump is printing one newer edition number on every copy of the book in the same sitting, because someone asked for a new edition. Editing a workshop note does not print a new edition by itself. When the catalog card exists, the name on the card is the product name and the number on the card is the same number as the title page.

**Daily-life example:** The kitchen card says name `pancake-timer` and edition `1.2.0`. The title page, the cover sticker, and the change list all say `1.2.0`. The next ordered edition is `1.2.1` on all of those surfaces together. A note in the workshop drawer does not become `1.2.1` on its own.

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-08-09 | Active 1.0.0 | Initial Python CLI interface law for VideoJoin |
| 2026-10-04 | Active 1.1.0 | Empty argv opens the text menu on a terminal and prints help off a terminal. Typed verbs. Join questions are the `join` verb |
| 2026-10-04 | Active 1.1.1 | `language` is not an argv verb. Menu row 4 owns it |
| 2026-10-04 | Active 1.1.2 | Verb `about` is `requirement-python-about`. Rule 33 no longer claims a live ffmpeg probe. Product version **1.0.5** |
| 2026-10-10 | Active 1.1.3 | Verb `setup` is typed. It does not open the text menu or the window. The second mention is `requirement-runtime-prerequisites`. `TP-SETUP-02` is have |
| 2026-10-11 | Active 1.1.4 | Product version is **2.0.0**. Terminologies copies the ship-version term |
| 2026-10-12 | Active 1.1.5 | Distribution name is VideoEditor. Console script is `video-editor`. Current release string is **1.0.0**. |

---

**Last Updated**: 2026-10-12
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
