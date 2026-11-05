# 常见食源性抗氧化小分子筛选方案（Phase 0–1）

版本：1.0（2026-09-17）；状态：提交研究者审核，尚未用于正式排名。

## 1. 目标与适用范围

本项目筛选综合科学价值高、具有人体相关性并适合后续机制与靶点研究的常见食源性抗氧化小分子。候选来源覆盖全球正常膳食，暴露证据按国家、地区、人群和食品形态分别记录；一般成年人及膳食可达暴露是主评价基准，患者和高风险人群证据保留但单独标记。项目采用广义 redox-modulating 定义，区分 direct_antioxidant、redox_regulatory 与 indirect_redox_related；后者只有在研究同时报告可信的氧化还原终点时才构成抗氧化证据。

Phase 0–1 只冻结规则、字段和来源优先级，不生成 Top20，不批量提取靶点。

## 2. 候选实体与榜单分层

主榜实体必须是天然存在于正常食品、饮料或常见香辛料中的原型小分子，具有可唯一解析的结构、PubChem CID 或可核验的等价结构标识，以及至少一条定量食物含量证据。主要来自药用植物或补充剂、内源性物质、人体代谢物、混合物、聚合物、矿物元素和结构不明确实体进入 extended/secondary list。盐、溶剂化物、互变异构体、立体异构体与糖苷/苷元不得仅凭名称合并；以结构标准化记录建立 parent–form 关系。

每个原型化合物均建立代谢物子表，至少记录吸收/循环代谢物、II 相结合物和肠菌来源代谢物。代谢物不与母体竞争主榜；若有人体系统暴露、活性和靶点证据，可进入 secondary candidate list。

## 3. 候选宇宙生成规则

候选生成采用多源并集、结构去重、证据门控：

1. 从 Phenol-Explorer、USDA flavonoid/special-interest data、FoodData Central、FooDB 及区域权威食物成分库提取可定位到单一结构的食物成分；跨类别补充 carotenoids、tocopherols/tocotrienols、organosulfur compounds、betalains、quinones、含氮植物小分子及其他具有 redox 证据的食源性实体。
2. 以 PubChem 和 ChEBI 解析名称、同义词、CID、InChIKey、SMILES、分子式、分子量和立体化学；保留来源原始标识与映射方法。
3. 只有同时满足 `structure_resolved=yes`、`normal_diet_occurrence=yes`、至少一条可追溯食物证据且非排除实体者进入 main-candidate universe。仅检出但无可解释含量者可进入候选池，标记 `exposure_status=trace_or_unknown`，不得获得高食物暴露分。
4. 用食品含量 × 地区消费量估计现实暴露；不能获得消费量时仅报告含量，不推断摄入。食品形态、加工、分析方法、湿/干重、聚合/苷元换算必须保留。
5. 数据库命中只是候选生成依据，不等同于生物效应、直接靶点或临床证据。

排除规则包括：结构无法消歧；主要来源不是正常膳食；仅为内源性物质或人体代谢物；无可靠食物来源；证据仅来自未表征提取物且不能归因于单一化合物。缺乏人体证据、缺乏直接靶点或存在安全疑虑不是早期硬排除项。

## 4. 检索与证据纳入

候选生成与证据评价采用独立检索轨道：食物出现/含量、人体效应、人体 PK/代谢物、动物/细胞 redox、机制、直接靶点、安全性和组合相互作用。每条检索保存数据库、平台、完整检索式、日期、时间范围、过滤器、命中数和导出文件；报告遵循 PRISMA-S 的可复现原则。PubMed 为生物医学主源，Crossref 用于 DOI 元数据补全而非效应证据来源。

正式纳入记录须能回到原始论文或权威数据库。综述用于发现研究与解释背景，除方法学共识外不替代原始证据。重复队列、重复数据集和同一试验多篇报告合并为 evidence family，避免重复计数。

## 5. 分级与质量修正

人体证据 H1–H6、抗氧化证据 A1–A5、机制 M1–M5 和靶点 T1–T5 的操作定义见评分表。设计层级只给出起始等级；研究质量、偏倚风险、终点有效性、剂量相关性和可重复性决定降级。RCT 使用 RoB 2；非随机干预使用 ROBINS-I V2；观察研究采用预先定义的领域式偏倚判断。证据体置信度参考 GRADE 的 risk of bias、inconsistency、indirectness、imprecision 和 publication bias，但不机械套用数值。

优先 redox 终点包括经验证的 F2-isoprostanes、氧化 DNA/蛋白/脂质损伤标志物、GSH/GSSG 以及经验证方法测得的特定 ROS。MDA/TBARS、总抗氧化能力和非特异荧光探针需降级；仅凭 SOD/CAT/GPX 表达变化不等同于抗氧化改善。DPPH、ABTS、FRAP、ORAC 只属于 A5，并且不同 assay 的数值不得直接排序。

## 6. 100 分评分框架

基线权重为 Human relevance 25、Antioxidant biological evidence 25、Food exposure 20、Mechanistic evidence 15、Direct-target evidence & tractability 15。每域先产生 0–1 的域分，再乘权重；`not_searched`、`searched_none`、`conflicting` 与 `not_applicable` 必须分开，不得都编码为零。

域分由最高可信层级决定主值，独立复制、跨模型一致性和剂量/暴露匹配提供有限加分。论文数量只在同层级内使用饱和函数：首个独立 evidence family 提供全部基础分，第 2–3 个最多增加该域满分的 10%，第 4 个以后不加分。任何低层级证据累积不得跨越上一层级的最低门槛。高风险偏倚、无正交验证、明显超生理剂量或母体 Cmax 不匹配触发降级或 translation penalty。

建议的域内归一化锚点为：Human 1.00/0.85/0.65/0.45/0.35/0（H1–H6；H5 为暴露支持，不能替代获益）；Antioxidant 1.00/0.75/0.50/0.25/0.10（A1–A5）；Mechanism 1.00/0.75/0.50/0.25/0.10（M1–M5）；Target/tractability 1.00/0.85/0.60/0.30/0.10（T1–T5）；Food exposure 由定量含量、消费频率、地区覆盖、估计摄入和数据质量五项组成，只有检出信息时最高 0.20。

敏感性分析至少运行四套权重：

| 方案 | Human | Antioxidant | Food | Mechanism | Target/tractability |
|---|---:|---:|---:|---:|---:|
| 原始基线 | 25 | 25 | 20 | 15 | 15 |
| 人体优先 | 35 | 25 | 20 | 10 | 10 |
| 暴露平衡 | 25 | 20 | 30 | 15 | 10 |
| 实验转化优先 | 20 | 20 | 15 | 20 | 25 |

原始基线建议作为预注册主分析，另三套为真正不同的敏感性方案。后续报告 Top20 入选频率、名次中位数/IQR、Spearman/Kendall 相关、权重扰动下的 rank acceptability，并单列缺失数据敏感性。Safety/dose window 不并入早期总分，作为风险旗标和决胜规则，避免把知识缺口误作安全。

## 7. 食物暴露、生物利用度与剂量转换

食物暴露至少保存原食物、加工状态、地理来源、分析方法、中心值/范围、单位、湿干基、消费量、估计摄入和不确定性。食物存在不等于现实暴露。人体研究中分别记录母体和代谢物的 Cmax、AUC、基质、时间点；体外有效浓度与自由浓度/人体 Cmax 比值构成 `dose_translation_gap`。若细胞效应浓度远高于可信系统暴露，保留证据但降低转化相关性。

## 8. 安全性和情境作用

安全性记录典型膳食暴露、干预剂量、体外浓度、Cmax、AE 阈值、UL、特殊人群、药物相互作用、金属依赖、hormesis、prooxidant transition 与证据等级。无 UL 不表示安全。协同/拮抗必须记录零模型（Bliss、Loewe、CI/isobologram、ZIP 等）、剂量矩阵、重复和统计不确定性；描述性联合效应最多为 `possible_synergy` 或 `possible_antagonism`。

## 9. 数据管理与复现

所有表使用 UTF-8 CSV、稳定 snake_case 字段名、ISO 8601 日期和明确缺失值原因。每条证据保存 PMID、DOI、数据库记录、检索日期、Zotero item key 和 BibTeX key。原始导出只读保存，清洗脚本版本化，人工判定保留判定者、日期、理由和第二审状态。关键纳入与层级判定应双人复核；冲突由第三人或共识解决。

## 10. Phase 0–1 停止条件与下一阶段

本方案、四份数据字典/评分表、来源审计、决策日志、交接文件和内部审计完成即停止。Phase 2 建议依次为：2A polyphenol-first universe；2B 跨类别扩展；2C 证据提取与初筛；2D 权重敏感性和名次稳定性；2E provisional Top20；Phase 3 用 EGCG 试运行 T1–T5 全流程。任何排名前应冻结评分实现、缺失值规则和检索日期。

## 11. 核心方法学依据

- Murphy MP et al. *Nature Metabolism* 2022;4:651–662. DOI: 10.1038/s42255-022-00591-z; PMID: 35760871.
- Rethlefsen ML et al. *Systematic Reviews* 2021;10:39. DOI: 10.1186/s13643-020-01542-z.
- Sterne JAC et al. RoB 2; ROBINS-I V2 (2025 release); GRADE/Cochrane Handbook.
- Mateus A et al. *Annual Review of Pharmacology and Toxicology* 2022;62:465–482. DOI: 10.1146/annurev-pharmtox-052120-013205.
- Ianevski A et al. *Nucleic Acids Research* 2022;50:W739–W743. DOI: 10.1093/nar/gkac382.
