# Package Release Runbook

## Pre-release

- package dir と依存 package が確定しているか
- quality gate が通っているか
- install / upgrade validation が定義されているか

## Release

- package version create 前提が揃っているか
- install 対象 org と upgrade 対象 org が明確か
- unpackaged metadata の扱いが明確か

## Post-release

- smoke test が定義されているか
- release note と影響範囲が整理されているか
- 切り戻し条件があるか
