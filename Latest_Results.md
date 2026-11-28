# Latest results

New to the project? Start with the [project handoff and next actions](README.md#start-here).

## Manuscript Part 1

- [Part 1 manuscript (Word)](06_manuscript/result/Manuscript_Part1_Nature_Communications.docx)
- [Methods](06_manuscript/01_methods_working.md)
- [Results 1](06_manuscript/result/02_results_working.md)
- [Candidate rank sensitivity](03_candidate_selection/result/table/03_rank_sensitivity.csv) and [model validation](03_candidate_selection/result/model/02_whole_doi_validation.json) from the expanded conditional analysis
- [Figure 1 panel order](06_manuscript/03_figure1_panel_order.md) and [component and conditional rankings](03_candidate_selection/result/table/04_figure1_candidate_ranks.csv)
- [Compound evidence inclusion](03_candidate_selection/result/table/05_compound_evidence_inclusion.csv) and [round comparison](03_candidate_selection/result/table/06_round_rank_comparison.csv) document the first-round fit (125 observations, 14 DOI reports, 51 compounds). The separate [released Carthamus comparison](03_candidate_selection/12_evidence_expansion/run_carthamus_2026-11-27/Release_Record.json) increased the connected model from 113 to 115 observations and kept the same Top 20 membership within that comparison. [Update figure](03_candidate_selection/result/figure/capacity_update_carthamus_2026-11-27.png).

- Figure 1 ordered independent parts A/B/C (no composite) | [A](06_manuscript/result/figure/figure1_A.flow_chart.png) | [B](06_manuscript/result/figure/figure1_B.evidence_screening_and_ranking.png) | [C](06_manuscript/result/figure/figure1_C.pathway_framework.png)
- figure1_A.flow_chart (detailed screening workflow) | [PNG](06_manuscript/result/figure/figure1_A.flow_chart.png) | [SVG](06_manuscript/result/figure/figure1_A.flow_chart.svg)
- figure1_B.evidence_screening_and_ranking | [PNG](06_manuscript/result/figure/figure1_B.evidence_screening_and_ranking.png) | [SVG](06_manuscript/result/figure/figure1_B.evidence_screening_and_ranking.svg)
- figure1_C.pathway_framework (provisional top-down pathway framework) | [PNG](06_manuscript/result/figure/figure1_C.pathway_framework.png) | [SVG](06_manuscript/result/figure/figure1_C.pathway_framework.svg)

## Supporting component previews (supplementary)

| Panel | PNG | Editable SVG |
|---|---|---|
| Figure 1-1. Candidate discovery | [PNG](06_manuscript/result/figure/supplementary/figure1-1_candidate_discovery.png) | [SVG](06_manuscript/result/figure/supplementary/figure1-1_candidate_discovery.svg) |
| Figure 1-2. Literature screening | [PNG](06_manuscript/result/figure/supplementary/figure1-2_literature_screening.png) | [SVG](06_manuscript/result/figure/supplementary/figure1-2_literature_screening.svg) |
| Figure 2-1. Model validation | [PNG](06_manuscript/result/figure/supplementary/figure2-1_model_validation.png) | [SVG](06_manuscript/result/figure/supplementary/figure2-1_model_validation.svg) |
| Figure 2-2. Rank stability | [PNG](06_manuscript/result/figure/supplementary/figure2-2_candidate_rank_stability.png) | [SVG](06_manuscript/result/figure/supplementary/figure2-2_candidate_rank_stability.svg) |
| Pathway UpSet (top-down, solid) | [PNG](06_manuscript/result/figure/supplementary/figure1_C_pathway_upset.png) | [SVG](06_manuscript/result/figure/supplementary/figure1_C_pathway_upset.svg) |

figure1_A/B/C are independent part-figures delivered in assembly order (A→B→C; no composite). The [panel order](06_manuscript/03_figure1_panel_order.md) describes the scheme. Legacy component previews and the prior composite are preserved in [supplementary](06_manuscript/result/figure/supplementary/); the [component R script](06_manuscript/code/02_render_manuscript_panels.R) now exports there.

## Evidence status

- [In vivo mechanism evidence for the 12 retained candidates](02_identity_and_evidence/result/table/04_candidate_in_vivo_mechanism_evidence.md) and [DOI-linked evidence table](02_identity_and_evidence/result/table/04_candidate_in_vivo_mechanism_evidence.csv).

The [targeted evidence update](03_candidate_selection/12_evidence_expansion/README.md) records the scope checkpoint of 100 of 567 priority reports with a logged source-review scope. The [working Results](06_manuscript/result/02_results_working.md) also describes subsequent targeted full-text work and the approved Carthamus release. The [conditional four-phenolic-acid trial](03_candidate_selection/12_evidence_expansion/Trial_Phenolic_Acid_Rank_Comparison.csv) tests one additional report using its table's stated unit. Figure 1A/B use the first-round model.

- The [2026-11-26 full-text tranche](02_identity_and_evidence/inputs/provenance/ORAC_Tranche1_Observations_2026-11-26.csv) logged 12 further scope records; its seven pure-compound rows remain held and no model input was released. The [P0 mechanism adjudication worksheet](02_identity_and_evidence/result/table/audit/P0_Mechanism_Adjudication_Worksheet_2026-11-26.md) prepares the quercetin, chlorogenic-acid and hesperetin review verdicts.

- [Candidate coverage](02_identity_and_evidence/result/table/01_candidate_report_coverage.csv)
- [Quantitative DOI crosswalk](02_identity_and_evidence/result/table/03_quantitative_report_crosswalk.csv)
- [Full-text batches](02_identity_and_evidence/result/table/audit/Fulltext_Batch_Summary.json)
- [Experimental validation plan](04_05_experimental_validation/README.md)

See the [research workflow](README.md) for inputs, handoffs and reproduction.
