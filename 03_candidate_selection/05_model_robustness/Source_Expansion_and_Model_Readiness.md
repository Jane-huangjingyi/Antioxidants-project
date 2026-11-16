# Source expansion and model readiness

The original-source update in [Step 03.6](../06_verified_source_update/README.md) is the current assessment after researcher-supplied PDFs and the recovered 60-flavonoid table. The figures below describe the preceding fixed-model comparison and its original reference inputs.

The current model estimates 34 of 193 indexed candidates (17.6%). 20 model candidates have one contributing DOI. Food occurrence, exact form, protocol qualification and original-experiment independence remain candidate-specific requirements. Retrieval volume does not establish representation of chemical classes.

Nested leave-paper-out log RMSE is 0.3902, compared with 0.3911 for the source-summary baseline. This modest difference supports retaining the baseline in future comparisons. Existing source-deletion checks preserve a direction for 68 of 561 candidate pairs across every omission. These diagnostics do not establish a stable global Top20.

## Newly recovered source checks

Six mapped rows from three new DOIs can be compared numerically with fixed prior estimates. Their source units or direct molar ratios are preserved in the extraction. Missing protocol and material fields make these descriptive cross-condition checks. The four matched phenolic acids from one new paper give six dependent pair comparisons, with 6 agreeing directions. The unit of source replication here is one paper. Ratios to prior estimates expose magnitude differences without attributing their cause to intrinsic potency or model error.

The existing estimate is exp(log location), a conditional geometric location. Expected arithmetic molar capacity requires an adequately identified outcome distribution or a validated retransformation. That target distinction remains part of model development.

## Conditions for the next model update

Resolve exact chemical forms and dietary scope, recover original numeric endpoints and error definitions, assign experiment clusters across related reports, and document final pH, temperature, solvent and AUC rule. Evaluate a strict pH 7.4/37 C protocol-stratified analysis before broader sensitivity pooling. Keep repeated concentrations within a source rather than counting them as independent studies.

For qualified data, assess candidate-paper graph connectivity and estimability before fitting. Select tuning parameters inside study-level validation, then assess held-out papers and chemical groups. Compare capacity error, within-paper ordering, source-deletion sensitivity and cutoff membership across justified protocol/quality analyses. Report the actual changes as new sources arrive. Formal stability thresholds and a final Top20 have not been selected from these inspected results.

Article IF is bibliographic context. It does not substitute for assay compatibility, original-data provenance or experimental precision. Article-method quality can be represented through documented exclusions and sensitivity strata while quantitative bias/variance weights require a defensible measurement model.

Reproduce with `python 02_identity_and_evidence/01_systematic_supplement/extract_capacity_followup.py`, then `python 03_candidate_selection/05_model_robustness/check_new_source_transfer.py`. This script reads the existing selected estimates and never fits them to new source outcomes. All review states remain NOT_REVIEWED and change_applied=NO.
