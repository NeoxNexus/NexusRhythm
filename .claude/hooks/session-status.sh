#!/usr/bin/env bash

set -eu

ROOT="${CLAUDE_PROJECT_DIR:-$(pwd)}"
RPATH=""

if [ -f "$ROOT/ROADMAP.md" ]; then
  RPATH="$ROOT/ROADMAP.md"
elif [ -f "$ROOT/docs/ROADMAP.md" ]; then
  RPATH="$ROOT/docs/ROADMAP.md"
fi

if [ -z "$RPATH" ]; then
  exit 0
fi

extract_field() {
  field_name="$1"
  grep -E "^${field_name}:" "$RPATH" | head -1 | sed -E "s/^${field_name}:[[:space:]]*\"?([^\"]+)\"?.*$/\\1/"
}

phase="$(extract_field Current_Phase)"
status="$(extract_field Phase_Status)"
mode="$(extract_field Active_Mode)"
debt="$(extract_field Pending_Debt)"
deadline="$(extract_field Debt_Deadline)"

printf '═══════════════════════════════\n'
printf '📍 Phase: %s\n' "$phase"
printf '🔄 Status: %s\n' "$status"
printf '⚙️  Mode: %s  |  🔧 Debt: %s\n' "$mode" "$debt"
printf '═══════════════════════════════\n'

if [ "$deadline" != "null" ] && [ -n "$deadline" ]; then
  printf 'Debt_Deadline: %s\n' "$deadline"
fi
