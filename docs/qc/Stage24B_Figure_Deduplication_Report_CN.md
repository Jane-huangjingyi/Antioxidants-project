# Stage 24B Figure Deduplication Report

本轮只清理 derived figure deliverables；ranking、TopN、evidence tier、primary construct、DOI、confidence、stability、candidate universe和human-review decisions均未改变。

原始 PNG 总数为 **33**；最终 active canonical PNG 为 **23**；归档重复图 **10**，另归档重复derived status summaries **2**；其中 exact duplicate **1**、highly redundant **7**、partially redundant **2**。各目录 active PNG 数为：00_overview=4; 01_flavonoids=3; 02_phenolic_acids=3; 03_stilbenes_lignans=3; 04_water_soluble_vitamins=1; 05_betalains=1; 06_organosulfur=1; 07_other_aqueous_phytochemicals=3; 08_metal_chelation=1; 09_micronutrients=3。所有正式目录均非空；singleton Vitamin C 保留 literature-coverage figure和状态说明，不保留无信息增益的Top1图。active aqueous folder中不存在lipid-phase figure。

Overview最终保留 `Aqueous_All_Classes_Ranking_Overview.png`、`Aqueous_Class_Coverage_Overview.png`、`Aqueous_Primary_Literature_Coverage.png` 和 `Aqueous_Metal_Redox_Framework.png`。Metal层保留overview framework与更综合的`Metal_Chelation_or_Fenton_Evidence_Profile.png`。Micronutrient prooxidant-context图含profile与enzyme map没有的独立风险信息，因此继续保留。

`archive/history/2026-09-20/R_legacy/2026-09-20_plot_antioxidant_atlas_pre_modularization.R` 默认 `GENERATE_LEGACY_FIGURES <- FALSE`，不再生成归档图；如需重建历史Phase 2–22图必须人工显式启用。ChatGPT人类可读和机器可读sync manifests均已生成。

## HUMAN REVIEW REQUIRED — FIGURE DEDUPLICATION

本轮未发现无法确认来源的PNG、跨construct raw-value overview或“归档后导致唯一科学结果丢失”的情形，因此没有新增必须阻断清理的figure-deduplication裁决。Stage 24原有candidate identity/scope和metal/pigment方法学human-review事项保持不变。
