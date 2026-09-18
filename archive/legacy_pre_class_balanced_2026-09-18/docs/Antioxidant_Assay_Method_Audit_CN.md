# 抗氧化能力测定方法审计

版本 1.0（2026-09-17）。本审计只讨论 chemical antioxidant capacity，不代表人体抗氧化效果、疾病获益或体内 redox regulation。

## 1. 操作性定义

“抗氧化能力”不是单一物理量。HAT 指抗氧化剂向自由基转移氢原子，速率和化学计量共同决定链终止；ET/SET 指电子转移，结果受氧化还原电位、pH 和溶剂控制；radical scavenging 是结果性描述，可能由 HAT、ET、PCET、加成或其他反应产生。Reducing power 是还原金属/探针的能力，不等同于清除传播自由基。Peroxyl-radical chain-breaking 指截获脂质或水相链式氧化中的 ROO•；metal chelation 通过限制 Fe/Cu 催化氧化发挥预防作用，但也可能改变 assay；lipid oxidation inhibition 同时取决于本征反应性、相分配和界面定位；total radical trapping 关注一个抗氧化剂能捕获多少自由基及其诱导期。上述量不能互换。

本项目将主要 chemical capacity 操作性定义为：在固定 ORAC-FL 条件下，结构明确单体相对于 Trolox 抑制 AAPH 衍生过氧自由基引起的荧光素氧化、并由净 AUC 同时反映抑制程度和持续时间的摩尔等效链终止能力。

## 2. 核心方法比较

### ORAC / ORAC-FL

ORAC 全称 Oxygen Radical Absorbance Capacity；ORAC-FL 使用 fluorescein 取代早期 β-phycoerythrin。AAPH（也写作 ABAP 的相关水溶性偶氮引发剂）热分解产生恒定通量的过氧自由基，后者氧化 fluorescein 使荧光随时间衰减。抗氧化剂延缓衰减。对每孔按时间积分荧光曲线，扣除空白 AUC：`net AUC = AUC_sample − AUC_blank`；在有效线性范围内与 Trolox 标准曲线比较。

ORAC-FL 主要属于竞争性 HAT/过氧自由基链终止 assay；真实反应可能包含 PCET、二级自由基和探针特异动力学，因此不应把 AUC 解释为单一基本速率常数。Trolox 是水溶性 α-tocopherol 类似物和校准参照，不是生理效应标准。对纯化单体，推荐报告 `mol Trolox equivalents per mol compound (mol TE/mol)`；文献确有纯化合物以 µmol TE/µmol compound 或可换算的 µmol TE/mg 报告。后者只有在化合物身份、纯度和分子量明确时才可换算。

ORAC 受 AAPH/fluorescein/Trolox 浓度、缓冲液、pH、温度、孵育、加样顺序、氧、板型/位置、读板间隔、总时间、AUC 截断、空白扣除、样品浓度线性、溶剂、增溶剂、样品自发荧光/内滤效应和降解影响。不同论文即使都写 ORAC，也不能默认合并。

H-ORAC 在水相缓冲液测亲水组分。L-ORAC 通常用 randomly methylated β-cyclodextrin（RMCD）和含有机溶剂的体系增溶脂溶性分子，已有实验室间验证，但其值不与 H-ORAC 天然同标度。只有在同一 radical generator、probe、温度、pH、时间采样、AUC 算法、Trolox 校准、有效浓度范围、溶剂/增溶体系和质量控制下，且用共同 bridging standards 验证批间/实验室偏差后，才可把不同来源纳入同一排名。最佳方案是由一个中心实验室按锁定 SOP 复测全部候选。

跨类别存在技术限制。水溶性多酚适合 H-ORAC；tocopherols 和部分 carotenoids 需要 L-ORAC。Carotenoids 可能溶解不完全、聚集、吸光/荧光干扰，并可通过加成或电子转移而非典型 HAT 反应；tocopherol 的相定位又是其脂质保护能力的重要部分。H-ORAC 与 L-ORAC 可构成平行主轴，但不得把不同增溶环境产生的数值无条件混排。

### DPPH

DPPH• 是持久、有色、体内不存在的氮自由基，常在甲醇/乙醇或其他有机体系于约 515–520 nm 读取脱色。其反应可表现 ET、HAT 或 PCET，受溶剂、pH、氢键、立体可接近性、DPPH 浓度与反应时间强烈影响。体积较大或反应慢的分子可能被低估；样品颜色和浑浊造成光谱干扰。尽管存在 AOAC 指定食品版本，它不提供适用于跨论文纯单体的统一普适标度。正式角色：同一 protocol 下的 secondary mixed-mode/ET reactivity screen。

### ABTS / TEAC

ABTS•+ 是人工生成的自由基阳离子，常用过硫酸盐预生成后在 734 nm 读取脱色。它适用于较宽极性的体系并天然便于 Trolox 等效表达，但不同生成方式、残余氧化剂、溶剂、pH 和读数时间可改变机理与排序；慢反应分子在短 endpoint 被低估。ABTS•+ 不属于生理自由基。正式角色：secondary broad-polarity ET/mixed-mode assay，必须采用预生成自由基和固定 endpoint/kinetic 方案。

### FRAP

FRAP 在 pH 3.6 将 Fe(III)-TPTZ 还原为有色 Fe(II)-TPTZ，并于 593 nm 读取。它是 endpoint reducing-power assay，不是自由基清除或 chain-breaking assay。酸性条件、反应时间、溶解性、金属螯合和样品颜色影响结果；对反应慢、脂溶或某些硫醇化合物响应不足。正式角色：secondary reducing-power axis，不允许用 FRAP 代表总体抗氧化能力。

### CUPRAC

CUPRAC 测 Cu(II)-neocuproine 在近中性条件被还原为 Cu(I)-neocuproine，约 450 nm 读取。相较 FRAP，它对硫醇和经适当增溶的脂溶抗氧化剂更兼容，pH 更接近食品/生物条件；但仍测 reducing power，且 Cu 配位、溶剂和时间影响响应。正式角色：优先 ET 补充方法，若资源有限可在 FRAP 与 CUPRAC 中优先选择 CUPRAC，但保留 FRAP 便于与传统文献对照。

### TRAP

TRAP 通过持续产生的 peroxyl radicals 测总自由基捕获/诱导期，经典实现用氧电极，后来也用 luminol/fluorescent probes。它与 chain-breaking 概念高度相关，可报告 radicals trapped 或 Trolox equivalents，但检测格式众多、计算和基质效应不统一。正式角色：secondary mechanistic confirmation，而非大规模主排序。

### HORAC、TOSC 和 ROS-specific assays

HORAC 关注 Fenton-like/Co(II) 系统中 hydroxyl-radical damage 的避免，常同时反映金属螯合与探针保护，不能纯粹称为 •OH 清除。TOSC 用 KMBA 氧化产生乙烯并以 GC 积分，可区分 peroxyl、hydroxyl 和 peroxynitrite 条件，但专门仪器、生成体系和单位限制跨研究应用。Superoxide assay 必须排除对生成酶的抑制和探针 redox cycling；hydroxyl radical assay 必须区分 chelation 与 scavenging，并优先 EPR/特异产物。它们均作为 supportive mechanism assays。

### Lipid peroxidation inhibition

脂质体、LDL、乳液或油脂氧化更接近真实食品脂相中的功能保护，应采用 lag phase、propagation rate、oxygen uptake、conjugated dienes 或经验证的氧化产物，而非仅用 TBARS。结果强烈依赖相分配、界面、脂质组成、氧、金属和引发剂，因此适合作为按应用场景设计的 secondary assay，不能与水相 ORAC 值直接合并。

## 3. 是否可用于统一单体排名

纯单体均可在已知摩尔浓度下进行 molar normalization，但“能换算成 molar”不等于“可跨论文比较”。必须有相同化学实体/立体异构体、纯度、参考标准、反应体系、浓度线性、时间终点和数据算法。Trolox 等效也只是 assay-specific ratio；DPPH-TE、ABTS-TE 与 ORAC-TE 不可互换。

本项目推荐以同一实验室锁定 ORAC-FL SOP 的 `mol TE/mol compound` 生成主排序。外部文献值只能进入 `literature_support` 层；若满足完整 protocol equivalence、原始曲线或足够 QC、共同标准物质桥接和可接受的实验室间偏差，才进入可合并数据集。普通 meta-analysis 式合并不合适。

## 4. Primary–Secondary–Supportive 框架

Primary：ORAC-FL family，H-ORAC 与经验证的 L-ORAC 为平行、明确标记的测量臂。选择理由不是文献量，而是它使用持续生成的 peroxyl radical、评价竞争性 chain-breaking、记录完整 kinetic curve、AUC 同时捕捉程度与持续时间、可用 Trolox 建立摩尔比，并存在经典标准化建议和 L-ORAC 实验室间验证。

Secondary：CUPRAC（ET/reducing power）、ABTS-TEAC（宽极性人工自由基响应）、DPPH（固定有机体系的 mixed-mode reactivity）、FRAP（酸性 ferric reducing power）、TRAP（总 peroxyl trapping）及一个预先规定的 lipid-peroxidation model。它们用于揭示机制差异、异常值和应用情境，不与 ORAC 原值相加。

Supportive：HORAC、TOSC、superoxide、hydroxyl-radical、metal-chelation-specific assays，以及其他特定 ROS assays。只有与研究假设匹配且控制充分时使用。

不建议把 assay 内 z-score 加权成默认 multi-assay composite。不同 assay 测量不同构念，z-score 会把 cohort 组成和缺失模式引入分数，也会让高噪声 assay 与经过验证的 assay 获得相似权重。若后续需要多维汇总，采用 radar/profile 或预先定义的机制域分数，并进行缺失敏感性；探索性 composite 必须与 ORAC 主轴并列而非替代。

## 5. 无 ORAC 数据的处理

缺少 ORAC 标记为 `not_measured`，不是零分，也不构成候选排除。保留其 secondary assay、人体、生物学、食物暴露和机制证据；进入统一实验补测队列。无法测量者记录原因，如不可溶、探针干扰或化合物不稳定，并可使用相应 L-ORAC、TRAP 或脂质氧化模型形成机制特异证据，但不能伪造 ORAC 排名。任何临时排名都要报告 coverage，并用 complete-case、missing-category 和不含 chemical-capacity 域的敏感性分析检查排除偏倚。

## 6. 推荐的 ORAC-FL 最低 SOP 元数据

必须冻结并报告：化合物结构/形式/纯度；H-或 L-ORAC；溶剂和最终百分比；RMCD 类型与浓度；buffer/pH；AAPH、fluorescein、Trolox 浓度；温度；加样顺序；板型、仪器、激发/发射；读取间隔和总时长；AUC 公式和 baseline；空白、无 AAPH、溶剂和自发荧光控制；至少三个样品浓度、线性判据；板内/板间 CV；Trolox 曲线合格标准；共同 QC compounds；批次和操作者。建议 α-tocopherol、ascorbate、quercetin 和一个 carotenoid 作为跨化学类别桥接 QC，但 carotenoid 必须先验证溶解与光谱干扰。

## 7. 15 个最终问题的明确结论

1. 推荐 ORAC-FL 作为 primary chemical metric，但仅限 harmonized project-generated data；不是人体效应指标。
2. 定义为固定体系内对 AAPH-derived peroxyl radical 引发的 fluorescein 氧化的竞争性、动力学积分链终止能力。
3. 纯单体报告 `mol TE/mol compound`，同时保存原始浓度–net AUC 斜率、CI 和 CV。
4. 不允许不同论文 ORAC 数据默认直接合并。
5. 只有 protocol、化学实体、溶剂、温度、试剂浓度、时间/AUC、校准、线性与 QC 等价，并经 bridging standards 验证时才能合并。
6. DPPH 是 secondary fixed-protocol mixed ET/HAT reactivity assay。
7. ABTS 是 secondary broad-polarity artificial-radical ET/mixed-mode assay。
8. FRAP 是 secondary acidic ferric reducing-power assay。
9. CUPRAC 是 secondary、优先的 near-neutral ET/reducing-power complement。
10. TRAP 是 secondary peroxyl total-trapping mechanistic confirmation。
11. 不推荐默认 multi-assay composite 或 z-score 加权。
12. 需要 H-ORAC/L-ORAC 等适配不同类别，但保持共同 radical/probe 逻辑和分臂报告；部分 carotenoids 还需脂质体系补充。
13. 没有 ORAC 但其他证据强者保留，标记缺失并优先补测。
14. 不把缺失当零分，不把 ORAC 作为候选硬门槛，并报告 coverage/缺失敏感性。
15. 一句话定义见单独文件：本项目的主化学抗氧化能力是统一 ORAC-FL 条件下、以 mol TE/mol 表示的过氧自由基链终止能力，且不代表体内抗氧化效果。

## 8. 核心文献

Ou B et al. 2001, DOI 10.1021/jf010586o；Prior RL et al. 2003, DOI 10.1021/jf0262256；Prior RL et al. 2005, DOI 10.1021/jf0502698；Huang D et al. 2005, DOI 10.1021/jf030723c；Watanabe J et al. 2016, PMID 26860561；Schaich KM et al. 2015, DOI 10.1016/j.jff.2015.01.043；Re R et al. 1999, DOI 10.1016/S0891-5849(98)00315-3；Benzie IF & Strain JJ 1996, DOI 10.1006/abio.1996.0292；Apak R et al. 2004, DOI 10.1021/jf048741x；Wayner DDM et al. 1985, DOI 10.1016/0014-5793(85)81208-4；Murphy MP et al. 2022, DOI 10.1038/s42255-022-00591-z。
