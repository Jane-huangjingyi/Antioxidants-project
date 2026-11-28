# Figure 1. Independent parts in assembly order

Figure 1 is delivered as **independent part-figures in assembly order A→B→C (no composite)**. Naming convention: `figure1_<Part>.<slug>.png` + `.svg` (editable vector pair). The current counts are 204 discovery records, 193 compound profiles, 76,383 provisional reports, 567 priority ORAC leads, 100 recorded review scopes and 467 pending; the conditional model uses 125 observations from 14 DOI reports across 51 compounds.

## figure1_A.flow_chart

The detailed screening workflow: compound discovery and database exports → title/abstract screening → full-text review → unit harmonization → conditional ORAC-FL fitting, with example search-term routes (assay, compound-class, named-compound), counts labeled by denominator, and a model-input box. Generator: [06_render_screening_workflow.R](code/06_render_screening_workflow.R). Standalone tall flow (10 × 14.7 in).

## figure1_B.evidence_screening_and_ranking

Left panel (literature evidence by compound: observed ORAC-FL percentile, typed-SD report fraction, distinct model DOI count) and right panel (conditional rank and stability). Shows the twelve retained candidates and two illustrative hold cases, ordered by conditional rank. Generator: [04_render_figure1.R](code/04_render_figure1.R). Data: [candidate rank table](../03_candidate_selection/result/table/04_figure1_candidate_ranks.csv) (193 profiles, 51 fitted conditional ranks).

| Component | Value and order |
|---|---|
| B1 Observed relative ORAC-FL | Within each DOI and protocol block with at least two compounds, fraction below the candidate plus half the tied peers; median across blocks within each DOI, then across DOIs. Larger ranks higher. |
| B2 Documented uncertainty | Proportion of model DOI reports with an explicit SD; numerator and denominator shown. Auditable reporting dimension; quality-weighted rank pending. |
| B3 Research support | Distinct DOI reports in the conditional ORAC-FL model; wider search coverage and previously confirmed independent H-ORAC studies kept in separate columns. |

## figure1_C.pathway_framework (provisional)

Top-down antioxidant pathway framework: a curated universe U1–U20 (Reactome/KEGG-anchored, see [Pathway_Universe_Curated.csv](../02_identity_and_evidence/result/table/audit/Pathway_Universe_Curated.csv)) × the 12 retained candidates. Cells are graded from the checked mechanism evidence plus a systematic NCBI literature expansion search (2026-11-26/27): **108 solid (7 functional + 101 body readout), 18 abstract-level cells, 9 cell-only, 105 searched-no-report (incl. 82 full-text-rejected), 0 pending**. 163 candidates were adjudicated (71 upgraded, 4 pathway-reassigned, 82 rejected, 2 formulation-context, 4 no-access) across OA, user-downloaded PDFs and deep search; see [Pathway_Fulltext_Verification_2026-11-27.csv](../02_identity_and_evidence/result/table/audit/Pathway_Fulltext_Verification_2026-11-27.csv). The 4 unverifiable candidates were excluded from the evidence base (researcher 2026-11-28); the download list is closed. Abstract-level candidates are NOT_REVIEWED and require full-text/identity/context verification (mixture, formulation and computational studies flagged at review); follow-up tracked in [Pathway_Expansion_Register.csv](../02_identity_and_evidence/result/table/audit/Pathway_Expansion_Register.csv) and the search inventory [Pathway_Expansion_Search_Results.csv](../02_identity_and_evidence/result/table/audit/Pathway_Expansion_Search_Results.csv). Absence of evidence is not evidence of non-participation. Generator: [07_render_figure1_C_pathway.R](code/07_render_figure1_C_pathway.R); data: [07_pathway_framework_matrix.csv](../02_identity_and_evidence/result/table/07_pathway_framework_matrix.csv). A supplementary [top-down UpSet](result/figure/supplementary/figure1_C_pathway_upset.png) shows shared-pathway intersections. **figure1_C is an independent main figure in the assembly order.** Evidence grades describe the supporting study. See the separate [researcher adjudication record](../02_identity_and_evidence/result/table/audit/Researcher_Adjudication_Record_2026-11-26.csv) for reviewed entries.

## Assembly order (no composite)

The Word manuscript embeds [figure1_A](result/figure/figure1_A.flow_chart.png) → [figure1_B](result/figure/figure1_B.evidence_screening_and_ranking.png) → [figure1_C](result/figure/figure1_C.pathway_framework.png) in this order, each as an independent PNG+SVG pair; no composite image is produced. Future parts (e.g. figure1_D) append to this sequence. Generators: [06_render_screening_workflow.R](code/06_render_screening_workflow.R), [04_render_figure1.R](code/04_render_figure1.R), [07_render_figure1_C_pathway.R](code/07_render_figure1_C_pathway.R).

## Retention rule (unchanged)

Retain a candidate when every position in the combined fit-scenario and whole-DOI-deletion range is within ten places of its expanded conditional rank; hold candidates that exceed the limit or disappear in any deletion. Under the current snapshot, 12 of 51 candidates meet the joint criterion, 21 exceed the displacement limit and 18 lose their rank after at least one deletion. The first-round fit is anchored to commit `e4c300c`; the manuscript and primary ranking preserve that checkpoint.

## Supplementary previews

Legacy component previews (figure1-1 candidate discovery, figure1-2 literature screening, figure2-1 model validation, figure2-2 rank stability), the prior detailed screening workflow (figure1a) and the prior a/b/c composite are preserved in [supplementary/](result/figure/supplementary/). The [component R script](code/02_render_manuscript_panels.R) now exports to supplementary.
