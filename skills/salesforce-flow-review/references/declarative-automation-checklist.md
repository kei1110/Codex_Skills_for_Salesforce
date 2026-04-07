# Declarative Automation Checklist

## 対象

- Flow
- Validation Rule
- Approval Process
- Record Type
- package 外で扱う宣言的 metadata

## 観点

- 仕様と一致しているか
- Apex と責務が衝突していないか
- 実行主体が current user か automated user かで前提が変わらないか
- 権限や UI 導線が破綻していないか
- package install、source deploy、手動設定で成立条件が変わらないか
- エラー時の挙動が利用者にとって理解可能か
- 運用時の手修正や例外対応が必要になりすぎないか
