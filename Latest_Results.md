# Latest results

## Manuscript Part 1

- [Part 1 manuscript (Word)](06_manuscript/result/Manuscript_Part1_Nature_Communications.docx)
- [Methods](06_manuscript/01_methods_working.md)
- [Results 1](06_manuscript/result/02_results_working.md)
- [Candidate rank sensitivity](03_candidate_selection/result/table/03_rank_sensitivity.csv) and [model validation](03_candidate_selection/result/model/02_whole_doi_validation.json) from the expanded conditional analysis
- [Figure 1 panel order](06_manuscript/03_figure1_panel_order.md) and [component and conditional rankings](03_candidate_selection/result/table/04_figure1_candidate_ranks.csv)
- [Compound evidence inclusion](03_candidate_selection/result/table/05_compound_evidence_inclusion.csv) and [first-round versus updated ranking](03_candidate_selection/result/table/06_round_rank_comparison.csv). The first-round fit is available. Updated rank fields await admissible new observations and a refit.

- Figure 1 | [PNG](06_manuscript/result/figure/figure1_evidence_screening_and_ranking.png) | [Editable SVG](06_manuscript/result/figure/figure1_evidence_screening_and_ranking.svg)
- Screening workflow (standalone view of Figure 1a) | [PNG](06_manuscript/result/figure/figure1a_screening_workflow.png) | [Editable SVG](06_manuscript/result/figure/figure1a_screening_workflow.svg)

## Supporting component previews

| Panel | PNG | Editable SVG |
|---|---|---|
| Figure 1-1. Candidate discovery | [PNG](06_manuscript/result/figure/figure1-1_candidate_discovery.png) | [SVG](06_manuscript/result/figure/figure1-1_candidate_discovery.svg) |
| Figure 1-2. Literature screening | [PNG](06_manuscript/result/figure/figure1-2_literature_screening.png) | [SVG](06_manuscript/result/figure/figure1-2_literature_screening.svg) |
| Figure 2-1. Model validation | [PNG](06_manuscript/result/figure/figure2-1_model_validation.png) | [SVG](06_manuscript/result/figure/figure2-1_model_validation.svg) |
| Figure 2-2. Rank stability | [PNG](06_manuscript/result/figure/figure2-2_candidate_rank_stability.png) | [SVG](06_manuscript/result/figure/figure2-2_candidate_rank_stability.svg) |

The [R script](06_manuscript/code/02_render_manuscript_panels.R) exposes colors, font, sizes and geometry. The draft exports above are component previews for the single Figure 1 specified in the panel order.

## Evidence status

The [targeted evidence update](03_candidate_selection/12_evidence_expansion/README.md) records 88 of 567 priority reports with a logged source-review scope and 479 pending. The [conditional four-phenolic-acid trial](03_candidate_selection/12_evidence_expansion/Trial_Phenolic_Acid_Rank_Comparison.csv) tests one additional report using its table's stated unit. The Part 1 manuscript and primary ranking preserve the first-round checkpoint.

- [Candidate coverage](02_identity_and_evidence/result/table/01_candidate_report_coverage.csv)
- [Quantitative DOI crosswalk](02_identity_and_evidence/result/table/03_quantitative_report_crosswalk.csv)
- [Full-text batches](02_identity_and_evidence/result/table/audit/Fulltext_Batch_Summary.json)
- [Experimental validation plan](04_05_experimental_validation/README.md)

See the [research workflow](README.md) for inputs, handoffs and reproduction.
