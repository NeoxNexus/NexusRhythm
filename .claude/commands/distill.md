---
description: Distill recent lessons into reusable rules for future Claude sessions.
disable-model-invocation: true
---

通过脚本扫描 Journal、Walkthrough 和 Code Review，去重后更新 `.claude/rules/lessons.md`：

```bash
python3 scripts/nr.py distill
```

脚本会：

- 扫描 `docs/journal/`、`docs/walkthroughs/`、`docs/reviews/`
- 合并重复教训
- 按技术栈 / 架构 / 工作流分类
- 更新时间戳和蒸馏来源
