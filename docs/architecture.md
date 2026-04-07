# Architecture

## 3 層モデル

- `skills/`
  - 企業標準の core skill
- `overlays/workflows/`
  - 開発様式ごとの差分
- `overlays/repos/`
  - repo 固有差分

この 3 層で、共通知識と repo 固有事情を分離する。

## 正本

- repo 固有情報の正本は `overlay.yaml`
- Codex は `scripts/resolve-overlay.py` で解決済み JSON を使う
- 人向け補足は `README.md`

## 主要補助スクリプト

- `scripts/resolve-overlay.py`
  - overlay を解決して正規化 JSON を返す
- `scripts/validate-overlays.py`
  - schema と継承整合を検証する
- `scripts/parse-static-analysis.py`
  - PMD / SFDX Scanner を正規化する
- `scripts/evaluate-quality-gates.py`
  - static analysis を理由付き quality gate に変換する
- `scripts/prune-context.py`
  - changed files と軽量依存解析で context を絞る
- `scripts/discover-overlay.py`
  - 既存 repo から overlay 候補を推定する
- `scripts/doctor.py`
  - kit 導入状態を診断する

## schema v3 の要点

- `schema_version: 3` は必須
- `quality_gates.static_analysis`
  - command / parser / threshold / blocking rule を持つ
- `context_pruning`
  - source / docs / dependency hints を持つ
- list field は patch syntax を使える
  - `replace`
  - `values`
  - `remove`
