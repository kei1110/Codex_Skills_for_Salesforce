# Trigger Scaffold Checklist

## 配置前確認

- 対象オブジェクトと operation が明確か
- 既存 Trigger / Flow / Process と責務衝突がないか
- service 層へ切り出すべき処理を見極めたか

## Trigger 実装

- Trigger には再帰ガードと委譲だけを置いているか
- before / after の不要メソッドを持っていないか
- handler / service の責務が分離されているか

## Bulk / ガバナ

- 200 件を前提にしても SOQL / DML が線形増加しないか
- ループ内 SOQL / DML がないか
- `Map` / `Set` を使って再利用しているか

## テスト

- 正常系、異常系、Bulk のケースがあるか
- 再帰ガードや二重実行の考慮が必要か
- Queueable / future を使うなら `Test.stopTest()` 後に検証しているか
