执行三道强制门禁检查。根据项目 `ROADMAP.md` 中的 `Core_Tech_Stack` 自动判断使用哪些检查命令。

**可选参数**：$ARGUMENTS（指定仅检查某一项，例如 `types` / `build` / `tests`）

---

### ❶ 类型检查 / 静态分析

根据技术栈选择对应命令：
- Python：`mypy . --strict` 或 `pyright`
- TypeScript：`tsc --noEmit`
- Go：`go vet ./...`
- Rust：`cargo check`

**标准**：零错误，零警告（警告视为错误）

---

### ❷ 构建检查

根据技术栈选择对应命令：
- Python：`python -c "import [主模块]"` 或 `pip install -e . --dry-run`
- Node：`npm run build`
- Go：`go build ./...`
- Rust：`cargo build`

**标准**：退出码为 0，无错误输出

---

### ❸ 全量测试

根据技术栈选择对应命令：
- Python：`pytest --tb=short -q`
- Node：`npm test`
- Go：`go test ./...`
- Rust：`cargo test`

**标准**：100% 通过，零跳过（skipped），零失败

---

### 结果汇报

如果全部通过：
```
✅ GATE CHECK PASSED
❶ 类型检查：PASS
❷ 构建检查：PASS  
❸ 全量测试：PASS（N 个测试）

ROADMAP Phase_Status 已更新为 GATE_CHECK ✓
现在可以运行 /phase-end 执行阶段结束仪式。
```

如果有失败项：
```
❌ GATE CHECK FAILED — 禁止提交

失败项目：[列出]
失败详情：[列出具体错误]

修复后重新运行 /gate-check。
```
