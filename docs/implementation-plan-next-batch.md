# Next Batch Implementation Plan

この文書は、次の改善バッチを実装前にレビューするための計画書です。
目的は、設計論点を先に潰し、実装はレビュー合意後にまとめて着手することです。

## 目的

- manifest と補助スクリプトを強化し、AI の主観ではなく構造化データで判断できる範囲を増やす
- 複数 repo 運用で効く改善を優先し、repo 数が増えても保守コストが急増しない状態を目指す
- skill 文面の追加より、overlay schema、resolver、validator、helper scripts を強くする

## 今回の基本方針

- まず「運用で効く改良」を優先する
- 既存の 3 層モデルは維持する
- `overlay.yaml` と helper scripts を正本に寄せる
- 難易度の高い解析は段階導入する
- 一度に全部は入れず、review で合意した順にバッチ実装する

## 今回採る改善

### A. Quality Gate を理由付き出力にする

現状の `PASS / FAIL / CONDITIONAL` だけでは運用ログ、PR コメント、リリース判断で弱い。
そのため `evaluate-quality-gates.py` の出力を explanation-rich に拡張する。

追加する出力項目:

- `status`
- `summary`
- `reasons`
- `next_actions`
- `blocking_rules_applied`

最小 shape:

```json
{
  "status": "FAIL",
  "summary": {
    "critical": 2,
    "warning": 1,
    "advisory": 0
  },
  "reasons": [
    {
      "type": "static_analysis",
      "tool": "pmd",
      "rule": "ApexCRUDViolation",
      "severity": "Critical",
      "count": 2
    }
  ],
  "next_actions": [
    "CRUD/FLS ガード実装を確認",
    "2GP 公開境界への影響を確認"
  ],
  "blocking_rules_applied": [
    "Critical が 1 件でもあれば FAIL"
  ]
}
```

### B. overlay の list 上書き・削除対応を追加する

現状は list を加算マージするため、workflow overlay で入れた値を repo overlay 側で外しにくい。
ただし schema を複雑にしすぎないよう、最初は list に限定した最小機能だけ入れる。

今回入れるもの:

- `replace: true`
- `values: []`
- `remove: []`

今回入れないもの:

- `clear: true`
- map 単位の高度な patch DSL

例:

```yaml
source:
  apex:
    replace: true
    values:
      - force-app/custom/main/default/classes
```

```yaml
quality_gates:
  smoke_tests:
    remove:
      - sf org run smoke --target-org old-sandbox
```

### C. Flow / approval / unpackaged metadata の専用チェックを厚くする

Salesforce で事故りやすい領域なので、Apex/LWC と同じ深さまで上げる。
まずは analyzer より先に review 観点と出力テンプレートを強化する。

重点対象:

- Flow の entry 条件競合
- before-save / after-save の責務混在
- Approval Process の手動設定漏れ
- UI 到達性と権限の不整合
- unpackaged post deploy の順序漏れ

対象 skill:

- `salesforce-flow-review`
- `salesforce-release-check`
- `salesforce-smoke-check`

### D. `prune-context.py` を軽量 dependency-aware 化する

いきなり完全依存解析には行かず、heuristic に「証拠」を足す形で段階導入する。

Phase 1 の対象:

- Apex: class 内参照、`new Xxx()`、`Xxx.method()`、`Database.executeBatch(Xxx)` の簡易抽出
- Trigger: handler 参照と関連 test の補強
- LWC: `import`、`@salesforce/apex/...`、`c/...` の抽出
- package boundary: `sfdx-project.json` の `packageDirectories` と metadata path を使った境界判定
- 複数 changed files の重み付け

Phase 1 で入れないもの:

- Apex SymbolTable の完全利用
- Salesforce metadata の完全 cross-reference
- org 実体依存の依存解決

### E. Skill 出力フォーマットを共通化する

JSON 強制はまだ行わず、まず Markdown テンプレートを共通化する。
対象は critical skill 群。

共通テンプレート:

```md
## Summary
## Decision
## Critical
## Warning
## Advisory
## Missing Evidence
## Next Actions
```

対象 skill:

- `salesforce-review`
- `salesforce-release-check`
- `salesforce-perm-check`
- `salesforce-spec-check`
- `salesforce-flow-review`
- `salesforce-smoke-check`

### F. repo onboarding の半自動化を追加する

`init-repo-overlay.sh` は雛形生成のみなので、初期推定を別スクリプトで補う。
shell ではなく Python ベースで実装する。

追加候補スクリプト:

- `scripts/discover-overlay.py`

初期推定対象:

- `sfdx-project.json` から `package_dirs`
- `force-app/**` 走査から source path
- `docs/` 配下から spec / technical 候補
- `permissionsets/` と `permissionsetgroups/` から security 候補
- CI 設定から lint / test コマンド候補

## 今回は見送る改善

### 1. `clear: true`

`replace: true, values: []` で代替できるため、初回実装では不要。

### 2. Git ref ベースの inherits

再現性、セキュリティ、validator の複雑さを考えると不採用。
version coexistence は `schema_version` とディレクトリ構成で扱う。

### 3. 完全 dependency-aware pruning

ROI に対して初回コストが高すぎる。
まずは軽量 dependency-aware を入れ、その後に必要なら深掘りする。

### 4. 生成系 skill の大幅拡張

価値はあるが、レビュー / release / security / metadata 側の改善を優先する。

## 実装バッチ

### Batch 1. Quality Gate と出力標準化

対象:

- `scripts/evaluate-quality-gates.py`
- `scripts/static_analysis.py`
- critical skill の `SKILL.md`
- validator

完了条件:

- reason-rich な gate 出力が返る
- critical skill に共通出力テンプレートが入る
- fixture test で gate 判定理由を検証できる

### Batch 2. overlay merge 強化

対象:

- `scripts/overlay_resolver.py`
- `scripts/validate-overlays.py`
- `overlays/overlay-schema.md`
- `_template` と fixture overlay

完了条件:

- list に `replace / values / remove` が使える
- 後方互換を壊さず既存 overlay が通る
- merge fixture が通る

### Batch 3. metadata リスク強化

対象:

- `salesforce-flow-review`
- `salesforce-release-check`
- `salesforce-smoke-check`
- 新しい reference

完了条件:

- Flow / approval / unpackaged metadata の観点が skill に明示される
- 出力テンプレートで metadata リスクが落ちない

### Batch 4. pruning 精度改善

対象:

- `scripts/prune-context.py`
- pruning fixture
- quick-test / review / flow-review の文面

完了条件:

- changed file 以外に依存候補を証拠付きで返せる
- Apex / LWC / Trigger / metadata の fixture が通る

### Batch 5. onboarding 半自動化

対象:

- `scripts/discover-overlay.py`
- `scripts/init-repo-overlay.sh`
- README

完了条件:

- 新規 repo から overlay の初期候補を出せる
- 雛形生成後の手入力量が目に見えて減る

## レビュー論点

レビューで最低限合意したい論点を先に固定する。

### Round 1: スコープ妥当性

- 今回の優先順位は妥当か
- 見送るものの線引きは妥当か
- まず Batch 1-2 までに絞るべきか

### Round 2: データモデル妥当性

- reason-rich quality gate の output shape は十分か
- overlay の list patch semantics は過不足ないか
- 共通 output template は skill 運用に合うか

### Round 3: 実装容易性と保守性

- pruning の Phase 1 は軽すぎないか / 重すぎないか
- onboarding 自動化を shell ではなく Python にする判断は妥当か
- validator 追加のコストは許容範囲か

### Round 4: 着手判定

- Batch 1 から順に入るか
- まとめて入れるか
- issue 分割を切ってから作業するか

## テスト計画

追加または更新するテスト:

- quality gate の reason-rich 出力 fixture
- list `replace / remove` merge fixture
- Flow / unpackaged metadata の review fixture
- pruning の dependency-aware fixture
- onboarding の発見ロジック fixture

既存テストの更新:

- `tests/overlay_resolution_test.py`
- `tests/context_pruning_test.py`
- `tests/static_analysis_parser_test.py`

## 成果物

最終的に揃えるもの:

- 更新された schema doc
- 更新された resolver / validator / helper scripts
- 更新された critical skill 文面
- fixture と unit test
- onboarding 補助スクリプト
- README の運用追記

## 実装開始条件

次の 3 点がレビューで合意できたら実装に入る。

1. Batch 順序
2. overlay patch semantics の最小仕様
3. quality gate 出力 shape と skill 共通 output template
