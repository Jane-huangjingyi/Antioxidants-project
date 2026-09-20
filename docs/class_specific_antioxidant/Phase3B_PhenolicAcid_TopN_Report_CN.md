# Phase 3B：Polyphenols–Phenolic acids / conjugates Top-N v1.0

**版本：v1.0｜日期：2026-09-18｜状态：provisional / literature-derived / Top available**

## 1. Question

本阶段回答：在正常膳食来源、结构明确并通过候选级锁定的 phenolic acids / conjugates 中，哪些化合物在方法学可接受的历史 H-ORAC-FL 文献中具有较高的 literature-derived chemical antioxidant capacity？主构念限定为 AAPH 引发的 fluorescein 氧化、以 Trolox 为参照的水相 ORAC-FL，并以 `mol TE/mol compound` 表示。该结果不回答人体抗氧化疗效、临床获益、生物利用度或最终实验优先级。

## 2. Universe

输入为 `data/candidate_universe/Antioxidant_Class_Candidate_Master.csv` 中 `analysis_panel == "Polyphenols - Phenolic acids / conjugates"` 的全部 29 个候选，而不是从已有高 ORAC 化合物反向生成名单。其构成为 Hydroxybenzoic acids 9 个、Hydroxycinnamic acids 7 个、Caffeoylquinic and related acids 8 个、Other defined phenolic conjugates 5 个。候选生成与 ORAC 数值、论文数量和期刊影响因子无关。

## 3. Eligibility lock

29 个候选中 25 个进入 `eligible_for_ranking`，4 个进入 `hold`，无候选被静默排除。`Feruloylquinic acid` 未指定酰基位置且缺 CID/InChIKey；泛称 `p-Coumaroylquinic acid` 未锁定 positional isomer；`2,3-Dihydroxybenzoic acid` 的候选特异正常食物来源与 dietary-parent 状态需复核；`3,4,5-Trimethoxybenzoic acid` 缺少游离酚羟基，其 phenolic-space membership 和 food gate 需研究者裁决。**需要研究者人工确认，暂停这些候选的排名决定。**其余候选沿用 Phase 2 已冻结身份和食物来源，但正式发布前仍需第二研究者完成 candidate-specific source 复核。

## 4. Literature coverage

证据主表含 47 行：Tier A=0、B1=34、B2=1、C=0、X=12。记录数是 record level；候选层面有 18 个化合物至少具有 1 条 A/B1，可进入当前探索性 class ranking。B1 来自 original pure-compound ORAC-FL studies，保留 DOI/PMID、exact location、原值、原单位、换算、independent experiment ID 和 assay metadata。2022 年同一 phenolic-acid comparison study 覆盖 10 个化合物，是明显的 single-laboratory coverage concentration；同一研究中的两个浓度被合并为一个 through-origin slope，并只计一个独立实验，避免伪重复。

## 5. Final Top-N

仅有 18 个候选达到 A/B1 最低要求，因此本阶段输出 **Top available 18**，不使用 Top20 名称，也不降低标准补足名额。

| Rank | Compound | Median H-ORAC | n | Confidence | Heterogeneity |
|---:|---|---:|---:|---|---|
| 1 | Rosmarinic acid | 18.720 | 1 | Low | not estimable |
| 2 | Caffeic acid | 8.260 | 3 | Moderate | high |
| 3 | Gentisic acid | 8.137 | 2 | Moderate | moderate |
| 4 | Protocatechuic acid | 7.360 | 2 | Moderate | high |
| 5 | Vanillic acid | 7.240 | 2 | Moderate | high |
| 6 | Sinapic acid | 5.990 | 2 | Moderate | high |
| 7 | Syringic acid | 5.120 | 2 | Moderate | high |
| 8 | p-Coumaric acid | 5.010 | 4 | High | moderate |
| 9 | Ferulic acid | 4.032 | 4 | Moderate | high |
| 10 | 4,5-Dicaffeoylquinic acid | 3.700 | 1 | Low | not estimable |
| 11 | Cryptochlorogenic acid | 3.540 | 1 | Low | not estimable |
| 12 | 3,4-Dicaffeoylquinic acid | 3.260 | 1 | Low | not estimable |
| 13 | 4-Hydroxybenzoic acid | 2.734 | 2 | Moderate | moderate |
| 14 | Chlorogenic acid | 2.210 | 1 | Low | not estimable |
| 15 | 3,5-Dicaffeoylquinic acid | 2.130 | 1 | Low | not estimable |
| 16 | Ellagic acid | 1.832 | 1 | Low | not estimable |
| 17 | Neochlorogenic acid | 1.470 | 1 | Low | not estimable |
| 18 | Gallic acid | 1.250 | 3 | Moderate | high |

这里的“较高”只能表述为“在纳入的历史 ORAC-FL 文献中报告值较高”。Rosmarinic acid 位居首位但只有一项独立 B1，应视为 single-study estimate；它不能被描述为“最强抗氧化剂”。

## 6. Evidence confidence

High=1、Moderate=9、Low=8。当前没有 Tier A。`p-Coumaric acid` 有 4 项独立 B1 且异质性未超过预设高阈值，因此为 High；Caffeic、Protocatechuic、Vanillic、Sinapic、Syringic、Ferulic 和 Gallic acid 的 `max/min > 2`，即使研究数增加也不能自动升级。**需要研究者人工确认，暂停对这些高异质性候选作正式 confidence 冻结；本阶段仅保留 provisional rank。**

## 7. Subclass distribution

Hydroxybenzoic acids：universe 9、lock eligible 7、A/B1 6、Top available 6；Hydroxycinnamic acids：7、7、4、4；Caffeoylquinic and related acids：8、6、6、6；Other defined phenolic conjugates：5、5、2、2。未设置 subclass quota，分布只用于识别检索和方法偏倚。

## 8. Identity and positional-isomer issues

5-O-CQA、3-O-CQA、4-O-CQA 以及 3,4-/3,5-/4,5-diCQA 被分别保留。Zuo 2021 明确报告各 positional isomer，因此可映射为 B1。Ou 2001 中泛称 “chlorogenic acid” 的 3.14 值没有足够信息唯一映射到本项目 `Chlorogenic acid` 结构，已作为 Tier X 保留而未并入 median。**需要研究者人工确认，暂停该条记录的 isomer mapping。**若未来 supplier/CAS/结构证实为本项目 5-O-CQA，可新增独立 B1 并重算 chlorogenic-acid median。

## 9. Major evidence gaps

Salicylic、o-Coumaric、m-Coumaric、Isoferulic、Chicoric、Caftaric 和 Coutaric acid 未定位到可用于本框架的 molar-convertible original ORAC-FL 值。候选 hold 项也未进入数值检索聚合。Sinapic acid 的一个 figure-only 结果保留为 B2，但不进入排名。缺数据表示 `not measured / insufficiently comparable`，不表示低 chemical capacity。

## 10. Sensitivity analysis

Primary A/B1 情景中 Rosmarinic acid 排名第 1，但 `n≥2 only` 情景将其移除，前列变为 Caffeic、Gentisic、Protocatechuic、Vanillic 和 Sinapic acid。剔除 high-heterogeneity candidates 后，Rosmarinic acid 仍以单研究值居首，随后为 Gentisic、p-Coumaric 和多个单研究 caffeoylquinic compounds，说明“限制异质性”不能替代 evidence-depth 约束。排除 positional-identity 存疑记录不会改变主榜，因为 Ou 2001 的 ambiguous chlorogenic record 原本就未参与聚合。当前前列对 evidence-depth 条件敏感，不能冻结为正式 Top20。

## 11. Bias and missingness

自由 hydroxybenzoic/hydroxycinnamic acids 的文献覆盖主要受 2022 年单实验室 comparison study 和少数 method-comparison papers 驱动；caffeic、ferulic、p-coumaric 被多篇研究覆盖，而 rare acids 多数只是未测。Conjugates 整体少于 free acids；caffeoylquinic positional isomers 的当前覆盖几乎集中在一个研究。food-chemistry popularity 因此同时影响“是否有值”和 confidence，排名不能解释为整个候选空间的无偏抽样。

## 12. What ranking means

本榜是 candidate-locked、identity-resolved、A/B1-only 的 exploratory literature-derived H-ORAC-FL 排名。每个数值可逆向追溯到 evidence ID、independent experiment、original paper、exact table、original value、conversion formula 和 normalized value。

## 13. What ranking does NOT mean

该榜不代表人体抗氧化效果、临床获益、生物利用度、疾病预防、细胞 redox regulation、target evidence 或最终实验价值；也不能与 L-ORAC、DPPH、ABTS、FRAP 或其他类别的 primary construct 直接合并。

## 14. Comparison with historical phenolic ranking

历史 H-ORAC phenolic ranking 混合多个 phenolic subclasses，主要用于早期可行性验证；本阶段从完整 29-candidate phenolic-acid/conjugate universe 重新执行 candidate lock、positional-isomer QC、record-level extraction 和 class-specific aggregation。旧值仅在其 provenance 与当前标准一致时迁移，未按旧名次保留或优先。

## 15. Readiness for Global Top Overview

数据结构已经具备未来 Global Top Overview 所需的 within-class rank、primary metric、confidence、evidence depth、identity risk 和 provenance 字段；科学上仍只能记为 **schema-ready / result-not-ready**。原因是本类只有 18 个 rankable candidates、Tier A=0、8 个 single-study estimates、多个高异质性候选和 5 项人工复核记录。本轮不生成跨类榜单。

## 16. Next step

先由第二研究者裁决 `Human_Review_Log.csv` 的候选身份、food gate 与 chlorogenic mapping，并复核所有 rank-changing conversions。随后针对缺失 acids、single-study Top available candidates 和高异质性 compounds 做 bounded evidence consolidation。达到至少 20 个 A/B1 candidates 或明确接受 Top available 形式后，再审议 Global Top Overview schema；不得直接进入跨类数值混排。

## Sync to ChatGPT

**A. universe N：**29。**B. eligibility lock N：**25 eligible、4 hold、0 excluded。**C. evidence counts：**record-level A=0、B1=34、B2=1、C=0、X=12；candidate-level A/B1=18。**D. Top-N list：**Rosmarinic, Caffeic, Gentisic, Protocatechuic, Vanillic, Sinapic, Syringic, p-Coumaric, Ferulic, 4,5-diCQA, Cryptochlorogenic, 3,4-diCQA, 4-Hydroxybenzoic, Chlorogenic, 3,5-diCQA, Ellagic, Neochlorogenic, Gallic acid。**E. Top5：**Rosmarinic 18.720、Caffeic 8.260、Gentisic 8.137、Protocatechuic 7.360、Vanillic 7.240 mol TE/mol。**F. confidence：**High=1、Moderate=9、Low=8。**G. single-study count：**8。**H. subclass distribution：**6 hydroxybenzoic、4 hydroxycinnamic、6 caffeoylquinic-related、2 other conjugates。**I. positional-isomer issues：**generic chlorogenic records不得自动映射；一个 Ou 2001 record 为 X。**J. identity issues：**4 个 candidate holds。**K. sensitivity：**Rosmarinic 的第 1 位依赖单研究；n≥2 后前列改变；排除高异质性亦明显改变顺序。**L. cutoff stability：**eligible N=18，不存在可冻结的 Top20 cutoff。**M. bias risks：**single-lab coverage concentration、publication popularity、free-acid overcoverage、conjugate/isomer undercoverage。**N. pending human review：**Feruloylquinic、generic p-Coumaroylquinic、2,3-DHBA、3,4,5-trimethoxybenzoic、Ou 2001 chlorogenic mapping，另有高异质性 confidence 需二审。**O. Global Top Overview readiness：**字段就绪，结果尚未达到正式跨类整合稳定性。

Zotero：沿用的 Ou 2001、Carvalho 2023 已有项目 key；其余正式采用文献标记 `pending_local_import`，未伪造 key。
