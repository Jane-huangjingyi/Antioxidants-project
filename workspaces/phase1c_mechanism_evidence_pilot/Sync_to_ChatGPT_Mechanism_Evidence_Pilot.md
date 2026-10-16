# 同步ChatGPT：Phase1C机制证据数据库与原儿茶酸试点 v0.1

已读取Phase1B的T002_ReadOnly_Audit_Report_v0.1.md、Sync_to_ChatGPT_Phase1B_T002_v0.1_CN.md、527行T002_Identity_and_CrossTable_Match_Audit_v0.1.csv及14项T002_Scientific_Risk_Register_v0.1.csv。它们仅是审计结果，不是人工科学批准。

原儿茶酸试点关联T002第61条（文件第62行）：CID72、YQUVCSBJEUQKSH-UHFFFAOYSA-N、C7H6O4与PubChem公共接口一致；这是参考标识核对，不是人工样品结构审核。未发现阻止参考母体关联的重大冲突。

检索截止2026-10-16。Europe PMC广义检索3809条，机制优先514条；PubMed广义检索3322条（保存全部PMID）。不同数据库/查询重叠，不相加。按PMID及DOI诊断去重后保留3940条发现记录，实际审阅决策14条，未筛3926条。PubMed-only记录中部分只保留ID，未假称已读摘要。检索式、实际响应、失败503及修复后响应均保留。本轮是系统化检索后的优先样本试点，不是完成全部原儿茶酸文献的系统综述。筛选与逐实验提取均为PARTIAL。

纳入10篇按DOI/PMID去重的原始研究，21条观察，66字段；其中全文文本核查6篇/15条，摘要4篇/6条。独立出版物数10不代表已证明跨论文样本或实验完全独立。关系分布：{"COMPUTATIONAL_PREDICTION": 3, "DIRECT_BINDING": 2, "FUNCTIONAL_CAUSAL": 5, "OMICS_ASSOCIATION": 2, "PATHWAY_MODULATION": 9}。实验支持的可物种定位基因/蛋白共7个（[["GATA4", "Homo sapiens"], ["HDAC1", "Homo sapiens"], ["Kmo", "Mus musculus"], ["Nfe2l2", "Mus musculus"], ["Nos3", "Mus musculus"], ["RELA", "Homo sapiens"], ["Sirt3", "Mus musculus"]]），此口径包含表达/磷酸化读数，不等于直接靶点；组学单独列出，家族/物种未解决不强制映射。仅预测的命名基因1个：["TAS2R16"]。通路关联观察14条，作者命名轴/过程9类，标准通路ID核实0个，均不冒填KEGG/Reactome编号。

直接结合类别2条，但本版可确认的“全文核查且具体蛋白身份明确”的直接结合靶点为0：TRAF2论文只核查摘要，重组蛋白物种/剂量/对照待查；α-amylase ITC方法与Figure2B图注存在制备对象冲突，且物种/亚型未明确，保留HOLD。TAS2R16仅模拟；SIRT3和HDAC1的对接不能升级为实验结合。SIRT3、NRF2敲除支持模型内功能参与；Akt抑制剂支持药理参与但不能指定AKT1；HDAC1平行表型及非加和不等同必要性或救援。促氧化、高剂量GSH耗竭和无额外显著效应均保留，未筛掉阴性结果。

PMID26180584/DOI10.1155/2015/351827有2026撤稿关联（通知PMID41947015），两者不计有效研究。原儿茶酸乙酯PMID29129792不当作母体；LOX晶体中由quercetin生成PCA的研究PMID14705020暂缓形式/来源审查。Nature Food2021（10.1038/s43016-021-00243-7）仅作未来框架背景，未生成PPI、网络接近度或训练结果。

程序质控17项通过、0项失败；主表与单物质表字节一致，evidence_id唯一，191条覆盖索引中仅AFF-0061标为已检索但筛选部分，另190条NOT_SEARCHED且不填零证据。639个既有跟踪文件SHA256未变，开始/结束HEAD为dbad6d1f5ec7f96550e1fd9eb33a4d16d21a1d87，main分支。只新增本工作区，未commit/push。

所有记录为试点待审数据，不是人工批准的药物靶点目录。参考母体身份与每篇实验试剂鉴定分列，未改T002、T004、T110、既有字典、身份审核、临时映射、157×5矩阵或Frozen Top20。Phase1B的26/7/2、AFF-0082/AFF-0150缺失、155临时映射/2待审、21项字典缺口及Crosswalk/Phase2/Release HOLD均保持。

FULL_TEXT_VERIFIED表示已读正文方法、结果及相关图注/表注，不表示已独立逐像素核查图像、原始数据或补充材料；本版未做原始图像完整性审计。ABSTRACT_ONLY不填写推测剂量、对照、时长或Figure编号。需要具体剂量却尚未读出时保留UNRESOLVED，不填0。

未解决事项与人工顺序：先核查TRAF2原始全文、α-amylase方法/图注对象及试剂物种，随后复核遗传与药理因果界限、HDAC1非加和解释、KEAP1未逐浓度提取、旧促氧化研究的全文与对照，再核对蛋白/通路标准标识和所有逐图定位。随后确定原儿茶酸剩余筛选范围及跨研究实验独立性。尚不建议扩大到其他候选物；先完成本试点的Gate 2审查。

Gate 1：HOLD。附件未给出正式Gate 1判据，本轮只确认PROGRAMMATIC_QC=PASS，不替用户定义正式通过门槛；筛选/提取完整性、全文及关键身份问题仍开放。Gate 2：HUMAN_SCIENTIFIC_REVIEW_REQUIRED。Release：HOLD。Phase 2：HOLD。不可把程序通过解释为人工证据批准。

## 需要上传/转交的完整相对路径

补充P0：`Source_Review_Open_Items.md`，完整相对路径`workspaces/phase1c_mechanism_evidence_pilot/qc/Source_Review_Open_Items.md`。补充P1：`Final_Validation.json`，完整相对路径`workspaces/phase1c_mechanism_evidence_pilot/qc/Final_Validation.json`。最终独立验证20项通过、0项失败；初次构建17项检查另行保留。来源复读更正记录于上述P0文件。

- P0：`Sync_to_ChatGPT_Mechanism_Evidence_Pilot.md`；`workspaces/phase1c_mechanism_evidence_pilot/Sync_to_ChatGPT_Mechanism_Evidence_Pilot.md`
- P0：`Mechanism_Evidence_Pilot_QC_Report.md`；`workspaces/phase1c_mechanism_evidence_pilot/qc/Mechanism_Evidence_Pilot_QC_Report.md`
- P0：`AFF-0061_Protocatechuic_Acid_Mechanism_Evidence.csv`；`workspaces/phase1c_mechanism_evidence_pilot/compounds/AFF-0061_Protocatechuic_Acid_Mechanism_Evidence.csv`
- P0：`Study_Register.csv`；`workspaces/phase1c_mechanism_evidence_pilot/master/Study_Register.csv`
- P1：`Compound_Mechanism_Evidence_Master.csv`；`workspaces/phase1c_mechanism_evidence_pilot/master/Compound_Mechanism_Evidence_Master.csv`
- P1：`Mechanism_Evidence_Field_Dictionary.csv`；`workspaces/phase1c_mechanism_evidence_pilot/dictionaries/Mechanism_Evidence_Field_Dictionary.csv`
- P1：`Protocatechuic_Acid_Search_Log.csv`；`workspaces/phase1c_mechanism_evidence_pilot/search_logs/Protocatechuic_Acid_Search_Log.csv`
- P1：`Protocatechuic_Acid_Screening_Log.csv`；`workspaces/phase1c_mechanism_evidence_pilot/search_logs/Protocatechuic_Acid_Screening_Log.csv`
- P1：`Compound_Mechanism_Coverage.csv`；`workspaces/phase1c_mechanism_evidence_pilot/indexes/Compound_Mechanism_Coverage.csv`
- P2：`Mechanism_Evidence_User_Guide_CN.md`；`workspaces/phase1c_mechanism_evidence_pilot/docs/Mechanism_Evidence_User_Guide_CN.md`
- P2：`Counts_and_Checks.json`；`workspaces/phase1c_mechanism_evidence_pilot/qc/Counts_and_Checks.json`
- P2：`Compound_Identity_Check.json`；`workspaces/phase1c_mechanism_evidence_pilot/qc/Compound_Identity_Check.json`

完成后停止，未向其他聊天自动发送；请用户转交并共同审查。未经本轮新授权不commit/push，不自动进入其他候选物或Phase2。
