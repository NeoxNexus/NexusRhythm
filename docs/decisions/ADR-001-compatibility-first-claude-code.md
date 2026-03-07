# ADR-001: Claude Code compatibility first, with gradual migration to skills

**状态**：已采纳
**日期**：2026-03-08
**阶段**：Phase 0
**决策者**：Neo / Codex

---

## 背景

NexusRhythm 的核心价值建立在 Claude Code 的 hooks、commands、subagents 和项目级指令加载之上。当前仓库已经形成一套可工作的 `.claude/` 结构，但在官方文档快速演进后，部分实现出现了偏差，例如 hook matcher、阻断返回码和命令能力模型与当前文档不完全对齐。

如果继续靠猜测维护，风险很高：用户会在看似可用的脚手架上建立流程，但真实运行时可能出现 silent failure，尤其是 `PreToolUse` 这种被拿来承担守门职责的环节。

---

## 决策

> **我们选择了：以官方 Claude Code 兼容性为第一优先级，先修正高风险偏差，再逐步把命令式工作流迁移到 skills 能力模型。**

短期保留 `.claude/commands/` 以保证当前使用路径稳定；中期通过 skills、hook scripts、smoke tests 和 CI 增强确定性。

---

## 考虑过的方案

| 方案 | 优势 | 劣势 | 结论 |
|------|------|------|:----:|
| 兼容性优先 + 渐进迁移 ⭐ | 风险可控，能快速修复高价值问题，同时保留现有用户路径 | 会经历一段 commands 与 skills 并存期 | ✅ 采纳 |
| 立刻全面迁移到 skills/plugin | 一次性拥抱官方推荐能力 | 改动大，回归风险高，Phase 0 会被拉长 | ❌ 拒绝 |
| 保持现状，仅补文档说明 | 成本最低 | 守门能力不可靠，长期技术债持续累积 | ❌ 拒绝 |

---

## 后果

**正面影响**：
- 关键工作流先对齐官方规范，减少 silent failure
- 保留当前 `.claude/commands/` 入口，降低迁移摩擦
- 为后续 plugin/skills/CI 产品化建立更清晰的演进路径

**负面影响 / 风险**：
- 短期内会有 commands 与未来 skills 并存的复杂度
- 需要持续追踪 Claude Code 文档和 changelog，防止再次漂移

**技术债务**：
- 仍有部分工作流依赖 prompt，而非脚本化验证
- 尚未建立自动 smoke tests 去验证 hooks、commands、subagents 的真实行为

---

## 重新评估触发条件

> 如果以下情况发生，需要重新审视此决策：

- Claude Code 官方停止推荐或弱化 `.claude/commands/` 路径
- skills 或 plugins 提供了足够稳定的替代能力，且迁移成本显著下降
- 项目开始面向团队大规模分发，需要更强的可安装性和版本化机制

---

## 相关资源

- [Claude Code Hooks Docs](https://code.claude.com/docs/en/hooks)
- [Claude Code Slash Commands Docs](https://code.claude.com/docs/en/slash-commands)
- [Claude Code Subagents Docs](https://code.claude.com/docs/en/subagents)
- [Claude Code Changelog](https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md)
