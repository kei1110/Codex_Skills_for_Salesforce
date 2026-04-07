# Seed Readiness Checklist

## 実行前

- 対象 org が初期セットアップ済みか
- 必要 package がすべて deploy 済みか
- profiles など seed 実行に必要な unpackaged metadata が反映済みか
- seed 実行ユーザーに必要権限があるか

## 依存関係

- seed が前提とする Custom Metadata や初期設定があるか
- 参照先オブジェクトや RecordType が存在するか
- approval や通知を使う seed なら、手動設定前提 metadata がその org に存在するか
- 複数 package の seed 順序が明確か

## 実行後

- 主要レコードが期待件数で作成されているか
- LWC や画面フローの代表シナリオを試せる状態か
- 冪等性や再実行可否を明記したか
