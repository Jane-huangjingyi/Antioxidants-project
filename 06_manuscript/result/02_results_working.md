# Working Results 1. Literature-informed candidate prioritization

## Literature screening

The available exports yielded 76,383 provisional report records after identifier reconciliation. Automated screening used titles and abstracts for 65,424 records and titles alone for 10,959. It linked 185 of 193 compound profiles to at least one report. The priority ORAC queue contains 567 records, with 84 scoped reviews recorded and 483 records pending. Final scientific eligibility remains open. See the [candidate evidence coverage table](../../02_identity_and_evidence/result/table/01_candidate_report_coverage.csv) and [full-text batch summary](../../02_identity_and_evidence/result/table/audit/Fulltext_Batch_Summary.json).

## Conditional ORAC-FL ranking

The conditional model used 125 observations from 14 DOI reports and covered 51 compounds. The protocol sensitivity used 130 observations from 15 DOI reports. For the same 81 estimable whole-report holdout observations, log-capacity RMSE was 0.595 for the prior model, 0.518 for the expanded conditional model, and 0.521 for the protocol sensitivity. The [rank and source-deletion table](../../03_candidate_selection/result/table/03_rank_sensitivity.csv) shows conditional ranks and their sensitivity to source choice. DOI counts describe reports. Independent experiments require separate verification.

With the ±10-position stability rule, 12 of 51 ranked compounds were retained for further evaluation. 21 exceeded ten positions and 18 lost their rank in at least one DOI deletion. The [Figure 1 ranking table](../../03_candidate_selection/result/table/04_figure1_candidate_ranks.csv) records each decision. Experimental validation in the selected absorbance assay remains a future step.
