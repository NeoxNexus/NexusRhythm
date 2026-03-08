---
name: gate-check
description: Run the three mandatory quality gates and explain whether the project can proceed to phase closeout.
disable-model-invocation: true
---

# Gate Check Skill

Use this skill when the user wants to verify whether the current project is ready for phase closeout, whether quality gates are blocking progress, or which gate failed.

## What this skill does

1. Run the quality gates:

```bash
python3 scripts/nr.py gate-check ${ARGUMENTS:-all}
```

2. Interpret the result for the user with this structure:

```text
当前步骤：[当前是在执行三门禁 / 定位失败门禁 / 准备进入 phase-end]
原因：[为什么当前门禁结果会阻塞或放行下一步]
下一步：[继续修复失败项，还是进入 /phase-end]
```

3. Keep the explanation short:
- all pass: can continue to phase closeout
- some fail: fix the failing gate before phase-end

## Notes

- This skill is the Phase 2 Slice B trial migration of the existing `/gate-check` workflow.
- `/gate-check` remains the compatibility command surface; this skill adds interpretation, not a second gate implementation.
- If the user explicitly asks for command-level detail, include the raw gate-check output after the short interpretation.
