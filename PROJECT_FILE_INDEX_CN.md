# Antioxidants Project 当前文件导航

当前科学主线是 candidate universe → class-specific antioxidant characterization → unified literature screen → Stage25B H-ORAC-FL → future Top20。本文件回答“当前文件在哪里、哪个是 canonical”；历史顺序请查 `docs/PROJECT_STAGE_INDEX_CN.md`。

| 我要查阅的内容 | 当前 canonical 位置 |
|---|---|
| 157 aqueous candidate universe | `data/candidate_universe/Aqueous_Antioxidant_Candidate_Master.csv` |
| 全类别 candidate master | `data/candidate_universe/Antioxidant_Class_Candidate_Master.csv` |
| 类别内 ranking/profile | `data/class_specific_antioxidant/` |
| H-ORAC evidence master | `data/class_specific_antioxidant/Aqueous_Antioxidant_Primary_Literature_Evidence.csv` |
| Stage25A 157-row master | `data/literature_screening/master/Literature_Screening_Candidate_Master.csv` |
| 论文 provenance | `data/literature_screening/provenance/Literature_Screening_Publication_Provenance.csv` |
| Provisional Top50 | `data/literature_screening/shortlist/Literature_Screening_Provisional_Top50.csv` |
| Stage25B retrieval candidates | `data/literature_screening/shortlist/Stage25B_HORAC_Retrieval_Eligible_Candidates.csv` |
| Top50 targeted QC | `data/literature_screening/qc/Top50_PreStage25B_QC.csv` |
| Metal/redox 与 micronutrients | `data/metal_and_micronutrients/` |
| 当前方法与 taxonomy | `docs/methods/` |
| 早期仍有效的 H-ORAC SOP | `docs/methods/h_orac_framework/` |
| 导师汇报文件 | `docs/supervisor/` |
| ChatGPT 同步文件 | `docs/sync/` |
| 当前 active figures | `figures/aqueous_antioxidant_atlas/` |
| Figure→R→Data map | `figures/FIGURE_CODE_DATA_MAP.csv` |
| R code | `R/`；总入口为 `R/render_all_active_figures.R` |
| 文件迁移记录 | `PROJECT_FILE_MIGRATION_MAP.csv` |
| 历史与被替代文件 | `archive/` |

当前 active stages 为 Stage 23、24、24B、25A 和 25A.1。当前 canonical scientific assets 已按功能归入 candidate universe、class-specific antioxidant、literature screening、metal/micronutrients、methods/QC、supervisor 和 sync。Stage 0–22 的仍有效方法资产已移入对应 current module；纯历史或被替代版本进入 archive，未删除。
