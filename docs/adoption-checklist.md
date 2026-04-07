# Adoption Checklist

## 前提

- Git 管理されている
- `python3` が使える
- `CODEX_HOME` の配置先が決まっている

## repo 側

- `sfdx-project.json` がある、または package dir を把握している
- `permissionsets/` と `permissionsetgroups/` の配置を把握している
- `docs/` や仕様書の置き場所を把握している
- CI や local command の lint / test 導線を把握している

## kit 側

- `./scripts/bootstrap-kit.sh` が通る
- `python3 scripts/doctor.py --json` で `FAIL` がない
- `python3 scripts/validate-overlays.py` が通る
- `./scripts/validate-skills.sh` が通る

## 最初に使う skill

- 最小導入: `salesforce-review`, `salesforce-release-check`, `salesforce-quick-test`, `salesforce-perm-check`
- Flow-heavy repo: `salesforce-flow-review`, `salesforce-smoke-check` も追加
- packaging 重視: `salesforce-package-release`, `salesforce-package-topology-check` も追加
