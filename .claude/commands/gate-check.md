---
description: Execute the three mandatory quality gates for the current project.
argument-hint: "[types|build|tests]"
disable-model-invocation: true
---

执行脚本化三门禁。脚本会根据 `ROADMAP.md` 的 `Core_Tech_Stack` 和仓库结构推断检查命令：

```bash
python3 scripts/nr.py gate-check ${ARGUMENTS:-all}
```

如果全部通过，脚本会将 `ROADMAP.md` 的 `Phase_Status` 更新为 `GATE_CHECK`。
