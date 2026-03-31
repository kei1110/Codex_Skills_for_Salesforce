# Security Review Checklist

## CRUD / FLS

- `without sharing` なら Custom Permission 等で入口制御しているか
- 返却 DTO に不要フィールドを含めていないか
- FLS 漏れが起きそうな変更か

## インジェクション

- 動的 SOQL に文字列連結がないか
- JSON deserialize からの危険な upsert がないか
- LWC で `innerHTML` 相当の危険なパターンがないか

## アクセス制御

- 受け取った `Id` をそのまま信用していないか
- `UserInfo.getUserId()` でスコーピングすべき箇所が漏れていないか

## 並行処理

- `FOR UPDATE` の使い方が妥当か
- ロック失敗時のユーザーフレンドリな扱いがあるか

## エラーハンドリング

- 生例外をクライアントに漏らしていないか
- catch で握りつぶしていないか
