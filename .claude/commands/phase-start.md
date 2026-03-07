---
description: Start a new phase by checking prerequisites, updating ROADMAP, and invoking the architect workflow.
argument-hint: "[阶段名称]"
disable-model-invocation: true
---

执行新阶段启动检查清单。严格按顺序执行，任一步骤失败则停止并报告原因：

**阶段名称**：$ARGUMENTS（如未提供，从 ROADMAP.md 读取下一个计划中的阶段）

---

### Step 1: 前置条件检查
- [ ] 读取 ROADMAP.md，确认 `Pending_Debt: false`
  - ❌ 如果为 true：**停止**，告知用户必须先清理债务（运行 /distill 和 debt-collector agent）
- [ ] 确认上一阶段的 `Phase_Status` 为 `DONE`
  - ❌ 如果不是：**停止**，告知还有未完成的阶段结束仪式

### Step 2: 明确本阶段目标
引导用户用**一句话**说清楚：
- 本阶段要交付什么？
- 成功的可验证标准是什么？（至少 2 个可量化指标）

### Step 3: 更新 ROADMAP
- 将新阶段信息填入阶段仪表盘
- 将 `Phase_Status` 更新为 `PLANNING`
- 将 `Current_Phase` 更新为新阶段名称

### Step 4: 启动架构师 Agent
调用 `architect` agent，开始：
1. 编写本阶段的 SPEC 文档
2. 基于 SPEC 编写红灯测试用例

### Step 5: 状态确认
输出本阶段启动完成的摘要，提醒用户：
- SPEC 文档位置
- 红灯测试文件位置
- 下一步：让 AI 实现代码，直到测试全绿
