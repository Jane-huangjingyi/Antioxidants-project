# Results

## Evidence discovery and screening coverage

The available exports yielded 76,383 provisional report records after identifier reconciliation (Fig. 1a). Automated screening used titles and abstracts for 65,424 records and titles alone for 10,959. It linked 185 of 193 compound profiles to at least one report. The priority ORAC queue contained 567 records. At the analysis checkpoint, 100 had a documented source-review scope and 467 remained pending. Targeted extraction also used original reports from earlier source-recovery work. See the [candidate evidence coverage table](../../02_identity_and_evidence/result/table/01_candidate_report_coverage.csv) and [full-text batch summary](../../02_identity_and_evidence/result/table/audit/Fulltext_Batch_Summary.json).

## Conditional ORAC-FL ranking

The conditional model used 125 observations from 14 DOI reports and covered 51 compounds. The protocol sensitivity used 130 observations from 15 DOI reports. For the same 81 estimable whole-report holdout observations, log-capacity RMSE was 0.595 for the prior model, 0.518 for the expanded conditional model, and 0.521 for the protocol sensitivity. The [rank and source-deletion table](../../03_candidate_selection/result/table/03_rank_sensitivity.csv) shows conditional ranks and their sensitivity to source choice. DOI counts describe reports. Independent experiments require separate verification.

In the separate single-report structure analysis, scaffold-holdout RMSE was 0.945 for the selected Ridge analysis and 0.953 for the matched baseline, with an out-of-fold R² of −0.24. This analysis provided no cross-report validation of structure-based predictions.

## Rank stability identified compounds for further evaluation

With the ±10-position rule, 12 of 51 ranked compounds were retained (Fig. 1c). The retained set comprised Quercetin, Catechin, Hesperetin, Genistein, Hesperidin, Myricetin, p-Coumaric acid, Chlorogenic acid, Gallic acid, Syringic acid, L-Ascorbic acid and Glutathione. Of the remaining compounds, 21 exceeded ten positions and 18 lost their rank in at least one DOI deletion. Rosmarinic acid ranked 1 in the conditional model. Its combined range reached rank 23. L-ascorbic acid ranked 50 and was supported by 7 conditional-model reports. These examples illustrate the distinct roles of observed capacity, reporting coverage and model stability (Fig. 1b,c). The [Figure 1 ranking table](../../03_candidate_selection/result/table/04_figure1_candidate_ranks.csv) records each decision. The retained compounds constitute candidates for experimental qualification in a prospective absorbance assay.
