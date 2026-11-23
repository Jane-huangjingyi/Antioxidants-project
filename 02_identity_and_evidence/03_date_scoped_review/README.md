# Date-scoped original-capacity review

The primary literature window is 2020-01-01 through 2026-11-16. The 2016-2019 extension applies to undercovered candidates. Earlier original sources retain a historical analysis role. The current candidate-linked corpus contains 77,594 provisional article keys; multi-database coverage and scientific eligibility screening continue.

## Current evidence

Start with [source decisions](results/Current_Scientific_Source_Decisions.csv), [candidate coverage](results/Candidate_Date_Window_and_Reuse.csv), and the [fixed 109-source progress register](results/Original_ORAC_Source_Progress.csv). The work cohort contains 72 recorded targeted reading scopes and 37 access-pending sources. Reading scopes identify exactly which methods, results, tables or captions were inspected. Supplement, identity and independence tasks remain in [the missing-field queue](results/Prior_Review_Missing_Field_Queue.csv). Final article eligibility requires adjudication.

[The active queue](results/Original_Capacity_Fulltext_Queue.csv) contains sources awaiting their first recorded scientific scope. Its size contracts as decisions are recorded. The fixed-cohort progress register retains the denominator. [Database coverage gaps](results/Database_Coverage_Gaps.csv) identify outstanding institutional exports and search logs. The acquisition inventory preserves 76 previously attempted PMC sources, including 74 recovered XML files. The latest two retries both returned HTTP500.

## Original values requiring qualification

[Reference controls](results/Reference_Control_Original_Extraction.csv) contain four rows, including two separate ascorbic-acid reports. [Additional endpoints](results/Additional_Endpoint_Original_Extraction.csv) retain four IC50-type outcomes. [Sesame comparison](results/Sesame_Comparison_Original_Extraction.csv) preserves six original Table4 rows, including sesamin and ferulic acid, with the printed micromol-TE/mM denominator and study-independence questions. [Hop Table6](results/Hop_Original_Table_Transcription.csv) preserves twelve experimental ORAC cells transcribed from the browser-accessible original PDF text. Local publisher requests returned a client challenge, so its original local-file and hash fields remain blank.

[The public deposit audit](results/Public_ORAC_Deposit_Summary_Audit.csv) checks eight slope summaries from DOI10.57745/WWSOBP. Seven compound errors reproduce mean absolute deviation. The Trolox error reproduces the first three slopes' mean absolute deviation, while its mean uses four slopes. [The manifest](results/Public_ORAC_Deposit_Manifest.csv) records public file identifiers, URLs and SHA256. Curve-PDF visual inspection found duplicate3f panel labels and a4a label requiring reconciliation with the CSV codes. These records retain endpoint, material, normalization or error-definition holds.

Earlier retained outputs include [blueberry molar values](results/Blueberry_Original_Capacity_Extraction.csv), [printed-unit holds](results/Current_Standard_Unit_Holds.csv), [distinct endpoints](results/Distinct_Endpoint_Original_Extraction.csv) and [secondary-source tracing](results/Secondary_ORAC_Original_Source_Trace.csv). [Recovery requests](results/Original_Reference_Recovery_Requests.csv) retain specific original-source gaps. Capacity-model label release remains NO for this review stage.

## Reproduction

Use the existing local XML and bibliographic caches. Public deposit retrieval supports an explicit --fetch option. Run the extractors as needed, then update reuse and queue status.

```sh
python 02_identity_and_evidence/03_date_scoped_review/code/audit_public_orac_deposit.py --fetch
python 02_identity_and_evidence/03_date_scoped_review/code/extract_reference_controls.py
python 02_identity_and_evidence/03_date_scoped_review/code/extract_additional_endpoint_holds.py
python 02_identity_and_evidence/03_date_scoped_review/code/extract_sesame_comparison_hold.py
python 02_identity_and_evidence/03_date_scoped_review/code/preserve_hop_table_transcription.py
python 02_identity_and_evidence/03_date_scoped_review/code/reconcile_existing_work.py
python 02_identity_and_evidence/03_date_scoped_review/code/triage_existing_abstracts.py
python 02_identity_and_evidence/03_date_scoped_review/code/update_orac_queue_progress.py
python 06_manuscript/code/01_build_manuscript_outputs.py
python 07_quality_control/code/02_validate_workflow.py
```

The hop script reproduces the recorded manual transcription. Rechecking its source cells requires the linked original Table6. Local XML acquisition uses recover_current_fulltexts.py. Preserve the fixed work-cohort progress file when refreshing the active queue. Human review states remain NOT_REVIEWED and formal changes remain change_applied=NO.

## Locator refresh and study versions

[Verified locator updates](results/Source_Locator_Refresh.csv) add four PMC identifiers. Exact normalized titles identify candidates, then the DOI inside each downloaded original XML confirms the match. The master retrieval files retain their original content. The date-scoped register applies the verified locator overlay. Reproduce with `python 02_identity_and_evidence/03_date_scoped_review/code/refresh_source_locators.py --fetch`, then reconciliation and triage.

[Study version links](results/Study_Version_Link_Register.csv) record two publisher-declared preprint/publication families. The public notices link the Ampelopsis preprint to DOI10.3390/molecules30112354 and the soymilk preprint to DOI10.3390/foods12183401. Each family receives one canonical study key in the all-reference consideration register. Numeric equivalence between versions remains unassessed. Local preprint PDF requests returned403; publication notices and their journal links were checked in the browser. Reproduce the curated links with `python 02_identity_and_evidence/03_date_scoped_review/code/record_declared_study_versions.py`, followed by the Step03.7 integration script.

The four newly recovered originals include three matrix/fraction studies and one isolated-compound raw-AUC comparison. The latter includes vitexin at5microgram/mL. Molecular TE normalization and exact figure values remain pending. The existing sesame denominator and hop normalization questions retain their holds after the present access checks. New capacity-model labels released in this pass equal zero.

The public supplement for DOI10.1080/14786419.2025.2493187 was recovered from Figshare article29040279, file54460089. FigureS5 was visually inspected. Its axis prints micromolTE/mol compound, whereas Methods3.4 reports micromolTE/micromol. Exact means, SEM and molecular normalization retain a hold. The original supplement includes ascorbic acid and luteolin comparators.

The public supplement for DOI10.1080/14786419.2025.2493187 (Figshare article29040279,file54460089) was inspected through text and FigureS5 visual review. Methods3.4 reports micromolTE/micromol; the figure axis prints micromolTE/mol compound. This denominator conflict remains on hold. Exact means, SEM and ORAC-specific n require reconciliation. Methods specify37C and40minutes. No numerical figure values were digitized.

[Institutional retrieval priorities](results/Fulltext_Access_Request_Priority.csv) cover the active access queue and the main article needed to resolve the tiliroside supplementary-unit conflict. Reproduce with `python 02_identity_and_evidence/03_date_scoped_review/code/build_access_priority.py`. Priorities reflect original capacity/standard comparison needs. Scientific eligibility remains pending.
