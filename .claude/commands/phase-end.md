---
description: Run the phase-end ritual, gate checks, walkthrough generation, and reviewer handoff.
disable-model-invocation: true
---

执行阶段结束仪式（5 步）。严格按顺序执行：

---

### Step 1: 三门禁检查（必须全部通过）
运行以下检查（根据项目实际技术栈调整命令）：

```
❶ 类型检查 / 静态分析
❷ 项目构建
❸ 全量测试
```

**如果任何一项失败：停止仪式，报告失败原因，等待修复。**

将 `Phase_Status` 保持在 `GATE_CHECK`，直到三门禁全部通过。

---

### Step 2: 更新 ROADMAP.md
- 将当前阶段 `Phase_Status` 更新为 `REVIEW`
- 填写阶段仪表盘中的"实际耗时"
- 更新"总体进度"百分比（用你的最佳判断估算）

---

### Step 3: 产出 Walkthrough
基于 `docs/templates/WALKTHROUGH_TEMPLATE.md`，在 `docs/walkthroughs/` 目录创建 `WALKTHROUGH_PHASE_N.md`：
- 列出本阶段完成的主要工作
- 记录关键技术决策（链接到对应 ADR）
- 填写踩坑记录表

---

### Step 4: 启动评审 Agent
调用 `reviewer` agent，执行深度代码评审：
- 生成 `docs/reviews/CODE_REVIEW_PHASE_N.md`
- 如果评审结果是 CHANGES REQUIRED，Phase_Status 回退到 GREEN_CODE

---

### Step 5: 小复盘 + 点子评审 + 阶段归档
引导填写 Walkthrough 末尾的小复盘模板：
- 实际耗时 vs 预估
- 最大意外
- 最大收获/教训
- 下阶段改进点

如果本阶段产生了新点子：
- 运行 `/idea-review`
- 将 `Approved Now` / `Approved Later` 的点子同步进 `docs/ideas/IDEA_PORTFOLIO_REVIEW.md`
- 只把审核通过的点子写入计划文档或 `ROADMAP.md`

完成后：
- 将 `Phase_Status` 更新为 `DONE`
- 递增 `Phases_Since_Vibe` 计数器
- 如果 `Phases_Since_Vibe >= 3`：提示用户已解锁 Vibe Sprint 资格！

---

✅ **阶段结束仪式完成！** 运行 `/phase-start` 开启下一阶段。
