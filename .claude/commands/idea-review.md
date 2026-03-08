---
description: Review raw ideas from the backlog, approve or defer them, and sync approved items into plans and ROADMAP.
argument-hint: "[范围或阶段]"
disable-model-invocation: true
---

执行一次 backlog 点子评审，将“执行过程中顺手记下的想法”转化为有结论的计划输入。

注意：

- 这个命令只负责 backlog 准入，不负责 Discovery 主链路
- 模糊想法立项请使用 `/idea-capture -> /mvp-shape -> /roadmap-init`

**评审范围**：`$ARGUMENTS`（如未提供，默认评审 `docs/ideas/IDEA_BACKLOG.md` 中自上次审查以来的新增点子）

---

### Step 1: 收集候选点子
1. 读取 `docs/ideas/IDEA_BACKLOG.md`
2. 读取最近阶段的 Walkthrough、Code Review、Journal
3. 只提取本阶段新产生的、尚未审查的点子

### Step 2: 客观评审
对每个点子按以下维度打结论：
- 是否解决已证实的问题
- 是否符合当前阶段目标
- 实现成本是否与项目体量匹配
- 是否会引入过早架构化或过早产品化

结论仅允许：
- `Approved Now`
- `Approved Later`
- `Hold`
- `Reject`

### Step 3: 产出评审结果
更新或生成 `docs/ideas/IDEA_PORTFOLIO_REVIEW.md`：
- 记录每个点子的结论与原因
- 明确 `Approved Now` 和 `Approved Later` 的推荐顺序

### Step 4: 同步已通过点子
仅对 `Approved Now` / `Approved Later`：
- 将近期要做的点子写入当前阶段计划文档
- 如果影响阶段规划或优先级，更新 `ROADMAP.md`
- 如果形成结构性决策，提示运行 `/decision`

**禁止**将未审查点子直接写进 `ROADMAP.md`。

### Step 5: 汇报
输出：
- 新审查点子数
- 通过 / 暂缓 / 拒绝数量
- 同步到了哪些文档
- 下一步建议
