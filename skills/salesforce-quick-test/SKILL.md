---
name: salesforce-quick-test
description: Run targeted tests for changed Salesforce files with TA-grade escalation rules. Use this for quick test, 差分テスト, impact-based test selection, and deciding when to escalate to release check.
metadata:
  short-description: Run targeted tests with escalation
---

# Salesforce Quick Test

変更差分に対する対象テストを回し、必要なら release gate へ昇格する。

## 最初に確認する入力

- 変更ファイル範囲
- resolver が使えるなら解決済み JSON の `quality_gates.unit_tests`
- `prune-context.py` で絞った `selected.source`、`selected.tests`、`selected.docs`

## 最初に読むもの

- resolver が使えるなら解決済み JSON の `quality_gates`
- `references/quick-test-escalation.md`
- `references/context-pruning.md`

## 手順

1. 変更ファイルを集める。
2. `python3 scripts/prune-context.py --repo <repo-slug> --changed-file <path> --pretty` で読む source / tests / docs を絞る。
3. 直接変更テストと依存テストを分ける。
4. `references/quick-test-escalation.md` に沿って release-check へ昇格すべき変更か判定する。
5. quick test でよい場合だけ対象 unit test を実行する。

## 出力

- 実行したテスト一覧
- `PASS / FAIL / ESCALATE`
- release-check へ上げる理由
