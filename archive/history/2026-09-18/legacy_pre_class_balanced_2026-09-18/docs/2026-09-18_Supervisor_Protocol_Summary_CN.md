# Antioxidant Screening Protocol v2.0：导师摘要

本项目的筛选目标现被明确拆分为两个问题。第一阶段只回答结构明确的食源性单体在可比化学条件下谁具有更强的化学抗氧化能力；第二阶段再回答其中哪些候选更值得开展人体营养、机制和靶点实验。因此，今后不再用一个混合人体、食物暴露、体外实验和靶点证据的“综合分”表示抗氧化能力。

Stage 1 有条件采用 ORAC-FL 作为主指标。其操作性定义为：结构明确单体在统一、锁定或方法学可比的 ORAC-FL 条件下，对 AAPH-derived peroxyl radicals 引起的 fluorescein 氧化所表现的 kinetic integrated chain-breaking capacity，以 mol Trolox equivalents/mol compound（mol TE/mol）表示。ORAC-FL 同时反映抑制强度与持续时间，并采用 Trolox 参照和摩尔归一，因而适合在严格方法约束下比较单体。它仍是 chemical assay，不代表人体抗氧化效果、临床获益、生物利用度或细胞信号调控。

现有文献数据只有通过可比性审查后才能排序。Tier A 要求化合物身份、形式/立体化学、纯度、ORAC-FL 类型、H/L arm、AAPH、fluorescein、Trolox、buffer/pH、温度、溶剂/增溶剂、读数计划、AUC、浓度线性和 mol TE/mol 换算均可核实，并排除关键干扰；它可进入主数值排名。Tier B 只缺少非关键细节，可作定量支持，但不能决定接近名次。Tier C 存在已知不兼容条件，只作定性支持。Tier X 是方法信息不足，需补全文献。不得取每篇论文的最大值，不得把 food-level ORAC 用于单体排名，也不得直接拼接不同 protocol。

H-ORAC 与 L-ORAC 作为不同 assay arm。多数水溶性多酚适合 H-ORAC；tocopherols、tocotrienols 和部分 carotenoids 通常需要 L-ORAC 或增溶体系。两臂的溶剂、包合、聚集和校准行为不同，未经桥接验证不能混排。Carotenoids 还需检查溶解、光降解、吸光、荧光内滤和聚集；若无法证明跨臂等价，正式结果应分别给出 H-ORAC 与 L-ORAC 排名，而不是强行形成一个 Top20。

DPPH、ABTS 和 FRAP 不再作为主排名指标。DPPH 使用非生理自由基且高度依赖溶剂、位阻和反应终点；ABTS•+ 是人工自由基，虽能覆盖较宽极性范围，但对介质和时间敏感；FRAP 本质上测 ferric reducing power，不能代表过氧自由基链终止。CUPRAC 作为首选 secondary orthogonal assay，提供 ET/reducing-power 信息；TRAP 用于确认 peroxyl-radical trapping；lipid-peroxidation assays 用于脂相或食品情境。HORAC、TOSC、superoxide、hydroxyl-radical 和 metal-chelation assays 仅作机制支持。由于这些方法测量不同构念，不进行简单平均或默认 z-score 合成；多维结果采用 profile 或 concordance 展示。

多条 Tier A 记录在方法同质时报告 study-level median，并同时报告 range，数据足够时报告 IQR；异质时按 arm、化合物形式或 protocol family 分层。数值接近且不确定性重叠时使用并列或 rank band。没有 ORAC 数据的候选标为 `not_measured` 或 `insufficiently_comparable`，不记为 0、不排除，并进入 ORAC measurement priority list。文献覆盖不足时，榜单必须写作 provisional。

Stage 2 独立评价 human evidence、dietary exposure、bioavailability/dose translation、biological redox evidence、mechanistic evidence、direct-target evidence、experimental tractability 和 safety/prooxidant risk，同时记录 major human metabolites 与 context interactions。v1.0 的 25/25/20/15/15 框架更名为 legacy Translational Priority Score，不再产生化学 Top20。T1–T5 靶点证据体系、PK 与 efficacy 分离、direct target 非硬门槛、安全性非早期硬排除等既有原则保持不变。

下一步建议在 protocol 审核后开展 10–20 个跨类别代表性成分的 ORAC literature pilot，测试 A/B/C/X 比例、H/L 可比性、CUPRAC 覆盖及单位换算。Pilot 的目的不是立即宣布 Top20，而是判断现有文献是否足以支持正式排序，并识别需要统一复测的候选。
