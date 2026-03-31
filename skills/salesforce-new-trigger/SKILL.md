---
name: salesforce-new-trigger
description: Scaffold a Salesforce trigger in line with enterprise architecture patterns. Use this when adding a trigger, handler, service-connected workflow, and bulk-safe automation with metadata awareness.
metadata:
  short-description: Scaffold enterprise trigger
---

# Salesforce New Trigger

新規 Trigger を企業標準アーキテクチャへ接続する前提で作る。

## 最初に確認する入力

- 対象オブジェクト
- before / after と operation 種別
- resolver が使えるなら解決済み JSON の `source`

## 最初に読むもの

- resolver が使えるなら解決済み JSON の `source`
- `references/scaffold-checklist.md`

## 生成後に必ず確認すること

- service / selector への責務分離
- Bulk / lock / async 影響
- 関連 metadata と test の不足
