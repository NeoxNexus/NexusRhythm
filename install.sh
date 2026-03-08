#!/usr/bin/env bash
# NexusRhythm — install.sh
# 将框架文件注入已有项目（不覆盖已有文件）
#
# 用法：
#   bash install.sh                    # 在当前目录安装
#   bash install.sh /path/to/project   # 指定项目目录
#   curl -fsSL https://raw.githubusercontent.com/NeoxNexus/NexusRhythm/main/install.sh | bash

set -euo pipefail

SCRIPT_PATH="${BASH_SOURCE[0]:-$0}"
SCRIPT_DIR="$(cd "$(dirname "$SCRIPT_PATH")" && pwd)"
TARGET_DIR="${1:-$(pwd)}"
SOURCE_DIR=""
BOOTSTRAP_DIR=""
REPO_SLUG="${NEXUSRHYTHM_REPO:-NeoxNexus/NexusRhythm}"
REPO_REF="${NEXUSRHYTHM_REF:-main}"

cleanup() {
  if [ -n "$BOOTSTRAP_DIR" ] && [ -d "$BOOTSTRAP_DIR" ]; then
    rm -rf "$BOOTSTRAP_DIR"
  fi
}

trap cleanup EXIT

has_source_tree() {
  local root="$1"
  local required=(
    "CLAUDE.md"
    "ROADMAP.md"
    "docs/RHYTHM.md"
    "docs/SYSTEM_CONTEXT.md"
    "docs/ideas/README.md"
    ".claude/settings.json"
    "scripts/nr.py"
  )
  local relative_path=""
  for relative_path in "${required[@]}"; do
    if [ ! -e "$root/$relative_path" ]; then
      return 1
    fi
  done
  return 0
}

download_source_tree() {
  local archive_url="https://codeload.github.com/${REPO_SLUG}/tar.gz/refs/heads/${REPO_REF}"
  if ! command -v curl >/dev/null 2>&1; then
    echo "❌ 未找到 curl，无法下载 NexusRhythm 源码。" >&2
    exit 1
  fi
  if ! command -v tar >/dev/null 2>&1; then
    echo "❌ 未找到 tar，无法解压 NexusRhythm 源码包。" >&2
    exit 1
  fi

  BOOTSTRAP_DIR="$(mktemp -d)"
  echo "🌐 未检测到完整源码，正在下载 ${REPO_SLUG}@${REPO_REF} ..."
  curl -fsSL "$archive_url" | tar -xzf - -C "$BOOTSTRAP_DIR"
  SOURCE_DIR="$(find "$BOOTSTRAP_DIR" -mindepth 1 -maxdepth 1 -type d | head -n 1)"

  if [ -z "$SOURCE_DIR" ] || ! has_source_tree "$SOURCE_DIR"; then
    echo "❌ 已下载源码包，但缺少安装所需文件。" >&2
    exit 1
  fi
}

resolve_source_dir() {
  if [ -n "${NEXUSRHYTHM_SOURCE_DIR:-}" ]; then
    SOURCE_DIR="$(cd "$NEXUSRHYTHM_SOURCE_DIR" && pwd)"
    if ! has_source_tree "$SOURCE_DIR"; then
      echo "❌ NEXUSRHYTHM_SOURCE_DIR 未指向有效的 NexusRhythm 源码目录。" >&2
      exit 1
    fi
    return
  fi

  if has_source_tree "$SCRIPT_DIR"; then
    SOURCE_DIR="$SCRIPT_DIR"
    return
  fi

  download_source_tree
}

resolve_source_dir

echo ""
echo "🎵 NexusRhythm — 安装开始"
echo "   目标目录: $TARGET_DIR"
echo ""

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

copy_if_not_exists() {
  local src="$1"
  local dst="$2"
  if [ -e "$dst" ]; then
    echo -e "  ${YELLOW}⚠️  已存在（跳过）${NC}: $(basename "$dst")"
  else
    mkdir -p "$(dirname "$dst")"
    cp "$src" "$dst"
    echo -e "  ${GREEN}✅ 已创建${NC}: ${dst#$TARGET_DIR/}"
  fi
}

echo "📋 安装核心文件..."
copy_if_not_exists "$SOURCE_DIR/CLAUDE.md" "$TARGET_DIR/CLAUDE.md"
copy_if_not_exists "$SOURCE_DIR/ROADMAP.md" "$TARGET_DIR/ROADMAP.md"

echo ""
echo "📚 安装文档规范..."
copy_if_not_exists "$SOURCE_DIR/docs/RHYTHM.md" "$TARGET_DIR/docs/RHYTHM.md"
copy_if_not_exists "$SOURCE_DIR/docs/SYSTEM_CONTEXT.md" "$TARGET_DIR/docs/SYSTEM_CONTEXT.md"
copy_if_not_exists "$SOURCE_DIR/docs/ideas/README.md" "$TARGET_DIR/docs/ideas/README.md"

echo ""
echo "📝 安装文档模板..."
for tmpl in "$SOURCE_DIR/docs/templates/"*.md; do
  fname=$(basename "$tmpl")
  copy_if_not_exists "$tmpl" "$TARGET_DIR/docs/templates/$fname"
done

echo ""
echo "🤖 安装 Claude Code 集成..."
copy_if_not_exists "$SOURCE_DIR/.claude/settings.json" "$TARGET_DIR/.claude/settings.json"

echo ""
echo "🛠️  安装脚本执行层..."
for script in "$SOURCE_DIR/scripts/"*.py; do
  fname=$(basename "$script")
  copy_if_not_exists "$script" "$TARGET_DIR/scripts/$fname"
done

for hook in "$SOURCE_DIR/.claude/hooks/"*.sh; do
  fname=$(basename "$hook")
  copy_if_not_exists "$hook" "$TARGET_DIR/.claude/hooks/$fname"
done

for agent in "$SOURCE_DIR/.claude/agents/"*.md; do
  fname=$(basename "$agent")
  copy_if_not_exists "$agent" "$TARGET_DIR/.claude/agents/$fname"
done

if [ -d "$SOURCE_DIR/.claude/skills" ]; then
  while IFS= read -r -d '' skill_file; do
    relative_path="${skill_file#"$SOURCE_DIR/"}"
    copy_if_not_exists "$skill_file" "$TARGET_DIR/$relative_path"
  done < <(find "$SOURCE_DIR/.claude/skills" -type f -print0)
fi

for rule in "$SOURCE_DIR/.claude/rules/"*.md; do
  fname=$(basename "$rule")
  copy_if_not_exists "$rule" "$TARGET_DIR/.claude/rules/$fname"
done

for cmd in "$SOURCE_DIR/.claude/commands/"*.md; do
  fname=$(basename "$cmd")
  copy_if_not_exists "$cmd" "$TARGET_DIR/.claude/commands/$fname"
done

echo ""
echo "📁 创建必要目录..."
for dir in \
  "tests" \
  "docs/specs" \
  "docs/walkthroughs" \
  "docs/reviews" \
  "docs/journal" \
  "docs/decisions" \
  "docs/ideas" \
  ".nexus/tasks" \
  ".nexus/memory"; do
  if [ ! -d "$TARGET_DIR/$dir" ]; then
    mkdir -p "$TARGET_DIR/$dir"
    touch "$TARGET_DIR/$dir/.gitkeep"
    echo -e "  ${GREEN}✅ 已创建${NC}: $dir/"
  fi
done

copy_if_not_exists "$SOURCE_DIR/.nexus/tasks/README.md" "$TARGET_DIR/.nexus/tasks/README.md"
copy_if_not_exists "$SOURCE_DIR/.nexus/memory/today.md" "$TARGET_DIR/.nexus/memory/today.md"
copy_if_not_exists "$SOURCE_DIR/.nexus/memory/active-tasks.json" "$TARGET_DIR/.nexus/memory/active-tasks.json"
copy_if_not_exists "$SOURCE_DIR/.nexus/memory/blockers.md" "$TARGET_DIR/.nexus/memory/blockers.md"
copy_if_not_exists "$SOURCE_DIR/.nexus/memory/handoff.md" "$TARGET_DIR/.nexus/memory/handoff.md"

echo ""
echo "════════════════════════════════════════"
echo "🎉 NexusRhythm 安装完成！"
echo ""
echo "   下一步："
echo "   1. 编辑 ROADMAP.md — 填写项目名称、目标、技术栈"
echo "   2. 编辑 docs/SYSTEM_CONTEXT.md — 描述架构决策"
echo "   3. 用 Claude Code 打开项目，输入 /sync"
echo "════════════════════════════════════════"
echo ""
