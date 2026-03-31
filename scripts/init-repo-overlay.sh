#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

usage() {
  cat <<'EOF'
usage: ./scripts/init-repo-overlay.sh <repo-slug> <display-name> [workflow-overlay-path]

example:
  ./scripts/init-repo-overlay.sh my-repo "My Repo" overlays/workflows/2gp-managed-monorepo/overlay.yaml
EOF
}

if [[ $# -lt 2 || $# -gt 3 ]]; then
  usage
  exit 1
fi

REPO_SLUG="$1"
DISPLAY_NAME="$2"
WORKFLOW_PATH="${3:-}"
TARGET_DIR="$ROOT_DIR/overlays/repos/$REPO_SLUG"

if [[ ! "$REPO_SLUG" =~ ^[a-z0-9][a-z0-9-]*$ ]]; then
  echo "[error] repo-slug は lowercase letters, digits, hyphen のみ使えます" >&2
  exit 1
fi

if [[ -e "$TARGET_DIR" ]]; then
  echo "[error] $TARGET_DIR already exists" >&2
  exit 1
fi

mkdir -p "$TARGET_DIR"
if [[ -n "$WORKFLOW_PATH" && ! -f "$ROOT_DIR/$WORKFLOW_PATH" ]]; then
  echo "[error] workflow overlay not found: $WORKFLOW_PATH" >&2
  exit 1
fi

cat > "$TARGET_DIR/overlay.yaml" <<EOF
schema_version: 3
kind: repo
name: $DISPLAY_NAME
inherits: $WORKFLOW_PATH
source:
  apex: []
  lwc: []
  triggers: []
  flows: []
  objects: []
  permissionsets: []
  permissionsetgroups: []
  profiles: []
  layouts: []
  recordtypes: []
  approval_processes: []
  unpackaged: []
docs:
  specs: []
  screens: []
  roadmap: []
  technical: []
  runbooks: []
packaging:
  package_dirs: []
  package_aliases: []
  namespace:
  dependencies: []
  unpackaged_post_deploy: []
  install_validation: []
  upgrade_validation: []
security:
  permission_sets:
    user: []
    admin: []
    elevated: []
  permission_set_groups: []
  muting_permission_sets: []
  custom_permissions: []
  licenses: []
  record_type_assignments: []
  ui_visibility: []
org_bootstrap:
  scratch_def:
  default_alias:
  dev_hub_alias:
  feature_setup: []
  settings_setup: []
  permission_assignments: []
  user_setup: []
  seed: []
  manual_steps: []
quality_gates:
  api_version_check:
  lint: []
  unit_tests: []
  integration_tests: []
  smoke_tests: []
  blocking_rules: []
  static_analysis:
    commands: []
    thresholds:
      critical_max: 0
      warning_max:
      advisory_max:
    blocking_rules: []
context_pruning:
  roots:
    source:
      - source.apex
      - source.lwc
      - source.triggers
      - source.flows
      - source.objects
    docs:
      - docs.specs
      - docs.screens
      - docs.technical
  dependency_hints:
    apex_tests:
      - "*Test.cls"
    lwc_tests:
      - "__tests__"
notes: []
EOF

cat > "$TARGET_DIR/README.md" <<EOF
# Repo Overlay Template

core skill を特定リポジトリへ当てるための TA 向け雛形。

Codex が最初に使う正本は \`overlay.yaml\` を resolver で解決した JSON。これは人向け補足と記入メモ用。

## リポジトリ概要

- リポジトリ名: \`$DISPLAY_NAME\`
- ドメイン:
- パッケージ構成:
- 利用する workflow overlay: \`$WORKFLOW_PATH\`

## source

- Apex:
- LWC:
- Trigger:
- Flow:
- Object:
- Permission Set:
- Permission Set Group:
- Profile:
- unpackaged metadata:

## docs

- 主要仕様書:
- 画面設計:
- ロードマップ:
- 技術設計:
- runbook:

## packaging / security / org / quality

- package dirs:
- dependencies:
- 主要 Permission Set:
- PSG / muting:
- license:
- Record Type assignment:
- scratch org:
- permission assignment:
- seed:
- static analysis:
- context pruning:

## 作成手順

1. 先に \`overlay.yaml\` を埋める
2. 必要なら \`python3 scripts/discover-overlay.py --workspace-root <repo-path> --name "$DISPLAY_NAME" --pretty\` で初期候補を作る
3. \`python3 scripts/validate-overlays.py --overlay overlays/repos/$REPO_SLUG/overlay.yaml\` で確認する
4. 必要なら \`quality_gates.static_analysis\` と \`context_pruning\` を埋める
5. 必要な背景説明だけこの README に足す
6. \`./scripts/validate-skills.sh\` で全体確認する
EOF

echo "[ok] initialized $TARGET_DIR"
echo "next:"
echo "  1. overlay.yaml を埋める"
echo "  2. 必要なら python3 ./scripts/discover-overlay.py --workspace-root <repo-path> --name \"$DISPLAY_NAME\" --pretty で候補を確認する"
echo "  3. python3 ./scripts/validate-overlays.py --overlay overlays/repos/$REPO_SLUG/overlay.yaml を実行する"
echo "  4. README.md に補足を足す"
echo "  5. ./scripts/validate-skills.sh を実行する"
