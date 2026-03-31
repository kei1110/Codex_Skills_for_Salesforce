# Deploy Readiness Checklist

## API バージョン

- `sfdx-project.json` と全 `-meta.xml` の `apiVersion` が一致するか

## Permission Set

- 全 `*Controller.cls` が適切な Permission Set に入っているか
- `without sharing` Controller は Custom Permission 前提か

## 依存関係

- Trigger が参照する Handler があるか
- LWC の Apex import が実在するか
- App / Tab / FlexiPage の参照が解決するか

## デプロイ順序

- Object / Field
- MessageChannel
- Apex / Trigger
- FlexiPage / Tab / App
- Permission Set / Profile
