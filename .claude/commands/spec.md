---
description: Generate a SPEC document for a new feature or phase scope.
argument-hint: "[功能名]"
disable-model-invocation: true
---

基于 `docs/templates/SPEC_TEMPLATE.md` 生成当前阶段的 SDD 文档。

**功能描述**：$ARGUMENTS

---

### 执行步骤

1. **读取上下文**
   - 读取 `ROADMAP.md` 确认当前阶段
   - 如果存在，读取 `Project_Stage` 与 `Idea_Clarity`
   - 读取 `docs/SYSTEM_CONTEXT.md` 了解架构约束
   - 如果存在，读取 `docs/ideas/IDEA_BRIEF.md`
   - 如果存在，读取 `docs/ideas/MVP_CANVAS.md`
   - 检查是否有相关的已有 SPEC 文档

2. **生成 SPEC**
   基于功能描述和项目上下文，自动填充模板的以下部分：
   - 背景与目标（含范围和非范围）
   - 接口契约（函数/API 签名）
   - 数据流图（mermaid）
   - 边界条件表格（至少 4 行：正常 + 空值 + 越界 + 并发）
   - 兼容性影响评估
   - 测试用例清单（每个边界条件对应一个 test case）

3. **Scope 漂移检查**
   - 若当前功能明显超出 `MVP_CANVAS` 中的 `In Scope`，必须先提示 scope 漂移
   - Discovery 产物只回答“为什么做/为谁做/做到什么程度”
   - SPEC 只回答“本阶段具体怎么实现”

4. **保存文件**
   保存到 `docs/specs/SPEC_PHASE_N_[功能名称].md`
   
5. **更新 ROADMAP**
   将 `Phase_Status` 更新为 `SPEC_READY`

6. **提示下一步**
   ```
   ✅ SPEC 已创建：docs/specs/SPEC_PHASE_N_[功能名称].md
   
   下一步：运行 /phase-start 让 architect agent 基于此 SPEC 编写红灯测试用例。
   ```

---

> 💡 如果不提供 $ARGUMENTS，将引导你输入功能描述。
