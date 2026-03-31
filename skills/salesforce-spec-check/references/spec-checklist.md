# Spec Check Checklist

## データモデル

- SPEC にあるオブジェクトがメタデータにあるか
- SPEC にあるフィールドが実装済みか
- Picklist 値や deleteConstraint が一致するか

## ビジネスロジック

- 状態遷移
- 承認後処理
- バッチ / Queueable の責務
- 通知の送信条件
- 締めロックや権限制御

## UI

- LWC の表示要素
- 導線
- ページネーション
- エラー表示

## 権限 / セキュリティ

- Permission Set に必要権限があるか
- `without sharing` の入口制御があるか

## ロードマップ

- 後続 Phase 予定の項目を「未実装バグ」と混同しない
