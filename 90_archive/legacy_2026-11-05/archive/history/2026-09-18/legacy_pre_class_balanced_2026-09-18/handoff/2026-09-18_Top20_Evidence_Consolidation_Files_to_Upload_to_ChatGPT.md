# Files to upload to ChatGPT

## Priority 1

| filename | path | purpose | why needed | priority |
|---|---|---|---|---|
| Top20_Ranking_Before_After.csv | data/Top20_Ranking_Before_After.csv | 排名与置信度变化 | 审核榜单是否稳定 | Priority 1 |
| Target_Mapping_Shortlist_v0.1.csv | data/Target_Mapping_Shortlist_v0.1.csv | 分层 shortlist | 决定下一阶段范围 | Priority 1 |
| Top20_Evidence_Consolidation_Results_CN.md | docs/Top20_Evidence_Consolidation_Results_CN.md | 完整科学解释 | 审核结论和边界 | Priority 1 |
| Supervisor_Top20_Evidence_Consolidation_CN.md | docs/Supervisor_Top20_Evidence_Consolidation_CN.md | 导师版 | 阶段汇报 | Priority 1 |
| Top20_Before_After_Rank_Comparison.png | figures/Top20_Before_After_Rank_Comparison.png | 排名变化图 | 直观看新增证据影响 | Priority 1 |

## Priority 2

| filename | path | purpose | why needed | priority |
|---|---|---|---|---|
| Top20_Evidence_Consolidation_Records.csv | data/Top20_Evidence_Consolidation_Records.csv | 研究级证据与独立实验ID | 复核 eligibility、单位和来源 | Priority 2 |
| High_Importance_Missing_ORAC_Candidates.csv | data/High_Importance_Missing_ORAC_Candidates.csv | 关键缺失候选 | 评估系统性低覆盖 | Priority 2 |
| Top20_B1_Evidence_Depth.png | figures/Top20_B1_Evidence_Depth.png | B1深度图 | 区分排名与证据稳定性 | Priority 2 |
| Missing_Key_Phenolics_ORAC_Status.png | figures/Missing_Key_Phenolics_ORAC_Status.png | 关键缺失状态图 | 审核 EGCG/花色苷/木脂素结论 | Priority 2 |
| Top20_Evidence_Consolidation_Sync_to_ChatGPT_CN.md | handoff/Top20_Evidence_Consolidation_Sync_to_ChatGPT_CN.md | 决策同步 | 保留全部变更和风险 | Priority 2 |

## Priority 3

| filename | path | purpose | why needed | priority |
|---|---|---|---|---|
| Top20_Evidence_Change_Log_CN.md | docs/Top20_Evidence_Change_Log_CN.md | 变更审计 | 追踪新增、排除和纠错 | Priority 3 |
| build_top20_consolidation.py | scripts/build_top20_consolidation.py | 可复现脚本 | 复核统计和绘图实现 | Priority 3 |

