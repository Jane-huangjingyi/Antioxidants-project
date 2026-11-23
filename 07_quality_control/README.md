# 07. Scientific and reproducibility checks

`python run_pipeline.py` checks the rebuilt workflow. `python 07_quality_control/code/02_validate_workflow.py` checks the existing scientific snapshot. Registered source hashes are defined in `02_identity_and_evidence/source_manifest.json`; optional local corpora are distinguished from required bundled sources.

Checks cover the 191 literal seed identities, 157-framework coverage, reference formulas, candidate/source joins, selection gates, cutoff ties, all ten frozen assets and editable SVG structure. Algorithm tests use synthetic in-memory traces. Read [QC status](workflow_qc.json) and [workflow checks](Workflow_QC.md) for the outputs. Reconcile failed checks at the owning step before release. The [root results page](../Latest_Results.md) links current products after verification.
