# Tests — VideoEditor

Executable proof for product law. **Design map:** `docs/reviews/test-plan.md`.  
**RTM:** `docs/reviews/requirement-test-matrix.md`.

## Status (2026-10-04, product 1.0.5)

| Item | State |
|------|--------|
| Design TP map | **present** under `docs/reviews/test-plan.md` |
| Automated suites | `tests/test_about.py` covers **TP-ABOUT-01** through **TP-ABOUT-14** and **TP-ABOUT-16** (have). There is no **TP-ABOUT-15**. `tests/test_tui.py` covers **TP-TUI-09** and **TP-TUI-10** (have). `tests/test_language.py` covers **TP-LANG-01** (have). `tests/test_docs.py` covers **TP-DOC-01** (have). **TP-DOC-03** stays `todo`. **TP-LOG-*** and **TP-OOP-*** stay `todo` |
| Runner | `tests/run.sh` (`python3 -m unittest discover`) |
| Last run | 2026-10-04 `./tests/run.sh` — 23 tests, OK |

## Planned layout

| File | TP families |
|------|-------------|
| `test_about.py` | TP-ABOUT-01..14 and TP-ABOUT-16 (have). No TP-ABOUT-15 |
| `test_tui.py` | TP-TUI-09 and TP-TUI-10 (have). TP-TUI-01..08 still todo |
| `test_language.py` | TP-LANG-01 (have) |
| `test_docs.py` | TP-DOC-01 (have). TP-DOC-03 stays todo |
| `test_structure.py` | TP-STRUCT |
| `test_packaging.py` | TP-PKG |
| `test_prerequisites.py` | TP-PRE |
| `test_cli.py` | TP-CLI |
| `test_domain_join.py` | TP-VIDEOJOIN |
| `test_ffmpeg_pipeline.py` | TP-FFMPEG |
| `test_errors.py` | TP-ERR |
| `test_fs_publish.py` | TP-FS |

## Rules

1. Assert messages / test names **MUST** include the **TP-ID**.  
2. Run media cases only with **generated fixtures** in temp dirs — never user media.  
3. Core cases **MUST NOT** require public network.  
4. Flip `todo` → `have` in `docs/reviews/test-plan.md` and requirement DTV only after green runs.  
5. Do not place executable tests under `docs/templates/`.

## Run (when suites exist)

```bash
./tests/run.sh
```
