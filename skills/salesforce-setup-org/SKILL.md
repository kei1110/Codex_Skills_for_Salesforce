---
name: salesforce-setup-org
description: Create and bootstrap a Salesforce scratch org with TA-grade setup checks. Use this for scratch org setup, org 作成, feature/settings bootstrap, permission assignment, and release-ready repo bootstrap.
metadata:
  short-description: Setup scratch org runbook
---

# Salesforce Setup Org

Scratch Org の作成から初期セットアップまでを runbook として行う。

## 最初に確認する入力

- resolver が使えるなら解決済み JSON の `org_bootstrap`、`packaging`、`quality_gates`

## 最初に読むもの

- resolver が使えるなら解決済み JSON の `org_bootstrap`
- `references/setup-checklist.md`
- `references/operability-runbook.md`

## 手順

1. `scratch_def`、`default_alias`、`dev_hub_alias` を確認する。
2. `feature_setup`、`settings_setup`、`permission_assignments`、`user_setup` を確認する。
3. scratch org を作成する。
4. package / unpackaged metadata の deploy 順序を確認して初期デプロイを行う。
5. user setup と permission assignment を行う。
6. `manual_steps` を残件としてまとめる。

## 出力

- 実行した bootstrap 手順
- 未完了の手動作業
- seed へ進めるかどうか

## フォールバック

- resolver も overlay も使えなければ setup 手順の欠落を明記し、完全実施扱いにしない
