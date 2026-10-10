**file**: docs/requirements/requirement-domain-videotools.md
**Status**: Active (Version 1.0.0)
**Area**: domain
**Key**: `requirement-domain-videotools`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

This requirement is the domain surface Single Source of Truth for VideoTools: the join steps inherited from the VideoJoin architecture, the edit steps added from VideoSpeed, and how help and about describe both.

Operational FFmpeg processing is owned by `requirement-video-ffmpeg-pipeline`. Typed verbs, empty argv, and `--json` routing are owned by `requirement-python-cli-interface`. The screen is owned by `requirement-python-tui`. Class homes are `requirement-python-oop`.

This file is the sole Active `requirement-domain-*`. It supersedes `requirement-domain-videojoin` on this workspace. Headings and pictures in the root user document are `requirement-python-readme`. Domain rows stay in this file.

### 1.1 Human-facing

**In one sentence:** VideoTools joins two videos in the current folder, and it can cut, speed, or boomerang one MP4.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | Person joining two local videos, or cutting one MP4 | `video-tools join` or `video-tools edit --file clip.mp4 --start 1 --end 5` |
| The other role | The menu, FFmpeg, and the OpenCV duration probe | `requirement-python-tui`, `requirement-video-ffmpeg-pipeline` |
| Not this file | The rounded menu frame, pip install, and the log folder | TUI, packaging, and logging requirements |

| Includes | Excludes |
|----------|----------|
| Two-file join in the current folder. Formats `.mp4` `.mov` `.mkv` `.avi` `.m4v`. No folder prompt | Joining more than two files, a recursive join scan, cut or speed inside `join` |
| Edit of one MP4: folder, then file, cut, length percent 20–200, one tail (none, boomerang, or repeat) | Non-MP4 as an edit input, a multi-file edit queue |
| `list-videos` and `list-mp4` as typed lists. Neither encodes | A front-board row for either list |
| Help and about as real pages | A downloaded-script installer on the about page |

| Surface | What you open | What for |
|---------|---------------|----------|
| `video-tools join` | Join questions on a terminal | First video, second video, output name |
| `video-tools list-videos` | Name list | Eligible files in this folder. No concat |
| `video-tools edit` | Folder, then file, then cut, percent, tail | One MP4 beside the source |
| `video-tools list-mp4` | MP4 list | Recursive MP4 names. No encode |
| `video-tools about` | About page | Name, version, both jobs, FFmpeg, OpenCV, how to start it |
| `video-tools help` | Help page | The same capabilities, including what join does not do |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Join two videos | Pick the first index, then the second from the list that remains, then the output name. Empty name uses the two file stems. The scan is this folder only. | `video-tools join` |
| See what can be joined | The program lists `.mp4`, `.mov`, `.mkv`, `.avi`, and `.m4v` in this folder and stops. | `video-tools list-videos` |
| Cut and speed one file | Pick a folder, then one MP4, then start, end, length percent, and one tail. Flags can name the whole job. | `video-tools edit --file clip.mp4 --start 1 --end 5 --percent 50` |
| See MP4 files | The program lists MP4 files under the folder and stops. | `video-tools list-mp4` |
| Read about | You see VideoTools, the package version, both jobs, FFmpeg and OpenCV, and the ways to start the program. | `video-tools about` |

## 2. Core Rules / Requirements (Mandatory)

### 2.1 Pillar A — Specialized CLI surface (workflow steps)

Two workflows. Empty argv does not start either one. On a terminal the text screen asks the questions in the bottom box.

#### Join (current folder only)

| Step ID | User action | Inputs | Output / effect | Ops SSOT |
|---------|-------------|--------|-----------------|----------|
| J-01 | Discover videos | scan the current working directory only | Sorted eligible video list | domain + `Join.discover` |
| J-02 | Choose first video | 1-based index into the list | Chosen `Path` for the first input | domain + TUI |
| J-03 | Choose second video | 1-based index into the remaining list (first removed) | Chosen `Path` for the second input. **MUST NOT** allow the same path twice | domain + TUI |
| J-04 | Choose output name | free string; empty → default pattern | Final output filename | domain + pipeline |
| J-05 | Join | two source paths + output name | Concat via FFmpeg (copy first, re-encode fallback) | `requirement-video-ffmpeg-pipeline` |
| J-06 | Report result | — | Success or failure message. Temps cleaned | error peer + pipeline |

**Join routing:** `video-tools join` and front-board row **1** **MUST** reach J-01. Bare `video-tools` on a terminal opens the front board and **MUST NOT** start J-01. `video-tools list-videos` lists the J-01 names and **MUST NOT** continue to J-02. Join **MUST NOT** ask for a folder.

#### Edit (folder, then file)

| Step ID | User action | Inputs | Output / effect | Ops SSOT |
|---------|-------------|--------|-----------------|----------|
| E-01 | Select source folder | path string; empty → current directory | Recursive MP4 list | domain + `EditWalk` |
| E-02 | Select video | 1-based index into that MP4 list | Chosen `Path` to the source | domain + TUI |
| E-03 | Show duration | — | Human duration from the OpenCV probe | domain + `MediaInfo` |
| E-04 | Cut segment | start seconds, end seconds | Bounds validated; feed pipeline | `requirement-video-ffmpeg-pipeline` |
| E-05 | Speed / length percent | percent number; empty or omitted → 100; allowed 20–200 | Feed pipeline | `requirement-video-ffmpeg-pipeline` |
| E-06 | One tail | `none`, `boomerang`, or `repeat`; empty → none | Feed pipeline. Boomerang appends the reverse. Repeat appends the forward clip once | `requirement-video-ffmpeg-pipeline` |
| E-07 | Write result | derived filename | Final MP4 beside the source | `requirement-video-ffmpeg-pipeline` |
| E-08 | Again | y/n | Loop from E-04, or return. This is another job. It is not the tail named repeat | CLI + TUI |

**Edit routing:** Front-board row **2** and the verb `edit` **MUST** reach E-01 when the folder and file are not already named. `list-mp4` runs E-01 and stops. It shows the MP4 list. It does not choose one file and it does not encode. On a terminal, `edit` asks for the folder first, then for the file. A complete non-interactive job is `edit` with `--file`, `--start`, and `--end` (percent defaults to 100, tail defaults to none). The same complete job with no verb and those selectors **MUST** encode and **MUST NOT** open the menu. `--percent`, `--boomerang`, or `--repeat` without a complete file, start, and end **MUST** fail closed. `--boomerang` and `--repeat` together **MUST** fail closed.

**Job flags (also named on `requirement-python-cli-interface`):** `--file`, `--folder`, `--start`, `--end`, `--percent`, `--boomerang`, `--repeat`.

**Output switch (not a domain step):** `--json`, owned by `requirement-python-cli-interface`. It does not add a cut, a percent, or a tail.

**Console names:** `video-tools` is the primary script. `video-join` and `video-speed` call the same entry. Samples in this file use `video-tools`.

**Non-goals (unless a later requirement adds them):** join more than two files, a recursive join scan, a folder prompt on the text-menu join, cut or speed or boomerang inside join, non-MP4 as an edit input, a multi-file edit queue, cloud upload, timeline multi-track editor, automatic color grade, a shell installer, a Control-C confirm question. The X11 window is `requirement-python-gui`. It is not a timeline editor. The `join` verb and the text menu still pick two files from the current folder.

Complete invocation samples this pillar owns:

```text
video-tools join
video-tools list-videos
video-tools edit --file clip.mp4 --start 1 --end 5 --percent 100
video-tools edit --file clip.mp4 --start 1 --end 5 --percent 50 --boomerang
video-tools edit --file clip.mp4 --start 1 --end 5 --percent 50 --repeat
video-tools list-mp4
```

`video-tools join` on a terminal asks for the first index, the second index from the remaining list, and the output name. With no terminal, `join` exits non-zero and `list-videos` prints the names and returns 0 (`requirement-python-cli-interface`).

Those edit commands write `clip_cut1.0-5.0s_100pct.mp4`, `clip_cut1.0-5.0s_50pct_BOOMERANG.mp4`, and `clip_cut1.0-5.0s_50pct_REPEAT.mp4` beside the source.

```python
name = "{0}_cut{1:.1f}-{2:.1f}s_{3:d}pct".format(stem, start, end, int(percent))
if tail == "boomerang":
    name += "_BOOMERANG"
elif tail == "repeat":
    name += "_REPEAT"
name += ".mp4"
```

### 2.2 Pillar B — Specialized features (surface map)

| Feature area | Domain role | Full law |
|--------------|-------------|----------|
| Join discovery (cwd, case-insensitive suffixes) | Expose the list for selection and for `list-videos` | this file |
| Two-file selection without duplicates | First index, then second from the remaining list | this file + TUI |
| Join output naming | Default `{stem1} + {stem2}.mp4`. Append `.mp4` when the extension is not in the allowed set | this file |
| Lossless join when possible | Prefer stream copy | `requirement-video-ffmpeg-pipeline` |
| Compatible re-encode fallback | When concat-copy fails | `requirement-video-ffmpeg-pipeline` |
| MP4 discovery for edit (recursive `*.mp4` / `*.MP4`) | Expose the list for selection and for `list-mp4` | this file |
| Duration probe | Show length before the cut | OpenCV via `MediaInfo`; fail closed on unreadable media |
| Segment cut | User-defined start and end in seconds | `requirement-video-ffmpeg-pipeline` |
| Playback length percent | User percent, range 20–200, default 100 | `requirement-video-ffmpeg-pipeline` |
| Boomerang (forward + reverse) | One tail. Exclusive with repeat | `requirement-video-ffmpeg-pipeline` |
| Repeat (forward + forward) | One tail. The clip plays twice. Exclusive with boomerang | `requirement-video-ffmpeg-pipeline` |
| Edit output naming | `{stem}_cut{start:.1f}-{end:.1f}s_{int(ratio)}pct[_BOOMERANG|_REPEAT].mp4` beside the source | this file + pipeline |
| Wait line | While the edit encode runs, the operator sees `please wait for time consuming process` | `requirement-video-ffmpeg-pipeline` |
| FFmpeg presence | Fail closed when `join` or `edit` encodes and FFmpeg is missing. The front board may still open | `requirement-runtime-prerequisites` |

Domain **MUST NOT** restate full FFmpeg command graphs. Pointers and the feature catalog only.

### 2.3 Pillar C — Specialized project help items

`video-tools help` and `python -m VideoTools --help` **MUST** list the capabilities and the non-goals in this file. Help is a typed verb. It is not a numbered menu row.

The help page **MUST** include:

| Help row | Text intent |
|----------|-------------|
| Working directory for join | Videos must be in the current folder. The join scan is not recursive. Join does not ask for a folder |
| Join formats | `.mp4`, `.mov`, `.mkv`, `.avi`, `.m4v` |
| Join selection | First video, then second video. The second list excludes the first |
| Join output | Default `{name1} + {name2}.mp4` |
| Join list | `list-videos` lists those files and does not join |
| Join quality | Stream copy first. Re-encode fallback if needed |
| Edit | Folder, then file. Cut start and end in seconds. Length percent default 100, allowed 20–200. Tail is none, boomerang, or repeat. Empty means none |
| Edit input | MP4. A script passes `edit --file`, `--start`, and `--end` |
| Edit list | `list-mp4` lists MP4 files and does not encode |
| Edit output | Written next to the source with the cut, percent, and optional `_BOOMERANG` or `_REPEAT` name |
| Flags | `--file`, `--folder`, `--start`, `--end`, `--percent`, `--boomerang`, `--repeat` |
| JSON | `--json` prints one object and does not open the text menu |
| Prerequisite | FFmpeg on PATH for a join or an encode. OpenCV is the duration probe. The menu can open without FFmpeg |
| Menu | On a terminal, `video-tools` with no words shows the front board. Row 1 is join. Row 2 is edit |
| Split | This product does not cut, speed, or boomerang inside join |
| Aliases | `video-join` and `video-speed` call this same program |

Root `README.md` domain rows **MUST** match this catalog.

### 2.4 Pillar D — Specialized project about items

The domain sentence on the about page is this pillar. The page, the host check, and the star box are `requirement-python-about`. `video-tools about` and text-menu row 83 show that page. Class `AboutPage` composes it (`requirement-python-oop`).

| Field | Content |
|-------|---------|
| Product name | VideoTools |
| Version | `__version__`, the same string as `pyproject.toml` (current `1.1.0`) |
| Domain summary | Concatenate two local videos, and cut, speed, or boomerang an MP4 |
| Runtime tools | FFmpeg (copy, re-encode, cut, speed); OpenCV (duration) |
| Entry points | `video-tools`, `video-join`, `video-speed`, `python -m VideoTools` |

The page **MUST** use that domain sentence. About is not a remote version check. It **MUST NOT** advertise a shell `curl|sh` installer. It **MUST NOT** claim pip installs FFmpeg. Pip install stays on rows 84–87.

Complete invocation samples:

```text
video-tools about
video-tools help
```

### 2.5 Implementation Notes (this project)

| Item | Value |
|------|--------|
| **Product / package name** | `VideoTools` |
| **Primary console script** | `video-tools` |
| **Alias console scripts** | `video-join`, `video-speed` (same `VideoTools.cli:main`) |
| **Join class** | `Join` in `src/VideoTools/join.py` |
| **Edit classes** | `EditWalk` in `src/VideoTools/edit_walk.py`, `Encoder` in `src/VideoTools/encoder.py`, `FileStage` in `src/VideoTools/file_stage.py`, `MediaInfo` in `src/VideoTools/media_info.py`, `RunOutput` in `src/VideoTools/run_output.py` |
| **About composer** | `AboutPage` in `src/VideoTools/about_page.py` |
| **Entry** | `src/VideoTools/cli.py` |
| **VERSION** | `1.1.0` (`__init__.py` and `pyproject.toml`) |
| **Join input formats** | `.mp4`, `.mov`, `.mkv`, `.avi`, `.m4v` (suffix match, case-insensitive) |
| **Join scan** | Current working directory only. Not recursive. No folder prompt |
| **Join output default** | `{vid1.stem} + {vid2.stem}.mp4` |
| **Join output extension** | If the name does not end with `.mp4`, `.mkv`, or `.mov` (case-insensitive), append `.mp4` |
| **Edit input** | MP4 only (`*.mp4`, `*.MP4`), recursive under the selected folder |
| **Edit percent** | 20–200 inclusive. Default 100 |
| **Edit output** | Same directory as the source. Pattern in pillar A |
| **Ops SSOT** | `requirement-video-ffmpeg-pipeline` |
| **CLI SSOT** | `requirement-python-cli-interface` |
| **Screen** | `requirement-python-tui`. Questions stay in the bottom box |
| **User docs** | Root `README.md` lists both jobs, row 2, and the verb union |

### 2.6 Why This Requirement Exists (CIAO)

- **Principle 2 – Intentional**: Join and edit stay two workflows. Empty argv starts neither.
- **Principle 5 – SSOT**: One Active domain file for both catalogs.
- **Principle 1 – Caution**: Join still has no folder prompt and no N-file batch. Edit does not run inside join.

## Under command line for normal user only

On Termux, Git Bash, Windows cmd, or the same class, join, list-videos, edit, and list-mp4 run as the normal user. **This requirement:** do not use administrator privilege, `sudo`, `apt`, or a dedicated system user to scan videos or to write the output. Do not pipe a downloaded script into a shell. Type 1 and Type 2 are unused on Termux, Git Bash, and Windows cmd. Git Bash and Windows cmd do not call Termux `pkg`.

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** Do not invent a second FFmpeg command graph in this file.
- **Intentional:** Pillars A–D only. `list-videos` is a list, not a join. `list-mp4` is a list, not an encode.
- **Anti-fragile:** README, help, and about name the same two jobs.
- **Over-protect:** Keep the sole Active domain file.

## 4. Protection Rule (Sacred)

**Future AI assistants, Grok, or maintainers MUST NOT**:

1. Duplicate full FFmpeg command law here.
2. Add a shell installer, cloud upload, or root elevation as silent domain behavior.
3. Create a second Active `requirement-domain-*` without superseding this one.
4. Drop the two-file join, the join format list, or the edit catalog (cut, percent, tail of none, boomerang, or repeat).
5. Add a folder prompt, an N-file join, or a recursive join scan.
6. Cut, speed, or boomerang inside the join workflow.
7. Make `list-videos` or `list-mp4` run FFmpeg, or make empty argv start J-01 or E-01.
8. Treat non-MP4 files as edit inputs without updating this file and its peers.
9. Drop `--file`, `--start`, and `--end` without updating this file and the CLI peer.

**Violating this rule is a critical domain regression.**

## 5. Acceptance criteria

| ID | Criterion |
|----|-----------|
| AC-1 | Four pillars present. `join` runs J-01 through J-06. `edit` runs E-01 through E-08 |
| AC-2 | Two-video selection without duplicates is documented, with no folder prompt |
| AC-3 | Join output naming and the edit output pattern, including a sample basename, are documented |
| AC-4 | `list-videos` lists the join formats and does not join. `list-mp4` lists MP4 files and does not encode |
| AC-5 | Help and about are real verb surfaces. About names both jobs and does not advertise a shell installer |
| AC-6 | Non-goals include N-file join, a text-menu join folder prompt, cut inside join, a timeline editor, cloud, and a shell installer. The X11 window is `requirement-python-gui` |
| AC-7 | This file stays the sole Active domain SSOT |

## 6. Related requirements (peer keys only)

| Key | Relationship |
|-----|----------------|
| `requirement-video-ffmpeg-pipeline` | Join concat and edit encode |
| `requirement-python-cli-interface` | Typed verbs, flags, empty argv, `--json` |
| `requirement-python-about` | About page. This file keeps the domain sentence |
| `requirement-python-tui` | Screen for J-02 through J-04 and for E-01 through E-08. Row 83 shows the about page |
| `requirement-python-oop` | `Join`, `EditWalk`, `Encoder`, `AboutPage` |
| `requirement-runtime-prerequisites` | FFmpeg and OpenCV |
| `requirement-python-error-handling` | Fewer than two videos. Invalid cut. FFmpeg failures |
| `requirement-class-software-dev` | Class residual |
| `requirement-python-readme` | Headings and pictures in the user document. Domain rows stay here |
| `docs/requirements/index.md` | Registry |

## Design-time verification

| TP family / ID | Suite | Status | Note |
|----------------|-------|--------|------|
| **TP-VIDEOTOOLS-01** | `tests/test_domain_join.py` | todo | `join` on a terminal asks the two indexes and the output name, then concatenates |
| **TP-VIDEOTOOLS-02** | `tests/test_domain_join.py` | todo | Empty join output name is `{stem1} + {stem2}.mp4` |
| **TP-VIDEOTOOLS-03** | `tests/test_domain_join.py` | todo | Fewer than two videos fails closed and does not encode |
| **TP-VIDEOTOOLS-04** | `tests/test_domain_edit.py` | todo | Complete `edit --file --start --end` writes the cut name and does not open the menu |
| **TP-TUI-10** | `tests/test_tui.py` | have | Front row 2 is `edit`. Wide columns include that row |
| **TP-LANG-01** | `tests/test_language.py` | have | Front numbers include 2. Row 4 stays language. Row 3 stays system-log |

**Matrix:** `docs/reviews/requirement-test-matrix.md`
**Map:** `docs/reviews/test-plan.md`

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-08-09 | Superseded | Prior domain file on this tree was the VideoJoin two-file catalog |
| 2026-10-10 | Active 1.0.0 | One domain SSOT for VideoTools. Join J-01..J-06 and edit E-01..E-08. Replaces Active `requirement-domain-videojoin` |

---

**Last Updated**: 2026-10-10
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
