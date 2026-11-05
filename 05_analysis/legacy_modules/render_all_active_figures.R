# Supplementary historical construct; not the current review-panel result.
# Thin active-figure entry point. Run from the project root.
scripts <- c(
 "05_analysis/legacy_modules/00_overview/plot_aqueous_overview.R",
 "05_analysis/legacy_modules/01_class_specific_antioxidant_ranking/flavonoids/plot_class_outputs.R",
 "05_analysis/legacy_modules/01_class_specific_antioxidant_ranking/phenolic_acids/plot_class_outputs.R",
 "05_analysis/legacy_modules/01_class_specific_antioxidant_ranking/stilbenes_lignans/plot_class_outputs.R",
 "05_analysis/legacy_modules/01_class_specific_antioxidant_ranking/water_soluble_vitamins/plot_literature_coverage.R",
 "05_analysis/legacy_modules/01_class_specific_antioxidant_ranking/betalains/plot_profile.R",
 "05_analysis/legacy_modules/01_class_specific_antioxidant_ranking/organosulfur/plot_profile.R",
 "05_analysis/legacy_modules/01_class_specific_antioxidant_ranking/other_aqueous_phytochemicals/plot_class_outputs.R",
 "05_analysis/legacy_modules/02_metal_and_micronutrients/metal_redox/plot_profile.R",
 "05_analysis/legacy_modules/02_metal_and_micronutrients/micronutrients/plot_profiles.R",
 "05_analysis/legacy_modules/03_unified_literature_screening/01_primary_ranking/plot_research_evidence_density.R",
 "05_analysis/legacy_modules/03_unified_literature_screening/02_metric_validation/plot_publication_vs_citation.R",
 "05_analysis/legacy_modules/03_unified_literature_screening/02_metric_validation/plot_recent_vs_historical.R",
 "05_analysis/legacy_modules/03_unified_literature_screening/03_shortlist_stability/plot_shortlist_stability.R",
 "05_analysis/legacy_modules/03_unified_literature_screening/04_class_representation/plot_class_representation.R",
 "05_analysis/legacy_modules/03_unified_literature_screening/05_evidence_breadth/plot_evidence_domain_breadth.R")
for(script in scripts){message("Rendering: ",script);source(script,local=new.env(parent=globalenv()))}
message("All active canonical figures regenerated: ",length(scripts)," modular scripts.")
