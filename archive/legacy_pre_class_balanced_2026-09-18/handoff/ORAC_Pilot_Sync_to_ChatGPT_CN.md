# ORAC Pilot 同步给 ChatGPT/研究者

## A. 候选范围最终定义

主候选限定为正常膳食中天然存在、结构明确、可独立计量并唯一映射 PubChem CID/InChIKey 的原型小分子。顶层 taxonomy 为 phenolic/polyphenolic compounds、vitamins/vitamin-like antioxidants、carotenoids、organosulfur compounds 和少量其他明确食源类别。Phenolic acids 是 phenolic compounds 的 subclass；chemical class、抗氧化功能和 ORAC compatibility 分开建字段。

## B. Pilot compound list

EGCG、catechin、epicatechin、quercetin、kaempferol、gallic acid、caffeic acid、ferulic acid、chlorogenic acid、trans-resveratrol、L-ascorbic acid、alpha-tocopherol、gamma-tocopherol、lycopene、beta-carotene、lutein、sulforaphane，共 17 个。

## C. 各类别数量

Phenolic/polyphenolic 10；vitamin/vitamin-like 3；carotenoid 3；organosulfur 1。

## D. H/L/special-case 分类

预期 H-ORAC 11，L-ORAC 5，noncanonical special-case 1。共有 8 个候选带至少一个 special-case QC flag；special-case 与 H/L arm 可重叠。H/L 未混排。

## E. Tier A 覆盖

正式抽取 11 条原始 ORAC-FL 记录，但 Tier A=0、Tier B=11。Tier B 涉及 catechin、quercetin、gallic acid、caffeic acid、chlorogenic acid、L-ascorbic acid、alpha-tocopherol 和 gamma-tocopherol。其余 9 个为 `not_measured`。主要降级原因是 numerical purity、完整 compound-specific linearity、全部 reading parameters 或 optical/interference QC 未同时满足。

## F. 历史数据能否支持排名

不能。H-ORAC 与 L-ORAC 内部均缺少 Tier A；跨 H/L 更不能排名。两张 distribution 文件因此按 protocol 输出为 coverage diagnostic，没有用 Tier B 值制造主排序。

## G. 最重要的统计结果

同一化合物的 Tier B 数值差异很大：quercetin 7.28 与 16.62 mol TE/mol，caffeic acid 4.37 与 8.26，L-ascorbic acid 0.95 与 0.53。该结果显示 protocol/solvent/kinetic analysis 足以明显改变数值，支持禁止跨论文直接拼接。

## H. 数据最稳定的 compounds

严格意义上没有达到稳定历史排序。Quercetin、caffeic acid 和 L-ascorbic acid 各有两条独立 Tier B，信息量相对最高，但差异也证明需要方法分层或统一复测。Catechin、gallic acid、chlorogenic acid、alpha/gamma-tocopherol 只有单条 Tier B。

## I. 最薄弱的数据

EGCG、epicatechin、kaempferol、ferulic acid、resveratrol、lycopene、beta-carotene、lutein 和 sulforaphane 在本轮没有完成可审计的原始 ORAC-FL record。Carotenoids 的溶解、聚集和光学 QC 是最突出缺口；sulforaphane 的 redox relevance 也不应以低/缺失 ORAC 解释。

## J. CUPRAC coverage

17 个候选中有 9 个识别到至少一个可能的 CUPRAC 数据源，集中于 catechins、quercetin、phenolic acids、ascorbic acid 和 alpha-tocopherol。覆盖足以支持后续 secondary pilot，但不足以跨类别排名，本轮未计算 CUPRAC 名次。

## K. 是否建议进入正式 Top20

不建议。候选 scope 可以冻结，但 ORAC evidence layer 尚不足以产生 formal Chemical Antioxidant Capacity Top20。

## L. 下一步建议

先对 Huang 2002、Dávalos 2004 及候选特异原始论文完成全文级 extraction/adjudication，判断是否能把部分记录升级 Tier A；随后优先统一复测 carotenoids、EGCG/epicatechin/kaempferol、resveratrol、ferulic acid 和 sulforaphane，并分别锁定 H-ORAC 与 L-ORAC SOP。若 Tier A 仍极少，应把正式榜单设计为 harmonized-experiment ranking，而不是 literature-only ranking。

## M. Zotero 新增文献

本轮新增至 `antioxidants project`：

1. Huang et al. 2002, *Development and validation of oxygen radical absorbance capacity assay for lipophilic antioxidants using randomly methylated beta-cyclodextrin as the solubility enhancer*, DOI 10.1021/jf0113732, PMID 11902917, Zotero key `2TR33GW5`。
2. Figueroa et al. 2023, *Exploiting Kinetic Features of ORAC Assay for Evaluation of Radical Scavenging Capacity*, DOI 10.3390/antiox12020505, PMID 36829987, Zotero key `EHLKNP4E`。
3. Apak et al. 2007, *Comparative Evaluation of Various Total Antioxidant Capacity Assays Applied to Phenolic Compounds with the CUPRAC Assay*, DOI 10.3390/12071496, PMID 17909504, Zotero key `BC43GAEF`。

Ou et al. 2001 已存在于 collection，Zotero key `4FIGEV33`，因此未重复导入。
