#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STATUS=0

fail() {
  echo "[error] $1" >&2
  STATUS=1
}

check_frontmatter() {
  local file="$1"
  local first
  local closing
  first="$(sed -n '1p' "$file")"
  if [[ "$first" != "---" ]]; then
    fail "$file: frontmatter opening '---' がありません"
    return
  fi

  closing="$(grep -n '^---$' "$file" | sed -n '2p' | cut -d: -f1)"
  if [[ -z "$closing" ]]; then
    fail "$file: frontmatter closing '---' がありません"
  fi

  if ! grep -q '^name:' "$file"; then
    fail "$file: frontmatter に name がありません"
  fi

  if ! grep -q '^description:' "$file"; then
    fail "$file: frontmatter に description がありません"
  fi
}

check_agent_yaml() {
  local file="$1"
  if ! grep -q '^interface:' "$file"; then
    fail "$file: interface セクションがありません"
  fi
  if ! grep -q 'display_name:' "$file"; then
    fail "$file: display_name がありません"
  fi
  if ! grep -q 'short_description:' "$file"; then
    fail "$file: short_description がありません"
  fi
  if ! grep -q 'default_prompt:' "$file"; then
    fail "$file: default_prompt がありません"
  fi
}

check_skill_refs() {
  local skill_dir="$1"
  local skill_md="$skill_dir/SKILL.md"
  while IFS= read -r ref; do
    [[ -n "$ref" ]] || continue
    if [[ ! -e "$skill_dir/$ref" && ! -e "$ROOT_DIR/$ref" ]]; then
      fail "$skill_md: 参照先 $ref が存在しません"
    fi
  done < <(grep -oE '(references|scripts|assets)/[^` )]+' "$skill_md" | sort -u || true)
}

check_required_section() {
  local file="$1"
  local pattern="$2"
  local label="$3"
  if ! grep -q "$pattern" "$file"; then
    fail "$file: 必須セクション $label がありません"
  fi
}

check_critical_skill_contract() {
  local file="$1"
  check_required_section "$file" '^## 最初に読むもの' '最初に読むもの'
  check_required_section "$file" '^## 手順' '手順'
  check_required_section "$file" '^## 出力' '出力'
}

check_output_template() {
  local file="$1"
  for label in '## Summary' '## Decision' '## Critical' '## Warning' '## Advisory' '## Missing Evidence' '## Next Actions'; do
    if ! grep -q "$label" "$file"; then
      fail "$file: 出力テンプレート $label がありません"
    fi
  done
}

check_contains_text() {
  local file="$1"
  local pattern="$2"
  local label="$3"
  if ! grep -q "$pattern" "$file"; then
    fail "$file: 必須キーワード $label がありません"
  fi
}

for skill_dir in "$ROOT_DIR"/skills/*; do
  [[ -d "$skill_dir" ]] || continue

  if [[ ! -f "$skill_dir/SKILL.md" ]]; then
    fail "$skill_dir: SKILL.md がありません"
    continue
  fi

  if [[ ! -f "$skill_dir/agents/openai.yaml" ]]; then
    fail "$skill_dir: agents/openai.yaml がありません"
  fi

  check_frontmatter "$skill_dir/SKILL.md"
  check_agent_yaml "$skill_dir/agents/openai.yaml"
  check_skill_refs "$skill_dir"
done

for critical_skill in \
  "$ROOT_DIR/skills/salesforce-review/SKILL.md" \
  "$ROOT_DIR/skills/salesforce-release-check/SKILL.md" \
  "$ROOT_DIR/skills/salesforce-perm-check/SKILL.md" \
  "$ROOT_DIR/skills/salesforce-spec-check/SKILL.md" \
  "$ROOT_DIR/skills/salesforce-setup-org/SKILL.md" \
  "$ROOT_DIR/skills/salesforce-seed-data/SKILL.md"; do
  check_critical_skill_contract "$critical_skill"
done

for skill_name in salesforce-review salesforce-spec-check salesforce-deploy-check salesforce-release-check salesforce-quick-test salesforce-seed-data salesforce-setup-org salesforce-phase-summary salesforce-gen-test salesforce-new-lwc salesforce-new-trigger salesforce-perm-check salesforce-package-release salesforce-flow-review salesforce-smoke-check salesforce-package-topology-check; do
  if [[ ! -d "$ROOT_DIR/skills/$skill_name" ]]; then
    fail "skills/$skill_name: README に載っているが directory がありません"
  fi
done

check_contains_text "$ROOT_DIR/skills/salesforce-review/SKILL.md" 'prune-context.py' 'prune-context.py'
check_contains_text "$ROOT_DIR/skills/salesforce-review/SKILL.md" 'context-pruning.md' 'context-pruning.md'
check_contains_text "$ROOT_DIR/skills/salesforce-release-check/SKILL.md" 'static_analysis' 'quality_gates.static_analysis'
check_contains_text "$ROOT_DIR/skills/salesforce-release-check/SKILL.md" 'static-analysis-gate.md' 'static-analysis-gate.md'
check_contains_text "$ROOT_DIR/skills/salesforce-release-check/SKILL.md" 'unpackaged-post-deploy-checklist.md' 'unpackaged-post-deploy-checklist.md'
check_contains_text "$ROOT_DIR/skills/salesforce-release-check/SKILL.md" 'approval-configuration-checklist.md' 'approval-configuration-checklist.md'
check_contains_text "$ROOT_DIR/skills/salesforce-quick-test/SKILL.md" 'prune-context.py' 'prune-context.py'
check_contains_text "$ROOT_DIR/skills/salesforce-quick-test/SKILL.md" 'context-pruning.md' 'context-pruning.md'
check_contains_text "$ROOT_DIR/skills/salesforce-flow-review/SKILL.md" 'prune-context.py' 'prune-context.py'
check_contains_text "$ROOT_DIR/skills/salesforce-flow-review/SKILL.md" 'flow-risk-checklist.md' 'flow-risk-checklist.md'
check_contains_text "$ROOT_DIR/skills/salesforce-flow-review/SKILL.md" 'approval-configuration-checklist.md' 'approval-configuration-checklist.md'
check_contains_text "$ROOT_DIR/skills/salesforce-package-release/SKILL.md" 'static_analysis' 'quality_gates.static_analysis'
check_contains_text "$ROOT_DIR/skills/salesforce-smoke-check/SKILL.md" 'static_analysis' 'quality_gates.static_analysis'
check_contains_text "$ROOT_DIR/skills/salesforce-smoke-check/SKILL.md" 'unpackaged-post-deploy-checklist.md' 'unpackaged-post-deploy-checklist.md'
check_contains_text "$ROOT_DIR/skills/salesforce-smoke-check/SKILL.md" 'approval-configuration-checklist.md' 'approval-configuration-checklist.md'

for templated_skill in \
  "$ROOT_DIR/skills/salesforce-review/SKILL.md" \
  "$ROOT_DIR/skills/salesforce-release-check/SKILL.md" \
  "$ROOT_DIR/skills/salesforce-perm-check/SKILL.md" \
  "$ROOT_DIR/skills/salesforce-spec-check/SKILL.md" \
  "$ROOT_DIR/skills/salesforce-flow-review/SKILL.md" \
  "$ROOT_DIR/skills/salesforce-smoke-check/SKILL.md"; do
  check_output_template "$templated_skill"
done

while IFS= read -r readme; do
  dir="$(dirname "$readme")"
  if [[ ! -f "$dir/overlay.yaml" ]]; then
    fail "$dir: README.md はあるが overlay.yaml がありません"
  fi
done < <(find "$ROOT_DIR/overlays" -name README.md | sort)

if ! python3 "$ROOT_DIR/scripts/validate-overlays.py"; then
  STATUS=1
fi

if [[ "$STATUS" -eq 0 ]]; then
  echo "[ok] skill 構成は整合しています"
fi

exit "$STATUS"
