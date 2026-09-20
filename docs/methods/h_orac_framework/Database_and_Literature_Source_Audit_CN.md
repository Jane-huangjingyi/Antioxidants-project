# 数据库与文献来源审计（截至 2026-09-17）

版本/日期为本轮可核实状态；动态资源在正式提取时必须再次记录 release 或 access date。

| 来源 | 最适用途 | 类型与更新状态 | 访问/自动化 | 主要偏倚与限制 | 正式筛选建议 |
|---|---|---|---|---|---|
| Phenol-Explorer | 多酚候选、食物含量、加工、PK/代谢物线索 | 人工整理；主要公开版本 3.0（2013），网页可访问 | 网页/可追溯原文；批量能力有限且版本较旧 | 多酚中心；食品与分析方法异质；更新陈旧 | 推荐作为多酚种子和定量来源，必须用新文献/区域库更新 |
| USDA Flavonoid DB | 食物中黄酮含量 | 权威整理；Release 3.3（2018）；另有 WWEIA 2017–2018 数据 | 可下载 | 美国食物与较旧版本；化合物范围有限 | 推荐交叉验证与美国摄入估计 |
| USDA FoodData Central | 食物组成和消费映射 | 权威；Foundation Foods 2026-04，持续更新 | REST API、CSV/JSON 下载 | 多数非传统营养小分子覆盖不足；品牌数据异质 | 推荐做食品实体、营养背景及消费映射，不作为抗氧化全集 |
| EFSA Comprehensive DB/FoodEx2 | 欧洲分人群消费量和标准食物编码 | 权威；数据库 2024-12 更新，页面 2026 审核 | 仪表板/下载，自动化受接口限制 | 调查方法跨国异质、低报/误报 | 推荐暴露建模，保留国家与调查层级 |
| FooDB | 广覆盖候选发现与食物关联 | 混合整理/预测；bulk pre-release 1.0（2020），谱图 2022 | CSV/XML/JSON/SQL 下载；条款需核对 | 旧 bulk；预测与实测混合；出现不等于摄入 | 仅候选生成和交叉链接，定量值需原始证据验证 |
| PubChem | 结构标准化、同义词、BioAssay 线索 | 聚合+NCBI；持续更新，PubChem 2025 update | PUG REST/下载 | 聚合来源质量不同；BioAssay 命中不自动是 direct target | 强烈推荐结构主索引；assay 逐条复核 |
| ChEBI 2.0 | 化学本体、结构、类别和稳定 ID | 人工本体；月度发布、ontology nightly；2.0 于 2025 上线 | REST、TSV/SDF/OWL/PostgreSQL | 生物活性/食物暴露不是重点；覆盖不等于验证 | 推荐身份与分类辅助；与 PubChem 双向核验 |
| HMDB | 人体代谢物、生物流体、代谢酶线索 | 混合人工/预测；5.0（2022） | XML/SDF/MetaboCard 下载 | 预测结构/谱图与实测混合；版本较旧 | 推荐代谢物候选，人体浓度必须回原文 |
| Exposome-Explorer | 饮食暴露生物标志物与肠菌代谢物 | 人工整理；Release 4.0 引用可用，网站称持续更新 | 网页和 downloads | 覆盖由已发表 biomarker 研究决定；人群不均 | 推荐 human exposure/metabolite 支持，不替代疗效 |
| BindingDB | 定量 protein–ligand affinity | 人工整理+导入；2026-09 dump，更新至 2026-08-30 | TSV/SDF/MySQL 下载 | assay、构建体和活性类型异质；数据库记录不保证 T1 | 推荐直接靶点候选；回看 assay 和原文后定级 |
| ChEMBL | 生物活性与靶点候选 | 人工标准化；ChEMBL 36（2026-01） | API、SQLite/MySQL/PostgreSQL/SDF | target confidence 与 assay confidence 需过滤；IC50 不等于 binding | 推荐批量发现，按 assay/target confidence 和原文审核 |
| IUPHAR/BPS GtoPdb | 高质量药理配体–靶点关系 | 专家整理；2026.3 于 2026-09-16 发布 | REST、CSV/TSV、RDF、PostgreSQL | 天然食源分子覆盖较窄；药理靶点偏倚 | 强烈推荐高精度交叉验证 |
| PubChem BioAssay | assays 和活性线索 | 聚合；持续更新 | PUG REST/下载 | assay 层级、confirmatory 状态和干扰差异大 | 推荐发现；必须解析 assay type 和 counterscreen |
| UniProt | 蛋白身份、物种、功能和 accession | Swiss-Prot 人工+TrEMBL 自动；频繁发布 | REST/下载 | 功能注释不是化合物直接结合证据 | 强烈推荐靶点规范化，不用于独立证明关系 |
| DrugBank | 药物、代谢与靶点补充 | 商业/人工；5.1.22，2026 时 academic bulk 暂停 | 注册/许可；批量和自动化受限 | 药物偏倚、许可与可复现访问限制 | 仅辅助；不作为 pipeline 必需依赖 |
| CTD | 化学–基因调控和毒理关联 | 人工整理并含推断；通常月度更新 | 可下载 | interaction 多为表达/调控；inferred network 易被误作靶点 | 推荐 T4/关联层辅助，禁止自动归为 T1/T2 |
| STITCH 5 | 化学–蛋白网络发现 | 文献、数据库与预测整合；主要版本 5（2016） | 下载/API 曾提供；当前可用性需复核 | 旧、混合证据、网络分数非直接结合 | 仅候选发现和交叉检查 |
| SwissTargetPrediction | 预测候选靶点 | 相似性预测；公开模型/数据主要 2019 | 网页，validation dataset 可下；无稳定批量 API 保证 | 化学空间和训练集偏倚；相似分子共享信息 | 仅 T5，永不作为验证 |
| PDB | 结构结合证据 | 原始结构档案；持续更新 | API/下载 | 配体身份、晶体条件、共价/缓冲成分需检查 | 推荐 T1 结构证据，人工检查 density 与文献 |
| PubMed | 人体、机制、PK、安全与靶点原文检索 | MEDLINE+publisher records；持续更新 | E-utilities/API | 生物医学覆盖好但食品化学期刊可能缺失；发表偏倚 | 核心来源；保存完整检索式与日期 |
| Crossref | DOI 与书目信息补全 | 出版商元数据；动态 | REST API | 不是证据数据库；摘要和 PMID 不完整 | 推荐去重/元数据，不参与效应定级 |

正式来源组合建议：候选生成使用 Phenol-Explorer + USDA + FooDB + 区域成分库并用 PubChem/ChEBI 统一结构；暴露使用定量食物数据 × EFSA/WWEIA/各国调查；代谢物使用人体 PK 原文 + Phenol-Explorer/HMDB/Exposome-Explorer；直接靶点优先 GtoPdb、BindingDB、ChEMBL、PDB、PubChem BioAssay，随后回到原始实验；CTD/STITCH 用于 T4/发现，SwissTargetPrediction 与 docking 仅 T5。

审计发现的新要点：ChEBI 2.0 提供现代 REST 与月度数据产品；GtoPdb 2026.3 是本轮最新确认的专家整理版本；BindingDB 2026-09 bulk 可复现；FooDB 可下载 bulk 明显落后于当前年份；DrugBank academic bulk 在核查时暂停，不能设计成必要依赖；ROBINS-I V2 已于 2025-11 发布；Exposome-Explorer 对人体饮食生物标志物和肠菌代谢物比一般食物库更有价值。
