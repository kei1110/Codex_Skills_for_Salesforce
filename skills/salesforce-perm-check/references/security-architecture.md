# Security Architecture Checklist

## Permission Model

- Permission Set だけでなく Permission Set Group も確認したか
- muting permission set の影響を見たか
- Custom Permission の入口制御があるか

## Access Surface

- Record Type assignment が揃っているか
- App / Tab / FlexiPage visibility が揃っているか
- license 制約で付与不能な権限がないか

## External / Specialized Users

- 外部ユーザーや特殊ライセンス利用者がいる場合の差分を見たか
- UI 到達性とデータ到達性を分けて確認したか
