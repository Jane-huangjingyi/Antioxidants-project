# Files to Upload to ChatGPT

## Priority 1：必须上传，用于下一轮核心决策

| file name | full relative path | purpose | why ChatGPT needs it | priority |
|---|---|---|---|---|
| Antioxidant_Screening_Protocol_CN.md | docs/Antioxidant_Screening_Protocol_CN.md | 中文正式筛选方案 | 审核范围、纳排、评分和阶段边界 | Priority 1 |
| Evidence_Hierarchy_and_Scoring_Rubric.csv | config/Evidence_Hierarchy_and_Scoring_Rubric.csv | 证据层级与分值锚点 | 冻结 H/A/M/T/F/S 操作定义 | Priority 1 |
| Candidate_Universe_Data_Dictionary.csv | config/Candidate_Universe_Data_Dictionary.csv | 候选主表字段规范 | 审核 Phase 2 自动化输入与缺失规则 | Priority 1 |
| Phase_0_1_Decision_Log_CN.md | docs/Phase_0_1_Decision_Log_CN.md | 已冻结与开放决策 | 对未冻结阈值和治理规则作决定 | Priority 1 |
| Sync_to_ChatGPT_CN.md | handoff/Sync_to_ChatGPT_CN.md | 阶段交接摘要 | 快速理解成果、风险、修改和下一步 | Priority 1 |

## Priority 2：建议上传，用于规则核查

| file name | full relative path | purpose | why ChatGPT needs it | priority |
|---|---|---|---|---|
| Target_Evidence_Classification_CN.md | docs/Target_Evidence_Classification_CN.md | T1–T5 中文判定规则 | 核查 direct/functional/regulated/predicted 边界 | Priority 2 |
| Compound_Target_Data_Dictionary.csv | config/Compound_Target_Data_Dictionary.csv | 靶点表 schema | 验证 Phase 3 是否可执行和可审计 | Priority 2 |
| Compound_Context_Interaction_Data_Dictionary.csv | config/Compound_Context_Interaction_Data_Dictionary.csv | 协同/拮抗 schema | 核查 interaction model 与 context 字段 | Priority 2 |
| Database_and_Literature_Source_Audit_CN.md | docs/Database_and_Literature_Source_Audit_CN.md | 数据源版本、用途和偏倚审计 | 决定正式数据栈与可复现访问方案 | Priority 2 |

## Priority 3：仅在进一步检查时需要

| file name | full relative path | purpose | why ChatGPT needs it | priority |
|---|---|---|---|---|
| Antioxidant_Screening_Protocol_EN.md | docs/Antioxidant_Screening_Protocol_EN.md | 英文对应 protocol | 双语一致性或英文协作审查 | Priority 3 |
| Target_Evidence_Classification_EN.md | docs/Target_Evidence_Classification_EN.md | 英文靶点规则 | 国际协作或术语复核 | Priority 3 |
| Database_and_Literature_Source_Audit_EN.md | docs/Database_and_Literature_Source_Audit_EN.md | 英文来源审计 | 国际协作与英文核查 | Priority 3 |
| Phase_0_1_Decision_Log_EN.md | docs/Phase_0_1_Decision_Log_EN.md | 英文决策日志 | 英文审计和共享 | Priority 3 |
| core_methodology_import.bib | handoff/core_methodology_import.bib | 本轮 Zotero 导入记录 | 复核或迁移核心引文元数据 | Priority 3 |
