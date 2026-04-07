# Unpackaged Post Deploy Checklist

## 配置と順序

- package 外 metadata の deploy 順序が明確か
- local setup、CI、package build、install 後の手順で送られる metadata が一致しているか
- 一部環境では `profiles` のみ、別経路では `flows` や `approvalProcesses` を含むなどの差が明示されているか
- FlexiPage / Layout / Record Type / Permission Set の依存順が崩れていないか
- post deploy 手順が package install 後に実行される想定か

## 手動作業

- activation、割当、公開設定などの手動作業が runbook にあるか
- source deploy できない metadata が template / 手作業として整理されているか
- 手動作業の完了条件が書かれているか
- 手動作業後の smoke が定義されているか

## 実行方針

- `--ignore-conflicts` が常用前提になっていないか
- package install だけでは成立しないなら、追加 deploy / manual setup の順序が明確か
- unpackaged metadata の未反映で seed、approval、smoke が偽失敗しないか

## リスク

- package version install だけでは成立しない構成が明示されているか
- sandbox / production で差が出る手順がないか
