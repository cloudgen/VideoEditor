**file**: docs/requirements/requirement-domain-videojoin.md
**Status**: Superseded (Version 1.1.2)
**Area**: domain
**Key**: `requirement-domain-videojoin`
**Superseded by**: `requirement-domain-videoeditor` (sole Active domain SSOT as of 2026-10-10). Do not apply this file.
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

This requirement is the domain surface Single Source of Truth for VideoJoin: which user-facing video-join steps exist, what features the product claims, and how help and about describe them.

Operational FFmpeg processing (concat stream-copy, re-encode fallback, temp list cleanup) is owned by `requirement-video-ffmpeg-pipeline`. Typed verbs and empty argv are owned by `requirement-python-cli-interface`. The screen that asks the join questions is owned by `requirement-python-tui`. Class `Join` and class `AboutPage` are named by `requirement-python-oop`.

This file remains the sole Active `requirement-domain-*` (four pillars). Headings and pictures in the root user document are `requirement-python-readme`. Domain rows in that document stay in this file.

### 1.1 Human-facing

**In one sentence:** VideoJoin concatenates two videos that are already in the folder you are in, and it can list those videos without joining them.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | Person choosing two local videos | `video-join join` |
| The other role | The menu that asks the questions, and FFmpeg that concatenates | `requirement-python-tui`, `requirement-video-ffmpeg-pipeline` |
| Not this file | The rounded menu frame, pip install, and the log folder | TUI, packaging, and logging requirements |

| Includes | Excludes |
|----------|----------|
| Two-file join in the current folder. Formats `.mp4` `.mov` `.mkv` `.avi` `.m4v` | Joining more than two files, a recursive scan, a folder prompt |
| `list-videos`, which lists and does not join | A front-board row for that list |
| Help and about as real pages | A downloaded-script installer advertised on the about page |

| Surface | What you open | What for |
|---------|---------------|----------|
| `video-join join` | Join questions on a terminal | First video, second video, output name |
| `video-join list-videos` | Name list | Eligible files. No concat |
| `video-join about` | About page | Name, version, what the product does, FFmpeg, how to start it |
| `video-join help` | Help page | The same capabilities, including what this product does not do |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Join two videos | Pick the first index, then the second from the list that remains, then the output name. Empty name uses the two file stems. | `video-join join` |
| See what can be joined | The program lists `.mp4`, `.mov`, `.mkv`, `.avi`, and `.m4v` in this folder and stops. | `video-join list-videos` |
| Read about | You see VideoJoin, the package version, the two-file summary, whether FFmpeg is present, and the two ways to start the program. | `video-join about` |

## 2. Core Rules / Requirements (Mandatory)

### 2.1 Pillar A — Specialized CLI surface (workflow steps)

The `join` verb expresses the domain as these ordered steps. Empty argv does not start them. On a terminal the text screen asks them in the bottom box. There is no folder prompt.

| Step ID | User action | Inputs | Output / effect | Ops SSOT |
|---------|-------------|--------|-----------------|----------|
| D-01 | Discover videos | scan the current working directory only | Sorted eligible video list | domain + `Join.discover` |
| D-02 | Choose first video | 1-based index into the list | Chosen `Path` for the first input | domain + TUI |
| D-03 | Choose second video | 1-based index into the remaining list (first removed) | Chosen `Path` for the second input. **MUST NOT** allow the same path twice | domain + TUI |
| D-04 | Choose output name | free string; empty → default pattern | Final output filename | domain + pipeline |
| D-05 | Join | two source paths + output name | Concat via FFmpeg (copy first, re-encode fallback) | `requirement-video-ffmpeg-pipeline` |
| D-06 | Report result | — | Success or failure message. Temps cleaned | error peer + pipeline |

**Routing:** `video-join join` and front-board row 1 **MUST** reach D-01. Bare `video-join` on a terminal opens the front board and **MUST NOT** start D-01. `video-join list-videos` lists the D-01 names and **MUST NOT** continue to D-02.

**Non-goals (unless a later requirement adds them):** join more than two files in one session, recursive multi-folder batch, a folder prompt, GUI, cloud upload, timeline multi-track editor, automatic color grade, cut / speed / boomerang editing, a shell installer, file-operand flags for the two inputs.

Complete invocation samples this pillar owns:

```text
video-join join
video-join list-videos
```

`video-join join` on a terminal asks for the first index, the second index from the remaining list, and the output name. `video-join list-videos` prints the eligible names and does not join. With no terminal, `join` exits non-zero and `list-videos` prints the names and returns 0 (`requirement-python-cli-interface`).

### 2.2 Pillar B — Specialized features (surface map)

| Feature area | Domain role | Full law |
|--------------|-------------|----------|
| Video discovery (cwd, case-insensitive suffixes) | Expose the list for selection and for `list-videos` | this file |
| Two-file selection without duplicates | First index, then second from the remaining list | this file + TUI |
| Output naming | Default `{stem1} + {stem2}.mp4`. Append `.mp4` when the extension is not in the allowed set | this file |
| Lossless join when possible | Prefer stream copy | `requirement-video-ffmpeg-pipeline` |
| Compatible re-encode fallback | When concat-copy fails | `requirement-video-ffmpeg-pipeline` |
| FFmpeg presence | Fail closed when `join` runs and FFmpeg is missing. The front board may still open | `requirement-runtime-prerequisites` |

Domain **MUST NOT** restate full FFmpeg command graphs. Pointers and the feature catalog only.

### 2.3 Pillar C — Specialized project help items

`video-join help` and `python -m VideoJoin --help` **MUST** list the capabilities and the non-goals in this file. Help is a typed verb. It is not a numbered menu row.

The help page **MUST** include:

| Help row | Text intent |
|----------|-------------|
| Working directory | Videos must be in the current folder. The scan is not recursive |
| Formats | `.mp4`, `.mov`, `.mkv`, `.avi`, `.m4v` |
| Selection | First video, then second video. The second list excludes the first |
| Output | Default `{name1} + {name2}.mp4` |
| List | `list-videos` lists those files and does not join |
| Quality | Stream copy first. Re-encode fallback if needed |
| Prerequisite | FFmpeg on PATH for a join. The menu can open without it |
| Menu | On a terminal, `video-join` with no words shows the front board |

Root `README.md` domain rows **MUST** match this catalog when that README is next edited. This pass does not edit the root README.

### 2.4 Pillar D — Specialized project about items

The domain sentence on the about page is this pillar. The page, the host check, and the star box are `requirement-python-about`. `video-join about` and text-menu row 83 show that page. Class `AboutPage` composes it (`requirement-python-oop`).

| Field | Content |
|-------|---------|
| Product name | VideoJoin |
| Version | `__version__`, the same string as `pyproject.toml` (current `1.0.5`) |
| Domain summary | Concatenate two local videos with FFmpeg (copy, then fallback) |

The page **MUST** use that domain sentence. About is not a remote version check. It **MUST NOT** advertise a shell `curl|sh` installer. It **MUST NOT** claim pip installs FFmpeg. Pip install stays on rows 84–87.

Complete invocation samples:

```text
video-join about
video-join help
```

### 2.5 Implementation Notes (this project)

| Item | Value |
|------|--------|
| **Product / package name** | `VideoJoin` |
| **Console script** | `video-join` |
| **Domain class (end state)** | `Join` in `src/VideoJoin/join.py`. About composer is `AboutPage` in `src/VideoJoin/about_page.py` |
| **Running module** | `src/VideoJoin/cli.py` still holds the prompt session |
| **VERSION** | `1.0.5` (`__init__.py` and `pyproject.toml`) |
| **Input formats** | `.mp4`, `.mov`, `.mkv`, `.avi`, `.m4v` (suffix match, case-insensitive) |
| **Scan scope** | Current working directory only (`Path('.').iterdir()`). Not recursive |
| **Output location** | The name as entered, or the default, in the current directory |
| **Output name default** | `{vid1.stem} + {vid2.stem}.mp4` |
| **Output extension rule** | If the name does not end with `.mp4`, `.mkv`, or `.mov` (case-insensitive), append `.mp4` |
| **Ops SSOT** | `requirement-video-ffmpeg-pipeline` |
| **CLI SSOT** | `requirement-python-cli-interface` |
| **Screen** | `requirement-python-tui`. Questions stay in the bottom box |
| **User docs** | Root `README.md` Features / Usage / Examples must list the two-file cwd join, the formats, and copy-then-fallback when that README is next edited |

### 2.6 Why This Requirement Exists (CIAO)

- **Principle 2 – Intentional**: The four pillars stay explicit, and `join` is not what empty argv does.
- **Principle 5 – SSOT**: One Active domain file for the feature catalog.
- **Principle 1 – Caution**: Non-goals stay listed so a later edit does not add a folder prompt, an N-file batch, or a shell installer.

## Under command line for normal user only

On Termux, Git Bash, Windows cmd, or the same class, join and list-videos run as the normal user against the current folder. **This requirement:** do not use administrator privilege, `sudo`, `apt`, or a dedicated system user to scan videos or to write the output. Do not pipe a downloaded script into a shell. Type 1 and Type 2 are unused on Termux, Git Bash, and Windows cmd. Git Bash and Windows cmd do not call Termux `pkg`.

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** Do not invent a second FFmpeg command graph in this file.
- **Intentional:** Pillars A–D only. `list-videos` is a list, not a join.
- **Anti-fragile:** README, help, and about name the same two-file job.
- **Over-protect:** Keep the sole Active domain file.

## 4. Protection Rule (Sacred)

**Future AI assistants, Grok, or maintainers MUST NOT**:

1. Duplicate full FFmpeg command law here.
2. Add a shell installer, cloud upload, or root elevation as silent domain behavior.
3. Create a second Active `requirement-domain-*` without superseding this one.
4. Drop the two-file join or the format list from the catalog.
5. Claim a recursive batch, an N-file join, or a folder prompt without updating this file and its peers.
6. Re-scope this product into cut, speed, or boomerang editing.
7. Make `list-videos` run FFmpeg, or make empty argv start D-01.

**Violating this rule is a critical domain regression.**

## 5. Acceptance criteria

| ID | Criterion |
|----|-----------|
| AC-1 | Four pillars present, and `join` is the verb that runs D-01 through D-06 |
| AC-2 | Two-video selection without duplicates is documented, with no folder prompt |
| AC-3 | Output naming default and the extension rule are documented |
| AC-4 | `list-videos` lists the format set and does not join, and the invocation sample is in this file |
| AC-5 | Help and about are real verb surfaces. About does not advertise a shell installer |
| AC-6 | Non-goals include N-file batch, recursion, GUI, cloud, cut/speed/boomerang, and a shell installer |
| AC-7 | This file stays the sole Active domain SSOT |

## 6. Related requirements (peer keys only)

| Key | Relationship |
|-----|----------------|
| `requirement-video-ffmpeg-pipeline` | Concat SSOT |
| `requirement-python-cli-interface` | Typed `join` and `list-videos` |
| `requirement-python-about` | About page. This file keeps the domain sentence |
| `requirement-python-tui` | Screen that asks D-02 through D-04. Row 83 shows the about page |
| `requirement-python-oop` | `Join` and `AboutPage` |
| `requirement-runtime-prerequisites` | FFmpeg presence |
| `requirement-python-error-handling` | Fewer than two videos. FFmpeg failures |
| `requirement-class-software-dev` | Class residual |
| `requirement-python-readme` | Headings and pictures in the user document. Domain rows stay here |
| `docs/requirements/index.md` | Registry |

## Design-time verification

| TP family / ID | Suite | Status | Note |
|----------------|-------|--------|------|
| **TP-VIDEOJOIN-01** | `tests/test_domain_join.py` | todo | `join` on a terminal asks the two indexes and the output name, then concatenates |
| **TP-VIDEOJOIN-02** | `tests/test_domain_join.py` | todo | Empty output name is `{stem1} + {stem2}.mp4` |
| **TP-VIDEOJOIN-03** | `tests/test_domain_join.py` | todo | Fewer than two videos fails closed and does not encode |
| **TP-VIDEOJOIN-04** | `tests/test_domain_join.py` | todo | The second list excludes the first path |
| **TP-VIDEOJOIN-05** | `tests/test_domain_join.py` | optional | Discovery includes `.mov`, `.mkv`, `.avi`, and `.m4v` |
| **TP-CLI-03** | `tests/test_cli.py` | todo | Peer: fewer than two videos, no encode |

**Matrix:** `docs/reviews/requirement-test-matrix.md`
**Map:** `docs/reviews/test-plan.md`

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-08-09 | Active 1.0.0 | Domain SSOT for VideoJoin interactive two-file join |
| 2026-10-04 | Active 1.1.0 | D-01 through D-06 are the `join` verb. `list-videos`, help, and about are real surfaces. Empty argv does not start D-01 |
| 2026-10-04 | Active 1.1.1 | Headings and pictures in the user document are `requirement-python-readme`. Domain rows stay here |
| 2026-10-04 | Active 1.1.2 | Pillar D keeps the domain sentence. The page is `requirement-python-about`. Product version **1.0.5** |

---

**Last Updated**: 2026-10-04
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
