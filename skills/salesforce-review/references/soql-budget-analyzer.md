# SOQL / CPU Review Checklist

## SOQL

- 1 メソッドあたりの SOQL 数を見積もる
- `SELECT DISTINCT` を使っていないか
- ループ内 SOQL / DML がないか
- `FOR UPDATE` と `ORDER BY` の不正併用がないか

## CPU

- 日付ごとのループ、ユーザー数ごとのループ、月数ごとのループを数える
- `50 user x 3 month` など代表シナリオで反復数を概算する

## ページロード

- 1 画面で複数 `@AuraEnabled` を叩く場合の合計コストを意識する
- 同一クエリの重複呼び出しがないか確認する
