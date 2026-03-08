---
description: Record a daily project journal entry using the project template.
disable-model-invocation: true
---

帮我记录今日项目日志。

---

### Step 1: 检查今日日志文件
查找 `docs/journal/` 目录下是否已有今天日期的日志文件（格式：`YYYY-MM-DD.md`）。

- 如果已有：打开文件，追加到对应章节
- 如果没有：基于 `docs/templates/JOURNAL_TEMPLATE.md` 创建新文件

### Step 2: 引导填写

逐项引导（可以一次性输入，也可以逐一问答）：

**今日完成**：今天完成了什么？（输入后帮我格式化为 checklist）

**踩坑记录**：遇到了什么坑？怎么解决的？
（格式：`🕳️ [坑的现象] → [解决方案]`）

**突发灵感**：有什么值得记录的想法？（可选）

如果属于值得后续规划的点子：
- 追加到 `docs/ideas/IDEA_BACKLOG.md`
- 不直接写入 `ROADMAP.md`
- 提醒后续在阶段结束前运行 `/idea-review`

**阻塞 / 待解决**：有什么还没解决的问题？（可选）

**明日计划**：明天打算做什么？

### Step 3: 保存并确认

保存文件，输出摘要：
```
✅ 日志已保存：docs/journal/YYYY-MM-DD.md

📊 今日概览：
  完成：N 项
  踩坑：N 个
  明日计划：N 项

💡 如果今天的踩坑值得永久记录，运行 /distill 提炼到项目教训库。
💡 如果今天出现了值得投入评估的新点子，记录到 `docs/ideas/IDEA_BACKLOG.md`，并在阶段结束前运行 /idea-review。
```

---

> 📅 每天花 2 分钟记录，每个阶段花 5 分钟 `/distill`，让 AI 越来越懂你的项目。
