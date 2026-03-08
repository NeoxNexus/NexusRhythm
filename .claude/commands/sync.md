---
description: Read ROADMAP status and render the current navigation card.
disable-model-invocation: true
---

通过脚本读取 `ROADMAP.md`、项目状态和 `.nexus` 热记忆，并输出当前导航卡：

```bash
python3 scripts/nr.py sync
```

输出包括：

- 轻量状态横幅（沿用会话启动协议）
- 当前步骤 / 原因 / 下一步
- 项目摘要
- `.nexus/memory/` 热记忆摘要
- 后置的附加技术状态（用于调试）

约束：

- SessionStart Hook 只显示轻量 banner，不显示完整导航卡
- 显式执行 `/sync` 才显示完整导航卡
- 详细的默认协作原则与渐进式披露策略见 `CLAUDE.md` 与 `docs/designs/NEW_USER_ZERO_COGNITIVE_LOAD_STRATEGY.md`
