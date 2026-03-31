# LWC Review Checklist

## Apex 連携

- `@wire` より命令型が適切か
- エラー時に `ShowToastEvent` などで通知しているか
- データ変更後の再取得導線があるか

## コンポーネント設計

- `@api` / state の持ち方が妥当か
- 親子間の通知が `CustomEvent` ベースか
- `connectedCallback` / `disconnectedCallback` の責務が明確か

## HTML

- `for:each` に `key` があるか
- 読み込み中、空状態、エラー状態があるか
- `lightning-card` のタイトルやラベルが一貫しているか

## アクセシビリティ

- icon / spinner に代替テキストがあるか
- ボタンラベルが曖昧でないか

## テスト観点

- Apex モックが `__esModule: true, default: jest.fn()` か
- `flushPromises` で非同期完了を待っているか
