---
name: salesforce-review
description: Review Salesforce Apex, LWC, packaging, and metadata changes in a Salesforce repo. Use this for TA review, レビュー, governor-limit review, security review, packaging boundary review, LDV/selectivity review, and missing test detection.
metadata:
  short-description: Review Salesforce changes
---

# Salesforce Review

Salesforce 変更のレビューを TA 観点で行う。

## 使う場面

- 直近の `git diff` をレビューしたい
- 実装、権限、metadata、packaging、運用リスクをまとめて見たい
- 実装が SPEC とずれていないか確認したい

## 最初に確認する入力

- 対象変更範囲
- resolver が使えるなら解決済み JSON の `source`、`docs`、`security`、`packaging`
- 差分中心のレビューなら `prune-context.py` で絞った `selected.source`、`selected.docs`、`selected.tests`

## 最初に読むもの

- resolver が使えるなら `python3 ${CODEX_HOME:-$HOME/.codex}/salesforce-kit/scripts/resolve-overlay.py --repo <repo-slug> --pretty`
- toolkit がない場合は repo 内の `python3 scripts/resolve-overlay.py --overlay <overlay-path> --pretty`
- 差分中心なら `python3 scripts/prune-context.py --repo <repo-slug> --changed-file <path> --pretty`
- `references/apex-reviewer.md`
- `references/lwc-reviewer.md`
- `references/security-reviewer.md`
- `references/soql-budget-analyzer.md`
- `references/bulk-scenario-tester.md`
- `references/test-coverage-analyzer.md`
- `references/change-sync-checklist.md`
- `references/spec-compliance-reviewer.md`
- `references/operability-runbook.md`
- `references/context-pruning.md`

## 手順

1. 対象変更を特定する。
2. resolver が使えるなら `source`、`docs`、`security`、`packaging` を先に固定する。
3. 差分レビューでは `prune-context.py` を使い、読む source / docs / tests を絞る。
4. static analysis の正規化結果があるなら AI 所見とは分けて先に読む。
5. Apex / Trigger / LWC / metadata / packaging に分ける。
6. 変更種別ごとに Permission Set / Profile / FlexiPage / Tab / App / test / docs などの連動更新漏れを確認する。
7. 実装品質、セキュリティ、SPEC 整合、運用性を順に見る。
8. LDV / selectivity / mixed DML / async chain / lock contention / package 境界の観点を追加で見る。
9. 指摘を `Critical / Warning / Advisory` で統合する。

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

- `Decision` は通常 `CONDITIONAL`
- `Critical` は直すべき不具合、権限漏れ、ガバナ破綻、SPEC 逸脱、運用事故候補
- `Warning` は設計や将来運用での高リスク項目
- `Advisory` は改善案、追加テスト候補、runbook への追記候補

## フォールバック

- resolver も overlay も使えなければ repo から source / docs / security を探索する
- 仕様書や packaging 情報がなければ評価不能範囲を明記する
