# 项目逻辑地图

2026-10-16 路径整理后，H-ORAC 主表位于 `data/h_orac_stage25b/stage25b/`；阶段产物按 `stage25b1/` 至 `stage25b4/` 分类。历史版本通过 `current_review/HISTORICAL_VERSION_INDEX.csv` 查找，旧路径通过 `current_review/File_Reorganization_Migration_2026-10-16.csv` 查找。现位置与科学状态分开登记，移动不改变正式版本。

2026-10-15 当前入口：[`current_review/PROJECT_NAVIGATION.md`](current_review/PROJECT_NAVIGATION.md) 提供全部当前权威文件的直链、状态和冻结标记；[`current_review/LATEST_PROJECT_STATUS_CN.md`](current_review/LATEST_PROJECT_STATUS_CN.md) 概述 Stage25B.6D 与综合框架 Phase 1。Stage25B.5 Frozen Top20 v1.0 仍是正式版本；Stage25B.6D 仅为待审证据诊断，未建立 v1.1。Track B 157 候选、三个应用场景的未评分 v0.1 框架见 `docs/framework/` 和 `data/framework/`；双轨映射见 `docs/dual_track_phase1/` 和 `data/dual_track_phase1/`。以下旧时间线保留历史语境，不应覆盖本段最新状态。

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

当前 active mainline来自 Stage 23、24、24B、25A、25A.1、架构审计25A.2及Stage25B–25B.4工作包。Stage25B.4已canonicalize H-ORAC rubric v2并迁移74条已裁决experiments；post-migration A/B1/B2/X=7/61/4/2、rankable N=28，primary Top20 membership不变，但freeze仍需人工决定。剩余1,641条pending records未处理。Stage 0–22 的仍有效方法资产已进入对应 current module；历史或被替代版本进入archive。

## Stage25B.5 frozen package

- Frozen tables: `data/h_orac_stage25b/frozen/`
- Final method: `docs/methods/h_orac_framework/Stage25B_HORAC_Selection_and_Ranking_Method_Final_CN.md`
- Freeze/closure: `docs/qc/Stage25B5_Primary_Top20_Freeze_Decision_CN.md`, `docs/qc/Stage25B5_Final_Freeze_and_Closure_Report_CN.md`
- Canonical figures: `figures/aqueous_antioxidant_atlas/HORAC_Primary_Top20_Frozen.*`, `HORAC_Top20_B2_Sensitivity.*`
- Downstream skeleton: `data/top20_characterization/Top20_Downstream_Handoff_Master.csv`
- Status: STAGE25B CLOSED — PRIMARY H-ORAC TOP20 FROZEN WITH EXPLICIT B2 SENSITIVITY QUALIFICATION.

## Stage25B.6A supervisor feedback audit

Diagnostic CSVs: `data/h_orac_stage25b/stage25b6a/`. Scientific assessment and draft framework: `docs/qc/stage25b6a/`. ChatGPT handoff: `docs/sync/CHATGPT_SYNC_STAGE25B6A.md`. Stage25B Frozen Top20 v1.0 remains the current formal version.

## Stage25B.6C source independence and targeted adjudication

16 个既有 DOI 的原文/来源核查、28 种候选的逐对独立性及资格表、定点新来源、误差、研究历史、情景与变更请求见 `data/h_orac_stage25b/stage25b6c/`。导师汇报与 QC 见 `docs/qc/stage25b6c/`；交接见 `docs/sync/CHATGPT_SYNC_STAGE25B6C.md`。7 个既有来源定位原始纯品结果，9 种候选满足拟议双独立研究门槛；正式 Top20 v1.0、Rubric v2.0 与 canonical 表不变，v1.1 未建立。
