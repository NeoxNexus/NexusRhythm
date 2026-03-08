---
description: Invoke the reviewer agent to perform a focused quality audit for the current phase or a specified scope.
argument-hint: "[范围]"
disable-model-invocation: true
---

调用 `reviewer` agent，对当前阶段或 `$ARGUMENTS` 指定范围执行一次深度评审：

1. 读取当前阶段相关的 SPEC 文档和 ROADMAP 状态
2. 聚焦最近修改的文件或用户指定范围
3. 从代码质量、安全、性能、SPEC 符合度、测试质量五个维度输出结论
4. 如果需要，生成或更新 `docs/reviews/CODE_REVIEW_PHASE_N.md`

输出格式：
- 评审范围
- 关键发现（按严重程度排序）
- 结论：`APPROVED` / `APPROVED WITH NOTES` / `CHANGES REQUIRED`
- 下一步建议
