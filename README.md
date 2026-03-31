# codex-skills

Codex CLI 向けに整理した Salesforce 用スキル集です。

- 対象: Salesforce 2GP / monorepo / Apex + LWC 開発
- 形式: `skills/<skill-name>/SKILL.md` + 必要に応じて `references/`
- 方針: Codex は `resolve-overlay.py` で schema v3 overlay を解決し、正規化 JSON を起点に repo 固有情報を使う
- 目標: 各 skill は単体で `~/.codex/skills` に置いて使え、repo 固有差分は overlay で補う

主なスキル:

- `salesforce-review`
- `salesforce-spec-check`
- `salesforce-deploy-check`
- `salesforce-release-check`
- `salesforce-quick-test`
- `salesforce-seed-data`
- `salesforce-setup-org`
- `salesforce-phase-summary`
- `salesforce-gen-test`
- `salesforce-new-lwc`
- `salesforce-new-trigger`
- `salesforce-perm-check`
- `salesforce-package-release`
- `salesforce-flow-review`
- `salesforce-smoke-check`
- `salesforce-package-topology-check`

## レイヤ構成

- `skills/`
  Salesforce 全般で使える core skills
- `overlays/workflows/`
  開発様式ごとの差分。`README.md` は人向け説明、`overlay.yaml` は Codex 向け manifest
- `overlays/repos/`
  個別リポジトリごとの差分。source、packaging、security、org bootstrap、quality gate、static analysis、context pruning を `overlay.yaml` にまとめる

## 推奨アーキテクチャ: 3 層モデル

このリポジトリは、企業内で複数の Salesforce repo を並行開発する前提で、次の 3 層モデルで運用することを推奨する。

1. 企業標準層
   - 配置先: `skills/`
   - 役割: 会社全体で共通化したいレビュー観点、release gate、権限確認、仕様確認などを置く
   - 例: `salesforce-review`, `salesforce-release-check`, `salesforce-perm-check`
2. 開発様式標準層
   - 配置先: `overlays/workflows/`
   - 役割: 2GP、monorepo、unpackaged metadata など、複数 repo で共通する構造差分を持つ
   - 例: `2gp-managed-monorepo`
3. 案件・repo 専用層
   - 配置先: `overlays/repos/`
   - 役割: source、docs、packaging、security、org bootstrap、quality gate など、その repo だけの差分を持つ
   - 例: `gatcha`

この 3 層で責務を分けることで、共通 skill を複数 repo へ横展開しつつ、案件ごとの差分だけを overlay に局所化できる。

## 推奨運用ルール

- まず企業標準層で吸収できるかを考える
- repo ごとの差分は `overlays/repos/<repo>/overlay.yaml` に置く
- 同種の repo 群で共通する前提は `overlays/workflows/` に置く
- 特定案件だけの業務ルールが強い場合だけ project 専用 skill を追加する
- repo 固有事情を `skills/` へ直接書き戻さない
- overlay 変更時は `resolve-overlay.py` と validator を前提に整合を取る
- 実運用 overlay は `schema_version: 3` を使う
- 静的解析の結果は overlay に保存せず、`parse-static-analysis.py` と `evaluate-quality-gates.py` で都度正規化する

判断に迷ったら、次の順で置き場所を決める。

1. 全 repo で再利用するなら `skills/`
2. 同じ開発様式の repo 群だけで共通なら `overlays/workflows/`
3. その repo だけなら `overlays/repos/`

## 使い方

1. まず `skills/` の core skill を使う
2. 開発様式に応じて `overlays/workflows/<name>/overlay.yaml` を用意する
3. 対象リポジトリに応じて `overlays/repos/<name>/overlay.yaml` を用意する
4. `python3 scripts/resolve-overlay.py --repo <name> --pretty` で TA 向け解決済み JSON を得る
5. 差分中心の作業では `python3 scripts/prune-context.py --repo <name> --changed-file <path>` で読む source / docs / tests を絞る
6. 詳細な補足が必要なときだけ overlay の `README.md` を読む

## そのまま使う

`skills/` 配下は単体で持ち運べる構成にしてある。`~/.codex/skills` へリンクする場合は次を使う。

```bash
./scripts/install-to-codex-home.sh
```

既定では `${CODEX_HOME:-$HOME/.codex}/skills` へ skill を symlink し、あわせて `${CODEX_HOME:-$HOME/.codex}/salesforce-kit` へこのリポジトリ全体を symlink する。

構成検証には次を使う。

```bash
python3 -m pip install -r scripts/requirements.txt
python3 scripts/validate-overlays.py
./scripts/validate-skills.sh
```

静的解析の正規化と quality gate 判定には次を使う。

```bash
python3 scripts/parse-static-analysis.py --parser pmd-json --input pmd-report.json --pretty
python3 scripts/evaluate-quality-gates.py --repo <name> --report normalized-report.json --pretty
```

企業内での標準的な運用フローは次の通り。

1. `skills/` を企業標準セットとして配布する
2. repo ごとに `overlays/repos/<repo>/overlay.yaml` へ source / packaging / security / bootstrap / static analysis / pruning を管理する
3. 新しい repo は `init-repo-overlay.sh` で雛形を切る
4. Codex は `resolve-overlay.py` で解決済み JSON を取得してから skill を使う
5. skill 本体を変える前に、overlay で吸収できないかを確認する

## 収録内容

- workflow overlay 例
  - `overlays/workflows/2gp-managed-monorepo/`
- repo overlay 例
  - `overlays/repos/gatcha/`
  - `overlays/repos/_template/`

## 新しい Salesforce repo を足すとき

1. core skill だけで不足する repo 固有情報を洗う
2. 既存 workflow overlay で足りるか確認する
3. `./scripts/init-repo-overlay.sh <repo-slug> <display-name> [workflow-overlay-path]` で雛形を作る
4. `overlays/repos/<repo-slug>/overlay.yaml` を埋めて repo 固有情報を機械可読化する
5. `python3 scripts/validate-overlays.py --overlay overlays/repos/<repo-slug>/overlay.yaml` で manifest を確認する
6. 必要な補足だけ `README.md` に書き、`./scripts/validate-skills.sh` で全体確認する

## schema v3 の要点

- `schema_version: 3` は実運用 overlay で必須
- `quality_gates.static_analysis` は PMD / SFDX Scanner の実行コマンド、parser、thresholds、blocking rule を持つ
- `context_pruning` は差分ファイルから読む source / docs / tests を絞るための hint を持つ
- `inherits` は repo root 基準の相対パスのみを許可し、Git のタグやブランチ継承は扱わない
