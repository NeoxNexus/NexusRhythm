# Idea Backlog

**Date Started**: 2026-03-08  
**Purpose**: 收集本轮执行中出现的高价值改进想法，留待后续集中头脑风暴

> 这是原始收集区，不是承诺区。只有经过 `/idea-review` 审核通过的点子，才能进入计划文档、ADR 或 `ROADMAP.md`。

---

## Product Direction

- 提供一个最小 demo repo，证明 NexusRhythm 在真实项目里能跑通一轮完整 phase cycle
- 把脚手架升级为 Claude Code plugin，支持团队共享安装和版本管理
- 设计一条“轻量模式”路径，适配不需要完整 Phase 仪式的小项目
- 设计一条“零感知使用”路径：普通用户只表达意图，由 AI 自动路由 Discovery / Delivery、尽量隐藏命令和术语面

## Compatibility / Reliability

- 将最关键的 `/phase-start`、`/gate-check`、`/phase-end` 从纯 prompt 升级为 skills + supporting scripts
- 建一个 nightly 文档对照脚本，自动检查官方 Claude Code 文档是否出现关键字段变更
- 为 hooks 增加 smoke tests，避免 silent failure 再次出现

## Developer Experience

- 提供 `/doctor` 或 `/self-check` 命令，一次性检查仓库是否装好 hooks、commands、agents、templates
- 为新用户提供“Phase 0 向导”，自动填充 ROADMAP、SYSTEM_CONTEXT 和首个 ADR
- 把 README、GUIDE、HANDBOOK 的内容按“首次上手 / 深度使用 / 维护者视角”重新分层

## Architecture

- 让 reviewer subagent 支持预加载评审规则 skill，而不是在 prompt 中硬编码全部检查项
- 为 debt-collector 增加基于 SPEC 和目录约定的缺口扫描脚本
- 引入统一的 machine-readable metadata 文件，避免 ROADMAP 既做展示又做状态存储

## Distribution

- 让 `install.sh` 使用中立的项目模板，而不是直接复制脚手架仓库自身的 `ROADMAP.md`
- 发布一个 `install --upgrade` 路径，而不仅是“不覆盖已有文件”的初次注入
- 为 GitHub Template、curl 安装和 plugin 安装三种方式分别提供文档
- 增加版本号和升级日志，便于团队知道何时需要同步脚手架变更
