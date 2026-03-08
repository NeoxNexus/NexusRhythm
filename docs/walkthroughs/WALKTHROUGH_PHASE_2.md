# WALKTHROUGH — Phase 2: 自动化与硬门禁

**日期范围**：2026-03-09 至 2026-03-09
**实际耗时**：2.5 小时
**预估耗时**：4 小时
**误差率**：37.5% （节省）

---

## 1. 本阶段完成了什么

本阶段把 NexusRhythm 从“本地能跑通的脚手架”推进到了“默认带自动化门禁、并开始形成稳定 skills 边界”的状态。前半段先把 `doctor`、smoke tests 和 `gate-check` 接到 GitHub Actions，并把这条自动化基线传播到安装后的项目；后半段再补上 `gate-check` 的第二个 skill 试点，验证 command 与 skill 可以围绕同一个脚本入口稳定共存。结果是：关键流程不再只靠 prompt 和自觉执行，项目自身也更接近一个可复制、可验证的工程产品。

### 主要交付物
- [x] 新增 GitHub Actions workflow：`.github/workflows/ci.yml`
- [x] `install.sh` 支持复制 `.github/workflows/` 到目标项目
- [x] `scripts/nr.py doctor quick` 新增 `ci_workflow` 接线检查
- [x] 新增 `.claude/skills/gate-check/SKILL.md`，作为第二个 workflow skill 试点
- [x] 为 CI 配置、安装传播、doctor 缺失检测和 gate-check skill 增加 smoke tests
- [x] 形成两份阶段 SPEC：`docs/specs/SPEC_PHASE_2_ci-backed-hard-gates.md` 与 `docs/specs/SPEC_PHASE_2_gate-check-skill-boundary-hardening.md`

---

## 2. 关键技术决策

### 决策一：先硬化 CI 基线，再继续推进 skills 迁移
- **背景**：Phase 2 同时包含“脚本化门禁”“CI”“skills 稳定化”“默认引导增强”等多个方向，天然容易范围失控。
- **选择**：把阶段拆成两刀，先做 `CI-backed hard gates`，再做第二个 skill 试点。
- **原因**：先解决“门禁没人跑”的真实风险，再处理入口边界，比同时推进多条主线更稳。

### 决策二：CI 与 skill 都必须复用既有 `nr.py` 脚本入口
- **背景**：如果 workflow 和 skill 各自复制一份 shell 逻辑，本地、CI 和解释层会快速分叉。
- **选择**：CI 只跑 `doctor quick`、smoke tests 和 `gate-check`，`gate-check` skill 只包装 `python3 scripts/nr.py gate-check`。
- **原因**：这样仓库内始终只有一套门禁实现，新增的是执行层和解释层，而不是新的规则源。

### 决策三：第二个 skill 试点选择 `gate-check`，而不是更复杂的 `review` / `phase-end`
- **背景**：Phase 1 已经用 `doctor` 证明“已有脚本入口 + skill 包装”的路径可行，但还缺第二个样本。
- **选择**：迁移 `gate-check`，继续保留 `/gate-check` command 兼容入口。
- **原因**：`gate-check` 的输入输出边界清晰、失败语义稳定，适合作为验证 command-first / skill-first 共存边界的低风险试点。

---

## 3. 踩坑记录

> 这里的坑将在 `/distill` 时被提炼进 `.claude/rules/lessons.md`

| # | 坑的描述 | 根本原因 | 解决方案 |
|---|----------|----------|----------|
| 1 | Phase 2 一开始很容易被写成“CI + skills + 统一入口”的大杂烩 | ROADMAP 顶层目标太宽，缺少本轮唯一核心目标 | 先补 Phase 2 SPEC，把阶段拆成两刀推进 |
| 2 | 为缺失 CI 的 doctor 测试写红灯时，测试先因为目录不存在直接报错 | 测试假设实现已部分存在，表达需求的方式不够稳 | 改成直接删除 `ci.yml` 文件并断言 `doctor` 输出缺失项 |
| 3 | 仅在主仓新增 workflow 还不够，下游项目安装后仍可能没有自动化 | 初版思路只考虑仓库自身，没有覆盖 install 传播链路 | 同步扩展 `install.sh` 和 smoke tests，保证模板项目与安装目标一致 |
| 4 | 直接把 Phase 2 改名成 `2A/2B` 会和既有 `phase-end`、walkthrough、review 命名规则冲突 | 脚本与产物命名都以单一阶段编号为锚点 | 保留 `Phase 2` 编号，在 ROADMAP 中显式拆成 Slice A / Slice B |

---

## 4. 测试覆盖摘要

- 新增测试用例：4 个
- 测试通过率：100%
- 覆盖率（如有追踪）：N/A
- 本阶段门禁验证：
  - `python3 scripts/nr.py doctor quick`
  - `python3 -m unittest tests.test_nexusrhythm_smoke`
  - `python3 scripts/nr.py gate-check`

---

## 5. 性能影响评估

- `doctor quick` 只增加一次 `.github/workflows/ci.yml` 的存在性检查，对本地执行耗时影响可忽略
- `gate-check` skill 只新增轻量解释层，不引入第二套门禁执行逻辑
- GitHub Actions workflow 复用现有 Python 命令入口，无新增运行时依赖
- 无业务热路径，无明显性能影响

---

## 6. 下阶段注意事项

> 写给**下一个开始 Phase N+1 的自己/AI**的话

- Phase 2 已经证明“已有脚本入口 + skill 包装 + smoke test 锁边界”的模式可行，Phase 3 不要退回大 prompt 驱动
- 如果下一步做示例工程或产品化验证，优先证明“安装后零感知可跑通”，而不是先扩更多命令
- 任何新增仓库级资产都继续保持“三条链路一起验证”：仓库存在、安装可传播、doctor 或 smoke tests 可诊断
- 更复杂的 skill 迁移应先明确 supporting files 与 command 兼容入口的边界，再动手实现

---

## 7. 小复盘

**最大意外**：真正让 Phase 2 开始变硬的，不是再加一条规则，而是把现有规则同时接进 CI、安装链路和 skill 解释层。

**最大收获 / 教训**：工程化脚手架要先保证“同一条规则在本地、CI 和安装目标里都一致”，否则任何单点能力都会迅速漂移。

**下个阶段工作方式上想改进的地方**：继续用小 slice 推进产品化，不把示例工程、体验重构和分发机制混成一次大改。
