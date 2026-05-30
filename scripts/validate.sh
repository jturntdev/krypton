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
  "VERSION"
  "README.md"
  "LICENSE"
  ".codex-plugin/plugin.json"
  ".claude-plugin/plugin.json"
  "skills/krypton-planning/SKILL.md"
  "skills/krypton-planning/agents/openai.yaml"
  "skills/krypton-planning/plan-reviewer-prompt.md"
  "skills/krypton-execution/SKILL.md"
  "skills/krypton-execution/agents/openai.yaml"
  "skills/krypton-execution/post-plan-reviewer-prompt.md"
  "skills/krypton-execution/reviewer-prompt.md"
  "skills/krypton-execution/maintainer-prompt.md"
  "docs/required-roles.md"
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

python3 - "$ROOT" <<'PY'
import json
import pathlib
import sys

root = pathlib.Path(sys.argv[1])
version = (root / "VERSION").read_text().strip()
checks = {
    ".codex-plugin/plugin.json": json.loads((root / ".codex-plugin/plugin.json").read_text())["version"],
    ".claude-plugin/plugin.json": json.loads((root / ".claude-plugin/plugin.json").read_text())["version"],
    ".claude-plugin/marketplace.json": json.loads((root / ".claude-plugin/marketplace.json").read_text())["plugins"][0]["version"],
}

for path, value in checks.items():
    if value != version:
        raise SystemExit(f"version mismatch: {path} has {value}, VERSION has {version}")
PY

if command -v claude >/dev/null 2>&1; then
  claude plugin validate --strict "$ROOT/.claude-plugin/plugin.json" >/dev/null
  claude plugin validate --strict "$ROOT/.claude-plugin/marketplace.json" >/dev/null
fi

echo "validation passed"
