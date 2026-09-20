# SOP 09 Aggregation Ranking Confidence

版本：1.0；所有判断须遵循 MASTER v1.0，冲突进入 gap audit。

## Purpose

从record生成compound summary与排名

## Scope

去重A/B1 records

## Required input

compound summary模板

## Required tools

Excel、R/Python；现有build脚本

## Step-by-step procedure

分组；计算n/median/range/IQR；赋confidence；按median排序；输出图

## Decision rules

一条=Low；两条=Moderate；≥3且异质性可接受=High；只有B2=Very low

## QC checklist

抽查公式；不取最大；confidence与数值分开

## Common mistakes

用mean掩盖异质性；热门分子因论文多加分

## Required output

summary、ranking和confidence图

## Stop condition

记录数与summary一致，排序复算通过

## Example

Quercetin多记录以median而非maximum排序。
