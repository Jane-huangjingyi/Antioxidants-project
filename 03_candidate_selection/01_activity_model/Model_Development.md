# Current modelling outcome

The exploratory source-specific modelling pipeline is complete. Joint nested selection gave pooled MAE 0.695 and RMSE 0.945 against baseline 0.689 and 0.953; out-of-fold R-squared was -0.240. The model did not establish a consistent predictive improvement. Six-descriptor ridge (alpha 10) was selected for the full-development artifact, and mapped-candidate order was sensitive to scaffold-group removal. Only 16 of 193 current profiles are mapped; no score or negative activity inference is assigned to the remaining 177. A formal cross-paper primary model and global Top20 are not established.

Run from the project root:

```sh
python 03_candidate_selection/01_activity_model/run_model_checks.py --figures
```

The runner regenerates source/condition audits, model comparisons, nested selection, manuscript Results and three editable PNG/SVG figure pairs. R requires ggplot2 and svglite; chemistry dependencies are pinned in `requirements_structure.txt` and the local `.runtime_chem` environment is excluded from Git. The JSON artifact records scaling and coefficients. Its predictions are log locations under one source protocol, not arithmetic mean molar capacities or target absorbance results.

Inspect [completed metrics](results/completed_model_summary.json), [held-out predictions](results/Completed_Model_Heldout_Predictions.csv), [group errors](results/Completed_Model_Fold_Metrics.csv), [mapped-candidate diagnostics](results/Mapped_Candidate_Model_Diagnostics.csv), [all-profile coverage](results/Candidate_Model_Coverage.csv) and [exported artifact](results/completed_exploratory_model.json). The mapped positions are in-sample diagnostic order and refit influence, not validated potency ranks or an experimental panel. Verification passed: held-out-label perturbation left training selection/predictions unchanged; an independent primal ridge solution matched the exported dual coefficients; artifact reload reproduced predictions; all source/frozen hashes and SVG text/vector checks passed. Prior development/source-review records follow and retain their original scope.

# ORAC-FL model development

## ORAC-FL capacity model and validation protocol

On 2026-11-08 the researcher selected ORAC-FL molar capacity as the first modelling endpoint, followed by empirical validation of transfer to a future absorbance assay. This decision does not approve individual evidence rows, target conditions or a final ranking. The machine-readable rules are `inputs/model_protocol_v0.1.json`; run `check_model_protocol.py` for the current fold-design diagnostic.

The first comparison is an interpretable within-family baseline versus a study/condition-adjusted model, if its effects are estimable. Do not fit a complex model merely to obtain a complete candidate order. The primary score is expected conditional capacity, with uncertainty alongside it. Estimator family, vehicle, timing and other target conditions must be fixed or explicitly stratified before interpreting a common ranking. Methodological differences are not automatically proof that adjustment is impossible; they require data and validated assumptions.

Validation holds out complete papers/data-generating studies, including all their doses and technical replicates. Reused data across papers must be grouped together. All preprocessing and tuning remain within training folds. Structural models additionally need scaffold/applicability checks and evaluation on unseen compounds. Assess prediction errors, uncertainty calibration and rank stability where held-out comparable data support them. No numerical acceptance threshold is invented at this stage.

The nine-row model-candidate subset contains three papers and no compound measured in more than one of them. Under the confirmed primary core conditions, six rows from two papers remain in the condition-coverage diagnostic; three pH 7.0 observations stay outside that scope. Both core-condition leave-paper-out coverage checks contain entirely unseen test compounds. These coverage checks are not approved validation folds. A compound-identity-only model cannot predict those held-out effects. This does not apply automatically to a future structure-based model, nor does it imply the broader 99-row inventory lacks overlaps. New source-rechecked bridges are not yet eligible for a common-effect fit. The immediate data task is to close method/scale/error gates on the bridge observations, then rebuild model inputs and reassess the folds.

First implement supported family-specific analyses. Only adopt a more complex model when its held-out performance and assumptions support the target. ORAC-FL prediction and absorbance transfer remain two distinct validation stages. No new score, final Top20 or scientific approval is generated here.


## Extended model-input review

Run `build_extended_model_inputs.py` after `build_analysis_entry.py`. It replaces reliance on the nine-row preparation subset with an explicit review of all 31 rechecked observations in the 99-row inventory. This is a proposed modelling view, not evidence approval. Separately extracted leads outside that inventory are not silently appended.

The view contains eight papers, two source-identity holds and 29 observations usable for source-specific description. Three conditional variance candidates retain their original assumptions; they are not approved meta-analysis weights. Seven estimator/scale-review families expose unresolved transformations and protocols. These families are working review partitions, not a claim that harmonization is theoretically impossible. In particular, mass normalization is a transformation issue rather than a separate chemical assay; its row remains separate until the target estimator and experimental conditions are reviewed.

The slope-ratio family contains two papers but no common compounds in this integrated subset; its papers also differ in protocol conditions. Other groups currently contain one paper each. Therefore no supported leave-paper-out validation of compound-identity effects is available within these working partitions. This does not rule out a structure-based model or an explicitly justified hierarchical model; neither has yet demonstrated predictive performance. Do not turn source-group administrative separation into a claim that these methods measure unrelated biology.

Next expand original experimental labels and material/endpoint annotations together. The existing 36-flavonoid log-scale extraction is a useful source-specific candidate for a structural prediction baseline, but must first be mapped to the food-chemical universe and checked for raw-scale/error interpretation and scaffold coverage. It cannot substitute for cross-study external validation. Decide and document the target estimator/conditions before reporting a global capacity rank. No fitted coefficient, validation metric or Top20 is invented here.

Outputs: `results/Extended_Model_Input_Review.csv`, `results/Extended_Validation_Feasibility.csv` and `results/extended_model_readiness.json`. Original sources, scientific review states and frozen rankings remain unchanged.


## Source-label crosswalk and null prediction benchmark

Run `map_flavonoid_labels.py`. Of 36 original experimental log-ORAC rows, 16 match current candidate names exactly and 20 do not. Exact matches carry reference CID, InChIKey and formula but still require source-form equivalence. Unmatched compounds are not assigned existing candidate IDs or added to the food panel. No synonym, stereochemistry or glycoside substitution is inferred from a similar name.

The script establishes an intercept-only prediction benchmark using all 36 source labels. For each held-out source row, the prediction is the mean of the other 35 log-ORAC values. Internal MAE is approximately 0.663 and RMSE 0.873 on the natural-log scale. These are null-model errors, not demonstrated structure-model performance or external validation. No error bars from the source table enter the calculation; their experimental statistic remains unresolved. The benchmark uses source rows outside the current candidate universe solely to characterize this source dataset, not to nominate them for experiments.

The next structural model must improve on a suitable null baseline under a declared validation design. All labels currently come from one paper, so a held-out-paper test is unavailable within this dataset. Row-wise internal assessment must not be presented as independent-study generalization. Obtain validated molecular graphs/descriptors for all intended training rows, document stereochemistry and source identity, and assess scaffold grouping before selecting model complexity. Molecular formula alone does not distinguish positional isomers or provide a complete structure representation. The current default Python environment has no RDKit/scikit-learn/numpy available; no dependency has been installed and no graph descriptors invented.

Current outputs are `results/Flavonoid_Candidate_Crosswalk.csv`, `results/Flavonoid_Null_Baseline.csv` and `results/flavonoid_mapping_qc.json`. No structural coefficients, new-candidate predictions, global capacity ranks or human approvals are generated. All original and frozen records remain unchanged.


## Structure mapping and grouped validation

`recover_flavonoid_structures.py` is an explicit online PubChem refresh. It requests stored CIDs for mapped candidates and names for unmatched source rows. Responses, hashes and multiple-hit information are retained in `inputs/flavonoid_structure_candidates.json`; raw responses stay local. Run `audit_flavonoid_structures.py` to reproduce the scoped audit offline.

A PubChem record is a candidate graph. Reference InChIKey agreement does not establish the original experimental material's stereochemistry. Name-only hits require comparison against the source's explicit structure; no record is promoted into the food universe automatically. For stereogenic structures, compare original drawing, supplementary optimized geometry and reagent identity. Do not assign an enantiomer from a common name or assume a racemate.

Validation design: first group identical constitutional connectivity (InChIKey first block) so stereoisomers or duplicate graphs cannot appear on both sides of a split. This is a leakage-control key, not a Bemis-Murcko scaffold. Then compute non-isomeric Bemis-Murcko scaffolds with a pinned graph toolkit and inspect whether generic ring frameworks collapse too many flavonoids into one group. If they do, report the collapse and compare predeclared scaffold and fingerprint-cluster splits without tuning the split to improve performance. Cluster thresholds and fold count remain unset until the graph coverage and group sizes are inspected. No invented scaffold folds are exported.

Keep all observations for a compound and all reused data together. Fit descriptors, preprocessing and model tuning within training folds. Report unseen-structure prediction against the intercept-only baseline, with group sizes, unsupported folds and applicability domain. One-paper internal structural validation remains distinct from leave-study-out external validation. No structure model is fitted until graph mapping and grouping are checked.

## Computed scaffold update, 2026-11-08

All 36 candidate graphs are now available and parse with RDKit 2026.09.1. One graph (CID 145826) uses the exact fields from a successful short API response retained as a structured extraction, not raw HTTP bytes; its atom stereo counts remain missing. The other 35 have cached-response provenance. `build_scaffold_groups.py` computes five non-isomeric RDKit Murcko groups with sizes 23, 8, 3, 1 and 1; genericization yields four frameworks. These are provisional database-graph groups, not approved original-material identities. Same-connectivity grouping is asserted, including Catechin/Epicatechin.

Install the pinned `requirements_structure.txt` into the ignored `.runtime_chem` directory using Python 3.12, then run the structure and stereo audit builders followed by `build_scaffold_groups.py`. No runtime packages are research deliverables or Git inputs. The generated `results/Flavonoid_Scaffold_Groups.csv` and `results/scaffold_group_qc.json` record group membership and toolkit version. A leave-scaffold-out design must report its 1-member test groups and the 23-member dominant group; random row CV is not a substitute. Source drawings and supplementary geometries are still unreviewed because source access was unavailable; source-material stereochemistry is not approved.

## Error diagnosis and feature sensitivity

The four-descriptor representation has eight collision sets, including Catechin/Epicatechin, Quercetin/Morin and several differently hydroxylated positional isomers. Six held-out rows have at least one descriptor outside their corresponding training range. These observations identify limited representation and coverage, not a demonstrated causal explanation for source-label differences. Adding phenolic-OH and aryl-methoxy counts changes pooled MAE/RMSE to 0.673/0.927 versus the matched mean baseline 0.689/0.953. This is a small post-hoc gain, not independent confirmation. Neither source labels nor test groups were changed. The next model-development step should evaluate positional graph information and label/material consistency, then seek a new independent-study test set; repeating model selection on these same outer folds cannot supply that test. No final ranking is justified yet. Methods and Results include this distinction and reproduction commands.

## Morgan fingerprint sensitivity

Radius-2, 1024-bit non-chiral Morgan fingerprints yield 35 distinct vectors for the 36 candidate graphs. Using the same nested scaffold protocol, ridge MAE/RMSE are 0.652/0.914 versus the mean baseline 0.689/0.953. Four of five scaffold folds improve by MAE, but the three-member catechin-related fold worsens to 0.922 versus 0.350. This subgroup failure must remain visible; pooled improvement is not a validated global rank. Catechin/Epicatechin retain identical fingerprints because chirality is deliberately excluded pending source-material identity checks. No labels were changed, and no outer fold was omitted. This is post-hoc method development; further model selection on these same labels does not create independent confirmation. Methods/Results document the procedure and references.

## Reproduce this model-development milestone

With Python 3.12, install `requirements_structure.txt` into `.runtime_chem` at the project root, then run `python 03_candidate_selection/01_activity_model/run_model_checks.py`. This offline entry rebuilds preparation tables, candidate graph audits, scaffold groups, the four-descriptor, six-descriptor and Morgan comparisons, diagnostics and manuscript Results. It does not refresh network sources, approve source identity, predict a final panel or modify frozen observations. Package files remain ignored. The default `run_pipeline.py --tables-only` remains the core evidence workflow; structural development is an explicit additional step.

## Catechin labels and independent-source preparation

`audit_catechin_and_external_sources.py` checks the three original catechin-related log labels against legacy back-transformed numbers. All three legacy rows have a scale/unit-label conflict; the training labels already use the original log column, so no label repair changes model metrics. The script constructs a retrospective queue of 28 observations from ten other papers covering 13 mapped compounds. These are not yet approved external labels, and they are not blind data. DOI/source independence, method equivalence, exact scale and material identity must close before test-set locking. The ORBi record for 10.1016/j.foodchem.2008.08.013 currently offers request-copy rather than accessible original numeric text; no request was sent and no full-text reading claimed. Other DOI access attempts did not recover new original tables this round.

## First retrospective external-source recovery

The original Ishimoto advance-view PDF (10.1271/bbb.110717) explicitly reports (+)-Catechin 9.0 and (-)-Epicatechin 10.0 mol TE/mol in its Results. Methods specify pH 7.0, 37 C, 90-minute observations and quadratic concentration/net-AUC regression. SD is defined for three separate experiments but numeric SDs were not estimated from figure bars. The scoped extraction is `inputs/ishimoto_external_source_check.json`. Two rows in the external-source queue now carry verified original means and source named isomers, but remain pending common-target and material-equivalence review; no external metric, fit or blind-test claim is generated. The retrieved version is labelled advance-view rather than final pagination.

## Second external-source check

Rothe Table 6 experimental ORAC means and reported plus/minus values were verified in the original open-access PDF. The external queue now contains four original-mean checks across two papers. Normalization, pure-compound errors and material equivalence remain unresolved; beer or literature columns were not imported as experimental compound labels. No model was refitted or scored against this queue. Methods reference 8 documents this scope.

## Retrospective protocol-shift diagnostic

Run `python 03_candidate_selection/01_activity_model/run_model_checks.py` from the root to regenerate development models, source checks, the pressure test and manuscript outputs. Development-only group CV selected alpha 10. Both known compounds received log prediction 1.5796, below source log arithmetic means 2.1972 and 2.3026. Model MAE/RMSE were 0.6703/0.6724, compared with 0.9690/0.9704 for the development-mean baseline. This two-observation retrospective diagnostic does not establish external or new-structure validity. Material identity, summary-estimand differences and missing numeric SD remain unresolved. No ranking or settings were changed using these outcomes; common-target validation remains HOLD.

## Rothe targeted source decision

The 2026-11-08 recheck retained both Table 6 records on HOLD. Checked sections establish TE calibration and four measurements but do not close the pure-compound molar denominator, hydrate concentration basis, epicatechin reagent identity or plus/minus definition. See the structured `targeted_recheck` in `inputs/rothe_external_source_check.json` and row-specific requirements in `results/External_Comparability_Decisions.csv`. No numeric conversion, pressure-test expansion, variance weighting or training update was performed. Source-method references do not supply missing details of this experiment. The next useful evidence is original calculation/material documentation or additional directly normalized studies.

## Matched-calibrator gate

The Carvalho recheck closes the molar-estimator trace for one queued record. A matched-matrix calibrator is now explicit in the source decision; the row stays outside fitting and pressure testing until remaining material and estimand checks close. Source audit totals: five original means across three papers; zero approved common-target external labels. Existing model settings and n=2 diagnostic are unchanged.

## Batch external-source and modelling-readiness milestone

The offline runner now also generates paper-level readiness and scoped connectivity tables. Six means across four papers have been checked, including baicalein with an explicitly reported SEM; four records have traced molar estimators. No common-target external label is released. The ten-paper queue has no repeated observation key, which does not close shared-data independence. Three ACS originals were denied, one repository offers request-copy access, and two further sources remain preview/access-limited. These are access findings, not negative activity evidence.

The external-only graph and the development-anchored graph are reported separately. Adding four traced external observations to all 36 development rows connects the design (40 edges, rank 39), with only one redundant edge. Material/protocol/estimand gates remain decisive. No cross-paper model or rank is fitted. Priority is original multi-compound tables with shared verified compounds, followed by source-specific identity and estimator checks; additional model architectures cannot replace those inputs.

## Publisher recovery and normalization milestone

The Paillat publisher full text was recovered after the earlier DOI-only access failure. Both mapped microplate entries were extracted; the baicalein entry is an additional observation, not a new candidate or independent paper. Audit queue: 29 records across ten papers; eight numeric source values rechecked across five papers. Two parent-reference conversions are held separately from the four traced molar-estimator records. Unknown microplate protocol and uncertainty were not filled from the online arm. Conditional-row topology adds one further closed loop (42 edges, rank 40) to the development anchor, without changing eligibility or model fitting.

The evidence schema now uses `original_value_verified`, `original_summary_statistic` and `source_reported_material_name`: a table value is not automatically a mean and a reagent name is not stereo approval. `Source_Normalization_Audit.csv` preserves original units, reference constants, arithmetic and restrictions. Original training labels, selected penalties, two-row pressure test and frozen selection are unchanged.

## Current analysis-set authority

Use `results/Analysis_Set_Decisions.csv` to inspect each reference, original label and recovered addition; `results/analysis_set_manifest.json` pins their inputs and permitted analysis roles. Reproduce with the existing offline runner. The 136 provenance rows contain 14 non-analytic alternate representations, 36 authorized exploratory training labels, two separate authorized pressure-test observations and 84 waiting records. The primary common-target set remains empty; this is not evidence that the compounds lack activity. Primary scope is now fixed to pH 7.4 and 37 C with explicit vehicle/AUC/integration strata; source-material/stratum alignment and study independence still need closure. The original 36-label input remains the structural model authority; no duplicate or conditional value is silently added.

Fourteen development-source references were matched by compound, DOI, Table 3 locator and arithmetic: thirteen rounded exponentials and one direct log value. Missing variance alone does not rule out unweighted regression; it rules out invented inverse-variance weights. Table recovery priority is now explicit in `External_Paper_Readiness.csv`, ordered by unresolved observation coverage rather than chemical activity. No new model acceptance thresholds or scientific approvals were assigned.

The researcher confirmed that primary scope on 2026-11-09. `inputs/model_protocol_v0.1.json` retains its existing path and now declares internal protocol version 0.2. Null vehicle/window/estimator target values denote source-specific stratification, not permission to impute a common setting; readiness checks distinguish these fields from an unset fixed target. Every disposition row now reports core-condition matching separately from eligibility. The pH 7.0 diagnostic remains sensitivity-only.

## Protocol lineage closure for the phenolic bridge

The accessible Sakurai original and its cited Watanabe SOP have now been traced separately. Nine existing records have direct pH evidence and shared A/B temperature support, explicitly tagged as inherited rather than confirmed execution. The cited reference range matches the B benchmark and twice its reproducibility SD; neither fact authorizes assignment of the executed SOP or a compound SD. Final solvent, dilution/estimator variant, run confirmation and independent preparation remain unresolved. See `Protocol_Lineage_Check.csv`; no new measurements, error replacements, model labels or ranks were generated. This check reduces the unknown-condition inventory without changing the 36-label model or the two-observation pressure test.

## Scope-consistent validation diagnostics

`protocol_scope.py` now supplies the shared condition lookup to all three readiness/disposition builders. The 31-row extended review contains seven direct core-condition matches, three outside-scope rows, seven inherited-SOP rows and fourteen unconfirmed rows. Direct matches occupy five source-specific pending strata; no stratum currently supports a cross-paper validation fold. This result concerns the reviewed subset, not every observation in the project. Gallic acid has conflicting original stock-solvent descriptions and stays in its own unresolved vehicle stratum. Source descriptions and arithmetic remain recorded without assumed correction. The 36-label model and n=2 pressure test are unchanged.
