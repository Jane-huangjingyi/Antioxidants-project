# Model and selection protocol v1.0

The analysis specification and release inputs are fixed for reproduction of v1.0. Scientific approval remains limited to decisions already recorded in source governance. The candidate placements and material release remain pending human review.

| Decision | Inputs and rule | Missing values and authority |
|---|---|---|
| Discovery and eligibility | Use defined food-derived single compounds. Verify ID, formula, form and dietary occurrence separately. Retain standards as assay controls. | Unknown form or food evidence triggers review. Requires researcher adjudication. |
| Observation | Original value and units, locator, comparator, assay probe/endpoint, material, protocol and replicate/error definition. Only like quantities are converted. | Retain missing and conflicting fields. No imputed variance or effects. |
| Independence | Group by DOI and inspect versions, reuse, experiment clusters and materials before treating evidence as independent. | DOI counts measure report support. Unresolved independence remains unknown. |
| Activity synthesis | Compare within DOI, assay, endpoint/protocol and unit. Use reported means and assay direction. Require two different verified comparison IDs for a rank. Preserve ties. | Out-of-scope, inconsistent, censored and extrapolated outcomes are retained as held. No cross-assay composite. |
| Model diagnostic | Model log molar FL by candidate plus centered source-block effects. Fixed penalty 10 on block contrasts, from the earlier exploratory implementation. Fit connected components and use whole-report holdout. | An unseen candidate or non-estimable effect gets no prediction. Unseen protocol offsets are not applied. Strict reported pH 7.4/37 C is a sensitivity, not full protocol equivalence. |
| Experimental priorities | Apply activity, reliability and expected aqueous suitability as separate inputs. A is the qualification-first proposal with food evidence and useful chemistry contrast. B awaits source or assay clarification. C has a substantial current material, bridge or interference barrier. | There are no fitted weights or approved numeric thresholds. Current placements are curated in review_inputs.py. Unknown lot, stability or interference precludes bench release. New evidence triggers researcher re-adjudication. |
| Output QC | Verify raw provenance, input hashes, valid identity joins, grouped rank direction, release files and independent replay. | Hold conflicting records and investigate numerical drift. Version any scientific method change. |

The [original implementation](../../03_candidate_selection/09_aqueous_candidate_priority_v0.1/QC_Report.md) and [frozen diagnostics](../../03_candidate_selection/08_capacity_review_validation/README.md) supply exact source handling. Historical rubric and prior approval records retain their original scope.
