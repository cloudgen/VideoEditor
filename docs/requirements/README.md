# Requirements

Authoritative specialized product law for **VideoEditor** lives here.

**Current state (2026-10-12):** Specialized **software-development** product. Left genesis. Registry is populated — see `index.md`. One Active domain file. Product version is **1.0.0**.

## Product identity (summary)

| Field | Value |
|-------|--------|
| Product / package | `VideoEditor` |
| Version SSOT | **`1.0.0`** (`pyproject.toml` + `src/VideoEditor/__init__.py`) |
| Product README SSOT | Root `README.md` (app-name, short description, target version **1.0.0**). Sections and pictures: `requirement-python-readme` |
| Ship surface | Python package; console scripts **`video-editor`**, **`video-join`**, **`video-speed`**; module `python -m VideoEditor` |
| Install mode | **pip / local package** (`pip install VideoEditor`; this tree **1.0.0**; checkout `pip install -e .`) — not shell Type O |
| Domain surface | `requirement-domain-videoeditor` — four pillars (join, edit, help, about). `requirement-domain-videojoin` is Superseded |
| Text menu | `requirement-python-tui` — front rows join, edit, system-log, language, self-management, Exit. Default path word is `Path` |
| Menu language | `requirement-python-cli-language` — row 4, thirteen codes, leaf `~/.local/VideoEditor/language`. Window controls use the same codes. `language` is not an argv verb |
| Status logger | `requirement-python-cli-logging` — `ChronicleLogger(...)` inside `def main`. Required |
| Class map | `requirement-python-oop` — join classes and edit classes under `src/VideoEditor/` |
| Encode ops | `requirement-video-ffmpeg-pipeline` — join stream-copy then re-encode; edit cut, speed, one tail (none, boomerang, or repeat); unique temps; **`shutil.move`** publish |
| Coding style | `requirement-python-coding-style` — temps + `shutil.move`; gate **`CL-PYTHON-SHUTIL-MOVE-PUBLISH`** |
| Runtime tools | **FFmpeg** on PATH for a join or an encode. **OpenCV** (`opencv-python-headless>=5.0.0.93`) for duration. **ChronicleLogger>=1.3.1** required. Live `pyproject.toml` declares both floors |

## Class requirement gate

| Class | Required class file |
|-------|---------------------|
| software-development | `requirement-class-software-dev.md` (**Active**) |
| genesis-template | N/A — this workspace is no longer genesis for product law |

## Purpose

- **Plan** designs work by reading and updating these docs.  
- **Implement** delivers code that **traces** to these requirements.  
- **Review** verifies delivery against requirements and CIAO checklists.  
- Product **README** must stay honest with this law (install, features, version).

## Layout

| Path | Role |
|------|------|
| `docs/requirements/index.md` | Registry of all requirements — keep in sync |
| `docs/requirements/requirement-*.md` | CIAO-style project requirements |

## Status values

Typical: `draft` · `Active` · `approved` · `in-progress` · `done` · `deprecated` · `superseded`

## Rules

1. Never invent paths — verify on disk.  
2. Class files only via class process; non-class via create-specific process.  
3. Never dump harness inventories into this versioned surface.  
4. Online shell install and Type 1 elevation stay **absent** unless product mode is explicitly changed.  
5. Sole Active domain SSOT: `requirement-domain-videoeditor.md`. `requirement-domain-videojoin.md` is Superseded.  
6. When changing join/publish behavior: update pipeline + coding-style REQs **and** root `README.md` in the same change.  
7. Version dual SSOT + README Version badge must match when a release is claimed.
