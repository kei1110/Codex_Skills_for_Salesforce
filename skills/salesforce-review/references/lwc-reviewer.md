# LWC Review Checklist

## Apex 連携

- `@wire` より命令型が適切か
- エラー時に `ShowToastEvent` などで通知しているか
- データ変更後の再取得導線があるか

## コンポーネント設計

- `@api` / state の持ち方が妥当か
- `@api` setter で再取得が必要なら setter 内で明示的に制御しているか
- 親子間の通知が `CustomEvent` ベースか
- `bubbles` / `composed` を必要以上に広げていないか
- `connectedCallback` / `disconnectedCallback` の責務が明確か
- 非同期結果が切断後や古いリクエストで state を上書きしないか
- 重い `map` / `filter` / `sort` を getter に書いていないか

## HTML

- `for:each` に `key` があるか
- 読み込み中、空状態、エラー状態があるか
- `lightning-card` のタイトルやラベルが一貫しているか
- テンプレートで unary 演算や複雑式に頼っていないか
- `lwc:dom="manual"` や直接 DOM 操作が最小限か

## アクセシビリティ

- icon / spinner に代替テキストがあるか
- ボタンラベルが曖昧でないか
- モーダル、タブ、カスタム picker に必要な `role` / `aria-*` があるか

## テスト観点

- Apex モックが `__esModule: true, default: jest.fn()` か
- `flushPromises` で非同期完了を待っているか
- `disconnectedCallback` 後に非同期結果が返っても壊れないか
- `@api` boolean の既定値やプロパティ変化で再描画が崩れないか
