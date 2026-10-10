**file**: docs/requirements/requirement-python-project-structure.md
**Status**: Active (Version 1.1.2)
**Area**: python
**Key**: `requirement-python-project-structure`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

Define the repository layout and the package structure for VideoJoin: where source, packaging, and requirement law live, and which modules exist today versus which modules the class map names.

### 1.1 Human-facing

**In one sentence:** The installable code lives in `src/VideoTools/`, including the join modules and the edit modules.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | Maintainer looking for the program | Open `src/VideoTools/cli.py` |
| The other role | The class map | `requirement-python-oop` names the later files. They are not on disk yet |
| Not this file | What the menu shows, and how two videos are concatenated | TUI, domain, and pipeline requirements |

| Includes | Excludes |
|----------|----------|
| `src/VideoTools/__init__.py`, `__main__.py`, and `cli.py` as the running package | A second installable package name |
| The class files as the allowed end state, landed by a later implement order | Treating those files as already required on disk |
| Root `pyproject.toml`, root `README.md`, root `CHANGELOG.md`, and `docs/requirements/` | Deleted design notes listed as if they were still present |

| Surface | What you open | What for |
|---------|---------------|----------|
| `src/VideoTools/` | The package | Version, module entry, and the running session |
| `pyproject.toml` | Packaging | Name, version, console script |
| `docs/requirements/index.md` | Registry | Which requirement files are Active |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Run from a checkout | The module entry calls `main` in `cli.py`. | `python -m VideoTools` |
| Look for the menu classes | They are named by the OOP requirement. They are not in the running tree. | Read `requirement-python-oop` |
| Read the product history | Use the changelog at the repository root. | `CHANGELOG.md` |

## 2. Core Rules (Mandatory)

### 2.1 Source package layout

1. **MUST** keep the installable package under `src/VideoTools/`.
2. The running package **MUST** include `__init__.py` (version export), `__main__.py` (module entry), and `cli.py` (class `Cli` and `def main`).
3. The package **MUST** also include the modules named by `requirement-python-oop`, including `tui.py`, `gui.py`, `menu_painter.py`, `menu_model.py`, `menu_session.py`, `menu_language.py`, `system_log.py`, `self_management.py`, `check_system.py`, `about_page.py`, `join.py`, `edit_walk.py`, `encoder.py`, `file_stage.py`, `media_info.py`, and `run_output.py`. `cli.py` holds class `Cli` and `def main`, and it does not hold the other classes’ methods.
4. **MUST NOT** scatter a second installable package name that contradicts the packaging SSOT.

### 2.2 Project root layout

5. **MUST** keep `pyproject.toml` at the repository root.
6. **MUST** keep product user docs at root `README.md`. Sections, badges, and pictures in that document are `requirement-python-readme`.
7. **MUST** keep the product changelog at root `CHANGELOG.md`.
8. **MUST** keep specialized product law under `docs/requirements/` with the `requirement-` prefix and the registry `index.md`.
9. **MUST NOT** list a deleted design note as a present file. `docs/CHANGELOG.md`, `docs/VideoJoin-spec.md`, and `docs/folder-structure.md` are not in the tree.

### 2.3 Generated / non-source

10. **MUST NOT** commit `build/` or `dist/` artifacts as the product source of truth.
11. Egg-info, `__pycache__`, and compiled `.so` **MUST** remain ignore-friendly.
12. Optional Cython or `build.sh` tooling **MAY** exist as maintainer tooling. It **MUST NOT** replace `src/VideoTools` as the runtime package.

### 2.4 Requirements surface discipline

13. Product-law files **MUST** use the basename prefix `requirement-`.
14. **MUST** register every Active requirement in `docs/requirements/index.md`.
15. Product source comments that cite law **MUST** cite live `requirement-*.md` keys only.

### 2.5 Implementation Notes (this project)

| Path | Role |
|------|------|
| `src/VideoTools/` | Installable package |
| `src/VideoTools/__init__.py` | `__version__` (`1.1.0`) |
| `src/VideoTools/__main__.py` | Module entry. Imports `main` from `cli` |
| `src/VideoTools/cli.py` | Class `Cli` and `def main` |
| `src/VideoTools/join.py` | Class `Join` |
| `src/VideoTools/edit_walk.py` | Class `EditWalk` |
| `src/VideoTools/encoder.py` | Class `Encoder` |
| `src/VideoTools/file_stage.py` | Class `FileStage` |
| `src/VideoTools/media_info.py` | Class `MediaInfo` |
| `src/VideoTools/run_output.py` | Class `RunOutput` |
| `pyproject.toml` | Packaging SSOT |
| `build.sh` | Maintainer build helper |
| `docs/requirements/` | Product law |
| `CHANGELOG.md` | Product changelog at the repository root |
| `tests/` | Proof. Today the tree holds `tests/README.md` only. Suites are not law |
| `README.md` | User documentation |

The class modules named in rule 3 are absent. That absence matches this file. It does not match the allowed end state in `requirement-python-oop`.

### 2.6 Why This Requirement Exists (CIAO)

- **Principle 2 – Intentional**: The running tree and the target tree are both named.
- **Principle 5 – SSOT**: One package path. One requirements registry. One changelog path.
- **Principle 17 – Storage**: Generated directories are not source.

## Under command line for normal user only

On Termux, Git Bash, Windows cmd, or the same class, the package is the normal user’s `video-join`. **This requirement:** do not use administrator privilege, `sudo`, `apt`, or a dedicated system user to lay out the package or to start it. Do not pipe a downloaded script into a shell. Type 1 and Type 2 are unused on Termux, Git Bash, and Windows cmd. Git Bash and Windows cmd do not call Termux `pkg`.

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** Do not invent a parallel package, and do not invent files that were deleted.
- **Intentional:** `src/` is the layout. The class map says what a later edit adds.
- **Anti-fragile:** Build debris stays ignored.
- **Over-protect:** The registry stays aligned with the files on disk.

## 4. Protection Rule (Sacred)

**Future AI assistants, Grok, or maintainers MUST NOT**:

1. Move the installable package out of `src/VideoTools/` without a packaging update.
2. Delete the `docs/requirements/index.md` discipline.
3. Commit secrets under `src/` or `docs/requirements/`.
4. Cite a template or a skill from product source as product law.
5. Treat a design note as a second law SSOT over an Active requirement.
6. List `docs/CHANGELOG.md`, `docs/VideoJoin-spec.md`, or `docs/folder-structure.md` as present.
7. Require the OOP class files on disk before an implement order, or keep `cli.py` as the permanent home of every other class after that order.

**Violating this rule is a critical structure regression.**

## 5. Acceptance criteria

| ID | Criterion |
|----|-----------|
| AC-1 | The package lives under `src/VideoTools/` |
| AC-2 | Root `pyproject.toml` is present |
| AC-3 | Requirements live under `docs/requirements/` with an index |
| AC-4 | Generated `build/` and `dist/` are not the source SSOT |
| AC-5 | The running tree is the three modules. The target modules are named, not required yet |
| AC-6 | The product changelog path is root `CHANGELOG.md` |

## 6. Related requirements (peer keys only)

| Key | Relationship |
|-----|----------------|
| `requirement-python-oop` | Target modules |
| `requirement-python-packaging` | Manifest |
| `requirement-python-cli-interface` | Entry module |
| `requirement-class-software-dev` | Class residual |
| `requirement-python-readme` | Sections, badges, and pictures in root `README.md` |
| `docs/requirements/index.md` | Registry |

## Design-time verification

| TP family / ID | Suite | Status | Note |
|----------------|-------|--------|------|
| **TP-STRUCT-01** | `tests/test_structure.py` | todo | Running package has `__init__`, `__main__`, and `cli` |
| **TP-OOP-01** | `tests/test_oop.py` | todo | Target class files. Not part of TP-STRUCT-01 until they land |

**Matrix:** `docs/reviews/requirement-test-matrix.md`
**Map:** `docs/reviews/test-plan.md`

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-08-09 | Active 1.0.0 | Initial project structure law for VideoJoin |
| 2026-10-04 | Active 1.1.0 | Running tree is three modules. Target modules are the OOP map. Deleted design-note paths are not listed as present. Changelog is root `CHANGELOG.md` |
| 2026-10-04 | Active 1.1.1 | Sections, badges, and pictures in root `README.md` are `requirement-python-readme` |
| 2026-10-04 | Active 1.1.2 | Allowed end state names `check_system.py`. `__version__` is **1.0.5** |

---

**Last Updated**: 2026-10-04
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
