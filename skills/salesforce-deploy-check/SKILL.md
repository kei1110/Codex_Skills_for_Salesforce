---
name: salesforce-deploy-check
description: Run lightweight deploy-readiness checks for a Salesforce repo before deployment. Use this for deploy readiness, デプロイ前確認, 権限漏れ確認, API バージョン確認, LWC/Apex 参照確認, and metadata consistency checks without running the full test suite.
metadata:
  short-description: Check deploy readiness
---

# Salesforce Deploy Check

テスト実行なしで、デプロイ前の軽量整合チェックを行う。

## 使う場面

- package deploy 前にメタデータ整合だけ先に見たい
- Profile / Permission Set / API バージョンの漏れを潰したい
- `salesforce-release-check` を回す前に軽く赤信号を洗いたい

## 最初に確認する入力

- 対象 repo の source path
- Permission Set / Profile の配置場所
- repo overlay と resolver の有無
- repo 固有の API version check コマンドの有無

## 最初に読むもの

- resolver が使えるなら `python3 ${CODEX_HOME:-$HOME/.codex}/salesforce-kit/scripts/resolve-overlay.py --repo <repo-slug> --pretty`
- toolkit がない場合は repo 内の `python3 scripts/resolve-overlay.py --overlay <overlay-path> --pretty`
- `references/deploy-readiness.md`
- `references/profile-auditor.md`

## 手順

1. resolver が使えるなら解決済み JSON の `commands.api_version_check` と `paths` を先に確認する。
2. repo に API version check コマンドが定義されていれば使う。
3. コマンドがなければ `sfdx-project.json` と主要 `*-meta.xml` の `apiVersion` を手動確認する。
4. `references/deploy-readiness.md` を使って以下を確認する。
   - `classAccesses`
   - `objectPermissions`
   - `fieldPermissions`
   - LWC -> Apex 参照
   - Trigger -> Handler 参照
5. Admin Profile や unpackaged metadata を使う repo では `references/profile-auditor.md` を使って確認する。
6. 結果を `READY / NOT READY` でまとめ、未解決項目を列挙する。

## 出力

- 総合判定 `READY / NOT READY`
- 問題の種別
  - API version
  - Permission / Profile
  - 依存関係
  - デプロイ順序
- 先に直すべき項目

## フォールバック

- resolver も overlay も使えなければ repo から Apex / Trigger / LWC / Permission Set のパスを探索する
- Profile が存在しない repo では Profile 監査を省略し、その旨を明記する
