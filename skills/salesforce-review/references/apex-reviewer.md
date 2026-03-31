# Apex Review Checklist

## ガバナ制限

- SOQL / DML がループ内にないか
- 取得結果を `Map` / `Set` 化して再利用しているか
- 200 件バルクを前提にしても SOQL 数が固定に近いか

## セキュリティ

- 既定は `with sharing` か
- `without sharing` なら理由が明確か
- `@AuraEnabled` 入口で権限チェックしているか
- 動的 SOQL が bind 変数中心になっているか

## プロジェクト固有ルール

- 日付取得は repo 標準の utility に揃える
- `@AuraEnabled(cacheable=true)` は読み取り専用だけに使う
- `apiVersion` は repo 標準に揃える

## テスト

- 正常系と異常系があるか
- `Test.startTest()` / `Test.stopTest()` を適切に使っているか
- Queueable は `stopTest()` 後に検証しているか
- `AuraHandledException` はメッセージではなく例外型を確認しているか
