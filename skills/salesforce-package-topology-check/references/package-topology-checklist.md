# Package Topology Checklist

## 境界

- package dir ごとの責務が分離されているか
- cross-package 前提が過剰でないか
- namespace や install 単位の境界と矛盾していないか

## 依存

- dependency が片方向で整理されているか
- upgrade 時に壊れやすい依存を持っていないか

## unpackaged metadata

- package に入れられない metadata だけを外へ出しているか
- deploy 順序と install 後手順が整理されているか
