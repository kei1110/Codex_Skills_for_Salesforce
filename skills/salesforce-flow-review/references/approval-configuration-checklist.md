# Approval Configuration Checklist

## 配置形態

- Approval Process が source deploy 対象か、参考テンプレートとして手動作成する前提か
- 2GP や package install だけで成立しない場合、その理由が runbook に明記されているか
- scratch org / CI org では再現せず、本番や sandbox でのみ手動作成する前提が混ざっていないか

## 前提条件

- 承認者経路に必要な role hierarchy、queue、public group、manager 関係が揃っているか
- 通知、メールテンプレート、提出ボタン、関連 Layout / Record Type / Permission Set が揃っているか
- submitter と approver の UI 到達性が両方確保されているか

## 動作確認

- 承認開始、承認、却下、再申請の導線を代表ユーザーで確認できるか
- 承認後の Field Update、Flow、通知、ロック解除などの後続処理が期待通りか
- activation と手動作業の完了条件が `manual_steps` や release runbook に書かれているか
