# Reproducibility guide

The v1.0 evidence snapshot was derived from commit c69f31ca2f4e9842cfe61766744b9d2b4379288f. The [release manifest](Results1_Manifest.json) gives source and artifact hashes. The snapshot includes original observation IDs, ranks, priority decisions, source locators and units. Underlying original records and prior decisions retain their existing locations. Python 3.12, R 4.5.3 with svglite, and the bundled Node.js spreadsheet runtime 26.1119.11507 were used. NumPy 2.5.4 was used for the model replay. The release calculations and figure use no random sampling. The inherited scaffold split is the preserved deterministic grouping.

Run from the repository root.

```sh
python 06_manuscript/Results1_v1.0/rebuild_release.py --out download_raw/Results1_replay
python 03_candidate_selection/08_capacity_review_validation/review_and_validate.py
python 07_quality_control/code/validate_workflow.py
```

Set RESULTS1_RSCRIPT and RESULTS1_NODE if the executables are outside PATH. Excel generation needs @oai/artifact-tool. With the desktop runtime, set CODEX_SPREADSHEET_MODULES to the runtime node_modules path. The R renderer reads Figure1_Data.csv and exposes the palette, font, size and typography. It exports native SVG text and vectors, and 300 dpi PNG. The model replay needs NumPy on the same Python interpreter's path. Compare original data CSVs and figure bytes in the same environment. Compare XLSX worksheet content across builds, as container metadata can vary. Published outputs remain available without the optional local full-text and institutional caches.
