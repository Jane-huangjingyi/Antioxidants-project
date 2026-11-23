# Machine-assisted literature screening and numeric priority readiness

Start with the [Methods draft](../../06_manuscript/01_methods_working.md) and [screening counts](../result/table/audit/Screening_QC.json). The current corpus comprises the PubMed export, the Europe PMC route snapshot and the available WoS batch. The screen performs title/abstract triage and routes pending evidence. Full-text eligibility, independent experiment adjudication and final systematic inclusion remain open.

| Output | Use |
|---|---|
| [Candidate report coverage](../result/table/01_candidate_report_coverage.csv) | One row per profile, with previous report links, deduplicated current links, literal name leads, ORAC priority leads and pending inclusion counts |
| [Candidate role leads](../result/table/02_candidate_evidence_role_leads.csv) | Per-candidate counts by possible evidence role, allowing multiple roles |
| [Quantitative report crosswalk](../result/table/03_quantitative_report_crosswalk.csv) | Existing report DOIs, assay groups and rows used for descriptive ranks or the connected model |
| [Original observation locators](../inputs/provenance/results1_v1.0/original_observations.csv) | Assay rows with original units, methods and source locator |
| [New source and extraction decisions](../../03_candidate_selection/10_orac_evidence_increment/README.md) | Source-specific review, harmonization, uncertainty and expanded conditional fit |
| [Anchor recall](../result/table/audit/Anchor_Recall_Pilot.csv) | Control retrieval and routing |
| [Numeric priority readiness](../../03_candidate_selection/result/table/audit/Objective_Priority_Readiness.csv) | Sensitivity gate, report counts and dispersion evidence by modeled compound |

The [full-text batch summary](../result/table/audit/Fulltext_Batch_Summary.json) gives access and scoped-review status for the 567 priority records. The [scoped reviews](../inputs/provenance/Fulltext_Scope_Review.csv) record the exact JATS body sections and tables examined. They distinguish novel pure-compound measures, secondary ORAC values, different endpoints and matrix studies. The generated local `ORAC_Fulltext_Batches.csv` assigns unresolved records to work batches of up to 25 by access route and reports cached PMCID/DOI checks and table leads. Use the publisher or the [Europe PMC open-access API](https://dev.europepmc.org/RestfulWebService) for missing eligible XML.

From the repo root run `python run_pipeline.py --literature` for discovery, identity, screening, original-source model diagnostics and batch routing. To replay only the title/abstract screen and its QC, run:

```powershell
python 02_identity_and_evidence/code/02_screen_public_snapshot.py
python 02_identity_and_evidence/code/03_summarize_screening.py
```

Prerequisites are the cached Stage 2 Europe PMC export, the 164 raw PubMed XML batches and their SHA-256 manifest, and the WoS institutional normalized and reconciled records. See the [Stage 2 intake procedures](../05_multidatabase_retrieval/README.md). The screen reads the source text without writing back to the retrieval files. The complete report-level list, many-to-many link list and stratified recall sample are written under the Git-ignored directory `download_raw/stage2_machine_screening/` as `Report_Screening.csv`, `Candidate_Report_Links.csv`, and `Recall_Audit_Sample.csv`. Filter by report key, DOI, candidate ID or evidence role. Role labels and record associations are machine leads. The numeric role can be triggered by an unrelated numerical expression in a matching abstract. Study independence and source/form identity require verification. No record was automatically excluded. Sampling is deterministic and the sample remains unreviewed.
