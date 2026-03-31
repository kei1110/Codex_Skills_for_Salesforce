---
name: salesforce-spec-check
description: Compare Salesforce implementation and metadata against project specification documents. Use this for spec check, 仕様確認, Apex/LWC/Flow/Validation/Approval comparison, and roadmap-versus-implementation review.
metadata:
  short-description: Check implementation against specs
---

# Salesforce Spec Check

仕様書と実装差分を metadata まで含めて確認する。

## 使う場面

- 実装が仕様書や画面設計に沿っているか確認したい
- 新規実装前に既存コードと metadata の到達点を把握したい
- リリース前に仕様逸脱を洗いたい

## 最初に確認する入力

- 対象機能または package
- resolver が使えるなら解決済み JSON の `docs` と `source`

## 最初に読むもの

- resolver が使えるなら解決済み JSON の `docs` と `source`
- `references/spec-checklist.md`
- `references/metadata-coverage.md`

## 手順

1. 対象を決める。
2. resolver が使えるなら `docs` と `source` を先に固定する。
3. `references/spec-checklist.md` と `references/metadata-coverage.md` を使って、Apex / LWC / Flow / Validation / Record Type / Approval の差分を確認する。
4. 差分を `準拠 / 逸脱 / 未実装 / 後続 Phase 予定` に分類する。
5. 評価不能な範囲があれば明記する。

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
- `Critical` には重大な仕様逸脱や release blocker を置く
- `Missing Evidence` には仕様書不足や metadata coverage 不足を書く

## フォールバック

- resolver も overlay も使えなければ repo から specs / screens / roadmap / metadata を探索する
