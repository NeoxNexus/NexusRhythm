---
description: Generate a SPEC document for a new feature or phase scope.
argument-hint: "[功能名]"
disable-model-invocation: true
---

基于 `docs/templates/SPEC.md` 模板，为以下功能生成一份完整的 SDD 文档：

**功能描述**：$ARGUMENTS

---

### 执行步骤

1. **读取上下文**
   - 读取 `ROADMAP.md` 确认当前阶段
   - 读取 `docs/SYSTEM_CONTEXT.md` 了解架构约束
   - 检查是否有相关的已有 SPEC 文档

2. **生成 SPEC**
   基于功能描述和项目上下文，自动填充模板的以下部分：
   - 背景与目标（含范围和非范围）
   - 接口契约（函数/API 签名）
   - 数据流图（mermaid）
   - 边界条件表格（至少 4 行：正常 + 空值 + 越界 + 并发）
   - 兼容性影响评估
   - 测试用例清单（每个边界条件对应一个 test case）

3. **保存文件**
   保存到 `docs/specs/SPEC_PHASE_N_[功能名称].md`
   
4. **更新 ROADMAP**
   将 `Phase_Status` 更新为 `SPEC_READY`

5. **提示下一步**
   ```
   ✅ SPEC 已创建：docs/specs/SPEC_PHASE_N_[功能名称].md
   
   下一步：运行 /phase-start 让 architect agent 基于此 SPEC 编写红灯测试用例。
   ```

---

> 💡 如果不提供 $ARGUMENTS，将引导你输入功能描述。
