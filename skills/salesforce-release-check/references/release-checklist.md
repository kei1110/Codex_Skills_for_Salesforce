# Release Check Checklist

## コマンド確認

- overlay に lint / Jest / Apex test / API version check が定義されているか
- package dir ごとの追加テストが必要か
- org alias が明確か

## 品質ゲート

- API version が揃っているか
- LWC lint が通るか
- LWC Jest が通るか
- Apex test が通るか

## 仕様 / 権限

- 主要変更が SPEC と矛盾していないか
- Permission Set / Profile / Custom Permission に漏れがないか
- LWC -> Apex 参照や Trigger -> Handler 参照が壊れていないか

## 手動確認

- FlexiPage activate など手動作業が残っていないか
- package dir 単位の deploy 順序に注意が必要か
