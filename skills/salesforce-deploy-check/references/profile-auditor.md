# Admin Profile Audit Checklist

対象: `unpackaged-metadata/profiles/Admin.profile-meta.xml`

## objectPermissions

- 全カスタムオブジェクトに権限があるか
- `__mdt` は除外

## fieldPermissions

- 非必須フィールドに FLS があるか
- `required: true` に不要な FLS がないか
- Formula は `editable=false` 相当になっているか

## application / tab visibility

- 全カスタムアプリ
- 全カスタムタブ

## 変更後の確認

- 新オブジェクト / 新フィールド追加後は Profile も同時に見直す
