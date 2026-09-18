# SOP 01 Candidate Generation

版本：1.0；所有判断须遵循 MASTER v1.0，冲突进入 gap audit。

## Purpose

建立与结果无关的候选全集

## Scope

冻结的H-arm食源性酚类范围

## Required input

scope文件；食品来源；PubChem/ChEBI

## Required tools

浏览器、PubChem、候选模板

## Step-by-step procedure

按subclass列候选；核对膳食来源；锁定CID/InChIKey；分开苷元/糖苷及立体异构体

## Decision rules

不得按ORAC结果反向纳入；混合物、提取物及主要药用来源不入主榜

## QC checklist

每项有唯一结构；food occurrence有来源；第二人复核身份

## Common mistakes

把quercetin、quercitrin、rutin合并；先看ORAC再决定候选

## Required output

版本化candidate universe CSV

## Stop condition

所有候选身份已解决或标记待解决

## Example

Quercetin、quercitrin、rutin分别建行。
