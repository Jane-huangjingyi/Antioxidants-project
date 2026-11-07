# Protocol constraints on the source bridge

Run `python 03_candidate_selection/01_activity_model/build_bridge_protocol_matrix.py` to regenerate `results/Bridge_Protocol_Matrix.csv` and `results/Bridge_Pairwise_Decisions.csv`. Five original sources and six named-overlap pairs are represented. These source-level shared names do not assert that all their numerical rows have already been rechecked or that exact chemical forms match. The 30-record verification table remains authoritative for that narrower scope.

The eugenol Foods source explicitly uses sample/Trolox net-AUC calibration-slope ratios, 55 minutes and pH 7. The 2014 phenolic-acid source uses a Trolox net-AUC regression, 60 minutes, pH 7.4 and four replicates; it does not establish four independent batches. The 2022 phenolic-acid source uses 80 minutes with two reported compound concentrations. The Sakurai paper invokes a standardized SOP whose complete equation and timing are still to be recovered. Thus, matching molar units and overlapping compounds are necessary provenance checks but do not demonstrate a single exchangeable outcome.

The 2014 ORAC Methods provide direct detail rather than the previously unresolved generic replicate description. However, the experimental plus/minus definition still needs verification. A four-replicate statement cannot by itself justify dividing a reported error squared by four. The Foods independent-experiment SD permits a conditional variance candidate, while the other sources' unresolved replication, endpoint errors and calibration covariance remain explicit. Missing conditions are blank rather than copied from neighbouring studies.

## Current model decision

All six source pairs remain DO_NOT_POOL_CURRENTLY. This is an integration decision, not evidence of low antioxidant activity. Adding arbitrary quality points or journal weights would not solve endpoint incompatibility. Within-paper observations can support source-specific descriptive comparisons; a cross-paper target-capacity model requires justified harmonization, enough shared compounds, and a predeclared target protocol. Source-specific ranks should not be labelled the experimental Top20.

Next recover the Sakurai standardized SOP and clarify error/independence definitions for the bridge papers. If harmonization remains unsupported, use separate method-family analyses and validate a shared compound panel experimentally after device selection. No FL-to-absorbance conversion is inferred. All source HOLDs, formal observations, frozen ranks and NOT_REVIEWED states are retained; change_applied remains NO.

## Primary-source locations

- Foods: https://pmc.ncbi.nlm.nih.gov/articles/PMC8392586/ (Methods 2.5.4, Table 5).
- Sakurai: https://pmc.ncbi.nlm.nih.gov/articles/PMC8981064/ (Methods 2.2, Table 1).
- Skroza: https://pmc.ncbi.nlm.nih.gov/articles/PMC9495677/ (Methods 2.1, 2.2.2, Table 2).
- Koroleva: https://pmc.ncbi.nlm.nih.gov/articles/PMC4200783/ (Methods 3.2.3, Table 2).
- Antioxidants 2023: https://pmc.ncbi.nlm.nih.gov/articles/PMC9951910/ (ORAC Methods, Table 3).

The numerical protocol entries are curated from previously recovered original text and the targeted original HTML check; the builder is offline. Online source refresh is a separate explicit operation. No new source article was claimed recovered in this step.
