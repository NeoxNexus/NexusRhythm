---
description: Read ROADMAP status and report the current project phase.
disable-model-invocation: true
---

读取项目 ROADMAP.md 的 YAML 头部，给我一份结构化的状态报告：

1. **当前状态**
   - 项目名称
   - 当前阶段（Current_Phase）
   - 阶段状态（Phase_Status）
   - 工作模式（Active_Mode）及其含义

2. **债务状态**
   - Pending_Debt 是否为 true
   - 如果是，Debt_Deadline 是否超期

3. **进度概览**
   - 从进度仪表盘提取各阶段状态

4. **Vibe Sprint 状态**
   - Phases_Since_Vibe 计数
   - 是否已解锁下一次 Vibe Sprint（≥3 即可）

5. **下一步行动建议**
   - 基于当前 Phase_Status，建议下一步操作
   - 如果有阻塞，明确指出

输出格式要清晰，使用 emoji 增强可读性。
