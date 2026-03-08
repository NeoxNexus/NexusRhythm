---
description: Capture a fuzzy idea into a structured IDEA_BRIEF and update project discovery status.
argument-hint: "[原始想法]"
disable-model-invocation: true
---

将模糊想法收敛成 `docs/ideas/IDEA_BRIEF.md`，并回写 `ROADMAP.md` 的 Discovery 状态：

```bash
python3 scripts/nr.py idea-capture "$ARGUMENTS"
```

执行后：

- `Project_Stage` 切到 `DISCOVERY`
- `Idea_Clarity` 初始化为 `1`
- 生成当前项目的 `IDEA_BRIEF`

下一步：运行 `/mvp-shape`。
