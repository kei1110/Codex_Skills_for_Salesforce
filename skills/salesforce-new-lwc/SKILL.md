---
name: salesforce-new-lwc
description: Scaffold a new Salesforce LWC in line with enterprise architecture patterns. Use this when creating a new LWC, 新規画面, Apex-connected UI, and metadata-aware component scaffolding.
metadata:
  short-description: Scaffold enterprise LWC
---

# Salesforce New LWC

新規 LWC を企業標準アーキテクチャへ接続する前提で作る。

## 最初に確認する入力

- component 名
- 配置先 package dir
- resolver が使えるなら解決済み JSON の `source` と `security`

## 最初に読むもの

- resolver が使えるなら解決済み JSON の `source` と `security`
- `references/scaffold-checklist.md`

## 生成後に必ず確認すること

- Permission Set / PSG / UI visibility
- 必要 metadata の更新
- エラー contract と DTO shape
- Jest と Apex test の要否
