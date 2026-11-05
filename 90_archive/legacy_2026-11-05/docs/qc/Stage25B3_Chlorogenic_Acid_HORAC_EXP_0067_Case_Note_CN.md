# Stage25B.3 — Chlorogenic Acid HORAC_EXP_0067 case note

原始方法（DOI `10.3390/foods10051079`，Methods 2.4.3）将 20 µL methanolic compound sample 与 120 µL fluorescein混合并预孵育，随后加入60 µL AAPH，总well volume为200 µL；因此若“sample prepared in MeOH”指加入well时仍为100% methanol，则 final methanol = 20/200 = 10% v/v。该推断依赖两个假设：sample在加入前未再以buffer稀释，以及20 µL aliquot保持原始methanol composition。文章没有明确写final methanol percentage，也没有明确说明ORAC Trolox/blank wells含等量methanol；现有方法只说明AAPH group free of samples用于net-AUC blank correction，不能证明matched solvent control存在。

10% methanol按照 v2 DRAFT R3 trigger属于HIGH cosolvent risk。H-ORAC-FL动力学可能受有机溶剂影响，若Trolox与sample wells solvent不匹配，slope ratio不能视为充分bridgeable。同时该记录的assay-material purity/form报告不完整；这与另一个historical chlorogenic-acid X record的positional identity问题不同，但增加人工核查需要。

Old tier为B1；simulated v2 tier为B2，理由是unresolved material cosolvent comparability，而不是数值大小或排名位置。建议在正式migration前执行 `HUMAN REVIEW REQUIRED — CHLOROGENIC ACID SOLVENT COMPARABILITY`：优先核实sample working dilution与matched solvent control；若确认final methanol显著低于推导值或存在匹配控制，可维持B1；若约10%且无匹配控制，建议正式downgrade至B2；若sample preparation本身无法解析，则考虑X而不是C。它当前rank 24，模拟移出A+B1后Top20 membership不变，rank 20仍为Ferulic Acid、rank 21仍为Morin；不确定性主要来自working-solution composition未明确，而非计算式本身。
