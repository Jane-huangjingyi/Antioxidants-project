# Global Top Overview Schema Pilot v0.1

**日期：2026-09-18｜状态：Schema pilot completed; global comparison not completed**

## 1. Purpose and boundary

本文件验证一个可扩展的 Global Top Overview 数据结构。本轮只纳入已完成的两个 H-ORAC-FL class-specific outputs：Flavonoids Top20 和 Phenolic acids / conjugates Top available 18，共 38 行。表格并列展示 class-specific rank、原始 primary construct、evidence depth、confidence、stability 与 caveat；不创建 global rank、global score、z-score、weighted score 或 composite antioxidant score，也不按 H-ORAC 数值把两类重新混排。

## 2. Percentile definition

`within_class_percentile = 100 × (within_class_N_rankable − within_class_rank + 1) / within_class_N_rankable`。Rank 1 固定为 100；最低类内名次仍保留大于 0 的百分位。该字段只反映候选在自己类别及其已获得 A/B1 的 rankable universe 中的位置。Flavonoid Rank 1/25 与 phenolic-acid Rank 1/18 都可为 100，但这不表示二者 chemical antioxidant magnitude 相等或可直接比较。

## 3. Evidence stability definition

`Stable` 要求多项独立 eligible records、低或中等异质性、身份清楚，并达到较深证据量；`Moderately stable` 表示至少两项记录，但仍有 protocol differences、Moderate confidence 或一定异质性；`Fragile` 表示单研究、高异质性或未解决的 identity/assay concern。Stability 描述 estimate robustness；confidence 描述现有证据等级与深度，二者不与 primary value 合成总分。

## 4. Flavonoids Top20

| Compound | Analysis panel | Class rank | Rankable N | Percentile | Primary construct | Primary value | n | Confidence | Stability | Major caveat |
|---|---|---:|---:|---:|---|---:|---:|---|---|---|
| Epicatechin | Polyphenols - Flavonoids | 1 | 25 | 100.0 | H-ORAC-FL | 9.37 | 5 | High | Stable | Broadly comparable, non-identical historical protocols. |
| Catechin | Polyphenols - Flavonoids | 2 | 25 | 96.0 | H-ORAC-FL | 8.45 | 6 | Moderate | Fragile | High cross-study dispersion; confidence not upgraded. |
| Gallocatechin | Polyphenols - Flavonoids | 3 | 25 | 92.0 | H-ORAC-FL | 8.3 | 1 | Low | Fragile | Single-study estimate. |
| Apigenin | Polyphenols - Flavonoids | 4 | 25 | 88.0 | H-ORAC-FL | 8.207 | 2 | Moderate | Moderately stable | Broadly comparable, non-identical historical protocols. |
| Isorhamnetin | Polyphenols - Flavonoids | 5 | 25 | 84.0 | H-ORAC-FL | 8.07 | 1 | Low | Fragile | Single-study estimate. |
| Naringenin | Polyphenols - Flavonoids | 6 | 25 | 80.0 | H-ORAC-FL | 8.04 | 3 | High | Stable | Broadly comparable, non-identical historical protocols. |
| Kaempferol | Polyphenols - Flavonoids | 7 | 25 | 76.0 | H-ORAC-FL | 7.697 | 4 | High | Stable | Broadly comparable, non-identical historical protocols. |
| Daidzein | Polyphenols - Flavonoids | 8 | 25 | 72.0 | H-ORAC-FL | 7.66 | 1 | Low | Fragile | Single-study estimate. |
| Eriodictyol | Polyphenols - Flavonoids | 9 | 25 | 68.0 | H-ORAC-FL | 7.486 | 1 | Low | Fragile | Single-study estimate. |
| Hesperetin | Polyphenols - Flavonoids | 10 | 25 | 64.0 | H-ORAC-FL | 7.457 | 2 | Moderate | Moderately stable | Broadly comparable, non-identical historical protocols. |
| Genistein | Polyphenols - Flavonoids | 11 | 25 | 60.0 | H-ORAC-FL | 7.32 | 3 | High | Stable | Broadly comparable, non-identical historical protocols. |
| Quercetin | Polyphenols - Flavonoids | 12 | 25 | 56.0 | H-ORAC-FL | 7.226 | 6 | Moderate | Fragile | High cross-study dispersion; confidence not upgraded. |
| Fisetin | Polyphenols - Flavonoids | 13 | 25 | 52.0 | H-ORAC-FL | 7.092 | 1 | Low | Fragile | Single-study estimate. |
| Epicatechin gallate | Polyphenols - Flavonoids | 14 | 25 | 48.0 | H-ORAC-FL | 6.75 | 1 | Low | Fragile | Single-study estimate. |
| Rutin | Polyphenols - Flavonoids | 15 | 25 | 44.0 | H-ORAC-FL | 6.705 | 2 | Moderate | Moderately stable | Broadly comparable, non-identical historical protocols. |
| Kaempferol 3-O-glucoside | Polyphenols - Flavonoids | 16 | 25 | 40.0 | H-ORAC-FL | 6.6 | 1 | Low | Fragile | Single-study estimate. |
| Quercitrin | Polyphenols - Flavonoids | 17 | 25 | 36.0 | H-ORAC-FL | 6.47 | 1 | Low | Fragile | Single-study estimate. |
| Myricitrin | Polyphenols - Flavonoids | 18 | 25 | 32.0 | H-ORAC-FL | 6.0 | 1 | Low | Fragile | Single-study estimate. |
| Hesperidin | Polyphenols - Flavonoids | 19 | 25 | 28.0 | H-ORAC-FL | 4.5 | 1 | Low | Fragile | Single-study estimate. |
| Isoquercitrin | Polyphenols - Flavonoids | 20 | 25 | 24.0 | H-ORAC-FL | 4.5 | 1 | Low | Fragile | Single-study estimate. |

## 5. Phenolic acids / conjugates Top available 18

| Compound | Analysis panel | Class rank | Rankable N | Percentile | Primary construct | Primary value | n | Confidence | Stability | Major caveat |
|---|---|---:|---:|---:|---|---:|---:|---|---|---|
| Rosmarinic acid | Polyphenols - Phenolic acids / conjugates | 1 | 18 | 100.0 | H-ORAC-FL | 18.72 | 1 | Low | Fragile | Single-study estimate. |
| Caffeic acid | Polyphenols - Phenolic acids / conjugates | 2 | 18 | 94.4 | H-ORAC-FL | 8.26 | 3 | Moderate | Fragile | High historical dispersion; confidence not upgraded. |
| Gentisic acid | Polyphenols - Phenolic acids / conjugates | 3 | 18 | 88.9 | H-ORAC-FL | 8.137 | 2 | Moderate | Moderately stable | Broadly comparable, non-identical historical protocols. |
| Protocatechuic acid | Polyphenols - Phenolic acids / conjugates | 4 | 18 | 83.3 | H-ORAC-FL | 7.36 | 2 | Moderate | Fragile | High historical dispersion; confidence not upgraded. |
| Vanillic acid | Polyphenols - Phenolic acids / conjugates | 5 | 18 | 77.8 | H-ORAC-FL | 7.24 | 2 | Moderate | Fragile | High historical dispersion; confidence not upgraded. |
| Sinapic acid | Polyphenols - Phenolic acids / conjugates | 6 | 18 | 72.2 | H-ORAC-FL | 5.99 | 2 | Moderate | Fragile | High historical dispersion; confidence not upgraded. |
| Syringic acid | Polyphenols - Phenolic acids / conjugates | 7 | 18 | 66.7 | H-ORAC-FL | 5.12 | 2 | Moderate | Fragile | High historical dispersion; confidence not upgraded. |
| p-Coumaric acid | Polyphenols - Phenolic acids / conjugates | 8 | 18 | 61.1 | H-ORAC-FL | 5.01 | 4 | High | Stable | Broadly comparable, non-identical historical protocols. |
| Ferulic acid | Polyphenols - Phenolic acids / conjugates | 9 | 18 | 55.6 | H-ORAC-FL | 4.032 | 4 | Moderate | Fragile | High historical dispersion; confidence not upgraded. |
| 4,5-Dicaffeoylquinic acid | Polyphenols - Phenolic acids / conjugates | 10 | 18 | 50.0 | H-ORAC-FL | 3.7 | 1 | Low | Fragile | Single-study estimate. |
| Cryptochlorogenic acid | Polyphenols - Phenolic acids / conjugates | 11 | 18 | 44.4 | H-ORAC-FL | 3.54 | 1 | Low | Fragile | Single-study estimate. |
| 3,4-Dicaffeoylquinic acid | Polyphenols - Phenolic acids / conjugates | 12 | 18 | 38.9 | H-ORAC-FL | 3.26 | 1 | Low | Fragile | Single-study estimate. |
| 4-Hydroxybenzoic acid | Polyphenols - Phenolic acids / conjugates | 13 | 18 | 33.3 | H-ORAC-FL | 2.734 | 2 | Moderate | Moderately stable | Broadly comparable, non-identical historical protocols. |
| Chlorogenic acid | Polyphenols - Phenolic acids / conjugates | 14 | 18 | 27.8 | H-ORAC-FL | 2.21 | 1 | Low | Fragile | Single-study estimate. Ou 2001 generic chlorogenic mapping remains Tier X and is not pooled. |
| 3,5-Dicaffeoylquinic acid | Polyphenols - Phenolic acids / conjugates | 15 | 18 | 22.2 | H-ORAC-FL | 2.13 | 1 | Low | Fragile | Single-study estimate. |
| Ellagic acid | Polyphenols - Phenolic acids / conjugates | 16 | 18 | 16.7 | H-ORAC-FL | 1.832 | 1 | Low | Fragile | Single-study estimate. |
| Neochlorogenic acid | Polyphenols - Phenolic acids / conjugates | 17 | 18 | 11.1 | H-ORAC-FL | 1.47 | 1 | Low | Fragile | Single-study estimate. |
| Gallic acid | Polyphenols - Phenolic acids / conjugates | 18 | 18 | 5.6 | H-ORAC-FL | 1.25 | 3 | Moderate | Fragile | High historical dispersion; confidence not upgraded. |

Phase 3B 的 4 个 candidate holds 不在 18-row overview 中，因为它们没有进入 class ranking；Ou 2001 generic chlorogenic record 继续保持 Tier X，未并入 chlorogenic-acid primary value。高异质性候选维持 provisional confidence，没有在本轮重新裁决。

## 6. Head-to-head class leaders

下表只把两个 panel 各自 Top5 并列展示，便于查看数据结构；不回答“谁整体更强”。

| Compound | Analysis panel | Class rank | Rankable N | Percentile | Primary construct | Primary value | n | Confidence | Stability | Major caveat |
|---|---|---:|---:|---:|---|---:|---:|---|---|---|
| Epicatechin | Polyphenols - Flavonoids | 1 | 25 | 100.0 | H-ORAC-FL | 9.37 | 5 | High | Stable | Broadly comparable, non-identical historical protocols. |
| Catechin | Polyphenols - Flavonoids | 2 | 25 | 96.0 | H-ORAC-FL | 8.45 | 6 | Moderate | Fragile | High cross-study dispersion; confidence not upgraded. |
| Gallocatechin | Polyphenols - Flavonoids | 3 | 25 | 92.0 | H-ORAC-FL | 8.3 | 1 | Low | Fragile | Single-study estimate. |
| Apigenin | Polyphenols - Flavonoids | 4 | 25 | 88.0 | H-ORAC-FL | 8.207 | 2 | Moderate | Moderately stable | Broadly comparable, non-identical historical protocols. |
| Isorhamnetin | Polyphenols - Flavonoids | 5 | 25 | 84.0 | H-ORAC-FL | 8.07 | 1 | Low | Fragile | Single-study estimate. |
| Rosmarinic acid | Polyphenols - Phenolic acids / conjugates | 1 | 18 | 100.0 | H-ORAC-FL | 18.72 | 1 | Low | Fragile | Single-study estimate. |
| Caffeic acid | Polyphenols - Phenolic acids / conjugates | 2 | 18 | 94.4 | H-ORAC-FL | 8.26 | 3 | Moderate | Fragile | High historical dispersion; confidence not upgraded. |
| Gentisic acid | Polyphenols - Phenolic acids / conjugates | 3 | 18 | 88.9 | H-ORAC-FL | 8.137 | 2 | Moderate | Moderately stable | Broadly comparable, non-identical historical protocols. |
| Protocatechuic acid | Polyphenols - Phenolic acids / conjugates | 4 | 18 | 83.3 | H-ORAC-FL | 7.36 | 2 | Moderate | Fragile | High historical dispersion; confidence not upgraded. |
| Vanillic acid | Polyphenols - Phenolic acids / conjugates | 5 | 18 | 77.8 | H-ORAC-FL | 7.24 | 2 | Moderate | Fragile | High historical dispersion; confidence not upgraded. |

## 7. Cross-Class Comparability Matrix

本轮定义 16 个比较维度：6 个在使用共同单位或共同证据 rubric 时可较直接比较，5 个只能作 profile comparison，5 个不得直接数值混排。Dietary intake、study count、evidence confidence、human evidence、direct-target tier 与 safety/prooxidant status 可在定义一致时并列；within-class percentile、mechanism domains、bioavailability、experimental tractability 和 evidence stability 只用于 profile；H-ORAC、L-ORAC、singlet-oxygen quenching、KEAP1/NRF2 evidence 与 mineral-cofactor relevance 必须保留各自 construct。详细规则见 `archive/history/2026-09-18/superseded_outputs/2026-09-18_Cross_Class_Comparability_Matrix_v0.1.csv`。

## 8. Missingness audit

Identity、class-specific rank、primary construct/value、eligible study count、confidence、single-study、heterogeneity、caveat 和 provenance 已齐全。Direct chemical antioxidant profile 可由现有 H-ORAC-FL 字段表达。以下字段尚未按统一 protocol 系统审阅，统一标记为 `Not reviewed` 或 `NA`：quantitative dietary exposure、exposure quality、bioavailability/PK、human evidence、endogenous-defense mechanisms、lipid-phase activity、singlet-oxygen activity、NRF2/GSH/GPX、SOD/CAT、NOX/mitochondrial ROS、ferroptosis/lipid profile、direct-target tier、safety/prooxidant context 和 experimental tractability。`Not reviewed` 不得改写为 `No evidence`。

## 9. Readiness assessment

1. **当前是否可以正式做 Global Top Overview？** 数据结构可用于 pilot 并列展示，但不能宣称已经完成正式 Global Overview。
2. **哪些字段齐全？** 两类的 identity、within-class rank/percentile、primary H-ORAC-FL construct/value、evidence depth、confidence、heterogeneity、stability、assay/identity caveat 和 provenance 齐全。
3. **哪些字段缺失？** 暴露、PK、人体、机制、target、安全与实验可开发性尚未系统审阅。
4. **是否需要 non-H-ORAC class？** 是。当前两个输入都是 polyphenol subclasses，并共享 H-ORAC-based construct，尚不能验证 schema 对真正不同 primary constructs 的适配性。至少完成 Vitamins 或 Carotenoids 后才能测试。
5. **最大科学风险是什么？** 把相同的类内 percentile 或 evidence category误读为跨 construct 的 antioxidant magnitude，或因两个现有类别都使用 H-ORAC 而错误认为未来所有类别都可用相同数值轴。

## 10. Recommended next non-H-ORAC test class

建议先执行 **Carotenoids ranking**，因为它能直接压力测试 singlet-oxygen/lipid-phase primary construct、光学干扰、溶解与聚集问题，并明确证明 overview 必须保留原始 class-specific unit，而不能退回 ORAC 单轴。Vitamins 类别混合 vitamin C 与 tocopherol/tocotrienol，内部还需要 H/L 与具体 construct 分层，作为首个 schema stress test 的解释复杂度更高。本建议不等于开始执行该排名。

## 11. Human-review status

本轮没有触发新的 candidate adjudication，也未修改现有排名。Phase 3B 的 Feruloylquinic acid、generic p-Coumaroylquinic acid、2,3-Dihydroxybenzoic acid、3,4,5-Trimethoxybenzoic acid、Ou 2001 generic chlorogenic mapping 与高异质性事项继续按 `data/class_specific_antioxidant/Human_Review_Log.csv` 保持 pending；overview 仅继承现有 identity risk、stability 与 caveat。

## Sync to ChatGPT

**A. rows included：**38。**B. classes included：**Flavonoids Top20 与 Phenolic acids / conjugates Top available 18。**C. fields complete：**identity、class rank/percentile/status、H-ORAC-FL construct/value/unit、n、confidence、single-study、heterogeneity、identity/assay risk、depth、stability、caveat、provenance。**D. fields missing：**quantitative exposure、PK、human、mechanism、target、安全和 tractability。**E. comparability dimensions：**6 directly comparable with shared definitions，5 profile comparable。**F. non-comparable dimensions：**H-ORAC、L-ORAC、singlet-oxygen quenching、KEAP1/NRF2、mineral cofactor relevance。**G. stability distribution：**Stable=5、Moderately stable=5、Fragile=28。**H. class leaders：**Flavonoids 为 epicatechin、catechin、gallocatechin、apigenin、isorhamnetin；phenolic acids 为 rosmarinic、caffeic、gentisic、protocatechuic、vanillic acid。**I. schema risks：**percentile 被误读为 magnitude、Not reviewed 被误读为 no evidence、两个 H-ORAC panels 无法验证跨 construct 适配性。**J. formal Global Overview ready：**否；schema pilot ready。**K. recommended next non-H-ORAC class：**Carotenoids。**L. human-review item triggered：**无新增；继承 Phase 3B pending items。


## Non-H-ORAC stress test

Carotenoids 是第一个使用 direct singlet-oxygen `kq` 而不是 H-ORAC-FL 的 panel。`Global_Top_Overview_Master_v0.2.csv` 证明既有 schema 可保存不同 primary construct、value 与 unit；within-class percentile 仍然只依赖类内 rank，因此可工作；confidence 和 stability 也仍由证据深度、异质性与 identity/assay risk 产生，不要求共同 assay。需要修订的是 comparability 解释：primary raw value 与 primary unit 必须明确标记为 **not directly comparable across classes**，而 percentile 只允许并列展示，不能解释为效应大小等距。此次 stress test 进一步证明无法建立 unified antioxidant score。Carotenoid organic-solvent `kq`、polyphenol H-ORAC-FL、未来 lipid-phase 或 causal regulatory evidence 应保留各自 construct，再通过 shared translational fields 做 profile comparison。

## Same parent class, different constructs — stress test II

Phase 3D 证明同一 parent class 也可能需要不同 primary constructs。`Vitamins / vitamin-like antioxidants` 下，Vitamin C aqueous 使用 audited H-ORAC-FL，Vitamin E lipid-phase 使用 peroxyl-radical chain-breaking `k_inh`。因此 v0.3 新增 `analysis_subpanel`，正式层级为 `parent_class → analysis_panel → analysis_subpanel`。rank、rankable N 与 percentile 必须在 mechanistically coherent ranking subpanel 内计算。研究者已确认不生成 Vitamins parent-class percentile；L-ascorbic acid 是 aqueous subpanel 唯一 eligible candidate，因此 percentile 为 `NA` 并标记 `single eligible candidate / percentile not informative`，而不是机械赋值 100%。Vitamin E 的 percentile 在八个 vitamers 内计算。该测试进一步确认 Global Overview 是结构化并列展示，不是跨 construct 数值榜。
