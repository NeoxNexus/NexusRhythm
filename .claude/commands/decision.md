---
description: Capture an architecture decision record and update the system context index.
argument-hint: "[主题]"
disable-model-invocation: true
---

帮我记录一个架构决策（ADR）。

**决策主题**：$ARGUMENTS

---

### Step 1: 准备
1. 扫描 `docs/decisions/` 目录，获取下一个 ADR 编号（ADR-NNN）
2. 读取 `docs/SYSTEM_CONTEXT.md` 了解当前架构约束背景

### Step 2: 引导填写

**如果已提供 $ARGUMENTS**：直接基于主题开始引导。

**引导问题**（可以一次性输入所有信息，也可以逐一问答）：

1. **背景**：为什么需要做这个决策？面临什么约束或问题？
2. **最终选择**：你们最终选择了什么方案？
3. **考虑过的方案**：除了选定的方案，还考虑过哪些？每个方案的优劣是什么？
4. **后果**：这个决策的正面和负面影响各是什么？
5. **触发重新评估的条件**：什么情况下需要重新审视这个决策？

### Step 3: 生成 ADR 文档

基于 `docs/templates/ADR_TEMPLATE.md`，在 `docs/decisions/ADR-NNN-[主题slug].md` 生成完整的 ADR 文档。

同时在 `docs/SYSTEM_CONTEXT.md` 的"关键架构决策索引"表格中追加一行。

### Step 4: 完成确认

```
✅ 决策已记录：docs/decisions/ADR-NNN-[主题].md
   SYSTEM_CONTEXT.md 索引已更新

📋 决策摘要：
  选择：[最终方案]
  主要理由：[核心原因]
```
