# Food-Derived Antioxidant Candidate Selection

**Start here.** The project builds a traceable food-chemical discovery collection, identifies a 20-slot review panel, and prepares an aqueous absorbance assay. It does not claim that a review slot is a potency rank or a laboratory-approved material.

## Research sequence

| Step | Scientific task | Authoritative entry |
|---|---|---|
| 00 | Define the question, food scope and decision rules | [Project protocol](00_project/Protocol.md) |
| 01 | Discover names independently of antioxidant rank; retain exclusions | [Candidate discovery](01_candidate_discovery/README.md) |
| 02 | Resolve formulas/identifiers and join source-linked evidence | [Identity and evidence](02_identity_and_evidence/README.md) |
| 03 | Apply transparent gates, disclose ties and prepare 20 review slots | [Candidate selection](03_candidate_selection/README.md) |
| 04 | Compare non-fluorescent methods and prepare validation | [Absorbance assay](04_absorbance_assay/README.md) |
| 05 | Generate editable figures and analyze future experimental data | [Analysis](05_analysis/README.md) |
| 06 | Assemble actual Methods, descriptive Results, Figures and Tables | [Manuscript](06_manuscript/README.md) |
| 07 | Check source preservation, links, selection logic and exports | [Quality control](07_quality_control/README.md) |

Run from this directory with Python 3.10 or newer:

```sh
python run_pipeline.py --tables-only
python run_pipeline.py
```

The first command needs only the Python standard library and builds all numerical tables. The second also renders three manuscript figures using R, `ggplot2` and `svglite`. [Environment instructions](00_project/Environment.md) cover optional supplementary graphics and Excel export. Default runs use committed source snapshots and do not query the network.

The working snapshot contains 204 discovery records, 193 identity/evidence profiles, 25 review-eligible candidates and 20 provisional review slots. Nine candidates pass the two-confirmed-study sensitivity. No candidate is currently laboratory-ready. See [generated Results](06_manuscript/Results.md), [Table 2](06_manuscript/tables/Table_2_Provisional_Review_Panel.csv) and the [cutoff tie set](03_candidate_selection/results/cutoff_tied_candidates.csv).

The historic 191-name collection is reconstructed from its original literal curation code, not relabelled as an exhaustive database search. Candidate-specific food occurrence remains a visible gap for many names. Glutathione is reopened for food-scope review and ergothioneine is added as a documented coverage gap; neither is silently inserted into the frozen ranking.

For manual review, open the [current English workbook](06_manuscript/tables/Candidate_Review_Workbook.xlsx). The [identity and evidence guide](02_identity_and_evidence/README.md) links the larger preserved evidence catalogue and all source tables. Record actual screening decisions in `03_candidate_selection/config/researcher_decisions.csv`; the workbook is an export of those inputs.

All active explanations, code and manuscript outputs are in English. Original-language source records and prior approvals remain immutable in [the preserved source baseline](90_archive/README.md). [Git workflow](00_project/Git_Workflow.md) identifies the current branch and explains why older branches need no repeated merging. File organization does not grant scientific approval.
