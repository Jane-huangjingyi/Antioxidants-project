# Results: source-bounded candidate discovery and screening preparation

As of 2026-11-05, the reproducible discovery register contained 204 records: 191 names reconstructed from the original class-based enumeration, 12 preserved exclusion records rescreened under the current food-source rule, and one targeted ergothioneine addition. The register is a versioned discovery collection, not an exhaustive census of food chemicals.

The workflow produced 193 candidate identity/evidence profiles; 191 had reference CID, InChIKey and formula, while 184 also met the molecular-form scope check. The existing five-dimensional framework covered 157 preserved candidates. Other profiles were labelled outside that snapshot instead of assigned negative evidence.

25 candidates met the review-queue gates using preserved candidate-specific source closure. The two-confirmed-study sensitivity retained 9. A 20-slot administrative preview was produced, with 12 candidates in the cutoff evidence stratum; all tied candidates remain visible for researcher adjudication. Candidate IDs resolve display order only.

The preview overlapped the frozen H-ORAC Top20 in 12 candidates; 8 preview candidates were outside the frozen set and 8 frozen members were outside the preview. This is a comparison of different selection purposes, not a revised activity ranking.

0 profiles met all laboratory-ready gates. No new absorbance assay results, effective concentrations, causal targets or human benefits were generated.

Tables 1-3 report the discovery flow, reference formulas/source-linked review panel, and comparison with the frozen reference. Table S1 records identity/food-source gaps. Figures 1-3 visualize screening preparation only.

## Suggested manuscript use

These are descriptive workflow results suitable for a methods-development or candidate-prioritization manuscript. Laboratory efficacy, dose-response and mechanism Results remain unwritten until real data and adjudications exist.


## Exploratory structural validation

The 36 single-paper log-ORAC labels and database candidate graphs were evaluated by nested leave-one-scaffold-group-out validation (five groups: 23, 8, 3, 1 and 1). Four-descriptor ridge regression yielded pooled MAE 0.692 and RMSE 0.950, compared with 0.689 and 0.953 for the matched training-mean baseline. The model did not show a consistent improvement across these two metrics. These are exploratory internal errors, not independent-study validation or established performance for verified experimental structures. No global ranking was generated. Per-fold errors are provided in the structural validation tables.

Adding phenolic-OH and aryl-methoxy counts in a post-hoc sensitivity analysis gave MAE 0.673 and RMSE 0.927. This small improvement is exploratory, since feature selection followed inspection of initial validation results. It does not establish an independently validated ranking model.

A further post-hoc Morgan-fingerprint analysis yielded MAE 0.652 and RMSE 0.914, with 35 distinct vectors across 36 candidate structures. Pooled errors improved relative to the mean baseline, but the three-member catechin-related scaffold group worsened (MAE 0.922 versus 0.350). This heterogeneous result does not support a final global ranking. Chirality was excluded and source-material stereochemistry remained unresolved.

## Retrospective protocol-shift pressure test

The separately authorized two-observation diagnostic used explicit molar means from DOI 10.1271/bbb.110717. Development-only scaffold CV selected alpha 10; external values were not used for tuning. Both known compounds received log prediction 1.5796, below source log arithmetic means 2.1972 (Catechin) and 2.3026 (Epicatechin). Descriptive model MAE/RMSE were 0.670/0.672, compared with 0.969/0.970 for the development-mean baseline. These observations compare different summary estimands and protocols; they establish neither formal external validation nor new-structure validity. No ranking was updated. Individual residuals are recorded in Retrospective_Pressure_Test.csv.

## External evidence readiness

The retrospective queue contained 28 observations across 10 papers. Original numeric text was rechecked for 6 observations; molar-estimator provenance was traced for 4, while 0 common-target external labels were released. No duplicate observation keys were found, but cross-paper data-generation independence remained unresolved. Adding traced external observations to the 36 development rows produced one connected topology (40 edges, additive indicator-design rank 39, topological redundancy 1). This sparse connection does not resolve protocol/material differences or justify fitting study-adjusted ranks. External_Paper_Readiness.csv and External_Connectivity_Readiness.csv report the source-specific gates and graph scopes.
