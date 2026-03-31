# Test Coverage Review Checklist

## パス網羅

- 正常系
- 異常系
- 境界値
- 権限拒否
- Bulk

## 無効テストの兆候

- `catch` で `System.assert(true)` だけ
- assert がない
- Permission Set を付けずに例外だけ見ている

## データ準備

- `@TestSetup` が使えるところは使っているか
- 共通 factory を使っているか
- `SeeAllData=true` を避けているか
