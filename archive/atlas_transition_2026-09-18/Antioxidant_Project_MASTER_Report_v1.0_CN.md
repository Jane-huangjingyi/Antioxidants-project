# Antioxidants Project MASTER Report v1.0

**版本日期：2026-09-18｜状态：供研究者与导师审核的 class-balanced functional-factor panel v1.0**

## 1. 项目问题与结论边界

本项目最初以食源性酚类/多酚的 H-ORAC-FL 文献比较为入口，已经完成候选范围、A/B1/B2/C/X 可比性规则、50 个 H-arm 候选、provisional Top20、证据整合和靶点映射准备度分层。导师的新要求改变的是最终面板的组成逻辑，而不是否定这些成果：H-ORAC 结果现在作为酚类来源层和 direct chemical capacity 证据层使用，不再作为跨化学类别的唯一总排名。本版回答的是“哪些正常膳食来源、结构明确且在抗氧化/redox 网络中承担不同功能的因子，适合组成覆盖主要类别、膳食暴露大体可比并可继续做机制研究的面板”。它不回答谁是人体内“最强抗氧化剂”，不将 ORAC 外推为临床获益，也不将不同 assay、摄入量和机制证据相乘形成伪精确总分。

## 2. 候选范围与面板结构

有机功能因子面板共 20 个：多酚 5 个（epicatechin、quercetin、EGCG、genistein、naringenin），酚酸/酚酸结合物 4 个（caffeic acid、ferulic acid、chlorogenic acid、gallic acid），维生素 3 个（L-ascorbic acid、alpha-、gamma-tocopherol），类胡萝卜素 4 个（beta-carotene、lycopene、lutein、zeaxanthin），有机硫 2 个（sulforaphane、allicin），其他结构明确食源性酚类 2 个（sesamol、eugenol）。另设 selenium、zinc、manganese、copper、iron 五个 micronutrient context nodes。矿物质不与有机小分子做 ORAC 比较；Cu/Fe 同时被标记为必需辅因子和在游离/过量状态下的促氧化风险节点。

面板采用三层状态。`core_panel` 有 12 个，覆盖主要有机类别并使用可解释的日摄入估计；其 µmol/day 最大/最小比为 18.6，满足预设 100 倍窗口。`exceptional_representative` 有 5 个，包括 vitamin C 以及 4 个酚酸/结合物；这些因子具有明确科学代表性，但其摄入量显著更高或受“游离体、总量、酸水解后苷元当量、咖啡异构体”定义影响，不能为了满足窗口而改写数据。`extended_special_case` 有 3 个（zeaxanthin、allicin、sesamol），保留类别覆盖，但暴露拆分、稳定性或低摄入使其不适合与核心层作同强度定量比较。

## 3. 选择次序与不使用综合乘积的原因

选择次序被冻结为：先满足类别覆盖，再检查正常膳食暴露及可追溯性，最后用机制和证据强度决定是否值得保留。候选生成不得反向依据 ORAC 高低。ORAC、摄入量和机制强度描述的是不同 construct：ORAC 是特定体系中的过氧自由基链终止能力，摄入量是进入消化道的膳食量，机制证据是具体实验设计支持的 redox 过程。将它们相乘会混合量纲、放大测量误差并错误暗示系统暴露和因果效应，因此本项目明确禁止 `ORAC × intake` 或默认 multi-assay composite score。

## 4. ORAC 的保留方式

ORAC-FL 的操作性定义仍为：结构明确单体在统一或方法学可比条件下，对 AAPH-derived peroxyl radicals 引起的 fluorescein 氧化所表现的 kinetic integrated chain-breaking capacity，以 mol Trolox equivalents/mol compound 表示。H-ORAC 与 L-ORAC 不跨臂混排。已有 H-ORAC 排名、median、B1 count、confidence 和 readiness 被原样带入 `Antioxidant_Panel_Master.csv`；tocopherols 与 carotenoids 保持 L-arm/context-specific 标记。H-ORAC 的历史 B1 是探索性可比证据，并非 Tier A 标准化实测真值。

## 5. 膳食暴露框架

主暴露量统一为 `typical_intake_umol_day`，同时保留 mg/day、人口、数据类型和引用。`log10_exposure` 仅用于展示跨度。暴露证据按人口调查/食物组成推算、代表性情境估计、营养参考摄入和不确定估计分别标记，不能互换。本版较可靠的调查值包括韩国成年人 quercetin 14.0 mg/day、naringenin 5.29 mg/day、catechin/epicatechin 类摄入，US 成人 genistein 0.95 mg/day，EFSA 成人 alpha-tocopherol 摄入范围，以及 NHANES 矿物质摄入趋势。酚酸数值采用芬兰调查经综述报告的苷元当量，特别容易受分析定义影响；EGCG、sulforaphane、allicin、gamma-tocopherol、zeaxanthin 等使用的是明确标注的情境或近似估计，冻结面板前需要以人口原始研究替换。

## 6. 机制分类

机制证据分为六类：A，direct chemical antioxidant，包括 HAT/ET、过氧自由基链终止、特定 ROS/RNS 捕获、金属螯合、脂质过氧化抑制和抗氧化剂再生；B，endogenous defense regulation，包括 KEAP1–NRF2、GSH/GPX、TXN/PRDX 和 SOD/CAT/GPX；C，ROS formation suppression，包括 NOX 与线粒体 ROS；D，lipid/ferroptosis-related control，包括膜脂链反应、GPX4、FSP1/CoQ 和铁依赖脂质过氧化；E，redox-linked inflammatory signaling，只有存在 ROS、GSH/GSSG、脂质氧化、DNA氧化或其他 redox endpoint 时才记录 NF-κB/MAPK/NLRP3；F，mineral cofactor pathways。通路改变不等于直接蛋白靶点，只有直接结合/共价占位或细胞靶标接合证据才可进入 T1/T2 层。

## 7. 证据强度和 ledger 用法

`Antioxidant_Mechanism_Evidence_Master.csv` 每行代表 compound × mechanism/pathway × independent evidence item。Strong、Moderate、Limited、Predictive 按实验设计与因果信息分级，不按期刊声望分级；`journal_prestige_note` 明确写为不参与评级。当前 ledger 有 25 条首轮核心证据：H-ORAC 酚类以原记录集为 provenance，alpha-tocopherol 使用人体 F2-isoprostane 剂量反应试验，lycopene 使用随机对照氧化 DNA 损伤试验，lutein/zeaxanthin 使用人体干预证据，sulforaphane 使用 KEAP1 cysteine sensing 的直接生化证据，矿物质使用酶辅因子/营养状态框架。该 ledger 是“最小可审计证据集”，不是穷尽性系统综述；每个化合物的第二、第三篇机制原始研究仍需在正式 target mapping 前补齐。

## 8. 人体证据与 direct target 的隔离

人体证据单独记录为 exposure、PK、controlled intervention 或 nutrient requirement/deficiency，不能把人体暴露等同人体功效。当前 direct-target 声明极少：sulforaphane 对 KEAP1 cysteine 的共价修饰可视为直接 engagement；矿物质的酶辅因子关系属于营养生化 context，不按普通 small-molecule target 处理。其他候选即使影响 NRF2、NF-κB、SOD 或 GPX，也不得自动写为这些蛋白的直接靶点。

## 9. 各类别的科学解释

多酚/酚酸的优势是 H-ORAC 与化学机制资料较多，但 publication density 高，且母体化合物的体外浓度经常远高于人体循环浓度。Vitamin C 是水相电子供体及 tocopherol regeneration 节点；tocopherols 是脂相链终止抗氧化剂，不能由 H-ORAC 表示。Carotenoids 的共轭多烯结构支持 singlet-oxygen quenching 和膜相作用，但溶解、聚集、氧分压和光学干扰使 ORAC/荧光法跨类比较风险很高。Sulforaphane 的核心价值是 electrophile–KEAP1–NRF2 轴而非自由基捕获；allicin 是不稳定的 reactive sulfur species，其 parent exposure 和蛋白选择性尚不清楚。Sesamol/eugenol提供食品油和香辛料相关的化学空间，但人群干预证据薄弱。

## 10. 安全性、剂量和促氧化情境

“抗氧化”不是固定分子标签。EGCG 可在培养基中自氧化并生成 H2O2；quercetin、gallic acid、vitamin C 等在 Fe/Cu 条件下可发生促氧化化学；beta-carotene 高剂量补充在吸烟人群中有不利结果；tocopherol 高剂量补充不能等同膳食摄入；sulforaphane/allicin 的 electrophilic/thiol-reactive 性质意味着浓度升高可能转为应激。Cu 和 Fe 的双重角色必须在任何机制图中显式表示。所有机制结论都受剂量、时间、氧张力、pH、金属和基质限制。

## 11. 数据溯源与历史文件

活跃主表通过 `provenance_record_ids`、`legacy_source_file` 和 `legacy_record_id` 回溯旧记录。旧项目文件被移动至 `archive/legacy_pre_class_balanced_2026-09-18/`，不删除。H-ORAC 值可沿“panel master → archived shortlist/candidate universe → archived record-level extraction → DOI/PMID/exact location → original value and conversion”回溯。新增机制文献的 Zotero 字段在本地 Zotero 接口不可用时统一写 `pending_local_import`，绝不伪造 item key；正式审阅后应由研究者导入 `antioxidants project` collection 并回填。

## 12. 图形解释

`Class_Balanced_Antioxidant_Panel.png` 显示 20 个有机候选的类别覆盖，矿物质单列；`Dietary_Exposure_Range.png` 使用 log10(µmol/day) 显示摄入跨度和核心层 100 倍窗口；`Compound_Pathway_Evidence_Heatmap.png` 使用 Strong=3、Moderate=2、Limited=1、Predictive=0.5、无证据=0，但颜色编码只表示当前 ledger 的证据强度，不是机制效应大小；`Antioxidant_Evidence_Map.png` 显示化合物、机制域和矿物质情境连接。四图都由 `scripts/make_antioxidant_figures.py` 从两张 master CSV 重建。

## 13. 已知缺口与当前结论

当前面板已满足类别平衡、结构唯一、正常膳食来源、H/L 分臂、核心摄入 100 倍窗口和矿物质隔离等结构性要求，但尚未达到“所有暴露值和每个核心机制均由 1–3 篇已完成双人核对的原始文献支持”的最终证据冻结标准。最大缺口是若干 intake estimate 仍为情境值、phenolic acid 定义异质、parent compound intake 与代谢物暴露未桥接、allicin/zeaxanthin 的独立摄入不确定、机制 ledger 仍偏稀疏，以及 Zotero key 尚待本地导入。现阶段最合理的表述是：已形成一个可审计的 **class-balanced dietary antioxidant functional-factor panel v1.0**，可用于导师审阅、暴露证据补强和小规模机制/target pilot；不得称为跨类别“最强抗氧化剂 Top20”。

## 14. Target mapping handoff

下一阶段只应从身份明确、面板状态为 core/exceptional、机制证据可追溯且无重大 assay/暴露歧义的候选开始。优先 pilot 可考虑 quercetin（丰富 H-ORAC 与多机制文献）、alpha-tocopherol（脂相链终止与人体 F2-isoprostane）、sulforaphane（KEAP1 direct engagement）和 lycopene（人体氧化损伤 endpoint），用来测试 T1–T5 分类能否跨机制类别一致执行。进入批量 mapping 前，应先补齐每个候选 1–3 篇核心机制原始研究、回填 Zotero key，并对 direct target 声明做第二研究者复核。

## 15. 关键来源（本版直接采用或用于框架）

- Korean dietary antioxidant/flavonoid intake database, PMCID: PMC11417454。
- Recent US flavonoid intake analysis, PMCID: PMC12599756。
- NHANES mineral intake trend analysis, PMCID: PMC11100034。
- Selenium/tocopherol oxidative-stress trial, PMID 27012420, DOI 10.1016/j.freeradbiomed.2016.03.010。
- Vitamin E dose–F2-isoprostane trial, PMID 17936185, DOI 10.1016/j.freeradbiomed.2007.06.019。
- Purified lycopene randomized trial, PMID 18689558, DOI 10.1080/07315724.2008.10719699。
- KEAP1 sulfhydryl sensor study, PMID 12193649。
- Lutein neonatal randomized trial, PMID 24876916。
- Macular xanthophyll human intervention, PMID 38890092。
- Sesame lignan intake study, PMCID: PMC7230771。

## 16. Sync to ChatGPT

**A. Panel size：**20 个有机功能因子，另加 5 个矿物质情境节点。**B. Classes：**多酚、酚酸/结合物、维生素、类胡萝卜素、有机硫、其他食源性酚类；矿物质独立。**C. Exposure range：**核心层约 3.5–65.4 µmol/day，最大/最小 18.6 倍。**D. 100-fold compliance：**核心层满足；高摄入或定义敏感因子进入 exceptional，暴露不确定/低值进入 extended。**E. Major pathways：**直接链终止/还原/螯合、KEAP1–NRF2、GSH/GPX、SOD/CAT、线粒体/NOX、膜脂/ferroptosis、redox-linked inflammation、矿物辅因子。**F. Strongest evidence：**epicatechin/quercetin 的 H-ORAC 记录深度、alpha-tocopherol 的人体 F2-isoprostane、lycopene 的随机人体氧化损伤、sulforaphane 的 KEAP1 cysteine engagement。**G. Weak evidence：**allicin、sesamol、eugenol及若干独立 intake estimate。**H. Minerals：**只作为 context layer，Cu/Fe 显式标记促氧化可能。**I. Target readiness：**可以开展小规模跨类别 pilot，不宜直接批量 mapping。**J. Risks：**暴露定义异质、parent/metabolite gap、体外剂量外推、光学/溶解干扰、ledger 尚未穷尽、Zotero 待回填。**K. Next step：**双人复核暴露和核心机制原始文献，完成 Zotero 导入，再用 3–4 个跨类候选验证 target pipeline。

