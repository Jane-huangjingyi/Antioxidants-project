# Files to upload to ChatGPT

## Priority 1

| filename | path | purpose | why needed | priority |
|---|---|---|---|---|
| H_ORAC_Provisional_Ranking.csv | data/H_ORAC_Provisional_Ranking.csv | 20 项 provisional 排名及置信度 | 审核名次、数值和限制 | Priority 1 |
| H_ORAC_Phenolic_Candidate_Universe.csv | data/H_ORAC_Phenolic_Candidate_Universe.csv | 50 项候选全集 | 审核范围、身份与缺失情况 | Priority 1 |
| H_ORAC_Provisional_Top20.png | figures/H_ORAC_Provisional_Top20.png | 主排序图 | 导师汇报的核心结果 | Priority 1 |
| Supervisor_H_ORAC_Top20_Update_CN.md | docs/Supervisor_H_ORAC_Top20_Update_CN.md | 1–2 页汇报稿 | 快速评议结论和下一步 | Priority 1 |
| H_ORAC_Top20_Sync_to_ChatGPT_CN.md | handoff/H_ORAC_Top20_Sync_to_ChatGPT_CN.md | 决策同步 | 保留解释边界与未决风险 | Priority 1 |

## Priority 2

| filename | path | purpose | why needed | priority |
|---|---|---|---|---|
| H_ORAC_Phenolic_Literature_Records.csv | data/H_ORAC_Phenolic_Literature_Records.csv | 原始研究级记录及排除项 | 追踪每个数值和 eligibility | Priority 2 |
| H_ORAC_Evidence_Confidence.png | figures/H_ORAC_Evidence_Confidence.png | 证据层级图 | 防止把高数值误当成高置信度 | Priority 2 |
| H_ORAC_Subclass_Coverage.png | figures/H_ORAC_Subclass_Coverage.png | 子类覆盖图 | 审核 candidate-generation bias | Priority 2 |

## Priority 3

| filename | path | purpose | why needed | priority |
|---|---|---|---|---|
| build_h_orac_top20.py | scripts/build_h_orac_top20.py | 可复现生成脚本 | 复核统计、排序和绘图逻辑 | Priority 3 |
| ORAC_Literature_Eligibility_Rubric.csv | config/ORAC_Literature_Eligibility_Rubric.csv | A/B1/B2/C/X 规则 | 深入方法学复核时使用 | Priority 3 |

