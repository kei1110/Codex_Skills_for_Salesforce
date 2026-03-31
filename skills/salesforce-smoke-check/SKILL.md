---
name: salesforce-smoke-check
description: Run or define post-deploy and post-seed smoke checks for Salesforce repos. Use this for smoke check, deploy verification, seed verification, representative user-path validation, and minimum go-live confirmation.
metadata:
  short-description: Run Salesforce smoke checks
---

# Salesforce Smoke Check

deploy / seed 後の最低限の確認を標準化する。

## 使う場面

- deploy 後に最低限の動作確認をしたい
- seed 後に代表ユーザー導線を確認したい
- release 前後の smoke 観点を整理したい

## 最初に確認する入力

- resolver が使えるなら解決済み JSON の `quality_gates.smoke_tests`、`org_bootstrap.manual_steps`
- 対象 org

## 最初に読むもの

- resolver が使えるなら解決済み JSON の `quality_gates.smoke_tests`
- `references/smoke-checklist.md`
- `references/unpackaged-post-deploy-checklist.md`
- `references/approval-configuration-checklist.md`

## 手順

1. smoke 対象のユーザー導線と機能導線を決める。
2. `quality_gates.static_analysis` の未解決 `Critical` が残っていれば smoke の前提不足として扱う。
3. `quality_gates.smoke_tests` があればそれを基準にする。
4. `references/unpackaged-post-deploy-checklist.md` を使って unpackaged metadata 由来の activation、割当、手動作業が完了しているか確認する。
5. `references/approval-configuration-checklist.md` を使って通知、承認経路、承認対象画面の導線を確認する。
6. 画面導線、代表 CRUD、権限制御、通知や承認導線を確認する。
7. 手動作業が残っている場合は smoke 完了扱いにしない。

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
- `Missing Evidence` には未確認導線、未実施 smoke、approval 通知未確認、手動作業の残りを書く

## フォールバック

- smoke 定義がなければ最小観点だけ提示し、正式完了扱いにしない
