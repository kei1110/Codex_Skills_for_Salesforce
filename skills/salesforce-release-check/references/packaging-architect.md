# Packaging Architecture Checklist

## 2GP / Package Topology

- package dir ごとの責務が分離されているか
- package 間依存が意図通りか
- unpackaged metadata が package 外で管理されているか

## Install / Upgrade

- install validation があるか
- upgrade 時の破壊的変更がないか
- post-install 相当の確認が必要か

## Release Gate

- package version create 前提が揃っているか
- dependency package のバージョンが固定されているか
- rollback または切り戻し判断があるか
