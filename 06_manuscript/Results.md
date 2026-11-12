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

The retrospective queue contained 29 observations across 10 papers. Original numeric text was rechecked for 8 observations; molar-estimator provenance was traced for 4, while 0 common-target external labels were released. No duplicate observation keys were found, but cross-paper data-generation independence remained unresolved. Adding traced external observations to the 36 development rows produced one connected topology (40 edges, additive indicator-design rank 39, topological redundancy 1). This sparse connection does not resolve protocol/material differences or justify fitting study-adjusted ranks. Two further source values have conditional reference-parent mass-to-mole conversions, retained outside fitting and shown in a separate topology sensitivity. External_Paper_Readiness.csv and External_Connectivity_Readiness.csv report the source-specific gates and graph scopes.

## Analysis-set disposition

The reproducible disposition table retained 152 provenance rows: 99 capacity references, 36 original log labels and 17 additional source row. Fourteen capacity references matched development Table 3 records and were retained only as alternate representations, not additional measurements. Authorized sensitivity roles comprised 36 exploratory development labels and two separate retrospective challenge observations. The table contained 100 waiting rows, including two existing source-identity HOLDs, and 0 common-target primary labels. These are provenance/disposition counts, not independent studies or candidate ranks. Primary scope is fixed to pH 7.4 and 37 degrees C, with vehicle/AUC/window stratification. Source-material, stratum and estimand alignment remain prerequisites to primary modelling; formal human review states were unchanged.

## Protocol lineage

Cited-SOP checks mapped 9 existing phenolic observations without adding numeric measurements. Shared method conditions were distinguished from confirmed execution, and the quality-control acceptance range was not reassigned as compound measurement error. Executed A/B variant, final vehicle and estimator remain unresolved; no primary labels were released. Protocol_Lineage_Check.csv records the row-level implications.

## Scope-consistent validation readiness

Of nine source-verified model-candidate rows, 6 from 2 papers matched the fixed core conditions; 3 stayed outside this diagnostic. Both leave-paper-out identity-coverage checks lacked shared compounds. The 31-row extended review separated core-condition evidence from inherited and unconfirmed conditions and identified 5 source-specific pending strata. None supported a cross-paper fold within verified compatible strata. These are design diagnostics, not validation errors or newly fitted models.

## Completed exploratory modelling

Joint family/penalty selection nested within five scaffold folds gave pooled MAE 0.695 and RMSE 0.945, versus 0.689 and 0.953 for the matched mean baseline. Out-of-fold R-squared was -0.240, with Spearman correlation 0.238. Mean group MAE was 0.594 versus 0.701. The differing pooled and group-level results do not establish a consistent predictive advantage. Development-only CV selected DESC6 ridge with alpha 10 for the exported full-data artifact.

The fitted order covered only 16 of 193 current profiles; 177 received no score. Group-removal refits showed unstable positions. Figures Model_Heldout_Predictions, Model_Scaffold_Errors and Model_Order_Stability show held-out predictions, group errors and refit influence. This completes the exploratory pipeline, while a formal primary model and global Top20 remain unestablished. All positions are diagnostic source-specific model outputs, not validated candidate-selection decisions.

## Cross-structure evidence expansion

Two additional original papers contributed 16 source observations: 15 numeric entries, including one reported zero, and one reported no-activity result without a numeric value. Three observations mapped to existing candidate profiles; source-reference compounds outside the current index were retained without adding candidate members. The new records did not satisfy all primary scope/material/estimator gates, so no primary labels were released and the completed model was not retrained using them. A twelve-profile method-bridge preparation panel was generated separately from potency selection. No experiments were executed.

## Confirmed experimental route

The researcher confirmed absorbance-only measurement availability. Future formal modelling will use a separately validated absorbance-capacity endpoint; ORAC-FL remains prior/source-model evidence. No paired numerical transfer, actual assay response or new model performance is claimed.

## Absorbance preparation status

Offline source-status and synthetic formula checks passed; 36 pilot manifest fields remain unfilled. Two original 2015 method equations remain source-pending. An additional 2006 original-abstract inhibition formula was identified as a distinct endpoint; it did not release a capacity label. Synthetic matched-vehicle checks retain nonpositive responses and reject incompatible protocol, vehicle, preparation or sampling-grid assignments. The staged design is prepared, while assay execution readiness is NOT_READY. No experimental responses or formal absorbance model were generated.

## Identified reader feasibility

The researcher identified the Opentrons Flex Absorbance Plate Reader Module GEN1. The source-linked audit found 1 exact channel match among 3 checked method readouts. This is optical compatibility, not capacity validation. Local accessories, thermal history and timing qualification remain unresolved. Execution readiness remains NOT_READY; no experimental response or formal absorbance model was generated.

## Simulation-only method diagnostic

In the prespecified dimensionless toy model, equal synthetic capacity with different capture rates produced a 3.067-fold difference in normalized-AUC slope ratios for one fixed acquisition window. Halving the integration step changed ratios by at most 1.1e-06. These numerical counterexamples concern interpretation under assumed kinetics, not measured crocin behavior, molar TE, candidate ranks or formal model validation. The fixed-protocol molar-protection endpoint remains a development candidate.

## Supplemental retrieval coverage

Public supplemental retrieval covered all 193 current profiles through 579 canonical-route queries and 193 expanded capacity queries. The supplemental register contained 49906 provisional identifier groups. Reconciliation with historical metadata yielded 87386 master groups and 106123 candidate-article links. These are bibliographic retrieval counts awaiting conflict review, screening and quantitative extraction. Existing model labels were not expanded from metadata alone.
