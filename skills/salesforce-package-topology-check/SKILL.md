---
name: salesforce-package-topology-check
description: Review Salesforce package boundaries and topology. Use this for package topology review, package dir boundary review, dependency review, namespace boundary review, and unpackaged metadata placement checks.
metadata:
  short-description: Review package topology
---

# Salesforce Package Topology Check

package dir、依存、unpackaged metadata の構成妥当性を確認する。

## 使う場面

- package dir 分割が妥当か見たい
- package 間依存や境界が崩れていないか確認したい
- unpackaged metadata の置き方を見直したい

## 最初に確認する入力

- resolver が使えるなら解決済み JSON の `packaging` と `source`

## 最初に読むもの

- resolver が使えるなら解決済み JSON の `packaging` と `source`
- `references/package-topology-checklist.md`

## 手順

1. `package_dirs` と `dependencies` を確認する。
2. source path が package 境界と矛盾していないかを見る。
3. unpackaged metadata が package 外で扱うべきものだけか確認する。
4. install / upgrade 観点で問題になる分割や依存を確認する。

## 出力

- `Critical / Warning / Advisory`
- package 境界の問題
- 依存関係の問題
- unpackaged metadata の問題

## フォールバック

- resolver も overlay も使えなければ package dir と unpackaged metadata を探索して推定する
