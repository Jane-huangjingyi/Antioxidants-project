# Phase 3A：Polyphenols–Flavonoids Top20 Ranking v1.0

## 1. Question

本阶段回答：在正常膳食来源、结构明确并通过 Phase 3 candidate-level lock 的 flavonoids 中，哪些化合物在方法学可接受的历史 AAPH–fluorescein–Trolox H-ORAC-FL 文献中具有较高的 literature-derived chemical antioxidant capacity？这里的数值描述 AAPH-derived radical oxidation of fluorescein / peroxyl-radical-related chain-breaking capacity，不代表人体抗氧化疗效、生物利用度、临床获益或跨类别总体价值。

## 2. Universe

输入为 `Antioxidant_Class_Candidate_Master.csv` 中 `analysis_panel == Polyphenols - Flavonoids` 的完整 **59 candidates**，覆盖 Flavan-3-ols、Flavonols、Flavonol glycosides、Flavones、Flavone glycosides、Flavanones、Flavanone glycosides、Anthocyanidins、Anthocyanins、Isoflavones 和 Isoflavone glycosides。候选生成不使用 ORAC 数值反向筛选。

## 3. Eligibility lock

完成 59 个候选的 identity/form/food-source second review：**57 eligible_for_ranking、2 hold、0 excluded**。Chrysin 和 baicalein 延续 Phase 2 unresolved 状态，因为普通膳食暴露及候选级来源仍不足以冻结；它们即使存在 ORAC 数据也不进入当前排名。当前 lock 是第一研究者审阅结果，正式冻结前仍需第二研究者复核。

## 4. Literature coverage

Evidence master 共 **94 rows**：Tier A=0、B1=53、B2=5、C=7、X=29。按 compound 计，共 **25 个候选至少有一条 A/B1 数值**，足以在不降低标准的情况下形成 Top20。B1 包括既有项目已经审计的 Ou、Tabart、Zhang、Ishimoto、Rothe、Dávalos 等研究，以及 Žuvela 等 2019 年原始实验的 Table 3；该研究报告 `ln(ORAC)`，本项目用 `exp(reported ln(ORAC))` 可逆地恢复 molar ORAC，并保留原值与公式。β-phycoerythrin、HORAC、figure-only、非目标 probe 和不可转换数据不进入主排名。

Anthocyanidins/anthocyanins 的精确历史值均保留为 B2，因为原文没有充分处理 absorbance/fluorescence overlap、inner-filter effect、self-fluorescence、quenching 与 pH transformation；因此本版不能把其榜单缺席解释为低 antioxidant capacity。

## 5. Final Top20

| Rank | Compound | Subclass | Median H-ORAC | n | Confidence | Main caveat |
|---:|---|---|---:|---:|---|---|
| 1 | Epicatechin | Flavan-3-ols | 9.370 | 5 | High | 历史 protocols 非完全一致 |
| 2 | Catechin | Flavan-3-ols | 8.450 | 6 | Moderate | 跨研究异质性高 |
| 3 | Gallocatechin | Flavan-3-ols | 8.300 | 1 | Low | single-study |
| 4 | Apigenin | Flavones | 8.207 | 2 | Moderate | 两项 protocol 来源 |
| 5 | Isorhamnetin | Flavonols | 8.070 | 1 | Low | single-study |
| 6 | Naringenin | Flavanones | 8.040 | 3 | High | 中度方法差异 |
| 7 | Kaempferol | Flavonols | 7.697 | 4 | High | 中度方法差异 |
| 8 | Daidzein | Isoflavones | 7.660 | 1 | Low | single-study |
| 9 | Eriodictyol | Flavanones | 7.486 | 1 | Low | single-study |
| 10 | Hesperetin | Flavanones | 7.457 | 2 | Moderate | 两项 protocol 来源 |
| 11 | Genistein | Isoflavones | 7.320 | 3 | High | 中度方法差异 |
| 12 | Quercetin | Flavonols | 7.226 | 6 | Moderate | 跨研究范围 4.2–16.62 |
| 13 | Fisetin | Flavonols | 7.092 | 1 | Low | single-study |
| 14 | Epicatechin gallate | Flavan-3-ols | 6.750 | 1 | Low | single-study |
| 15 | Rutin | Flavonol glycosides | 6.705 | 2 | Moderate | 两项 protocol 来源 |
| 16 | Kaempferol 3-O-glucoside | Flavonol glycosides | 6.600 | 1 | Low | single-study |
| 17 | Quercitrin | Flavonol glycosides | 6.470 | 1 | Low | single-study |
| 18 | Myricitrin | Flavonol glycosides | 6.000 | 1 | Low | single-study |
| 19 | Hesperidin | Flavanone glycosides | 4.500 | 1 | Low | single-study |
| 20 | Isoquercitrin | Flavonol glycosides | 4.500 | 1 | Low | single-study |

排序值为 compound-level median mol TE/mol compound；未取最大值。n≥4 报告 IQR，完整 min/max/IQR 和 provenance record IDs 见正式 CSV。并列值未被人为拆分为伪精确差异。

## 6. Evidence confidence

Top20 中 High=4、Moderate=5、Low=11；11 个为 single-study estimates。Catechin 与 quercetin 虽分别有 6 条记录，但因跨研究差异超过两倍而降为 Moderate。Evidence confidence 不与 H-ORAC magnitude 合成总分。

## 7. Subclass distribution

Top20 构成为：Flavan-3-ols 4、Flavonols 4、Flavonol glycosides 5、Flavones 1、Flavanones 3、Flavanone glycosides 1、Isoflavones 2。Anthocyanidins、Anthocyanins、Flavone glycosides 和 Isoflavone glycosides 为 0。该分布只用于识别 coverage bias，不设 subclass quota，也不修改名次。

## 8. Major changes vs historical H-ORAC ranking

旧榜是跨 phenolic subclasses 的 provisional Top20，当前榜限定为完整 59-candidate flavonoid universe，二者不构成同一母体的直接版本替换。历史榜中的 epicatechin、catechin、quercetin、quercitrin、rutin 和 genistein继续进入本榜；luteolin 因扩展候选后低于当前 Top20 cutoff 而退出。新进入的 14 个 flavonoids主要来自完整 subclass universe 与新增原始文献覆盖。旧榜中的 phenolic acids、stilbenes 和 other phenolics 因本轮 class boundary 而退出，不应解释为 antioxidant capacity 下降。

## 9. Bias and missingness

文献覆盖明显集中于 tea flavan-3-ols、common flavonols 及少数 aglycones；glycosides覆盖较少，flavone/isoflavone glycosides尤其不足。Anthocyanins受 probe optical QC 系统性限制。29 个 X 代表未找到可提取合格记录，不代表低 antioxidant capacity。2019 年 36-flavonoid研究一次性贡献大量 B1，造成 single-laboratory coverage concentration；其记录仍分别计为 compound records，但共享同一 protocol，不能被解释为 36 个独立 laboratory replications。

## 10. What this ranking means

它是 **Polyphenols–Flavonoids class-specific、literature-derived、H-ORAC-FL-based、provisional v1.0 ranking**，用于比较方法学可接受的历史化学容量数据，并同时显示证据深度和异质性。

## 11. What this ranking does NOT mean

它不是 global antioxidant ranking、人体 efficacy ranking、bioavailability ranking、clinical ranking、disease-prevention ranking 或实验转化优先级。高排名也不等于证据更稳健；gallocatechin、isorhamnetin等高位候选仍只有单研究证据。

## 12. Readiness for Global Top Overview

本阶段已提供一个可审计的 flavonoid class-specific输出，但尚不能建立 Global Top Overview。按照冻结规则，至少还需完成 Phase 3B Phenolic acids/conjugates Top-N，且不同 class 的 primary constructs只能并列展示，不能构造伪统一 global score。

## 13. Next step

建议研究者先对 57 个 eligibility lock 和所有 rank-changing values 做第二人复核，重点核验 Žuvela 2019 的 `ln(ORAC)` 反变换、quercetin/catechin高异质性、以及 glycoside form。审核通过后进入 Phase 3B Phenolic acids/conjugates Top-N；本阶段不启动其他类别、Global Overview、target mapping 或机制扩展。

## Sync to ChatGPT

**A. Initial universe N：**59。**B. Final ranking eligible N：**57；hold=2；excluded=0。**C. Evidence rows：**A=0、B1=53、B2=5、C=7、X=29；25 compounds有A/B1。**D. Top20：**epicatechin、catechin、gallocatechin、apigenin、isorhamnetin、naringenin、kaempferol、daidzein、eriodictyol、hesperetin、genistein、quercetin、fisetin、epicatechin gallate、rutin、kaempferol 3-O-glucoside、quercitrin、myricitrin、hesperidin、isoquercitrin。**E. Top5：**epicatechin、catechin、gallocatechin、apigenin、isorhamnetin。**F. Confidence：**High=4、Moderate=5、Low=11。**G. Single-study：**11。**H. Subclass distribution：**Flavan-3-ols=4、Flavonols=4、Flavonol glycosides=5、Flavones=1、Flavanones=3、Flavanone glycosides=1、Isoflavones=2。**I. Historical comparison：**6 个旧榜 flavonoids保留；luteolin退出；其余退出多由 class boundary变化导致；14个新入榜。**J. Important missing：**anthocyanidins/anthocyanins、flavone glycosides、isoflavone glycosides及多种rare dietary flavonoids。**K. Bias：**tea/common-flavonoid publication density、single-laboratory coverage concentration、anthocyanin optical QC、aglycone优先。**L. Unresolved：**Tier A仍为0；Chrysin/baicalein food gate未冻结；Zotero API未运行，新增来源标为 `pending_local_import`。**M. Recommended Phase 3B：**沿用相同 eligibility lock、A/B1/B2/C/X、record-level provenance和median/confidence规则处理 Phenolic acids/conjugates。
