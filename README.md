<div align="center">
  <img src="https://avatars.githubusercontent.com/u/258567441?v=4" alt="NexusRhythm Logo" width="300"/>
  <h1>NexusRhythm</h1>
  <p>Claude Code workflow scaffold by Neo</p>
</div>

> **AI 时代的工程开发节奏** — 让 Claude Code 成为真正懂你项目的搭档

专为 Claude Code 深度集成而设计的项目开发框架。Clone 即用，也支持注入到已有项目。当前工作流由 `ROADMAP.md` 状态机和 `scripts/nr.py` 执行层共同驱动：先用 Discovery 把想法收敛清楚，再进入 Delivery 做高纪律交付。

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
| 🧭 **Discovery 入口** | `IDEA_BRIEF → MVP_CANVAS → ROADMAP_INIT` 把模糊想法收敛成可执行路线 |
| 🛠️ **脚本执行层** | `scripts/nr.py` 统一承接状态读写、门禁检测、自检和 Discovery/Delivery 命令执行 |
| 🧱 **防回退保护** | 一旦项目进入 `DELIVERY`，会拒绝误触发 Discovery 命令把状态机打回前期 |
| 🔥 **热记忆骨架** | `.nexus/memory/` 保存 today / active tasks / blockers / handoff，支持跨会话接力 |

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
# 在你的项目根目录执行（不覆盖已有文件）
curl -fsSL https://raw.githubusercontent.com/NeoxNexus/NexusRhythm/main/install.sh | bash

# 指定目标目录
curl -fsSL https://raw.githubusercontent.com/NeoxNexus/NexusRhythm/main/install.sh | bash -s -- /path/to/project

# 如果你已经 clone 了仓库，也可以直接运行
bash install.sh /path/to/project
```

### 初始化你的项目

1. 编辑 `ROADMAP.md`，填写项目名称、目标和技术栈
2. 编辑 `docs/SYSTEM_CONTEXT.md`，描述架构决策
3. 用 Claude Code 打开项目，输入 `/sync` 开始第一次会话
4. 建议立刻执行一次 `/doctor`，先确认 commands、templates、hooks 和脚手架接线完整

如果你现在只有一个模糊 idea：

1. `/idea-capture`
2. `/mvp-shape`
3. `/roadmap-init`
4. 将 `Project_Stage` 切到 `DELIVERY` 后，再运行 `/phase-start`

### Mode 2 使用前先确认

- Node.js 项目：请在 `package.json` 中提供 `coverage:check`、`test:coverage` 或 `coverage` 之一，否则 `Mode 2` 下的 `/gate-check` 会直接失败
- Python 项目：脚本会优先探测并使用 `pytest`；未探测到时才回退到 `unittest`
- 发版前建议至少执行一次 `/doctor` 和 `/gate-check`，分别确认脚手架完整性和宿主项目质量门禁

---

## 📁 目录结构

```
project/
├── CLAUDE.md                    # 🧠 Claude Code 控制面（每次自动加载）
├── ROADMAP.md                   # 📊 项目状态机（唯一真相源）
├── CHANGELOG.md                 # 📝 发布记录
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
│   │   ├── IDEA_BRIEF_TEMPLATE.md # Discovery brief 模板
│   │   ├── MVP_CANVAS_TEMPLATE.md # MVP 画布模板
│   │   ├── ROADMAP_INIT_TEMPLATE.md # Discovery 路线初始化模板
│   │   ├── WALKTHROUGH_TEMPLATE.md # Walkthrough 模板
│   │   ├── CODE_REVIEW_TEMPLATE.md # Code Review 模板
│   │   ├── JOURNAL_TEMPLATE.md  #   日志模板
│   │   ├── IDEA_REVIEW_TEMPLATE.md # 点子评审模板
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
    │   ├── change-auditor.md    # 🧾 变更审计 Agent
    │   ├── product-strategist.md # 🧭 Discovery Agent
    │   ├── reviewer.md          # 🔍 评审 Agent
    │   └── debt-collector.md    # 🧹 债务清理 Agent
    ├── rules/
    │   ├── lessons.md           # 🧠 项目教训（自动加载）
    │   └── conventions.md       # 📐 项目约定（自动加载）
    └── commands/
        ├── sync.md              # /sync
        ├── idea-capture.md      # /idea-capture
        ├── mvp-shape.md         # /mvp-shape
        ├── roadmap-init.md      # /roadmap-init
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
│
├── scripts/
│   └── nr.py                    # 🛠️ 状态读写、门禁、自检和 Discovery/Delivery 脚本入口
│
└── .nexus/
    ├── tasks/                   # 📦 阶段内任务粒度
    └── memory/                  # 🔥 热记忆（today / active tasks / blockers / handoff）
```

---

## 🎮 命令速查

| 命令 | 场景 | 说明 |
|------|------|------|
| `/sync` | 每次会话开始 | 读取并报告项目当前状态 |
| `/idea-capture` | 只有一个模糊想法 | 生成 `IDEA_BRIEF`，进入 Discovery |
| `/mvp-shape` | 收窄 MVP | 生成 `MVP_CANVAS`，明确 `Out Of Scope` |
| `/roadmap-init` | 准备立项 | 生成前三阶段路线草案 |
| `/phase-start [名称]` | 开新阶段 | 检查前置条件 → 召唤 architect → 写 SPEC 和红灯测试 |
| `/spec [功能名]` | 需要 SDD | 基于模板生成 SDD，自动填充数据流和边界条件 |
| `/gate-check` | 准备提交 | 三门禁：类型检查 + 构建 + 全量测试；Mode 2 下额外执行更严格 lint/coverage 检查 |
| `/review` | 需要独立评审时 | 手动触发 reviewer，输出审计结论 |
| `/idea-review` | 阶段结束前 | 审核 backlog 中的点子，合格后再同步计划 |
| `/doctor` | 会话早期或修复后 | 自检脚手架、hooks、commands、templates 和阶段材料是否健康 |
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
| `2` Production | 公开 API / 安全敏感 | 模式 1 + 更严格 lint/coverage 门禁 + reviewer 必须通过 |

---

## 💡 推荐工作流

### 一句话理解

- `Discovery` 负责把项目想清楚
- `Delivery` 负责把每个阶段做扎实

### 最短主线

```text
模糊想法
  -> /idea-capture
  -> /mvp-shape
  -> /roadmap-init
  -> 手动切到 DELIVERY
  -> /phase-start
  -> /spec
  -> 红灯测试
  -> 绿灯实现
  -> /gate-check
  -> /phase-end
  -> /retro -> /idea-review -> /distill
```

### 关键状态怎么理解

| 状态 | 它表示什么 |
|------|------------|
| `Project_Stage` | 项目是否已经想清楚了：`IDEA -> DISCOVERY -> MVP_DEFINED -> ROADMAP_READY -> DELIVERY` |
| `Phase_Status` | 当前开发阶段做到哪一步：`PLANNING -> SPEC_READY -> RED_TESTS -> GREEN_CODE -> GATE_CHECK -> REVIEW -> DONE` |
| `Pending_Debt` | 是否存在未清技术债；如果为 `true`，先清债，不开新功能 |
| `Active_Mode` | 当前工作模式：`0` 放飞、`1` 标准、`2` 生产 |

### 每个命令什么时候用

| 命令 | 触发时机 |
|------|----------|
| `/sync` | 每次新会话开始时 |
| `/doctor` | 安装后、修复后、发版前 |
| `/idea-capture` | 只有模糊 idea 时 |
| `/mvp-shape` | 已有 `IDEA_BRIEF`，需要收窄 MVP 时 |
| `/roadmap-init` | 已有 `IDEA_BRIEF` 和 `MVP_CANVAS` 时 |
| `/phase-start` | 项目已经进入 `DELIVERY`，准备开启新阶段时 |
| `/spec` | 阶段启动后，先定义契约时 |
| `/gate-check` | 准备提交或阶段收口前 |
| `/phase-end` | 三门禁通过、准备结束阶段时 |
| `/retro` `/idea-review` `/distill` | 阶段结束后的复盘与沉淀 |

### 当前实现里的几个关键保护

| 保护项 | 当前行为 |
|--------|----------|
| Discovery 防回退 | 项目已在 `DELIVERY` 时，`/idea-capture`、`/mvp-shape`、`/roadmap-init` 会拒绝执行 |
| `/doctor` 严格自检 | 会检查核心命令、模板、hooks 和关键路径，不再只看目录是否存在 |
| Python 测试探测 | 优先识别 `pytest` 项目；否则回退到 `unittest` |
| Node Mode 2 门禁 | 必须提供显式 coverage 脚本，否则 `/gate-check` 直接失败 |

### 失败时该回哪里

| 如果这一步失败 | 通常说明什么 | 应该怎么做 |
|----------------|--------------|------------|
| `/phase-start` 被拒绝 | 项目还没进入 `DELIVERY`，或上一阶段没收干净 | 回 Discovery 或先补阶段收尾 |
| `/gate-check` 失败 | 类型检查、构建或测试没过 | 修复后重新跑 |
| `/phase-end` 失败 | 缺阶段产物或门禁未过 | 先补 `WALKTHROUGH` / `CODE_REVIEW` 再结束 |
| Discovery 命令被拒绝 | 项目已经在 `DELIVERY` | 不要回退状态机，改去补 backlog 或调整规划 |

## 🗂️ 文档命名规则

- 根入口文档使用固定名称：`GUIDE.md`、`HANDBOOK.md`、`RHYTHM.md`、`SYSTEM_CONTEXT.md`
- 模板统一使用 `TYPE_TEMPLATE.md`
- 阶段文档分别使用 `SPEC_PHASE_N_*.md`、`WALKTHROUGH_PHASE_N.md`、`CODE_REVIEW_PHASE_N.md`
- ADR 使用 `ADR-NNN-*.md`，Journal 使用 `YYYY-MM-DD.md`
- `docs/assessments/`、`docs/designs/`、`docs/ideas/`、`docs/plans/` 下统一使用 `SCREAMING_SNAKE_CASE.md`

---

## 📄 License

MIT
