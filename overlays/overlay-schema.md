# Overlay Schema v3

`overlay.yaml` は Codex が repo 固有情報を TA 観点で正規化利用するための機械可読 manifest。

## Top-level keys

- `schema_version`
  - 現行は `3`
- `kind`
  - `repo` または `workflow`
- `name`
  - 表示名
- `inherits`
  - repo root 基準の相対パス
- `source`
- `docs`
- `packaging`
- `security`
- `org_bootstrap`
- `quality_gates`
- `context_pruning`
- `notes`

## quality_gates.static_analysis

- `commands`
  - `name`, `run`, `parser`
- `thresholds`
  - `critical_max`, `warning_max`, `advisory_max`
- `blocking_rules`

初期実装で使える `parser` は次の 2 つ。

- `pmd-json`
- `sfdx-scanner-json`

## context_pruning

- `roots.source`
  - 差分時に source 候補として使う key 名
- `roots.docs`
  - docs 候補として使う key 名
- `dependency_hints.apex_tests`
- `dependency_hints.lwc_tests`

## Merge Rules

- `inherits` は repo root 基準の相対パス
- map は再帰マージする
- list は親 -> 子の順で連結し、重複は初出優先で除去する
- scalar は子が非空なら上書きし、空文字または null は親を継承する
- `schema_version` は子の値を優先し、現行は `3` のみ許可する
