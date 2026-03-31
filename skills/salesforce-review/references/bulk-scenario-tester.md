# Bulk Scenario Checklist

## Trigger 200 件

- 200 件 insert/update で SOQL / DML が線形増加しないか

## リソース計算

- `50 user x 3 month` のような代表規模で CPU が破綻しないか

## 一括確定 / 一括保存

- DML 行数、ロック、集計クエリの件数を概算する

## アラート評価

- 全件ロード前提になっていないか
- ページネーションや事前集計の余地があるか
