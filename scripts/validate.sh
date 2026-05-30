#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

validate_skill() {
  local skill_dir="$1"
  local skill_name
  local frontmatter_name
  local description

  skill_name="$(basename "$skill_dir")"

  if [[ ! -f "$skill_dir/SKILL.md" ]]; then
    echo "missing SKILL.md: $skill_dir" >&2
    exit 1
  fi

  if [[ "$(sed -n '1p' "$skill_dir/SKILL.md")" != "---" ]]; then
    echo "missing YAML frontmatter start: $skill_dir/SKILL.md" >&2
    exit 1
  fi

  frontmatter_name="$(sed -n '2,20p' "$skill_dir/SKILL.md" | sed -n 's/^name: *//p' | tr -d '"')"
  description="$(sed -n '2,20p' "$skill_dir/SKILL.md" | sed -n 's/^description: *//p')"

  if [[ "$frontmatter_name" != "$skill_name" ]]; then
    echo "skill name mismatch: expected $skill_name, got $frontmatter_name" >&2
    exit 1
  fi

  if [[ ! "$frontmatter_name" =~ ^[a-z0-9-]+$ ]]; then
    echo "invalid skill name: $frontmatter_name" >&2
    exit 1
  fi

  if [[ -z "$description" ]]; then
    echo "missing skill description: $skill_dir/SKILL.md" >&2
    exit 1
  fi

  if [[ ! -f "$skill_dir/agents/openai.yaml" ]]; then
    echo "missing agents/openai.yaml: $skill_dir" >&2
    exit 1
  fi
}

required_files=(
  "README.md"
  "LICENSE"
  ".codex-plugin/plugin.json"
  ".claude-plugin/plugin.json"
  "skills/krypton-planning/SKILL.md"
  "skills/krypton-planning/agents/openai.yaml"
  "skills/krypton-execution/SKILL.md"
  "skills/krypton-execution/agents/openai.yaml"
  "examples/wrong-layer-feature.md"
  "tests/pressure-scenarios/wrong-layer.md"
)

for file in "${required_files[@]}"; do
  if [[ ! -f "$ROOT/$file" ]]; then
    echo "missing required file: $file" >&2
    exit 1
  fi
done

if grep -RInE "TODO|\\[TODO|tradetiros|Tradetir|\\.project-memory|backend/api|frontend/web" "$ROOT" \
  --exclude-dir=.git \
  --exclude=validate.sh; then
  echo "public package contains placeholders or private/project-specific references" >&2
  exit 1
fi

validate_skill "$ROOT/skills/krypton-planning"
validate_skill "$ROOT/skills/krypton-execution"

python3 -m json.tool "$ROOT/.codex-plugin/plugin.json" >/dev/null
python3 -m json.tool "$ROOT/.claude-plugin/plugin.json" >/dev/null

echo "validation passed"
