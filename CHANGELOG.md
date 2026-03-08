# Changelog

All notable changes to this project will be documented in this file.

## [0.2.0] - 2026-03-08

### Added

- Added a Discovery workflow before Delivery with `/idea-capture`, `/mvp-shape`, and `/roadmap-init`.
- Added `.nexus/tasks/` and `.nexus/memory/` scaffold directories for hot memory and handoff continuity.
- Added `scripts/nr.py` as the scripted entrypoint for sync, doctor, gate checks, phase controls, distill, and Discovery workflows.
- Added smoke tests covering install wiring, hooks, Discovery state transitions, doctor coverage, and gate-check regressions.
- Added a product strategist agent and new Discovery templates for idea brief, MVP canvas, and roadmap initialization.

### Changed

- Moved hook logic from inline shell parsing into `scripts/nr.py` to centralize state handling.
- Extended `ROADMAP.md`, `CLAUDE.md`, and the handbook docs with project-level Discovery state fields and transition rules.
- Hardened `/doctor` to validate shipped commands and key templates instead of only checking top-level directories.
- Hardened Discovery commands so they cannot silently advance with missing upstream artifacts or rewind a project already in `DELIVERY`.
- Improved gate detection for injected projects by prioritizing host-repo signals before scaffold-only checks.

### Fixed

- Fixed false-positive `/gate-check` passes on injected repositories where the scaffold metadata would previously override the host tech stack.
- Fixed `/doctor` false negatives for missing command files and template files.
- Fixed Python test command selection so pytest-based projects can use pytest instead of always falling back to `unittest`.
- Fixed Mode 2 gate enforcement gaps by adding stricter production checks and rejecting unsupported coverage setups instead of passing silently.
- Fixed Discovery state regressions where `/idea-capture`, `/mvp-shape`, or `/roadmap-init` could push or pull the project into invalid states.

### Verification

- `python3 -m unittest discover -s tests -p 'test_*.py'`
- `python3 scripts/nr.py doctor full`

