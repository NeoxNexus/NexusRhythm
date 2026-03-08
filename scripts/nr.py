#!/usr/bin/env python3

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import shlex
import subprocess
import sys
from pathlib import Path
from typing import Any


SCALAR_PATTERN = re.compile(r"^([A-Za-z0-9_]+):\s*(.*?)\s*(#.*)?$")
YAML_BLOCK_PATTERN = re.compile(r"```yaml\s*\n(.*?)\n```", re.DOTALL)


def main() -> int:
    """
    主命令入口函数。

    作用：
    初始化解析器并运行对应的子命令，返回执行结果状态码给操作系统。

    工作流程：
    1. 调用 `build_parser()` 构建命令行参数解析器。
    2. 解析传入的 `sys.argv`。
    3. 调用解析后参数中绑定的 `func` 方法。

    局限性：
    - 紧耦合了 argparse 作为命令行基础。
    - 所有子命令都必须签名一致接收 Namespace 并返回 int 状态码。
    """
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


def build_parser() -> argparse.ArgumentParser:
    """
    构建命令行参数解析器及其所有子命令。

    作用：
    集中定义和注册 NexusRhythm 脚手架提供的所有 CLI 操作（如 doctor, sync, gate-check 等）。

    工作流程：
    1. 实例化根 Parser。
    2. 注册 `--root` 参数，默认回退到环境变量 `CLAUDE_PROJECT_DIR` 或当前路径。
    3. 注册所有的子解析器（subparsers），并为每个子功能绑定具体的执行回调函数 `func`。

    局限性：
    - 添加新的脚手架命令必须手动在此处添加注册代码。
    - 脚手架的命令相对扁平，无法自动发现插件化命令。
    """
    parser = argparse.ArgumentParser(description="NexusRhythm automation helpers")
    parser.add_argument(
        "--root",
        default=os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd(),
        help="Project root directory",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    sync_parser = subparsers.add_parser("sync", help="Read and report project state")
    sync_parser.add_argument("--hook", action="store_true", help="Print hook banner only")
    sync_parser.set_defaults(func=cmd_sync)

    doctor_parser = subparsers.add_parser("doctor", help="Run scaffold checks")
    doctor_parser.add_argument("mode", nargs="?", default="full", choices=["quick", "full"])
    doctor_parser.set_defaults(func=cmd_doctor)

    gate_parser = subparsers.add_parser("gate-check", help="Run quality gates")
    gate_parser.add_argument("scope", nargs="?", default="all", choices=["all", "types", "build", "tests"])
    gate_parser.add_argument("--no-update", action="store_true", help="Do not update ROADMAP status")
    gate_parser.set_defaults(func=cmd_gate_check)

    phase_start_parser = subparsers.add_parser("phase-start", help="Validate and start a phase")
    phase_start_parser.add_argument("phase_name", nargs="?", default="")
    phase_start_parser.set_defaults(func=cmd_phase_start)

    phase_end_parser = subparsers.add_parser("phase-end", help="Complete phase-end checks")
    phase_end_parser.add_argument("--no-update", action="store_true", help="Do not update ROADMAP status")
    phase_end_parser.set_defaults(func=cmd_phase_end)

    distill_parser = subparsers.add_parser("distill", help="Distill lessons into rules")
    distill_parser.set_defaults(func=cmd_distill)

    idea_parser = subparsers.add_parser("idea-capture", help="Create IDEA_BRIEF")
    idea_parser.add_argument("raw_idea", nargs="+")
    idea_parser.set_defaults(func=cmd_idea_capture)

    mvp_parser = subparsers.add_parser("mvp-shape", help="Create MVP_CANVAS")
    mvp_parser.add_argument("north_star", nargs="*", default=[])
    mvp_parser.set_defaults(func=cmd_mvp_shape)

    roadmap_init_parser = subparsers.add_parser("roadmap-init", help="Create ROADMAP_INIT")
    roadmap_init_parser.set_defaults(func=cmd_roadmap_init)

    block_parser = subparsers.add_parser("hook-block-debt", help="Hook entrypoint for PreToolUse")
    block_parser.set_defaults(func=cmd_hook_block_debt)

    return parser


def repo_root(root: str) -> Path:
    """
    获取安全绝对的项目根路径。

    作用：防止相对路径在终端环境和进程上下文中发生漂移。
    """
    return Path(root).resolve()


def roadmap_path(root: Path) -> Path | None:
    """
    查找工程中的 ROADMAP.md 文件。

    作用/工作流程：从优先极高的 `ROADMAP.md` 找起，如果没有则去 `docs/ROADMAP.md`，返回找到的路径。
    
    局限性：写死了路径候选项，不支持用户自定义路径结构。
    """
    candidates = [root / "ROADMAP.md", root / "docs" / "ROADMAP.md"]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def load_roadmap(root: Path) -> tuple[Path, str, dict[str, Any]]:
    """
    读取并解析路线图文件及元数据。

    作用：读取 ROADMAP.md 的文本，并提取其中隐藏在 Markdown ```yaml 块里配置的元数据信息。
    """
    path = roadmap_path(root)
    if path is None:
        raise FileNotFoundError("ROADMAP.md not found")
    text = path.read_text(encoding="utf-8")
    metadata = parse_yaml_metadata(text)
    return path, text, metadata


def parse_yaml_metadata(text: str) -> dict[str, Any]:
    """
    手工解析 Markdown 中的简单 YAML 块。

    作用：
    为了避免让使用者安装外部依赖包（如 PyYAML），这提供了一个非常轻量正则表达式解析器。
    
    工作流程：
    1. 寻找 Markdown 文档中的第一个 ````yaml` 代码块。
    2. 按行拆解，过滤空行和注释。
    3. 利用正则匹配 `Key: Value` 的标量模式。
    
    局限性：
    - 无法处理真正的多层级嵌套 YAML，不支持列表跨行，仅支持非常平铺基础的键值对。
    """
    match = YAML_BLOCK_PATTERN.search(text)
    if not match:
        return {}
    block = match.group(1)
    lines = [line.rstrip() for line in block.splitlines()]
    cleaned = [line for line in lines if line.strip() != "---"]
    data: dict[str, Any] = {}
    for line in cleaned:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        scalar_match = SCALAR_PATTERN.match(line)
        if not scalar_match:
            continue
        key, raw_value, _comment = scalar_match.groups()
        data[key] = parse_scalar(raw_value)
    return data


def parse_scalar(raw_value: str) -> Any:
    """
    将提取的 YAML 字符串标量转换为 Python 基本类型。

    作用：支持 null, bool, int, 以及被引号包裹的字符串和内联字面量 JSON 数组解析。
    局限性：不支持浮点数（正则没有包含点位），不支持无引号的多行文字块解析。
    """
    value = raw_value.strip()
    if value in {"null", "Null", "NULL"}:
        return None
    if value in {"true", "false"}:
        return value == "true"
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    if len(value) >= 2 and value[0] == '"' and value[-1] == '"':
        return value[1:-1]
    if len(value) >= 2 and value[0] == "'" and value[-1] == "'":
        return value[1:-1]
    if value.startswith("[") and value.endswith("]"):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value
    return value


def format_scalar(value: Any) -> str:
    """
    将 Python 标量类型反序列化为 YAML 表字符。

    作用：安全格式化输出以供写回到文件。
    限制：列表会直接当作一行 json 写出。
    """
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, list):
        return json.dumps(value, ensure_ascii=False)
    return json.dumps(str(value), ensure_ascii=False)


def update_roadmap_fields(text: str, updates: dict[str, Any]) -> str:
    """
    将更新后的新元数据写入 ROADMAP 的 YAML 块中。

    工作流程：
    1. 查找到现有的 yaml 块起止位置。
    2. 如果 updates 里面的 key 在文件中已经存在，进行正则行替换（保留注释）。
    3. 如果 key 是新增的，插入到 yaml 块的末尾区域。
    4. 拼接回完整的 markdown 正文字符串。

    局限性：
    - 无法管理 YAML 行间的空格、多维嵌套。
    - 若没有 `---` 边界符可能会导致尾插位置错误。
    """
    match = YAML_BLOCK_PATTERN.search(text)
    if not match:
        raise ValueError("ROADMAP.md is missing a ```yaml block")
    block = match.group(1)
    lines = block.splitlines()
    stripped_lines = [line.strip() for line in lines]
    closing_index = max(index for index, line in enumerate(stripped_lines) if line == "---")
    seen: set[str] = set()
    for index, line in enumerate(lines):
        scalar_match = SCALAR_PATTERN.match(line)
        if not scalar_match:
            continue
        key = scalar_match.group(1)
        if key not in updates:
            continue
        seen.add(key)
        comment = scalar_match.group(3) or ""
        comment_suffix = f" {comment}" if comment and not comment.startswith(" ") else comment
        lines[index] = f"{key}: {format_scalar(updates[key])}{comment_suffix}"
    insertion_lines = [f"{key}: {format_scalar(value)}" for key, value in updates.items() if key not in seen]
    if insertion_lines:
        lines[closing_index:closing_index] = insertion_lines
    updated_block = "\n".join(lines)
    return text[: match.start(1)] + updated_block + text[match.end(1) :]


def save_roadmap(root: Path, updates: dict[str, Any]) -> dict[str, Any]:
    """
    修改后的值保存落盘到文件系统，并返回合并后的完整字典以供后续流程内存流转使用。
    """
    path, text, metadata = load_roadmap(root)
    merged = dict(metadata)
    merged.update(updates)
    path.write_text(update_roadmap_fields(text, updates), encoding="utf-8")
    return merged


def today_string() -> str:
    """获取当前时间的 YYYY-MM-DD 格式字符串。"""
    return dt.datetime.now(dt.timezone.utc).astimezone().strftime("%Y-%m-%d")


def ensure_parent(path: Path) -> None:
    """确保给定文件路径的父目录存在，不存在则递归创建。"""
    path.parent.mkdir(parents=True, exist_ok=True)


def slugify(value: str) -> str:
    """将字符串转换为只包含字母、数字和连字符的 URL 安全缩写形式。"""
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.lower()).strip("-")
    return slug or "untitled"


def read_text(path: Path, default: str = "") -> str:
    """
    安全读取文本文件。
    作用：如果文件不存在则返回提供的 default 默认值，而不会抛出异常。
    """
    if not path.exists():
        return default
    return path.read_text(encoding="utf-8")


def banner(metadata: dict[str, Any]) -> str:
    """
    基于项目元数据生成控制台展示用的状态横幅。
    作用：供各类命令调用或终端登录时显示当前项目研发处于哪个环节。
    """
    phase = metadata.get("Current_Phase", "Unknown")
    status = metadata.get("Phase_Status", "Unknown")
    mode = metadata.get("Active_Mode", "Unknown")
    debt = str(metadata.get("Pending_Debt", "Unknown")).lower()
    lines = [
        "═══════════════════════════════",
        f"📍 Phase: {phase}",
        f"🔄 Status: {status}",
        f"⚙️  Mode: {mode}  |  🔧 Debt: {debt}",
        "═══════════════════════════════",
    ]
    deadline = metadata.get("Debt_Deadline")
    if deadline not in (None, "", "null"):
        lines.append(f"Debt_Deadline: {deadline}")
    return "\n".join(lines)


def collect_memory_summary(root: Path) -> dict[str, Any]:
    """
    收集项目内部的记忆上下文（Memory Context）简报。

    工作流程：
    扫描 `.nexus/memory` 目录下的：
    - `today.md`：当日焦点
    - `active-tasks.json`：正在进行的代码任务
    - `blockers.md`：当前研发受阻项
    - `handoff.md`：交接清单
    并返回它们各自的统计值或首行标题以便快速了解当前上下文负担。
    """
    memory_root = root / ".nexus" / "memory"
    summary = {
        "today": "未记录",
        "active_tasks": 0,
        "blockers": 0,
        "handoff": "未记录",
    }
    today_path = memory_root / "today.md"
    if today_path.exists():
        lines = [line.strip() for line in today_path.read_text(encoding="utf-8").splitlines() if line.strip()]
        summary["today"] = next((line for line in lines if not line.startswith("#")), "已存在，待补充")
    active_tasks_path = memory_root / "active-tasks.json"
    if active_tasks_path.exists():
        try:
            payload = json.loads(active_tasks_path.read_text(encoding="utf-8"))
            summary["active_tasks"] = len(payload.get("tasks", []))
        except json.JSONDecodeError:
            summary["active_tasks"] = -1
    blockers_path = memory_root / "blockers.md"
    if blockers_path.exists():
        blockers = [
            line
            for line in blockers_path.read_text(encoding="utf-8").splitlines()
            if line.lstrip().startswith("- ") and "暂无阻塞" not in line
        ]
        summary["blockers"] = len(blockers)
    handoff_path = memory_root / "handoff.md"
    if handoff_path.exists():
        lines = [line.strip() for line in handoff_path.read_text(encoding="utf-8").splitlines() if line.strip()]
        summary["handoff"] = next((line for line in lines if not line.startswith("#")), "已存在，待补充")
    return summary


def next_action(metadata: dict[str, Any]) -> str:
    """
    根据当前项目的元数据状态，推断出“下一步”最需要做的标准动作建议。
    作用：为用户或 AI 助理提供上下文导航。
    """
    if metadata.get("Pending_Debt"):
        return "Pending_Debt 为 true；先清债，再考虑任何新功能。"
    project_stage = metadata.get("Project_Stage")
    if project_stage and project_stage != "DELIVERY":
        if project_stage == "IDEA":
            return "项目仍在 IDEA；先运行 /idea-capture 收敛问题定义。"
        if project_stage == "DISCOVERY":
            return "项目仍在 DISCOVERY；先运行 /mvp-shape 收窄 MVP。"
        return "项目尚未进入 DELIVERY；先运行 /roadmap-init 完成路线初始化。"
    phase_status = metadata.get("Phase_Status")
    mapping = {
        "PLANNING": "下一步：运行 /spec 生成当前阶段 SPEC。",
        "SPEC_READY": "下一步：编写红灯测试并推进到 RED_TESTS。",
        "RED_TESTS": "下一步：实现代码直到测试全绿。",
        "GREEN_CODE": "下一步：运行 /gate-check。",
        "GATE_CHECK": "下一步：补齐 walkthrough / review 后运行 /phase-end。",
        "REVIEW": "下一步：处理 review 结论并完成阶段归档。",
        "DONE": "下一步：运行 /phase-start 开启下一阶段。",
    }
    return mapping.get(phase_status, "下一步：先运行 /doctor 核对工作流状态。")


def sync_navigation_card(metadata: dict[str, Any]) -> dict[str, str]:
    """
    为 `/sync` 生成面向用户的导航卡文案。

    目标：
    - 首屏优先讲“现在在做什么、为什么、接下来怎么推进”
    - 默认使用人话，而不是要求用户先理解状态机术语
    - 把技术状态保留到附加信息中，而不是作为主文案
    """
    if metadata.get("Pending_Debt"):
        return {
            "current_step": "先清理当前遗留问题",
            "reason": "项目里还有已确认但未清理的债务，现在继续开新功能，后面只会更难维护。",
            "next_step": "先把当前债务收口并恢复到可继续推进的状态，再开始新的功能或阶段。",
        }

    project_stage = metadata.get("Project_Stage")
    clarity = metadata.get("Idea_Clarity", 3)
    if project_stage and project_stage != "DELIVERY":
        discovery_mapping = {
            "IDEA": {
                "current_step": "先把想法说清楚",
                "reason": "现在还只有一个模糊方向，直接写代码很容易做成你并不真正需要的东西。",
                "next_step": "先整理目标用户、核心问题和为什么值得做，再收敛最小版本。",
            },
            "DISCOVERY": {
                "current_step": "继续收敛问题和最小版本",
                "reason": "方向已经有了，但边界还不够清楚，现在进入实现会让范围越来越散。",
                "next_step": "先把最小可验证版本、范围边界和成功标准压缩清楚，再进入实现。",
            },
            "MVP_DEFINED": {
                "current_step": "把最小版本变成执行路线",
                "reason": "最小版本已经有轮廓了，但还没拆成可执行的阶段目标。",
                "next_step": "先把接下来几个阶段的目标排清楚，再进入正式交付。",
            },
            "ROADMAP_READY": {
                "current_step": "确认路线后再进入正式开发",
                "reason": "项目路线已经初步成型，但还需要确认当前阶段目标和整体约束，避免开工后漂移。",
                "next_step": "先确认路线、补齐项目上下文，再进入正式交付阶段。",
            },
        }
        if project_stage in discovery_mapping:
            return discovery_mapping[project_stage]

    if isinstance(clarity, int) and clarity < 3:
        return {
            "current_step": "先把目标和边界讲明白",
            "reason": "当前需求清晰度还不够，马上进入实现会让 AI 和人一起猜需求。",
            "next_step": "先补充目标用户、核心问题和最小版本边界，再开始新的开发阶段。",
        }

    phase_status = metadata.get("Phase_Status")
    phase_mapping = {
        "PLANNING": {
            "current_step": "先定义这一阶段到底要交付什么",
            "reason": "如果不先把范围、接口和边界说清楚，后面的测试和实现都会飘。",
            "next_step": "先把这一阶段的契约、边界和验收方式写清楚，再开始写测试。",
        },
        "SPEC_READY": {
            "current_step": "先把验收条件变成失败中的测试",
            "reason": "现在约束已经写清楚了，下一步应该先证明需求被准确表达出来，而不是直接实现。",
            "next_step": "先补齐会失败的测试，让验证标准落地，再开始写实现。",
        },
        "RED_TESTS": {
            "current_step": "把失败中的测试修到全绿",
            "reason": "验收条件已经就位，当前重点是只做满足这些条件的实现，避免一边写一边扩范围。",
            "next_step": "围绕已有测试完成最小实现，直到测试全部通过。",
        },
        "GREEN_CODE": {
            "current_step": "先做质量门禁检查",
            "reason": "代码已经初步完成，但还没证明它在类型、构建和测试层面都可交付。",
            "next_step": "执行完整的质量门禁检查，确认类型、构建和测试都通过后再收尾。",
        },
        "GATE_CHECK": {
            "current_step": "补齐阶段收尾材料",
            "reason": "质量门禁已经通过，但阶段还没有形成可追溯的评审和复盘证据。",
            "next_step": "补齐 walkthrough 和 review 产物，再结束当前阶段。",
        },
        "REVIEW": {
            "current_step": "处理评审结论并完成归档",
            "reason": "现在的关键不是继续扩功能，而是把评审提出的问题和结论收干净。",
            "next_step": "处理评审反馈，确认结果落地后完成阶段归档。",
        },
        "DONE": {
            "current_step": "准备进入下一阶段",
            "reason": "当前阶段已经完成，继续有效推进的关键是先明确下一个阶段只做什么。",
            "next_step": "确定下一阶段的唯一核心目标，然后启动新阶段。",
        },
    }
    return phase_mapping.get(
        phase_status,
        {
            "current_step": "先确认当前工作流状态",
            "reason": "当前状态没有被清晰识别，直接推进容易把节奏搞乱。",
            "next_step": "先核对脚手架和状态信息，确认当前位置后再继续。",
        },
    )


def sync_project_summary(metadata: dict[str, Any]) -> list[str]:
    """返回 `/sync` 的项目摘要信息。"""
    lines: list[str] = []
    core_problem = metadata.get("Core_Problem")
    if core_problem:
        lines.append(f"核心问题：{core_problem}")
    target_user = metadata.get("Target_User")
    if target_user:
        lines.append(f"目标用户：{target_user}")
    success_metrics = metadata.get("Success_Metrics")
    if success_metrics:
        lines.append(f"成功标准：{success_metrics}")
    return lines


def sync_debug_state(metadata: dict[str, Any]) -> list[str]:
    """返回 `/sync` 的附加技术状态，便于调试但不抢占首屏。"""
    project_stage = metadata.get("Project_Stage", "—")
    idea_clarity = metadata.get("Idea_Clarity", "—")
    vibe_count = metadata.get("Phases_Since_Vibe", 0)
    vibe_status = "已解锁" if isinstance(vibe_count, int) and vibe_count >= 3 else "未解锁"
    return [
        f"Project_Stage: {project_stage}",
        f"Idea_Clarity: {idea_clarity}",
        f"Vibe Sprint: {vibe_status}（计数 {vibe_count}）",
    ]


def cmd_sync(args: argparse.Namespace) -> int:
    """
    命令：/sync

    作用：读取并向控制台报告整个开发流程的状态快照，包括：
    - 当前阶段和状态机环节 (Banner)
    - 项目愿景与灵感成熟度
    - 近期记忆和遗留技术债
    - 下一步导航建议
    """
    root = repo_root(args.root)
    try:
        _, _, metadata = load_roadmap(root)
    except FileNotFoundError:
        if args.hook:
            return 0
        print("ROADMAP.md not found.")
        return 1
    print(banner(metadata))
    if args.hook:
        return 0
    navigation = sync_navigation_card(metadata)
    project_summary = sync_project_summary(metadata)
    memory = collect_memory_summary(root)
    debug_state = sync_debug_state(metadata)
    print()
    print("🧭 当前导航卡")
    print(f"当前步骤：{navigation['current_step']}")
    print(f"原因：{navigation['reason']}")
    print(f"下一步：{navigation['next_step']}")
    if project_summary:
        print()
        print("🎯 项目摘要")
        for line in project_summary:
            print(f"- {line}")
    print()
    print("🧠 热记忆摘要")
    print(f"  Today: {memory['today']}")
    print(f"  Active Tasks: {memory['active_tasks']}")
    print(f"  Blockers: {memory['blockers']}")
    print(f"  Handoff: {memory['handoff']}")
    print()
    print("🔎 附加状态")
    for line in debug_state:
        print(f"- {line}")
    return 0


def run_check(command: list[str], cwd: Path) -> tuple[bool, str]:
    """
    在宿主机子进程中执行给定命令。
    作用：用于质量门禁、脚本检测等执行。并将 stdout 和 stderr 合并返回。
    """
    result = subprocess.run(command, cwd=cwd, capture_output=True, text=True)
    output = "\n".join(part for part in [result.stdout.strip(), result.stderr.strip()] if part).strip()
    return result.returncode == 0, output


def fail_command(message: str) -> list[str]:
    """构造一个带可读错误信息的失败命令，供 gate-check 兜底使用。"""
    return ["python3", "-c", f"import sys; sys.stderr.write({message!r} + '\\n'); raise SystemExit(1)"]


def active_mode(metadata: dict[str, Any]) -> int:
    """将 ROADMAP 中的 Active_Mode 归一化为整数。"""
    try:
        return int(metadata.get("Active_Mode", 1))
    except (TypeError, ValueError):
        return 1


def package_scripts(root: Path) -> dict[str, str]:
    """读取 package.json 里的 scripts，读取失败时返回空字典。"""
    package_path = root / "package.json"
    if not package_path.exists():
        return {}
    try:
        payload = json.loads(package_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    scripts = payload.get("scripts", {})
    return scripts if isinstance(scripts, dict) else {}


def node_mode2_coverage_command(root: Path) -> list[str]:
    """
    生产模式下要求 Node 项目显式提供覆盖率校验脚本。
    优先寻找更明确的 coverage 校验脚本名；没有则直接失败。
    """
    scripts = package_scripts(root)
    for script_name in ["coverage:check", "test:coverage", "coverage"]:
        if script_name in scripts:
            return ["npm", "run", script_name]
    return fail_command("Mode 2 requires a Node coverage script: coverage:check, test:coverage, or coverage.")


def python_uses_pytest(root: Path) -> bool:
    """通过常见配置文件和 pytest 特征文件判断 Python 项目是否使用 pytest。"""
    config_candidates = [
        "pyproject.toml",
        "setup.py",
        "requirements.txt",
        "Pipfile",
        "pytest.ini",
        ".pytest.ini",
        "tox.ini",
    ]
    for name in config_candidates:
        path = root / name
        if path.exists() and "pytest" in path.read_text(encoding="utf-8").lower():
            return True
    return (root / "conftest.py").exists()


def collect_python_files(root: Path, base: Path | None = None) -> list[str]:
    """
    递归收集根目录下所有的 .py 源码文件以供检查编译。
    限制：自动忽略含有 `.venv` 和 `__pycache__` 的路径层级。
    """
    base_path = base or root
    return [
        str(path.relative_to(base_path))
        for path in root.rglob("*.py")
        if ".venv" not in path.parts and "__pycache__" not in path.parts
    ]


def detect_gate_commands(root: Path, metadata: dict[str, Any]) -> dict[str, list[list[str]]]:
    """
    动态感知并匹配项目质量门禁命令。

    作用：
    根据当前目录结构探寻主流技术栈标志点（如 package.json, go.mod, Cargo.toml 等），
    自动返回对应的类型检测、编译和测试的预置 CLI 命令集合。

    工作流程：
    1. 按主流工程入口文件检查优先顺序依此向后匹配。
    2. 如果探测到了已知语言特征文件，返回特定的三件套（type, build, tests）执行命令数组字典。
    3. 如果 Active_Mode 为 2（生产模式），则会为其自动追加更严苛的代码风格、静态分析和覆盖率检查门槛（如 require --coverage）。
    4. 如果都没有探测到，最后根据 ROADMAP 是否携带 Markdown 标签执行脚手架自身的基线命令。
    
    局限性：
    - 使用了极其硬编码的特征推断。
    - 无法处理 Monorepo 多微服务下的多入口文件（只扫描 root 层）。
    """
    mode = active_mode(metadata)
    if (root / "package.json").exists():
        commands = {
            "types": [["npm", "run", "typecheck"]],
            "build": [["npm", "run", "build"]],
            "tests": [["npm", "test"]],
        }
        if mode == 2:
            commands["types"].append(["npm", "run", "lint"])
            commands["tests"].append(node_mode2_coverage_command(root))
        return commands
    if (root / "pyproject.toml").exists() or (root / "setup.py").exists():
        py_files = collect_python_files(root)

        has_pytest = python_uses_pytest(root)
        if has_pytest:
            test_cmd = ["pytest"]
            coverage_cmd = ["pytest", "--cov=.", "--cov-report=term-missing", "--cov-fail-under=80"]
        else:
            test_cmd = ["python3", "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py"]
            coverage_cmd = ["coverage", "run", "-m", "unittest", "discover"]
            
        commands = {
            "types": [["python3", "-m", "py_compile", *py_files]] if py_files else [],
            "build": [["python3", "-m", "compileall", "."]],
            "tests": [test_cmd],
        }
        if mode == 2:
            commands["types"].insert(0, ["python3", "-m", "pylint", *py_files]) if py_files else None
            if has_pytest:
                commands["tests"] = [coverage_cmd]
            else:
                commands["tests"] = [coverage_cmd, ["coverage", "report", "-m", "--fail-under=80"]]
        return commands
    if (root / "go.mod").exists():
        commands = {
            "types": [["go", "vet", "./..."]],
            "build": [["go", "build", "./..."]],
            "tests": [["go", "test", "./..."]],
        }
        if mode == 2:
            commands["types"].insert(0, ["golangci-lint", "run"])
            commands["tests"] = [["go", "test", "-coverprofile=coverage.out", "./..."], ["go", "tool", "cover", "-func=coverage.out"]]
        return commands
    if (root / "pom.xml").exists():
        commands = {
            "types": [["mvn", "compiler:compile"]],
            "build": [["mvn", "package", "-DskipTests"]],
            "tests": [["mvn", "test"]],
        }
        if mode == 2:
            commands["types"].insert(0, ["mvn", "checkstyle:check"])
            commands["tests"] = [["mvn", "jacoco:report", "jacoco:check"]]
        return commands
    if (root / "build.gradle").exists() or (root / "build.gradle.kts").exists():
        gradlew = "./gradlew" if (root / "gradlew").exists() else "gradle"
        commands = {
            "types": [[gradlew, "classes"]],
            "build": [[gradlew, "assemble"]],
            "tests": [[gradlew, "test"]],
        }
        if mode == 2:
            commands["types"].insert(0, [gradlew, "checkstyleMain", "checkstyleTest"])
            commands["tests"].append([gradlew, "jacocoTestReport"])
        return commands
    if (root / "Cargo.toml").exists():
        commands = {
            "types": [["cargo", "check"]],
            "build": [["cargo", "build"]],
            "tests": [["cargo", "test"]],
        }
        if mode == 2:
            commands["types"].insert(0, ["cargo", "clippy", "--", "-D", "warnings"])
            commands["types"].insert(0, ["cargo", "fmt", "--", "--check"])
        return commands
    if (root / "CMakeLists.txt").exists():
        commands = {
            "types": [["cmake", "-B", "build"]],
            "build": [["cmake", "--build", "build"]],
            "tests": [["ctest", "--test-dir", "build"]],
        }
        if mode == 2:
            commands["types"].insert(0, ["clang-tidy", "-p", "build"])
            commands["tests"] = [["ctest", "--test-dir", "build", "--output-on-failure"]]
        return commands
    stack = str(metadata.get("Core_Tech_Stack", "")).lower()
    if "markdown" in stack and (root / ".claude" / "settings.json").exists() and (root / "scripts" / "nr.py").exists():
        commands = {
            "types": [["python3", "-m", "json.tool", ".claude/settings.json"]],
            "build": [],
            "tests": [["python3", "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py"]],
        }
        if (root / "install.sh").exists():
            commands["build"].append(["bash", "-n", "install.sh"])
        hook_files = sorted((root / ".claude" / "hooks").glob("*.sh"))
        for hook in hook_files:
            commands["build"].append(["bash", "-n", str(hook.relative_to(root))])
        python_files = collect_python_files(root / "scripts", root) if (root / "scripts").exists() else collect_python_files(root, root)
        if python_files:
            commands["build"].append(["python3", "-m", "py_compile", *python_files])
        if not any((root / "tests").glob("test_*.py")):
            commands["tests"] = [["python3", "-c", "print('No tests discovered; scaffold baseline only.')"]]
        return commands
    fallback_commands = {
        "types": [["python3", "-m", "json.tool", ".claude/settings.json"]] if (root / ".claude" / "settings.json").exists() else [],
        "build": [["bash", "-n", "install.sh"]] if (root / "install.sh").exists() else [],
        "tests": [["python3", "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py"]] if (root / "tests").exists() else [],
    }
    if mode == 2 and (root / "tests").exists():
        fallback_commands["tests"] = [["coverage", "run", "-m", "unittest", "discover", "-s", "tests"], ["coverage", "report", "-m", "--fail-under=80"]]
    return fallback_commands


def cmd_gate_check(args: argparse.Namespace) -> int:
    """
    命令：/gate-check

    作用：执行项目阶段性的质量门禁检查（Quality Gates）。

    工作流程：
    1. 动态探测本项目应使用的类型检测、编译、测试命令。
    2. 针对指定 scope（或全部）依此执行宿主机子进程验证。
    3. 如果全部通过，自动将 ROADMAP.md 的 Phase_Status 更新为 `GATE_CHECK`（除非传入 `--no-update`）。
    4. 任意一环失败都会阻断流程并打印错误日志。
    """
    root = repo_root(args.root)
    _, _, metadata = load_roadmap(root)
    commands = detect_gate_commands(root, metadata)
    scopes = [args.scope] if args.scope != "all" else ["types", "build", "tests"]
    failures: list[str] = []
    results: list[str] = []
    for scope in scopes:
        scope_commands = commands.get(scope, [])
        if not scope_commands:
            failures.append(f"{scope}: no command configured")
            continue
        for command in scope_commands:
            ok, output = run_check(command, root)
            label = f"{scope} -> {' '.join(shlex.quote(part) for part in command)}"
            if ok:
                results.append(f"PASS {label}")
            else:
                failures.append(f"FAIL {label}\n{output}".rstrip())
    if failures:
        print("❌ GATE CHECK FAILED")
        for item in failures:
            print()
            print(item)
        return 1
    if not args.no_update:
        save_roadmap(root, {"Phase_Status": "GATE_CHECK"})
    print("✅ GATE CHECK PASSED")
    for item in results:
        print(item)
    if not args.no_update:
        print("ROADMAP Phase_Status 已更新为 GATE_CHECK。")
    return 0


def discovery_guard_message(metadata: dict[str, Any]) -> str | None:
    """
    检查早期需求探索阶段防越权发车（Discovery Guardrails）。
    如果尚未达到交付标准（Idea不够清晰，或者还在收集 MVP），返回拦截的话术提示。
    """
    stage = metadata.get("Project_Stage", "DELIVERY")
    clarity = metadata.get("Idea_Clarity", 3)
    if stage != "DELIVERY":
        if stage == "IDEA":
            return "Project_Stage 仍为 IDEA，请先运行 /idea-capture。"
        if stage == "DISCOVERY":
            return "Project_Stage 仍为 DISCOVERY，请先运行 /mvp-shape。"
        return "Project_Stage 尚未进入 DELIVERY，请先运行 /roadmap-init。"
    if isinstance(clarity, int) and clarity < 3:
        return "Idea_Clarity < 3，请先补充 /idea-capture 或 /mvp-shape。"
    return None


def cmd_phase_start(args: argparse.Namespace) -> int:
    """
    命令：/phase-start

    作用：开启新的开发循环阶段。
    
    验证逻辑：
    - 不能有未清的技术债(`Pending_Debt`)。
    - 不能绕过早期产品发现流程(`discovery_guard_message`)。
    - 上一个 Phase 必须为 `DONE` 状态。
    如果全通过，会将阶段推进至 `PLANNING` 态。
    """
    root = repo_root(args.root)
    _, _, metadata = load_roadmap(root)
    if metadata.get("Pending_Debt"):
        print("Pending_Debt 为 true；禁止开启新阶段。")
        return 1
    guard = discovery_guard_message(metadata)
    if guard:
        print(guard)
        return 1
    if metadata.get("Phase_Status") != "DONE":
        print("上一阶段尚未完成；先完成 phase-end ritual。")
        return 1
    updates: dict[str, Any] = {"Phase_Status": "PLANNING"}
    if args.phase_name:
        updates["Current_Phase"] = args.phase_name
    merged = save_roadmap(root, updates)
    print("✅ Phase start checks passed")
    print(f"Current_Phase: {merged.get('Current_Phase')}")
    print("Phase_Status: PLANNING")
    print("下一步：运行 /spec 生成当前阶段 SPEC，并进入红灯测试。")
    return 0


def current_phase_number(metadata: dict[str, Any]) -> str:
    """提取形如 'Phase 1: xxx' 中匹配的数字 1。"""
    phase_text = str(metadata.get("Current_Phase", ""))
    match = re.search(r"Phase\s+(\d+)", phase_text)
    return match.group(1) if match else "X"


def cmd_phase_end(args: argparse.Namespace) -> int:
    """
    命令：/phase-end

    作用：结束当前开发阶段的收尾闭环。
    
    工作流程：
    1. 强制复核三道门禁(`/gate-check`)。
    2. 检查本次开发是否有归档产物证据（Walkthrough 和 Code Review）。
    3. 如果检查通过，将阶段标为 `DONE`。
    4. 累计未遇到技术债的快乐冲刺次数（Vibe），三连则触发正反馈提示。
    """
    root = repo_root(args.root)
    _, _, metadata = load_roadmap(root)
    gate_status = cmd_gate_check(argparse.Namespace(root=str(root), scope="all", no_update=True))
    if gate_status != 0:
        print("阶段结束已停止：三门禁未通过。")
        return 1
    phase_number = current_phase_number(metadata)
    walkthrough_path = root / "docs" / "walkthroughs" / f"WALKTHROUGH_PHASE_{phase_number}.md"
    review_path = root / "docs" / "reviews" / f"CODE_REVIEW_PHASE_{phase_number}.md"
    missing = [str(path.relative_to(root)) for path in [walkthrough_path, review_path] if not path.exists()]
    if missing:
        print("阶段结束已停止：缺少阶段产物。")
        for item in missing:
            print(f"- {item}")
        return 1
    vibe_count = metadata.get("Phases_Since_Vibe", 0)
    if not isinstance(vibe_count, int):
        vibe_count = 0
    updates = {"Phase_Status": "DONE", "Phases_Since_Vibe": vibe_count + 1}
    if not args.no_update:
        save_roadmap(root, updates)
    print("✅ 阶段结束检查通过")
    print(f"Walkthrough: {walkthrough_path.relative_to(root)}")
    print(f"Code Review: {review_path.relative_to(root)}")
    if vibe_count + 1 >= 3:
        print("🏄 已解锁下一次 Vibe Sprint。")
    return 0


def extract_lessons_from_journal(text: str) -> list[str]:
    lessons: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if "🕳️" in stripped:
            lessons.append(clean_lesson(stripped.replace("🕳️", "", 1)))
        if "最大意外" in stripped or "最大收获/教训" in stripped:
            parts = stripped.split("：", 1)
            if len(parts) == 2:
                lessons.append(clean_lesson(parts[1]))
    return [lesson for lesson in lessons if lesson]


def extract_lessons_from_review(text: str) -> list[str]:
    lessons: list[str] = []
    capture = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("## "):
            capture = "发现的问题" in stripped or "教训提炼" in stripped
            continue
        if capture and (stripped.startswith("- ") or stripped.startswith("|")):
            lessons.append(clean_lesson(stripped.lstrip("- ").strip("| ")))
    return [lesson for lesson in lessons if lesson]


def extract_lessons_from_walkthrough(text: str) -> list[str]:
    lessons: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("|") and "坑" not in stripped and "---" not in stripped:
            parts = [part.strip() for part in stripped.strip("|").split("|")]
            if len(parts) >= 2:
                lessons.append(clean_lesson(parts[1]))
        if "最大收获/教训" in stripped:
            parts = stripped.split("：", 1)
            if len(parts) == 2:
                lessons.append(clean_lesson(parts[1]))
    return [lesson for lesson in lessons if lesson]


def clean_lesson(text: str) -> str:
    """清理教训文本中的 Markdown 特殊字符。"""
    cleaned = re.sub(r"`+", "", text).strip()
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned.strip("- ").strip()


def classify_lesson(text: str) -> str:
    """
    根据关键字粗略推测该教训所属分类。
    作用：为 lessons.md 中的分栏做投递路由。
    """
    lowered = text.lower()
    if any(token in lowered for token in ["hook", "command", "workflow", "phase", "spec", "review", "gate", "估时"]):
        return "workflow"
    if any(token in lowered for token in ["架构", "boundary", "scope", "task", "memory", "状态机"]):
        return "architecture"
    return "tech"


def append_unique_lessons(existing: str, section: str, lessons: list[str]) -> tuple[str, int]:
    """将过滤排重后的教训集合安全写入到 Markdown 下对于的区块章节中。"""
    header = {
        "tech": "## 技术栈教训",
        "architecture": "## 架构教训",
        "workflow": "## 工作流教训",
    }[section]
    start = existing.find(header)
    if start == -1:
        return existing, 0
    next_header = existing.find("\n## ", start + len(header))
    section_body = existing[start: next_header if next_header != -1 else len(existing)]
    existing_items = {
        clean_lesson(line[2:])
        for line in section_body.splitlines()
        if line.strip().startswith("- ")
    }
    new_items = [lesson for lesson in lessons if lesson and clean_lesson(lesson) not in existing_items]
    if not new_items:
        return existing, 0
    insertion = "\n".join(f"- {lesson}" for lesson in new_items)
    if "当前为空" in section_body:
        updated_section = section_body.replace("> 当前为空。", "").replace("> 当前为空。执行 `/distill` 后会从 Journal 和 Walkthrough 中自动提炼。", "")
        updated_section = updated_section.rstrip() + "\n\n" + insertion + "\n"
    else:
        updated_section = section_body.rstrip() + "\n" + insertion + "\n"
    return existing.replace(section_body, updated_section), len(new_items)


def cmd_distill(args: argparse.Namespace) -> int:
    """
    命令：/distill

    作用：从项目开发历程的文书里提取智力结晶。
    
    工作流程：自动扫描过往所有的 Project Journal、Code Review 总结、Walkthroughs，
    把标注为“坑(🕳️)”或者“收获”的知识点提取出来。然后分门别类（技术栈、架构模式、工作流）
    排重后落盘写入 `.claude/rules/lessons.md`，使之转化为 AI 下次执行该项目的“长期记忆”。
    """
    root = repo_root(args.root)
    lessons_by_section = {"tech": [], "architecture": [], "workflow": []}
    source_counts = {"journal": 0, "walkthrough": 0, "review": 0}
    for path in sorted((root / "docs" / "journal").glob("*.md")):
        source_counts["journal"] += 1
        for lesson in extract_lessons_from_journal(path.read_text(encoding="utf-8")):
            lessons_by_section[classify_lesson(lesson)].append(lesson)
    for path in sorted((root / "docs" / "walkthroughs").glob("*.md")):
        source_counts["walkthrough"] += 1
        for lesson in extract_lessons_from_walkthrough(path.read_text(encoding="utf-8")):
            lessons_by_section[classify_lesson(lesson)].append(lesson)
    for path in sorted((root / "docs" / "reviews").glob("*.md")):
        source_counts["review"] += 1
        for lesson in extract_lessons_from_review(path.read_text(encoding="utf-8")):
            lessons_by_section[classify_lesson(lesson)].append(lesson)
    lessons_path = root / ".claude" / "rules" / "lessons.md"
    existing = read_text(lessons_path)
    new_total = 0
    updated = existing
    for section in ["tech", "architecture", "workflow"]:
        updated, added = append_unique_lessons(updated, section, dedupe(lessons_by_section[section]))
        new_total += added
    timestamp = dt.datetime.now(dt.timezone.utc).astimezone().isoformat(timespec="seconds")
    updated = re.sub(r"\*最后蒸馏时间：.*\*", f"*最后蒸馏时间：{timestamp}*", updated)
    updated = re.sub(
        r"\*蒸馏来源：.*\*",
        f"*蒸馏来源：{source_counts['journal']} Journal / {source_counts['walkthrough']} Walkthrough / {source_counts['review']} Review*",
        updated,
    )
    lessons_path.write_text(updated, encoding="utf-8")
    print("✅ 蒸馏完成")
    print(f"新增教训：{new_total}")
    print(
        "来源："
        f"{source_counts['journal']} Journal / "
        f"{source_counts['walkthrough']} Walkthrough / "
        f"{source_counts['review']} Review"
    )
    return 0


def dedupe(items: list[str]) -> list[str]:
    """保持写入顺序的通用排重。"""
    seen: set[str] = set()
    ordered: list[str] = []
    for item in items:
        normalized = clean_lesson(item)
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        ordered.append(normalized)
    return ordered


def render_template(template_path: Path, replacements: dict[str, str]) -> str:
    """简单的模板占位符渲染器。"""
    text = template_path.read_text(encoding="utf-8")
    for key, value in replacements.items():
        text = text.replace(key, value)
    return text


def write_project_doc(root: Path, relative_path: str, content: str) -> Path:
    """提供统一向工程写文档包裹口。包含连带创建无父文件夹的职责。"""
    path = root / relative_path
    ensure_parent(path)
    path.write_text(content, encoding="utf-8")
    return path


def cmd_idea_capture(args: argparse.Namespace) -> int:
    """
    命令：/idea-capture

    作用：在项目的极早期（IDEA 阶段）捕获原始的灵感。
    
    工作流程：
    1. 接收用户的单行/多行灵感输入。
    2. 基于模板生成结构化的 `docs/ideas/IDEA_BRIEF.md`。
    3. 驱动 ROADMAP 状态机进入 `DISCOVERY` 阶段，并置信度置为 1。
    """
    root = repo_root(args.root)
    _, _, metadata = load_roadmap(root)
    current_stage = metadata.get("Project_Stage", "IDEA")
    if current_stage not in {"IDEA", "DISCOVERY"}:
        print(f"❌ 错误：当前 Project_Stage 为 {current_stage}，不能直接重新运行 /idea-capture。")
        print("如需记录新想法，请写入 docs/ideas/IDEA_BACKLOG.md；如需重做 Discovery，请先手动确认并调整 ROADMAP。")
        return 1
    raw_idea = " ".join(args.raw_idea).strip()
    template_path = root / "docs" / "templates" / "IDEA_BRIEF_TEMPLATE.md"
    content = render_template(
        template_path,
        {
            "[DATE]": today_string(),
            "[RAW_IDEA]": raw_idea,
            "[VALUE_PROPOSITION]": "待明确",
            "[TARGET_USER]": "待明确",
            "[TRIGGER_SCENARIO]": "待明确",
            "[CORE_PAIN]": "待明确",
            "[CURRENT_ALTERNATIVES]": "待补充",
            "[WHY_NOW]": "待补充",
            "[UNKNOWNS]": "- 最大未知项：待验证",
            "[IDEA_CLARITY]": "1",
        },
    )
    output = write_project_doc(root, "docs/ideas/IDEA_BRIEF.md", content)
    save_roadmap(
        root,
        {
            "Project_Stage": "DISCOVERY",
            "Idea_Clarity": 1,
            "Core_Problem": raw_idea,
        },
    )
    print(f"✅ 已生成 {output.relative_to(root)}")
    print("下一步：运行 /mvp-shape 收窄 MVP。")
    return 0


def cmd_mvp_shape(args: argparse.Namespace) -> int:
    """
    命令：/mvp-shape

    作用：在项目探索中旬（DISCOVERY 阶段），强制收敛 MVP（最小可行性产品）边界。

    工作流程：
    1. 提取之前产出的 IDEA_BRIEF，合并接收用户的北极星指标。
    2. 基于模板生成 `docs/ideas/MVP_CANVAS.md`（定义 In Scope / Out of Scope）。
    3. 驱动 ROADMAP 状态机进入 `MVP_DEFINED`，置信度提升至 3。
    """
    root = repo_root(args.root)
    _, _, metadata = load_roadmap(root)
    current_stage = metadata.get("Project_Stage", "DISCOVERY")
    if current_stage in {"ROADMAP_READY", "DELIVERY"}:
        print(f"❌ 错误：当前 Project_Stage 为 {current_stage}，不能直接重新运行 /mvp-shape。")
        print("如需调整 MVP，请先手动确认并回退 ROADMAP 状态，或直接编辑现有 Discovery 文档。")
        return 1
    brief_path = root / "docs" / "ideas" / "IDEA_BRIEF.md"
    if not brief_path.exists():
        print("❌ 错误：未找到 IDEA_BRIEF.md。")
        print("请在收窄 MVP 之前先运行 /idea-capture 捕获初步灵感。")
        return 1
    idea_brief = read_text(brief_path)
    north_star = " ".join(args.north_star).strip() or "待明确的北极星目标"
    template_path = root / "docs" / "templates" / "MVP_CANVAS_TEMPLATE.md"
    content = render_template(
        template_path,
        {
            "[DATE]": today_string(),
            "[NORTH_STAR]": north_star,
            "[FIRST_USERS]": "待明确",
            "[CORE_JOURNEY]": "1. 进入 2. 完成关键动作 3. 获得验证反馈",
            "[IN_SCOPE]": "- 单一核心价值闭环",
            "[OUT_OF_SCOPE]": "- 非关键扩展功能\n- 过早平台化",
            "[SUCCESS_METRICS]": "- 指标 1：待明确\n- 指标 2：待明确",
            "[FAILURE_SIGNALS]": "- 信号 1：待明确",
            "[PRIMARY_RISK]": "待验证",
            "[VALIDATION_PLAN]": "通过最小原型或真实 workflow 验证。",
            "[UPSTREAM_IDEA]": idea_brief,
        },
    )
    output = write_project_doc(root, "docs/ideas/MVP_CANVAS.md", content)
    save_roadmap(
        root,
        {
            "Project_Stage": "MVP_DEFINED",
            "Idea_Clarity": 3,
            "Success_Metrics": "待在 MVP_CANVAS 中补充 2 个成功指标",
        },
    )
    print(f"✅ 已生成 {output.relative_to(root)}")
    print("下一步：运行 /roadmap-init 产出前三阶段路线。")
    return 0


def cmd_roadmap_init(args: argparse.Namespace) -> int:
    """
    命令：/roadmap-init

    作用：在需求探明后，为研发铺设前三个粗粒度的 Roadmap Phase 结构。
    
    工作流程：读取前置生成的 IDEA_BRIEF 和 MVP_CANVAS，合成一份初期整体目标路标。
    状态机将切片为 `ROADMAP_READY`，等待使用者手工将其切换成 `DELIVERY` 即可进入代码循环。
    """
    root = repo_root(args.root)
    _, _, metadata = load_roadmap(root)
    current_stage = metadata.get("Project_Stage", "MVP_DEFINED")
    if current_stage == "DELIVERY":
        print("❌ 错误：当前项目已进入 DELIVERY，不能直接重新运行 /roadmap-init。")
        print("如需重做路线，请先手动确认并回退 ROADMAP 状态，或直接编辑已有规划文档。")
        return 1
    
    # 强制卡点：如果没有产出前置的明确需求和单页画布，不允许生成整个项目的宏大 Roadmap
    brief_path = root / "docs" / "ideas" / "IDEA_BRIEF.md"
    canvas_path = root / "docs" / "ideas" / "MVP_CANVAS.md"
    
    missing: list[str] = []
    if not brief_path.exists():
        missing.append("IDEA_BRIEF.md")
    if not canvas_path.exists():
        missing.append("MVP_CANVAS.md")
        
    if missing:
        print(f"❌ 错误：未找到所需的前置探索文档 ({', '.join(missing)})。")
        print("请按顺序运行 /idea-capture 和 /mvp-shape 以收敛产品边界，之后再执行 /roadmap-init。")
        return 1

    idea_brief = read_text(brief_path)
    mvp_canvas = read_text(canvas_path)
    template_path = root / "docs" / "templates" / "ROADMAP_INIT_TEMPLATE.md"
    content = render_template(
        template_path,
        {
            "[DATE]": today_string(),
            "[PHASE_0_GOAL]": "初始化与验证准备",
            "[PHASE_1_GOAL]": "最小价值闭环",
            "[PHASE_2_GOAL]": "稳定性与反馈闭环",
            "[PHASE_3_GOAL]": "扩展能力或商业验证",
            "[PHASE_1_SINGLE_GOAL]": "只交付一个最小价值闭环",
            "[UPSTREAM_IDEA]": idea_brief,
            "[UPSTREAM_MVP]": mvp_canvas,
        },
    )
    output = write_project_doc(root, "docs/ideas/ROADMAP_INIT.md", content)
    save_roadmap(root, {"Project_Stage": "ROADMAP_READY"})
    print(f"✅ 已生成 {output.relative_to(root)}")
    print("下一步：补齐 ROADMAP / SYSTEM_CONTEXT 项目定义后，将 Project_Stage 切到 DELIVERY。")
    return 0


def cmd_hook_block_debt(args: argparse.Namespace) -> int:
    """
    命令：/hook-block-debt
    
    作用：供 Claude Code 的 `PreToolUse` hook 调用的拦截器。

    工作流程：
    解析 AI 要触发的工具请求，如果当前状态处于具有未还技术债（Pending_Debt 开启），
    且捕捉行为为 `git commit` 或 `git push`，则在标准错误流中输出阻止语，
    并返回非 0 退出码强制拦截当前 AI 修改，逼迫其先完成技术债清还。
    """
    root = repo_root(args.root)
    path = roadmap_path(root)
    if path is None:
        return 0
    metadata = parse_yaml_metadata(path.read_text(encoding="utf-8"))
    if not metadata.get("Pending_Debt"):
        return 0
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0
    command = payload.get("tool_input", {}).get("command", "")
    if re.search(r"(^|\s)git\s+(commit|push)(\s|$)", command):
        print("Blocked by NexusRhythm: Pending_Debt is true. Clear debt before commit or push.", file=sys.stderr)
        return 2
    return 0


def required_paths(root: Path) -> dict[str, Path]:
    """返回所有脚手架必需的核心文件与目录字典。"""
    return {
        "roadmap": root / "ROADMAP.md",
        "claude": root / "CLAUDE.md",
        "ci_workflow": root / ".github" / "workflows" / "ci.yml",
        "settings": root / ".claude" / "settings.json",
        "commands": root / ".claude" / "commands",
        "agents": root / ".claude" / "agents",
        "template_idea": root / "docs" / "templates" / "IDEA_BRIEF_TEMPLATE.md",
        "template_idea_review": root / "docs" / "templates" / "IDEA_REVIEW_TEMPLATE.md",
        "template_mvp": root / "docs" / "templates" / "MVP_CANVAS_TEMPLATE.md",
        "template_roadmap": root / "docs" / "templates" / "ROADMAP_INIT_TEMPLATE.md",
        "template_spec": root / "docs" / "templates" / "SPEC_TEMPLATE.md",
        "template_walkthrough": root / "docs" / "templates" / "WALKTHROUGH_TEMPLATE.md",
        "template_code_review": root / "docs" / "templates" / "CODE_REVIEW_TEMPLATE.md",
        "template_journal": root / "docs" / "templates" / "JOURNAL_TEMPLATE.md",
        "template_adr": root / "docs" / "templates" / "ADR_TEMPLATE.md",
        "nexus_tasks": root / ".nexus" / "tasks",
        "nexus_memory": root / ".nexus" / "memory",
    }


def expected_commands() -> list[str]:
    """列出按规管辖的系统插件化斜杠命令清单。"""
    return [
        "sync.md",
        "phase-start.md",
        "gate-check.md",
        "phase-end.md",
        "review.md",
        "idea-review.md",
        "doctor.md",
        "idea-capture.md",
        "mvp-shape.md",
        "roadmap-init.md",
        "spec.md",
        "distill.md",
        "journal.md",
        "decision.md",
        "retro.md",
    ]


def cmd_doctor(args: argparse.Namespace) -> int:
    """
    命令：/doctor
    
    作用：自我诊断检测当前工程中的脚手架是否安装正确、完备且合规。
    
    工作流程：
    1. 扫描 `roadmap.md`、`settings.json`、`hook.sh`、`commands` 等所有必须骨架存在情况。
    2. 使用 `bash -n` 检测注入钩子的语法是否损坏，验证其可执行位。
    3. 全量模式(`full`)下还会扫描项目的 README/手册是否有合规配置。
    4. 按照健康程度输出为（GREEN - 通过）、（YELLOW - 警告）、（RED - 严重损坏，挂载退出码 1）。
    """
    root = repo_root(args.root)
    green: list[str] = []
    yellow: list[str] = []
    red: list[str] = []
    for label, path in required_paths(root).items():
        if path.exists():
            green.append(f"{label}: {path.relative_to(root)}")
        else:
            red.append(f"missing {label}: {path.relative_to(root)}")
    settings_path = root / ".claude" / "settings.json"
    if settings_path.exists():
        try:
            json.loads(settings_path.read_text(encoding="utf-8"))
            green.append("settings.json is valid JSON")
        except json.JSONDecodeError as exc:
            red.append(f"settings.json invalid JSON: {exc}")
    for hook in sorted((root / ".claude" / "hooks").glob("*.sh")):
        ok, output = run_check(["bash", "-n", str(hook.relative_to(root))], root)
        if ok:
            green.append(f"hook syntax ok: {hook.relative_to(root)}")
        else:
            red.append(f"hook syntax failed: {hook.relative_to(root)} -> {output}")
        if os.access(hook, os.X_OK):
            green.append(f"hook executable: {hook.relative_to(root)}")
        else:
            yellow.append(f"hook not executable: {hook.relative_to(root)}")
    commands_dir = root / ".claude" / "commands"
    for filename in expected_commands():
        if (commands_dir / filename).exists():
            green.append(f"command wired: /{filename[:-3]}")
        else:
            red.append(f"missing command: /{filename[:-3]}")
    if args.mode == "full":
        docs_to_scan = [root / "README.md", root / "CLAUDE.md", root / "docs" / "RHYTHM.md", root / "ROADMAP.md"]
        for doc in docs_to_scan:
            content = read_text(doc)
            if "Project_Stage" in content or doc.name in {"CLAUDE.md", "RHYTHM.md"}:
                green.append(f"docs scanned: {doc.relative_to(root)}")
            else:
                yellow.append(f"docs may not mention discovery controls: {doc.relative_to(root)}")
        walkthrough = root / "docs" / "walkthroughs" / "WALKTHROUGH_PHASE_0.md"
        review = root / "docs" / "reviews" / "CODE_REVIEW_PHASE_0.md"
        if walkthrough.exists() and review.exists():
            green.append("phase artifact baseline exists")
        else:
            yellow.append("phase artifact baseline incomplete")
        memory_summary = collect_memory_summary(root)
        if memory_summary["active_tasks"] == -1:
            red.append("active-tasks.json is not valid JSON")
    status = "GREEN"
    if red:
        status = "RED"
    elif yellow:
        status = "YELLOW"
    print(f"{status} — doctor ({args.mode})")
    print("PASS:")
    for item in green:
        print(f"- {item}")
    print("WARN:")
    for item in yellow:
        print(f"- {item}")
    print("FAIL:")
    for item in red:
        print(f"- {item}")
    if red:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
