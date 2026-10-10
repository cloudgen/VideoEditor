#!/bin/sh
# VideoJoin test runner. TP-TUI-09, TP-LANG-01, and TP-DOC-01 do not need ffmpeg.
set -eu
ROOT="$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
export PYTHONPATH="${ROOT}/src${PYTHONPATH:+:$PYTHONPATH}"
python3 -m unittest discover -s tests -v
