from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def run(command: list[str], cwd: Path, *, env: dict[str, str] | None = None, input_text: str | None = None) -> subprocess.CompletedProcess[str]:
    merged_env = os.environ.copy()
    if env:
        merged_env.update(env)
    return subprocess.run(
        command,
        cwd=cwd,
        env=merged_env,
        input=input_text,
        text=True,
        capture_output=True,
        check=False,
    )


def install_project(target: Path) -> None:
    result = run(["bash", str(REPO_ROOT / "install.sh"), str(target)], REPO_ROOT)
    if result.returncode != 0:
        raise AssertionError(result.stderr or result.stdout)


def parse_roadmap_field(project_root: Path, key: str) -> str:
    text = (project_root / "ROADMAP.md").read_text(encoding="utf-8")
    match = re.search(rf"^{re.escape(key)}:\s*(.*?)\s*(?:#.*)?$", text, re.MULTILINE)
    if not match:
        raise AssertionError(f"Missing {key} in ROADMAP.md")
    value = match.group(1).strip()
    if value.startswith('"') and value.endswith('"'):
        return value[1:-1]
    return value


def replace_roadmap_field(project_root: Path, key: str, value: str) -> None:
    roadmap_path = project_root / "ROADMAP.md"
    text = roadmap_path.read_text(encoding="utf-8")
    updated = re.sub(
        rf"^({re.escape(key)}:\s*)(.*?)(\s*(?:#.*)?)$",
        lambda match: f"{match.group(1)}{value}{match.group(3)}",
        text,
        count=1,
        flags=re.MULTILINE,
    )
    roadmap_path.write_text(updated, encoding="utf-8")


def make_executable(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")
    path.chmod(0o755)


class NexusRhythmSmokeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.project_root = Path(self.temp_dir.name) / "project"
        install_project(self.project_root)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_install_wires_scripts_commands_templates_and_memory(self) -> None:
        expected_paths = [
            self.project_root / "scripts" / "nr.py",
            self.project_root / ".claude" / "commands" / "review.md",
            self.project_root / ".claude" / "commands" / "doctor.md",
            self.project_root / ".claude" / "commands" / "idea-capture.md",
            self.project_root / ".claude" / "commands" / "mvp-shape.md",
            self.project_root / ".claude" / "commands" / "roadmap-init.md",
            self.project_root / "docs" / "ideas" / "README.md",
            self.project_root / "docs" / "templates" / "IDEA_BRIEF_TEMPLATE.md",
            self.project_root / ".nexus" / "memory" / "active-tasks.json",
            self.project_root / ".nexus" / "tasks" / "README.md",
        ]
        for path in expected_paths:
            self.assertTrue(path.exists(), str(path))

    def test_session_start_status_output(self) -> None:
        result = run(
            ["bash", str(self.project_root / ".claude" / "hooks" / "session-status.sh")],
            self.project_root,
            env={"CLAUDE_PROJECT_DIR": str(self.project_root)},
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("📍 Phase:", result.stdout)
        self.assertIn("🔄 Status:", result.stdout)

    def test_session_start_without_roadmap_is_silent(self) -> None:
        (self.project_root / "ROADMAP.md").unlink()
        result = run(
            ["bash", str(self.project_root / ".claude" / "hooks" / "session-status.sh")],
            self.project_root,
            env={"CLAUDE_PROJECT_DIR": str(self.project_root)},
        )
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.strip(), "")

    def test_pre_tool_use_blocks_git_commit_with_debt(self) -> None:
        replace_roadmap_field(self.project_root, "Pending_Debt", "true")
        payload = json.dumps({"tool_input": {"command": "git commit -m test"}})
        result = run(
            ["bash", str(self.project_root / ".claude" / "hooks" / "block-debt-commits.sh")],
            self.project_root,
            env={"CLAUDE_PROJECT_DIR": str(self.project_root)},
            input_text=payload,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("Pending_Debt is true", result.stderr)

    def test_pre_tool_use_allows_safe_bash(self) -> None:
        replace_roadmap_field(self.project_root, "Pending_Debt", "true")
        payload = json.dumps({"tool_input": {"command": "npm test"}})
        result = run(
            ["bash", str(self.project_root / ".claude" / "hooks" / "block-debt-commits.sh")],
            self.project_root,
            env={"CLAUDE_PROJECT_DIR": str(self.project_root)},
            input_text=payload,
        )
        self.assertEqual(result.returncode, 0)

    def test_gate_check_passes_on_installed_scaffold(self) -> None:
        result = run(["python3", "scripts/nr.py", "gate-check"], self.project_root)
        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
        self.assertEqual(parse_roadmap_field(self.project_root, "Phase_Status"), "GATE_CHECK")

    def test_phase_start_rejects_when_project_not_in_delivery(self) -> None:
        replace_roadmap_field(self.project_root, "Project_Stage", '"DISCOVERY"')
        replace_roadmap_field(self.project_root, "Phase_Status", "DONE")
        result = run(["python3", "scripts/nr.py", "phase-start", "Phase 1 - Test"], self.project_root)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("/mvp-shape", result.stdout)

    def test_phase_start_rejects_when_idea_clarity_is_too_low(self) -> None:
        replace_roadmap_field(self.project_root, "Project_Stage", '"DELIVERY"')
        replace_roadmap_field(self.project_root, "Idea_Clarity", "2")
        replace_roadmap_field(self.project_root, "Phase_Status", "DONE")
        result = run(["python3", "scripts/nr.py", "phase-start", "Phase 1 - Test"], self.project_root)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Idea_Clarity < 3", result.stdout)

    def test_discovery_commands_generate_artifacts_and_update_state(self) -> None:
        replace_roadmap_field(self.project_root, "Project_Stage", '"IDEA"')
        result = run(["python3", "scripts/nr.py", "idea-capture", "A fuzzy workflow idea"], self.project_root)
        self.assertEqual(result.returncode, 0)
        self.assertTrue((self.project_root / "docs" / "ideas" / "IDEA_BRIEF.md").exists())
        self.assertEqual(parse_roadmap_field(self.project_root, "Project_Stage"), "DISCOVERY")

        result = run(["python3", "scripts/nr.py", "mvp-shape", "First usable workflow"], self.project_root)
        self.assertEqual(result.returncode, 0)
        self.assertTrue((self.project_root / "docs" / "ideas" / "MVP_CANVAS.md").exists())
        self.assertEqual(parse_roadmap_field(self.project_root, "Project_Stage"), "MVP_DEFINED")

        result = run(["python3", "scripts/nr.py", "roadmap-init"], self.project_root)
        self.assertEqual(result.returncode, 0)
        self.assertTrue((self.project_root / "docs" / "ideas" / "ROADMAP_INIT.md").exists())
        self.assertEqual(parse_roadmap_field(self.project_root, "Project_Stage"), "ROADMAP_READY")

    def test_idea_capture_refuses_to_rewind_delivery_projects(self) -> None:
        result = run(["python3", "scripts/nr.py", "idea-capture", "Late idea"], self.project_root)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("不能直接重新运行 /idea-capture", result.stdout)
        self.assertEqual(parse_roadmap_field(self.project_root, "Project_Stage"), "DELIVERY")

    def test_mvp_shape_refuses_to_rewind_delivery_projects(self) -> None:
        result = run(["python3", "scripts/nr.py", "mvp-shape", "North star"], self.project_root)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("不能直接重新运行 /mvp-shape", result.stdout)
        self.assertEqual(parse_roadmap_field(self.project_root, "Project_Stage"), "DELIVERY")

    def test_roadmap_init_refuses_to_rewind_delivery_projects(self) -> None:
        result = run(["python3", "scripts/nr.py", "roadmap-init"], self.project_root)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("当前项目已进入 DELIVERY", result.stdout)
        self.assertEqual(parse_roadmap_field(self.project_root, "Project_Stage"), "DELIVERY")

    def test_distill_appends_new_lessons(self) -> None:
        journal_path = self.project_root / "docs" / "journal" / "2026-03-08.md"
        journal_path.parent.mkdir(parents=True, exist_ok=True)
        journal_path.write_text("# Journal\n\n- 🕳️ Hooks drift must be validated with smoke tests.\n", encoding="utf-8")
        result = run(["python3", "scripts/nr.py", "distill"], self.project_root)
        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
        lessons_text = (self.project_root / ".claude" / "rules" / "lessons.md").read_text(encoding="utf-8")
        self.assertIn("Hooks drift must be validated with smoke tests.", lessons_text)
        self.assertNotIn("最后蒸馏时间：——", lessons_text)

    def test_spec_command_references_discovery_inputs_and_scope_drift(self) -> None:
        spec_text = (self.project_root / ".claude" / "commands" / "spec.md").read_text(encoding="utf-8")
        self.assertIn("IDEA_BRIEF", spec_text)
        self.assertIn("MVP_CANVAS", spec_text)
        self.assertIn("scope 漂移", spec_text)

    def test_doctor_fails_when_spec_template_is_missing(self) -> None:
        (self.project_root / "docs" / "templates" / "SPEC_TEMPLATE.md").unlink()
        result = run(["python3", "scripts/nr.py", "doctor", "quick"], self.project_root)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("missing template_spec", result.stdout)

    def test_gate_check_mode2_node_requires_coverage_script(self) -> None:
        replace_roadmap_field(self.project_root, "Active_Mode", "2")
        bin_dir = self.project_root / "bin"
        bin_dir.mkdir()
        npm_log = self.project_root / "npm.log"
        make_executable(
            bin_dir / "npm",
            "#!/usr/bin/env bash\n"
            "echo \"$*\" >> \"$NPM_LOG\"\n"
            "exit 0\n",
        )
        package_json = {
            "name": "demo",
            "scripts": {
                "typecheck": "echo typecheck",
                "lint": "echo lint",
                "build": "echo build",
                "test": "echo test",
            },
        }
        (self.project_root / "package.json").write_text(json.dumps(package_json), encoding="utf-8")
        env = {
            "PATH": f"{bin_dir}{os.pathsep}{os.environ['PATH']}",
            "NPM_LOG": str(npm_log),
        }
        result = run(["python3", "scripts/nr.py", "gate-check"], self.project_root, env=env)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Mode 2 requires a Node coverage script", result.stdout)

    def test_gate_check_uses_pytest_when_project_declares_it(self) -> None:
        bin_dir = self.project_root / "bin"
        bin_dir.mkdir()
        pytest_log = self.project_root / "pytest.log"
        make_executable(
            bin_dir / "pytest",
            "#!/usr/bin/env bash\n"
            "echo \"$*\" > \"$PYTEST_LOG\"\n"
            "exit 0\n",
        )
        (self.project_root / "pyproject.toml").write_text(
            "[project]\nname = \"demo\"\nversion = \"0.1.0\"\n\n[tool.pytest.ini_options]\naddopts = \"-q\"\n",
            encoding="utf-8",
        )
        env = {
            "PATH": f"{bin_dir}{os.pathsep}{os.environ['PATH']}",
            "PYTEST_LOG": str(pytest_log),
        }
        result = run(["python3", "scripts/nr.py", "gate-check", "tests"], self.project_root, env=env)
        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
        self.assertEqual(pytest_log.read_text(encoding="utf-8").strip(), "")

    def test_gate_check_mode2_pytest_adds_coverage_flags(self) -> None:
        replace_roadmap_field(self.project_root, "Active_Mode", "2")
        bin_dir = self.project_root / "bin"
        bin_dir.mkdir()
        pytest_log = self.project_root / "pytest-mode2.log"
        make_executable(
            bin_dir / "pytest",
            "#!/usr/bin/env bash\n"
            "echo \"$*\" > \"$PYTEST_LOG\"\n"
            "exit 0\n",
        )
        (self.project_root / "pyproject.toml").write_text(
            "[project]\nname = \"demo\"\nversion = \"0.1.0\"\n\n[tool.pytest.ini_options]\naddopts = \"-q\"\n",
            encoding="utf-8",
        )
        env = {
            "PATH": f"{bin_dir}{os.pathsep}{os.environ['PATH']}",
            "PYTEST_LOG": str(pytest_log),
        }
        result = run(["python3", "scripts/nr.py", "gate-check", "tests"], self.project_root, env=env)
        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
        logged_args = pytest_log.read_text(encoding="utf-8").strip()
        self.assertIn("--cov=.", logged_args)
        self.assertIn("--cov-fail-under=80", logged_args)


if __name__ == "__main__":
    unittest.main()
