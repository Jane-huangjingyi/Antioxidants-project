# Date-scoped review and reuse of completed work

The primary window is 2020-01-01 through 2026-11-16. The extension window adds 2016-2019 for undercovered compounds. These explicit calendar ranges implement the researcher's instructions. Earlier original-source data remain documented as historical evidence, with their scope retained.

This reconciliation reuses the master bibliographic register, original-extraction associations, abstract packages, located body paragraphs, dated core-record caches, 79 existing source-screen entries and the 194-row capacity audit. It executes no new searches and repeats no source reading. The screening register records the scope of previously completed work and the missing work for each article.

Start with [the article register](results/Date_Scoped_Article_Register.csv), [candidate windows and reuse](results/Candidate_Date_Window_and_Reuse.csv), and [database coverage gaps](results/Database_Coverage_Gaps.csv). Counts are provisional article identifier groups in the existing candidate-linked corpus. Complete multi-database searches, identifier-conflict review and relevance screening remain necessary before a final retrieval denominator or PRISMA inclusion count.

First-publication dates from cached core records take priority over issue years. Year-only dates require verification. Known dates after the cutoff are excluded from the current scope; unresolved dates remain explicit. Undercoverage is provisionally fewer than 20 located leads in the primary window. Scientific review may identify further compounds requiring extension. A scarcity exception remains unestablished.

Europe PMC/PubMed records, PubChem synonyms and previous source reviews are reused. Web of Science and CNKI exports and logged Google Scholar searches retain pending status. CNKI and the Chinese National Knowledge Infrastructure are one database. Source reuse does not establish complete full-text review for every linked compound.

```sh
python 02_identity_and_evidence/03_date_scoped_review/code/reconcile_existing_work.py
```

Next screen the in-scope original-capacity leads, fill missing fields in already reviewed sources, and trace shared-compound references. Retain study exclusions and actual reading scopes throughout extraction. Date-window model sensitivity follows qualified extraction, alongside the historical source analysis.

## Current screening sequence

Run `python 02_identity_and_evidence/03_date_scoped_review/code/triage_existing_abstracts.py` after reconciliation, then `python 02_identity_and_evidence/03_date_scoped_review/code/recover_current_fulltexts.py` for public acquisition. [Triage counts](results/triage_summary.json) distinguish scientific scope reuse, automated abstract triage and title-only triage. [Source decisions](results/Current_Scientific_Source_Decisions.csv) retain actual reading scope.

DOI10.1007/s11130-023-01121-2 main-body Table2, Figure2 and reference19 distinguish tea-matrix ORAC from HPLC composition and secondary catechin values. Reference19 points to original DOI10.1207/S15327914NC4502_13 (2003), retained as historical provenance outside the active windows. The methods supplement remains pending.

The current public recovery log covers 76 PMC-linked candidates, with 74 XMLs obtained and two access failures. Forty-five other queued reports require additional source recovery. [Blueberry extraction](results/Blueberry_Original_Capacity_Extraction.csv) retains five exact glycosides, raw SD and molar units. Four glycosides remain outside the current193 index. The resveratrol/polydatin source retains a unit-scale reconciliation decision. Scientific source decisions and public acquisition counts remain separate.

Run `python 02_identity_and_evidence/03_date_scoped_review/code/extract_blueberry_source.py` after recovery to reproduce the five source-row transcriptions. Scripts are stored in code and derived outputs in results.

After recording scientific decisions, rerun reconciliation and triage. Already recorded reading scopes leave the new-source queue and retain their missing-field tasks. Acquisition counts describe their recovery batch, while the active queue reflects subsequent decisions.

[Previously reviewed sources with missing-field tasks](results/Prior_Review_Missing_Field_Queue.csv) retain the recorded reading scope and schedule only unchecked methods, supplements, materials and independence fields. [The active new-source queue](results/Original_Capacity_Fulltext_Queue.csv) is updated after those reuse decisions.

The current source decision table now includes the2020 citrus single-compound study, a2024 four-standard unit hold, and a2023 six-anthocyanidin figure-recovery task. Reproduce the unit-hold table with `python 02_identity_and_evidence/03_date_scoped_review/code/extract_current_unit_holds.py`. These decisions feed back into review reuse. The expanded conditional model in Step03.8 includes four parent-mapped citrus rows.
