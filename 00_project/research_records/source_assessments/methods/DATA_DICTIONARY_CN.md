# Core Data Dictionary

本字典覆盖当前核心 masters；完整列仍以 CSV header 为准。`candidate_id` 是项目内稳定候选键，`PubChem_CID` 与 `InChIKey` 是结构身份锚点，`analysis_panel/class/subclass` 描述 taxonomy，`candidate_eligible` 与 `Stage25B_status` 属于不同决策层。

| Table | Key fields | Meaning / unit / allowed values |
|---|---|---|
| `candidate_universe/Antioxidant_Class_Candidate_Master.csv` | candidate_id, canonical_name, PubChem_CID, InChIKey, analysis_panel, candidate_eligible | 全项目候选身份、食物来源和类别 gate；candidate_eligible 为 yes/unresolved/excluded 类型状态 |
| `candidate_universe/Aqueous_Antioxidant_Candidate_Master.csv` | compound, analysis_panel, primary_construct, aqueous_assay_eligible | 冻结 157 aqueous candidates；不得在 Stage25A.1 增删 |
| `literature_screening/master/Literature_Screening_Candidate_Master.csv` | metadata_deduplicated_original_publication_N, ranks, citations, Stage25B_status | 一行一候选；publication count 为研究证据密度代理，不是 independent-study count；citations 来自 OpenAlex |
| 同上 legacy field | antioxidant_independent_publication_N | backward compatibility only；数值映射到 metadata-deduplicated count，禁止在正式展示中称 independent study |
| `literature_screening/provenance/Literature_Screening_Publication_Provenance.csv` | candidate_id, DOI/PMID, paper_title, include_primary_metric, citation_count | 一行 candidate×publication；citation unit 为 OpenAlex cited_by_count，retrieval date 单独记录 |
| `literature_screening/shortlist/Literature_Screening_Provisional_Top50.csv` | primary_rank, metadata publication count, Stage25B_status | research-density Top50；不因 H-ORAC eligibility 删除或补位 |
| `literature_screening/shortlist/Stage25B_HORAC_Retrieval_Eligible_Candidates.csv` | retrieval_decision, Stage25B_status | Top50 中 Ready 或方法学 Conditional 且无 unresolved scope gate 的 43 个 retrieval candidates；不是最终 Top20 |
| `class_specific_antioxidant/Aqueous_Antioxidant_Primary_Literature_Evidence.csv` | original_value/unit, normalized_value/unit, DOI, exact location, tier | H-ORAC 与其他 class-specific primary evidence provenance；单位和 assay construct 不得无条件混合 |
| `metal_and_micronutrients/Aqueous_Metal_Redox_Evidence.csv` | metal ion/state, chelation_or_reduction, evidence_strength | 金属结合、还原、Fenton 与 net endpoint profile；不进入 ORAC ranking |

`Stage25B_status` 允许 Ready、Conditional、Not suitable for H-ORAC ranking、Insufficient identity、Insufficient evidence。`human_review_required=yes` 表示不得由自动流程静默裁决。缺失数据不得编码为零。
