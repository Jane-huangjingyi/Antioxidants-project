# Scientific sources

Use the [source document index](results/source_document_index.csv) to locate every retained scientific input and process record. The [table index](results/source_file_index.csv) adds row counts and original field names for CSV sources. Both describe current source locations; repeated records and review versions are not independent studies.

| Research purpose | Source collection | Interpretation |
|---|---|---|
| Reconstruct initial names and exclusions | `01_candidate_discovery/inputs/curation_baseline` | Original literal curation; not an exhaustive database census |
| Chemical identities | `inputs/identity_reference` and dated PubChem responses | Molecular references; not purchased-lot certification |
| Chemical observations, 157-candidate framework and source closure | `inputs/reference_collection/data` | Preserve original units, source locations, tiers and missingness |
| AFF-0061 observations and scientific review | `inputs/mechanism_evidence` | Original review, HOLD and change-applied states retained |
| Frozen H-ORAC reference | `03_candidate_selection/inputs/frozen_reference` | Independent historical reference; not the new experimental panel |
| Retrieval corpus | `inputs/source_corpus/stage25a` | Locally held source snapshots, optional on a clone; not all retrieved text is verified full text |
| Governance and scientific development | `00_project/research_records` and mechanism governance subfolders | Decisions and source assessments; not active pipeline entry points |
| Method QC references | `04_absorbance_assay/inputs/method_reference` | Reference settings, not approval of experimental parameters |

The [source manifest](source_manifest.json) records SHA256 and whether each source is bundled. Offline calculations require only bundled sources. Locally held corpora remain excluded from publication. Original source files retain their original language, schemas and content. Current instructions and outputs are English. Relative paths inside an original source are interpreted in that source's recorded historical context; locate current material by filename and scientific role in the source indexes.

The dated [full evidence catalogue](inputs/catalogue_reference/Evidence_Catalog_2026-10-30.xlsx) remains a supporting source snapshot. The generated [current review workbook](../06_manuscript/tables/Candidate_Review_Workbook.xlsx) provides the current selection chain and source indexes. Journal metrics retain their reported year and verification status; they are not updated by moving files and do not enter selection.

## Source inconsistencies requiring interpretation

One original visual record remains in `00_project/research_records/source_discrepancies`: the candidate-eligibility figure shows different category counts from the maintained historical recipe. The old image displays 22 eligible candidates in the other-phytochemicals category, while the maintained reference rendering displays 24. This earlier visual snapshot is retained pending interpretation; neither replaces the current 193-profile scope and explicit review gates. It is not a current manuscript result or an approved change to evidence. Vitamin C source rows retain their values and study identities; current rendering labels them by evidence ID, with original-source closure assessed separately.
