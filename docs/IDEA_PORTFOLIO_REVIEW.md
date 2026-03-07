# Idea Portfolio Review

**Date**: 2026-03-08  
**Reviewer**: Change Auditor rubric + Codex  
**Input Source**: [IDEA_BACKLOG.md](/Users/neo/.codex/worktrees/7a12/NexusRhythm/docs/IDEA_BACKLOG.md)

---

## Review Method

对每个点子按以下维度做审查：

1. **与当前阶段是否匹配**
2. **是否解决已证实的问题，而不是凭感觉优化**
3. **实现成本是否适合当前项目体量**
4. **是否会引入过早产品化或过早架构化**

结论分为：

- `Approved Now`：应尽快纳入近阶段计划
- `Approved Later`：方向正确，但不应现在做
- `Hold`：信息不足或收益不确定
- `Reject`：当前不建议推进

---

## Portfolio Decisions

| Idea | Decision | Reason |
|------|----------|--------|
| 最关键命令迁移为 skills + scripts | Approved Now | 直接对应当前“prompt 约束过重”的核心问题 |
| nightly 官方文档对照脚本 | Approved Later | 有价值，但先有 smoke tests 再做持续监测更合理 |
| hooks smoke tests | Approved Now | 这是当前最短板，也是 Phase 1 最核心任务 |
| `/doctor` 或 `/self-check` | Approved Now | 对安装与自检价值高，且实现边界清晰 |
| Phase 0 向导 | Approved Later | 提升首次体验明显，但优先级低于可靠性 |
| 重构 README / GUIDE / HANDBOOK 分层 | Approved Later | 文档体系已够用，但可在产品化前做 |
| reviewer 预加载 skill | Hold | 方向合理，但需先确定 skills 迁移模式 |
| debt-collector 缺口扫描脚本 | Approved Later | 有用，但依赖更稳定的 SPEC / review / walkthrough 产物基础 |
| 引入统一 machine-readable metadata | Hold | 有潜在收益，但会引入 ROADMAP 结构重构，不适合当前阶段 |
| demo repo | Approved Later | 对外产品化前必须有，但当前优先级低于核心兼容性 |
| 升级为 plugin | Hold | 战略性方向，当前证据不足，时机也偏早 |
| 轻量模式路径 | Hold | 需要更多真实用户/使用场景数据支撑 |
| install --upgrade | Approved Later | 分发成熟后很重要，但当前安装链路先保证首次注入稳定 |
| 三种安装方式分别写文档 | Approved Later | 适合产品化阶段推进 |
| 版本号与升级日志 | Approved Later | 分发稳定后应当补齐 |

---

## Approved Now

### 1. Hooks smoke tests

**为什么现在做**  
这是当前最直接的可靠性缺口。没有它，兼容性修复仍然缺乏行为级验证。

**计划落点**
- Phase 1
- 验证 `SessionStart` 是否能读取 ROADMAP
- 验证 `Pending_Debt: true` 时 Git 提交/推送被阻断
- 验证无 ROADMAP 时 hook 安静退出

### 2. 关键流程迁移为 skills + scripts

**为什么现在做**  
官方已把 commands 和 skills 合并到统一能力模型，继续只堆 `.claude/commands/` 会限制可扩展性。

**计划落点**
- Phase 1 试点迁移一个流程，不全量迁移
- 建议先试点 `/review` 或 `/doctor`
- 迁移后保留旧 commands 兼容入口，避免破坏已有路径

### 3. `/doctor` 或 `/self-check`

**为什么现在做**  
这类工程最怕“装了但没真生效”。一个诊断入口能显著降低使用摩擦，也方便排查环境问题。

**计划落点**
- Phase 1 或 Phase 2 早期
- 检查 `ROADMAP.md`、`.claude/settings.json`、hooks、commands、agents、templates、安装结果
- 输出红黄绿状态，不做隐式修复

---

## Approved Later

这些方向已确认值得做，但应在 hooks smoke tests 和最小 skills 试点之后推进：

- nightly 官方文档对照脚本
- Phase 0 向导
- README / GUIDE / HANDBOOK 分层重构
- debt-collector 缺口扫描脚本
- demo repo
- install --upgrade
- 分安装方式文档
- 版本号与升级日志

---

## Hold / Not Yet

- reviewer 预加载 skill：需先确定 skills 试点模式
- plugin 化：偏战略动作，当前没有足够验证基础
- 轻量模式：需要真实使用反馈决定是否值得引入分叉路径
- machine-readable metadata：重构收益不明，且会增加状态源复杂度

---

## Evolution Recommendation

基于当前审查，建议把 `IDEA_BACKLOG` 的近阶段演进压缩成一条更克制的路径：

1. 先建立 hooks smoke tests
2. 再做一个 `doctor` 自检入口
3. 然后试点迁移一个 command 到 skill
4. 最后再做文档分层和分发增强

这条路径和当前 Phase 1 / Phase 2 规划是一致的，也更符合“先解决已证实风险，再扩展体验”的原则。
