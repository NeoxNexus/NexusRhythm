# RELEASE_CHECKLIST_V0_2_0

## Scope

- Release target: `v0.2.0`
- Release date: `2026-03-08`
- Release type: feature release

## Preflight

- [x] Discovery workflow commands are present: `/idea-capture`, `/mvp-shape`, `/roadmap-init`
- [x] `scripts/nr.py` is wired from hooks and command entrypoints
- [x] `.nexus/tasks/` and `.nexus/memory/` are installed by `install.sh`
- [x] `/doctor` validates core commands and shipped templates
- [x] `/gate-check` handles injected repositories before scaffold fallback
- [x] Discovery commands block invalid state transitions

## Verification

- [x] `python3 -m unittest discover -s tests -p 'test_*.py'`
- [x] `python3 scripts/nr.py doctor full`
- [x] Node Mode 2 without a coverage script fails explicitly
- [x] Missing `SPEC_TEMPLATE.md` causes `/doctor quick` to fail
- [x] pytest-based Python repos are detected and routed through `pytest`
- [x] Discovery commands refuse to rewind a project already in `DELIVERY`

## Release Steps

1. Review the final diff and confirm no unrelated local experiments remain.
2. Commit the release candidate changes.
3. Create an annotated tag: `git tag -a v0.2.0 -m "NexusRhythm v0.2.0"`
4. Push the branch and tag: `git push origin <branch>` and `git push origin v0.2.0`
5. Publish release notes using `docs/assessments/RELEASE_NOTES_V0_2_0.md`
6. After release, verify GitHub release links to `CHANGELOG.md`

## Release Gates

- Block release if smoke tests fail
- Block release if `/doctor full` reports `RED`
- Block release if tag name or notes drift from `CHANGELOG.md`
- Block release if install flow is not reproducible on a clean directory

