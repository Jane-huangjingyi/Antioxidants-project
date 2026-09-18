# Antioxidant Functional Factor Atlas：类别内排名阶段汇报

## 1. 当前项目目标

本项目正在构建 **Antioxidant Functional Factor Atlas**：先在化学机制和测定条件可比的类别或亚面板内部完成排名，再进行跨类别 profile 比较，而不是用单一 assay 或统一 raw value 对全部膳食抗氧化因子强行排序。

## 2. 为什么不同类别使用不同方法

| Class / subpanel | Primary construct | 采用原因 |
|---|---|---|
| Flavonoids | H-ORAC-FL | 多数候选可在水相 AAPH–fluorescein 体系中比较 peroxyl-radical-related chain-breaking capacity。 |
| Phenolic acids / conjugates | H-ORAC-FL | 可沿用相同水相构念和 `mol TE/mol compound` 单位，但只在本面板内部解释。 |
| Carotenoids | direct singlet-oxygen quenching `kq` | 长共轭多烯结构的经典功能是 physical quenching of singlet oxygen；当前 primary environment 为 homogeneous organic solvent，仍属 provisional。 |
| Vitamin C — aqueous | H-ORAC-FL | L-ascorbic acid 有两条可比较的水相历史记录；当前只有一个 eligible candidate，不能形成有信息量的 percentile。 |
| Vitamin E — lipid phase | peroxyl-radical chain-breaking `k_inh` | tocopherols/tocotrienols 的核心化学作用是终止脂相 peroxyl-radical chain；L-ORAC 仅作为 secondary profile。 |

这些构念的反应对象、环境和单位不同。H-ORAC-FL、singlet-oxygen `kq` 与 chain-breaking `k_inh` 的 raw values 不具有共同数值尺度，因此不得直接混排或合成总分。

## 3. 当前已完成的排名

| Class / subpanel | Universe / eligible | Ranking output | Top candidates | Confidence note |
|---|---:|---|---|---|
| Flavonoids | 59 universe；57 candidate-lock eligible；25 有 A/B1 | provisional Top20 | Epicatechin；Catechin；Gallocatechin；Apigenin；Isorhamnetin | Top20：High 4、Moderate 5、Low 11；11 个 single-study。 |
| Phenolic acids / conjugates | 29 universe；25 candidate-lock eligible；18 有 A/B1 | Top available 18 | Rosmarinic acid；Caffeic acid；Gentisic acid；Protocatechuic acid；Vanillic acid | High 1、Moderate 9、Low 8；Rosmarinic acid 为 single-study，多个候选异质性高。 |
| Carotenoids | 19 universe；17 candidate-lock eligible；9 有 primary A/B1 | Top available 9 | all-trans-Lycopene；Canthaxanthin；alpha-Carotene；all-trans-beta-Carotene；Zeaxanthin | Moderate 5、Low 4；环境、异构体及聚集风险仍需二审。 |
| Vitamin C — aqueous | 2 universe；1 ranking eligible | all eligible / Top available 1 | L-ascorbic acid | Moderate、Moderately stable；singleton percentile=`NA`。 |
| Vitamin E — lipid phase | 8 universe；8 ranking eligible | Top available 8 | alpha forms；gamma forms；beta forms；delta forms | 8 个均为 Low / Fragile；对应 tocopherol 与 tocotrienol homologues 当前并列。 |

Vitamin E 当前按 `k_inh` 排列：alpha-tocopherol 与 alpha-tocotrienol 并列 rank 1，gamma forms 并列 rank 3，beta forms 并列 rank 5，delta forms 并列 rank 7。该并列关系来自当前 homogeneous kinetic evidence，不代表其膜分配、人体吸收或维生素效价相同。

## 4. What the rankings mean

这些结果是 **class-specific、literature-derived、provisional、assay/construct-specific** 的化学或机制相关排名。它们用于识别各可比面板中的头部候选、证据深度与稳定性，并暴露 single-study、环境依赖、异构体和 assay interference 等问题。

Evidence confidence 的 High / Moderate / Low 反映独立 eligible evidence depth、跨研究异质性，以及身份和实验环境的稳健程度。Confidence 与 antioxidant magnitude 分开报告，不合并成总分；高名次不自动意味着证据更稳定。

## 5. What the rankings do NOT mean

这些排名不等于人体抗氧化效果、临床价值、吸收利用度、疾病预防效果或 final experimental priority，也不能回答不同类别中谁是“最强抗氧化剂”。尤其不能将 H-ORAC-FL、singlet-oxygen `kq` 和 lipid-phase `k_inh` 的 raw values、z-score 或 intake-adjusted values 合并为 global composite ranking。

## 6. Global Overview 当前进度

Global Overview schema 已能够并列展示 within-class rank、within-class/subpanel percentile、primary construct、confidence 和 stability。当前导师版 CSV 共纳入 56 行：Flavonoids 20、Phenolic acids / conjugates 18、Carotenoids 9、Vitamin C 1、Vitamin E 8。Percentile 的分母始终是 mechanistically coherent ranking panel；Vitamin C 因只有一个 eligible candidate 而保留 `NA`，不赋值 100%。该 schema 已适合阶段汇报，但尚不支持正式 global rank。

## 7. 尚未完成的类别

- Polyphenols–Stilbenes / lignans
- Organosulfur compounds
- Betalains / nitrogen-containing phytochemicals
- Other food-derived redox-active phytochemicals
- Antioxidant-related micronutrients / mineral cofactors profile

下一步建议优先处理 **Organosulfur compounds**，用于测试 KEAP1/NRF2、thiol reactivity、endogenous defense 和 causal redox evidence 这类不以直接 chemical scavenging 为核心的 ranking framework；本轮不启动该分析。

## Suggested supervisor update

目前已完成黄酮类、酚酸及其缀合物、类胡萝卜素、维生素 C 水相面板和维生素 E 脂相面板的 provisional 类别内排名。不同类别采用与其主要化学机制相符的 primary construct：多酚使用 H-ORAC-FL，类胡萝卜素使用单线态氧淬灭速率，维生素 E 使用脂质过氧自由基链终止动力学。现阶段已经可以比较各类别内部的头部候选及其证据稳定性，但不同构念的 raw values 不能直接组成跨类别总排名。仍需完成 stilbenes/lignans、有机硫、betalains 等类别；下一阶段建议优先建立 Organosulfur ranking framework。

## Sync to ChatGPT

**A. Included ranking panels：**Flavonoids、Phenolic acids / conjugates、Carotenoids、Vitamin C aqueous、Vitamin E lipid-phase。**B. Compounds shown：**导师 CSV 共 56 个排名行；图展示前三类各 Top5、Vitamin C singleton，以及 Vitamin E rank≤5 的全部并列候选。**C. Current class-specific Top5：**Flavonoids 为 Epicatechin、Catechin、Gallocatechin、Apigenin、Isorhamnetin；Phenolic acids 为 Rosmarinic、Caffeic、Gentisic、Protocatechuic、Vanillic acid；Carotenoids 为 all-trans-Lycopene、Canthaxanthin、alpha-Carotene、all-trans-beta-Carotene、Zeaxanthin；Vitamin E 依次为 alpha、gamma、beta、delta homologous forms。**D. Primary constructs：**H-ORAC-FL、direct singlet-oxygen `kq`、peroxyl-radical `k_inh`。**E. Confidence summary：**Flavonoids 和 phenolic acids 混合 High/Moderate/Low；carotenoids 为 Moderate/Low；Vitamin C Moderate；Vitamin E 全部 Low。**F. Major caveats：**Tier A 缺失、single-study estimates、protocol/environment heterogeneity、identity/aggregation/optical risks，以及 Vitamin E homolog-equivalence evidence。**G. Unfinished classes：**Stilbenes/lignans、Organosulfur、Betalains/nitrogen-containing、other redox-active phytochemicals、micronutrient/mineral-cofactor profile。**H. Recommended next phase：**Organosulfur compounds。**I. Supervisor package ready：**是；仅用于 class-specific 阶段汇报，不构成 global composite ranking。
