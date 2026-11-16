# All-reference integration

All 193 current candidate profiles are considered against the complete candidate-linked master corpus. The current register contains 106167 candidate/article associations and 77594 unique article keys. Forty-four associations are added from original numeric extractions, including one article absent from the earlier linked scope. Article-level relevance, experimental independence and quality assessment remain pending for the unprocessed records.

Start with [the complete consideration register](All_Reference_Consideration_Register.csv), [candidate coverage](All_Candidate_Integration_Coverage.csv) and [conditional component orders](Expanded_Conditional_Component_Orders.csv). Each reference has an explicit role and reason. Contextual literature remains available for dietary origin, mechanisms and methodological interpretation. Article counts supply coverage information. The per-paper numeric potency-weight field remains empty while qualification is pending.

## Conditional numeric expansion

The preceding conflict-excluded dataset contributes 78 observations. Eight additional positive ORAC-FL observations have previously extracted source values or conditional parent-MW conversions. They add BJOC 2015 ferulic acid and zingerone, four Foods 2022 phenolic acids, PLOS ONE 2021 sesamin, and Molecules 2024 ascorbic acid. The curcumin source's conflicting assay column and concentration scale retain their unresolved disposition. All original values, formula assumptions and protocol issues are preserved in [the extraction register](../../02_identity_and_evidence/01_systematic_supplement/Original_Capacity_Followup.csv).

The expanded dataset contains 49 candidates, 11 source DOIs and 106 observations. Candidate/source-protocol bipartite connected components are determined before fitting. The largest component contains 48 candidates, ten papers and 105 observations. The 2022 phenolic-acid bridge joins the former four-acid component. Sesamin forms a second component with one paper and one observation. Relative locations across components require additional shared-compound evidence.

Within each component, the existing log-capacity additive candidate/source-block model is refitted using fixed shrinkage lambda=10, separately with equal-row and equal-total-DOI weighting. The transformation, penalty and solver follow [Step 03.6](../06_verified_source_update/README.md). The eight additional rows occupy their own source/protocol blocks. Positive converted values retain their conditional material assumptions. Missing variances receive no invented precision weights. This broad cross-protocol analysis preserves missing pH, material identity and assay-detail fields as unresolved. Its component positions describe model sensitivity. The earlier reported-pH/temperature analysis remains available for its own defined scope.

The current update does not estimate new held-out predictive performance. Article-quality appraisal, sampling uncertainty, compound-specific protocol effects and cross-component comparability require further evidence before final selection.

## Reproduction

```sh
python 03_candidate_selection/07_all_reference_integration/integrate_references.py
python 07_quality_control/code/validate_workflow.py
```

Inputs are the master article/link registers, the Step 03.6 analysis dispositions, the original supplemental extraction table and current candidate profiles. The master CSVs can be restored using the existing deterministic bibliographic snapshots. Source methods and references are recorded in the linked extraction registers and manuscript Methods.

The current integration also reads 20 conditional two-dose rows from Step 03.8, DOI 10.3390/antiox11091784. Both doses share one paper and occupy separate source/protocol blocks. Their micromolar-TE/reported-dose conversion retains concentration-scale and final-well dilution assumptions.
