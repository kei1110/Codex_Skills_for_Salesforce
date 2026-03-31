---
name: salesforce-release-check
description: Run the TA-grade release gate for a Salesforce repo. Use this for release check, リリース前確認, packaging gate, lint + unit + integration test validation, spec alignment, permission readiness, and install/upgrade smoke validation.
metadata:
  short-description: Run TA release gate
---

# Salesforce Release Check

リリース前の TA 向け総合品質ゲート。

## 使う場面

- package / release / deploy 前に go/no-go 判定を出したい
- packaging、権限、metadata、テスト、仕様整合を一括で見たい
- `salesforce-quick-test` では不十分な変更量になった

## 最初に確認する入力

- 対象 org alias
- resolver が使えるなら解決済み JSON の `packaging`、`quality_gates`、`security`
- package dir ごとの install / upgrade 確認要否

## 最初に読むもの

- resolver が使えるなら解決済み JSON の `packaging`、`quality_gates`、`security`
- `references/release-checklist.md`
- `references/packaging-architect.md`
- `references/static-analysis-gate.md`
- `references/unpackaged-post-deploy-checklist.md`
- `references/approval-configuration-checklist.md`

## 手順

1. resolver が使えるなら `quality_gates` と `packaging` を確認する。
2. `quality_gates.api_version_check` を確認する。
3. `quality_gates.static_analysis` が定義されていれば、PMD / SFDX Scanner の結果を `parse-static-analysis.py` で正規化し、`evaluate-quality-gates.py` で閾値判定する。
4. `quality_gates.lint`、`quality_gates.unit_tests`、`quality_gates.integration_tests` を順に確認する。
5. `references/packaging-architect.md` に沿って package topology、dependency、install / upgrade validation を確認する。
6. `references/unpackaged-post-deploy-checklist.md` に沿って `source.unpackaged` の deploy 順序、package 外 metadata、手動作業、後続 smoke を確認する。
7. `references/approval-configuration-checklist.md` に沿って `source.approval_processes`、関連通知、承認者経路、手動 activation を確認する。
8. `security` と `source.unpackaged` / `source.approval_processes` を見て permission / unpackaged metadata の整合を確認する。
9. `quality_gates.smoke_tests` があれば release 前 smoke として確認する。
10. `quality_gates.blocking_rules` と `quality_gates.static_analysis.blocking_rules` を満たしているかで `PASS / FAIL / CONDITIONAL` を判定する。

## 出力

次のテンプレートで返す。

```md
## Summary
## Decision
## Critical
## Warning
## Advisory
## Missing Evidence
## Next Actions
```

- `Decision` は `PASS / FAIL / CONDITIONAL`
- `Summary` には quality gate、static analysis、packaging の総評を書く
- `Missing Evidence` には install / upgrade / smoke / permission / unpackaged post deploy / approval activation の不足証跡を書く

## フォールバック

- resolver も overlay も使えなければ repo 標準コマンドを探索する
- packaging / install / upgrade 情報がなければ `CONDITIONAL` 以上にはしない
