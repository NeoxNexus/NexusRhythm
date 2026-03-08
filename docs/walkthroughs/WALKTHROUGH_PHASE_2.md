# WALKTHROUGH — Phase 2: 自动化与硬门禁

**日期范围**：2026-03-09 至 2026-03-09
**实际耗时**：1.5 小时
**预估耗时**：4 小时
**误差率**：62.5% （节省）

---

## 1. 本阶段完成了什么

本轮没有把 Phase 2 一次性做成“大而全”的自动化改造，而是先把最脆弱的一段链路硬化了：仓库本身现在有默认 CI，会显式运行 `doctor quick`、smoke tests 和 `gate-check`；安装到新项目时，这条自动化基线也会一起被带过去；`/doctor` 也开始能发现“CI 接线缺失”这种过去只能靠人眼发现的问题。换句话说，Phase 1 形成的本地门禁第一次被提升成了仓库级默认约束。

### 主要交付物
- [x] 新增 GitHub Actions workflow：`.github/workflows/ci.yml`
- [x] `install.sh` 支持复制 `.github/workflows/` 到目标项目
- [x] `scripts/nr.py doctor quick` 新增 `ci_workflow` 接线检查
- [x] 为 CI 配置、安装传播和 doctor 缺失检测补齐 smoke tests
- [x] 形成聚焦的 Phase 2 SPEC：`docs/specs/SPEC_PHASE_2_ci-backed-hard-gates.md`

> 说明：本 walkthrough 记录的是 Phase 2 当前 slice 的收口，不代表整个 Phase 2 已结束。

---

## 2. 关键技术决策

### 决策一：先做 CI-backed hard gates，而不是同时推进更多 skills
- **背景**：Phase 2 原始目标里同时包含脚本、CI、skills 稳定化和 AI 默认引导增强，范围天然容易膨胀。
- **选择**：把本轮范围收敛成一个最小闭环，只覆盖 CI workflow、安装传播和 doctor 接线检查。
- **原因**：真实风险首先来自“门禁存在但没人跑”，先把本地验证提升到默认自动化，比继续扩充能力面更能降低失效概率。

### 决策二：CI 必须复用 `scripts/nr.py`，不允许再造一套 shell 门禁
- **背景**：如果 workflow 自己再写一套检查脚本，会让本地与 CI 逻辑分叉，形成新的漂移源。
- **选择**：CI 只调用既有入口：`doctor quick`、`unittest` 和 `gate-check`。
- **原因**：这样仓库内只有一套门禁定义，CI 只是执行层，不是第二套规范系统。

### 决策三：让 `doctor` 提前暴露 CI 缺线问题
- **背景**：仅靠 CI 文件存在并不够，安装后的项目如果少了 workflow，用户往往要到远端仓库才会发现。
- **选择**：把 `.github/workflows/ci.yml` 纳入 `doctor` 必需项。
- **原因**：这让“自动化接线是否完整”变成本地可诊断问题，符合 `/doctor` 作为脚手架健康检查器的定位。

---

## 3. 踩坑记录

> 这里的坑将在 `/distill` 时被提炼进 `.claude/rules/lessons.md`

| # | 坑的描述 | 根本原因 | 解决方案 |
|---|----------|----------|----------|
| 1 | Phase 2 一开始很容易被写成“CI + skills + 统一入口”的大杂烩 | ROADMAP 顶层目标太宽，缺少本轮唯一核心目标 | 先补 Phase 2 SPEC，把当前 slice 固定成 CI-backed hard gates |
| 2 | 为缺失 CI 的 doctor 测试写红灯时，测试先因为目录不存在直接报错 | 测试假设实现已部分存在，表达需求的方式不够稳 | 改成直接删除 `ci.yml` 文件并断言 `doctor` 输出缺失项 |
| 3 | 仅新增 workflow 文件还不够，下游项目安装后依然可能没有自动化 | 初版思路只考虑仓库自身，没有覆盖 install 传播链路 | 同步扩展 `install.sh` 和 smoke tests，保证模板项目与安装目标一致 |

---

## 4. 测试覆盖摘要

- 新增测试用例：3 个
- 测试通过率：100%
- 覆盖率（如有追踪）：N/A
- 本轮验证：
  - `python3 scripts/nr.py doctor quick`
  - `python3 -m unittest tests.test_nexusrhythm_smoke`
  - `python3 scripts/nr.py gate-check --no-update`

---

## 5. 性能影响评估

- `doctor quick` 只新增一次 `.github/workflows/ci.yml` 的存在性检查，对本地执行耗时影响可忽略
- CI workflow 复用现有 Python 命令入口，没有引入额外运行时依赖或重复检查逻辑
- 无业务热路径，无明显性能影响

---

## 6. 下阶段注意事项

> 写给**下一个继续 Phase 2 的自己/AI**的话

- 不要把新增 workflow 当成“自动化已完成”；后续仍需判断是否要补更稳定的 skills 边界
- 如果继续扩展 Phase 2，优先复用现有 `nr.py` 入口，不要在 workflow 或命令层复制业务规则
- 当前 walkthrough/review 是中期收口材料；只有在 Phase 2 剩余目标明确收束后，才执行 `phase-end`
- 如果下一步要扩 skills，优先挑已有脚本入口且低风险的流程，不要直接把复杂命令一次性迁完

---

## 7. 小复盘

**最大意外**：真正让 Phase 2 开始“有硬度”的，不是新增更多规则，而是把现有规则接进默认 CI 并纳入安装链路。

**最大收获 / 教训**：流程自动化要先打通一条从仓库到安装目标都一致的最小闭环，否则很容易只在主仓里看起来完整。

**下个阶段工作方式上想改进的地方**：继续保持按 slice 收敛目标的节奏，避免把 Phase 2 再次扩回“所有自动化一次做完”。
