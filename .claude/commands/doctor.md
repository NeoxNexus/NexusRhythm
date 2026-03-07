---
description: Run a self-check on the project scaffold, workflow wiring, and phase artifact completeness.
argument-hint: "[quick|full]"
disable-model-invocation: true
---

执行一次项目自检，确认 NexusRhythm 的脚手架、工作流接线和阶段产物是否处于健康状态。

**检查模式**：`$ARGUMENTS`
- `quick`：只做关键存在性和配置检查
- `full`：做完整检查（默认）

---

### Step 1: 核心文件存在性
检查以下文件或目录是否存在：
- `ROADMAP.md`
- `CLAUDE.md`
- `.claude/settings.json`
- `.claude/commands/`
- `.claude/agents/`
- `docs/templates/`

### Step 2: 配置与脚本健康度
执行最小静态检查：
- `python3 -m json.tool .claude/settings.json`
- `bash -n` 检查 `.claude/hooks/*.sh`
- 检查 hooks 脚本是否具备执行权限

### Step 3: 工作流接线检查
确认以下命令与规则已接入：
- `/sync`
- `/phase-start`
- `/gate-check`
- `/phase-end`
- `/review`
- `/idea-review`
- `/doctor`

并检查：
- `README.md`
- `CLAUDE.md`
- `docs/RHYTHM.md`
- `ROADMAP.md`

中是否存在关键规则漂移或缺失说明。

### Step 4: 阶段产物完整性
检查：
- 已完成阶段是否存在对应的 Walkthrough
- 已完成阶段是否存在对应的 Code Review
- `ROADMAP.md` 是否与现有阶段产物状态一致

### Step 5: 点子治理闭环检查
确认：
- `docs/IDEA_BACKLOG.md` 存在
- `docs/IDEA_PORTFOLIO_REVIEW.md` 存在
- `docs/templates/IDEA_REVIEW_TEMPLATE.md` 存在
- 规则已声明“未审查点子不得直接进入 ROADMAP”

### Step 6: 结果汇报
按红黄绿输出结果：

- `GREEN`：结构完整，可继续工作
- `YELLOW`：存在非阻塞缺口，应尽快修正
- `RED`：存在阻塞问题，当前工作流不可信

输出必须包含：
- 检查范围
- 通过项
- 失败项
- 建议修复动作

**禁止**在 `/doctor` 中隐式修改文件；默认只诊断、不修复。
