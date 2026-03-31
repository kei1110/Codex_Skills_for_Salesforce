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

## 手順

1. smoke 対象のユーザー導線と機能導線を決める。
2. `quality_gates.static_analysis` の未解決 `Critical` が残っていれば smoke の前提不足として扱う。
3. `quality_gates.smoke_tests` があればそれを基準にする。
4. 画面導線、代表 CRUD、権限制御、通知や承認導線を確認する。
5. 手動作業が残っている場合は smoke 完了扱いにしない。

## 出力

- `PASS / FAIL / CONDITIONAL`
- 実施した smoke 項目
- 未確認の導線

## フォールバック

- smoke 定義がなければ最小観点だけ提示し、正式完了扱いにしない
