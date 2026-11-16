# 03.6 Original-source model update

This is the current diagnostic after original PDFs and the 60-flavonoid supplement were supplied. [Source assessment](../../02_identity_and_evidence/02_user_supplied_sources/Source_Assessment.md) documents the corrected 2004 Quercetin value, unlocated Kaempferol association and 2020 conflicts. The preceding 34-candidate model reflects its earlier reference inputs. Current estimates are generated from original-source extractions with explicit dispositions.

Start with [analysis data and dispositions](results/Analysis_Data_and_Dispositions.csv), then [diagnostic orders](results/Diagnostic_Orders_and_Coverage.csv), [whole-paper validation](results/Leave_DOI_Out_Predictions.csv), [source deletion](results/Source_Deletion_Order_Sensitivity.csv), [common-universe membership](results/Common_Universe_Membership_Sensitivity.csv), and [all-candidate coverage](results/All_Candidate_Coverage.csv).

## Data and model

Five supplied ORAC reports provide 116 FL source rows. Tabart 2009 adds 24 Trolox-normalized ratios with unreported ORAC pH and absent table errors. Current-index mappings and exclusions determine the analysis sets. The previously recovered original 2023 Table 3 contributes five FL AUC-slope ratios, counted once. Its buffer and 5%-ethanol/matched-Trolox measurements occupy distinct reported protocol blocks. Paper-level validation removes all blocks from the omitted DOI together.

For a reported positive mean capacity m, fit y=log(m), with candidate location alpha and reported source/protocol-block effect u. The objective is

$$\sum_r w_r (y_r-\alpha_{i(r)}-u_{b(r)})^2 + 10\sum_b u_b^2,\qquad \sum_b u_b=0.$$

The fixed shrinkage value 10 reuses the preceding exploratory setting. Outcomes in this update supply no new tuning. Baseline estimates are candidate means of source log means. OLS, fixed shrinkage and equal-total-DOI-weight shrinkage are retained in Candidate_Model_Estimates.csv. Equal-row fitting uses w=1. The weighting sensitivity uses w=N/(P*n_s), where n_s is a DOI's row count, N is the variant's total row count and P is its number of DOIs. This gives equal total influence to DOIs. It represents a source-influence sensitivity. Sampling variances and article-IF weights remain unestimated.

The fitted exp(alpha) is a conditional geometric location under the training-centered block convention. A common standardized assay's expected arithmetic capacity requires protocol qualification and a justified response distribution/retransformation. Final solvent fractions and compound-specific protocol effects are incompletely identified here. A block effect cannot establish their removal.

## Analysis variants

| Variant | Candidates | Rows | DOIs | Reported protocol blocks | Single-DOI candidates |
| --- | --- | --- | --- | --- | --- |
| Reported pH 7.4 and 37 C | 23 | 34 | 4 | 5 | 16 |
| Extended names with unknown-pH 2020 source | 43 | 82 | 6 | 7 | 20 |
| Extended with recorded source conflicts excluded | 41 | 78 | 6 | 7 | 19 |

Every variant excludes the three numeric/alignment-conflict rows and ambiguous duplicate compound 27. The third variant additionally excludes all recorded identity-annotation conflicts. Exact chemical forms and full protocol alignment remain qualification fields across the sets. Core-condition matching is the stated reported-pH/temperature filter.

Held-out comparison uses training outcomes only, with an average training source-block effect of zero for prediction. Estimability is checked in the unpenalized design before scoring. A paper with new candidate identities can leave those outcomes unestimable. This coverage is visible in Leave_DOI_Out_Design.csv. The identity-indicator model supplies no predictions for an entirely held-out chemical scaffold or unseen candidate.

| Variant | Matched held-out rows | Fixed-shrinkage log RMSE | Baseline log RMSE |
| --- | --- | --- | --- |
| Reported pH/temperature | 11 | 0.4006 | 0.3939 |
| Extended names | 62 | 0.4986 | 0.5045 |
| Recorded conflicts excluded | 59 | 0.4686 | 0.4766 |

Different variants evaluate different outcomes. The core-condition model has no improvement over its baseline on these matched rows. Extended sets show a modest improvement on their own comparisons. The evidence remains concentrated in four or six source papers and many single-source candidates.

Source-deletion fits record absolute-location estimability and candidate-pair contrast estimability. The row-space projection uses relative singular-value tolerance 1e-12 and contrast residual tolerance 1e-8. h estimable higher candidates imply position >=h+1, while l estimable lower candidates imply position <=N-l in the variant's fixed universe. Bounds retain unidentified candidates' possible positions. Missing comparisons contribute no inferred low activity. These are model-identification and sensitivity bounds.

The name-based and recorded-conflict-excluded models share 41 candidates. Their Top20 sets within that common universe overlap in 19 members, with Myricetin replaced by Hesperetin after conflict exclusions. This comparison uses a shared candidate universe. The other two common-universe comparisons contain only 23 candidates, so a 20-member overlap has limited discriminatory value. Global ranking across all 193 profiles remains unresolved.

## Reproduction and figures

```sh
python 03_candidate_selection/06_verified_source_update/fit_verified_source_diagnostics.py
Rscript 05_analysis/R/render_verified_source_diagnostics.R
python 07_quality_control/code/validate_workflow.py
```

The model imports the existing shrinkage solver in Step 03.5 and uses the project's existing NumPy environment. Figure colors, sizes, fonts, labels and dimensions are editable at the top of the complete R script. [Held-out predictions](../../06_manuscript/figures/Verified_Source_Heldout/analysis_v0.1/png/Verified_Source_Heldout.png) and [source-deletion order sensitivity](../../06_manuscript/figures/Verified_Source_Order_Sensitivity/analysis_v0.1/png/Verified_Source_Order_Sensitivity.png) each have a matching text/vector SVG in the corresponding `svg` directory.

Next close the 2020 identity/value conflicts and missing protocol fields, and qualify additional independent source rows. Structure-based prediction of uncovered candidates requires a separately validated structural model. Current orders retain NOT_REVIEWED, change_applied=NO and an empty global-193 rank.

The [evidence stability assessment](Evidence_Stability_Assessment.md) and [joined candidate table](results/Candidate_Evidence_and_Stability.csv) show DOI support, original locators, deletion bounds and weighting sensitivity. Reproduce with `python 03_candidate_selection/06_verified_source_update/build_evidence_priorities.py`.
