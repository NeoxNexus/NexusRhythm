<div align="center">
  <img src="https://github.com/NeoxNexus/.github/raw/main/profile/logo.png" alt="NeoxNexus Logo" width="300"/>
  <h1>NeoxNexus</h1>
  <p>Next-Gen AI Ecosystem by Neo</p>
</div>

# NexusRhythm 🎵

> **AI 时代的工程开发节奏** — 让 Claude Code 成为真正懂你项目的搭档

专为 Claude Code CLI 深度集成而设计的项目开发框架。Clone 即用，无需安装。

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
git clone https://github.com/[your-username]/nexus-scaffold.git my-project
cd my-project
rm -rf .git && git init
```

### 已有项目

```bash
# 将框架文件注入已有项目（不覆盖已有文件）
curl -sSL https://raw.githubusercontent.com/[your-username]/nexus-scaffold/main/install.sh | bash
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
│   ├── RHYTHM.md                # 📖 完整开发规范（人类可读）
│   ├── SYSTEM_CONTEXT.md        # 🏗️ 架构决策记录
│   ├── templates/               # 📝 文档模板
│   │   ├── SPEC.md              #   SDD 模板
│   │   ├── WALKTHROUGH.md       #   Walkthrough 模板
│   │   ├── CODE_REVIEW.md       #   Code Review 模板
│   │   ├── JOURNAL.md           #   日志模板
│   │   └── ADR.md               #   架构决策记录模板
│   ├── specs/                   # SDD 文档存放（自动生成）
│   ├── walkthroughs/            # Walkthrough 存放（自动生成）
│   ├── reviews/                 # Code Review 存放（自动生成）
│   ├── journal/                 # 每日日志（YYYY-MM-DD.md）
│   └── decisions/               # ADR 记录
│
└── .claude/
    ├── settings.json            # ⚙️ Hooks 配置
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
会话开始 → /sync → 确认状态
     ↓
开新功能 → /phase-start → (architect 写 SPEC + 红灯测试)
     ↓
实现代码 → 编码直到测试绿灯
     ↓
准备提交 → /gate-check → 三门禁全通过
     ↓
阶段结束 → /phase-end → (reviewer 评审) → /retro → /distill
     ↓
下个阶段循环 ↑
```

---

## 📄 License

MIT
