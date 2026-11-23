# Frozen evidence reference from Results 1 v1.0

This directory preserves the fixed process inputs used by the current literature workflow. The original release is recoverable from commit `5ee3bc8a6325225533e36403c1d360cd3b84e3d3`, including its original manuscript, Table 1, figures, supplements and replay instructions. See the [release tree](https://github.com/Jane-huangjingyi/Antioxidants-project/tree/5ee3bc8a6325225533e36403c1d360cd3b84e3d3/06_manuscript/Results1_v1.0).

| Input | Role |
|---|---|
| [Original observations](original_observations.csv) | 304 primary-source observations with original units, DOI and locators. |
| [Assay-specific reference ranks](assay_specific_reference_ranks.csv) | 225 historical ranks within report, assay and protocol. These are the reference used by the DOI crosswalk. |
| [Evidence snapshot](evidence_snapshot.json) | Fixed observations, ranks and prior panel attributes for evidence-change diagnostics. |
| [Data dictionary](evidence_data_dictionary.csv) | Original field definitions and interpretation rules. |

The scientific source manifest stores the byte hashes and original release paths. For new observations, use the [intake template](../../templates/evidence_update_intake.csv) and the [update procedure](../../../../03_candidate_selection/README.md#reviewed-evidence-updates). Keep corrections in separately reviewed evidence. Current counts and rankings are generated into the relevant `result/` directories.

## Reproduce the old release

Open the release commit in a separate checkout and follow its `06_manuscript/Results1_v1.0/Reproducibility_Guide.md`. Use the [current workflow](../../../../README.md) for the working manuscript and current rankings.
