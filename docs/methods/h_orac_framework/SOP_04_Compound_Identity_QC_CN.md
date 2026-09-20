# SOP 04 Compound Identity QC

版本：1.0；所有判断须遵循 MASTER v1.0，冲突进入 gap audit。

## Purpose

确保每条数值对应唯一化学实体

## Scope

通过assay初筛的记录

## Required input

原文试剂、PubChem、CID/InChIKey

## Required tools

PubChem/ChEBI、结构查看器

## Step-by-step procedure

核对名称、form、盐/水合物、MW、立体化学和糖苷位置

## Decision rules

结构不同即分行；实验form决定MW

## QC checklist

CID和InChIKey匹配；两人复核

## Common mistakes

用aglycone MW换算glycoside；忽略hydrate

## Required output

身份已确认的record字段

## Stop condition

无法唯一识别时停止换算并判C/X

## Example

Cyanidin与C3G不可合并。
