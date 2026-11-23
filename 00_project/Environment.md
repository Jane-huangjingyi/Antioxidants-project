# Environment and execution

On Windows, use Git long-path support when cloning: `git -c core.longpaths=true clone <repository-url>`. For an existing checkout, `git config core.longpaths true` enables it locally. The root `.gitattributes` retains original scientific source bytes and fixes active text exports to LF so source verification survives checkout on another platform.

Core numerical workflow: Python 3.12 with the [pinned scientific dependencies](../03_candidate_selection/01_activity_model/requirements_structure.txt) for ORAC-FL and structure models. R figures use R >=4.3 with `ggplot2`, `svglite` and `jsonlite`. Supplementary historical graphics also use `dplyr`, `tidyr`, `readr`, `stringr`, `forcats`, `scales`, `ggrepel`, `igraph`, `ggraph` and `patchwork`. Install the dependencies in an ignored local environment:

```powershell
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r 03_candidate_selection/01_activity_model/requirements_structure.txt
.venv/Scripts/python.exe run_pipeline.py --literature
```

```r
install.packages(c("ggplot2", "svglite", "jsonlite"))
```

```sh
python run_pipeline.py --literature
python run_pipeline.py --tables-only
python run_pipeline.py
python run_pipeline.py --legacy-figures
```

The literature workflow requires NumPy and the local database exports and raw PubMed XML listed in the [screening guide](../02_identity_and_evidence/06_machine_screening/README.md). It also uses any matching cached open full text to route work batches. The frozen manuscript has a [historical release replay](../02_identity_and_evidence/inputs/provenance/results1_v1.0/README.md#reproduce-the-old-release).

The pipeline locates `Rscript` on PATH or the standard Windows R installation. The working renderer also recognizes the ignored `04_05_experimental_validation/local_library` when available. For the frozen release replay, make that library available through `R_LIBS_USER` if packages are installed there. Session/package versions are recorded in `07_quality_control/R_session_info.txt`. Package installations stay local.

Network refresh is explicit and separate from offline reproduction:

```sh
python 02_identity_and_evidence/code/refresh_pubchem.py
python 04_05_experimental_validation/code/search_methods.py
python run_pipeline.py
```

Refreshes can change snapshots and must be reviewed before commit. A name query returning multiple records is marked ambiguous. Method-search hits, including reviews, are discovery records and do not automatically become adopted primary sources. Search logs state query, date, response hash and pagination coverage.

The optional English review workbook is a convenience export. `00_project/exporters/build_review_workbook.mjs` uses Node and `@oai/artifact-tool` when available; it is not a dependency of the manuscript's scientific calculations. All underlying tables remain plain CSV and can be opened directly in Excel. Readers without the exporter can fully reproduce the research tables and R graphics.

Manual Illustrator edits belong in a `manual_edits` folder beside the generated task/version outputs, with an `_edited_YYYYMMDD` suffix and a source-figure reference. Generators never write to that folder.
