# Gatcha Repo Overlay

`codex-skills` の Salesforce core skills を、Gatcha / Gatcha Work に適用するときの具体例。

Codex が最初に使う正本は `overlay.yaml` を resolver で解決した JSON。これは補足説明と運用メモ用。

## リポジトリ概要

- リポジトリ名: `Gatcha`
- ドメイン: 勤怠管理 + 工数管理
- パッケージ構成: `gatcha` / `gatchawork` の 2 パッケージ
- 利用する workflow overlay: `../../workflows/2gp-managed-monorepo/overlay.yaml`

## ソースパス

- Apex
  - `force-app/gatcha/main/default/classes`
  - `force-app/gatchawork/main/default/classes`
- LWC
  - `force-app/gatcha/main/default/lwc`
  - `force-app/gatchawork/main/default/lwc`
- Trigger
  - `force-app/gatcha/main/default/triggers`
  - `force-app/gatchawork/main/default/triggers`
- Permission Sets
  - `force-app/gatcha/main/default/permissionsets`
  - `force-app/gatchawork/main/default/permissionsets`
- unpackaged metadata
  - `unpackaged-metadata/profiles`
  - `unpackaged-metadata/approvalProcesses`

## 仕様 / 設計ドキュメント

- 主要仕様書
  - `docs/SPEC.md`
  - `docs/SPEC_WORK.md`
- 画面設計
  - `docs/SCREENS_WORK.md`
- ロードマップ
  - `docs/ROADMAP.md`
  - `docs/WORK_ROADMAP.md`
- 技術設計
  - `docs/technical-setup.md`

## Permission / Security 具体例

- 一般利用者向け Permission Set
  - `AttendanceUser.permissionset-meta.xml`
  - `WorkforceUser.permissionset-meta.xml`
- 管理者向け Permission Set
  - `AttendanceManager.permissionset-meta.xml`
- 高度権限向け Permission Set
  - `AttendanceAdmin.permissionset-meta.xml`
  - `ResourcePlanner.permissionset-meta.xml` があれば追加対象
- 主要 Custom Permission
  - `Workforce_Approver`
  - `Workforce_ResourcePlanner`

## セットアップ / シード

- org 初期セットアップ
  - `./scripts/setup-scratch-org.sh my-org`
- デプロイ手順
  - `sf project deploy start --source-dir force-app/gatcha --target-org my-org`
  - `sf project deploy start --source-dir force-app/gatchawork --target-org my-org`
  - `sf project deploy start --source-dir unpackaged-metadata/profiles --target-org my-org --ignore-conflicts`
- seed データ
  - `sf apex run --file scripts/seed-demo-data.apex --target-org my-org`
  - `sf apex run --file scripts/seed-work-demo-data.apex --target-org my-org`
- 手動作業
  - FlexiPage の Activate
  - 承認プロセスの手動設定

## テスト / 検証

- Apex テスト
  - `sf apex run test --test-level RunLocalTests --code-coverage --result-format human --wait 30 --target-org my-org`
- LWC Jest
  - `npm test`
- E2E
  - `npm run test:e2e`
- 軽量確認
  - `./scripts/api-version-check.sh`

## skill への当て込みメモ

- `salesforce-review`
  - classes / lwc / triggers / permissionsets / approvalProcesses を重点確認
- `salesforce-spec-check`
  - `docs/SPEC.md`, `docs/SPEC_WORK.md`, `docs/SCREENS_WORK.md`, `docs/ROADMAP.md`, `docs/WORK_ROADMAP.md`
- `salesforce-perm-check`
  - `AttendanceUser`, `AttendanceManager`, `AttendanceAdmin`, `WorkforceUser`, `ResourcePlanner`
- `salesforce-seed-data` / `salesforce-setup-org`
  - 上記 setup / seed コマンドを使う

## manifest 更新ルール

- パス、docs、Permission Set、コマンドの変更があれば先に `overlay.yaml` を更新する
- 更新後は `python3 scripts/validate-overlays.py --overlay overlays/repos/gatcha/overlay.yaml` で確認する
- README には背景説明や注意点だけを残す
