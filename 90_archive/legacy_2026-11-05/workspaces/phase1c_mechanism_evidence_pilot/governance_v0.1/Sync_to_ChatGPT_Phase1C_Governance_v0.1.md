# 同步ChatGPT：Phase1C治理规则 v0.1

2026-10-21。治理方案已整理为可审议文本，尚未人工批准，未实施数据迁移。推荐B结构：主观察表＋少量关联表，原evidence_id稳定；Publication、Experiment/Material与Observation分别表示出版物、设计/材料与检测比较，Review_Event独立追加。现Study_Register登记15个出版物，其中10篇支持21条纳入观察，不能称15个独立研究或21个独立实验。

建议增加独立target_confirmation_class（七类）、antioxidant_relevance_primary（六类）及可空受控secondary；dose_basis另列，来源核查范围/问题及测量层级、方向/显著性通过旁表治理。五种关系仍为名义类别，不做强弱单轴排名。单一抑制剂不自动证明特定蛋白必要性；敲除/补回不证明结合；Co-IP需区分蛋白–蛋白与小分子–蛋白；对接仍为计算。NRF2细胞补回不移用于动物6L，GSH下降是真实红氧观察但不是蛋白靶点。

共24项人工治理决策，15项建议优先批准原则、9项需讨论阈值/架构/责任及Gate政策；全部HUMAN_DECISION_REQUIRED，change_applied=NO。优先批准建议为GOV-01、04–07、09–10、12、14–18、20、24；讨论为GOV-02/03/08/11/13/19/21/22/23。没有规则已由Codex批准。“可优先批准”是审议建议，不是已获授权。

66字段中沿用Gate2的17项重点调整：compound_form、PubChem_CID、InChIKey、target_role、dose、dose_unit、evidence_relation_type、target_validation_status、functional_outcome、effect_context、source_verification_status、publication_date_precision、experiment_id、target_experimental_support、direct_target_status、human_review_status、publication_status。其余49字段全部保留并逐项给出映射/治理规则；优先级不是删字段许可，不能只加三列就视为完成迁移。

21条潜在影响逐ID记录于影响评估：保留Gate2的12暂定、2重分类提案、7来源HOLD；0人工批准、0确定具体直接结合支持。Akt及TYR两条关系收窄仍待逐行批准，HDAC1-005的NS表述另行收窄，SIRT3模型身份补全仅元数据提案。其他变化包括条件与剂量基准拆分、实验共享关联及独立性核查，不自动合并原experiment_id。190未检索候选仍NOT_SEARCHED/计数空白而非零证据；Phase1B风险不关闭。

建议状态：Gate1=HOLD；Gate2=HUMAN_SCIENTIFIC_REVIEW_REQUIRED；Scale-up暂定收集/已审纳入/分析排名/发布四权限均HOLD/NOT_AUTHORIZED；Release=HOLD。本轮提出完整验收规则，不宣布任何Gate通过。有限下一批暂定收集可作为日后单独审批事项，不以清空所有HOLD为唯一前提，也不允许绕过未定通用分类政策。

下一步仅为用户与ChatGPT共同审查24项规则，确定具名科学审核者、维护者和9项待讨论政策；之后另行授权副本迁移演练及21条人工科学复审。本轮完成后停止，不自动检索新候选物、不运行网络/排名/训练、不创建正式数据版本。此文是可转交材料，未自动向其他聊天发送。

## 完整相对路径转交清单

P0：`workspaces/phase1c_mechanism_evidence_pilot/governance_v0.1/Mechanism_Evidence_Governance_Decision_v0.1.md`

P0：`workspaces/phase1c_mechanism_evidence_pilot/governance_v0.1/Governance_Decision_Matrix_v0.1.csv`

P0：`workspaces/phase1c_mechanism_evidence_pilot/governance_v0.1/Sync_to_ChatGPT_Phase1C_Governance_v0.1.md`

P1：`workspaces/phase1c_mechanism_evidence_pilot/governance_v0.1/Mechanism_Evidence_Controlled_Vocabulary_v0.1.csv`

P1：`workspaces/phase1c_mechanism_evidence_pilot/governance_v0.1/Mechanism_Evidence_Entity_Relationship_Design_v0.1.md`

P1：`workspaces/phase1c_mechanism_evidence_pilot/governance_v0.1/Mechanism_Evidence_Gate_Criteria_v0.1.md`

P1：`workspaces/phase1c_mechanism_evidence_pilot/governance_v0.1/Mechanism_Evidence_Migration_Impact_Assessment_v0.1.md`

P2：`workspaces/phase1c_mechanism_evidence_pilot/governance_v0.1/Governance_QC_Report_v0.1.md`

必要QC附件同目录：`Start_Baseline.json`、`Governance_Validation_v0.1.json`、`validate_governance.mjs`、`.gitignore`。预览与依赖junction仅本地排除，不提交。

## Git与资产保护

起始main/HEAD d29a6936603886e654b3cdfb24ccd3a1e76cee23，工作树干净；在独立codex/phase1c-governance-v0.1分支生成本轮新增文件。Start_Baseline保存685个既有跟踪文件及41个本地来源文件SHA256，完成时逐项复核均不变；程序QC29项通过、0项失败，实际明细见Governance_Validation和QC报告。保护范围覆盖原21条/66字段/Master、T002/T004/T110、Phase1B、临时crosswalk、冻结Top20和157×5矩阵，以及既有来源缓存。本轮没有未经批准的科学数据变更。

本文件为提交前同步快照；实际commit SHA与push结果由最终回复及Git记录报告，避免在待提交文件中虚构自指提交哈希。按本轮明确授权仅提交治理文档及必要QC，不合并main。Git归档不是科学规则批准。
