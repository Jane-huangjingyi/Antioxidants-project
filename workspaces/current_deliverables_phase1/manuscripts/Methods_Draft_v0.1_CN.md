# Methods Draft v0.1 CN
DRAFT | 2026-10-16 | Baseline 24653d04f4b96849bdcc57039aecfb3cda99da4f
状态标签区分已完成方法、已观察结果、已批准未实施规则、计划分析和未核实细节。

## 1 研究设计与数据库范围

本数据库以文献证据为基础，按化学构念组织数据。全类别背景表包含九个分析面板的191条记录，当前水相分析纳入七个面板的157种候选物，两者属于不同分析范围。本轮没有将191条记录重新认定为经身份去重的191种化合物，也未把不同实验方法合成为通用效力分数。[COMPLETED_METHOD]

来源：[Source](D:/JANE/GitHub/antioxidants%20project/data/candidate_universe/Antioxidant_Class_Candidate_Master.csv); [Source](D:/JANE/GitHub/antioxidants%20project/data/candidate_universe/Aqueous_Antioxidant_Candidate_Master.csv); [Source](D:/JANE/GitHub/antioxidants%20project/docs/methods/Antioxidant_Functional_Factor_Taxonomy_CN.md)

## 2 候选物识别与分类

候选身份通过项目标识、首选及来源保留名称、PubChem标识、InChIKey和化学形式组织。水相表compound字段对应筛选主表canonical_name。本轮仅在只读关联核查中规范化CID尾随的.0，结构标识组合一致。现有身份审计仍有两项未解决，157项中文名尚未校订。已批准的宽食物来源准入规则与测定适用性、暴露和安全评价分别处理。[COMPLETED_METHOD；身份细节UNVERIFIED]

来源：[Source](D:/JANE/GitHub/antioxidants%20project/data/candidate_universe/Antioxidant_Class_Candidate_Master.csv); [Source](D:/JANE/GitHub/antioxidants%20project/data/candidate_universe/Aqueous_Antioxidant_Candidate_Master.csv); [Source](D:/JANE/GitHub/antioxidants%20project/data/literature_screening/master/Literature_Screening_Candidate_Master.csv); [Source](D:/JANE/GitHub/antioxidants%20project/data/framework/Candidate_Identity_and_Synonym_Audit.csv); [Source](D:/JANE/GitHub/antioxidants%20project/docs/qc/Stage25A1_Human_Review_Resolution_CN.md)

## 3 文献检索

Stage25A元数据筛选保留Europe PMC检索式，检索日期为2026年9月20日；引用信息由OpenAlex按已记录的标识符匹配审计提供。候选物与论文来源表保留文献标识、筛选决策和引用信息检索记录。随后在暂定Top50中完成方法适用性审查，形成47种候选物的H-ORAC检索框架，初始检索日志日期为2026年9月21日。后续定点来源恢复单独记录；这些日期不证明全文裁决完成或达到VSIR的SEARCH_COMPLETE。[COMPLETED_METHOD]

来源：[Source](D:/JANE/GitHub/antioxidants%20project/data/literature_screening/master/Literature_Screening_Candidate_Master.csv); [Source](D:/JANE/GitHub/antioxidants%20project/data/literature_screening/provenance/Literature_Screening_Publication_Provenance.csv); [Source](D:/JANE/GitHub/antioxidants%20project/data/literature_screening/qc/Literature_Screening_Literature_Search_Log.csv); [Source](D:/JANE/GitHub/antioxidants%20project/data/h_orac_stage25b/stage25b/Stage25B_HORAC_Search_Log.csv); [Source](D:/JANE/GitHub/antioxidants%20project/docs/qc/Stage25A_Citation_Source_Audit_CN.md)

## 4 证据资格

既有定量记录采用H-ORAC Evidence Rubric v2.0，以测定可比性核心和客观触发的化合物特定检查进行分层。主集合使用A和B1，B2仅用于敏感性分析，C或X不进入主汇聚。VSIR v1.0科学设计另行条件性冻结，以可核查性、统计有效性、独立性和可复现性界定纯化合物H-ORAC-FL证据资格，至少要求两项符合要求且真正独立的原始研究。自动GO或NO-GO还要求SEARCH_COMPLETE及EVIDENCE_CLOSED；关键证据未闭环或存在重大争议时进入HOLD与人工复核。VSIR实施及12项边界测试尚未执行。[既有v2为COMPLETED_METHOD；VSIR为APPROVED_NOT_IMPLEMENTED]

来源：[Source](D:/JANE/GitHub/antioxidants%20project/docs/methods/h_orac_framework/H_ORAC_Evidence_Rubric_v2.0_CN.md); [Source](D:/JANE/GitHub/antioxidants%20project/docs/methods/h_orac_framework/Stage25B_HORAC_Selection_and_Ranking_Method_Final_CN.md)

## 5 数据提取

实验表按候选物与实验记录组织，保留测定身份、材料形式、原值和单位、原文位置、溶剂与对照、换算信息及复核标记。文献标识和实验标识支持导航，但本身不证明研究独立性。来源缺失或不确定的信息保持显式记录。本轮交付制作读取既有抽取表，没有开展新的全文抽取工作。[COMPLETED_METHOD]

来源：[Source](D:/JANE/GitHub/antioxidants%20project/data/h_orac_stage25b/stage25b/Stage25B_HORAC_Experiment_Evidence.csv); [Source](D:/JANE/GitHub/antioxidants%20project/methods_qc/config/ORAC_Literature_Extraction_Data_Dictionary.csv)

## 6 数据标准化

仅当原始尺度和受测化学形式允许可重建换算时，H-ORAC结果以mol Trolox equivalents/mol compound表示。原值若为micromol TE/g，则乘以对应摩尔质量并除以一百万得到mol TE/mol。原值、原单位和换算公式分别保存。固定浓度AUC、羟自由基HORAC及其他测定构念在缺少有效标定与科学桥接时不换算；未知误差类型不改称SD或SE。[COMPLETED_METHOD]

来源：[Source](D:/JANE/GitHub/antioxidants%20project/data/h_orac_stage25b/stage25b/Stage25B_HORAC_Experiment_Evidence.csv); [Source](D:/JANE/GitHub/antioxidants%20project/docs/methods/h_orac_framework/H_ORAC_Evidence_Rubric_v2.0_CN.md); [Source](D:/JANE/GitHub/antioxidants%20project/data/h_orac_stage25b/stage25b6d/Stage25B6D_Error_and_Replicate_Audit.csv)

## 7 统计分析

既有主排名按合格A加B1记录的中位数汇总，来源计数、范围和离散性作为描述信息保留。本轮在不修改表格的情况下独立复算28个中位数。数值误差覆盖及已核实类型按记录计数，技术重复与独立研究数分开处理。由于误差定义和实验单位尚不完整，本轮未计算候选物置信区间、排名概率或荟萃效应量。后续模型需另行预设分析方案。[COMPLETED_METHOD；后续模型为PLANNED]

来源：[Source](D:/JANE/GitHub/antioxidants%20project/data/h_orac_stage25b/stage25b/Stage25B_HORAC_Quantitative_Ranking.csv); [Source](D:/JANE/GitHub/antioxidants%20project/data/h_orac_stage25b/stage25b/Stage25B_HORAC_Experiment_Evidence.csv); [Source](D:/JANE/GitHub/antioxidants%20project/data/h_orac_stage25b/stage25b6d/Stage25B6D_Error_and_Replicate_Audit.csv)

## 8 研究独立性

来源级和候选级审计区分原始实验贡献、综述引用、数据复用与研究内重复。现有6D表记录局部原始来源核查及其历史门槛下的候选资格。两个不同DOI或多个测量孔不自动证明研究独立，6D的PASS_VERIFIED不能转换为VSIR GO。本轮没有实施新的正式独立性门槛，也未赋予新的候选资格。[局部审计为COMPLETED_METHOD；VSIR为APPROVED_NOT_IMPLEMENTED]

来源：[Source](D:/JANE/GitHub/antioxidants%20project/data/h_orac_stage25b/stage25b6d/Stage25B6D_Source_Closure.csv); [Source](D:/JANE/GitHub/antioxidants%20project/data/h_orac_stage25b/stage25b6d/Stage25B6D_Candidate_Eligibility.csv); [Source](D:/JANE/GitHub/antioxidants%20project/data/h_orac_stage25b/stage25b6d/Stage25B6D_Study_Independence_Adjudication.csv)

## 9 证据核查

结构、文件完整性、算术、原文解释和独立复核分别登记。来源闭环表反映此前全文核查结果，本轮未重新裁决全部原文。CR原始记录保留。研究者确认CR-001至CR-016已在对话完成裁决，但本轮输入没有各项完整裁决内容，因此建立决策缺口登记，不从旧提案推断结果。[COMPLETED_METHOD；个别裁决细节UNVERIFIED]

来源：[Source](D:/JANE/GitHub/antioxidants%20project/data/h_orac_stage25b/stage25b6d/Stage25B6D_Source_Closure.csv); [Source](D:/JANE/GitHub/antioxidants%20project/data/h_orac_stage25b/stage25b6d/Stage25B6D_Proposed_Change_Requests.csv); [Source](D:/JANE/GitHub/antioxidants%20project/docs/methods/h_orac_framework/Two_Reviewer_QC_Rules_CN.md)

## 10 排名与综合

Stage25B.5 Frozen Top20 v1.0继续作为正式历史化学容量成果，A加B1顺序仅在已裁决证据范围内解释，并伴随B2敏感性结果。D1至D5框架在食品配料开发、营养健康干预和机制研究场景下，分别评价活性、可靠性、成熟度、生物学相关性与应用可行性。本轮不生成综合分数、综合Top20或跨场景最终排名。今后经验证的VSIR GO表示证据资格，也不自动建立跨研究定量可比性。[既有排名为COMPLETED_METHOD；后续综合为PLANNED]

来源：[Source](D:/JANE/GitHub/antioxidants%20project/data/h_orac_stage25b/frozen/Stage25B_Frozen_Primary_HORAC_Top20.csv); [Source](D:/JANE/GitHub/antioxidants%20project/data/framework/Comprehensive_Antioxidant_Indicator_Dictionary_v0.1.csv); [Source](D:/JANE/GitHub/antioxidants%20project/data/framework/Application_Scenario_Applicability_Matrix.csv)

## 11 可复现性

本轮制作基线为提交24653d04f4b96849bdcc57039aecfb3cda99da4f。源路径和内容按该提交核对，行尾不同时分别记录本地字节与Git blob哈希；制作前后比对既有受跟踪文件哈希，并按十项清单检查冻结包。结构和算术通过不表示所有历史分析均能重跑：归档脚本仍保留当时环境与路径假设，完整锁定的端到端环境尚未验证。[所述检查为COMPLETED_METHOD；历史重跑为UNVERIFIED]

来源：[Source](D:/JANE/GitHub/antioxidants%20project/data/h_orac_stage25b/stage25b/Stage25B_HORAC_Experiment_Evidence.csv); [Source](D:/JANE/GitHub/antioxidants%20project/data/h_orac_stage25b/frozen/Stage25B5_Frozen_Asset_SHA256_Manifest.csv); [Source](D:/JANE/GitHub/antioxidants%20project/archive/HISTORY_NAVIGATION_CN.md)
