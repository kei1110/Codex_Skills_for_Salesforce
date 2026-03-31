# 2GP Managed Monorepo Overlay

Salesforce の Managed 2GP を monorepo で扱うときの前提差分。

Codex が最初に使う正本は `overlay.yaml` を resolver で解決した JSON。これは背景説明と補足メモ用。

## 想定する構成

- 1 リポジトリに複数パッケージを持つ
- `sf` CLI を使う
- Scratch Org で検証する
- パッケージに含められないメタデータを別ディレクトリで扱う

## よくある差分ポイント

### パッケージ分割

- `force-app/<package-name>/main/default/` のように複数 package dir を持つ
- cross-namespace 直接参照を避ける
- 共通化より独立性を優先する箇所がある

### 2GP 制約

- Profile は通常パッケージに含めない
- Approval Process は 2GP に含められない
- Sharing Rules など一部メタデータは扱いに制約がある
- InstallHandler / UninstallHandler は Scratch Org と 2GP 実体で差が出ることがある

### デプロイ / 検証

- package dir 単位デプロイ
- `unpackaged-metadata/` の別デプロイ
- API バージョン整合チェック
- Permission Set / Profile / Custom Permission の整合確認

### テスト / レビュー

- Apex / LWC / E2E を分けて見る
- ガバナ制限、CRUD/FLS、sharing、Custom Permission を重点確認する

## core skill への当て方

- `salesforce-review`
  package dir が複数ある前提で source を拾う
- `salesforce-deploy-check`
  package 本体と `unpackaged-metadata` の両方を見る
- `salesforce-seed-data`
  package ごとに seed を分けるか確認する
- `salesforce-setup-org`
  Scratch Org で必要な追加初期化を repo overlay で具体化する

## manifest 運用

- `paths` で共通の source path パターンを定義する
- repo 固有の command や docs は repo overlay 側で上書きする
- `notes` は 2GP 制約や review 時の注意点だけを短く持つ
