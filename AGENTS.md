- 常に日本語で応答してください

- Salesforce 関連の作業では、まず `resolve-overlay.py` で overlay を解決し、解決済み JSON を正本として扱ってください
- repo 固有事情を推測で埋めず、`overlays/workflows/` または `overlays/repos/` に定義された情報を優先してください
- repo 固有事情を `skills/` へ直接書き戻さず、共通化できるものは `skills/`、差分は `overlays/` に置いてください

- Salesforce のレビュー、確認、計画では Apex / LWC だけでなく、Flow、Validation Rule、Record Type、Approval Process、Permission Set Group、muting、packaging、org bootstrap も確認対象に含めてください
- Salesforce TA 観点で、実装品質だけでなく、権限、metadata 整合、release readiness、install / upgrade 影響、運用性も確認してください

- 指摘は `Critical / Warning / Advisory` で整理してください
- release や deploy 可否の判定が必要な場合は `PASS / FAIL / CONDITIONAL` を使ってください
- Permission、metadata、package 境界変更は quick test だけで済ませず、必要に応じて `salesforce-release-check` 相当へ昇格してください

- 新しい repo 対応を追加する場合は、まず overlay で吸収できるかを検討し、必要な場合だけ新しい skill を追加してください
- 新しい overlay や skill を追加・更新した場合は、`validate-overlays.py` と `validate-skills.sh` を通る状態を維持してください
