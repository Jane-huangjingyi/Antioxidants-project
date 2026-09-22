# 项目逻辑地图

当前科学主线为：Candidate Universe → Class-specific Antioxidant Characterization → Unified Literature Research-density Screen → Provisional Top50 → H-ORAC Eligibility QC → Stage25B Retrieval Set → Future H-ORAC Quantitative Ranking → Future Top20 → Future Target / Mechanism Prioritization。Stage25B及其后节点尚未执行。本文件回答“当前文件在哪里、哪个是 canonical”；完整机器可读登记见 `CANONICAL_ASSET_REGISTRY.csv`，历史顺序见 `docs/PROJECT_STAGE_INDEX_CN.md`，科学决策变化见根目录 MASTER HISTORY。

| 科学节点 | Canonical data | Canonical method / QC | Canonical figure / R |
|---|---|---|---|
| Candidate Universe | `data/candidate_universe/Antioxidant_Class_Candidate_Master.csv`；`data/candidate_universe/Aqueous_Antioxidant_Candidate_Master.csv` | `docs/methods/Antioxidant_Functional_Factor_Taxonomy_CN.md` | `figures/candidate_universe/`；当前 supporting figures |
| Class-specific characterization | `data/class_specific_antioxidant/Aqueous_Antioxidant_Primary_Literature_Evidence.csv`及各class TopN/profile | `docs/methods/Class_Specific_TopN_Ranking_Rules_CN.md` | `figures/aqueous_antioxidant_atlas/01_class_specific_antioxidant_ranking/`；`R/01_class_specific_antioxidant_ranking/` |
| Unified literature screen | `data/literature_screening/master/Literature_Screening_Candidate_Master.csv`；`data/literature_screening/provenance/Literature_Screening_Publication_Provenance.csv` | `docs/qc/Stage25A_Citation_Source_Audit_CN.md` | `figures/aqueous_antioxidant_atlas/03_unified_literature_screening/`；`R/03_unified_literature_screening/` |
| Top50 / H-ORAC eligibility | `data/literature_screening/shortlist/Literature_Screening_Provisional_Top50.csv`；`data/literature_screening/shortlist/Stage25B_HORAC_Retrieval_Eligible_Candidates.csv` | `data/literature_screening/qc/Top50_PreStage25B_QC.csv` | Stage25A screening figures；无新的potency rank figure |
| Stage25B / 25B.1（进行中；未冻结） | `data/h_orac_stage25b/`；checkpoint见其`checkpoints/` | `docs/qc/Stage25B_HORAC_Retrieval_and_Adjudication_Report_CN.md`；`docs/qc/Stage25B1_Top20_Cutoff_Stability_Report_CN.md`；frozen rubric | 尚未生成正式图；cutoff稳定前不绘制排名主图 |
| Metal / micronutrients | `data/metal_and_micronutrients/Aqueous_Metal_Redox_Evidence.csv`；`data/metal_and_micronutrients/Antioxidant_Micronutrient_Redox_Profile_v2.csv` | class-specific construct rules | `figures/aqueous_antioxidant_atlas/02_metal_and_micronutrients/`；`R/02_metal_and_micronutrients/` |

| 我要查阅的内容 | 当前 canonical 位置 |
|---|---|
| 157 aqueous candidate universe | `data/candidate_universe/Aqueous_Antioxidant_Candidate_Master.csv` |
| 全类别 candidate master | `data/candidate_universe/Antioxidant_Class_Candidate_Master.csv` |
| 类别内 ranking/profile | `data/class_specific_antioxidant/` |
| H-ORAC evidence master | `data/class_specific_antioxidant/Aqueous_Antioxidant_Primary_Literature_Evidence.csv` |
| Stage25B publication / experiment / ranking work products | `data/h_orac_stage25b/` |
| Stage25A 157-row master | `data/literature_screening/master/Literature_Screening_Candidate_Master.csv` |
| 论文 provenance | `data/literature_screening/provenance/Literature_Screening_Publication_Provenance.csv` |
| Provisional Top50 | `data/literature_screening/shortlist/Literature_Screening_Provisional_Top50.csv` |
| Stage25B retrieval candidates | `data/literature_screening/shortlist/Stage25B_HORAC_Retrieval_Eligible_Candidates.csv` |
| Top50 targeted QC | `data/literature_screening/qc/Top50_PreStage25B_QC.csv` |
| Stage25A.1 Human Review Resolution | `docs/qc/Stage25A1_Human_Review_Resolution_CN.md` |
| Append-only human review history | `data/class_specific_antioxidant/Human_Review_Log.csv` |
| Metal/redox 与 micronutrients | `data/metal_and_micronutrients/` |
| 当前方法与 taxonomy | `docs/methods/` |
| 早期仍有效的 H-ORAC SOP | `docs/methods/h_orac_framework/` |
| 导师汇报文件 | `docs/supervisor/` |
| ChatGPT 同步文件 | `docs/sync/` |
| 当前 active figures | `figures/aqueous_antioxidant_atlas/` |
| Figure→R→Data map | `figures/FIGURE_CODE_DATA_MAP.csv` |
| Canonical asset registry | `CANONICAL_ASSET_REGISTRY.csv` |
| Figure scientific-message audit | `figures/FIGURE_SCIENTIFIC_MESSAGE_AUDIT.csv` |
| R code | `R/`；总入口为 `R/render_all_active_figures.R` |
| 文件迁移记录 | `PROJECT_FILE_MIGRATION_MAP.csv` |
| 历史与被替代文件 | `archive/` |

当前 active mainline来自 Stage 23、24、24B、25A、25A.1、架构审计25A.2及尚未冻结的Stage25B/25B.1工作包。Stage25B.1已对1,657条队列建立优先级并完成两个rank-relevant batch；rankable N为29，但B2 sensitivity继续改变Top20且shared cutoff sources未恢复，因此状态为HUMAN REVIEW REQUIRED，不得把当前interim ranking解释为正式Top20。Stage 0–22 的仍有效方法资产已进入对应 current module；旧排名和跨类结果若仍有解释价值则标为 supporting，纯历史或被替代版本进入 archive。Stage编号不是active目录组织原则。
