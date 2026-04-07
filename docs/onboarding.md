# Onboarding

## 最短フロー

1. 雛形を作る

```bash
./scripts/init-repo-overlay.sh <repo-slug> "<display-name>" [workflow-overlay-path]
```

2. 既存 repo から候補を出す

```bash
python3 scripts/discover-overlay.py --workspace-root /path/to/salesforce-repo --name "<display-name>" --pretty
```

3. `overlays/repos/<repo-slug>/overlay.yaml` を埋める

4. 検証する

```bash
python3 scripts/validate-overlays.py --overlay overlays/repos/<repo-slug>/overlay.yaml
./scripts/validate-skills.sh
```

## `init` と `discover` の使い分け

- `init-repo-overlay.sh`
  - repo overlay 雛形を作る
  - 新規 repo の枠組みを先に作りたいときに使う
- `discover-overlay.py`
  - 既存 repo の構造から source / docs / permissions / quality gate 候補を出す
  - 既存 repo の初回導入に使う

## 仕上げの確認

- `package_dirs` は正しいか
- `permission_sets` と `permission_set_groups` は不足していないか
- `docs.specs` と `docs.technical` は実態と合っているか
- `quality_gates.static_analysis` は実 repo の CI と整合しているか
- `context_pruning` は repo 構造と矛盾していないか
