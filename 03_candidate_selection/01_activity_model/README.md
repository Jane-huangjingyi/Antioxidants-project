# 03.1 Predict molar chemical antioxidant capacity

The researcher selected molar antioxidant capacity as the primary endpoint on 2026-11-05. Reaction rate is a separate secondary endpoint. The target assay and its pH, solvent, temperature, concentration window and duration remain to be validated and fixed. This is a model-preparation step, not a new ranking.

Run from the project root:

```sh
python 03_candidate_selection/01_activity_model/audit_data.py
```

Read `results/readiness_summary.json`, then filter `results/Candidate_Capacity_Coverage.csv` for the candidate of interest. Inspect its observation IDs, original table locations and gaps in `results/Observation_Readiness.csv`. Candidate-level literature counts are not training labels. Source absence is not inactivity. Vitamin C's two historical rows are exposed without upgrading their provenance or adding them to the frozen ranking.

First recover the original measurement, mean/median definition, units, numeric error, replication unit, sample size and exposure conditions. Source studies can share data; distinct DOIs and technical repeats are not independent studies automatically. Log-scale error cannot be copied onto a molar scale, and error reported at a source concentration requires a justified transformation. No missing SD or sample size is invented. The generic modelling flag remains unapproved until the effect scale and target conditions are reviewed; it is not an assessment that every row lacks scientific value.

After the audit, compare an assay-specific random-effects baseline with a condition-adjusted hierarchical model. A conceptual model is `y_is = theta_i + beta * (conditions_is - target_conditions) + study_effect_s + error_is`. Transformation, covariance and identifiability must be decided from usable data. Predicting expected capacity is the primary objective; uncertainty is reported separately. A lower-confidence-bound ranking can be a sensitivity analysis, not a hidden change of objective. No assay conversion or multivariate pooling is assumed before overlapping measurements validate it.

Machine learning requires actual continuous capacity labels, adequate chemical coverage and held-out validation by study and chemical scaffold. It must outperform a simple baseline on the target endpoint before influencing selection. Cross-validation and any data transformations must avoid leakage. Hyperparameters are chosen by predictive performance, not whether a desired compound enters Top20.

Methodological starting points: [random-effects meta-regression](https://www.jstatsoft.org/article/view/v036i03), [multivariate evidence synthesis](https://pmc.ncbi.nlm.nih.gov/articles/PMC4142066/), and [structure-based antioxidant classification](https://pmc.ncbi.nlm.nih.gov/articles/PMC11519722/). The last study predicts ABTS/DPPH activity classes, not our continuous molar-capacity endpoint. These methods motivate assessment; none is presented as already validated for this project.

The existing review queue, frozen H-ORAC assets and all original observations remain unchanged. Next decisions are the primary assay/conditions and the targeted source-recovery order. No final coefficients, weights, ML performance or new Top20 is produced at this stage.

## Targeted source follow-up

Run `python 03_candidate_selection/01_activity_model/build_source_followup.py` after the readiness audit. It uses the committed source extractions to generate three source-linked CSV tables, without changing the original evidence. `recover_sources.py` is an optional online public-XML retrieval attempt; its current access log records failed retrievals, while the source-resolution input separately states what was readable through primary article pages. Raw XML is local and ignored.

The [priority source table](results/Targeted_Source_Followup.csv) tracks both vitamin C rows and four typed-SD rows. The Hayes paper's original Table 1 and statistical methods support ellagic acid's 151.77 +/- 3.57 g TE/100 g dry compound and three determinations. [Conditional conversion](results/Conditional_Unit_Conversion.csv) applies the same declared linear molecular-weight factor to mean and SD, yielding approximately 1.8324 +/- 0.0431 mol TE/mol. Replication independence and target-method compatibility remain unapproved. [Original paper](https://capa.ufpr.br/portal/wp-content/uploads/2017/10/Food-Chemistry.pdf).

The [paired-assay candidates](results/Paired_Assay_Source_Candidates.csv) retain three pure-parent flavonol pairs from a single paper, excluding oxidation mixtures and the Trolox reference. Their reported FL/PGR orders differ. The displayed index equation does not establish molar normalization, and the PGR method reports an unresolved 800 mM final AAPH concentration. These are source leads, not approved calibration data or target-protocol settings. [Original Table 1 and Methods](https://pmc.ncbi.nlm.nih.gov/articles/PMC12024297/).

Vitamin C and the three Foods-study SD records retain their earlier values and uncertainty states: newly recovered original tables did not close those issues this round. No missing variance is inferred from a different endpoint or a calibration-slope error. Before fitting a target-capacity model, recover remaining original tables and determine whether the proposed absorbance assay measures the intended capacity construct sufficiently well for the planned inference.
