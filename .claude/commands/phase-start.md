---
description: Start a new phase by checking prerequisites, updating ROADMAP, and invoking the architect workflow.
argument-hint: "[阶段名称]"
disable-model-invocation: true
---

执行脚本化阶段启动检查：

```bash
python3 scripts/nr.py phase-start "$ARGUMENTS"
```

硬约束：

- `Pending_Debt` 必须为 `false`
- 上一阶段 `Phase_Status` 必须为 `DONE`
- `Project_Stage` 必须为 `DELIVERY`
- `Idea_Clarity >= 3`

若 Discovery 条件不满足：

- `IDEA` → `/idea-capture`
- `DISCOVERY` → `/mvp-shape`
- `MVP_DEFINED` / `ROADMAP_READY` → `/roadmap-init`

通过后：

- `Phase_Status` 更新为 `PLANNING`
- 如提供参数，则更新 `Current_Phase`
- 下一步进入 `/spec`
