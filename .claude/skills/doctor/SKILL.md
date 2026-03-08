---
name: doctor
description: Render the scaffold health report and explain the result using current step, reason, and next step.
disable-model-invocation: true
---

# Doctor Skill

Use this skill when the user wants to verify whether the NexusRhythm scaffold is installed correctly, whether the current workflow wiring is trustworthy, or why the project health is blocking progress.

## What this skill does

1. Run the scaffold health check:

```bash
python3 scripts/nr.py doctor ${ARGUMENTS:-full}
```

2. Interpret the result for the user with this structure:

```text
当前步骤：[当前是在确认脚手架健康度 / 修复阻塞项 / 继续推进]
原因：[为什么当前健康状态会影响下一步]
下一步：[应该继续工作，还是先修复缺口]
```

3. Keep the explanation short:
- `GREEN`: can continue
- `YELLOW`: non-blocking gaps, recommend fixing soon
- `RED`: workflow is not trustworthy, fix before continuing

## Notes

- This skill is the Phase 1 trial migration of the existing `/doctor` workflow.
- SessionStart and `/sync` remain lightweight navigation surfaces; detailed health diagnosis stays here.
- If the user explicitly asks for command-level detail, include the raw `doctor` result after the short interpretation.
