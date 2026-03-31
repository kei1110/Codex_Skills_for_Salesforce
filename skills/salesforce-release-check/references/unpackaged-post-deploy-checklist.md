# Unpackaged Post Deploy Checklist

## 配置と順序

- package 外 metadata の deploy 順序が明確か
- FlexiPage / Layout / Record Type / Permission Set の依存順が崩れていないか
- post deploy 手順が package install 後に実行される想定か

## 手動作業

- activation、割当、公開設定などの手動作業が runbook にあるか
- 手動作業の完了条件が書かれているか
- 手動作業後の smoke が定義されているか

## リスク

- package version install だけでは成立しない構成が明示されているか
- sandbox / production で差が出る手順がないか
