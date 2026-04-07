# Approval Configuration Checklist

## 構成

- Approval Process の activation 状態が想定通りか
- Approval Process が source deploy 対象か、template を手動作成する前提か
- 承認者経路、通知、メールテンプレートが揃っているか
- role hierarchy、queue、public group、対象オブジェクト、Record Type、Layout と整合しているか

## 運用

- 承認開始、承認、却下、再申請の導線が確認されているか
- 手動設定が必要なら release runbook に書かれているか
- package install 後に管理者が行う作業と、その完了条件が明記されているか
- 代表ユーザーで到達確認する smoke があるか
