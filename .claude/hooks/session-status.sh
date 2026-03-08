#!/usr/bin/env bash

set -eu

ROOT="${CLAUDE_PROJECT_DIR:-$(pwd)}"

if [ ! -f "$ROOT/scripts/nr.py" ]; then
  exit 0
fi

python3 "$ROOT/scripts/nr.py" --root "$ROOT" sync --hook
