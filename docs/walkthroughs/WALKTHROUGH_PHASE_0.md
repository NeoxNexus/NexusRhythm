# WALKTHROUGH — Phase 0: 初始化与规划

**日期范围**：2026-03-08 至 2026-03-08
**实际耗时**：3.5 小时
**预估耗时**：4 小时
**误差率**：12.5% （节省）

---

## 1. 本阶段完成了什么

本阶段把 NexusRhythm 从“有完整模板，但项目自身仍是模板占位状态”的脚手架，推进成了一个已经完成自我描述、完成官方兼容性审计、形成下一阶段执行计划的项目。更具体地说，这一轮工作没有扩展新功能，而是先校准项目自身，让后续开发建立在真实、可验证、可复盘的基础上。

### 主要交付物
- [x] 完成项目级正式评估报告 `docs/PROJECT_ASSESSMENT.md`
- [x] 完成 Claude Code 合规审计 `docs/CLAUDE_CODE_COMPLIANCE_AUDIT.md`
- [x] 完成 Phase 0 执行计划 `docs/PHASE_0_EXECUTION_PLAN.md`
- [x] 完成 Phase 1 SPEC 初稿 `docs/specs/SPEC_PHASE_1_claude-code-compatibility-hardening.md`
- [x] 完成 ADR-001，明确“兼容性优先、渐进迁移到 skills”的演进策略
- [x] 新增 `/review` 命令，补齐文档已承诺但仓库缺失的命令入口
- [x] 将关键 hooks 从内联 shell 迁移为 `.claude/hooks/*.sh` 脚本
- [x] 创建变更审计 subagent，为后续阶段结束复核提供固定角色

---

## 2. 关键技术决策

### 决策一：先修兼容性，再谈产品化
- **背景**：仓库的价值高度依赖 Claude Code 的 hooks、commands、subagents 能否真实工作。如果这些配置存在 silent failure，再漂亮的流程文档也不可靠。
- **选择**：先围绕官方文档做兼容性审计，修掉高置信配置问题，再制定后续自动化与产品化阶段。
- **原因**：这是最短风险路径。先消除“文档写对了但配置没生效”的隐患，能显著降低后续阶段返工。
- **ADR 链接**：[ADR-001-compatibility-first-claude-code.md](/Users/neo/.codex/worktrees/7a12/NexusRhythm/docs/decisions/ADR-001-compatibility-first-claude-code.md)

### 决策二：保留 `.claude/commands/`，但按当前官方能力补 frontmatter
- **背景**：官方当前把 custom commands 和 skills 合并到统一能力模型里，但已有 `.claude/commands/*.md` 仍然有效。
- **选择**：不做激进迁移，保留 `.claude/commands/` 路径，同时按官方 frontmatter 规则增强现有命令。
- **原因**：这样可以兼顾兼容性与迁移成本，避免在 Phase 0 就引入大规模结构重写。

### 决策三：把高风险 hook 逻辑外提到独立脚本
- **背景**：原来的 hook 逻辑全部写在 `settings.json` 的内联 shell 字符串里，维护性差，错误也难定位。
- **选择**：使用 `.claude/hooks/session-status.sh` 和 `.claude/hooks/block-debt-commits.sh` 承载逻辑，`settings.json` 只做路由。
- **原因**：脚本化后更可读、更可测试，也更接近官方推荐使用 `$CLAUDE_PROJECT_DIR` 引脚本的方式。

---

## 3. 踩坑记录

> 这里的坑将在 `/distill` 时被提炼进 `.claude/rules/lessons.md`

| # | 坑的描述 | 根本原因 | 解决方案 |
|---|----------|----------|----------|
| 1 | `PreToolUse` 的 matcher 写成了 `BashTool`，看起来像对的，但不符合官方工具名约定 | 早期配置没有对照当前官方 hooks 文档复核 | 改为 `Bash`，并在合规审计文档中记录原因 |
| 2 | 原始阻断逻辑依赖 `CLAUDE_TOOL_INPUT` 环境变量，兼容性不可靠 | 把 tool 输入来源想当然地写成环境变量，而不是官方 stdin JSON | 改为从 stdin 读取 JSON，并按 `tool_input.command` 解析 |
| 3 | 文档承诺存在 `/review`，但仓库里并没有这个命令文件 | README / CLAUDE 与实现长期漂移 | 新增 `.claude/commands/review.md` 并同步文档 |
| 4 | 项目自身仍是模板占位状态，导致评估报告一开始只能判断“方法论完整”，无法判断“项目已初始化” | 仓库建立了流程框架，但没有先完成对自身的 Phase 0 初始化 | 补齐 ROADMAP、SYSTEM_CONTEXT、ADR、SPEC 和阶段计划 |

---

## 4. 测试覆盖摘要

- 新增测试用例：0 个
- 测试通过率：N/A（本阶段以文档、配置与脚本校准为主）
- 覆盖率（如有追踪）：N/A
- 已执行的最小验证：
  - `python3 -m json.tool .claude/settings.json`
  - `bash -n install.sh`
  - `bash -n .claude/hooks/session-status.sh`
  - `bash -n .claude/hooks/block-debt-commits.sh`

---

## 5. 性能影响评估

- 本阶段未引入运行时业务逻辑，无热路径性能变化
- hooks 增加了极轻量的 shell / Python JSON 解析，预期影响只发生在 Claude Code 生命周期事件中，对用户业务代码无性能副作用

---

## 6. 下阶段注意事项

> 写给**下一个开始 Phase N+1 的自己/AI**的话

- 不要继续无界扩文档，下一阶段必须把兼容性工作推进到 smoke tests 和可验证行为
- 如果要迁移到 `.claude/skills/`，先挑一个代表性流程试点，不要一次性重构全部命令
- 每次引用 Claude Code 新特性前都要重新对照官方文档，不要凭记忆写配置
- `docs/IDEA_BACKLOG.md` 里很多点子是方向，不是承诺；必须先做客观筛选再进阶段计划

---

## 7. 小复盘

**最大意外**：真正的高风险问题不是“缺功能”，而是几个看似很小的 Claude Code 配置偏差，它们会让守门逻辑静默失效。

**最大收获 / 教训**：对于 AI 工程脚手架，兼容性审计和行为验证本身就是核心功能，不是附属工作。

**下个阶段工作方式上想改进的地方**：尽快把 prompt 约束替换成 smoke tests、skills 和脚本验证，减少“口头正确”的部分。
