---
description: Shape a discovery brief into an MVP canvas with explicit scope boundaries.
argument-hint: "[北极星目标]"
disable-model-invocation: true
---

基于 `docs/ideas/IDEA_BRIEF.md` 生成 `docs/ideas/MVP_CANVAS.md`：

```bash
python3 scripts/nr.py mvp-shape "$ARGUMENTS"
```

必须产出：

- `In Scope`
- `Out Of Scope`
- 至少 2 个成功指标
- 至少 1 个失败信号

下一步：运行 `/roadmap-init`。
