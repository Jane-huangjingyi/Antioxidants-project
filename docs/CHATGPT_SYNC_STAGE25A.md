# ChatGPT Sync — Stage 25A Unified Literature-Evidence Screening

Stage 25A 已在冻结的 157 个 aqueous candidates 上完成统一的 metadata-level literature/evidence screen。Primary metric 是 `antioxidant_independent_publication_N`，实际操作定义为 DOI/PMID/规范化标题去重后的 antioxidant/redox original-publication proxy；它不是 antioxidant potency、evidence quality 或 human efficacy。Europe PMC 用于文献元数据检索，OpenAlex 是唯一 citation source，retrieval date 为 2026-09-20。

OpenAlex 前置 audit 为 37/37 work matched、37/37 citation metadata available。全量纳入 41,967 条 original-publication records；40,233 条具有 DOI/PMID，40,193 条匹配 OpenAlex，因此 DOI/PMID→OpenAlex matching rate=99.90%，matched-work citation availability=100%。所有 class、publication-era 和 identity-complexity strata 均分别通过 95% 阈值。未匹配分类为：missing DOI/PMID 1,734；OpenAlex work not found 38；identifier mismatch 2；citation metadata unavailable 0；ambiguous match 0。没有混用其他 citation counts。

Primary Top10：Curcumin；L-Ascorbic acid；Quercetin；Epigallocatechin；Gallic acid；Epigallocatechin gallate；Salicylic acid；Rutin；Caffeic acid；Ferulic acid。Top20/30/40/50/60 累计 publication coverage 分别为 68.96%、79.95%、87.18%、91.42%、94.36%。Primary vs citation overlap 分别为 19/20、28/30、40/40、49/50、58/60；primary vs recent overlap 为 18/20、29/30、39/40、46/50、58/60。Citation/year 与主排名明显不一致，不能替代 primary metric。

建议下一阶段采用 provisional Top50 retrieval frame：它保留七个 aqueous panels、累计覆盖 91.4%、citation overlap 98%、recent overlap 92%。这不是 class-balanced quota，也不是最终 Top20。Top50 内必须继续依据 `Stage25B_status` 排除或人工裁决不适合 H-ORAC 的候选。全体 readiness 为 Ready 86、Conditional 45、Not suitable for H-ORAC ranking 24、Insufficient identity 2；11 个 candidate-universe issues 保留 HUMAN REVIEW REQUIRED，未静默修复。

最重要的未决风险是独立性和 endpoint 的全文复核。当前自动流程能可靠完成标题 identity anchor、publication type、redox topic、identifier/title deduplication 和 citation linkage，但不能证明 same cohort/same experiment 的论文完全独立，也不能对 41,967 条记录逐篇完成 full-text endpoint adjudication。因此 Stage 25A 输出应称为 provisional metadata-level research-density screen；进入 Stage 25B 前建议对 Top50 做双人分层抽样并在 rank-changing error 出现时重算。

核心文件：`data/Stage25A_Unified_Literature_Screening_Master.csv`；`data/Stage25A_Publication_Provenance.csv`；`data/Stage25A_Recommended_Stage25B_Shortlist_Top50.csv`；`data/Stage25A_Shortlist_Cutoff_Sensitivity.csv`；`data/Stage25A_Class_Representation_Sensitivity.csv`；`data/Stage25A_OpenAlex_Bulk_Coverage_By_Stratum.csv`；`data/Stage25A_OpenAlex_Bulk_Unmatched_Publications.csv`；`docs/Stage25A_Citation_Source_Audit_CN.md`；`docs/Supervisor_Stage25A_Unified_Screening_CN.md`；`figures/aqueous_antioxidant_atlas/10_unified_literature_screening/`。
