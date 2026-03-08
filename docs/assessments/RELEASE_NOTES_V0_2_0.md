# RELEASE_NOTES_V0_2_0

## NexusRhythm v0.2.0

This release turns NexusRhythm from a mostly prompt-driven scaffold into a more scripted workflow system with a real Discovery layer ahead of Delivery.

### Highlights

- Added Discovery commands: `/idea-capture`, `/mvp-shape`, `/roadmap-init`
- Added `scripts/nr.py` to centralize sync, doctor, gate-check, phase controls, and Discovery logic
- Added `.nexus/tasks/` and `.nexus/memory/` to support cross-session continuity
- Hardened `/doctor` and `/gate-check` so they catch more real installation and workflow failures
- Added smoke tests for the scaffold install and key regression paths

### Notable Fixes

- Fixed injected-project gate detection so host repository commands win over scaffold fallback
- Fixed Discovery commands so missing prerequisites no longer advance project state
- Fixed false-negative `/doctor` checks for missing command files and template files
- Fixed Python test detection so pytest projects can use pytest
- Fixed production-mode enforcement gaps by rejecting unsupported Mode 2 coverage setups

### Upgrade Notes

- If you use Mode 2 on a Node project, expose one of these scripts in `package.json`: `coverage:check`, `test:coverage`, or `coverage`
- Discovery commands are now guarded and will refuse to rewrite a project already in `DELIVERY`
- `/doctor` is stricter; missing templates or command files that used to slip through now fail fast

### Suggested Tag

- `v0.2.0`

