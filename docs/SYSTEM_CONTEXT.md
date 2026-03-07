# SYSTEM_CONTEXT
> 用于记录项目高阶架构决策，方便快速恢复跨会话上下文。
> 每次重要架构变更后更新本文件。

---

## 1. 项目定位与核心价值主张

NexusRhythm 是一套面向 Claude Code 的项目级协作脚手架，用文件、命令、hook 和 subagent 把 AI 开发过程从“即兴补全”提升为“阶段化交付”。

**目标用户**：重度使用 Claude Code 的个人开发者、小团队以及需要把 AI 协作流程标准化的项目维护者
**核心价值**：用最小文件集提供可复制的开发节奏、上下文记忆、阶段门禁和文档沉淀能力
**非目标**（刻意不做的事）：
- 不作为运行时库嵌入业务应用
- 不承诺替代 CI、测试框架或项目管理系统

---

## 2. 核心架构模式

本项目采用“文件即协议”的脚手架架构：`ROADMAP.md` 负责状态机，`CLAUDE.md` 负责项目级系统指令，`.claude/settings.json` 负责 hook 入口，`.claude/commands/` 和 `.claude/agents/` 负责工作流分工，`docs/` 负责规范、模板和产出物沉淀。

```
User
  -> ROADMAP.md (phase/source of truth)
  -> CLAUDE.md (global behavior contract)
  -> .claude/settings.json (hooks)
  -> .claude/commands/*.md (manual workflows)
  -> .claude/agents/*.md (specialized subagents)
  -> docs/templates/*.md (output structure)
  -> docs/specs|reviews|walkthroughs|journal|decisions (project memory)
```

---

## 3. 核心技术约定

| 类别 | 约定 | 原因 |
|------|------|------|
| 配置入口 | 项目级配置以 `ROADMAP.md` + `CLAUDE.md` + `.claude/settings.json` 为准 | 降低会话漂移，保持可追踪性 |
| Hooks | 用独立脚本承载 hook 逻辑，`settings.json` 只做路由 | 便于复用、测试和与官方文档对齐 |
| Commands / Skills | 兼容现有 `.claude/commands/`，逐步向 skills 能力迁移 | 保持现有用户路径，同时获得更强扩展性 |
| Agent 权限 | subagent 默认遵循最小权限原则，只授予完成任务所需工具 | 降低误操作风险并减少上下文噪音 |

---

## 4. 关键架构决策索引

> 详细决策见 `docs/decisions/` 目录（ADR 格式）

| ADR | 决策摘要 | 状态 |
|-----|----------|------|
| [ADR-001](decisions/ADR-001-compatibility-first-claude-code.md) | 以官方 Claude Code 兼容性为第一优先级，保留命令式工作流并逐步迁移到 skills | ✅ 已采纳 |

---

## 5. 已知技术约束与限制

- 项目高度依赖 Claude Code 当前功能和文件约定，官方规范变更会直接影响可用性
- 现阶段多数工作流仍是 prompt 驱动，缺少脚本化验证和 CI 兜底

---

## 6. 外部依赖与集成点

| 依赖 | 用途 | 版本 | 风险等级 |
|------|------|------|----------|
| Claude Code | 运行 hooks、commands、subagents、skills | 跟随官方最新 | 高 |
| Bash | 执行安装脚本与 hook 脚本 | 系统内置 | 中 |
| Git / GitHub | 分发脚手架、协作与版本管理 | 跟随用户环境 | 中 |
