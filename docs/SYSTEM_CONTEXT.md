# SYSTEM_CONTEXT
> 用于记录项目高阶架构决策，方便快速恢复跨会话上下文。
> 每次重要架构变更后更新本文件。

---

## 1. 项目定位与核心价值主张

NexusRhythm 是一套面向 Claude Code 的项目级协作脚手架，用文件、命令、hook 和 subagent 把 AI 开发过程从“即兴补全”提升为“Discovery + Delivery 双段式协作”。

**目标用户**：重度使用 Claude Code 的个人开发者、小团队以及需要把 AI 协作流程标准化的项目维护者
**核心价值**：用最小文件集提供可复制的开发节奏、上下文记忆、阶段门禁和文档沉淀能力
**非目标**（刻意不做的事）：
- 不作为运行时库嵌入业务应用
- 不承诺替代 CI、测试框架或项目管理系统

### 首批用户与核心场景

- 首批用户：已经在用 Claude Code，但希望把“高质量节奏”固定成项目协议的人
- 典型场景：从模糊 idea 启动一个新项目；或在已有项目里持续执行高纪律交付
- 关键判断：项目在进入 Delivery 前必须先定义“为谁做、解决什么问题、先做到什么程度”

---

## 2. 核心架构模式

本项目采用“文件即协议”的脚手架架构：`ROADMAP.md` 负责项目级 + 阶段级状态机，`CLAUDE.md` 负责项目级系统指令，`.claude/settings.json` 负责 hook 入口，`.claude/commands/` 和 `.claude/agents/` 负责工作流分工，`scripts/nr.py` 负责状态读写与关键自动化，`docs/` 负责规范、模板和产出物沉淀，`.nexus/` 负责任务与热记忆。

```
User
  -> ROADMAP.md (project + phase source of truth)
  -> CLAUDE.md (global behavior contract)
  -> .claude/settings.json (hooks)
  -> scripts/nr.py (stateful workflow automation)
  -> .claude/commands/*.md (manual workflows)
  -> .claude/agents/*.md (specialized subagents)
  -> docs/templates/*.md (output structure)
  -> docs/ideas|specs|reviews|walkthroughs|journal|decisions (project memory)
  -> .nexus/tasks|memory (execution continuity)
```

---

## 3. 核心技术约定

| 类别 | 约定 | 原因 |
|------|------|------|
| 配置入口 | 项目级配置以 `ROADMAP.md` + `CLAUDE.md` + `.claude/settings.json` 为准 | 降低会话漂移，保持可追踪性 |
| Hooks | 用独立脚本承载 hook 逻辑，`settings.json` 只做路由 | 便于复用、测试和与官方文档对齐 |
| Commands / Scripts | `.claude/commands/` 负责入口说明，`scripts/nr.py` 负责关键状态读写与检查 | 避免关键规则只停留在 prompt 文案 |
| Discovery / Delivery | `Project_Stage` 管项目定义成熟度，`Phase_Status` 管 Delivery 节奏 | 防止模糊 idea 与阶段实现状态混淆 |
| Agent 权限 | subagent 默认遵循最小权限原则，只授予完成任务所需工具 | 降低误操作风险并减少上下文噪音 |

---

## 4. 状态字段 / 命令 / 产物职责表

| 对象 | 负责什么 | 不负责什么 |
|------|----------|------------|
| `Project_Stage` | idea 到 roadmap 的成熟度 | 当前 Phase 的实现进度 |
| `Phase_Status` | 当前 Delivery 阶段的执行状态 | 项目定义是否清晰 |
| `IDEA_BRIEF` | 问题定义与未知项 | 阶段级接口设计 |
| `MVP_CANVAS` | 最小验证范围与成功指标 | 当前 Phase 的实现细节 |
| `ROADMAP_INIT` | 前三阶段路线草案 | 阶段内测试清单 |
| `SPEC` | 当前 Phase 的契约、边界、测试映射 | 产品为什么做、MVP 边界 |
| `.nexus/tasks` | 阶段内任务粒度 | 项目总体节奏 |
| `.nexus/memory` | 跨会话热记忆 | 长期蒸馏与 ADR |

---

## 5. 关键架构决策索引

> 详细决策见 `docs/decisions/` 目录（ADR 格式）

| ADR | 决策摘要 | 状态 |
|-----|----------|------|
| [ADR-001](decisions/ADR-001-compatibility-first-claude-code.md) | 以官方 Claude Code 兼容性为第一优先级，保留命令式工作流并逐步迁移到 skills | ✅ 已采纳 |

---

## 6. 已知技术约束与限制

- 项目高度依赖 Claude Code 当前功能和文件约定，官方规范变更会直接影响可用性
- 现阶段仍在从“prompt 驱动”迁移到“脚本 + smoke tests 驱动”，并非所有工作流都已完全硬化
- `.nexus/tasks` 与 `.nexus/memory` 当前先提供骨架，后续再补 CLI 和并行能力

---

## 7. 验证路径

- Discovery：`/idea-capture -> /mvp-shape -> /roadmap-init`
- Delivery：`/phase-start -> /spec -> RED_TESTS -> GREEN_CODE -> /gate-check -> /phase-end`
- 跨会话恢复：`/sync` 读取 `.nexus/memory/` 摘要，`/doctor` 检查骨架健康度

---

## 8. 外部依赖与集成点

| 依赖 | 用途 | 版本 | 风险等级 |
|------|------|------|----------|
| Claude Code | 运行 hooks、commands、subagents、skills | 跟随官方最新 | 高 |
| Bash | 执行安装脚本与 hook 脚本 | 系统内置 | 中 |
| Python 3 | 执行 `scripts/nr.py` 和内置 smoke tests | 系统内置 | 中 |
| Git / GitHub | 分发脚手架、协作与版本管理 | 跟随用户环境 | 中 |
