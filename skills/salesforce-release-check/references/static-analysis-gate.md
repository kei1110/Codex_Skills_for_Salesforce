# Static Analysis Gate

- PMD と SFDX Scanner の結果は `parse-static-analysis.py` で正規化する
- severity は `Critical / Warning / Advisory` に統一する
- `evaluate-quality-gates.py` は overlay の `quality_gates.static_analysis.thresholds` で判定する
- `Critical` 超過は原則 `FAIL`、`Warning` / `Advisory` の超過は `CONDITIONAL` 候補とする
