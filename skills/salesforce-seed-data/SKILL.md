---
name: salesforce-seed-data
description: Seed demo data into a Salesforce org with TA-grade runbook checks. Use this for seed data, デモデータ投入, staged bootstrap, idempotent seed review, and post-seed smoke preparation.
metadata:
  short-description: Seed data runbook
---

# Salesforce Seed Data

Scratch Org に seed データを runbook として投入する。

## 最初に確認する入力

- resolver が使えるなら解決済み JSON の `org_bootstrap.seed`、`quality_gates.smoke_tests`

## 最初に読むもの

- resolver が使えるなら解決済み JSON の `org_bootstrap.seed`
- `references/seed-readiness.md`
- `references/operability-runbook.md`

## 手順

1. package / metadata が deploy 済みか確認する。
2. seed の前提権限と依存データを確認する。
3. `org_bootstrap.seed` を順に実行する。
4. 冪等性と再実行可否を確認する。
5. `quality_gates.smoke_tests` があれば post-seed smoke を確認する。

## 出力

- 実行した seed 手順
- 成否
- 再実行可否
- post-seed smoke の状況

## フォールバック

- resolver も overlay も使えなければ seed 手順不足を明記し、正式な完了扱いにしない
