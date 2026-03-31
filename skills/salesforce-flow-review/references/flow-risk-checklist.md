# Flow Risk Checklist

## Entry 条件

- 同じオブジェクト / 同じ条件帯で競合する Flow がないか
- before-save / after-save の責務が混在していないか
- Trigger や Apex と二重更新になっていないか

## 実行順序

- 更新順序が暗黙依存になっていないか
- 再入やループで意図せず再実行しないか
- 非同期処理や通知との順序が破綻していないか

## 運用性

- Activation 条件が明確か
- 失敗時のエラー導線と復旧方法が分かるか
- Record Type / Layout / Permission Set と齟齬がないか
