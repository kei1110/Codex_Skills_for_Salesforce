# Repo Overlay Template

core skill を特定リポジトリへ当てるための雛形。

Codex が最初に使う正本は `overlay.yaml` を resolver で解決した JSON。これは人向け補足と記入メモ用。

## リポジトリ概要

- リポジトリ名:
- ドメイン:
- パッケージ構成:
- 利用する workflow overlay:

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

## 仕様 / 設計ドキュメント

- 主要仕様書:
- 画面設計:
- ロードマップ:
- 技術設計:

## packaging / security / org

- package dirs:
- dependencies:
- 一般利用者向け Permission Set:
- 管理者向け Permission Set:
- 高度権限向け Permission Set:
- PSG / muting:
- 主要 Custom Permission:
- license:
- Record Type assignment:
- scratch org:
- permission assignment:
- seed:

## セットアップ / シード

- org 初期セットアップ:
- デプロイ手順:
- seed データ:
- 手動作業:

## テスト / 検証

- Apex テストコマンド:
- LWC Jest:
- E2E:
- 軽量確認コマンド:

## skill への当て込みメモ

- `salesforce-review` で見る主な場所:
- `salesforce-spec-check` で使う仕様書:
- `salesforce-perm-check` で対象にする Permission Set:
- `salesforce-seed-data` / `salesforce-setup-org` の具体コマンド:

## 作成手順

1. 可能なら `./scripts/init-repo-overlay.sh <repo-slug> <display-name> [workflow-overlay-path]` で作る
2. 先に `overlay.yaml` を埋める
3. `python3 scripts/validate-overlays.py --overlay overlays/repos/<repo-slug>/overlay.yaml` で manifest を確認する
4. 必要な背景説明だけこの README に足す
5. `./scripts/validate-skills.sh` で構成を確認する
