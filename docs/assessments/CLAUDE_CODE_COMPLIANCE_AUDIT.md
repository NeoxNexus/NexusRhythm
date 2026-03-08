# Claude Code Compliance Audit

**Date**: 2026-03-08  
**Auditor**: Codex  
**Audit Scope**: `.claude/settings.json`, `.claude/commands/`, `.claude/agents/`, install flow, documented command surface

---

## Sources Used

Primary sources only:

- [Claude Code Hooks Docs](https://code.claude.com/docs/en/hooks)
- [Claude Code Slash Commands Docs](https://code.claude.com/docs/en/slash-commands)
- [Claude Code Skills Docs](https://code.claude.com/docs/en/skills)
- [Claude Code Subagents Docs](https://code.claude.com/docs/en/subagents)
- [Claude Code Plugins Docs](https://code.claude.com/docs/en/plugins)
- [Claude Code Changelog](https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md)

Audit timestamp: 2026-03-08 Asia/Shanghai.

---

## Summary

项目的总体方向与 Claude Code 官方能力是对齐的，但本轮审计前存在 3 个关键兼容性问题：

1. `PreToolUse` matcher 写成了 `BashTool`，而官方 matcher 针对工具名，应使用 `Bash`
2. 债务阻断逻辑使用 `exit 1`，而官方说明 `PreToolUse` 需要 `exit 2` 或显式 deny decision 才会阻断
3. hook 逻辑依赖未在当前文档中说明的 `CLAUDE_TOOL_INPUT` 环境变量，而官方 command hook 输入通过 stdin JSON 传递

这些问题都已经在本轮修复。

---

## Detailed Findings

| Area | Local State Before Audit | Official Guidance | Status |
|------|--------------------------|------------------|--------|
| Hook matcher | `PreToolUse.matcher = "BashTool"` | `PreToolUse` 的 matcher 针对 tool name，示例使用 `Bash` | Fixed |
| Hook blocking semantics | `exit 1` 作为阻断 | 官方文档规定 `exit code 2` 才是 blocking error | Fixed |
| Hook input channel | 依赖 `CLAUDE_TOOL_INPUT` | 官方文档说明 command hooks 通过 stdin 接收 JSON | Fixed |
| Hook script pathing | 逻辑直接内联在 `settings.json` | 官方文档推荐使用 `$CLAUDE_PROJECT_DIR` 引用脚本路径 | Fixed |
| Commands availability | README/CLAUDE 声称有 `/review`，仓库中缺失 | `.claude/commands/review.md` 是合法命令入口 | Fixed |
| Commands invocation control | 现有命令无 frontmatter | 官方文档说明 commands 与 skills 一样支持 frontmatter，适合为副作用流程加 `disable-model-invocation: true` | Fixed |
| Subagent file format | YAML frontmatter + markdown body | 与官方文档一致 | Valid |
| Subagent tool scoping | 已使用 `tools` 字段 | 与官方推荐一致，后续可继续细化 `permissionMode` / `skills` | Valid |
| Skills migration path | 仍以 `.claude/commands/` 为主 | 官方说明 commands 仍可用，但 skills 更推荐 | Accepted as transitional |

---

## What Was Changed

### Hooks

- 将 `SessionStart` 和 `PreToolUse` 的内联 shell 逻辑提取到 `.claude/hooks/`
- `PreToolUse.matcher` 改为 `Bash`
- 债务阻断脚本改为读取 stdin，并用 `exit 2` 阻断 Git 提交/推送

### Commands

- 为现有 commands 增加 frontmatter
- 对所有手动流程命令加上 `disable-model-invocation: true`
- 新增 `/review`，与现有 reviewer subagent 和文档承诺保持一致

### Install Flow

- 安装脚本现在会复制 `.claude/hooks/*.sh`
- 安装输出命名统一为 `NexusRhythm`

---

## Remaining Gaps

1. **尚未迁移到 `.claude/skills/`**
   - 当前 commands 可继续工作
   - 但 complex workflow 未来更适合迁移到 skills，支持 supporting files、forked context 和更细粒度前言字段

2. **缺少 smoke tests**
   - 目前仍缺少自动化验证来确认 hooks/commands/subagents 在干净仓库和新会话中真实可用

3. **文档全量统一尚未完成**
   - README 已对齐
   - GUIDE / HANDBOOK 仍可继续清理旧命名和旧示例

---

## Audit Verdict

**结论：基础兼容性已达可用水平，但还没有达到“可验证、可规模化复用”的成熟度。**

推荐策略：

1. 保持当前 `.claude/commands/` 兼容路径
2. 在 Phase 1 中试点迁移 1 个代表性 workflow 到 skills
3. 在 Phase 2 中建立 smoke tests 和 CI
