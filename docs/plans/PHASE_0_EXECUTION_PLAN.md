# Phase 0 Execution Plan

**Date**: 2026-03-08  
**Owner**: Codex  
**Purpose**: 将 Phase 0 从“模板状态”推进到“可交接的初始化完成状态”

---

## Current Objective

在不假设任何业务运行时代码存在的前提下，完成以下目标：

1. 明确 NexusRhythm 自身的项目定位和阶段规划
2. 校准 Claude Code 兼容性，修复关键 hook / command / subagent 偏差
3. 为下一阶段形成正式 SPEC，而不是继续无界地补文档

---

## Workstreams

### Workstream A: 项目基础上下文落地

- [x] 填充 `ROADMAP.md`
- [x] 填充 `docs/SYSTEM_CONTEXT.md`
- [x] 形成 ADR-001
- [x] 形成 Phase 1 SPEC 初稿

### Workstream B: Claude Code 兼容性加固

- [x] 对照官方文档审计 hooks / commands / subagents
- [x] 修正 `PreToolUse` matcher 与阻断语义
- [x] 把关键 hook 逻辑外提为脚本
- [x] 补齐 `/review` 命令
- [x] 为 commands 增加 frontmatter，约束为手动触发

### Workstream C: 评估与沉淀

- [x] 输出正式项目评估报告
- [x] 输出 Claude Code 合规审计报告
- [x] 输出想法收集文档
- [x] 输出 Phase 0 Walkthrough 与 Code Review

---

## Executed In This Autonomous Run

已执行事项：

- 修复了 `.claude/settings.json` 与官方 hooks 文档的关键不一致
- 新增 `.claude/hooks/session-status.sh`
- 新增 `.claude/hooks/block-debt-commits.sh`
- 新增 `.claude/commands/review.md`
- 更新安装脚本以复制 hook 脚本
- 清理 README 中关键路径、命令清单和仓库 URL
- 补齐项目评估、合规审计、ADR、SPEC、想法沉淀文档
- 产出 `docs/walkthroughs/WALKTHROUGH_PHASE_0.md`
- 产出 `docs/reviews/CODE_REVIEW_PHASE_0.md`
- 新增 `change-auditor` subagent，并据此完成一轮独立复核

---

## Phase 0 Closeout Status

- [x] 为 Phase 1 编写 smoke test / RED_TESTS 方向的 SPEC 初稿
- [x] 执行最小 gate check，覆盖文档、JSON、脚本语法完整性
- [x] 产出 `WALKTHROUGH_PHASE_0.md`
- [x] 产出 `CODE_REVIEW_PHASE_0.md`
- [x] 更新 `ROADMAP.md`，将 Phase 0 收尾推进到 `DONE`

---

## Proposed Immediate Next Step

建议下一步直接进入：

**Phase 1 的 RED_TESTS 准备**

也就是先不继续扩散做新功能，而是先为下列对象设计 smoke tests：

- hooks 能否在干净会话中被加载
- `Pending_Debt: true` 时 Git 提交是否被真实阻断
- `/review` 是否在命令列表中可见并可触发
- `/doctor` 自检入口是否能准确报告安装状态
- 安装脚本在空目录注入后，目录结构是否完整

这是把“文档正确”升级为“行为可验证”的最短路径。
