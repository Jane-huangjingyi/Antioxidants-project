# 06. Manuscript assembly

The [Part 1 manuscript (Word)](result/Manuscript_Part1_Nature_Communications.docx) combines the [editable manuscript sections](04_part1_manuscript_sections.md), [Methods](01_methods_working.md), [generated Results 1](result/02_results_working.md) and Figure 1 as ordered independent part-figures A/B/C (each PNG+SVG). See [Latest results](../Latest_Results.md) for the analysis data and diagnostics and the [historical release reference](../02_identity_and_evidence/inputs/provenance/results1_v1.0/README.md) for the prior snapshot.

Once the literature pipeline and rank tables are current, run these commands from the project root. The R script requires svglite, and Word assembly requires python-docx.

```shell
python 06_manuscript/code/03_build_working_results.py
Rscript 06_manuscript/code/06_render_screening_workflow.R   # figure1_A.flow_chart
Rscript 06_manuscript/code/04_render_figure1.R              # figure1_B.evidence_screening_and_ranking
Rscript 06_manuscript/code/07_render_figure1_C_pathway.R    # figure1_C.pathway_framework + supplementary UpSet
Rscript 06_manuscript/code/07_render_figure1_C_pathway.R   # figure1_C.pathway_framework
python 06_manuscript/code/05_build_part1_manuscript.py
```

Figure 1 is delivered as **independent part-figures in assembly order A→B→C** (no composite): [figure1_A.flow_chart](result/figure/figure1_A.flow_chart.png), [figure1_B.evidence_screening_and_ranking](result/figure/figure1_B.evidence_screening_and_ranking.png), [figure1_C.pathway_framework](result/figure/figure1_C.pathway_framework.png); the Word manuscript embeds them in this order. See the [panel order](03_figure1_panel_order.md). The [B figure script](code/04_render_figure1.R) exposes colors, labels, layout and export dimensions. Legacy component previews are regenerated with `Rscript 06_manuscript/code/02_render_manuscript_panels.R` into `result/figure/supplementary/`.

The [detailed screening workflow](result/figure/figure1_A.flow_chart.png) (figure1_A) combines example terms from the assay, compound-class and named-compound search routes with the current review counts and first-round model. See the [database search syntax](../02_identity_and_evidence/05_multidatabase_retrieval/Stage2_Manual_Export_Handoff.md) and [synonym search log](../02_identity_and_evidence/05_multidatabase_retrieval/PubMed_CID_Alias_Query_Status.csv) for query details. Run `Rscript 06_manuscript/code/06_render_screening_workflow.R` with jsonlite and svglite to reproduce the 300 dpi PNG and [editable SVG](result/figure/figure1_A.flow_chart.svg).
**Tables and verification.** The main tables link to their owning step or the frozen Results 1 release. Supplementary and audit files live below `result/table/`. Send the cited tables, figure panels and manuscript claims to [07 QC](../07_quality_control/README.md) with their source and generation commands.

## Supporting descriptive analysis

Read [Methods](Methods.md), [generated descriptive Results](Results.md), [Figure captions](Figure_Captions.md) and [the claim map](result/table/audit/Manuscript_Claim_Map.csv). Each claim identifies its input/code/output chain and its scientific status.

Run `python run_pipeline.py` to regenerate the supporting descriptive counts, Tables 1-3 and S1, Results and three figures. The optional review workbook is a filtered export from those source tables.

Methods and Results currently cover source-bounded discovery, identity references, evidence organization, selection sensitivity and assay preparation. Experimental dose-response, cellular benefit and causal mechanism Results require real data and scientific review. Do not turn planned procedures into past-tense claims that an experiment was performed.
