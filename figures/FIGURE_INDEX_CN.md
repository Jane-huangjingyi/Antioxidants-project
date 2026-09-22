# Active Figure Index（CN）

当前 active canonical figures 共 **29** 张，均由 R 从结构化 source data 生成。完整字段映射见 `figures/FIGURE_CODE_DATA_MAP.csv`。

## `Aqueous_All_Classes_Ranking_Overview.png`

- Path：`figures/aqueous_antioxidant_atlas/00_overview/Aqueous_All_Classes_Ranking_Overview.png`
- Scientific question：What is the current class ranking, coverage, provenance, and metal-redox framework?
- Stage：Stage 23–25A.1
- Canonical status：ACTIVE_CANONICAL
- Source data：`data/supervisor/Supervisor_Aqueous_Class_Ranking_Overview.csv; data/candidate_universe/Aqueous_Antioxidant_Candidate_Master.csv; data/class_specific_antioxidant/Aqueous_Antioxidant_Paper_Summary.csv`
- R script：`R/00_overview/plot_aqueous_overview.R`
- Caveat：within-panel percentiles do not form a global antioxidant scale
- Use：yes

## `Aqueous_Class_Coverage_Overview.png`

- Path：`figures/aqueous_antioxidant_atlas/00_overview/Aqueous_Class_Coverage_Overview.png`
- Scientific question：What is the current class ranking, coverage, provenance, and metal-redox framework?
- Stage：Stage 23–25A.1
- Canonical status：ACTIVE_CANONICAL
- Source data：`data/supervisor/Supervisor_Aqueous_Class_Ranking_Overview.csv; data/candidate_universe/Aqueous_Antioxidant_Candidate_Master.csv; data/class_specific_antioxidant/Aqueous_Antioxidant_Paper_Summary.csv`
- R script：`R/00_overview/plot_aqueous_overview.R`
- Caveat：within-panel percentiles do not form a global antioxidant scale
- Use：yes

## `Aqueous_Metal_Redox_Framework.png`

- Path：`figures/aqueous_antioxidant_atlas/00_overview/Aqueous_Metal_Redox_Framework.png`
- Scientific question：What is the current class ranking, coverage, provenance, and metal-redox framework?
- Stage：Stage 23–25A.1
- Canonical status：ACTIVE_CANONICAL
- Source data：`data/supervisor/Supervisor_Aqueous_Class_Ranking_Overview.csv; data/candidate_universe/Aqueous_Antioxidant_Candidate_Master.csv; data/class_specific_antioxidant/Aqueous_Antioxidant_Paper_Summary.csv`
- R script：`R/00_overview/plot_aqueous_overview.R`
- Caveat：within-panel percentiles do not form a global antioxidant scale
- Use：QC/internal

## `Aqueous_Primary_Literature_Coverage.png`

- Path：`figures/aqueous_antioxidant_atlas/00_overview/Aqueous_Primary_Literature_Coverage.png`
- Scientific question：What is the current class ranking, coverage, provenance, and metal-redox framework?
- Stage：Stage 23–25A.1
- Canonical status：ACTIVE_CANONICAL
- Source data：`data/supervisor/Supervisor_Aqueous_Class_Ranking_Overview.csv; data/candidate_universe/Aqueous_Antioxidant_Candidate_Master.csv; data/class_specific_antioxidant/Aqueous_Antioxidant_Paper_Summary.csv`
- R script：`R/00_overview/plot_aqueous_overview.R`
- Caveat：within-panel percentiles do not form a global antioxidant scale
- Use：QC/internal

## `Betalains_Profile_Comparison.png`

- Path：`figures/aqueous_antioxidant_atlas/01_class_specific_antioxidant_ranking/betalains/Betalains_Profile_Comparison.png`
- Scientific question：What assay-specific betalain evidence exists without forcing a common raw scale?
- Stage：Stage 23–25A.1
- Canonical status：ACTIVE_CANONICAL
- Source data：`data/class_specific_antioxidant/Betalains_Nitrogen_Profile_Evidence.csv`
- R script：`R/01_class_specific_antioxidant_ranking/betalains/plot_profile.R`
- Caveat：optical/pH interference and incompatible constructs
- Use：QC/internal

## `Flavonoids_Evidence_Depth.png`

- Path：`figures/aqueous_antioxidant_atlas/01_class_specific_antioxidant_ranking/flavonoids/Flavonoids_Evidence_Depth.png`
- Scientific question：What is the current within-class antioxidant ranking and evidence robustness?
- Stage：Stage 23–25A.1
- Canonical status：ACTIVE_CANONICAL
- Source data：`data/class_specific_antioxidant/Polyphenols_Flavonoids_Top20_v1.0.csv; data/class_specific_antioxidant/Aqueous_Antioxidant_Primary_Literature_Evidence.csv`
- R script：`R/01_class_specific_antioxidant_ranking/flavonoids/plot_class_outputs.R`
- Caveat：no cross-construct raw-value comparison; single-study estimates remain fragile
- Use：QC/internal

## `Flavonoids_Primary_Literature_Coverage.png`

- Path：`figures/aqueous_antioxidant_atlas/01_class_specific_antioxidant_ranking/flavonoids/Flavonoids_Primary_Literature_Coverage.png`
- Scientific question：What is the current within-class antioxidant ranking and evidence robustness?
- Stage：Stage 23–25A.1
- Canonical status：ACTIVE_CANONICAL
- Source data：`data/class_specific_antioxidant/Polyphenols_Flavonoids_Top20_v1.0.csv; data/class_specific_antioxidant/Aqueous_Antioxidant_Primary_Literature_Evidence.csv`
- R script：`R/01_class_specific_antioxidant_ranking/flavonoids/plot_class_outputs.R`
- Caveat：no cross-construct raw-value comparison; single-study estimates remain fragile
- Use：QC/internal

## `Flavonoids_TopN.png`

- Path：`figures/aqueous_antioxidant_atlas/01_class_specific_antioxidant_ranking/flavonoids/Flavonoids_TopN.png`
- Scientific question：What is the current within-class antioxidant ranking and evidence robustness?
- Stage：Stage 23–25A.1
- Canonical status：ACTIVE_CANONICAL
- Source data：`data/class_specific_antioxidant/Polyphenols_Flavonoids_Top20_v1.0.csv; data/class_specific_antioxidant/Aqueous_Antioxidant_Primary_Literature_Evidence.csv`
- R script：`R/01_class_specific_antioxidant_ranking/flavonoids/plot_class_outputs.R`
- Caveat：no cross-construct raw-value comparison; single-study estimates remain fragile
- Use：yes

## `Organosulfur_Redox_Mechanism_Profile.png`

- Path：`figures/aqueous_antioxidant_atlas/01_class_specific_antioxidant_ranking/organosulfur/Organosulfur_Redox_Mechanism_Profile.png`
- Scientific question：Which distinct redox mechanisms are supported for organosulfur compounds?
- Stage：Stage 23–25A.1
- Canonical status：ACTIVE_CANONICAL
- Source data：`data/class_specific_antioxidant/Organosulfur_Redox_Profile.csv`
- R script：`R/01_class_specific_antioxidant_ranking/organosulfur/plot_profile.R`
- Caveat：KEAP1, thiol and radical kinetics are not interchangeable
- Use：QC/internal

## `Other_Aqueous_Evidence_Depth.png`

- Path：`figures/aqueous_antioxidant_atlas/01_class_specific_antioxidant_ranking/other_aqueous_phytochemicals/Other_Aqueous_Evidence_Depth.png`
- Scientific question：What is the current within-class antioxidant ranking and evidence robustness?
- Stage：Stage 23–25A.1
- Canonical status：ACTIVE_CANONICAL
- Source data：`data/class_specific_antioxidant/Other_Aqueous_Phytochemicals_TopN_v1.0.csv; data/class_specific_antioxidant/Aqueous_Antioxidant_Primary_Literature_Evidence.csv`
- R script：`R/01_class_specific_antioxidant_ranking/other_aqueous_phytochemicals/plot_class_outputs.R`
- Caveat：no cross-construct raw-value comparison; single-study estimates remain fragile
- Use：QC/internal

## `Other_Aqueous_Primary_Literature_Coverage.png`

- Path：`figures/aqueous_antioxidant_atlas/01_class_specific_antioxidant_ranking/other_aqueous_phytochemicals/Other_Aqueous_Primary_Literature_Coverage.png`
- Scientific question：What is the current within-class antioxidant ranking and evidence robustness?
- Stage：Stage 23–25A.1
- Canonical status：ACTIVE_CANONICAL
- Source data：`data/class_specific_antioxidant/Other_Aqueous_Phytochemicals_TopN_v1.0.csv; data/class_specific_antioxidant/Aqueous_Antioxidant_Primary_Literature_Evidence.csv`
- R script：`R/01_class_specific_antioxidant_ranking/other_aqueous_phytochemicals/plot_class_outputs.R`
- Caveat：no cross-construct raw-value comparison; single-study estimates remain fragile
- Use：QC/internal

## `Other_Aqueous_TopN.png`

- Path：`figures/aqueous_antioxidant_atlas/01_class_specific_antioxidant_ranking/other_aqueous_phytochemicals/Other_Aqueous_TopN.png`
- Scientific question：What is the current within-class antioxidant ranking and evidence robustness?
- Stage：Stage 23–25A.1
- Canonical status：ACTIVE_CANONICAL
- Source data：`data/class_specific_antioxidant/Other_Aqueous_Phytochemicals_TopN_v1.0.csv; data/class_specific_antioxidant/Aqueous_Antioxidant_Primary_Literature_Evidence.csv`
- R script：`R/01_class_specific_antioxidant_ranking/other_aqueous_phytochemicals/plot_class_outputs.R`
- Caveat：no cross-construct raw-value comparison; single-study estimates remain fragile
- Use：yes

## `PhenolicAcids_Evidence_Depth.png`

- Path：`figures/aqueous_antioxidant_atlas/01_class_specific_antioxidant_ranking/phenolic_acids/PhenolicAcids_Evidence_Depth.png`
- Scientific question：What is the current within-class antioxidant ranking and evidence robustness?
- Stage：Stage 23–25A.1
- Canonical status：ACTIVE_CANONICAL
- Source data：`data/class_specific_antioxidant/Polyphenols_PhenolicAcids_TopN_v1.0.csv; data/class_specific_antioxidant/Aqueous_Antioxidant_Primary_Literature_Evidence.csv`
- R script：`R/01_class_specific_antioxidant_ranking/phenolic_acids/plot_class_outputs.R`
- Caveat：no cross-construct raw-value comparison; single-study estimates remain fragile
- Use：QC/internal

## `PhenolicAcids_Primary_Literature_Coverage.png`

- Path：`figures/aqueous_antioxidant_atlas/01_class_specific_antioxidant_ranking/phenolic_acids/PhenolicAcids_Primary_Literature_Coverage.png`
- Scientific question：What is the current within-class antioxidant ranking and evidence robustness?
- Stage：Stage 23–25A.1
- Canonical status：ACTIVE_CANONICAL
- Source data：`data/class_specific_antioxidant/Polyphenols_PhenolicAcids_TopN_v1.0.csv; data/class_specific_antioxidant/Aqueous_Antioxidant_Primary_Literature_Evidence.csv`
- R script：`R/01_class_specific_antioxidant_ranking/phenolic_acids/plot_class_outputs.R`
- Caveat：no cross-construct raw-value comparison; single-study estimates remain fragile
- Use：QC/internal

## `PhenolicAcids_TopN.png`

- Path：`figures/aqueous_antioxidant_atlas/01_class_specific_antioxidant_ranking/phenolic_acids/PhenolicAcids_TopN.png`
- Scientific question：What is the current within-class antioxidant ranking and evidence robustness?
- Stage：Stage 23–25A.1
- Canonical status：ACTIVE_CANONICAL
- Source data：`data/class_specific_antioxidant/Polyphenols_PhenolicAcids_TopN_v1.0.csv; data/class_specific_antioxidant/Aqueous_Antioxidant_Primary_Literature_Evidence.csv`
- R script：`R/01_class_specific_antioxidant_ranking/phenolic_acids/plot_class_outputs.R`
- Caveat：no cross-construct raw-value comparison; single-study estimates remain fragile
- Use：yes

## `Stilbenes_Lignans_Evidence_Depth.png`

- Path：`figures/aqueous_antioxidant_atlas/01_class_specific_antioxidant_ranking/stilbenes_lignans/Stilbenes_Lignans_Evidence_Depth.png`
- Scientific question：What is the current within-class antioxidant ranking and evidence robustness?
- Stage：Stage 23–25A.1
- Canonical status：ACTIVE_CANONICAL
- Source data：`data/class_specific_antioxidant/Stilbenes_Lignans_TopN_v1.0.csv; data/class_specific_antioxidant/Aqueous_Antioxidant_Primary_Literature_Evidence.csv`
- R script：`R/01_class_specific_antioxidant_ranking/stilbenes_lignans/plot_class_outputs.R`
- Caveat：no cross-construct raw-value comparison; single-study estimates remain fragile
- Use：QC/internal

## `Stilbenes_Lignans_Primary_Literature_Coverage.png`

- Path：`figures/aqueous_antioxidant_atlas/01_class_specific_antioxidant_ranking/stilbenes_lignans/Stilbenes_Lignans_Primary_Literature_Coverage.png`
- Scientific question：What is the current within-class antioxidant ranking and evidence robustness?
- Stage：Stage 23–25A.1
- Canonical status：ACTIVE_CANONICAL
- Source data：`data/class_specific_antioxidant/Stilbenes_Lignans_TopN_v1.0.csv; data/class_specific_antioxidant/Aqueous_Antioxidant_Primary_Literature_Evidence.csv`
- R script：`R/01_class_specific_antioxidant_ranking/stilbenes_lignans/plot_class_outputs.R`
- Caveat：no cross-construct raw-value comparison; single-study estimates remain fragile
- Use：QC/internal

## `Stilbenes_Lignans_TopN.png`

- Path：`figures/aqueous_antioxidant_atlas/01_class_specific_antioxidant_ranking/stilbenes_lignans/Stilbenes_Lignans_TopN.png`
- Scientific question：What is the current within-class antioxidant ranking and evidence robustness?
- Stage：Stage 23–25A.1
- Canonical status：ACTIVE_CANONICAL
- Source data：`data/class_specific_antioxidant/Stilbenes_Lignans_TopN_v1.0.csv; data/class_specific_antioxidant/Aqueous_Antioxidant_Primary_Literature_Evidence.csv`
- R script：`R/01_class_specific_antioxidant_ranking/stilbenes_lignans/plot_class_outputs.R`
- Caveat：no cross-construct raw-value comparison; single-study estimates remain fragile
- Use：yes

## `VitaminC_Primary_Literature_Coverage.png`

- Path：`figures/aqueous_antioxidant_atlas/01_class_specific_antioxidant_ranking/water_soluble_vitamins/VitaminC_Primary_Literature_Coverage.png`
- Scientific question：What rank-eligible primary evidence supports the aqueous vitamin subpanel?
- Stage：Stage 23–25A.1
- Canonical status：ACTIVE_CANONICAL
- Source data：`data/class_specific_antioxidant/Aqueous_Antioxidant_Primary_Literature_Evidence.csv`
- R script：`R/01_class_specific_antioxidant_ranking/water_soluble_vitamins/plot_literature_coverage.R`
- Caveat：singleton panel percentile is not informative
- Use：QC/internal

## `Metal_Chelation_or_Fenton_Evidence_Profile.png`

- Path：`figures/aqueous_antioxidant_atlas/02_metal_and_micronutrients/metal_redox/Metal_Chelation_or_Fenton_Evidence_Profile.png`
- Scientific question：How do binding, reduction and net oxidative endpoints differ by metal context?
- Stage：Stage 23–25A.1
- Canonical status：ACTIVE_CANONICAL
- Source data：`data/metal_and_micronutrients/Aqueous_Metal_Redox_Evidence.csv`
- R script：`R/02_metal_and_micronutrients/metal_redox/plot_profile.R`
- Caveat：not an ORAC competitor ranking
- Use：QC/internal

## `Micronutrient_Antioxidant_Enzyme_Map.png`

- Path：`figures/aqueous_antioxidant_atlas/02_metal_and_micronutrients/micronutrients/Micronutrient_Antioxidant_Enzyme_Map.png`
- Scientific question：What cofactor, enzyme and prooxidant contexts apply to micronutrients?
- Stage：Stage 23–25A.1
- Canonical status：ACTIVE_CANONICAL
- Source data：`data/metal_and_micronutrients/Antioxidant_Micronutrient_Redox_Profile_v2.csv`
- R script：`R/02_metal_and_micronutrients/micronutrients/plot_profiles.R`
- Caveat：minerals do not compete in ORAC ranking
- Use：QC/internal

## `Micronutrient_Prooxidant_Context.png`

- Path：`figures/aqueous_antioxidant_atlas/02_metal_and_micronutrients/micronutrients/Micronutrient_Prooxidant_Context.png`
- Scientific question：What cofactor, enzyme and prooxidant contexts apply to micronutrients?
- Stage：Stage 23–25A.1
- Canonical status：ACTIVE_CANONICAL
- Source data：`data/metal_and_micronutrients/Antioxidant_Micronutrient_Redox_Profile_v2.csv`
- R script：`R/02_metal_and_micronutrients/micronutrients/plot_profiles.R`
- Caveat：minerals do not compete in ORAC ranking
- Use：QC/internal

## `Micronutrient_Redox_Profile.png`

- Path：`figures/aqueous_antioxidant_atlas/02_metal_and_micronutrients/micronutrients/Micronutrient_Redox_Profile.png`
- Scientific question：What cofactor, enzyme and prooxidant contexts apply to micronutrients?
- Stage：Stage 23–25A.1
- Canonical status：ACTIVE_CANONICAL
- Source data：`data/metal_and_micronutrients/Antioxidant_Micronutrient_Redox_Profile_v2.csv`
- R script：`R/02_metal_and_micronutrients/micronutrients/plot_profiles.R`
- Caveat：minerals do not compete in ORAC ranking
- Use：QC/internal

## `Literature_Screening_Research_Evidence_Density_Top50.png`

- Path：`figures/aqueous_antioxidant_atlas/03_unified_literature_screening/01_primary_ranking/Literature_Screening_Research_Evidence_Density_Top50.png`
- Scientific question：Which frozen candidates have the densest antioxidant/redox original-publication record?
- Stage：Stage 23–25A.1
- Canonical status：ACTIVE_CANONICAL
- Source data：`data/literature_screening/master/Literature_Screening_Candidate_Master.csv`
- R script：`R/03_unified_literature_screening/01_primary_ranking/plot_research_evidence_density.R`
- Caveat：not potency, quality, efficacy, or true same-study adjudication
- Use：yes

## `Literature_Screening_Publication_Count_vs_Citations.png`

- Path：`figures/aqueous_antioxidant_atlas/03_unified_literature_screening/02_metric_validation/Literature_Screening_Publication_Count_vs_Citations.png`
- Scientific question：Does research-density ranking align with citation attention?
- Stage：Stage 23–25A.1
- Canonical status：ACTIVE_CANONICAL
- Source data：`data/literature_screening/master/Literature_Screening_Candidate_Master.csv`
- R script：`R/03_unified_literature_screening/02_metric_validation/plot_publication_vs_citation.R`
- Caveat：citations reflect attention and age, not evidence quality
- Use：yes

## `Literature_Screening_Recent_vs_Historical_Evidence.png`

- Path：`figures/aqueous_antioxidant_atlas/03_unified_literature_screening/02_metric_validation/Literature_Screening_Recent_vs_Historical_Evidence.png`
- Scientific question：Which candidates combine accumulated and recent research activity?
- Stage：Stage 23–25A.1
- Canonical status：ACTIVE_CANONICAL
- Source data：`data/literature_screening/master/Literature_Screening_Candidate_Master.csv`
- R script：`R/03_unified_literature_screening/02_metric_validation/plot_recent_vs_historical.R`
- Caveat：publication activity is not potency or quality
- Use：yes

## `Literature_Screening_Shortlist_Stability_Top20_to_Top60.png`

- Path：`figures/aqueous_antioxidant_atlas/03_unified_literature_screening/03_shortlist_stability/Literature_Screening_Shortlist_Stability_Top20_to_Top60.png`
- Scientific question：How stable is primary membership under supporting metrics?
- Stage：Stage 23–25A.1
- Canonical status：ACTIVE_CANONICAL
- Source data：`data/literature_screening/shortlist/Stage25A_Shortlist_Cutoff_Sensitivity.csv`
- R script：`R/03_unified_literature_screening/03_shortlist_stability/plot_shortlist_stability.R`
- Caveat：metrics share underlying publication records
- Use：yes

## `Literature_Screening_Class_Representation_Top20_to_Top60.png`

- Path：`figures/aqueous_antioxidant_atlas/03_unified_literature_screening/04_class_representation/Literature_Screening_Class_Representation_Top20_to_Top60.png`
- Scientific question：Which classes remain under publication-density cutoffs without quotas?
- Stage：Stage 23–25A.1
- Canonical status：ACTIVE_CANONICAL
- Source data：`data/literature_screening/qc/Literature_Screening_Class_Representation_Sensitivity.csv`
- R script：`R/03_unified_literature_screening/04_class_representation/plot_class_representation.R`
- Caveat：publication density differs systematically by class
- Use：QC/internal

## `Literature_Screening_Evidence_Domain_Breadth_Top30.png`

- Path：`figures/aqueous_antioxidant_atlas/03_unified_literature_screening/05_evidence_breadth/Literature_Screening_Evidence_Domain_Breadth_Top30.png`
- Scientific question：How broad are the evidence domains of high-density candidates?
- Stage：Stage 23–25A.1
- Canonical status：ACTIVE_CANONICAL
- Source data：`data/literature_screening/master/Literature_Screening_Candidate_Master.csv; data/literature_screening/provenance/Literature_Screening_Publication_Provenance.csv`
- R script：`R/03_unified_literature_screening/05_evidence_breadth/plot_evidence_domain_breadth.R`
- Caveat：metadata labels are not evidence-quality grades
- Use：QC/internal

## Stage25B.5 canonical H-ORAC figures

- `aqueous_antioxidant_atlas/HORAC_Primary_Top20_Frozen.png` / `.svg` — frozen A+B1 Top20, median H-ORAC with evidence depth and heterogeneity display.
- `aqueous_antioxidant_atlas/HORAC_Top20_B2_Sensitivity.png` / `.svg` — B2 sensitivity membership changes only (3 enter/3 leave), not a second formal ranking.

Deduplication audit found no pre-existing active Top20/ranking/sensitivity/cutoff figure carrying the same scientific message; therefore no archive move was required. Both canonical figures are reproducible from `R/stage25b5/` and the frozen CSV inputs.
