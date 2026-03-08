---
description: Read ROADMAP status and report the current project phase.
disable-model-invocation: true
---

通过脚本读取 `ROADMAP.md`、Discovery 状态和 `.nexus` 热记忆摘要：

```bash
python3 scripts/nr.py sync
```

输出包括：

- 当前 `Phase` / `Phase_Status` / `Mode` / `Pending_Debt`
- `Project_Stage` / `Idea_Clarity`
- Vibe Sprint 状态
- `.nexus/memory/` 热记忆摘要
- 下一步推荐动作
