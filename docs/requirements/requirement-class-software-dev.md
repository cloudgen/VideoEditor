**file**: docs/requirements/requirement-class-software-dev.md
**Status**: Active (Version 1.1.6 – VideoEditor software-development class law + residual stack)
**Area**: class
**Key**: `requirement-class-software-dev`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

Declare this workspace as a software-development project class and hold the residual collection of software-engineering stack facts not already owned by more specific Active peer requirements: primary language, toolchain policy, package and build tooling, and runtime OS family.

This file is class law plus the residual SSOT. It is not a second copy of domain join features, FFmpeg concat ops, the CLI surface, the text menu, the logger construct, the class map, packaging tables, or error-handling tables. Those stay on peer requirements.

### 1.1 Human-facing

**In one sentence:** This file records that VideoJoin is Python, built with setuptools, and it points at the requirement that owns each other topic.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | Maintainer checking which file owns a topic | The menu picture is the TUI requirement. The language row stays here |
| The other role | Peer requirements | CLI, TUI, logging, domain, packaging |
| Not this file | The join steps, the frame glyphs, and the pip command strings | Their own requirements. This file only points |

| Includes | Excludes |
|----------|----------|
| Language, interpreter, package tool, and the residual pointer table | A second copy of the menu, the logger construct, or the class map |
| Shell install and root elevation marked absent | A pip lifecycle marked absent. That lifecycle is owned by the CLI and the TUI |
| One human operator. No dest approver | A new actor-requirement file |

| Surface | What you open | What for |
|---------|---------------|----------|
| This file | Residual table | Which requirement owns the topic |
| `pyproject.toml` | Package tool facts | The concrete manifest. Packaging owns the tables |
| `video-join` | The program | You run it as the normal user |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Find the menu law | Open the TUI requirement. Do not expect the picture in this file. | `video-join` |
| Find the logger law | Open the logging requirement. The floor is packaging and runtime. | `video-join version` |
| Install | Use pip. There is no shell installer. | `python -m pip install VideoJoin` |

## 2. Core Rules (Mandatory)

### 2.0 Project class membership

1. **MUST** treat this workspace as software-development (shippable software), not genesis-template and not server-maintenance.
2. **MUST** use basename `requirement-class-software-dev.md` as the sole Active class-law file for this class.
3. **MUST NOT** register an Active `requirement-class-server-maintenance.md` while the class is software-development.
4. **MUST** retain portable harness knowledge when present. Specialized product knowledge lives in this and peer `requirement-*.md` files.
5. **MUST** apply the software-development SSOT and gate posture when claimed (identity, package ship surface, and a pre-commit check when git is used — as applicable).
6. **MUST NOT** invent hollow product docs solely to look specialized.

### 2.1 Residual collection principle (SSOT hygiene)

7. **MUST** treat this file as the default home for software-stack facts not owned by another Active requirement.
8. **MUST NOT** duplicate full normative tables that already live in a more specific Active requirement. Prefer a one-line pointer to the peer requirement key.
9. When a new specialized requirement takes ownership of a topic previously only listed here, **MUST** update this file in the same change: shrink the residual entry and point to the new owner.
10. **MUST NOT** leave contradictory stack facts across this file and peer requirements.

### 2.2 Programming language(s)

11. **MUST** declare at least one primary programming language for the ship unit.
12. **SHOULD** list secondary languages only when they are real product law.
13. **MUST** state whether the product is primarily interpreted, compiled, polyglot, or package-multi-language.
14. **MUST NOT** freeze a marketing product name as if it were the language name.

### 2.3 Compilers, interpreters, and toolchains

15. **MUST** declare the target toolchain class used to build or run the product.
16. **MUST** state version policy as one of: unconstrained, minimum version, range, or pinned.
17. **SHOULD** record whether cross-compilation is in scope.
18. **MUST** fail closed in docs claims: do not claim “supports all interpreters” without tests or an explicit unconstrained policy.

### 2.4 Project / package / build tools

19. **MUST** declare the primary project or package tool used for dependencies and builds.
20. **MUST** declare how dependencies are resolved when the ecosystem supports lockfiles.
21. **SHOULD** name the test runner and linter or formatter classes when they are project law.
22. **MUST NOT** require a secret token or a private registry password in this file.

### 2.5 Runtime and platform (residual)

23. **MUST** declare the intended primary runtime and OS family when not fully owned by another architecture requirement.
24. **SHOULD** declare minimum CPU or architecture support only when it is real product law.
25. **MUST** separate developer-machine toolchain requirements from end-user runtime requirements when they differ.

### 2.6 No-hardcode / dual policy (class file)

26. **MUST NOT** hard-code a single product brand, one organization’s production hostname, or a personal owner identity as universal core law.
27. **MUST** put the live product name, the repo slug, and the concrete stack choices in Implementation Notes.
28. **MUST NOT** store secrets, PATs, or toy credentials in this file.

### 2.7 Implementation Notes (this project)

| Field | Value (VideoJoin) |
|-------|---------------------|
| **Project display name** | VideoJoin |
| **Project class** | software-development |
| **Class requirement basename** | `requirement-class-software-dev.md` |
| **Primary language(s)** | Python |
| **Language role** | primary only for the runtime package under `src/VideoEditor/` |
| **Execution model** | interpreted package. Optional Cython or `build.sh` tooling is not required for the CLI |
| **Toolchain / interpreter** | CPython |
| **Toolchain version policy** | range declared in `pyproject.toml` (`requires-python`). Re-verify before advertising a specific minor as tested |
| **Cross-compile in scope?** | no |
| **Primary project/package tool** | setuptools via PEP 517/621 `pyproject.toml` |
| **Lockfile policy** | not used as product law |
| **Test runner** | none as project law today. Proof rows in `docs/reviews/test-plan.md` stay todo |
| **Linter/formatter** | none as project law |
| **Primary runtime / OS family** | Multi-OS where Python and FFmpeg run. Linux is the tested picture-window path. The Windows host contract is `requirement-python-windows` |
| **Architectures supported** | any architecture with CPython and an FFmpeg binary |
| **Git surface** | used — remote `https://github.com/cloudgen/VideoEditor` (`git@github.com:cloudgen/VideoEditor.git`) |
| **Ship surface** | installable Python package `VideoJoin`; console script `video-join`; module form `python -m VideoEditor` |
| **Product version SSOT** | `src/VideoEditor/__init__.py` → `__version__` and `pyproject.toml` `[project].version` stay equal when either is bumped (current: **1.0.0**) |
| **Install mode** | pip / local package. Not a shell online-install product |
| **Type 1 elevation** | intentionally absent. No root or sudo product surface |
| **Actor / role / subject / approver** | **Considered — no dest approver.** The human operator of `video-join` is the only actor. No dest approval machine. **None** is valid. Do not add an actor requirement file |
| **Dest fence conditions** | **Considered — no dest fence conditions.** No dest inbound, approve, or reject queue |
| **Author contact (non-secret)** | Wilgat Wong · `wilgat.wong@gmail.com` |

**Residual ownership table:**

| Topic | Owner | Notes |
|-------|-------|--------|
| Project class membership | **this file** | Fixed |
| Primary language + toolchain policy | **this file** | Python / CPython |
| Package/build tool + lockfile | **this file** + `requirement-python-packaging` | packaging owns the PEP 621 tables and the ChronicleLogger floor |
| Project layout | `requirement-python-project-structure` | Running tree versus the class map |
| Class homes | `requirement-python-oop` | One class per file. Do not duplicate the map |
| CLI entry / typed verbs | `requirement-python-cli-interface` | Empty argv and the verb table |
| Text menu | `requirement-python-tui` | Front board and the picture |
| Menu language | `requirement-python-cli-language` | Front row 4, the thirteen codes, and the language leaf |
| Status logger | `requirement-python-cli-logging` | Construct in `def main` |
| Domain surface | `requirement-domain-videoeditor` | Four pillars. The about page uses the domain sentence |
| About page | `requirement-python-about` | Identity, host check, and the star box |
| FFmpeg concat / re-encode | `requirement-video-ffmpeg-pipeline` | Ops SSOT |
| Python coding style / temps / `shutil.move` | `requirement-python-coding-style` | Publish. StateLogic stays unordered |
| Error / fail-closed user messaging | `requirement-python-error-handling` | Console sentences |
| Host runtime deps | `requirement-runtime-prerequisites` | FFmpeg binary and the logger floor |
| Windows host | `requirement-python-windows` | Detect, front door, and the rule that the picture window stays X11. Setup steps stay on `requirement-runtime-prerequisites` |
| Shell online install / shell self-update / Type O | **intentionally absent** | Not a shell channel |
| Pip lifecycle (`version-check`, `self-update`, `self-install`, `self-uninstall`) | `requirement-python-cli-interface` and `requirement-python-tui` | `python -m pip` only. Not a shell channel |
| Type 1 sudoers / root elevation | **intentionally absent** | No elevation law |
| Actor / role / subject / approver | **this file (residual)** | Considered — no dest approver |
| Dest fence conditions | **this file (residual)** | Considered — no dest fence conditions |

## 3. Why This Requirement Exists (Direct CIAO Alignment)

- **CIAO Principle 2 – Intentional**: Class and stack choices are explicit.
- **CIAO Principle 5 – SSOT**: Residual facts stay here until a peer takes the topic. The menu, the logger, and the class map have already moved.
- **CIAO Principle 1 – Caution**: This file does not invent a shell installer.
- **CIAO Principle 21 – Dual Policies**: Pointers stay short. Concrete values sit in Implementation Notes.
- **CIAO Principle 4 (O) + Principle 20**: One class file. No second stack SSOT.

## 4. Design Principles (CIAO / CIAO-Lite)

- **Caution**: FFmpeg is a host tool. This file does not install it.
- **Intentional**: The residual table points. It does not copy peer bodies.
- **Anti-fragile**: Packaging identity stays in `pyproject.toml`.
- **Over-protect**: Shell Type O stays absent while pip lifecycle is claimed on the CLI and the TUI.

## 5. Protection Rule (Sacred)

**Future AI assistants, Grok, or maintainers MUST NOT**:

1. Delete this file while the workspace remains software-development with other Active product requirements.
2. Rename the specialized basename away from `requirement-class-software-dev.md` without an explicit class-model change.
3. Hard-code secrets, personal tokens, or production host names into core rules as universal law.
4. Duplicate full peer requirement bodies into this residual section.
5. Leave Implementation Notes hollow while Status is Active.
6. Introduce a shell online-install channel, a `curl|sh` installer, or shell Type O empty-argv install-ensure. Pip lifecycle owned by the CLI and TUI requirements is not that channel.
7. Introduce Type 1 sudoers or root elevation without an explicit user order and an elevation allowlist.
8. Treat this file as server-maintenance allowlist law, or register an Active server-maintenance class file in parallel.
9. Invent a second primary language that contradicts the Python requirements.
10. Add an actor-requirement file while the residual says no dest approver.
11. Mark pip lifecycle absent, or mark shell Type O present.

**Violating any of these is a critical regression.**

## 6. Acceptance criteria

| ID | Criterion |
|----|-----------|
| AC-1 | The sole Active class file is `requirement-class-software-dev.md` |
| AC-2 | Primary language is Python with the CPython toolchain |
| AC-3 | The package tool is setuptools plus `pyproject.toml` |
| AC-4 | The residual table points at the CLI, TUI, logging, OOP, and domain peers without copying their bodies |
| AC-5 | Shell Type O and Type 1 elevation are absent. Pip lifecycle is owned by the CLI and the TUI |
| AC-6 | Registered in `docs/requirements/index.md` with Area `class` |
| AC-7 | Actor residual stays “no dest approver”. No actor requirement file |

## 7. Related requirements (peer keys only)

| Key | Relationship |
|-----|----------------|
| `requirement-python-packaging` | Manifest, entry point, logger floor |
| `requirement-python-project-structure` | Layout |
| `requirement-python-oop` | Class map |
| `requirement-python-cli-interface` | Typed verbs and empty argv |
| `requirement-python-tui` | Text menu |
| `requirement-python-cli-logging` | Logger construct |
| `requirement-domain-videoeditor` | Domain four pillars |
| `requirement-video-ffmpeg-pipeline` | Processing ops |
| `requirement-python-coding-style` | Temps and `shutil.move` |
| `requirement-python-error-handling` | Console errors |
| `requirement-runtime-prerequisites` | Host tools and the logger floor |
| `requirement-python-windows` | Windows host contract. This residual points |
| `docs/requirements/index.md` | Registry |

## Design-time verification

| TP family / ID | Suite | Status | Note |
|----------------|-------|--------|------|
| n/a | packaging and structure smoke | deferred | Class residual is exercised by TP-PKG, TP-STRUCT, TP-LOG, TP-TUI, and TP-OOP when those rows leave todo |

**Matrix:** `docs/reviews/requirement-test-matrix.md`
**Map:** `docs/reviews/test-plan.md`

## Under command line for normal user only

On Termux, Git Bash, Windows cmd, or the same class, VideoJoin runs as the normal user. **This requirement:** do not use administrator privilege, `sudo`, `apt`, or a dedicated system user. Do not pipe a downloaded script into a shell. Type 1 and Type 2 are unused on Termux, Git Bash, and Windows cmd. Git Bash and Windows cmd do not call Termux `pkg`. Pip lifecycle, when the operator asks for it, is `python -m pip` from the CLI and TUI requirements.

## Terminologies

### Proper project version bump

**Definition:** A proper project version bump is a user-ordered semver increase of the product ship version that is strictly newer than the previous local ship version, applied in the same change on every in-scope surface. When `pyproject.toml` exists, `[project].name` is the app and package name and `[project].version` equals the import-package `__version__`, the ship-unit version, the README Version badge, and the current CHANGELOG heading. A bump is not a side effect of editing a requirement, a skill, or a glossary file. Agents must not invent a second version literal beside the one the user ordered.

**Human daily-life explanation:** A proper project version bump is printing one newer edition number on every copy of the book in the same sitting, because someone asked for a new edition. Editing a workshop note does not print a new edition by itself. When the catalog card exists, the name on the card is the product name and the number on the card is the same number as the title page.

**Daily-life example:** The kitchen card says name `pancake-timer` and edition `1.2.0`. The title page, the cover sticker, and the change list all say `1.2.0`. The next ordered edition is `1.2.1` on all of those surfaces together. A note in the workshop drawer does not become `1.2.1` on its own.

## 8. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-08-09 | Active 1.0.0 | Initial software-dev class law for VideoJoin |
| 2026-10-04 | Active 1.1.0 | Residual pointers for the text menu, the logger, the class map, and pip lifecycle. Shell Type O stays absent |
| 2026-10-04 | Active 1.1.1 | Menu language points at `requirement-python-cli-language`. No new actor file |
| 2026-10-04 | Active 1.1.2 | Residual row for the about page. Product version **1.0.5** |
| 2026-10-10 | Active 1.1.3 | Git surface is `cloudgen/VideoEditor`. Product version current is **1.1.0** |
| 2026-10-11 | Active 1.1.4 | Primary runtime / OS family points at `requirement-python-windows`. Product version stays **1.1.0** |
| 2026-10-11 | Active 1.1.5 | Product version current is **2.0.0**. Terminologies copies the ship-version term |
| 2026-10-12 | Active 1.1.6 | Distribution name is VideoEditor. Console script is `video-editor`. Current release string is **1.0.0**. |

---

**Last Updated**: 2026-10-12
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
