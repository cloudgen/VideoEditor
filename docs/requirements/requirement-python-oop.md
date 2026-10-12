**file**: docs/requirements/requirement-python-oop.md
**Status**: Active (Version 1.0.6)
**Area**: python
**Key**: `requirement-python-oop`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

Define when VideoJoin uses a class, and name the file that holds each class. One class lives in one module. `def main` stays in `src/VideoEditor/cli.py`. Every class in the map accepts the one status logger as an `__init__` parameter so that class can log. The line text stays on `requirement-python-cli-logging`.

The menu picture stays on `requirement-python-tui`. The about page stays on `requirement-python-about`. The domain sentence stays on `requirement-domain-videoeditor`. Concat order and `shutil.move` stay on `requirement-video-ffmpeg-pipeline` and `requirement-python-coding-style`. This file decides the class and the file. It does not invent a second picture, a second about page, or a second concat order.

The target is an ordinary multi-class split. A StateLogic + `Attr` rewrite stays unordered. This file does not claim that rewrite. The notes still record the older three-module gap. `CheckSystem` and `AboutPage` are on disk for the about page. `TP-OOP-*` stay todo.

### 1.1 Human-facing

**In one sentence:** Each class lives in its own file, `main` stays in `cli.py`, and each class receives the logger in `__init__`.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | Maintainer adding a prompt, a log action, or a join step | Put it on the class that already owns that job |
| The other role | The menu picture, the about facts, and the concat order | Their own requirements |
| Not this file | A StateLogic rewrite of `main` | `requirement-python-coding-style` leaves that rewrite unordered |

| Includes | Excludes |
|----------|----------|
| One class per file. The class is the only public surface of that module. Constants that `Cli` owns live on class `Cli` | A second class in the same file, a module-level function beside the class, or a module-level assignment of `Cli`'s identity, verb lists, or suffixes |
| `def main` in `src/VideoEditor/cli.py` | Moving `main` to another module |
| Ordinary classes named in the map below | One class per function. A StateLogic rewrite |
| The one logger passed into `__init__`. `ClassName(...)` at the site that needs the object | A setter, a module global, a second logger built inside the class, or a factory |

| Surface | What you open | What for |
|---------|---------------|----------|
| `src/VideoEditor/cli.py` | `def main` and class `Cli` | Entry. Builds the other objects and runs one job |
| `src/VideoEditor/tui.py` | class `Tui` | Text-menu session |
| `src/VideoEditor/join.py` | class `Join` | Discover, pick two, name the output, run the concat |
| `src/VideoEditor/edit_walk.py` | class `EditWalk` | Folder, file, cut, percent, tail questions |
| `src/VideoEditor/encoder.py` | class `Encoder` | Cut, speed, and one tail: none, boomerang, or repeat |
| `src/VideoEditor/file_stage.py` | class `FileStage` | Temp paths for the edit encode |
| `src/VideoEditor/media_info.py` | class `MediaInfo` | OpenCV duration probe |
| `src/VideoEditor/run_output.py` | class `RunOutput` | Edit and JSON lines. Join questions stay on `Tui` |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Add a menu prompt | It is a method on `Tui`. The frame is `MenuPainter`. | Edit the class file this requirement names |
| Add a join step | It is a method on `Join`. The concat order stays on the pipeline requirement. | Edit `src/VideoEditor/join.py` |
| Start the program | The console scripts call `VideoEditor.cli:main`. | `video-editor` |
| Name a constant the program uses | It is an attribute of the class that owns it. `Cli` owns identity, the verb lists, and the suffix sets. | `Cli.APP_NAME` |

## 2. Core Rules (Mandatory)

### 2.1 Use a class when the functions share one job

1. When a set of functions shares one job, product Python **MUST** make them methods of one class and put that class in its own module under `src/VideoEditor/`.
2. **MUST NOT** make a class whose only method is a single function that nothing else in the file shares.
3. The class **MUST** be the only public surface of its module. A module-level `def` beside that class is a second home. **MUST NOT** add one.
4. That module **MUST** define one class. One exception type raised by that class **MAY** share the file. `MenuScreenError` shares `tui.py` with `Tui`.
5. The file name **MUST** be the class job in snake case (`MenuPainter` → `menu_painter.py`, `AboutPage` → `about_page.py`, `SelfManage` → `self_management.py`).
6. A full StateLogic + `Attr` rewrite of `main` and of the join stays unordered (`requirement-python-coding-style`). This file does not order that rewrite. The classes in the map are ordinary classes. The allowed end state is this map. **MUST NOT** collapse the end state back to a single procedural module. The running three-module tree remains legal until an implement order lands the files named here.

### 2.2 Entry: `main` stays in `cli.py`

7. `src/VideoEditor/cli.py` **MUST** define class `Cli` and **MUST NOT** define another class.
8. `def main` **MUST** stay in `src/VideoEditor/cli.py`. The signature stays `main(argv=None, basedir="", logdir="")`. `main` writes `ChronicleLogger(...)` (`requirement-python-cli-logging`), builds `Cli`, and runs one job. Empty `basedir` and `logdir` leave folder resolution to the library.
9. The console scripts **MUST** stay `video-editor`, `video-join`, and `video-speed`, each `VideoEditor.cli:main`. `src/VideoEditor/__main__.py` **MUST** keep `from .cli import main`.
10. `cli.py` **MUST NOT** define another class's methods. `Cli` owns `build_parser`, `dispatch`, `opens_text_screen`, `verb_help`, `verb_version`, `verb_about`, `verb_hello`, `verb_join`, `verb_list_videos`, `verb_lifecycle`, `unknown_verb`, `stdin_is_tty`, and `stdout_is_tty`. `Cli` does not own the ChronicleLogger construct. Lifecycle pip argument lists stay on `SelfManage`. The `setup` pip and winget argument lists stay on `HostSetup`. The about body stays on `AboutPage`. Join questions and the concat call stay on `Join`. The frame stays on `MenuPainter`.
11. `Cli` constructs the other classes and calls them. Each class receives its collaborators through its constructor.
11f. A constant or variable that class `Cli` or `def main` owns is an attribute of class `Cli`, or a name assigned inside `main()`. It is not a module-level assignment in `cli.py`. That set is `APP_NAME` (`VideoEditor`), `CONSOLE_NAME` (`video-editor`), `PRODUCT_VERBS`, `LIFECYCLE_VERBS`, `VIDEO_SUFFIXES`, `OUTPUT_SUFFIXES`, `AUTHOR_NAME`, `AUTHOR_EMAIL`, `HOMEPAGE`, `LAST_UPDATE`, `DOWNLOAD_URL`, `BASIC_USAGE`, `RATIO_MIN`, and `RATIO_MAX`. The about page prints the author name, the homepage, the box date, and the usage line. It does not print the email. The email stays on `Cli`. `Cli` reads the package version from `__version__` only and **MUST NOT** keep a second literal, including a fallback `"1.0.5"`. `Cli` **MUST NOT** keep `MAJOR`, `MINOR`, or `PATCH` integers. `Cli` passes the values other classes print. Those classes do not import the names from the `cli` module.
11g. Another class keeps its own constants. The frame glyphs, `MENU_ROWS`, `SELF_ROWS`, `LOG_ROWS`, `PATH_LABEL_EN`, and `PATH_LABEL_ZH_HANT` stay on `MenuPainter`. `Cli` does not own those names.

### 2.2a The logger arrives through `__init__`

11a. Every class in the map, and `MenuScreenError`, **MUST** accept the one ChronicleLogger as a parameter of `__init__`.
11b. `__init__` **MUST** store that object on `self.logger`. A class that constructs another class in the map **MUST** pass that same object into that constructor.
11c. `def main` writes `ChronicleLogger(...)` before `Cli` (`requirement-python-cli-logging`) and **MUST** pass that object into `Cli(...)`. `main` **MUST NOT** call `Cli.__new__` to build the logger. The parameter **MAY** default to absent so a caller that has no logger can omit it. `main` has the logger and **MUST NOT** omit it.
11d. **MUST NOT** construct a ChronicleLogger inside a class or from a method. **MUST NOT** attach the logger through a setter or a module global after `__init__` returns. **MUST NOT** call a module function to write the instantiation line. `__init__` calls `log_message` itself.
11e. The instantiation line, its level, and quiet stay on `requirement-python-cli-logging`. This file owns only that the logger arrives through `__init__`.
11h. The site that needs an object **MUST** write `ClassName(...)`. A factory is a function or a method whose job is to instantiate a class. This map does not include a factory. The class can be created without one. The ban on that factory also lives on `requirement-python-coding-style`.

### 2.3 Text menu

12. `src/VideoEditor/tui.py` **MUST** define class `Tui` and the exception `MenuScreenError`. No other class. `Tui` owns `open_text_menu`, `front_lines`, `self_lines`, `log_lines`, `language_lines`, `join_on_screen`, `list_on_screen`, `about_on_screen`, `help_on_screen`, `read_key`, and `notice`.
13. Class `MenuPainter` in `src/VideoEditor/menu_painter.py` owns `paint`, `paint_prompt`, `path_label`, `path_line`, `clock_text`, `format_rows`, `display_rows`, `screen_can_hold`, `display_width`, `clip_columns`, and `clip_columns_right`. The frame glyphs, `MENU_ROWS`, `SELF_ROWS`, `LOG_ROWS`, `PATH_LABEL_EN`, and `PATH_LABEL_ZH_HANT` live on that class. `display_width`, `clip_columns`, and `clip_columns_right` are methods of that class. The module does not define them beside the class. Wide and Fullwidth count as two. Ambiguous stays one. The column rule stays on `requirement-python-tui`. `FRAME_TOP_LEFT` **MUST NOT** appear in `cli.py`. `path_label`, `clock_text`, and `path_line` draw the first row of the front board, of the self-management board, of the system-log board, and of the language board. The clock shape, shortening the path from the left, and when the clock is omitted stay on `requirement-python-tui` rule 13. The selected word stays on `requirement-python-cli-language`. `path_label` returns that word. It does not read `LANG` or `LC_ALL`, and it does not invent a second line. `MenuPainter.__init__` writes `MenuLanguage(...)`.
14. Class `MenuModel` in `src/VideoEditor/menu_model.py` owns `apply_key`, `edge_keys`, `highlighted_row`, and `buffer_text`.
15. Class `MenuSession` in `src/VideoEditor/menu_session.py` owns `run`, `take_action`, `wait_key`, and `leave_to_front`. `wait_key` is the one-second clock wait from `requirement-python-tui` rule 13, including the language board. It does not start a thread. `run` loops until row 9 Exit. A leaf action returns to the front board. A language pick saves through the shared `MenuLanguage` and returns to the front board. `MenuSession` dispatches join, system-log, language, self-management, and exit. It does not paint the frame.
15a. Class `MenuLanguage` in `src/VideoEditor/menu_language.py` owns the thirteen codes, the language leaf, and the menu words. One class. No second class in that file. The logger arrives through `__init__`. The codes and the leaf stay on `requirement-python-cli-language`.
16. The menu picture stays on `requirement-python-tui`. These classes implement that picture. They do not invent a second layout.
17. Until an implement order lands this split, `cli.py` still holds the prompt session. After the split, `cli.py` **MUST NOT** hold `Tui`, `MenuPainter`, `MenuModel`, `MenuSession`, or `Gui` methods.
17a. Class `Gui` in `src/VideoEditor/gui.py` owns the X11 window in `requirement-python-gui`. One class. `Cli` writes `Gui(...)` and calls `open`. The window does not paint the text-menu frame.

### 2.4 About page and join

18. Class `AboutPage` in `src/VideoEditor/about_page.py` owns `framework_about`, `window_library_lines`, `about_box_lines`, `install_kind`, `install_sentence`, and `_is_source_checkout`. `framework_about` composes the page in `requirement-python-about`. The domain sentence stays on `requirement-domain-videoeditor`. `install_sentence` names GLOBAL, LOCAL, or UNINSTALLED. It **MUST NOT** name `python -m pip install VideoJoin` and **MUST NOT** name a downloaded-script installer. Class `CheckSystem` in `src/VideoEditor/check_system.py` owns the host-check reads, including the pyenv and conda paths. `Cli` writes `CheckSystem(...)` and then `AboutPage(...)`. `AboutPage` calls that object. It **MUST NOT** construct `CheckSystem`. Row 83 and the `about` verb call `framework_about`.
19. Class `Join` in `src/VideoEditor/join.py` owns `discover`, `remaining_after`, `resolve_output_name`, and `run`. `discover` scans the current working directory. `remaining_after` drops the first path. `resolve_output_name` applies the default name and the extension rule. `run` calls the concat pipeline (copy, then fail-closed re-encode, then `shutil.move`). **MUST NOT** add a separate encoder class or a separate file-stage class for this product. Concat order stays on `requirement-video-ffmpeg-pipeline`. Publish stays `shutil.move`.

### 2.5 The other jobs

20. Class `SystemLog` in `src/VideoEditor/system_log.py` owns `log_dir`, `log_files`, `read_log`, `clear_log`, and `folder_text`. The menu rows and the result-page words stay on `requirement-python-tui`. `Tui` writes `SystemLog(...)` at the site that needs it and passes the same logger. `cli.py` **MUST NOT** list the log files, read one, or empty one.
21. Class `SelfManage` in `src/VideoEditor/self_management.py` owns `local_version`, `argv_for`, `run_pip`, and `emit`. `local_version` reads `__version__` and does not call pip. `argv_for` builds the pip argument lists for `version-check`, `self-update`, `self-install`, and `self-uninstall`. The verb names and the command strings stay on `requirement-python-cli-interface` and `requirement-python-tui`. `cli.py` **MUST NOT** build those pip argument lists. The about body is not this class. Verb `setup` is not this class.
22. Version display stays the single string `__version__` in `src/VideoEditor/__init__.py`. **MUST NOT** add a second integer triple.
23. Class `HostSetup` in `src/VideoEditor/host_setup.py` owns `ensure_geteuid`, `argv_pip`, `argv_winget_ffmpeg`, and `run`. `ensure_geteuid` is a static method of that class. The module **MUST NOT** add a second public function beside the class. `def main` calls `HostSetup.ensure_geteuid()` before it imports ChronicleLogger (`requirement-python-cli-logging`). `run` is verb `setup` (`requirement-runtime-prerequisites`). One class in that file.

### 2.6 Implementation Notes (this project)

| Class | File | Owns |
|-------|------|------|
| `Cli` | `src/VideoEditor/cli.py` | Parser, dispatch, verbs, tty checks. Identity constants, verb lists, suffix sets (rule 11f). `def main` stays in this file |
| `Tui` | `src/VideoEditor/tui.py` | Text-menu session (rule 12). Shares the file with `MenuScreenError` |
| `MenuPainter` | `src/VideoEditor/menu_painter.py` | Frame, glyphs, `MENU_ROWS`, `SELF_ROWS`, `LOG_ROWS`, `PATH_LABEL_EN`, `PATH_LABEL_ZH_HANT`, `paint`, `path_label`, `path_line`, `clock_text`, `display_width`, `clip_columns`, `clip_columns_right`. Writes `MenuLanguage(...)` |
| `MenuLanguage` | `src/VideoEditor/menu_language.py` | Thirteen codes, the language leaf, and the menu words |
| `MenuModel` | `src/VideoEditor/menu_model.py` | Keystroke state. Shares the painter’s language object |
| `MenuSession` | `src/VideoEditor/menu_session.py` | `run`, `take_action`, `wait_key`, `leave_to_front` |
| `SystemLog` | `src/VideoEditor/system_log.py` | Log folder, file list, read, empty |
| `SelfManage` | `src/VideoEditor/self_management.py` | Local version and the pip commands for rows 84–87 |
| `CheckSystem` | `src/VideoEditor/check_system.py` | Host-check reads for the about page. Does not draw the star box |
| `AboutPage` | `src/VideoEditor/about_page.py` | `framework_about`, the star box, and the install kind. Calls `CheckSystem` |
| `Join` | `src/VideoEditor/join.py` | Discover, pick, output name, concat call |
| `Gui` | `src/VideoEditor/gui.py` | X11 window. Edit group and Join group. Calls `Join.run` and the edit encoder |
| `HostSetup` | `src/VideoEditor/host_setup.py` | `ensure_geteuid`, the `setup` pip lists, and the Windows FFmpeg winget list |

| Item | Value |
|------|--------|
| **Console script** | `video-join = VideoJoin.cli:main` |
| **Module entry** | `src/VideoEditor/__main__.py` imports `main` from `.cli` |
| **Running tree** | `src/VideoEditor/__init__.py`, `__main__.py`, `cli.py` only. Module-level `APP_NAME`, `CONSOLE_NAME`, `VIDEO_SUFFIXES`, and `OUTPUT_SUFFIXES` still live in `cli.py`. `_PKG_VERSION` still falls back to a second literal. That tree is the running package. It is not the allowed end state |
| **Landed** | `MenuLanguage` is on disk. The running-tree row above is still the open gap. `TP-OOP-01` through `TP-OOP-04` stay todo |
| **Logger** | Every class `__init__` in the map accepts `logger` and stores it. `def main` writes `ChronicleLogger(...)` and then `Cli(logger)`. Collaborators are `OtherClass(...)` at the site that needs them |
| **Not this split** | Menu rows, about line facts, concat order, version string, the wording of the instantiation line |

### 2.7 Why This Requirement Exists (CIAO)

- **Principle 2 – Intentional**: Each job has one class and one file. That class receives the logger in `__init__`.
- **Principle 5 – SSOT**: `cli.py` does not keep a second copy of another class's methods. `main` has one home.
- **Principle 1 – Caution**: The picture, the about facts, and the concat order stay where their requirements already put them. The running tree is not declared illegal before the split lands.

## Under command line for normal user only

On Termux, Git Bash, Windows cmd, or the same class, each class still receives the logger through `__init__` at this login. **This requirement:** do not use administrator privilege, `sudo`, `apt`, or a dedicated system user to construct a class or to pass the logger. Do not pipe a downloaded script into a shell. Type 1 and Type 2 are unused on Termux, Git Bash, and Windows cmd. Git Bash and Windows cmd do not call Termux `pkg`.

## Sample code

StateLogic stays unordered. The site writes the class name. This sample is the allowed end state. The running `cli.py` does not look like this yet.

```python
def main(argv=None, basedir="", logdir=""):
    logger = ChronicleLogger(logname="VideoJoin", is_quiet=opens_text_screen(argv))
    app = Cli(logger)
    return app.run(argv)

class Cli:
    APP_NAME = "VideoJoin"
    CONSOLE_NAME = "video-join"

    def __init__(self, logger=None):
        self.logger = logger
        if logger is not None:
            logger.log_message("instantiated", component="Cli")
        self.tui = Tui(logger)
        self.join = Join(logger)
```

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** Do not treat the running procedural file as the allowed end state, and do not pretend the class files are already on disk.
- **Intentional:** One job, one class, one file. `Join` is one class, not an encoder plus a file stage.
- **Anti-fragile:** `def main` and the console script keep their addresses.
- **Over-protect:** No factory, no second logger, no StateLogic rewrite hidden inside this map.

## 4. Protection Rule (Sacred)

**Future AI assistants or maintainers MUST NOT:**

1. Move `def main` out of `src/VideoEditor/cli.py`.
2. Put two classes in one module, except `MenuScreenError` beside `Tui`.
3. Leave a class that has only one method.
4. Construct ChronicleLogger inside a class.
5. Add a factory whose job is to instantiate a class in this map.
6. Put `MENU_ROWS`, `SELF_ROWS`, `LOG_ROWS`, or frame glyphs on `Cli`.
7. Keep a second version literal on `Cli`.
8. Add an encoder class or a file-stage class for this product.
9. Order a StateLogic + `Attr` rewrite from this file.
10. Mark `TP-OOP-*` have before the class files exist and the proofs pass.
11. Delete the running `cli.py` behavior in a requirement-only edit.

**Violating this rule is a critical structure regression.**

## 5. Acceptance criteria

| ID | Criterion |
|----|-----------|
| AC-1 | The map names `Cli`, `Tui`, `MenuPainter`, `MenuLanguage`, `MenuModel`, `MenuSession`, `SystemLog`, `SelfManage`, `CheckSystem`, `AboutPage`, `Join`, `Gui`, and `HostSetup`, each in its own file |
| AC-2 | `def main` stays in `cli.py`. The console script stays `VideoJoin.cli:main` |
| AC-3 | Every class `__init__` accepts the logger. The site writes `ClassName(...)` |
| AC-4 | `Cli` owns the identity constants. `MenuPainter` owns the row tuples and the glyphs |
| AC-5 | `AboutPage` composes the about page. `CheckSystem` owns the host check. `Join` discovers, picks, names, and calls the pipeline |
| AC-6 | The running tree is still three modules. Proofs stay todo |

## 6. Related requirements (peer keys only)

| Key | Relationship |
|-----|----------------|
| `requirement-python-cli-logging` | Construct, `instantiated` line, quiet. `HostSetup.ensure_geteuid()` before the ChronicleLogger import |
| `requirement-python-tui` | Picture the classes draw |
| `requirement-python-cli-interface` | Verb names `Cli` dispatches |
| `requirement-python-about` | About page line text. This file names `AboutPage` and `CheckSystem` |
| `requirement-domain-videoeditor` | Domain sentence and join steps |
| `requirement-video-ffmpeg-pipeline` | Concat order `Join.run` calls |
| `requirement-python-coding-style` | `shutil.move`. StateLogic stays unordered. Factory ban |
| `requirement-python-project-structure` | Running tree versus this map |
| `requirement-python-packaging` | Console script and `__version__` |
| `requirement-runtime-prerequisites` | Verb `setup` steps. `HostSetup.run` |
| `requirement-class-software-dev` | Residual pointer |
| `docs/requirements/index.md` | Registry |

## Design-time verification

| TP family / ID | Suite | Status | Note |
|----------------|-------|--------|------|
| **TP-OOP-01** | `tests/test_oop.py` | todo | The class files in the map exist. `cli.py` defines `Cli` and `def main` and does not define another class's methods |
| **TP-OOP-02** | `tests/test_oop.py` | todo | Every class `__init__` takes the logger, stores it, and logs `instantiated` |
| **TP-OOP-03** | `tests/test_oop.py` | todo | `MenuPainter` owns the frame glyphs and `MENU_ROWS` / `SELF_ROWS` / `LOG_ROWS`. Those names are absent from `cli.py` |
| **TP-OOP-04** | `tests/test_oop.py` | todo | `APP_NAME`, `CONSOLE_NAME`, `PRODUCT_VERBS`, `LIFECYCLE_VERBS`, `VIDEO_SUFFIXES`, and `OUTPUT_SUFFIXES` are attributes of `Cli`. Display version is `__version__` only |

**Matrix:** `docs/reviews/requirement-test-matrix.md`
**Map:** `docs/reviews/test-plan.md`

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-10-04 | Active 1.0.0 | L2 class map for VideoJoin. Running tree remains three modules. StateLogic unordered. Proofs todo |
| 2026-10-04 | Active 1.0.1 | `MenuPainter` owns `path_label`, `PATH_LABEL_EN`, and `PATH_LABEL_ZH_HANT`. Those methods do not detect a language. `TP-OOP-*` stay todo |
| 2026-10-04 | Active 1.0.2 | Class `MenuLanguage` is the language home. `MenuPainter` writes `MenuLanguage(...)`. `TP-OOP-*` stay todo |
| 2026-10-04 | Active 1.0.3 | `display_width`, `clip_columns`, and `clip_columns_right` are methods of `MenuPainter`. `TP-OOP-*` stay todo |
| 2026-10-04 | Active 1.0.4 | `CheckSystem` owns the host check. `AboutPage` owns `framework_about`. No second version triple. `TP-OOP-*` stay todo |
| 2026-10-10 | Active 1.0.5 | Class `HostSetup` owns `ensure_geteuid` and verb `setup`. `TP-OOP-*` stay todo |
| 2026-10-12 | Active 1.0.6 | Distribution name is VideoEditor. Console script is `video-editor`. Current release string is **1.0.0**. |

---

**Last Updated**: 2026-10-12
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
