# H-ORAC Screening Pipeline

新成员先读 `docs/MASTER_H_ORAC_SCREENING_PIPELINE_v1.0_CN.md`，再读 `docs/H_ORAC_Pipeline_Tutorial_CN.md`。实际执行依次使用 SOP_01 至 SOP_11；无AI环境直接按 `docs/NO_AI_MANUAL_EXECUTION_GUIDE_CN.md` 安排工作。

开始前复制五个模板：record extraction、compound summary、literature search log、exclusion log和ranking change log。每篇文献同时使用 `checklists/ORAC_Eligibility_Checklist_CN.md`。身份、tier、原值、换算、独立性和排名变更必须遵守 `docs/Two_Reviewer_QC_Rules_CN.md`。

脚本与输入输出对应关系见 `docs/Pipeline_Script_Map_CN.md`。现有脚本用于复现本项目历史版本，不能替代检索与人工判级。目录放置、版本和归档分别见 `Recommended_Project_Folder_Structure_CN.md` 与 `Versioning_and_Audit_Rules_CN.md`。

最终必须产生：candidate universe、search log、record table、exclusion log、compound summary、provisional ranking、confidence、consolidation records、before/after、change log和分层shortlist。自检标准：每个rank能沿 `Data_Provenance_Chain_CN.md` 回到原文；所有排除有原因；旧值未覆盖；派生值可重算；双人复核完成。已知缺口先查 `Pipeline_Gaps_and_Inconsistencies_CN.md`，不得自行静默修复。
