# Nexus Tasks

`.nexus/tasks/` 承载阶段内的任务粒度，不替代 `Phase`。

建议结构：

```text
.nexus/tasks/
└── YYYY-MM-task-name/
    ├── task.yaml
    ├── prd.md
    ├── handoff.md
    ├── implement.jsonl
    ├── review.jsonl
    └── debug.jsonl
```

规则：

- 每个任务必须有独立 handoff
- 任务只承载阶段内执行单元；项目主节奏仍由 `ROADMAP.md` 管理
