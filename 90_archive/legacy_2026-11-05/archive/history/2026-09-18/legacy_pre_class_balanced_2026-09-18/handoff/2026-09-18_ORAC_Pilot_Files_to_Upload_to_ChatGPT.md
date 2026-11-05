# ORAC Pilot files to upload to ChatGPT

## Priority 1：必须上传

| filename | path | purpose | why needed | priority |
|---|---|---|---|---|
| Candidate_Scope_Definition_CN.md | docs/Candidate_Scope_Definition_CN.md | 冻结中文候选 taxonomy 与 H/L/special-case 规则 | 决定后续“排哪些化合物” | Priority 1 |
| ORAC_Pilot_Raw_Extraction.csv | data/ORAC_Pilot_Raw_Extraction.csv | 11 条原始 ORAC-FL 逐记录数据与出处 | 审核每个数值、方法字段和 Tier B 判定 | Priority 1 |
| ORAC_Pilot_TierA_Analysis.csv | data/ORAC_Pilot_TierA_Analysis.csv | 17 个候选的 A/B/C/X coverage 与 Tier A 汇总 | 直接判断是否能正式排名 | Priority 1 |
| ORAC_Pilot_Results_CN.md | docs/ORAC_Pilot_Results_CN.md | 中文结果、风险和十五项结论 | 供研究者决定是否扩展或统一复测 | Priority 1 |
| ORAC_Literature_Coverage.png | figures/ORAC_Literature_Coverage.png | 各候选 coverage 图 | 直观显示 Tier A 缺失与数据集中位置 | Priority 1 |
| ORAC_Pilot_Sync_to_ChatGPT_CN.md | handoff/ORAC_Pilot_Sync_to_ChatGPT_CN.md | 决策摘要与 Zotero 清单 | 快速定位下一步拍板事项 | Priority 1 |

## Priority 2：建议上传

| filename | path | purpose | why needed | priority |
|---|---|---|---|---|
| Candidate_Scope_Definition_EN.md | docs/Candidate_Scope_Definition_EN.md | 英文候选范围 | 双语科学术语核查 | Priority 2 |
| ORAC_Pilot_Results_EN.md | docs/ORAC_Pilot_Results_EN.md | 英文 pilot 结果 | 英文审核和对外沟通 | Priority 2 |
| H_ORAC_Historical_Distribution.png | figures/H_ORAC_Historical_Distribution.png | H-arm coverage diagnostic | 说明为何不能绘制 Tier A distribution/ranking | Priority 2 |
| L_ORAC_Historical_Distribution.png | figures/L_ORAC_Historical_Distribution.png | L-arm coverage diagnostic | 显示 tocopherol 单研究覆盖及 carotenoid 缺口 | Priority 2 |
| CUPRAC_Coverage_Summary.csv | data/CUPRAC_Coverage_Summary.csv | CUPRAC secondary coverage | 决定是否启动 CUPRAC 二次 extraction | Priority 2 |
| One_Sentence_Candidate_Scope_CN.md | docs/One_Sentence_Candidate_Scope_CN.md | 导师版候选范围标准 | 统一候选范围表述 | Priority 2 |

## Priority 3：进一步核查时上传

| filename | path | purpose | why needed | priority |
|---|---|---|---|---|
| One_Sentence_Candidate_Scope_EN.md | docs/One_Sentence_Candidate_Scope_EN.md | 英文一句话标准 | 英文简报时使用 | Priority 3 |
| ORAC_Literature_Eligibility_Rubric.csv | config/ORAC_Literature_Eligibility_Rubric.csv | A/B/C/X 判定标准 | 复核为何没有 Tier A | Priority 3 |
| ORAC_Literature_Extraction_Data_Dictionary.csv | config/ORAC_Literature_Extraction_Data_Dictionary.csv | 字段定义 | 检查后续自动化可行性 | Priority 3 |
| orac_pilot_import.bib | handoff/orac_pilot_import.bib | 本轮 Zotero 导入记录 | 文献管理审计时使用 | Priority 3 |
