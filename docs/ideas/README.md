# Discovery Docs

`docs/ideas/` 只承载项目级 Discovery 产物，不承载阶段级实现细节。

## 生成顺序

1. `IDEA_BRIEF.md`
2. `MVP_CANVAS.md`
3. `ROADMAP_INIT.md`

## 消费关系

- `/idea-capture` 生成 `IDEA_BRIEF.md`
- `/mvp-shape` 读取 `IDEA_BRIEF.md`，生成 `MVP_CANVAS.md`
- `/roadmap-init` 读取 `IDEA_BRIEF.md` + `MVP_CANVAS.md`，生成 `ROADMAP_INIT.md`
- `/phase-start` 只在 `Project_Stage == DELIVERY` 且 `Idea_Clarity >= 3` 时允许进入 Delivery
- `/spec` 必须读取上游 Discovery 产物，避免 scope 漂移

## 命名约定

- 模板统一放在 `docs/templates/*_TEMPLATE.md`
- 当前项目的活动 Discovery 产物使用固定文件名：`IDEA_BRIEF.md`、`MVP_CANVAS.md`、`ROADMAP_INIT.md`
- 未经评审的 backlog 点子继续留在 `docs/ideas/IDEA_BACKLOG.md`，不与 Discovery 产物混用
