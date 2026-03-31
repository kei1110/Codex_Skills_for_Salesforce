# Context Pruning

- 差分レビューでは、まず `prune-context.py` で読む source / docs / tests を絞る
- changed file 自体は必ず読む
- Apex は `*Test.cls`、LWC は `__tests__`、metadata は関連 docs を候補に含める
- pruning は heuristic なので、影響範囲が広い変更では release-check へ昇格する
