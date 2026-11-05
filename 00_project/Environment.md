# Environment and execution

On Windows, use Git long-path support when cloning: `git -c core.longpaths=true clone <repository-url>`. For an existing checkout, `git config core.longpaths true` enables it locally. The root `.gitattributes` retains original scientific source bytes and fixes active text exports to LF so source verification survives checkout on another platform.

Core numerical workflow: Python >=3.10, standard library only. R figures: R >=4.3 plus `ggplot2` and `svglite`. Supplementary historical graphics also use `dplyr`, `tidyr`, `readr`, `stringr`, `forcats`, `scales`, `ggrepel`, `igraph`, `ggraph` and `patchwork`. Install the public CRAN packages before running, for example:

```r
install.packages(c("ggplot2", "svglite"))
```

```sh
python run_pipeline.py --tables-only
python run_pipeline.py
python run_pipeline.py --legacy-figures
```

The pipeline locates `Rscript` on PATH or the standard Windows R installation. Existing packages are reused from the ignored `05_analysis/local_library` when available. Session/package versions are recorded in `07_quality_control/R_session_info.txt`. Dependencies are not scientific source data and are not committed.

Network refresh is explicit and separate from offline reproduction:

```sh
python 02_identity_and_evidence/code/refresh_pubchem.py
python 04_absorbance_assay/code/search_methods.py
python run_pipeline.py
```

Refreshes can change snapshots and must be reviewed before commit. A name query returning multiple records is marked ambiguous. Method-search hits, including reviews, are discovery records and do not automatically become adopted primary sources. Search logs state query, date, response hash and pagination coverage.

The optional English review workbook is a convenience export. `00_project/exporters/build_review_workbook.mjs` uses Node and `@oai/artifact-tool` when available; it is not a dependency of the manuscript's scientific calculations. All underlying tables remain plain CSV and can be opened directly in Excel. Readers without the exporter can fully reproduce the research tables and R graphics.

Manual Illustrator edits belong in a `manual_edits` folder beside the generated task/version outputs, with an `_edited_YYYYMMDD` suffix and a source-figure reference. Generators never write to that folder.
