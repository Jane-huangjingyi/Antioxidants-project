# Methods Draft v0.1 EN
DRAFT | 2026-10-16 | Baseline 24653d04f4b96849bdcc57039aecfb3cda99da4f
Status tags distinguish completed work observed results approved but unimplemented rules planned analysis and unverified details.

## 1 Study design and database scope

We assembled a literature-derived database that preserves distinct chemical constructs rather than combining incompatible assays into a universal potency score. The broader classification table contains 191 background records across nine analysis panels. The current aqueous analysis includes 157 candidate entries across seven panels. These are different analytical populations; the 191 entries have not been recounted here as identity-deduplicated compounds. [COMPLETED_METHOD]

Sources: [Source](D:/JANE/GitHub/antioxidants%20project/data/candidate_universe/Antioxidant_Class_Candidate_Master.csv); [Source](D:/JANE/GitHub/antioxidants%20project/data/candidate_universe/Aqueous_Antioxidant_Candidate_Master.csv); [Source](D:/JANE/GitHub/antioxidants%20project/docs/methods/Antioxidant_Functional_Factor_Taxonomy_CN.md)

## 2 Candidate identification and classification

Candidate identity was organized using project identifiers, preferred and source-preserved names, PubChem identifiers, InChIKeys and chemical-form attributes. The aqueous table compound labels map to the screening master canonical_name values. Integer-like CID text ending in .0 was normalized only for the read-only join check, which showed matching structure pairs. Two candidate identities remain unresolved in the current audit, and all 157 Chinese-name entries remain uncurated. The approved broad food-source gate is distinguished from assay suitability, exposure and safety evaluation. [COMPLETED_METHOD; UNVERIFIED identity details]

Sources: [Source](D:/JANE/GitHub/antioxidants%20project/data/candidate_universe/Antioxidant_Class_Candidate_Master.csv); [Source](D:/JANE/GitHub/antioxidants%20project/data/candidate_universe/Aqueous_Antioxidant_Candidate_Master.csv); [Source](D:/JANE/GitHub/antioxidants%20project/data/literature_screening/master/Literature_Screening_Candidate_Master.csv); [Source](D:/JANE/GitHub/antioxidants%20project/data/framework/Candidate_Identity_and_Synonym_Audit.csv); [Source](D:/JANE/GitHub/antioxidants%20project/docs/qc/Stage25A1_Human_Review_Resolution_CN.md)

## 3 Literature retrieval

The Stage25A metadata screen used recorded Europe PMC queries with a retrieval date of 20 September 2026. OpenAlex supplied the citation metadata under the documented identifier-matching audit. The candidate by publication provenance retains identifiers, screening decisions and citation retrieval information. The subsequent H-ORAC retrieval frame contained 47 candidates from the provisional Top50 after applicability review. Its initial search log is dated 21 September 2026. Later targeted source recovery is recorded separately. These dates do not establish complete full-text adjudication or SEARCH_COMPLETE under VSIR. [COMPLETED_METHOD]

Sources: [Source](D:/JANE/GitHub/antioxidants%20project/data/literature_screening/master/Literature_Screening_Candidate_Master.csv); [Source](D:/JANE/GitHub/antioxidants%20project/data/literature_screening/provenance/Literature_Screening_Publication_Provenance.csv); [Source](D:/JANE/GitHub/antioxidants%20project/data/literature_screening/qc/Literature_Screening_Literature_Search_Log.csv); [Source](D:/JANE/GitHub/antioxidants%20project/data/h_orac_stage25b/stage25b/Stage25B_HORAC_Search_Log.csv); [Source](D:/JANE/GitHub/antioxidants%20project/docs/qc/Stage25A_Citation_Source_Audit_CN.md)

## 4 Evidence eligibility

Existing quantitative records were classified under H-ORAC Evidence Rubric v2.0, which combines an assay-comparability core with objectively triggered compound-specific checks. The primary set uses A and B1; B2 is retained for sensitivity analysis and C or X records do not enter that primary aggregation. VSIR v1.0 is separately conditionally frozen in scientific design: verifiability, statistical validity, independence and reproducibility govern pure-compound H-ORAC-FL evidence eligibility. It requires at least two qualifying genuinely independent original studies. Automated GO or NO-GO additionally requires SEARCH_COMPLETE and EVIDENCE_CLOSED; unresolved critical evidence or major dispute requires HOLD and human review. VSIR implementation and its 12 boundary tests were not performed. [COMPLETED_METHOD for existing v2; APPROVED_NOT_IMPLEMENTED for VSIR]

Sources: [Source](D:/JANE/GitHub/antioxidants%20project/docs/methods/h_orac_framework/H_ORAC_Evidence_Rubric_v2.0_CN.md); [Source](D:/JANE/GitHub/antioxidants%20project/docs/methods/h_orac_framework/Stage25B_HORAC_Selection_and_Ranking_Method_Final_CN.md)

## 5 Data extraction

The experiment table retains one candidate by experiment record with assay identity, material form, raw value and unit, source location, solvent and control information, conversion details and review flags. Publication identifiers and experiment identifiers support navigation but do not independently prove study independence. Missing or uncertain source details remain explicit. The present production task read existing extraction records; it did not conduct a new full-text extraction campaign. [COMPLETED_METHOD]

Sources: [Source](D:/JANE/GitHub/antioxidants%20project/data/h_orac_stage25b/stage25b/Stage25B_HORAC_Experiment_Evidence.csv); [Source](D:/JANE/GitHub/antioxidants%20project/methods_qc/config/ORAC_Literature_Extraction_Data_Dictionary.csv)

## 6 Data standardization

H-ORAC values are expressed as mol Trolox equivalents per mol compound only when the original scale and tested chemical form permit a reconstructable conversion. For a result reported as micromol TE per gram, multiplication by the appropriate molar mass and division by one million gives mol TE per mol. Original values, units and conversion formulas remain separate fields. Fixed-concentration AUC, hydroxyl radical HORAC and other assay constructs are not converted without a valid calibration and scientific bridge. Unknown error types are not relabeled as SD or SE. [COMPLETED_METHOD]

Sources: [Source](D:/JANE/GitHub/antioxidants%20project/data/h_orac_stage25b/stage25b/Stage25B_HORAC_Experiment_Evidence.csv); [Source](D:/JANE/GitHub/antioxidants%20project/docs/methods/h_orac_framework/H_ORAC_Evidence_Rubric_v2.0_CN.md); [Source](D:/JANE/GitHub/antioxidants%20project/data/h_orac_stage25b/stage25b6d/Stage25B6D_Error_and_Replicate_Audit.csv)

## 7 Statistical analysis

The existing primary ranking summarizes eligible A plus B1 records by their median, with source-reported counts, ranges and dispersion retained as descriptive information. We independently recalculated the 28 medians without altering the tables. Numeric error coverage and verified error types were counted at the record level. Technical replication and independent study counts were kept separate. Candidate-level confidence intervals, rank probabilities and meta-analytic effect estimates were not computed because the required error definitions and experimental units are incomplete. Any future model requires a separate prespecified analysis. [COMPLETED_METHOD; PLANNED for future models]

Sources: [Source](D:/JANE/GitHub/antioxidants%20project/data/h_orac_stage25b/stage25b/Stage25B_HORAC_Quantitative_Ranking.csv); [Source](D:/JANE/GitHub/antioxidants%20project/data/h_orac_stage25b/stage25b/Stage25B_HORAC_Experiment_Evidence.csv); [Source](D:/JANE/GitHub/antioxidants%20project/data/h_orac_stage25b/stage25b6d/Stage25B6D_Error_and_Replicate_Audit.csv)

## 8 Study independence

Source-level and candidate-level audits distinguish original experimental contributions from review citation, reused datasets and within-study replicates. The current 6D audit records partial original-source verification and candidate eligibility under its historical gate. Two different DOIs or multiple measurement wells do not establish independence, and 6D PASS_VERIFIED must not be translated into VSIR GO. This task did not implement the new formal independence gate or assign new candidate eligibility. [COMPLETED_METHOD for partial audit; APPROVED_NOT_IMPLEMENTED for VSIR]

Sources: [Source](D:/JANE/GitHub/antioxidants%20project/data/h_orac_stage25b/stage25b6d/Stage25B6D_Source_Closure.csv); [Source](D:/JANE/GitHub/antioxidants%20project/data/h_orac_stage25b/stage25b6d/Stage25B6D_Candidate_Eligibility.csv); [Source](D:/JANE/GitHub/antioxidants%20project/data/h_orac_stage25b/stage25b6d/Stage25B6D_Study_Independence_Adjudication.csv)

## 9 Evidence verification

Verification is recorded separately for schema, file integrity, arithmetic, original-source interpretation and independent review. The source closure table reports the earlier full-text audit outcomes; those papers were not all re-adjudicated for this deliverable. The original CR records are preserved. The researcher confirms CR-001 through CR-016 were decided in conversation, but the complete individual decisions are not available in this production input. A decision-gap register therefore records the missing locators rather than inferring outcomes from old proposals. [COMPLETED_METHOD; UNVERIFIED decision detail]

Sources: [Source](D:/JANE/GitHub/antioxidants%20project/data/h_orac_stage25b/stage25b6d/Stage25B6D_Source_Closure.csv); [Source](D:/JANE/GitHub/antioxidants%20project/data/h_orac_stage25b/stage25b6d/Stage25B6D_Proposed_Change_Requests.csv); [Source](D:/JANE/GitHub/antioxidants%20project/docs/methods/h_orac_framework/Two_Reviewer_QC_Rules_CN.md)

## 10 Ranking and synthesis

Stage25B.5 Frozen Top20 v1.0 remains the formal historical chemical-capacity product. Its A plus B1 ordering is interpreted within the adjudicated evidence and accompanied by B2 sensitivity. The D1 to D5 framework separates activity, reliability, maturity, biological relevance and application feasibility across food ingredient development, nutrition and health intervention, and mechanistic research. No composite score, comprehensive Top20 or cross-scenario final ranking was generated. VSIR GO, if later validated, would establish evidence eligibility rather than automatically establish cross-study quantitative comparability. [COMPLETED_METHOD for existing ranking; PLANNED for future synthesis]

Sources: [Source](D:/JANE/GitHub/antioxidants%20project/data/h_orac_stage25b/frozen/Stage25B_Frozen_Primary_HORAC_Top20.csv); [Source](D:/JANE/GitHub/antioxidants%20project/data/framework/Comprehensive_Antioxidant_Indicator_Dictionary_v0.1.csv); [Source](D:/JANE/GitHub/antioxidants%20project/data/framework/Application_Scenario_Applicability_Matrix.csv)

## 11 Reproducibility

The production baseline is commit 24653d04f4b96849bdcc57039aecfb3cda99da4f. Source paths and contents were checked against that commit, with local-byte and Git-blob hashes recorded separately where line endings differ. Existing tracked files were hashed before and after production. The frozen package was checked against its ten-entry manifest. Schema and arithmetic checks do not establish that every historical analysis can be rerun: archived scripts retain their original environment and path assumptions, and a locked end-to-end environment has not been verified. [COMPLETED_METHOD for the stated checks; UNVERIFIED for historical reruns]

Sources: [Source](D:/JANE/GitHub/antioxidants%20project/data/h_orac_stage25b/stage25b/Stage25B_HORAC_Experiment_Evidence.csv); [Source](D:/JANE/GitHub/antioxidants%20project/data/h_orac_stage25b/frozen/Stage25B5_Frozen_Asset_SHA256_Manifest.csv); [Source](D:/JANE/GitHub/antioxidants%20project/archive/HISTORY_NAVIGATION_CN.md)
