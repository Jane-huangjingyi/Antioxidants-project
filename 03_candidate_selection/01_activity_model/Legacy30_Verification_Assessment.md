# Thirty-record verification and integrated evidence

Run `reconcile_legacy30.py` after the existing extraction builders. Offline reproduction uses committed structured baseline and follow-up tables; online refresh is explicit through `recover_overlap_sources.py --legacy30`. The original files and frozen results are not edited.

All 30 unmatched H-ORAC-FL legacy records receive an individual disposition in `results/Legacy30_Verification.csv`. Nineteen have original-table numeric checks: seven Sakurai Table 1 rows; three Koroleva Table 2 ORAC rows; three Skroza Table 2 dose-dependent rows; five Foods caffeoylquinic-acid Table 4 rows; and one Eriodictyol experimental log row. These yield 22 derived observations because each Skroza row has two reported concentrations. They are not 22 new independent studies. Numeric equality is checked where the legacy value is a single untransformed mean.

Eleven remain SOURCE_PENDING: Quercitrin and Isoquercitrin from 10.1021/jf010586o; Epicatechin gallate and Isorhamnetin from 10.1021/jp307746c; six compounds from 10.1016/j.foodchem.2008.08.013; and trans-Resveratrol from 10.1093/chromsci/bmad007. Publisher/DOI access returned 403 or inaccessible responses on 2026-11-06. Their legacy locators are retained as claims, not newly verified locations. The online-HPLC article must additionally be checked for endpoint compatibility. No secondary numerical substitution is made.

The source table explicitly supplies SD for Sakurai and mean +/- SD with n at least three for Foods Table 4. Exact independent n is not established, so neither series receives sampling variances. Koroleva plus/minus values are preserved without assuming their type. Skroza ratios remain dose-specific; a rounded zero error is not an exact zero sampling variance. Eriodictyol is retained as 2.013 on the log scale, correcting only the derived representation of the legacy value/unit conflict. Caffeoylquinic-acid positional names follow legacy identity mapping and original compound numbers; no new identity approval is inferred from names alone.

## Integrated view

`results/Integrated_Capacity_Evidence.csv` contains the 77-row baseline traceable subset plus 22 newly reconciled derived rows, for 99 observations. It is a source-linked mixed-scale inventory, not a training matrix or potency ranking. Baseline newer-source annotations remain in `Traceable_Capacity_Evidence.csv`; do not treat baseline error fields as the latest review conclusion. Other previously extracted source checks are used in the source graph, not silently appended as duplicate baseline rows.

`results/Integrated_Source_Connectivity.csv` uses source-rechecked links from the current nine model candidates, the newly verified legacy rows, prior dose diagnostics and the quercetin comparison. Its 23 compounds and eight papers form three source-overlap components. These three components are not the same partition as the original nine-row graph: the phenolic-acid and eugenol groups now have source links, while ellagic acid and the caffeoylquinic-acid paper remain separate. Connectivity alone does not establish common units, protocol equivalence, independence or a fitted source effect.

The strict model-candidate design remains nine rows, three papers and three components; `audit_model_design.py` was rerun and remains unidentifiable for unrestricted between-component compound-plus-paper comparisons. No model eligibility, scientific approval or human-review state has been upgraded. All new audit rows are NOT_REVIEWED and change_applied=NO. Formal capacity ranks remain unset.

## QC and next step

The builder asserts exactly 30 audit rows, 99 integrated rows and 22 unique added compound/DOI/dose keys. Value and log-scale checks run with the extraction builders. `results/legacy30_qc.json` records the counts. Next close the eight-paper protocol and error definitions, prioritizing the source links that connect phenolic acids to eugenol, and reconcile these follow-ups into the main evidence workbook at a stable integration milestone. Original sources, source HOLDs and frozen ranking hashes remain governed by the existing workflow; this stage does not rewrite them.
