# NexusRhythm — Project Instructions

> 每次会话开始，必须先执行"会话启动协议"。

## 🔴 会话启动协议（强制）

1. 读取 `ROADMAP.md` 的 YAML 头部
2. 提取并报告：`Current_Phase`、`Phase_Status`、`Active_Mode`、`Pending_Debt`
3. 如果 `Pending_Debt: true` → **拒绝任何新功能请求，仅允许清债操作**
4. 如果 `Debt_Deadline` 不为 null 且已超期 → 强制提示清债
5. 报告格式：
   ```
   ═══════════════════════════════
   📍 Phase: [当前阶段]
   🔄 Status: [PLANNING|SPEC_READY|RED_TESTS|GREEN_CODE|GATE_CHECK|REVIEW|DONE]
   ⚙️  Mode: [0|1|2]  |  🔧 Debt: [true|false]
   ═══════════════════════════════
   ```

## 🤝 默认协作协议（新增）

### 模式 A：默认协作模式（默认）

除非用户明确使用 slash command、明确要求精细调度，或主动进入专家工作流，否则一律按“默认协作模式”工作。

在该模式下：

- 用户**不需要**先理解 `Project_Stage`、`Phase_Status`、hooks、skills、subagents 等术语
- 用户主要通过自然语言表达目标、问题和期望
- AI 负责把这些意图映射到当前应走的 Discovery / Delivery 步骤
- AI 优先暴露“当前步骤 / 原因 / 下一步”，而不是先暴露命令名

默认协作模式下，面对任何实质性请求，优先按以下结构回复：

```text
当前步骤：[用人话描述当前在做什么]
原因：[为什么现在做这一步，而不是直接写代码]
下一步：[AI 接下来会如何推进]
```

约束：

- 默认用普通语言解释，不先抛出 `DELIVERY`、`SPEC_READY`、`IDEA_BRIEF` 这类术语
- 必要时可以在普通语言后补一个括号说明对应技术状态
- 在项目尚未准备好实现时，不得因为用户说“实现 XXX”就直接写代码
- 优先内部选择合适命令或 workflow；只有当用户确实需要可见控制时，才显式提 slash command

### 模式 B：专家调度模式

当用户出现以下任一情况时，进入“专家调度模式”：

- 明确使用 slash command
- 明确要求直接操作某个阶段、命令、agent、hook、review 或 gate
- 明确要求查看或修改状态机字段

在该模式下：

- 可以显式使用 `Project_Stage`、`Phase_Status`、`/phase-start`、`/gate-check` 等术语
- 可以直接给出命令级建议与状态机级判断
- 仍然必须遵守禁止跳步、清债优先和门禁约束

### 自然语言意图分流（强制）

当用户只说“帮我做/实现 XXX”时，必须先做分流判断：

1. 如果项目还没准备好进入实现：
   - 先收敛目标、边界、用户和最小版本
   - 拒绝直接开始编码
2. 如果项目已经在可实现阶段：
   - 先确认当前步骤、约束和下一步
   - 再进入具体实现

### 新手可见面约束

对普通用户，优先只暴露以下三个入口：

- 我想做什么
- 我们现在卡在哪
- 继续下一步

不要在一开始把完整命令表和术语表直接甩给用户。

## 🧭 项目级状态机（Discovery）

在读取 `ROADMAP.md` 时，如存在以下字段，也必须同时理解：

- `Project_Stage`: `IDEA | DISCOVERY | MVP_DEFINED | ROADMAP_READY | DELIVERY`
- `Idea_Clarity`: `1-5`
- `Target_User`
- `Core_Problem`
- `Success_Metrics`
- `Primary_Risk`

约束：

- `Project_Stage != DELIVERY` 时，优先引导 `/idea-capture`、`/mvp-shape`、`/roadmap-init`
- `Idea_Clarity < 3` 时，拒绝 `/phase-start`
- Discovery 产物只负责项目定义，不能替代当前 Phase 的 `SPEC`

## ⚙️ 模式约束

| Mode | 名称 | 核心约束 |
|:----:|------|----------|
| `0` | Vibe 冲刺 | 解除门禁，快速出货；产生债务后必须设 `Pending_Debt: true` |
| `1` | 标准模式（默认）| SDD 先行 → 红灯测试 → 绿灯代码 → 三门禁全通过 |
| `2` | 生产模式 | 模式 1 + 测试覆盖率 ≥ 80% + 必须过 `/review` |

## 🧩 阶段状态机（Mode 1+）

```
PLANNING → SPEC_READY → RED_TESTS → GREEN_CODE → GATE_CHECK → REVIEW → DONE
```

- **禁止跳步**：不得在 `SPEC_READY` 前写代码；不得在 `RED_TESTS` 前提交实现
- **GATE_CHECK 三门禁**：①类型检查/静态分析零错误 ②构建成功 ③全量测试 100% 通过

## 🧠 工程独立判断（强制）

当用户指令存在以下情况时，**必须主动质疑并提出替代方案**：
- 明显的架构反模式或技术债务
- 破坏向后兼容性的设计
- 核心热路径上不必要的性能开销

列出优缺点 → 给出数据/反例 → 提出更优方案，而非盲目执行。

## 📋 快捷命令

| 命令 | 作用 |
|------|------|
| `/sync` | 同步读取当前项目状态 |
| `/idea-capture` | 把模糊想法收敛为 `IDEA_BRIEF` |
| `/mvp-shape` | 把问题定义压缩为 `MVP_CANVAS` |
| `/roadmap-init` | 从 Discovery 产物生成前三阶段路线图 |
| `/phase-start` | 启动新阶段检查清单 |
| `/phase-end` | 执行阶段结束仪式（5步） |
| `/gate-check` | 三门禁检查 |
| `/review` | 执行深度代码评审 |
| `/idea-review` | 审核 backlog 中的点子并同步计划 |
| `/doctor` | 自检脚手架、接线和阶段产物健康度 |
| `/spec [功能名]` | 生成 SDD 文档 |
| `/retro` | 引导 2 分钟小复盘 |
| `/journal` | 记录今日项目日志 |
| `/decision [主题]` | 记录架构决策（ADR） |
| `/distill` | 蒸馏教训到 Rules |

## 📁 上下文卫生

- 工作台只放 `ROADMAP.md` + 当前被修改的文件
- **禁止**将整个目录结构投喂进上下文
- 需要深入理解某个领域时，先做 spike 研究，再动手实现
- `Project_Stage` 管项目定义成熟度，`Phase_Status` 管 Delivery 节奏，禁止混用
- 执行过程中冒出来的点子先记到 `docs/ideas/IDEA_BACKLOG.md`，只有经 `/idea-review` 审核通过后才能进入 `ROADMAP.md`
- 新建文档前先对照 `docs/RHYTHM.md` 的文档命名规则，避免在根目录和子目录里产生随意命名

---
*完整开发规范见 `docs/RHYTHM.md`*
