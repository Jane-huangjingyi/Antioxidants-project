# Results Draft v0.1 EN
DRAFT | 2026-10-16 | Baseline 24653d04f4b96849bdcc57039aecfb3cda99da4f
Status tags distinguish completed work observed results approved but unimplemented rules planned analysis and unverified details.

## 1 Database composition

The database contains 191 background records spanning nine analysis panels, while the active aqueous population comprises 157 candidate entries in seven panels. The aqueous population consists of 59 flavonoids, 29 phenolic acids or conjugates, 15 stilbenes or lignans, two vitamin or vitamin-like entries, 15 organosulfur compounds, 11 betalain or nitrogen-containing entries and 26 other phytochemicals. These counts describe database scope rather than efficacy. [OBSERVED_RESULT]

Sources: [Source](D:/JANE/GitHub/antioxidants%20project/data/candidate_universe/Antioxidant_Class_Candidate_Master.csv); [Source](D:/JANE/GitHub/antioxidants%20project/data/candidate_universe/Aqueous_Antioxidant_Candidate_Master.csv)

## 2 Literature coverage

The provenance table contains 45,643 candidate by publication rows, of which 41,967 were included in the primary metadata metric. A publication associated with more than one candidate can contribute more than one row; the total therefore does not represent unique publications or independent experimental studies. The subsequent H-ORAC screening table contains 3,115 rows, including 1,641 awaiting full-text adjudication. The provisional Top50 and the 47-candidate retrieval frame remain distinct products. [OBSERVED_RESULT]

Sources: [Source](D:/JANE/GitHub/antioxidants%20project/data/literature_screening/provenance/Literature_Screening_Publication_Provenance.csv); [Source](D:/JANE/GitHub/antioxidants%20project/data/h_orac_stage25b/stage25b/Stage25B_HORAC_Publication_Screening.csv); [Source](D:/JANE/GitHub/antioxidants%20project/data/literature_screening/shortlist/Literature_Screening_Provisional_Top50.csv); [Source](D:/JANE/GitHub/antioxidants%20project/data/literature_screening/shortlist/Stage25B_HORAC_Retrieval_Eligible_Candidates.csv)

## 3 Experimental evidence availability

The canonical H-ORAC table contains 74 experiment records: seven A, 61 B1, four B2 and two X. The primary A plus B1 set therefore contains 68 records and supports the existing quantitative ordering of 28 candidates. This ordering reflects the previously adjudicated rubric and should not be described as a set of 28 candidates satisfying VSIR v1.0. [OBSERVED_RESULT]

Sources: [Source](D:/JANE/GitHub/antioxidants%20project/data/h_orac_stage25b/stage25b/Stage25B_HORAC_Experiment_Evidence.csv); [Source](D:/JANE/GitHub/antioxidants%20project/data/h_orac_stage25b/stage25b/Stage25B_HORAC_Quantitative_Ranking.csv)

## 4 Source verification

The 6D source audit marks eight of 16 existing DOI sources as verified original experiments and retains eight as unresolved. Hayes 2011 supplies an original ellagic-acid result reported as 151.77 plus or minus 3.57 g Trolox per 100 g dry sample, with the source footnote identifying three determinations and SD. This closes a source and precision-description gap but does not create a second independent study for that candidate. The source-level findings are inherited audit results rather than new full-text adjudications in this production task. [OBSERVED_RESULT]

Sources: [Source](D:/JANE/GitHub/antioxidants%20project/data/h_orac_stage25b/stage25b6d/Stage25B6D_Source_Closure.csv); [Source](D:/JANE/GitHub/antioxidants%20project/data/h_orac_stage25b/stage25b6d/Stage25B6D_Error_and_Replicate_Audit.csv)

## 5 Statistical completeness

Numeric error values are available in 27 of the 68 A plus B1 records. Four records have an identified SD, while 23 retain an unresolved error type; 41 have no recovered numeric error. All 68 error-audit rows remain CI_NOT_ESTIMABLE. The canonical table also retains 70 of 74 rows as PENDING_SECOND_REVIEW. These completeness results prevent an interpretation of record medians as precision-weighted pooled effects or probabilities of Top20 membership. [OBSERVED_RESULT]

Sources: [Source](D:/JANE/GitHub/antioxidants%20project/data/h_orac_stage25b/stage25b6d/Stage25B6D_Error_and_Replicate_Audit.csv); [Source](D:/JANE/GitHub/antioxidants%20project/data/h_orac_stage25b/stage25b/Stage25B_HORAC_Experiment_Evidence.csv)

## 6 Independent study coverage

The 6D candidate audit contains nine PASS_VERIFIED, ten UNRESOLVED and nine FAIL_ON_AVAILABLE_EVIDENCE entries among 28 candidates. The last category expresses insufficiency of the available audited evidence, not proof that no further research exists. The nine PASS_VERIFIED entries belong to the earlier partial audit and are not VSIR GO results. Full implementation of the approved VSIR conditions and the 12 boundary tests remains outstanding. [OBSERVED_RESULT; APPROVED_NOT_IMPLEMENTED for VSIR]

Sources: [Source](D:/JANE/GitHub/antioxidants%20project/data/h_orac_stage25b/stage25b6d/Stage25B6D_Candidate_Eligibility.csv); [Source](D:/JANE/GitHub/antioxidants%20project/data/h_orac_stage25b/stage25b6d/Stage25B6D_Source_Closure.csv)

## 7 Frozen H ORAC ranking

The existing Frozen Top20 v1.0 is headed by rosmarinic acid and ends with ferulic acid. Independent recalculation reproduced all 28 canonical A plus B1 medians and the frozen Top20 order. Adding B2 for sensitivity produces three entries and three departures relative to the primary Top20. The frozen product remains an eligibility-defined description of in vitro chemical capacity within the adjudicated evidence, with no update to v1.1 in this task. [OBSERVED_RESULT]

Sources: [Source](D:/JANE/GitHub/antioxidants%20project/data/h_orac_stage25b/frozen/Stage25B_Frozen_Primary_HORAC_Top20.csv); [Source](D:/JANE/GitHub/antioxidants%20project/data/h_orac_stage25b/stage25b/Stage25B_HORAC_Quantitative_Ranking.csv); [Source](D:/JANE/GitHub/antioxidants%20project/data/h_orac_stage25b/frozen/Stage25B_Frozen_Top20_B2_Sensitivity_Qualification.csv)

## 8 Comprehensive framework readiness

The provisional framework contains five dimensions, 26 secondary indicators, three application scenarios and 785 candidate by dimension coverage rows. D1 has eight AVAILABLE_VERIFIED and 20 AVAILABLE_UNVERIFIED entries within the existing H-ORAC scope; 127 are NOT_SEARCHED and two IDENTITY_UNRESOLVED. D2 has 28 unverified entries and no fully verified dimension entries. D3 remains metadata-based, D4 lacks outcome adjudication and D5 has not undergone application-feasibility assessment. No composite score or comprehensive Top20 was calculated. [OBSERVED_RESULT; PLANNED for further synthesis]

Sources: [Source](D:/JANE/GitHub/antioxidants%20project/data/framework/Candidate_157_Data_Availability_Matrix.csv); [Source](D:/JANE/GitHub/antioxidants%20project/data/framework/Comprehensive_Antioxidant_Indicator_Dictionary_v0.1.csv); [Source](D:/JANE/GitHub/antioxidants%20project/data/framework/Application_Scenario_Applicability_Matrix.csv)

## 9 Current evidence gaps

The outstanding work comprises original-source closure, identification of error definitions and replicate units, independent second review, VSIR implementation and boundary testing, reconciliation of final CR decisions, and biological and application-specific evidence appraisal. Vitamin C still requires closure of the Ou 2001 original table. Platzer 2022 includes an original pure-standard AAPH-fluorescein AUC experiment, but a reconstructable Trolox-equivalent conversion is unavailable for primary pooling. Missing evidence is retained as missing rather than interpreted as inactivity. [OBSERVED_RESULT; UNVERIFIED where source closure is absent]

Sources: [Source](D:/JANE/GitHub/antioxidants%20project/data/h_orac_stage25b/stage25b6d/Stage25B6D_Source_Closure.csv); [Source](D:/JANE/GitHub/antioxidants%20project/data/h_orac_stage25b/stage25b6d/Stage25B6D_Proposed_Change_Requests.csv); [Source](D:/JANE/GitHub/antioxidants%20project/docs/qc/stage25b6d/Stage25B6D_VitaminC_Reconciliation_CN.md); [Source](D:/JANE/GitHub/antioxidants%20project/docs/qc/stage25b6d/Stage25B6D_Ranking_Readiness_CN.md)
