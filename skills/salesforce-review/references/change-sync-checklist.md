# Change Sync Checklist

変更したファイル単体だけで完了にしない。  
Salesforce は metadata と権限が分散しているため、連動更新漏れを必ず確認する。

## カスタムフィールド追加・変更

- Permission Set / Permission Set Group / muting に `fieldPermissions` 追加が必要か
- Admin Profile や unpackaged profile に同じ反映が必要か
- `required: true` のフィールドに不要な FLS を足していないか
- Layout、Dynamic Form、Record Type、Validation Rule、Flow、Apex テストデータの連動修正が必要か
- 仕様書やデータモデル説明の更新が必要か

## カスタムオブジェクト追加・変更

- Permission Set / Profile の `objectPermissions` が必要か
- Tab、App、FlexiPage、Related List、Record Type の追加が必要か
- Trigger / Flow / Validation Rule / Approval Process の責務分担が崩れていないか
- seed、smoke、spec、roadmap の更新が必要か

## `@AuraEnabled` Controller 追加・変更

- LWC / Flow / Integration からの参照先更新が必要か
- Permission Set の `classAccesses`、Custom Permission、PSG / muting の反映が必要か
- `with sharing` / `without sharing` / `inherited sharing` の前提に合う test があるか
- 読み取りなら返却 DTO、更新なら CRUD/FLS 防御の追加が必要か

## Trigger / Service 追加・変更

- Trigger から参照する Handler / Service が存在するか
- before / after、insert / update / delete の対称パスで同じ修正が必要か
- Bulk テスト、再帰ガード、lock / async 影響の確認が必要か

## LWC 追加・変更

- `.js` / `.html` / `.js-meta.xml` / 必要なら `.css` と Jest の 3〜5 点セットになっているか
- FlexiPage、App Page、Tab、Navigation 導線の更新が必要か
- 親子コンポーネントの `@api` 伝搬、イベント、Apex import の更新漏れがないか
- 権限や UI visibility の更新が必要か

## Flow / Validation Rule / Approval Process 追加・変更

- Layout、Record Type、Permission Set、通知、承認者経路の連動更新が必要か
- 手動 activation や post-deploy 手順が増えていないか
- Apex / Trigger / LWC と責務重複や順序依存が発生していないか

## Permission / Security 追加・変更

- テストユーザー factory や `@TestSetup` の権限割当も更新が必要か
- UI 到達性、データ到達性、Record Type assignment の整合が取れているか
- license、PSG、muting の影響で付与不能な権限がないか

## 変更不要と判断した箇所

- 変更不要とした対称パスや関連 metadata は、理由を明示する
- 「既存と同じだから」ではなく、影響ケースを列挙して不要と判断する
