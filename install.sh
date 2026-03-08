#!/usr/bin/env bash
# NexusRhythm — install.sh
# 将框架文件注入已有项目（不覆盖已有文件）
#
# 用法：
#   bash install.sh                    # 在当前目录安装
#   bash install.sh /path/to/project   # 指定项目目录

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_DIR="${1:-$(pwd)}"

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
copy_if_not_exists "$SCRIPT_DIR/CLAUDE.md" "$TARGET_DIR/CLAUDE.md"
copy_if_not_exists "$SCRIPT_DIR/ROADMAP.md" "$TARGET_DIR/ROADMAP.md"

echo ""
echo "📚 安装文档规范..."
copy_if_not_exists "$SCRIPT_DIR/docs/RHYTHM.md" "$TARGET_DIR/docs/RHYTHM.md"
copy_if_not_exists "$SCRIPT_DIR/docs/SYSTEM_CONTEXT.md" "$TARGET_DIR/docs/SYSTEM_CONTEXT.md"
copy_if_not_exists "$SCRIPT_DIR/docs/ideas/README.md" "$TARGET_DIR/docs/ideas/README.md"

echo ""
echo "📝 安装文档模板..."
for tmpl in "$SCRIPT_DIR/docs/templates/"*.md; do
  fname=$(basename "$tmpl")
  copy_if_not_exists "$tmpl" "$TARGET_DIR/docs/templates/$fname"
done

echo ""
echo "🤖 安装 Claude Code 集成..."
copy_if_not_exists "$SCRIPT_DIR/.claude/settings.json" "$TARGET_DIR/.claude/settings.json"

echo ""
echo "🛠️  安装脚本执行层..."
for script in "$SCRIPT_DIR/scripts/"*.py; do
  fname=$(basename "$script")
  copy_if_not_exists "$script" "$TARGET_DIR/scripts/$fname"
done
copy_if_not_exists "$SCRIPT_DIR/scripts/__init__.py" "$TARGET_DIR/scripts/__init__.py"

for hook in "$SCRIPT_DIR/.claude/hooks/"*.sh; do
  fname=$(basename "$hook")
  copy_if_not_exists "$hook" "$TARGET_DIR/.claude/hooks/$fname"
done

for agent in "$SCRIPT_DIR/.claude/agents/"*.md; do
  fname=$(basename "$agent")
  copy_if_not_exists "$agent" "$TARGET_DIR/.claude/agents/$fname"
done

for rule in "$SCRIPT_DIR/.claude/rules/"*.md; do
  fname=$(basename "$rule")
  copy_if_not_exists "$rule" "$TARGET_DIR/.claude/rules/$fname"
done

for cmd in "$SCRIPT_DIR/.claude/commands/"*.md; do
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

copy_if_not_exists "$SCRIPT_DIR/.nexus/tasks/README.md" "$TARGET_DIR/.nexus/tasks/README.md"
copy_if_not_exists "$SCRIPT_DIR/.nexus/memory/today.md" "$TARGET_DIR/.nexus/memory/today.md"
copy_if_not_exists "$SCRIPT_DIR/.nexus/memory/active-tasks.json" "$TARGET_DIR/.nexus/memory/active-tasks.json"
copy_if_not_exists "$SCRIPT_DIR/.nexus/memory/blockers.md" "$TARGET_DIR/.nexus/memory/blockers.md"
copy_if_not_exists "$SCRIPT_DIR/.nexus/memory/handoff.md" "$TARGET_DIR/.nexus/memory/handoff.md"

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
