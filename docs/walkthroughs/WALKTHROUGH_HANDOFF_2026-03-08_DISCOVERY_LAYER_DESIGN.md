# WALKTHROUGH — Session Handoff: Discovery Layer Design

**日期**：2026-03-08
**适用对象**：接手当前设计并负责整合落地的 agent / 协作者
**范围**：本次会话仅完成设计收口，未修改实现逻辑
**落点目录**：`docs/walkthroughs/`

---

## 1. 本次会话的核心结论

本轮会话围绕一个明确问题展开：`NexusRhythm` 现阶段非常擅长在目标已清晰的前提下做高质量交付，但对“用户只有一个模糊 idea”这一入口支持不足。

最终结论是：

- 项目当前强项仍应定义为 `Delivery Rhythm`，即 `ROADMAP + SPEC + RED TESTS + GATE CHECK + REVIEW + DISTILL` 这一套工程节奏。
- 当前缺口不在交付段，而在交付前的 `Idea Discovery / MVP Shaping / Roadmap Init`。
- 不建议用“把 Discovery 强塞进 Phase 0”的方式修补。
- 更稳妥的做法是保留现有 Phase 状态机，同时在其之上增加一个**项目级状态机**，把模糊想法收敛为可进入 Delivery 的项目定义。

一句话设计方向：

`Idea Discovery -> MVP Shaping -> Roadmap Init -> Existing Delivery Rhythm`

---

## 2. 已确认的设计原则

后续实现应遵循以下原则：

- 不推翻现有 `Phase_Status` 流程，避免破坏当前项目最成熟的交付内核。
- 新增一层 `Project_Stage`，专门承载 idea 到 roadmap 的前置收敛。
- Discovery 阶段优先定义“问题和边界”，而不是过早讨论技术方案。
- 进入 `/phase-start` 前必须满足最小定义条件，避免把模糊想法直接推进到实现阶段。
- 所有 Discovery 产物都要落成文件，不能只停留在对话里。
- `SPEC` 必须可以追溯到上游的 idea 和 MVP 定义，防止后续 scope 漂移。

---

## 3. 推荐采用的状态模型

### 项目级状态机（新增）

建议在 `ROADMAP.md` YAML 中新增：

- `Project_Stage: IDEA | DISCOVERY | MVP_DEFINED | ROADMAP_READY | DELIVERY`
- `Idea_Clarity: 1-5`
- `Target_User`
- `Core_Problem`
- `Success_Metrics`
- `Primary_Risk`

说明：

- `Project_Stage` 管“项目定义成熟度”
- `Phase_Status` 管“当前阶段交付状态”
- 两者并列存在，不互相替代

### 阶段级状态机（保留现有）

继续保留：

`PLANNING -> SPEC_READY -> RED_TESTS -> GREEN_CODE -> GATE_CHECK -> REVIEW -> DONE`

### 进入 Delivery 的最小条件

只有满足以下条件，才允许切到 `Project_Stage: DELIVERY` 并进入 `/phase-start`：

- 有一句话价值主张
- 有明确目标用户
- 有非目标清单
- 有至少 2 个成功指标
- 有明确的 `Phase 1` 单一目标

---

## 4. 本轮达成的一致设计：逐文件改造范围

### 4.1 需要修改的现有文件

#### `ROADMAP.md`

职责调整：

- 从“阶段真相源”扩展为“项目定义 + 阶段真相源”

建议修改：

- YAML 增加 `Project_Stage`、`Idea_Clarity`、`Target_User`、`Core_Problem`、`Success_Metrics`、`Primary_Risk`
- 增加一段 `Discovery 摘要`
- 保留现有 Phase 仪表盘，不改动其基本职责

#### `docs/SYSTEM_CONTEXT.md`

职责调整：

- 从“架构上下文模板”升级为“项目定义 + 架构上下文”的承接文件

建议修改：

- 强化第 1 节：项目定位与核心价值主张
- 新增“首批用户与核心场景”
- 新增“非目标与范围边界”
- 新增“验证路径”

#### `CLAUDE.md`

职责调整：

- 在会话启动协议中接入 Discovery 规则

建议修改：

- 如果 `Project_Stage != DELIVERY`，优先引导 `/idea-capture`、`/mvp-shape`、`/roadmap-init`
- 如果 `Idea_Clarity < 3`，拒绝 `/phase-start`
- 当用户直接要求编码但项目仍处于 Discovery 时，必须先收敛问题定义

#### `README.md`

职责调整：

- 对外叙事从“开发节奏框架”升级为“从 idea 到高质量落地的 AI 协作框架”

建议修改：

- 增加总流程图
- 更新命令速查，把 Discovery commands 放在 `/phase-start` 之前
- 增加“适合什么样的用户”说明，覆盖模糊 idea 用户

#### `docs/GUIDE.md`

职责调整：

- 增加“模糊想法如何启动”的说明章节

建议修改：

- 新增 `如果你现在只有一个模糊想法`
- 明确 `IDEA_BRIEF -> MVP_CANVAS -> ROADMAP_INIT -> phase-start`

#### `docs/HANDBOOK.md`

职责调整：

- 把初始化流程升级为 `Discovery + Delivery` 双段式

建议修改：

- 将“初始化三步走”改成 “Discovery 三步走 + Delivery 三步走”
- 增加典型路径与失败回退路径

#### `docs/templates/SPEC.md`

职责调整：

- 增加上游追溯能力

建议修改：

- 新增 `Upstream Idea Brief`
- 新增 `Upstream MVP Canvas`
- 新增 `Mapped Success Metric`
- 新增 `Why This Phase Now`

#### `.claude/commands/phase-start.md`

职责调整：

- 接入项目级前置门禁

建议修改：

- 增加 `Project_Stage == DELIVERY` 检查
- 增加 `Idea_Clarity >= 3` 检查
- 如果失败，明确指出先执行哪个 Discovery command

#### `.claude/commands/spec.md`

职责调整：

- 生成 SPEC 时必须读取 Discovery 产物

建议修改：

- 增加对 `IDEA_BRIEF`、`MVP_CANVAS` 的读取
- 若功能超出 MVP，必须提示 scope 漂移

### 4.2 需要新增的文件

#### `docs/templates/IDEA_BRIEF_TEMPLATE.md`

职责：

- 把原始模糊描述转为结构化问题定义

建议字段：

- 原始 idea
- 一句话价值主张
- 目标用户
- 触发场景
- 核心痛点
- 当前替代方案
- 为什么是现在
- 未知项
- `Idea_Clarity`

#### `docs/templates/MVP_CANVAS_TEMPLATE.md`

职责：

- 把问题定义压缩成最小可验证产品

建议字段：

- 北极星目标
- 首批用户
- 核心用户旅程
- In Scope
- Out of Scope
- 成功指标
- 失败信号
- 关键风险
- 验证方式

#### `docs/templates/ROADMAP_INIT_TEMPLATE.md`

职责：

- 从 MVP 推出前 3 个阶段的初版路线图

建议字段：

- `Phase 0` 初始化与验证准备
- `Phase 1` 最小价值闭环
- `Phase 2` 稳定性与反馈闭环
- `Phase 3` 扩展能力或商业验证

#### `docs/ideas/README.md`

职责：

- 说明 Discovery 目录和文档关系

建议包含：

- 文件命名规范
- 文档生成顺序
- 哪些文档被后续命令消费

#### `.claude/agents/product-strategist.md`

职责：

- 作为 Discovery 主 agent

设计要求：

- 先澄清问题，不急于给技术方案
- 识别 scope 膨胀并主动收缩
- 输出结构化产物，而不是长篇咨询式对话
- 不负责编码、不负责测试、不触发 reviewer

#### `.claude/commands/idea-capture.md`

职责：

- 生成 `IDEA_BRIEF`

设计要点：

- 接受非常模糊的输入
- 输出 `Idea_Clarity` 和最大未知项
- 回写 `ROADMAP.md` 中的项目级字段

#### `.claude/commands/mvp-shape.md`

职责：

- 生成 `MVP_CANVAS`

设计要点：

- 强制写清 `Out of Scope`
- 强制写清成功指标和失败信号
- 默认优先收窄范围

#### `.claude/commands/roadmap-init.md`

职责：

- 生成初版 `ROADMAP` 和 `SYSTEM_CONTEXT` 项目定义段

设计要点：

- 读取 `IDEA_BRIEF + MVP_CANVAS + SYSTEM_CONTEXT`
- 只生成前 3 个阶段，不追求伪精确大路线图
- 明确给出 `Phase 1` 单一目标

#### `.claude/commands/idea-review.md`

职责：

- 进入 Delivery 前做一次 idea / scope 复核

建议检查：

- MVP 是否仍然过大
- 成功指标是否可验证
- `Phase 1` 是否承担过多责任

---

## 5. Discovery 与 Delivery 的衔接规则

这是本轮设计里最重要的约束之一，后续实现不要放松：

- `Discovery` 产物不等于 `SPEC`
- `SPEC` 只服务当前 Phase 的工程实现
- `IDEA_BRIEF` 和 `MVP_CANVAS` 负责回答“为什么做、为谁做、先做到什么程度”
- `SPEC` 负责回答“这个阶段具体实现什么、接口是什么、边界是什么”

推荐衔接链路：

`/idea-capture -> /mvp-shape -> /roadmap-init -> /phase-start -> /spec -> code -> /gate-check -> /phase-end -> /distill`

---

## 6. 推荐给下一个 agent 的实施顺序

不要一上来同时改所有文件。建议按以下顺序推进：

1. 先修改 `ROADMAP.md`、`CLAUDE.md`、`docs/SYSTEM_CONTEXT.md`
2. 再新增 `IDEA_BRIEF_TEMPLATE`、`MVP_CANVAS_TEMPLATE`、`ROADMAP_INIT_TEMPLATE`
3. 再新增 `product-strategist` 与 3 个核心 commands
4. 然后补 `README.md`、`docs/GUIDE.md`、`docs/HANDBOOK.md`
5. 最后改 `SPEC` 与 `phase-start/spec` 的衔接规则

理由：

- 先把状态机和入口守门立住
- 再补前置产物模板
- 再接入 command/agent 自动化
- 最后统一对外叙事和文档说明

---

## 7. 下一个 agent 的最小执行集合

如果下一个 agent 只想快速接棒，不重复阅读整段对话，最小需要理解以下事项：

- 本轮不是在推进“命令脚本化”或“执行层工程化”，而是在设计**模糊 idea 的前置收敛层**
- 设计的核心不是新增一个“更大的 Phase 0”，而是新增项目级 `Project_Stage`
- Discovery 产物最少包括：`IDEA_BRIEF`、`MVP_CANVAS`、`ROADMAP_INIT`
- 现有 Delivery 内核应尽量保持不动，重点是接入前置层
- `phase-start` 以后才进入现有的高纪律工程流程

---

## 8. 风险与待确认事项

后续落地前仍有两个需要保持注意的点：

- 现有仓库中已经存在其他演进方向文档和 handoff，不要把本轮“Discovery Layer 设计”与之前“执行层工程化路线”混成同一件事
- 用户消息中出现过 `docs/walkthrougs/` 的拼写，但仓库实际目录是 `docs/walkthroughs/`，本次已统一写入正确目录

待确认但不阻塞当前设计的事项：

- `docs/templates/SPEC.md` 是否应同步重命名为 `SPEC_TEMPLATE.md`
- `idea-review` 是否作为必选命令接入，还是先作为可选守门步骤
- `ROADMAP.md` 是否同时需要展示项目级状态图

---

## 9. 本次会话未做的事

为了避免误判，下一个 agent 需要知道本次没有做以下工作：

- 没有修改任何 `.claude/commands/` 实现文件
- 没有新增任何 Discovery 模板
- 没有运行测试
- 没有更新 `ROADMAP.md`、`README.md`、`CLAUDE.md`

本次产出仅为设计与 handoff 收口。

---

## 10. 建议下一步

最合理的下一步不是继续讨论抽象思路，而是：

1. 先把本 handoff 中列出的逐文件设计转换成一份正式设计文档
2. 再按第 6 节的顺序逐步修改仓库
3. 每完成一类改造后都补一次小型 handoff，防止后续 agent 漏掉最近演进

如果只做一个最小切口，建议从以下三件事开始：

- 在 `ROADMAP.md` 增加 `Project_Stage`
- 新增 `docs/templates/IDEA_BRIEF_TEMPLATE.md`
- 新增 `.claude/commands/idea-capture.md`

这三项一旦落地，模糊 idea 用户就已经有一个正式入口。
