# SOP 06 Unit Normalization

版本：1.0；所有判断须遵循 MASTER v1.0，冲突进入 gap audit。

## Purpose

统一为mol TE/mol compound

## Scope

身份确认且单位可解释的记录

## Required input

原值、单位、MW及来源

## Required tools

Excel或计算器；Python/R可选

## Step-by-step procedure

识别单位；写公式；计算；保留足够精度；第二人独立复算

## Decision rules

µmol TE/g×MW/1e6；直接mol/mol不再换算；form-specific MW

## QC checklist

original不覆盖；conversion_verified签名；有效数字合理

## Common mistakes

忘除1e6；用错误盐型MW；把food µmol/100g换成单体值

## Required output

带完整换算链的record

## Stop condition

换算可复现，否则B2/C/X

## Example

14,272×194.18/1e6=2.771。
