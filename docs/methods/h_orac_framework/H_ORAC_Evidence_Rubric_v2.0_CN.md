# H-ORAC Evidence Rubric v2.0 — CANONICAL

本规范自2026-09-22起为canonical H-ORAC-FL evidence rubric。核心架构为 universal assay-comparability core + compound-specific risk-triggered enhanced QC + independent QC/reporting flags。Tier与flags分离；缺少numerical purity不自动等于B2。

Universal core要求：defined pure-compound identity/form；AAPH–fluorescein–Trolox aqueous/buffer construct；buffer、pH、temperature及reagent concentrations显式、无歧义可推导或完全可追溯；candidate concentration/range；stock与final solvent可解释；kinetic fluorescence decay及net-AUC或等价kinetic calculation；original value、unit及mol TE/mol conversion可重建；replication/precision足以解释。

证据状态严格区分`EXPLICITLY_REPORTED`、`DERIVABLE_FROM_METHOD`、`TRACEABLE_TO_REFERENCED_PROTOCOL`、`NOT_REPORTED`、`UNCLEAR`。引用protocol本身不自动补齐条件。

R1 optical、R2 solubility/aggregation、R3 cosolvent、R4 redox/probe-interaction仅在客观trigger下要求enhanced QC。R1的“UV-visible chromophore且assay concentration >10 µM”仅为operational screening trigger；10 µM不是validated universal optical-interference threshold，浓度本身不得导致降级。R2必须优先使用可追溯solubility、logP/logD、assay concentration、precipitation/turbidity、dose response与stock-solvent evidence；证据不足记`UNCLEAR`，不得凭结构印象判LOW。

Tier A：core完整且所有triggered QC通过。Tier B1：core足以定量比较且无未解决material risk，但仍有报告限制。Tier B2：存在定量H-ORAC-like value但material comparability risk未解决，只用于sensitivity。Tier C：construct/arm/probe/radical/normalization已知不兼容。Tier X：source、identity、method或quantitative provenance不足。Canonical machine-readable rules见`methods_qc/config/ORAC_Literature_Eligibility_Rubric_v2.0.csv`与`H_ORAC_Compound_Risk_Trigger_Rules_v1.0.csv`。
