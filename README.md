# Salesforce Codex Kit

Salesforce 向けの Codex 運用キットです。  
skill 本文だけでなく、overlay、resolver、validator、static analysis、context pruning、repo discovery まで含めて企業利用しやすい形にしています。

## 5 分で導入する

1. 依存を確認する

```bash
python3 --version
```

2. repo ローカルの `.venv` を作り、必要な依存を入れる

```bash
python3 -m venv .venv
.venv/bin/pip install -r scripts/requirements.txt
```

3. kit を install して自己診断する

```bash
/bin/bash scripts/bootstrap-kit.sh
```

4. 詳細診断を JSON で見たい場合は次を使う

```bash
python3 scripts/doctor.py --json
```

## doctor の見方

- `OK`: そのまま使える
- `WARN`: 導入は進められるが整備した方がよい
- `FAIL`: 導入続行前に修正が必要
- `NEXT`: 次に実行すべき代表コマンド

依存は自動導入しません。不足があれば fix コマンドを表示します。

## bootstrap がやること

`bootstrap-kit.sh` は次を行います。

- `${CODEX_HOME:-$HOME/.codex}/skills` に各 skill の symlink を作る
- `${CODEX_HOME:-$HOME/.codex}/salesforce-kit` にこのリポジトリ全体の symlink を作る
- `doctor.py` を実行して導入状態を確認する

`CODEX_HOME` を変えたい場合は次を使えます。

```bash
/bin/bash scripts/bootstrap-kit.sh --codex-home /path/to/.codex
```

JSON で doctor を見たい場合は次でも構いません。

```bash
/bin/bash scripts/bootstrap-kit.sh --doctor-json
```

## 導入プリセット

- `minimal`
  - `salesforce-review`
  - `salesforce-release-check`
  - `salesforce-quick-test`
  - `salesforce-perm-check`
- `standard`
  - `minimal` + `salesforce-flow-review` + `salesforce-smoke-check` + `salesforce-package-release`
- `ta-full`
  - 全 skill

## Salesforce 作業の基本

Salesforce 関連の review、check、setup では、まず overlay を解決してください。  
Codex が最初に見る正本は `overlay.yaml` そのものではなく、`resolve-overlay.py` が返す解決済み JSON です。

```bash
python3 scripts/resolve-overlay.py --repo <repo-slug> --pretty
```

この JSON の `source`、`docs`、`packaging`、`security`、`org_bootstrap`、`quality_gates` を起点に作業します。  
人向けの補足が必要なときだけ `overlays/.../README.md` を読みます。

## 使い方サンプル

1. 既存 overlay を解決して内容を確認する

このリポジトリに入っている `gatcha` 例をそのまま確認する場合です。

```bash
python3 scripts/resolve-overlay.py --repo gatcha --pretty
```

`source` に読むべき metadata の場所、`docs` に仕様書、`security` に Permission Set 群、`quality_gates` に lint や test コマンドがまとまって出ます。

2. 既存 Salesforce repo から overlay の初期候補を作る

手元の Salesforce repo を kit に載せ始めるときの最小例です。

```bash
python3 scripts/discover-overlay.py \
  --workspace-root /path/to/salesforce-repo \
  --name "My Salesforce Repo" \
  --pretty
```

出てきた候補を見ながら `overlays/repos/<repo-slug>/overlay.yaml` を埋めます。

3. 新しい repo overlay を雛形から作る

workflow overlay も指定して開始したい場合の例です。

```bash
./scripts/init-repo-overlay.sh my-repo "My Salesforce Repo" \
  overlays/workflows/2gp-managed-monorepo/overlay.yaml
```

作成後は次で整合を確認します。

```bash
python3 scripts/validate-overlays.py --overlay overlays/repos/my-repo/overlay.yaml
./scripts/validate-skills.sh
```

## 新しい repo を導入する

1. 雛形を作る

```bash
./scripts/init-repo-overlay.sh <repo-slug> "<display-name>" [workflow-overlay-path]
```

2. 既存 repo から初期候補を出す

```bash
python3 scripts/discover-overlay.py --workspace-root /path/to/salesforce-repo --name "<display-name>" --pretty
```

3. overlay を埋めて検証する

```bash
python3 scripts/validate-overlays.py --overlay overlays/repos/<repo-slug>/overlay.yaml
./scripts/validate-skills.sh
```

## 更新後の確認

overlay、skill、script を更新したら次を通してください。

```bash
python3 scripts/validate-overlays.py
./scripts/validate-skills.sh
python3 -m unittest discover -s tests -p '*_test.py'
```

## 詳細ドキュメント

- [アーキテクチャ](docs/architecture.md)
- [repo onboarding](docs/onboarding.md)
- [導入チェックリスト](docs/adoption-checklist.md)
- [skill authoring](docs/skill-authoring.md)
- [直近の実装計画](docs/implementation-plan-next-batch.md)
