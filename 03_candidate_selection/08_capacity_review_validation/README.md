# Capacity source review and connected validation

This stage reconciles existing original-source extractions, adds a targeted 2024 kinetic-study audit and validates the connected conditional capacity set. The [capacity row review](Capacity_Row_Review.csv) contains 203 source rows from 15 DOIs, including other probes, unmapped compounds and unresolved endpoints. The [all-candidate progress table](Candidate_Review_and_Inclusion_Progress.csv) distinguishes retrieved associations, located leads, source-row-audited DOIs, extracted rows and conditionally analyzed rows for all 193 profiles. These counts retain their reading scopes. They do not establish complete scientific review of the bibliographic corpus.

## Source decisions

Original means, units, errors, materials, protocol fields, source locations and experiment clusters are retained. Missing independent sample sizes remain blank. Multiple compounds or technical repeats from one DOI share source dependence. Existing 2020 identity/value conflicts and the ambiguous duplicate rhamnoside row remain excluded from this validation input. The original 2004 Quercetin correction is retained. Secondary literature values require their cited original-source keys before quantitative inclusion.

The fresh PMC10886186 review checks DOI 10.3390/antiox13020222 Table 3 and sections 2.1-2.4/2.13. Five relative-AUC values are 4.0 +/- 0.4, 3.3 +/- 0.2, 2.0 +/- 0.1, 3.9 +/- 0.1 and 3.8 +/- 0.1 for p-coumaric, ferulic, sinapic, caffeic and chlorogenic acids. The source defines AUC(AH)/AUC(Trolox), pH 7.0, 37 C and 120-minute acquisition. Explicit net-AUC subtraction and column-specific error hierarchy remain unresolved. Kinetic parameter uncertainty arises from fitting; general triplicate/SD wording does not settle every column's hierarchy. Buffer concentration differs between sections. These five rows retain DISTINCT_AUC_ENDPOINT_HOLD and supply no fitted labels.

## Validation results

The full conditional dataset retains 52 candidates and 12 DOIs in two disconnected components, as described in [Step 03.7](../07_all_reference_integration/README.md). This validation uses the largest component, comprising 51 candidates, eleven DOIs and 113 rows. Twenty candidates have one DOI. The reported-pH-7.4/37-C subset contains 24 candidates, six DOIs and 37 rows. This subset retains material and protocol qualification gaps, including the printed 2024 AAPH unit ambiguity.

The existing fixed-lambda-10 model and validation code are reused. Whole-paper holdout removes all blocks from the omitted DOI and scores only estimable training-candidate locations. Expanded log RMSE is 0.6306 versus 0.6755 for the matched baseline, over 75 estimable outcomes. The reported-pH/temperature subset gives 0.4128 versus 0.4151 over nine outcomes. Different sets score different observations. The improvement is small.

The inherited name-based and conflict-excluded labels use the same already-conflict-excluded input here. Their agreement reflects identical data. It contributes no independent robustness evidence. The core-condition comparison shares only 24 candidates with the expanded set.

The [Top20 sensitivity table](Top20_Conditional_Uncertainty.csv) joins source counts, equal-row and equal-total-DOI positions and source-deletion identification bounds. Equal-row and DOI-balanced Top20 sets overlap in 15 members. Catechin, Quercetin, Hesperetin and Protocatechuic acid retain worst-case positions within 20 across recorded deletions. These bounds are conditional on the model and fixed candidate universe. Sampling intervals and calibrated Top20 probabilities remain unestimated. Final Top20 selection remains open.

## Reproduction

```sh
python 03_candidate_selection/08_capacity_review_validation/extract_bridge_source.py
python 03_candidate_selection/07_all_reference_integration/integrate_references.py
python 03_candidate_selection/08_capacity_review_validation/review_and_validate.py
Rscript 05_analysis/R/render_verified_source_diagnostics.R 03_candidate_selection/08_capacity_review_validation/results Reviewed_Capacity
python 07_quality_control/code/validate_workflow.py
```

The R script exposes colors, fonts, dimensions and line/point settings and exports matching PNG/SVG pairs under manuscript figures. Input CSVs, held-out predictions, deletion fits and row weights are in this directory and its results subdirectory. New qualified sources should first update the extraction registers, then rerun the commands.

Priority source work remains independent original capacity studies for leading single-DOI candidates and shared compounds connecting sesamin to the enlarged component. The current reviewed and included counts must be read alongside the substantial unprocessed corpus.

## New original bridge source

DOI 10.3390/antiox11091784, PMC9495677, Table 2 provides 20 original ORAC outcomes for ten phenolic acids at reported 2.5 and 5 micromolar concentrations. Section 2.1 describes Sigma standards and 80:20 ethanol/water stocks, section 2.2.2 reports 80-minute fluorimetric measurements and three replicates. The cited method DOI 10.3390/md20010064 specifies fluorescein and 37 C. The bridge paper's pH, final solvent fraction, replicate independence, plus/minus definition and final-well concentration scale remain unresolved. Raw micromolar-TE values and conditional TE/reported-dose ratios are retained together. Mixture outcomes supply no individual-compound labels.

Separate reported-dose blocks preserve both concentrations within one paper. A single-dose sensitivity refits the same 51-candidate set using either 2.5 or 5 micromolar rows. Top20 overlap is20/20 under equal-row and19/20 under equal-total-DOI weighting. The numeric bridge connects the four-acid component; sesamin remains disconnected. The conditional analysis shows appreciable dose/source sensitivity.

## Sesame-lignan targeted follow-up

[The targeted audit](Sesame_Lignan_Targeted_Audit.csv) preserves three original reported ORAC values from DOI 10.1007/s13197-014-1334-6. Indexed original-source methods, results and Figure 2 caption were checked. Public XML recovery returned HTTP500. The reported micromol-TE/mL outputs lack an unambiguous compound molar denominator. AAPH differs between methods (60mM) and caption (10mM); emission differs between 512 and 515nm. Source errors and independent experimental units remain unresolved. The three values retain a unit/protocol hold and contribute no new model label. Source materials are isolated sesame-oil sesamin/sesamolin and commercial sesamol, with >98% purity stated.

## Citrus single-source follow-up

Run `python 03_candidate_selection/08_capacity_review_validation/extract_citrus_source.py` before integration to reproduce nine original Table4 rows. Four parent-mapped rows add a source DOI to the conditional model. The printed compound100mg normalization is preserved separately from extract per-g methods. Exact forms, pH, final solvent and independent replicate units remain unresolved. The newly expanded model covers52 candidates and12 DOIs overall;51 candidates and11 DOIs form the connected validation set.

## Historical parent-name reconciliation

Four existing observations from Tabart et al. (2009), DOI 10.1016/j.foodchem.2008.08.013, were reconciled through a separate parent-name overlay. Hyphenation variants identify kaempferol 3-O-glucoside, cyanidin 3-O-rutinoside and delphinidin 3-O-glucoside; myricetin-3-rhamnoside is conditionally mapped to Myricitrin. Original evidence IDs, table values and source spelling are retained. Exact salt, sugar anomer, purity and final vehicle remain unresolved. Each observation occurs once in the consolidated audit. This historical source adds no new paper and remains outside the 2020–2026 review window. Three additional candidate identities enter the conditional connected analysis; Myricitrin gains an existing-paper observation.

Run `python 03_candidate_selection/08_capacity_review_validation/resolve_known_source_names.py` before integration and validation to reproduce the overlay.
