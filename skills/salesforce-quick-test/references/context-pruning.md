# Context Pruning

- quick test では changed files から読む source / tests / docs を先に絞る
- Apex class 変更は同名 `*Test.cls` を優先候補にする
- Trigger 変更は handler / handler test を候補に含める
- metadata、permission、package 境界変更は release-check への昇格候補にする
