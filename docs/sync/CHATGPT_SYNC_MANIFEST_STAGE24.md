# Stage 24 完成后，请把以下文件发给 ChatGPT

本清单只引用 Stage 24B 清理后实际存在的文件。已归档图不应上传。

## Priority 1 — 必须发送

- `docs/supervisor/Supervisor_Aqueous_Ranking_Progress_CN.md` — Stage 24 scientific summary
- `data/supervisor/Supervisor_Aqueous_Class_Ranking_Overview.csv` — Class/subpanel ranking overview
- `data/class_specific_antioxidant/Aqueous_Antioxidant_Primary_Literature_Evidence.csv` — Record-level DOI-traceable evidence
- `data/class_specific_antioxidant/Aqueous_Antioxidant_Paper_Summary.csv` — Paper-level evidence summary
- `data/class_specific_antioxidant/Stilbenes_Lignans_Evidence_Master.csv` — New class evidence master
- `data/class_specific_antioxidant/Stilbenes_Lignans_TopN_v1.0.csv` — Stilbenes/lignans Top available
- `data/class_specific_antioxidant/Betalains_Nitrogen_Profile_Evidence.csv` — Betalain profile evidence
- `data/class_specific_antioxidant/Organosulfur_Redox_Profile.csv` — Organosulfur redox profile
- `data/class_specific_antioxidant/Other_Aqueous_Phytochemicals_Evidence_Master.csv` — Other-aqueous evidence master
- `data/class_specific_antioxidant/Other_Aqueous_Phytochemicals_TopN_v1.0.csv` — Other-aqueous coherent-subpanel Top available
- `data/metal_and_micronutrients/Aqueous_Metal_Redox_Evidence.csv` — Metal mechanism evidence
- `data/metal_and_micronutrients/Antioxidant_Micronutrient_Redox_Profile_v2.csv` — Micronutrient profile
- `figures/FIGURE_INDEX_CN.md` — Canonical figure definitions and caveats

## Priority 2 — 建议发送的 canonical figures

- `figures/aqueous_antioxidant_atlas/00_overview/Aqueous_All_Classes_Ranking_Overview.png` — Canonical scientific figure
- `figures/aqueous_antioxidant_atlas/00_overview/Aqueous_Class_Coverage_Overview.png` — Canonical scientific figure
- `figures/aqueous_antioxidant_atlas/00_overview/Aqueous_Metal_Redox_Framework.png` — Canonical scientific figure
- `figures/aqueous_antioxidant_atlas/00_overview/Aqueous_Primary_Literature_Coverage.png` — Canonical scientific figure
- `figures/aqueous_antioxidant_atlas/01_class_specific_antioxidant_ranking/stilbenes_lignans/Stilbenes_Lignans_TopN.png` — Canonical scientific figure
- `figures/aqueous_antioxidant_atlas/01_class_specific_antioxidant_ranking/betalains/Betalains_Profile_Comparison.png` — Canonical scientific figure
- `figures/aqueous_antioxidant_atlas/01_class_specific_antioxidant_ranking/organosulfur/Organosulfur_Redox_Mechanism_Profile.png` — Canonical scientific figure
- `figures/aqueous_antioxidant_atlas/01_class_specific_antioxidant_ranking/other_aqueous_phytochemicals/Other_Aqueous_TopN.png` — Canonical scientific figure
- `figures/aqueous_antioxidant_atlas/02_metal_and_micronutrients/metal_redox/Metal_Chelation_or_Fenton_Evidence_Profile.png` — Canonical scientific figure
- `figures/aqueous_antioxidant_atlas/02_metal_and_micronutrients/micronutrients/Micronutrient_Redox_Profile.png` — Canonical scientific figure

## Priority 3 — 方法审计时可选

- `Antioxidant_Project_MASTER_HISTORY_AND_WORKFLOW_CN.md` — Method evolution and project history
- `docs/PROJECT_STAGE_INDEX_CN.md` — Stage status audit
- `archive/R_legacy/plot_antioxidant_atlas_pre_modularization.R` — Canonical plotting logic
- `figures/FIGURE_INVENTORY_AUDIT.csv` — Figure-level deduplication audit
- `archive/figure_redundancy_stage24/ARCHIVED_FIGURES_MANIFEST.csv` — Archived-figure provenance

## 不需要发送

- `archive/figure_redundancy_stage24/` 下的重复图。
- 旧 lipid/global overview、intermediate search logs、temporary CSV、Zotero cache。
- raw PDFs；只有某一 HUMAN REVIEW issue 需要核对全文时再提供。

## Minimal Sync Package

上传数量受限时，发送全部 Priority 1 文件，加以下四张 overview：

- `figures/aqueous_antioxidant_atlas/00_overview/Aqueous_All_Classes_Ranking_Overview.png`
- `figures/aqueous_antioxidant_atlas/00_overview/Aqueous_Class_Coverage_Overview.png`
- `figures/aqueous_antioxidant_atlas/00_overview/Aqueous_Primary_Literature_Coverage.png`
- `figures/aqueous_antioxidant_atlas/00_overview/Aqueous_Metal_Redox_Framework.png`
