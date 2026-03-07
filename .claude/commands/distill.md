---
description: Distill recent lessons into reusable rules for future Claude sessions.
disable-model-invocation: true
---

从项目记忆中蒸馏教训，更新 `.claude/rules/lessons.md`，让过去的坑永久影响未来的 AI 行为。

---

### Step 1: 采集原始素材

扫描以下来源，提取所有教训性内容：

**L0 Journal**（`docs/journal/`）：
- 提取所有 `🕳️` 踩坑记录
- 提取"最大意外"字段的内容

**L1 Walkthrough**（`docs/walkthroughs/`）：
- 提取"踩坑记录"表格的所有行
- 提取"小复盘"中的"最大收获/教训"

**L1 Code Review**（`docs/reviews/`）：
- 提取"发现的问题"章节中的 🔴 必须修复项
- 提取"教训提炼"章节

### Step 2: 去重与分类

对所有原始素材进行处理：
1. **合并重复/相似的教训**
2. **过滤**：只保留跨阶段通用的、可复用的教训（项目特定的单次问题不纳入）
3. **分类**：按以下类别分组
   - `技术栈教训`（具体库/框架的坑）
   - `架构教训`（设计模式/结构性问题）
   - `工作流教训`（流程/效率/估时）

### Step 3: 更新 lessons.md

以**追加**方式更新 `.claude/rules/lessons.md`：
- 不覆盖已有内容
- 只添加新的、不重复的教训
- 每条教训格式：`- [库/场景] [具体描述，不超过一行]`
- 在文件末尾更新"最后蒸馏时间"和"蒸馏来源"

### Step 4: 蒸馏报告

```
✅ 蒸馏完成！

📥 扫描来源：N 个日志，M 个 Walkthrough，K 个 Code Review
📊 提取原始教训：X 条
🔗 去重合并后：Y 条新教训
📝 追加到 .claude/rules/lessons.md

新增教训预览：
  技术栈：[N 条]
  架构：[N 条]
  工作流：[N 条]

🧠 这些教训将在下次会话启动时自动加载，永久影响 AI 的行为判断。
```

---

> ⏰ **推荐频率**：每 3 个阶段执行一次，或在 Vibe Sprint 还债时必须执行。
