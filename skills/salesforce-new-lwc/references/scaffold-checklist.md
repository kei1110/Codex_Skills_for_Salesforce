# LWC Scaffold Checklist

## 配置前確認

- component 名が repo 命名規約に沿っているか
- 配置 package dir が正しいか
- 既存コンポーネントとの責務重複がないか

## Apex 連携

- 読み取り専用なら `@AuraEnabled(cacheable=true)` を検討したか
- 更新系なら命令型呼び出しになっているか
- DTO に不要フィールドを返していないか

## UI

- 読み込み中、空状態、エラー状態があるか
- 主要操作に `ShowToastEvent` などの通知導線があるか
- `for:each` に `key` があるか

## テスト

- Apex controller test を用意したか
- Jest テストが必要か判断したか
- 権限や異常系のテストを検討したか

## metadata

- `apiVersion` が repo 標準に揃っているか
- 必要なら FlexiPage や app page への配置を確認したか
- Permission Set の `classAccesses` を追加したか
