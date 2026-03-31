---
name: salesforce-package-release
description: Run and coordinate Salesforce 2GP package release work. Use this for package release, package version create, install validation, upgrade validation, release note drafting, and safe rollout preparation in Salesforce repos.
metadata:
  short-description: Coordinate package release
---

# Salesforce Package Release

2GP package release を安全に進めるための runbook。

## 使う場面

- package version create 前に確認を揃えたい
- install / upgrade 観点を含めてリリース手順をまとめたい
- release note や切り戻し判断材料も含めて整理したい

## 最初に確認する入力

- resolver が使えるなら解決済み JSON の `packaging`、`quality_gates`、`org_bootstrap`
- 対象 release の package dir
- install / upgrade の対象 org または前提

## 最初に読むもの

- resolver が使えるなら解決済み JSON の `packaging`、`quality_gates`
- `references/package-release-runbook.md`

## 手順

1. `packaging.package_dirs`、`dependencies`、`package_aliases` を確認する。
2. `quality_gates` を確認し、release 前提が揃っているか整理する。
3. `quality_gates.static_analysis` が定義されていれば、静的解析結果を正規化して gate 判定へ組み込む。
4. `install_validation` と `upgrade_validation` を確認する。
5. package version create 前に blocking issue を洗う。
6. install / upgrade 後に必要な smoke を確認する。
7. release note、影響範囲、切り戻し条件をまとめる。

## 出力

- `PASS / FAIL / CONDITIONAL`
- release 前提の不足
- install / upgrade 観点の注意点
- release note 用の要約

## フォールバック

- resolver も overlay も使えなければ package topology と install / upgrade 観点の不足を明記する
