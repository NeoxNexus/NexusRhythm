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
- 执行过程中冒出来的点子先记到 `docs/ideas/IDEA_BACKLOG.md`，只有经 `/idea-review` 审核通过后才能进入 `ROADMAP.md`
- 新建文档前先对照 `docs/RHYTHM.md` 的文档命名规则，避免在根目录和子目录里产生随意命名

---
*完整开发规范见 `docs/RHYTHM.md`*
