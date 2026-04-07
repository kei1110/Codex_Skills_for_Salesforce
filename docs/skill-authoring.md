# Skill Authoring

## 原則

- repo 固有事情は `skills/` に戻さない
- repo 差分は `overlays/repos/`
- 開発様式差分は `overlays/workflows/`
- skill は core behavior と review 観点に集中させる

## skill を増やすとき

- `skills/<name>/SKILL.md`
- `skills/<name>/agents/openai.yaml`
- 必要なら `references/`

## 追加時の確認

- `SKILL.md` に用途、入力、手順、出力がある
- 出力テンプレート契約を守っている
- 参照ファイルが validator に通る
- repo 固有事情が文面に混ざっていない

## overlay を増やすとき

- `overlay.yaml` を正本にする
- `README.md` は補足だけにする
- `validate-overlays.py` を通してから使う
