---
description: Run the phase-end ritual, gate checks, walkthrough generation, and reviewer handoff.
disable-model-invocation: true
---

执行脚本化阶段结束检查：

```bash
python3 scripts/nr.py phase-end
```

脚本会：

- 重新执行三门禁
- 检查当前阶段对应的 `WALKTHROUGH_PHASE_N.md` 与 `CODE_REVIEW_PHASE_N.md`
- 通过后更新 `Phase_Status: DONE`
- 递增 `Phases_Since_Vibe`

脚本不会隐式生成 walkthrough 或 review；缺失时会明确报错并停止。
