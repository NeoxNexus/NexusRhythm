---
description: Initialize a three-phase roadmap from discovery artifacts.
disable-model-invocation: true
---

基于 `IDEA_BRIEF` + `MVP_CANVAS` 生成 `docs/ideas/ROADMAP_INIT.md`：

```bash
python3 scripts/nr.py roadmap-init
```

执行后：

- `Project_Stage` 切到 `ROADMAP_READY`
- 生成前三阶段路线草案
- 明确 `Phase 1` 的单一目标

完成 ROADMAP / SYSTEM_CONTEXT 的项目定义同步后，再把 `Project_Stage` 切到 `DELIVERY`。
