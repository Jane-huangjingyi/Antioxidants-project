# 07. Quality control

`python run_pipeline.py` runs the validation after rebuilding outputs. `python 07_quality_control/code/validate_workflow.py` checks the existing working snapshot without changing original scientific evidence. The migration manifest resolves every preserved old path to its new source-baseline path and stores SHA256. Tracked source files are required; unbundled optional local caches are reported separately on a fresh clone.

The checks cover reconstruction of the 191 literal seed names, preserved ID mapping, formula/reference presence, candidate/source joins, 157-framework boundaries, gate decisions, tie disclosure, no forced panel filling, frozen assets, governance observations, English active navigation, and vector-text exports. Numerical AUC checks use clearly synthetic in-memory data only and verify algorithmic rejection rules, not experimental performance.

Read `workflow_qc.json`, `branch_inventory.json`, `migration_manifest.json`, `file_role_inventory.csv`, `figure_export_registry.csv` and the concise `Workflow_QC.md` after a complete run. No source is deemed full-text verified simply because it appears in a catalogue. Existing unresolved source, journal, food-occurrence and identity questions remain open.
