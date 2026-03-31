---
name: salesforce-gen-test
description: Generate or extend Apex tests for a Salesforce class. Use this when adding a class, extending tests, テスト追加, 異常系テスト補強, 権限テスト追加, or bulk scenario coverage in a Salesforce repo.
metadata:
  short-description: Generate Apex tests
---

# Salesforce Generate Test

Apex クラスのテストを新規作成、または不足パスだけ補う。

## 使う場面

- 新規 Apex class / controller を追加した
- 既存テストで異常系、権限、境界値、Bulk が足りない
- `salesforce-review` でテスト不足が見つかった

## 最初に確認する入力

- 対象 class のパス
- 対応 test class の有無
- repo 標準の TestDataFactory や builder の有無
- Permission Set / Custom Permission の前提

## 手順

1. 対象 class を読み、`public` / `global` / `@AuraEnabled` メソッドを列挙する。
2. 既存 test class があれば、どのパスが未検証かを整理する。
3. 以下の観点でケースを設計する。
   - 正常系
   - 異常系
   - 境界値
   - 権限
   - Bulk
4. repo に既存の TestDataFactory や共通 builder があれば優先利用する。
5. `Test.startTest()` / `Test.stopTest()` をガバナ境界と非同期検証のために正しく配置する。
6. 期待結果は例外メッセージより振る舞い、戻り値、DML 結果で確認する。

## 出力

- 追加すべきテストケース一覧
- 新規作成または更新する test class
- 未解決の前提
  - Permission Set
  - Custom Permission
  - seed / factory 不足

## 注意

- `AuraHandledException` のメッセージ検証はしない
- `without sharing` Controller は Permission Set / Custom Permission を通す前提で作る
- `SeeAllData=true` は避ける
