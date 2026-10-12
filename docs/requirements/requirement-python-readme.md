**file**: docs/requirements/requirement-python-readme.md
**Status**: Active (Version 1.2.1)
**Area**: python
**Key**: `requirement-python-readme`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

This file owns the product user document at the repository root: which sections it has, which pictures it embeds, and the rule that a sentence in that document matches the requirement that owns the behavior. Project nature is a program a person builds and runs from a terminal. The menu picture stays on `requirement-python-tui`. The thirteen languages stay on `requirement-python-cli-language`. The verbs stay on `requirement-python-cli-interface`. The join stays on `requirement-domain-videoeditor` and `requirement-video-ffmpeg-pipeline`. The prerequisite sentences stay on `requirement-runtime-prerequisites`. The package name and the console script stay on `requirement-python-packaging`. The version string is `__version__`. This file does not restate those bodies.

### 1.1 Human-facing

**In one sentence:** You open the root user document to install the program, read how the window and the menu join two videos or edit one MP4, and see pictures of that window: edit, join, the language list, and self-management.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | The person reading how to run the program | Open `README.md` at the checkout root |
| The other role | The requirements that own the menu, the join, and the package | A sentence here matches those files |
| Not this file | The concat itself, the language file, and the host check | Pipeline, language, and domain |

| Includes | Excludes |
|----------|----------|
| Section order, badges, the Advantages contrast, install sentences, and the picture catalog | A second menu, a second verb list, or a second encode order |
| Absolute `https` image destinations for captures of the running X11 window | A generated drawing that invents control text. A relative `screenshots/` image destination in this package description. A text-menu PNG in `screenshots/` |
| The eight related-project lines | A shell online install, root as the documented path, or a setup script that is not on disk |

| Surface | What you open | What for |
|---------|---------------|----------|
| `README.md` | Root user document | Install, usage, pictures |
| `screenshots/` | Picture folder beside that document | The links in the Screenshots section |
| `video-join` | The program on a terminal | What those pictures show |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Read the install | The public path is pip. The document does not ask for root. | `pip install VideoEditor` |
| Check the pictures | The window pictures are edit, join, the language list, and self-management. The path line names the current directory. A player clock reads `00:00.00`. | `video-editor` on a terminal with `DISPLAY` set |
| Check the version line | The badge matches the package string. | `video-join version` |

## 2. Core Rules / Requirements (Mandatory)

The user document is how a person learns the program. It is not a second copy of product law. A claim in the document matches the requirement that owns that claim.

### 2.1 Where it lives

1. **MUST** keep the user document at the repository-root `README.md`. Product law stays under `docs/requirements/`. The layout rule that the file exists is `requirement-python-project-structure`. This file owns the sections and the pictures.
2. Pictures **MUST** live in a `screenshots/` folder at that same root. The user document **MUST** link every PNG in that folder. This document is the package description. Each image destination **MUST** be an absolute `https` URL that names that PNG on the public source host. A relative `screenshots/<file>` destination fails on the package index: the index fetches that path on its own host, and the picture folder is not in the published archive. The same relative destination still opens on the source forge. A link to a sibling document, such as `LICENSE.md`, **MAY** stay relative. A PNG on disk and absent from `README.md` fails this file. The URL base for this product is in Implementation Notes. That URL does not render on the package index until the file is on the public branch named in the URL.
3. **MUST NOT** freeze a session login or a `/home/<login>/` path in this requirement or in a sentence that is law. A picture may show the directory where that capture was started. The sentence in the document names “the current directory.”

### 2.2 What the document contains

The document **MUST** keep the sections in §2.5, in that order. A new heading, a dropped heading, or a reordered heading is a revision of this file.

Each behavioral sentence **MUST** match its owner and **MUST NOT** restate that owner’s procedure:

| Claim in the document | Owner |
|-----------------------|--------|
| Two-file join, formats, output name, no folder prompt | `requirement-domain-videoeditor` |
| Stream copy, then re-encode, publish with `shutil.move` | `requirement-video-ffmpeg-pipeline` and `requirement-python-coding-style` |
| Menu picture, path row, clock, row numbers | `requirement-python-tui` |
| Thirteen languages and what stays English | `requirement-python-cli-language` |
| Product verbs and pip lifecycle commands | `requirement-python-cli-interface` |
| Empty argv on a terminal opens the menu. Empty argv with no terminal prints help and returns 0. Direct `join` with no terminal exits non-zero | `requirement-python-cli-interface` |
| Package name, console script, pip install | `requirement-python-packaging` |
| Package string on the badge | `__version__` in `src/VideoEditor/__init__.py`, copied by `pyproject.toml` |
| `ChronicleLogger>=1.3.1` | `requirement-python-packaging` and `requirement-runtime-prerequisites` |
| FFmpeg on `PATH`, no root auto-install | `requirement-runtime-prerequisites` |

`--json` is named on the CLI requirement and in the user document. `hello` is a product verb. The user document does not name `./setup.sh` or `./build.sh`.

The text-menu first row in the user document **MUST** name the current directory on the left and a local clock (`HH:MM:SS`) on the right when the row has room. It **MUST NOT** name `Current`, a login, `USER`, `USERNAME`, or `getpass` as that right-hand field. The window path line **MUST** name the current directory and **MUST NOT** put that clock on the path line. A player clock in the window **MUST** be named `00:00.00` (`MM:SS.CC`). The text-menu path row stays on `requirement-python-tui`. The window picture stays on `requirement-python-gui`.

### 2.3 Pictures

1. A window picture **MUST** be a capture of the running X11 window. **MUST NOT** satisfy a window control with a drawing that invents its text. Every PNG in `screenshots/` **MUST** be linked from the user document. `screenshots/` **MUST** contain only those window captures. A text-menu board **MUST NOT** be stored there.
2. The Screenshots section **MUST** show edit, then join, then the language list, then self-management, in that order, and then no further PNG.
3. The pictured edit **MUST** show one source player and one generated player. The pictured join **MUST** show two source players and one generated player. The generated player **MUST** be empty in those captures, with Play and Stop disabled, because Run has not finished a file. The domain file owns the output-name pattern. This file owns that those two jobs are the pictured ones.
4. The language picture **MUST** show rows 41 through 53. The self-management picture **MUST** show rows 82 through 87. The header on a capture follows the saved menu language. The about page stays English and is not one of these four files. That split is `requirement-python-cli-language` and `requirement-python-about`.
5. A live-window capture satisfies this file when it shows the window the program paints, including the player clock `00:00.00` and a path line that names the current directory.
6. The heading of each picture **MUST** be that file’s basename. The paragraph and the image alt **MUST** be the catalog cells for that file. Those words come from the basename and from what the picture shows. A sentence that only says the file is a picture fails this file. The paragraph **MUST NOT** freeze a session login or a `/home/<login>/` path. The path line is “the current directory.”

### 2.4 Install honesty

1. The public install path **MUST** be pip. **MUST NOT** document a shell online install, `sudo pip`, or `sudo curl | sh`.
2. **MUST NOT** name a checkout setup script that is not on disk. This tree has no `setup.sh`. The document **MUST NOT** name `setup.sh`.
3. The document does not show a wheel or sdist example. **MUST NOT** add one unless the basename is the file the build writes and the version token matches the package version.
4. The prerequisite sentences **MUST** stay aligned with `requirement-runtime-prerequisites`. This file **MUST NOT** copy that table as a second owner.
5. **MUST NOT** add `./build.sh` verbs to the user document. Those verbs are not `video-join` verbs.

### 2.5 Implementation Notes (this project)

| Field | Value |
|-------|--------|
| **Document** | `README.md` |
| **Pictures** | `screenshots/` |
| **Package** | `VideoEditor` |
| **Console scripts** | `video-editor`, plus aliases `video-join` and `video-speed` |
| **Version** | `1.0.0` from `src/VideoEditor/__init__.py` (`__version__`). `pyproject.toml` copies that string |
| **Python** | `>=3.11`. The badge says 3.11+ |
| **License file** | `LICENSE.md` (MIT). The file is present. The document link stays relative |
| **Homes** | Product home `https://github.com/cloudgen/VideoEditor`. SSH remote `git@github.com:cloudgen/VideoEditor.git` |
| **Pictured edit** | One MP4 source. Cut `00:00.00` to `00:18.04`. Percent 100. Looping switch None is on. Output name ends `_cut0.0-18.0s_100pct.mp4`. Generated player empty. Process bar reads 處理 0% |
| **Pictured join** | Two sources. Output name `video-1 + video-2.mp4`. Generated player empty |
| **Every PNG** | `gui-edit.png`, `gui-join.png`, `gui-language.png`, `gui-self-management.png`. No other PNG in `screenshots/` |
| **Image URL** | `https://raw.githubusercontent.com/cloudgen/VideoEditor/main/screenshots/<basename>`. The package index can fetch that file only after it is on that public branch |

**Title:** `VideoEditor - Join two local videos, and cut, speed, or boomerang an MP4`.

**Badges:** a Version badge whose token is the package string; License MIT; CIAO linked to `https://github.com/cloudgen/ciao`; stars for `cloudgen/VideoEditor`; Python 3.11+; PyPI `VideoEditor` linked to `https://pypi.org/project/VideoEditor/`.

**Opening:** concatenate two videos in the current directory, and cut, speed, or boomerang an MP4. Prefer stream copy for join. Re-encode when copy fails. Publish with `shutil.move`. On a terminal with `DISPLAY` set and no arguments, the X11 window opens. With no display, the text menu opens. Neither starts join or edit by itself, and neither calls pip.

**Sections, in order.** Advantages is inserted after Features. Screenshots is inserted after Usage. The other headings keep the existing kit order.

| Heading | What this document must keep | Owner of the behavior |
|---------|------------------------------|------------------------|
| Features | Text menu: join **1**, edit **2**, system-log **3**, language **4**, self-management **8**, Exit **9**. Text-menu path and a local clock on the first row. Window path line is the current directory. Player clock `00:00.00`. Two files in the current directory. Stream copy, then re-encode. Edit is cut, speed, and optional boomerang or repeat. `shutil.move`. FFmpeg on `PATH`. Verbs `help`, `version`, `about`, `hello`, `tui`, `join`, `list-videos`, `edit`, `list-mp4`, `self-install`, `version-check`, `self-update`, `self-uninstall`, `setup` | Peers in §2.2. The clock sentences are §2.2 |
| Advantages | The four parts and the comparison table below | This file for the contrast. Peers in §2.2 for the behavior |
| Quick Installation | FFmpeg on `PATH`. `ChronicleLogger>=1.3.1` and `opencv-python-headless>=5.0.0.93`. `pip install VideoEditor`. Checkout uses a venv and `pip install -e .`. The fenced text menu includes row 2 edit | `requirement-runtime-prerequisites`, `requirement-python-packaging`, `requirement-python-tui` |
| Usage | Menu versus typed verbs. Join asks for two indexes and an output name. No folder prompt on join. Edit asks folder then file, or takes `--file`, `--start`, and `--end`. Esc returns. No terminal: empty argv prints help and returns 0. Direct `join` with no terminal exits non-zero. `self-uninstall` needs `--force`. No sudo | `requirement-python-cli-interface`, `requirement-domain-videoeditor`, `requirement-python-tui` |
| Screenshots | Lead: each heading is the file name, and the paragraph is what that picture shows. Package **1.0.0**. The four window captures and the catalog below. The header follows the saved language | This file |
| Examples | `cd` to a folder of clips, then `video-editor`, then `video-editor version`, then `video-editor join`. An edit example names `--file`, `--start`, and `--end` | `requirement-domain-videoeditor` |
| Platform Compatibility | Linux primary. macOS and Windows when Python and FFmpeg are present. `video-editor setup` installs the declared pip libraries. On Windows it also tries curses and FFmpeg. The picture window still needs `DISPLAY` and the host GTK 4 and GStreamer packages. The text menu needs a terminal and the curses module. A Python that cannot import curses still runs `about`, `version`, `help`, and `hello` | `requirement-runtime-prerequisites`, `requirement-python-tui` |
| Related Projects | The eight lines below, in that order, each with one sentence | This file |
| Contributing | Keep product law in sync. Do not strip `shutil.move`. Version strings stay together | `requirement-python-coding-style`, `requirement-python-packaging` |
| License | MIT, link `LICENSE.md`, and that file exists | `requirement-python-packaging` |
| Last Update | The latest line names package **1.0.0** and the X11 window. The **1.1.0** line stays as history | This file for the line. `__version__` for the string |

**Related projects, in this order.** The URLs stay in this order. VideoJoin and VideoSpeed are the two products this package combines. Each line is one sentence. Do not add an install recipe.

| Order | Link | Sentence |
|------:|------|----------|
| 1 | `https://github.com/Wilgat/VideoJoin` | Join architecture this package keeps |
| 2 | `https://pypi.org/project/VideoJoin/` | The join product on PyPI |
| 3 | `https://github.com/Wilgat/AnimeDlp` | Command-line downloader for anime video sites |
| 4 | `https://github.com/Wilgat/ChronicleLogger` | Status logger this program depends on (`ChronicleLogger>=1.3.1`) |
| 5 | `https://github.com/Wilgat/VideoSpeed` | Edit steps this package also keeps |
| 6 | `https://github.com/cloudgen/ciao` | Caution, Intentional, Anti-fragile, Over-engineered |
| 7 | `https://github.com/cloudgen/ciao-lite` | Short agent contract |
| 8 | `https://github.com/cloudgen/safe-rm` | Guarded `rm` |

**Advantages, after Features and before Quick Installation.** Four parts, then the comparison. The text-menu path row names the local clock. The window path line names the current directory. A player clock is `00:00.00`.

1. **Dual-mode interface.** The menu asks for two indexes and an output name on join, and for a folder, a file, a cut, a length percent, and a tail of none, boomerang, or repeat on edit. A typed verb asks the same questions. Join tries stream copy, then re-encodes if copy fails. Edit accepts `--file`, `--start`, and `--end`. `--json` prints one object and does not open the menu. With no arguments on a terminal, the text menu opens. With no terminal and no verb, the program prints help and returns 0. Direct `join` with no terminal exits non-zero.
2. **Built-in languages.** Row **4** lists thirteen languages: English, Simplified Chinese, Traditional Chinese, Spanish, Arabic, French, Portuguese, Russian, German, Japanese, Korean, Dutch, and Greek. The choice is saved for the next run.
3. **USB-safe staging.** Intermediate files are written beside the output when that folder can be written, including on a removable drive. The finished file is published with `shutil.move`. When that folder cannot be written, the stage uses the system temporary directory. The section **MUST NOT** say the stage never uses that directory.
4. **Lifecycle and diagnostics.** `version-check`, `self-update`, `self-install`, and `self-uninstall` are menu rows **84**–**87** and typed verbs. `self-uninstall` on the command line needs `--force`. They call pip and do not use root. **system-log** (**3**) views a log, clears a log, and shows the log folder. **about** (**83**) stays in English.

**Comparison table.** Columns: Feature, Raw FFmpeg CLI, Typical Python wrappers (moviepy), VideoEditor.

| Feature | Raw FFmpeg CLI | Typical Python wrappers (moviepy) | VideoEditor |
|---------|----------------|-----------------------------------|-----------|
| Learning curve | A concat or filter graph the person writes | A Python script | Text menu, or two file numbers and an output name, or edit flags |
| Non-interactive | Native command line | A custom script | Typed verbs. No terminal and no verb: help, return 0. Direct `join` with no terminal: non-zero. `--json` for an edit job or for help |
| Menu languages | None | None | Thirteen, kept for the next run |
| Temporary files | You choose the paths | Often the system temporary directory | Beside the output when that folder can be written. Otherwise the system temporary directory. Publish with `shutil.move` |
| Self-management | The system package manager | pip from outside the tool | Built-in version-check, self-update, self-install, and self-uninstall |
| Diagnostics and logs | The encode stream | A logging setup in the script | system-log (row 3) and about (83), in English |

**Screenshot catalog, in this order.** Each image destination is the absolute `https` URL in Implementation Notes, with that file’s basename. The paragraph and the alt are the words `README.md` prints for that file. The header on these captures is Traditional Chinese because that was the saved menu language. The paragraph names the English control beside the word on the screen. It does not freeze a login or a home path.

| Order | File | Paragraph | Alt |
|------:|------|-----------|-----|
| 1 | `gui-edit.png` | Edit is the group on screen. The window title is VideoEditor 1.0.0. The edit tab is highlighted and shares the group's left edge. A framed line under the header shows 專案根目錄 (Project Root) and the current directory. 輸入影片 (Input Video) holds one MP4, 選擇檔案 (Select file), and a player at `00:00.00` of `00:18.04`. A thumbnail strip sits under that picture. 剪輯控制 (Edit Controls) has 開始 (Start), 暫停 (Pause), 停止 (Stop), a jump field showing `00:00.00`, and 前往 (Go To). 起點 (Start) is `00:00.00` with 標記起點 (Mark start). 終點 (End) is `00:18.04` with 標記終點 (Mark end). 百分比 (Percent) is 100. 循環選項 (Looping Options) has 無 (None) on, and 迴旋 (Boomerang) and 重複 (Repeat) off. The output name is `video-1_cut0.0-18.0s_100pct.mp4`. 執行 (Run) has not been pressed. 輸出與結果 (Output & Result) shows that name. 已產生 (Generated) is empty. 結果影片 (Resulting Video) is empty, shows `00:00.00` of `00:00.00`, and its 播放 (Play) and 停止 (Stop) are disabled. The bottom bar reads 處理 0% (Process 0%). | Edit group, Traditional Chinese labels, generated player empty |
| 2 | `gui-join.png` | Join is the group on screen. The join tab is highlighted and shares the group's left edge. The same header, project-root line, and 處理 0% bar are on screen. 影片 1 (Video 1) and 影片 2 (Video 2) are loaded. The first player shows `00:00.00` of `00:18.04`. The second shows `00:00.00` of `00:12.04`. A thumbnail strip sits under each source picture. Each source has 播放 (Play) and 停止 (Stop). 輸出名稱 (Output name) is `video-1 + video-2.mp4`. The write line names the current directory and that file. 執行 (Run) has not been pressed. 已產生 (Generated) is empty. 結果影片 (Resulting Video) is empty, shows `00:00.00` of `00:00.00`, and its Play and Stop are disabled. | Join group, two source players, generated player empty |
| 3 | `gui-language.png` | The language page lists the thirteen menu languages. The header stays in the saved language. join and edit stay above the list and neither is highlighted. The rows are 41 English, 42 简体中文, 43 繁體中文, 44 Español, 45 العربية, 46 Français, 47 Português, 48 Русский, 49 Deutsch, 50 日本語, 51 한국어, 52 Nederlands, and 53 Ελληνικά. The project-root line names the current directory. The bottom bar reads 處理 0% (Process 0%). Choosing a row saves that language for the next window and for the text menu. | Language list, 41 English through 53 Greek |
| 4 | `gui-self-management.png` | Self-management shows the numbered actions and no extra page under them. The buttons are 82 version, 83 about, 84 version-check, 85 self-update, 86 self-uninstall, and 87 self-install. The header stays in the saved language. join and edit stay above the buttons and neither is highlighted. The project-root line names the current directory. The bottom bar reads 處理 0% (Process 0%). 83 about opens the English about page. The pip rows call pip and do not use root. `self-uninstall` on the command line needs `--force`. | Self-management, rows 82 through 87 |

`TP-DOC-01` asserts the Version badge token, that the four window PNGs are the only files in `screenshots/` and that each is linked with the absolute `https` URL above, that no markdown image uses a relative `screenshots/` destination, that the section headings are present, that the document does not name `setup.sh`, that the eight related-project URLs are in order, that the text-menu path row names the local clock, that a player clock is `00:00.00`, and that `video.png` is absent. `TP-DOC-03` asserts that each screenshot paragraph and alt equals the catalog cell, and it does not claim a pixel-by-pixel proof. `TP-DOC-03` stays **todo**. Map: `docs/reviews/test-plan.md`.

### 2.6 Why This Requirement Exists (Direct CIAO Alignment)

- **CIAO Principle 2 – Intentional** (https://github.com/cloudgen/ciao): The sections and every PNG in `screenshots/` are a named catalog. A later edit cannot drop a window capture, leave a PNG unlinked, or swap in a drawing for a control.
- **CIAO Principle 5 – SSOT** (https://github.com/cloudgen/ciao): This file owns the document. Behavior stays on the peer that already owns it.
- **CIAO Principle 16 – Interactive** (https://github.com/cloudgen/ciao): The pictures show the X11 window a person actually drives: edit, join, the language list, and self-management.
- **CIAO Principle 21 – Dual policies** (https://github.com/cloudgen/ciao): The portable rule is “the document matches its owner.” The VideoEditor headings and file names live in §2.5.
- **CIAO Principle 4 – Over-protect** (https://github.com/cloudgen/ciao): Do not publish a setup script that is not on disk, or a success line the program did not print.

## Under command line for normal user only

The documented install is for this login. **This requirement:** the user document **MUST NOT** tell the reader to use `sudo`, `sudo pip`, `sudo curl | sh`, or a dedicated system account. Git Bash and Windows cmd **MUST NOT** be told to invoke Termux `pkg`. The public install path is pip. A picture does not change who may run a verb.

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** An install sentence that names a missing script is a defect.
- **Intentional:** An Advantages section, four window pictures, one pictured edit, one pictured join, one section order. Each picture paragraph is the catalog cell for that file.
- **Anti-fragile:** A new PNG in `screenshots/` becomes a required link in the same change. A non-menu file stays labeled as itself.
- **Over-protect (Principle 20):** Do not let the user document become a second menu, a second verb list, or a second encode procedure.

## 4. Protection Rule (Sacred)

**Future AI assistants or maintainers MUST NOT**:

- Restate encode order, verb lists, menu numbers, language codes, or the prerequisite table in this file as a second procedure.
- Turn the Advantages section into an FFmpeg filter recipe. The concat graph may be named only as something the person does not write.
- Claim that intermediate files never use the system temporary directory.
- Replace a capture with a drawing that invents row text.
- Leave any PNG in `screenshots/` out of `README.md`.
- Use a relative `screenshots/` destination for a picture in this package description. The package index cannot fetch that path. A sibling-document link such as `LICENSE.md` may stay relative.
- Put a text-menu board or `video.png` in `screenshots/`. The picture folder is the window.
- Caption a picture with only a language name, or with a sentence that does not say what the picture shows.
- Describe the path row’s right side as `Current` or a login.
- Name `./setup.sh` while that file is absent.
- Add `./build.sh` verbs, a shell online install, `sudo pip`, or `sudo curl | sh` to the user document.
- Add `--json`, a length percent, a boomerang, or a folder prompt.
- Freeze a session login or a `/home/<login>/` path in this file.
- Mark `TP-DOC-03` have before the suite asserts that each catalog paragraph and alt equals the cell in §2.5.
- Treat `./build.sh` verbs as `video-join` verbs.

## 5. Definition of done

1. `README.md` has the sections in §2.5, in that order, including Advantages after Features and Screenshots after Usage.
2. The Version badge token matches the package string.
3. The Screenshots section links every PNG in `screenshots/`, in catalog order: `gui-edit.png`, `gui-join.png`, `gui-language.png`, `gui-self-management.png`. Each image destination is an absolute `https` URL. Each heading is the basename. Each paragraph and each image alt are the catalog cells for that file.
4. The text-menu path-row sentence names the local clock. The window player clock is `00:00.00`.
5. The document does not name `setup.sh`, `sudo pip`, or a shell online install.
6. Related Projects lists the eight URLs in §2.5, in that order.
7. `TP-DOC-01` is **have** in `tests/test_docs.py` (`./tests/run.sh`, 7 tests, OK). `TP-DOC-03` stays **todo** until the suite asserts that each paragraph and alt equals the catalog cell.

### Design-time verification

| TP family / ID | Suite | Status |
|----------------|-------|--------|
| **TP-DOC-01** Version badge matches the package string. The four window PNGs use the absolute `https` URL and are the only files in `screenshots/`. No relative `screenshots/` image. Section headings. No `setup.sh`. Eight related-project URLs in order. The text-menu path row names the local clock. A player clock is `00:00.00`. `video.png` is absent | `tests/test_docs.py` | have |
| **TP-DOC-03** Each screenshot paragraph and alt equals the catalog cell in §2.5 | `tests/test_docs.py` | todo |

## 6. Related requirements (peer keys only)

| Key | Relationship |
|-----|----------------|
| `docs/requirements/index.md` | Registry |
| `requirement-python-project-structure` | Root `README.md` exists. Sections and pictures are this file |
| `requirement-domain-videoeditor` | Domain rows inside the user document |
| `requirement-video-ffmpeg-pipeline` | Stream copy, then re-encode. This file does not restate that procedure |
| `requirement-runtime-prerequisites` | FFmpeg on `PATH`. No root auto-install |
| `requirement-python-packaging` | Package name, console script, pip install, `ChronicleLogger>=1.3.1` |
| `requirement-python-tui` | Menu picture and the clock |
| `requirement-python-about` | The about picture. This file does not own the page |
| `requirement-python-cli-language` | Row **4** and the thirteen codes. About stays English |
| `requirement-python-cli-interface` | Product verbs the document lists. `hello` is one of them |
| `requirement-python-coding-style` | `shutil.move` for the published file |
| `requirement-class-software-dev` | Class residual |
| `README.md` | The user document |
| `screenshots/` | The captures |
| `docs/reviews/test-plan.md` | `TP-DOC-01` and `TP-DOC-03` |

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
| 2026-10-04 | Active 1.0.0 | User-document sections, Advantages, eight related projects, and twenty-two pictures. Image destinations are absolute `https`. `TP-DOC-01` have. `TP-DOC-03` todo |
| 2026-10-04 | Active 1.0.1 | About and self-management pictures match the new page. Other menu pictures still show **1.0.4**. Package string is **1.0.5** |
| 2026-10-10 | Active 1.0.2 | The verb list names `setup`. Platform Compatibility names `video-editor setup`. The picture window still needs `DISPLAY` |
| 2026-10-10 | Active 1.1.0 | Public home is `cloudgen/VideoEditor`. `screenshots/` is the four X11 window captures. The text-menu clock stays `HH:MM:SS`. The player clock is `00:00.00` |
| 2026-10-11 | Active 1.2.0 | Package string is **2.0.0**. The catalog matches the recaptured window: project root, cards, looping switches, and Process 0% before Run. `TP-DOC-03` stays todo. Terminologies copies the picture-window term and the ship-version term |
| 2026-10-12 | Active 1.2.1 | Distribution name is VideoEditor. Console script is `video-editor`. Current release string is **1.0.0**. |

---

**Last Updated**: 2026-10-12
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
