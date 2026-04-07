# Test Coverage Review Checklist

## パス網羅

- 正常系
- 異常系
- 境界値
- 権限拒否
- Bulk

## 無効テストの兆候

- `catch` で `System.assert(true)` だけ
- 例外を期待するのに `try` 側で fail-fast していない
- assert がない
- Permission Set を付けずに例外だけ見ている
- `System.runAs` なしの管理者コンテキストで Controller を通している
- `Test.isRunningTest()` で飛ばした分岐を別テストで検証していない

## データ準備

- `@TestSetup` が使えるところは使っているか
- User 作成や Permission Set 割当を `@TestSetup` に寄せて Mixed DML を避けているか
- 共通 factory を使っているか
- `SeeAllData=true` を避けているか
- Private OWD 依存のオブジェクトで owner 文脈まで再現しているか

## 非同期 / 権限

- `Test.startTest()` / `Test.stopTest()` の境界が適切か
- Queueable / Future / PE publish の検証が `stopTest()` 後になっているか
- `without sharing` Controller は権限あり / 権限なしの両方を `System.runAs` で持っているか
