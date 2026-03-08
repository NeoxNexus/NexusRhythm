---
description: Run a self-check on the project scaffold, workflow wiring, and phase artifact completeness.
argument-hint: "[quick|full]"
disable-model-invocation: true
---

执行脚本化自检，检查脚手架、Discovery/Delivery 状态机、`.nexus` 热记忆和阶段产物：

```bash
python3 scripts/nr.py doctor ${ARGUMENTS:-full}
```

结果约定：

- `GREEN`：结构完整，可继续工作
- `YELLOW`：存在非阻塞缺口，应尽快修正
- `RED`：存在阻塞问题，当前工作流不可信

`/doctor` 默认只诊断，不隐式修复。
