---
name: salesforce-flow-review
description: Review Salesforce Flow and declarative automation changes. Use this for flow review, Validation Rule review, Approval Process review, Record Type review, and metadata-driven business logic review in Salesforce repos.
metadata:
  short-description: Review Flow and declarative automation
---

# Salesforce Flow Review

Flow と宣言的 metadata 変更を重点レビューする。

## 使う場面

- Flow、Validation Rule、Approval Process の変更をレビューしたい
- Apex ではなく metadata 側の業務ロジック差分を見たい
- `salesforce-review` の補完として宣言的 automation を深掘りしたい

## 最初に確認する入力

- resolver が使えるなら解決済み JSON の `source` と `docs`
- 対象 metadata の変更範囲
- 差分中心のレビューなら `prune-context.py` で絞った `selected.metadata` と `selected.docs`

## 最初に読むもの

- resolver が使えるなら解決済み JSON の `source` と `docs`
- 差分中心なら `python3 scripts/prune-context.py --repo <repo-slug> --changed-file <metadata-path> --pretty`
- `references/declarative-automation-checklist.md`
- `references/flow-risk-checklist.md`
- `references/approval-configuration-checklist.md`

## 手順

1. Flow、Validation Rule、Approval Process、Record Type の変更を特定する。
2. 差分レビューでは `prune-context.py` を使い、関連 metadata と docs を先に絞る。
3. metadata が担う業務ロジックと仕様を照合する。
4. `references/flow-risk-checklist.md` に沿って entry 条件競合、before-save / after-save の責務混在、再入・ループ、順序依存を確認する。
5. `references/approval-configuration-checklist.md` に沿って Approval Process の手動設定、通知、承認者経路、UI 到達性を確認する。
6. Apex との責務重複や順序依存を確認する。
7. 権限、エラー導線、運用性の観点を確認する。

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
- `Critical` には Flow 条件競合、権限制御欠落、運用事故候補を置く
- `Missing Evidence` には activation 条件、承認者経路、関連 Layout / Record Type / Permission Set の不足証跡を書く

## フォールバック

- resolver も overlay も使えなければ Flow / Validation / Approval の配置場所を探索する
