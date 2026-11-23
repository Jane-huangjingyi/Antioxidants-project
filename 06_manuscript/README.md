# 06. Manuscript assembly

Open the generated [Working Results 1](result/02_results_working.md) and the [historical release reference](../02_identity_and_evidence/inputs/provenance/results1_v1.0/README.md). The [working Methods](01_methods_working.md) integrates the current screening and modeling workflow for the next draft. [Current research](../Latest_Results.md) links the current data and diagnostics.

**Working panels.** After the literature replay, run `Rscript 06_manuscript/code/02_render_manuscript_panels.R`. It uses the discovery register, evidence counts, whole-DOI validation and rank table. The [latest results page](../Latest_Results.md) links each numbered PNG/SVG pair. Colors, type, dimensions and rendering settings are editable in the R script. Use `result/figure/supplementary/` for supporting figures. The root literature pipeline rebuilds the working Results from the current qualifying evidence and analysis outputs.

**Tables and verification.** The main tables link to their owning step or the frozen Results 1 release. Supplementary and audit files live below `result/table/`. Send the cited tables, figure panels and manuscript claims to [07 QC](../07_quality_control/README.md) with their source and generation commands.

## Supporting descriptive analysis

Read [Methods](Methods.md), [generated descriptive Results](Results.md), [Figure captions](Figure_Captions.md) and [the claim map](result/table/audit/Manuscript_Claim_Map.csv). Each claim identifies its input/code/output chain and its scientific status.

Run `python run_pipeline.py` to regenerate the supporting descriptive counts, Tables 1-3 and S1, Results and three figures. The optional review workbook is a filtered export from those source tables.

Methods and Results currently cover source-bounded discovery, identity references, evidence organization, selection sensitivity and assay preparation. Experimental dose-response, cellular benefit and causal mechanism Results require real data and scientific review. Do not turn planned procedures into past-tense claims that an experiment was performed.
