**file**: docs/requirements/requirement-python-packaging.md
**Status**: Active (Version 1.2.6)
**Area**: python
**Key**: `requirement-python-packaging`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

Define the packaging SSOT for the VideoTools Python distribution: `pyproject.toml`, metadata, dependencies, console entry points, and version consistency.

This file owns the ChronicleLogger floor together with `requirement-runtime-prerequisites`. There is no separate dependency-management requirement.

### 1.1 Human-facing

**In one sentence:** VideoTools is a pip package named VideoTools, version 2.0.0, and ChronicleLogger and OpenCV are required dependencies.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | Person installing the package | `python -m pip install VideoTools` |
| The other role | The manifest | `pyproject.toml` names the version, the console script, and the dependencies |
| Not this file | What the menu does after install, and how FFmpeg concatenates | CLI, TUI, and pipeline requirements |

| Includes | Excludes |
|----------|----------|
| Package name VideoTools, version 2.0.0, console scripts `video-tools`, `video-join`, and `video-speed`, required `ChronicleLogger>=1.3.1` and `opencv-python-headless>=5.0.0.93` | Re-exporting ChronicleLogger from the VideoTools package |
| Manifest floor `ChronicleLogger>=1.3.1`, same as this law | Calling the logger optional, or leaving the manifest at `>=1.2.3` |
| MIT license, homepage, Python range as declared | A claim that pip installs FFmpeg |

| Surface | What you open | What for |
|---------|---------------|----------|
| `pyproject.toml` | `[project]` | Name, version, dependencies, console script |
| `src/VideoTools/__init__.py` | `__version__` | The same version string |
| pip | Install | `python -m pip install VideoTools` |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Install | pip installs VideoTools and the required status library. It does not install FFmpeg. | `python -m pip install VideoTools` |
| Check the version | The badge, the manifest, and `__version__` are the same string. | Open `pyproject.toml` and `__init__.py` |
| Import the package | You get `__version__` and `main`. You do not get ChronicleLogger from this package. | `python -c "import VideoTools"` |

## 2. Core Rules (Mandatory)

### 2.1 Manifest SSOT

1. `pyproject.toml` **MUST** be the primary packaging manifest (PEP 517 / PEP 621).
2. **MUST** declare: name, version, description, authors, license text, requires-python, dependencies, build-system, and console scripts.
3. **MUST NOT** treat an ad-hoc `requirements.txt` as the primary product dependency SSOT.
4. A legacy `setup.py` under a build tree **MUST NOT** become a second source of runtime identity.

### 2.2 Version SSOT

5. The package version in `pyproject.toml` and `src/VideoTools/__init__.py` (`__version__`) **MUST** match when a release is claimed.
6. Bumping either **MUST** update both in the same change.
7. **MUST NOT** invent a third version constant. Display code **MUST NOT** keep a second literal, including a fallback of an older release (`requirement-python-oop`). The current release string is `2.0.0`. A version bump is a user order, not a side effect of editing this file.

### 2.3 Dependencies

8. **MUST** declare runtime Python dependencies required for the shipped CLI.
9. ChronicleLogger **MUST** be a required dependency at floor `ChronicleLogger>=1.3.1`. OpenCV **MUST** be a required dependency at floor `opencv-python-headless>=5.0.0.93`. Neither **MUST** be marked optional. The live `pyproject.toml` declares both floors. `requires-python` **MUST** be `>=3.11`.
10. System tools (FFmpeg, and GTK 4 plus GStreamer for the window in `requirement-python-gui`) **MUST NOT** be declared as pip packages. Document FFmpeg under `requirement-runtime-prerequisites`. The interpreter module `_curses` **MUST NOT** be declared as a pip package, and `windows-curses` **MUST NOT** be added to `pyproject.toml`. A missing `_curses` is avoided with `try` / `except ImportError` as `requirement-runtime-prerequisites` requires. Verb `setup` on Windows **MAY** run `python -m pip install windows-curses` when that import fails. That install stays on `requirement-runtime-prerequisites`. It **MUST NOT** become a `pyproject.toml` entry, and the load-time handler **MUST NOT** install it.
11. **MUST NOT** commit secrets or private index passwords into packaging files.
12. **MUST NOT** re-export `ChronicleLogger` from the VideoTools package.

### 2.4 Entry points

13. **MUST** declare console scripts `video-tools`, `video-join`, and `video-speed`, each → `VideoTools.cli:main`.
14. The entry function **MUST** stay `def main` in `src/VideoTools/cli.py`. `main` constructs ChronicleLogger and then `Cli` (`requirement-python-cli-logging`, `requirement-python-oop`).

### 2.5 Build / release helpers

15. Optional `build.sh` / Cython tooling **MAY** exist for maintainer packaging.
16. **MUST** keep helper scripts consistent with `pyproject.toml` identity (project name VideoTools).
17. Generated `build/` and `dist/` **MUST NOT** be treated as source SSOT.

### 2.6 Implementation Notes (this project)

| Item | Value |
|------|--------|
| **Manifest** | `pyproject.toml` |
| **Project name** | `VideoTools` |
| **Version** | `2.0.0` |
| **requires-python** | `>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*` (as declared — re-verify support claims before marketing) |
| **Dependencies (law)** | `opencv-python-headless>=5.0.0.93` and `ChronicleLogger>=1.3.1`, both required. `_curses` is not a pip dependency. `windows-curses` is not a `pyproject.toml` entry. The import uses `try`. Verb `setup` may install `windows-curses` on Windows when the import fails |
| **Dependencies (live manifest)** | Same two floors. `requires-python` is `>=3.11` |
| **Build backend** | `setuptools.build_meta` |
| **Console scripts** | `video-tools`, `video-join`, and `video-speed` = `VideoTools.cli:main` |
| **Homepage / repo** | `https://github.com/cloudgen/VideoTools` |
| **Maintainer build helper** | `build.sh` |
| **License** | MIT |
| **Public package exports** | `__version__`, `main` only. **MUST NOT** re-export `ChronicleLogger` |
| **User docs** | Root `README.md` Quick Installation documents pip and **MUST NOT** claim pip installs FFmpeg. This pass does not edit that README |
| **README version badge** | Must match packaging version (`2.0.0`) |

### 2.7 Why This Requirement Exists (CIAO)

- **Principle 5 – SSOT**: One manifest for identity and entry. One floor for ChronicleLogger.
- **Principle 2 – Intentional**: The live manifest lag is written down instead of being described as optional.
- **Principle 1 – Caution**: System FFmpeg is not declared as a pip package.

## Under command line for normal user only

On Termux, Git Bash, Windows cmd, or the same class, install and upgrade use pip as the normal user. **This requirement:** do not use administrator privilege, `sudo`, `apt`, or a dedicated system user to install VideoTools. Do not pipe a downloaded script into a shell. Type 1 and Type 2 are unused on Termux, Git Bash, and Windows cmd. Git Bash and Windows cmd do not call Termux `pkg`. The install line is `python -m pip install VideoTools`.

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** The version string has one home in the manifest and one matching `__version__`.
- **Intentional:** PEP 621 is the manifest. The logger floor is required.
- **Anti-fragile:** The console script and the module entry share `main`.
- **Over-protect:** No secrets in packaging files. No re-export of ChronicleLogger.

## 4. Protection Rule (Sacred)

**Future AI assistants, Grok, or maintainers MUST NOT**:

1. Remove or rename the `video-join` entry without a CLI and README update.
2. Let `__version__` and `pyproject.toml` diverge while claiming a release.
3. Add private credentials to `pyproject.toml`.
4. Replace the packaging SSOT with only `requirements.txt`.
5. Change the product name silently.
6. Mark ChronicleLogger optional, or leave the manifest at `>=1.2.3` once the packaging file is edited for the floor.
7. Re-export ChronicleLogger from the package.
8. Bump the product version as a side effect of editing this requirement.

**Violating this rule is a critical packaging regression.**

## 5. Acceptance criteria

| ID | Criterion |
|----|-----------|
| AC-1 | `pyproject.toml` names VideoTools |
| AC-2 | Console script `video-join` is declared |
| AC-3 | Law and the live manifest both require `ChronicleLogger>=1.3.1` |
| AC-4 | Version matches `__init__.py` when a release is claimed (`2.0.0`) |
| AC-5 | FFmpeg is external, not a pip dependency |
| AC-6 | Public exports are `__version__` and `main` only |
| AC-7 | `_curses` is not a pip dependency. `windows-curses` is absent from `pyproject.toml`. A missing module is avoided with `try` / `except ImportError`. Verb `setup` may install `windows-curses` on Windows when the import fails |

## 6. Related requirements (peer keys only)

| Key | Relationship |
|-----|----------------|
| `requirement-python-project-structure` | Package path |
| `requirement-python-cli-interface` | Entry behavior |
| `requirement-python-cli-logging` | Points here for the floor |
| `requirement-runtime-prerequisites` | Same floor. FFmpeg is a system binary. `_curses` stays off the pip list and the import uses `try` |
| `requirement-python-tui` | Text menu. The `try` lives on the load-time import, and the miss sentence stays there |
| `requirement-python-oop` | `main` stays the console target |
| `requirement-class-software-dev` | Residual stack |
| `docs/requirements/index.md` | Registry |

## Design-time verification

| TP family / ID | Suite | Status | Note |
|----------------|-------|--------|------|
| **TP-PKG-01** | `tests/test_packaging.py` | todo | Console script resolves. Package does not re-export ChronicleLogger |
| **TP-PKG-02** | `tests/test_packaging.py` | todo | `pyproject.toml` version equals `__version__` |
| **TP-PRE-02** | `tests/test_prerequisites.py` | todo | Peer: ChronicleLogger import. Floor target is `>=1.3.1` |

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
| 2026-08-09 | Active 1.0.0 | Initial packaging law for VideoTools |
| 2026-08-09 | Active 1.1.0 | Export honesty and version 1.0.3 |
| 2026-10-04 | Active 1.2.0 | ChronicleLogger is required at `>=1.3.1`. Live manifest still `>=1.2.3`. Product version stays 1.0.3 |
| 2026-10-04 | Active 1.2.1 | Product version **1.0.4**. Manifest floor is `ChronicleLogger>=1.3.1` |
| 2026-10-04 | Active 1.2.2 | Product version **1.0.5**. Floor stays `ChronicleLogger>=1.3.1` |
| 2026-10-10 | Active 1.2.3 | `_curses` is not a pip dependency. A missing module is avoided with `try` / `except ImportError` |
| 2026-10-10 | Active 1.2.4 | `windows-curses` stays out of `pyproject.toml`. Verb `setup` on Windows may install it when `import curses` fails. That step is `requirement-runtime-prerequisites` |
| 2026-10-10 | Active 1.2.5 | Homepage, repository, and issues are `https://github.com/cloudgen/VideoTools` |
| 2026-10-11 | Active 1.2.6 | Current release string is **2.0.0**. Terminologies copies the ship-version term |

---

**Last Updated**: 2026-10-11
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
