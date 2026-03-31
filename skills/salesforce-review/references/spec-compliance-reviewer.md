# SPEC Compliance Checklist

対象コードに応じて、対象リポジトリの仕様書や画面設計書の該当節を読み、以下を照合する。

## データモデル

- フィールドの有無
- 型
- Picklist 値
- リレーション

## ビジネスロジック

- 状態遷移
- バリデーション
- 計算式
- 承認や通知のタイミング

## UI / UX

- 表示項目
- 導線
- エラーメッセージ

## 権限

- Permission Set 想定
- `with sharing` / `without sharing`
- Owner / Manager の参照範囲
