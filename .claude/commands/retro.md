---
description: Run a short retrospective for the current phase.
disable-model-invocation: true
---

引导一次 2 分钟小复盘，并将结果记录到当前阶段的 Walkthrough 文件。

---

### Step 1: 找到当前 Walkthrough 文件
读取 `ROADMAP.md` 确认当前阶段编号，找到对应的 `docs/walkthroughs/WALKTHROUGH_PHASE_N.md`。

如果文件不存在，提示先运行 `/phase-end`。

### Step 2: 引导填写复盘

逐一提问（等待用户回答后再问下一题）：

**Q1**: 本阶段预估耗时多少小时？实际花了多少小时？
**Q2**: 最大的意外是什么？（预期之外的技术难题或发现）
**Q3**: 这个阶段最大的收获或教训是什么？（一句话）
**Q4**: 下个阶段，你希望在哪方面做得更好？（工作方式/速度/质量）

### Step 3: 追加到 Walkthrough
将用户的回答格式化后追加到 Walkthrough 文件的"小复盘"章节：

```markdown
## 7. 小复盘

**实际花费时间**：___ 小时
**预估时间**：___ 小时
**误差率**：___% （超出/节省）

**最大意外**：[用户回答]

**最大收获 / 教训**：[用户回答]

**下个阶段工作方式上想改进的地方**：[用户回答]
```

### Step 4: 完成提示
```
✅ 复盘记录完成！

💡 提示：如果这是一个重要教训，运行 /distill 将其蒸馏进 .claude/rules/lessons.md，
   让这个教训永久影响未来的 AI 会话。
```
