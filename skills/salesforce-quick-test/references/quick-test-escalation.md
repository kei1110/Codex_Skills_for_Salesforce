# Quick Test Escalation Rules

## そのまま quick test でよい変更

- Apex class 単体修正
- LWC 単体修正
- テストコードだけの修正

## release-check へ昇格する変更

- Permission Set / Profile / Permission Set Group
- package dir を跨ぐ変更
- Flow / Validation / RecordType / Approval metadata
- queueable / batch / platform event の変更

## 依存テスト追加が必要な変更

- Service / Selector / Domain の共通部品
- Trigger handler
- sharing / security の入口
