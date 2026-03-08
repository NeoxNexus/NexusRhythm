<div align="center">
  <img src="https://avatars.githubusercontent.com/u/258567441?v=4" alt="NexusRhythm Logo" width="300"/>
  <h1>NexusRhythm</h1>
  <p>Claude Code workflow scaffold by Neo</p>
</div>

> **AI 时代的工程开发节奏** — 让 Claude Code 成为真正懂你项目的搭档

专为 Claude Code 深度集成而设计的项目开发框架。Clone 即用，也支持注入到已有项目。

---

## ✨ 核心特性

| 特性 | 说明 |
|------|------|
| 🧠 **会话记忆** | `.claude/rules/` 自动加载项目教训，AI 每次启动都记得上次踩的坑 |
| 🤖 **多智能体分工** | architect（设计）→ reviewer（评审）→ debt-collector（清债） |
| 📋 **状态机驱动** | ROADMAP.md YAML 头部管理阶段状态，禁止跳步 |
| 🚦 **三门禁保障** | 类型检查 + 构建 + 全量测试，直接挂钩 git commit |
| ⚗️ **记忆蒸馏闭环** | Journal → ADR → Walkthrough → `/distill` → Rules → 影响行为 |
| 🏄 **Vibe Sprint** | 每 3 个阶段解锁一次放飞资格，有序管理技术债务 |

---

## 🚀 快速开始

### 新项目（推荐）

```bash
# 方式 1：GitHub Template（点击右上角 "Use this template"）
# 方式 2：直接 clone
git clone https://github.com/NeoxNexus/NexusRhythm.git my-project
cd my-project
rm -rf .git && git init
```

### 已有项目

```bash
# 将框架文件注入已有项目（不覆盖已有文件）
curl -sSL https://raw.githubusercontent.com/NeoxNexus/NexusRhythm/main/install.sh | bash
```

### 初始化你的项目

1. 编辑 `ROADMAP.md`，填写项目名称、目标和技术栈
2. 编辑 `docs/SYSTEM_CONTEXT.md`，描述架构决策
3. 用 Claude Code 打开项目，输入 `/sync` 开始第一次会话

---

## 📁 目录结构

```
project/
├── CLAUDE.md                    # 🧠 Claude Code 控制面（每次自动加载）
├── ROADMAP.md                   # 📊 项目状态机（唯一真相源）
│
├── docs/
│   ├── GUIDE.md                 # 📘 项目快速指南
│   ├── HANDBOOK.md              # 📗 人类协作手册
│   ├── RHYTHM.md                # 📖 完整开发规范（人类可读）
│   ├── SYSTEM_CONTEXT.md        # 🏗️ 架构决策记录
│   ├── assessments/             # 🧪 项目评估与合规审计
│   ├── designs/                 # 🧭 工作流与机制设计文档
│   ├── ideas/                   # 💡 点子收集与评审结果
│   ├── plans/                   # 🗺️ 阶段计划与执行方案
│   ├── templates/               # 📝 文档模板
│   │   ├── SPEC_TEMPLATE.md     #   SDD 模板
│   │   ├── WALKTHROUGH_TEMPLATE.md # Walkthrough 模板
│   │   ├── CODE_REVIEW_TEMPLATE.md # Code Review 模板
│   │   ├── JOURNAL_TEMPLATE.md  #   日志模板
│   │   └── ADR_TEMPLATE.md      #   架构决策记录模板
│   ├── specs/                   # SDD 文档（SPEC_PHASE_N_*.md）
│   ├── walkthroughs/            # 阶段 walkthrough（WALKTHROUGH_PHASE_N.md）
│   ├── reviews/                 # 阶段 review（CODE_REVIEW_PHASE_N.md）
│   ├── journal/                 # 每日日志（YYYY-MM-DD.md）
│   └── decisions/               # ADR 记录（ADR-NNN-*.md）
│
└── .claude/
    ├── settings.json            # ⚙️ Hooks 配置
    ├── hooks/                   # 🪝 可复用 hook 脚本
    ├── agents/
    │   ├── architect.md         # 🏛️ 架构师 Agent
    │   ├── reviewer.md          # 🔍 评审 Agent
    │   └── debt-collector.md    # 🧹 债务清理 Agent
    ├── rules/
    │   ├── lessons.md           # 🧠 项目教训（自动加载）
    │   └── conventions.md       # 📐 项目约定（自动加载）
    └── commands/
        ├── sync.md              # /sync
        ├── phase-start.md       # /phase-start
        ├── phase-end.md         # /phase-end
        ├── gate-check.md        # /gate-check
        ├── idea-review.md       # /idea-review
        ├── doctor.md            # /doctor
        ├── spec.md              # /spec [功能名]
        ├── retro.md             # /retro
        ├── journal.md           # /journal
        ├── decision.md          # /decision [主题]
        └── distill.md           # /distill
```

---

## 🎮 命令速查

| 命令 | 场景 | 说明 |
|------|------|------|
| `/sync` | 每次会话开始 | 读取并报告项目当前状态 |
| `/phase-start [名称]` | 开新阶段 | 检查前置条件 → 召唤 architect → 写 SPEC 和红灯测试 |
| `/spec [功能名]` | 需要 SDD | 基于模板生成 SDD，自动填充数据流和边界条件 |
| `/gate-check` | 准备提交 | 三门禁：类型检查 + 构建 + 全量测试 |
| `/review` | 需要独立评审时 | 手动触发 reviewer，输出审计结论 |
| `/idea-review` | 阶段结束前 | 审核 backlog 中的点子，合格后再同步计划 |
| `/doctor` | 会话早期或修复后 | 自检脚手架、hooks、commands 和阶段材料是否健康 |
| `/phase-end` | 阶段完工 | 三门禁 → 更新 ROADMAP → Walkthrough → 召唤 reviewer |
| `/retro` | 阶段结束后 | 引导 2 分钟小复盘并记录 |
| `/journal` | 每天 | 快速记录今日进展和踩坑 |
| `/decision [主题]` | 重要决策后 | 生成 ADR，更新 SYSTEM_CONTEXT 索引 |
| `/distill` | 每 3 个阶段 | 蒸馏教训到 `.claude/rules/`，构成记忆闭环 |

---

## ⚙️ 工作模式

| Mode | 场景 | 约束 |
|:----:|------|------|
| `0` Vibe | 周末实验 / 快速原型 | 解除门禁；产生债务时设 `Pending_Debt: true` |
| `1` Standard | 核心功能（默认）| SDD 先行 → 红灯测试 → 三门禁 |
| `2` Production | 公开 API / 安全敏感 | 模式 1 + 覆盖率 ≥80% + reviewer 必须通过 |

---

## 💡 推荐工作流

```
会话开始 → /sync → /doctor（可选）→ 确认状态
     ↓
开新功能 → /phase-start → (architect 写 SPEC + 红灯测试)
     ↓
实现代码 → 编码直到测试绿灯
     ↓
准备提交 → /gate-check → 三门禁全通过
     ↓
阶段结束 → /phase-end → (reviewer 评审) → /retro → /idea-review → /distill
     ↓
下个阶段循环 ↑
```

## 🗂️ 文档命名规则

- 根入口文档使用固定名称：`GUIDE.md`、`HANDBOOK.md`、`RHYTHM.md`、`SYSTEM_CONTEXT.md`
- 模板统一使用 `TYPE_TEMPLATE.md`
- 阶段文档分别使用 `SPEC_PHASE_N_*.md`、`WALKTHROUGH_PHASE_N.md`、`CODE_REVIEW_PHASE_N.md`
- ADR 使用 `ADR-NNN-*.md`，Journal 使用 `YYYY-MM-DD.md`
- `docs/assessments/`、`docs/designs/`、`docs/ideas/`、`docs/plans/` 下统一使用 `SCREAMING_SNAKE_CASE.md`

---

## 📄 License

MIT
