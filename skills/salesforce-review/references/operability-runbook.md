# Operability Checklist

## Runtime Risk

- mixed DML の危険がないか
- async chain が深くなりすぎていないか
- lock contention が想定される箇所がないか

## Data Growth

- selectivity が将来も維持できるか
- LDV で CPU / query plan が破綻しないか
- sharing recalculation が重くならないか

## Production Readiness

- エラー時の観測性があるか
- 切り戻し時にどこを触るか分かるか
- metadata / package 境界に運用上の抜けがないか
