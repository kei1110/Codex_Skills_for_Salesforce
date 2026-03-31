---
name: salesforce-phase-summary
description: Summarize the results of an implementation phase in a Salesforce repo. Use this for phase summary, フェーズ要約, 実装まとめ, changed files summary, test result summary, and next-step handoff after a delivery phase.
metadata:
  short-description: Summarize a phase
---

# Salesforce Phase Summary

Phase 完了時の成果物を要約する。

## 使う場面

- feature / phase 完了後に成果物を引き継ぎたい
- PR 群やコミット群の内容をまとめたい
- 次 Phase の前提や残課題を整理したい

## 最初に確認する入力

- 対象コミット範囲
- 主要変更ファイル
- テスト結果
- 関連する review / spec / release check の結果

## 手順

1. 対象コミット範囲を決める。
2. 変更ファイルを分類する。
   - Apex 本体
   - Apex テスト
   - Trigger
   - LWC
   - メタデータ
   - Permission / Profile
3. テスト結果を集約する。
4. 設計ポイント、review 対応、仕様差分を要約する。
5. 次 Phase に持ち越す前提とリスクをまとめる。

## 出力

- Phase の目的
- 主要成果物
- テスト状況
- 残課題
- 次 Phase の前提
