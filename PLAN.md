# NexusRhythm 整合计划：从 Phase 0 基线到 Discovery + Execution 双层演进

## Summary

- 以三份 handoff 的共同结论为基线：`Delivery Rhythm` 是现有产品内核，短板在“执行层工程化”和“模糊 idea 的前置收敛”。
- 不把 Discovery 设计直接塞回现有 Phase 0，也不把 Discovery 与执行层脚本化混成同一阶段实现；两者都改控制面，但目标不同，强行同做会让 Phase 1 失焦。
- 集成后的执行顺序定为：先把现有 Delivery 内核做成可验证、可脚本化的确定性系统，再在其上加 `Project_Stage` 驱动的 Discovery 前置层，随后补 Task / Hot Memory，最后再做评审路由、并行、CLI 和 preset。

## Implementation Changes

### 1. 立即阶段：锁定现有内核并完成行为级验证
- 保持 `ROADMAP.md` 当前承诺不变，下一阶段先执行现有 Phase 1 的“Claude Code 兼容性加固”。
- 将 `/sync`、`/phase-start`、`/gate-check`、`/phase-end`、`/distill` 的核心逻辑下沉到 `scripts/`，命令文档只保留人工入口和编排语义。
- 为 hooks、`/doctor`、安装流程和核心命令补行为级 smoke tests，替代“只验证文档和 shell 语法”的现状。
- 先完成这一层，再动 Discovery；否则后续新增的 `Project_Stage`、模板和命令仍会停留在 prompt 约束，重复当前短板。

### 2. 控制面收口：统一仓库真相源和命名契约
- 明确 `ROADMAP.md` 继续作为项目状态 SSOT，`Phase_Status` 只负责 Delivery 节奏，不承担 idea 收敛职责。
- 收口文档与命令引用的真实文件名，统一以仓库现状为准：`docs/templates/SPEC_TEMPLATE.md`、`docs/walkthroughs/`、现有 `.claude/commands/*.md`。
- 在 `docs/SYSTEM_CONTEXT.md` 或 `docs/RHYTHM.md` 补一张“状态字段 / 命令 / 产物”的职责表，避免后续 `Project_Stage` 和 `Phase_Status` 混用。
- 保留现有 `/idea-review` 的 backlog 准入职责，不在第一版里复用它做 Discovery 守门，避免一个命令承担两种不同语义。

### 3. Discovery Layer MVP：在 Delivery 之上新增项目级状态机
- 在 `ROADMAP.md` YAML 增加项目级字段：`Project_Stage`、`Idea_Clarity`、`Target_User`、`Core_Problem`、`Success_Metrics`、`Primary_Risk`。
- 新增 Discovery 产物模板：`IDEA_BRIEF_TEMPLATE.md`、`MVP_CANVAS_TEMPLATE.md`、`ROADMAP_INIT_TEMPLATE.md`，并补 `docs/ideas/README.md` 说明生成顺序和消费关系。
- 新增 `product-strategist` agent，职责限定为问题澄清、范围收窄、输出结构化产物，不参与编码或评审。
- 新增 `/idea-capture`、`/mvp-shape`、`/roadmap-init` 三个命令，形成链路：`idea-capture -> mvp-shape -> roadmap-init -> phase-start`。
- 更新 `/phase-start`：仅当 `Project_Stage == DELIVERY` 且 `Idea_Clarity >= 3` 时允许进入 Delivery。
- 更新 `/spec`：必须读取上游 `IDEA_BRIEF` 与 `MVP_CANVAS`，并在超出 MVP 时提示 scope 漂移。
- README、GUIDE、HANDBOOK、SYSTEM_CONTEXT 对外叙事统一升级为 “Discovery + Delivery” 双段模型。

### 4. Task Layer + Hot Memory：补足阶段内执行粒度与跨会话连续性
- 在 Discovery 和脚本化基础稳定后，引入 `.nexus/tasks/` 承载阶段内子任务，保留 `Phase` 作为项目主节奏，不让 Task 替代 Phase。
- 新增 `.nexus/memory/` 的热记忆文件，最小集合为 `today.md`、`active-tasks.json`、`blockers.md`、`handoff.md`。
- `/sync` 与 `/doctor` 后续读取热记忆摘要，但默认只注入最小上下文，避免上下文膨胀。
- 每个任务必须有独立 handoff，形成“项目阶段 -> 任务执行 -> 热记忆恢复”的连续链路。

### 5. 后续产品化层：在前四步稳定后再做
- 评审路由升级：拆分 reviewer / security / performance / debt 等角色。
- 可选并行模式：仅在任务边界清晰后接入 worktree 并行。
- CLI、preset、安装升级、可观测性和迁移能力排在最后，不提前稀释控制面设计。

## Public Interfaces / Contracts

- `ROADMAP.md` 将从“阶段真相源”扩展为“项目定义 + 阶段真相源”，但 `Project_Stage` 与 `Phase_Status` 必须并列，不互相替代。
- 新公共命令面：`/idea-capture`、`/mvp-shape`、`/roadmap-init`。
- 现有命令契约更新：`/phase-start` 增加 Discovery 前置门禁；`/spec` 增加上游追溯；`/sync` 后续可显示项目级状态；`/doctor` 增加安装、脚本、状态机健康检查。
- 新文档接口：`IDEA_BRIEF` 定义问题，`MVP_CANVAS` 定义最小验证边界，`ROADMAP_INIT` 定义前三阶段路线；`SPEC` 只定义当前 Phase 的工程实现，不承担产品定义职责。

## Test Plan

- Delivery 内核 smoke tests：会话启动状态输出、缺失 `ROADMAP.md` 的容错、`Pending_Debt: true` 时阻断 `git commit/push`、安全 bash 命令放行、`/review` 与 `/doctor` 可见性、安装后目录与接线完整。
- 脚本化命令测试：`/phase-start` 前置检查失败路径、`/gate-check` 技术栈探测与失败报告、`/phase-end` 编排顺序、`/distill` 素材扫描去重。
- Discovery 测试：模糊输入能生成 `IDEA_BRIEF`，`Idea_Clarity` 与未知项被记录；`/mvp-shape` 强制产出 `Out of Scope`、成功指标、失败信号；`/roadmap-init` 只能生成前三阶段且必须给出单一 `Phase 1` 目标。
- 门禁测试：`Project_Stage != DELIVERY` 或 `Idea_Clarity < 3` 时，`/phase-start` 必须拒绝并指向下一条 Discovery 命令；`/spec` 在超出 MVP 时必须提示 scope 漂移。
- Task / Hot Memory 测试：创建任务后能生成独立 handoff；新会话的 `/sync` 能读取活跃任务与 blocker 摘要；中断恢复不依赖翻全文档。

## Assumptions And Defaults

- 默认采用“先执行层、后 Discovery 层”的顺序；这是为了避免把新的前置流程继续做成纯提示词系统。
- `docs/templates/SPEC_TEMPLATE.md` 是模板真名，所有设计和后续实现都应按此名更新，不再使用 `docs/templates/SPEC.md`。
- 现有 `/idea-review` 保持 backlog 治理职责不变；如果后续确实需要 Discovery 复核入口，再单独设计，不在第一轮里复用。
- 产品路线图里的 `v0.2 -> v1.0` 继续作为中长期方向，只有完成“兼容性加固 + 命令脚本化 + Discovery MVP”后，才进入 Task、Hot Memory、并行和 CLI 层。
