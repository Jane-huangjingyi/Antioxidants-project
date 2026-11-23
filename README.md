# Food-derived antioxidant candidate selection

We identify defined dietary compounds with high expected aqueous antioxidant capacity and reproducible original evidence. We use assay-specific measurements to prioritize candidates for prospective absorbance-based validation. [Latest results](Latest_Results.md) opens the current figures, tables and working manuscript.

| Step | Input | Output and handoff |
|---|---|---|
| [00 Research scope](00_project/README.md) | Research objective, scope and decisions | Search and eligibility protocol for discovery and evidence review. |
| [01 Compound discovery](01_candidate_discovery/README.md) | Source-linked names, food records and search leads | Candidate register, aliases and exclusions for identity review. |
| [02 Literature and evidence](02_identity_and_evidence/README.md) | Search protocol, candidate register, database exports and original reports | Deduplicated reports, compound links, evidence roles and eligibility records for extraction and modeling. |
| [03 Modeling and ranking](03_candidate_selection/README.md) | Original capacities, material forms, conditions, uncertainty and structures | Molar evidence table, study-level model diagnostics and conditional order for experimental planning. |
| [04–05 Experimental validation and analysis](04_05_experimental_validation/README.md) | Candidate priorities, plate reader specifications and future raw traces | Assay design and trace-analysis rules for manuscript reporting. |
| [06 Manuscript](06_manuscript/README.md) | Verified counts, tables and model outputs | Working Methods, generated Results and editable figure panels. The frozen release remains in Git history. |
| [07 Quality control](07_quality_control/README.md) | Source manifests, scripts and results | Scientific invariants, output validation and reproduction checks. |

## Reproduce

Use the [environment guide](00_project/Environment.md). Run `python run_pipeline.py --literature` with the local search exports to reproduce discovery, title and abstract screening, conditional models and the full-text work queue. Run `Rscript 06_manuscript/code/02_render_manuscript_panels.R` for working PNG/SVG pairs. Use the [frozen evidence reference](02_identity_and_evidence/inputs/provenance/results1_v1.0/README.md) to reproduce the original Results 1 release.

The active literature results remain conditional. Full-text eligibility and independent experiment checks are ongoing. The new aqueous absorbance assay is at the design stage.
