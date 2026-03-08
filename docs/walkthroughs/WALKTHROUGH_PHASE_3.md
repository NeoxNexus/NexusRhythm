# WALKTHROUGH — Phase 3: 示例工程与产品化

**日期范围**：2026-03-09 至 2026-03-09
**实际耗时**：1.5 小时
**预估耗时**：3 小时
**误差率**：50% （节省）

---

## 1. 本阶段完成了什么

Phase 3 的第一刀没有去堆更多“对外发布材料”，而是先交付了一个能在干净目录里真正生成的 demo workspace。这个脚本会创建最小 Python 示例项目、写入 demo 自己的 `ROADMAP.md`、调用 `install.sh` 注入 NexusRhythm，然后让生成后的工程默认通过 `doctor quick` 和 `gate-check`。这让“示例工程”从一份静态目录，变成了一个可重复验证的产品化入口。

### 主要交付物
- [x] 新增 `scripts/create_demo_workspace.py`
- [x] 为 demo workspace 生成链路补齐 3 个 smoke tests
- [x] 生成后的 demo workspace 默认通过 `doctor quick`
- [x] 生成后的 demo workspace 默认通过 `gate-check --no-update`
- [x] 新增 Phase 3 Slice A SPEC：`docs/specs/SPEC_PHASE_3_demo-workspace-bootstrap.md`

---

## 2. 关键技术决策

### 决策一：示例工程采用“生成式 demo workspace”，而不是提交一整份静态 demo 仓库
- **背景**：静态 demo 很容易和脚手架自身演进脱节，后续维护成本高。
- **选择**：新增脚本在目标目录生成最小宿主项目，并复用现有 `install.sh` 注入脚手架。
- **原因**：这样 demo 走的就是未来真实用户的安装路径，验证价值更高。

### 决策二：demo workspace 先写自己的 ROADMAP，再执行安装
- **背景**：当前 `install.sh` 仍会复制仓库自身的 `ROADMAP.md`，这对 demo 项目会造成状态污染。
- **选择**：在 demo 生成器里先写入 demo 自己的最小 `ROADMAP.md`，再运行安装脚本。
- **原因**：这样能先保证 demo 体验真实可信，同时把更广泛的安装模板问题留作后续治理项。

### 决策三：宿主示例项目保持最小 Python + unittest 组合
- **背景**：Phase 3 的第一刀要证明“安装后能跑通”，不是展示多语言模板能力。
- **选择**：只生成极小的 Python 包和一个 `unittest` 用例。
- **原因**：这足够覆盖 `doctor`、`gate-check` 和安装链路，又不会把复杂度提前引入到多语言支持层。

---

## 3. 踩坑记录

> 这里的坑将在 `/distill` 时被提炼进 `.claude/rules/lessons.md`

| # | 坑的描述 | 根本原因 | 解决方案 |
|---|----------|----------|----------|
| 1 | 直接在 demo 目录里复制静态项目虽然快，但会制造第二份长期维护对象 | 示例工程与脚手架实现容易分叉 | 改用生成式脚本，复用 `install.sh` |
| 2 | 普通安装链路会把当前仓库的 ROADMAP 状态带进目标项目 | 现有安装逻辑仍复制项目自身的根级 `ROADMAP.md` | demo 生成器先写 demo 专用 ROADMAP，并把通用修复记入 backlog |
| 3 | 如果示例工程依赖 pytest 或第三方包，干净环境验证会变脆弱 | 产品化第一刀过早引入环境依赖 | 先用标准库 `unittest` 保持零额外依赖 |

---

## 4. 测试覆盖摘要

- 新增测试用例：3 个
- 测试通过率：100%
- 覆盖率（如有追踪）：N/A
- 本阶段验证：
  - `python3 -m unittest tests.test_nexusrhythm_smoke`
  - `python3 scripts/nr.py gate-check --no-update`

---

## 5. 性能影响评估

- demo 生成脚本只在显式调用时执行文件写入和安装，不影响日常热路径
- 新增 smoke tests 会增加少量测试时间，但换来真实安装链路的回归验证
- 无业务运行时性能影响

---

## 6. 下阶段注意事项

> 写给**下一个继续 Phase 3 的自己/AI**的话

- 先把“demo workspace 可生成且可验证”当成新的产品化基线，再决定是否扩首轮引导文档
- `install.sh` 复制根级 ROADMAP 的问题已经暴露，后续应收敛为更中立的项目模板方案
- 如果继续做 Phase 3，优先补 demo 的“第一会话示例”或根 README 入口，不要急着扩多语言

---

## 7. 小复盘

**最大意外**：真正让 Phase 3 有产品化味道的，不是写更多宣传文案，而是让示例工程可以被脚本稳定生成。

**最大收获 / 教训**：示例工程最有价值的时候，不是“长得像产品”，而是“真的复用了未来用户会走的那条安装路径”。

**下个阶段工作方式上想改进的地方**：继续保持“生成式优先”的思路，减少需要手工维护的示例资产。
