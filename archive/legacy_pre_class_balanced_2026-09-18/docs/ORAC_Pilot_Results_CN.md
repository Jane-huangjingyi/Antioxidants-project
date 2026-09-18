# 历史 ORAC 文献 Pilot 结果（中文）

## 1. Pilot 构成

Pilot 冻结 17 个化合物：10 个 phenolic/polyphenolic candidates、3 个 vitamins/vitamin-like candidates、3 个 carotenoids 和 1 个 organosulfur compound。预期测量分配为 11 个 H-ORAC、5 个 L-ORAC 和 1 个 noncanonical special-case（sulforaphane）。另有 8 个候选带技术 special-case flag；该 flag 可与 H/L arm 重叠。

身份通过 PubChem 官方记录核实，catechin、epicatechin、EGCG、aglycone/glycoside、trans-resveratrol、L-ascorbic acid、tocopherol homologues 和 carotenoid isomers 均作为不同实体处理。

## 2. 文献抽取结果

本轮正式抽取 11 条原始 ORAC-FL 数值记录，来自 3 篇原始方法/化合物研究：Ou et al. 2001（H-ORAC-FL，Table 4）、Huang et al. 2002（L-ORAC-FL，原文报告 tocopherol 值）和 Figueroa et al. 2023（H-ORAC-FL，Table 3）。记录包括 catechin 1 条、quercetin 2 条、gallic acid 1 条、caffeic acid 2 条、chlorogenic acid 1 条、L-ascorbic acid 2 条、alpha-tocopherol 1 条和 gamma-tocopherol 1 条。

按照冻结的 rubric，**Tier A=0，Tier B=11，Tier C=0，Tier X=0**。其余 9 个化合物在本次有限 pilot 中没有完成原始、可审计 ORAC-FL record extraction，标记 `not_measured`，而不是 0。

Tier B 的主要原因不是数值不存在，而是原始论文通常未同时报告 numerical purity、每个化合物的完整线性区间、compound-specific optical/interference QC 或所有 reading parameters。Huang 2002 的可访问摘要确认 L-ORAC 方法和数值，但完整逐字段方法尚需全文二次核对；因此不能升级为 Tier A。

| compound | Tier A | Tier B | Tier C/X | status |
|---|---:|---:|---:|---|
| EGCG | 0 | 0 | 0 | not_measured |
| Catechin | 0 | 1 | 0 | supportive_only |
| Epicatechin | 0 | 0 | 0 | not_measured |
| Quercetin | 0 | 2 | 0 | supportive_only |
| Kaempferol | 0 | 0 | 0 | not_measured |
| Gallic acid | 0 | 1 | 0 | supportive_only |
| Caffeic acid | 0 | 2 | 0 | supportive_only |
| Ferulic acid | 0 | 0 | 0 | not_measured |
| Chlorogenic acid | 0 | 1 | 0 | supportive_only |
| Resveratrol | 0 | 0 | 0 | not_measured |
| L-Ascorbic acid | 0 | 2 | 0 | supportive_only |
| alpha-Tocopherol | 0 | 1 | 0 | supportive_only |
| gamma-Tocopherol | 0 | 1 | 0 | supportive_only |
| Lycopene | 0 | 0 | 0 | not_measured |
| beta-Carotene | 0 | 0 | 0 | not_measured |
| Lutein | 0 | 0 | 0 | not_measured |
| Sulforaphane | 0 | 0 | 0 | not_measured |

## 3. 数值与可比性解释

Tier B 记录保留真实数值，但没有进入 `ORAC_Pilot_TierA_Analysis.csv` 的 median/range/IQR ranking。它们可显示方法异质性的量级：同一 compound 的 quercetin 报告 7.28 与 16.62 mol TE/mol，caffeic acid 报告 4.37 与 8.26，L-ascorbic acid 报告 0.95 与 0.53。该差异支持“不能直接拼接历史值”的既定规则，而不是提供可排序的中心估计。

Ou 2001 的方法使用 12.8 mM AAPH、48 nM fluorescein、75 mM phosphate pH 7.4、37 °C、每分钟读取 30 min；Figueroa 2023 使用不同 fluorescein/AAPH 配置，并专门显示 ethanol 和 kinetic analysis 会改变结果。方法差异与缺少全部 Tier A 字段共同阻止合并。

## 4. 图形结论

`H_ORAC_Historical_Distribution.png` 和 `L_ORAC_Historical_Distribution.png` 按 protocol 的停止规则被输出为 arm-specific coverage diagnostic，而非伪造的 distribution/rank plot，因为没有 Tier A record。`ORAC_Literature_Coverage.png` 显示当前支持集中于少数 phenolics、ascorbic acid 和 tocopherols；carotenoids、EGCG、epicatechin、kaempferol、ferulic acid、resveratrol 与 sulforaphane 在本轮仍为空缺。

## 5. 对十五个规定问题的回答

1. Pilot 包含 17 个 compounds。
2. 类别为 phenolic/polyphenolic 10、vitamin/vitamin-like 3、carotenoid 3、organosulfur 1。
3. 预期 H-ORAC 11 个。
4. 预期 L-ORAC 5 个。
5. 1 个候选以 noncanonical special-case 为主要分组；共有 8 个带至少一个技术 special-case flag。
6. 每个 compound 的 Tier A/B/C/X 计数见上表和 coverage CSV；总计 A=0、B=11、C/X=0，9 个无已完成记录。
7. 当前没有化合物达到“可较稳地历史排序”的 Tier A 要求。
8. 全部 17 个均不能进入正式数值排名；8 个仅有 supportive Tier B，9 个本轮未得到可用记录。
9. H-ORAC 内部正式排名目前不可行；只有少量 Tier B 且跨 protocol 差异明显。
10. L-ORAC 内部正式排名不可行；仅 alpha/gamma-tocopherol 各有一个待全文复核的 Tier B record。
11. 跨 H/L 明确不可行，且本轮没有执行。
12. CUPRAC 在 9/17 个候选中识别到至少一项可能数据，主要集中于 phenolics、ascorbic acid 和 alpha-tocopherol；可作为 secondary coverage 起点，但尚不足以跨全部类别形成统一证据层。
13. 当前历史数据不能支持 formal Top20。
14. 主要缺口是 Tier A 所需方法字段缺失、L-ORAC 和 carotenoid 原始数据薄弱、special-case QC 缺失，以及不同 protocol 对同一化合物产生大幅差异。
15. 统一复测优先级最高的是 carotenoids（lycopene、beta-carotene、lutein）、EGCG/epicatechin/kaempferol、resveratrol、ferulic acid 与 sulforaphane；tocopherols需先完成原文方法复核，再决定是否复测。

## 6. CUPRAC coverage

CUPRAC 仅做 coverage pilot，不排名。Apak et al. 的比较研究覆盖了 catechins、quercetin、phenolic acids、ascorbic acid 和 alpha-tocopherol 等多个本项目候选，证明它对 hydrophilic/lipophilic ET/reducing-power 补充具有价值。但 carotenoids、gamma-tocopherol、resveratrol、chlorogenic acid、lutein、lycopene 和 sulforaphane 的可比覆盖在本轮不足。正式纳入前仍需逐记录审查 assay conditions 和 molar unit。

## 7. 结论与停止点

候选范围可以冻结，但严格的历史 ORAC 排名目前不可执行。最有信息量的 pilot 结果不是一个名次，而是发现：已发表的常用 ORAC 数值在 frozen Tier A rubric 下全部降为 Tier B。下一步应先完成关键全文的二次方法抽取，并为高优先缺口设计统一 H-ORAC/L-ORAC 复测计划；本轮不扩展到正式 Top20、Stage 2 或靶点提取。
