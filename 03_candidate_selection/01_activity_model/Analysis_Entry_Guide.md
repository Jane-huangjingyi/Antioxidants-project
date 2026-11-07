# Read the evidence before interpreting a rank

Run `python 03_candidate_selection/01_activity_model/build_analysis_entry.py` from the project root. Open `results/Capacity_Analysis_Entry.csv` in Excel. This 99-row analysis entry preserves source identifiers, DOI links, original location, scale, errors, review state and comparison scope, with newer model-candidate annotations applied to the appropriate baseline rows. Original tables are not overwritten. The 193-candidate universe remains separate; this is the quantitative evidence subset.

The current split is 68 baseline rows pending source review, six rechecked rows requiring protocol review, and 25 rows admitted only to source-local descriptive subsets. Admission here is not human scientific approval or inverse-variance model eligibility. No global capacity score or rank is populated.

`results/Within_Source_Descriptive_Order.csv` orders 24 observations within six groups having at least two checked records. Groups are separated by DOI, scale and reported dose. This is an intentionally narrow view of newly checked legacy subsets and the three Foods slope-ratio records. It excludes the 2023 compounds from ordering because their vehicles differ, and leaves a single log-scale row without a rank. The checked subsets do not represent every compound in their source papers. Dense ranks preserve equal reported point estimates; error intervals and shared calibration are not used to declare significant differences.

In particular, Foods eugenol, vanillin and capsaicin may have different descriptive positions even though their source reports no significant ORAC difference. Such positions are not evidence of superiority. Missing or unreviewed observations are not assigned zero capacity.

## Reproduction and next integration milestone

The offline dependency order is: existing baseline builders; `build_traceable_evidence.py`; `audit_legacy_coverage.py`; source-specific extraction builders where local raw files are available; `reconcile_legacy30.py`; `build_analysis_entry.py`. Committed structured extractions support inspection without downloading articles. Online source refreshing remains explicit. The root tables-only pipeline now regenerates this analysis entry. The main workbook includes Capacity evidence, Source-local order, Legacy source review and Protocol constraints. CSV outputs remain authoritative; regenerate the optional workbook after changing inputs.

Next audit material/form and endpoint-group assignments, integrate the reviewed analysis entry and pending-source ledger into the workbook, and update manuscript Methods/Results to distinguish source-local ordering from cross-study prediction. Do not freeze a capacity Top20 until the endpoint and validation support it. The accompanying `results/analysis_entry_qc.json` checks row counts and states; original source HOLDs and frozen results remain unchanged.
