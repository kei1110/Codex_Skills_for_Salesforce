---
name: salesforce-perm-check
description: Check Salesforce security architecture and permission consistency. Use this for permission review, 権限確認, Permission Set Group review, record type assignment review, class/FLS checks, and Custom Permission gate validation.
metadata:
  short-description: Check TA permission model
---

# Salesforce Permission Check

Controller と metadata の権限制御を TA 観点で確認する。

## 使う場面

- `@AuraEnabled` controller を追加・変更した
- Permission Set / PSG / Record Type / UI visibility の漏れが不安
- `without sharing` の入口制御を確認したい

## 最初に確認する入力

- 対象 controller / class
- 使用オブジェクトとフィールド
- Record Type 利用の有無
- resolver が使えるなら解決済み JSON の `security`

## 最初に読むもの

- resolver が使えるなら解決済み JSON の `security`
- `references/security-architecture.md`

## 手順

1. `security.permission_sets`、`permission_set_groups`、`muting_permission_sets` を確認する。
2. `@AuraEnabled` を持つ controller を列挙する。
3. `classAccesses`、`objectPermissions`、`fieldPermissions` を確認する。
4. `record_type_assignments` と `ui_visibility` を確認する。
5. `without sharing` なら `custom_permissions` と入口制御を確認する。
6. `licenses` による制約がないかを確認する。

## 出力

- `Critical`: 入口制御欠落、PSG/muting の破綻、Record Type/visibility の重大漏れ
- `Warning`: 将来事故りやすい権限制御
- `Advisory`: 運用上の改善案

## 注意

- Permission Set だけ見て完了にしない
- `required: true` フィールドに不要な FLS を付けない
- UI 到達性とデータ到達性を分けて考える
