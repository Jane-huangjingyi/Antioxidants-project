# Antioxidant Screening Protocol v2.0（中文）

**版本：** 2.0  
**状态：** 待研究者/ChatGPT 审核；在审核冻结前不得启动正式排名  
**适用范围：** 常见食源性、结构明确的天然原型小分子

## 1. 目的与统一标准

本项目将两个科学问题分开回答。Stage 1 只比较化学抗氧化能力；Stage 2 再评价人体与实验转化价值。两种结果必须分别报告，不得用 Stage 2 综合分替代或命名为“抗氧化能力排名”。

**导师版一句话标准：** 本项目以方法学可比的 ORAC-FL 数据作为食源性单体化合物化学抗氧化能力的主排序依据，以 mol Trolox equivalents/mol compound（mol TE/mol）表示；CUPRAC 等方法仅补充不同反应机制，人体暴露、生物利用度、机制、靶点与安全性证据用于独立的第二层转化优先级评价。

## 2. 继承并冻结的范围原则

1. 主榜仅纳入正常膳食食品、饮料和常见香辛料中天然存在、具有唯一结构标识的原型小分子。
2. 多酚优先用于候选生成，但不设置类别配额；候选可包括 polyphenols、carotenoids、tocopherols/tocotrienols、organosulfur compounds、betalains、quinones 和 nitrogen-containing phytochemicals 等。
3. 人体代谢物不与母体化合物竞争主榜，但必须记录主要吸收/循环结合物及肠道菌群来源代谢物；具备独立暴露和活性证据者进入 secondary candidate list。
4. 证据质量优先于论文数量；同级文献数量只提供有上限的支持，不得形成热门分子偏倚。
5. Direct-target evidence 不是早期纳入硬门槛；T1–T5 靶点分类保持不变。
6. Safety/dose window 是风险与转化维度，而非早期硬排除门槛；严重且经权威证实的安全风险可触发独立审查。
7. 协同、拮抗和 food-matrix interaction 属于第二层情境证据，不定义单体基础化学抗氧化能力。
8. 人体 PK/bioavailability 与人体 efficacy 分开记录和分级。

## 3. 两阶段体系

### 3.1 Stage 1：Chemical Antioxidant Capacity Ranking

Stage 1 回答：“在可比条件下，哪些结构明确的食源性单体具有更强的化学抗氧化能力？”

Primary metric 为 ORAC-FL。操作性定义为：**结构明确单体在统一、锁定或方法学可比的 ORAC-FL 条件下，对 AAPH-derived peroxyl radicals 引起的 fluorescein 氧化所表现的 kinetic integrated chain-breaking capacity，并以 mol TE/mol compound 表示。**

该指标是化学体系中的、过氧自由基相关的动力学积分容量。它不代表人体抗氧化效果、临床获益、生物利用度、细胞 redox regulation 或最终实验优先级。

### 3.2 Stage 2：Translational Prioritization

Stage 2 回答：“在化学抗氧化能力较强或具有重要潜力的候选中，哪些更值得开展营养干预、机制和 target-protein 研究？”它产生 **Translational Priority**，不得称为 antioxidant-capacity ranking。

Stage 2 必须分别评价：human evidence、dietary exposure、bioavailability/dose translation、biological redox evidence、mechanistic evidence、direct-target evidence、experimental tractability、safety/prooxidant risk，并记录 major human metabolites 与 context interactions。Stage 1 名次不得自动决定 Stage 2 名次，Stage 2 也不得反向改写 Stage 1 化学容量值。

## 4. ORAC-FL 的方法边界

ORAC 全称为 oxygen radical absorbance capacity；ORAC-FL 使用 fluorescein 作为探针，通常由 AAPH 热分解持续产生 peroxyl radicals，以 Trolox 建立参照曲线。样品与空白荧光衰减曲线下面积之差形成 net AUC，再在已验证线性范围内换算为 Trolox equivalents。

推荐单位为 `mol Trolox equivalents/mol compound`。质量单位只有在化合物身份、分子量、盐型/水合物和计量基础明确时才可换算；food-level ORAC（例如 µmol TE/100 g food）不得用于单体分子排序。

H-ORAC 与 L-ORAC 必须作为不同 assay arm 记录。H-ORAC 适用于水相可溶体系；L-ORAC 通常依赖丙酮、共溶剂或 randomly methylated β-cyclodextrin（RMCD）等增溶体系。两臂的溶剂、传质、聚集和校准行为不同，未经桥接验证不得假定同尺度，也不得直接混排。

## 5. Literature-derived ORAC comparability framework

每条记录先按 `config/ORAC_Literature_Eligibility_Rubric.csv` 逐项审查，再分级：

- **Tier A（高度可比）：** 化合物身份、形式/立体化学、纯度、ORAC-FL 类型、H/L arm、AAPH、fluorescein、Trolox、buffer/pH、温度、溶剂/增溶剂、读数间隔与总时长、AUC 算法、浓度线性和单位换算均可核实；不存在已知关键不兼容或未解决干扰。可进入 primary numerical ranking。
- **Tier B（部分可比）：** 已确认是目标化合物和 ORAC-FL，arm、Trolox 基准及 molar conversion 可判断；少量非关键参数缺失或有可解释偏差。可作为 supportive quantitative evidence，不得决定数值接近候选的细名次。
- **Tier C（不可比）：** 已知采用不兼容的 probe/radical/protocol、food/extract-level 单位、不可恢复的质量归一、未验证的 H/L 混合、明显干扰或其他无法桥接条件。仅作定性文献支持，不进入正式数值排名。
- **Tier X（信息不足）：** 文献声称 ORAC，但方法信息不足以判断 A/B/C。保留记录并标为待补全文献，不得数值排名。

不得抽取每篇论文中的最大 ORAC 值。不得把不同 protocol 的数值直接拼接。不得将相同实验数据的重复出版物视为独立证据。

## 6. Stage 1 聚合与排名规则

1. 仅 Tier A 记录默认进入 primary numerical ranking；Tier B 单列并用于方向性支持。
2. 多条 Tier A 记录先检查 compound form、H/L arm、protocol family、实验浓度线性及研究独立性。
3. 足够同质时，以研究层面的 median 为中心估计，同时报告 range；记录数足够时增报 IQR。不得取最大值。
4. 存在可解释异质性时，按 assay arm、化合物形式或 protocol family 分层，不计算虚假的总体值。
5. 数值非常接近且不确定区间重叠时，报告并列或 rank band；不得用 Tier B 或低级 assay 强行拆分。
6. H-ORAC 与 L-ORAC 只有在预先规定的桥接研究证明测量等价性、校准一致性和误差可接受时才可合并；否则输出分臂排名。
7. Stage 1 表至少包含：rank、compound_name、PubChem_CID、InChIKey、chemical_class、ORAC_arm、ORAC_value_mol_TE_per_mol、ORAC_source、ORAC_comparability_tier、number_of_eligible_ORAC_studies、median_ORAC、ORAC_range、ORAC_confidence、CUPRAC_available、CUPRAC_value、secondary_assay_summary、notes。

## 7. 缺失 ORAC 数据

无 ORAC 数据不得编码为 0，不得直接排除，也不得推断为低化学抗氧化能力。统一编码为 `not_measured` 或 `insufficiently_comparable`。候选仍保留 CUPRAC、DPPH、ABTS、FRAP、人体、机制、食物暴露和靶点证据，并进入 **ORAC measurement priority list**。Stage 1 覆盖不足时只能发布 `provisional Chemical Antioxidant Capacity Top20`，并同时披露覆盖率和缺失模式。

## 8. Secondary 与 supportive assays

不同 assay 测量不同 antioxidant constructs，禁止 ORAC、DPPH、ABTS、FRAP 的简单平均，也不默认进行 z-score 加权。

| 方法 | 正式角色 | 解释边界 |
|---|---|---|
| CUPRAC | 首选 secondary orthogonal assay | ET/reducing power；不等同于 peroxyl chain breaking |
| ABTS/TEAC | secondary broad-polarity artificial-radical response | 人工自由基阳离子；强依赖介质和反应时间 |
| DPPH | secondary fixed-protocol mixed ET/HAT reactivity | 非生理自由基；受溶剂、位阻和终点时间影响 |
| FRAP | secondary ferric reducing power | 还原力 endpoint；不证明 radical chain breaking |
| TRAP | secondary peroxyl-radical trapping confirmation | 与 ORAC 概念相关但 probe、动力学和计算并不等价 |
| Lipid-peroxidation inhibition | context-specific secondary | 支持脂相或食品体系情境；强依赖底物和氧化条件 |
| HORAC、TOSC、superoxide、hydroxyl radical、metal chelation | supportive only | 用于机制补充和异常值解释，不进入主排序 |

如需展示多维证据，采用 radar/profile、mechanism-specific domains 和 concordance analysis；只有在明确预注册构念、尺度和外部验证后，才可另行探索 composite，且不得取代 Stage 1。

## 9. 跨类别可比性与分臂策略

- **Polyphenols：** 多数适合 H-ORAC，但糖苷化、聚合、氧化、pH 依赖和自发荧光/淬灭需检查；低溶解度成员可需要特定共溶剂。
- **Tocopherols/tocotrienols：** 亲脂性强，通常需要 L-ORAC；RMCD 包合与异构体身份会改变表观反应，不能与 H-ORAC 默认混排。
- **Carotenoids：** 通常需要脂相/增溶体系，易受溶解、聚集、光降解、氧分压、吸光和荧光内滤效应影响；ORAC-FL 可能低估或失真，必须设置 blank、光谱与回收 QC，并优先分臂报告。
- **Organosulfur compounds：** 部分化合物的主要 redox 行为依赖硫醇交换、亲电反应或酶调控，未必表现为强 peroxyl chain breaking；ORAC 低值不能代表缺少 redox relevance。

当跨臂等价性无法验证时，应发布 H-ORAC 与 L-ORAC 两个 rank table，以及“不可安全跨臂比较”的明确声明；不得为形成单一 Top20 而强行合并。

## 10. Stage 2 转化优先级

原 v1.0 的 25/25/20/15/15 框架更名为历史版 `Translational Priority Score`，停止用于基础化学 Top20。v2.0 先采用八域 profile，并在 pilot 后冻结权重：human evidence；dietary exposure；bioavailability/dose translation；biological redox evidence；mechanistic evidence；direct-target evidence；experimental tractability；safety/prooxidant risk。建议的初始敏感性分析权重为 20/15/15/15/10/10/10/5，而非既定真值；必须同步报告逐域分数、缺失项、风险旗标和替代权重下的 rank stability。

人体 PK 只进入 bioavailability/dose-translation 域，不得升级为 efficacy。Safety 域记录 dose window、UL/权威限制、特殊人群风险、hormesis、金属环境及 antioxidant-to-prooxidant transition；它作为风险修饰和研究设计依据，不以普通数据缺失触发早期排除。Major metabolites 是 bioavailability 与机制解释的必填注释；context interactions 独立记录，不并入基础 ORAC 值。

## 11. 靶点证据保持不变

T1 为直接 biochemical/biophysical binding；T2 为 cellular target engagement/chemical proteomics；T3 为 functional target validation；T4 为 regulated/pathway-associated protein；T5 为 predicted target。只有 T1/T2 进入 high-confidence direct-target layer。T3 标为 functional target，T4 标为 regulated/pathway-associated，T5 标为 predicted。Nrf2、NF-κB 活性、表达、磷酸化或核转位变化不得自动写为 direct binding。

## 12. 两种 Top20 的命名

- **Chemical Antioxidant Capacity Top20：** 仅由符合规则的 ORAC-FL Stage 1 数据产生；覆盖不足时冠以 `provisional`。
- **Translational Priority Top20：** 由 Stage 2 多域证据产生，表示研究优先级，不表示化学抗氧化能力。

两榜可重叠但不得合并成无定义的“综合抗氧化 Top20”。

## 13. 数据溯源与质量控制

每条正式记录保留原始单位、换算式、PMID、DOI、Zotero key、具体表格/图/补充材料位置、提取人和复核状态。数值换算必须由第二人或自动校验规则复核。必须检查：身份/立体化学、盐型/水合物、纯度、分子量、H/L arm、线性、光学干扰、重复出版、同研究非独立数据和选择性报告。

冻结排名前必须完成以下审计：Stage 1/2 命名是否混淆；是否将 ORAC 外推为人体效果；是否跨 protocol 或 H/L 无条件合并；缺失是否错误记零；是否创建默认 composite；T1–T5 是否混级；是否保留 safety、metabolites 和 interactions；跨类别覆盖是否系统性偏倚。

## 14. 下一阶段 pilot（提出但本轮不执行）

开展 10–20 个跨类别代表性单体的 **ORAC Literature Ranking Pilot**。样本应覆盖 catechin/EGCG、quercetin、phenolic acid、stilbene、tocopherol、carotenoid、vitamin C 与 organosulfur 类代表，但具体名单由候选宇宙和可追溯性决定，不机械固定。

Pilot 依次执行：检索与去重；逐条提取；A/B/C/X 分级；H/L 分臂；单位换算复核；Tier A 中位数与异质性评估；CUPRAC 覆盖检查；缺失候选进入测量优先清单。输出用于判断文献能否支持正式 Top20，以及哪些化合物需要统一复测。本 protocol 审核前不得启动 pilot。

## 15. 停止条件

本轮只冻结 v2.0 方法结构及数据规范；不生成 Top20、不批量抓取 ORAC 或 target、不修改知识图谱、不执行 Stage 2 排名、不开展实验。待研究者和 ChatGPT 审核后再进入 pilot。
