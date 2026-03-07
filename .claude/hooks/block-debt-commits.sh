#!/usr/bin/env bash

set -eu

ROOT="${CLAUDE_PROJECT_DIR:-$(pwd)}"
RPATH=""

if [ -f "$ROOT/ROADMAP.md" ]; then
  RPATH="$ROOT/ROADMAP.md"
elif [ -f "$ROOT/docs/ROADMAP.md" ]; then
  RPATH="$ROOT/docs/ROADMAP.md"
fi

INPUT="$(cat)"
COMMAND="$(
  printf '%s' "$INPUT" | python3 -c 'import json, sys
try:
    data = json.load(sys.stdin)
except Exception:
    print("")
    raise SystemExit(0)
print(data.get("tool_input", {}).get("command", ""))' 2>/dev/null || true
)"

if [ -z "$RPATH" ]; then
  exit 0
fi

if grep -qE '^Pending_Debt:[[:space:]]*true' "$RPATH"; then
  if printf '%s' "$COMMAND" | grep -qE '(^|[[:space:]])git[[:space:]]+(commit|push)([[:space:]]|$)'; then
    echo "Blocked by NexusRhythm: Pending_Debt is true. Clear debt before commit or push." >&2
    exit 2
  fi
fi

exit 0
