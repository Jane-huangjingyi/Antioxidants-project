# Systematic supplemental search across current candidates

This module begins harmonized supplemental retrieval for all 193 current candidates using public Europe PMC. Each candidate has broad antioxidant/redox, quantitative assay and dietary-occurrence search routes. Initial aliases are the canonical and reference names. CAS, stereochemical and additional synonym expansion remain pending. Searches are date-stamped at execution and retain exact queries, hit counts and raw metadata. This first source does not establish comprehensive multi-database coverage.

Run `python 02_identity_and_evidence/01_systematic_supplement/retrieve.py`. Successful query files are reused on resume. Failed searches are retried with the actual error retained. Capacity-route results are paginated through all returned hits. Broad and food routes capture hit counts and the first 100 records for initial screening. Their complete-result flags describe actual retrieval. Atomic per-query saves protect interrupted work. API requests are rate limited and retries are bounded.

Search_Coverage_Audit.csv records all candidate/route results and historical association counts. Raw records are search hits requiring deduplication and eligibility assessment. Source reading, extraction and quality approval follow recorded screening decisions. DOI/PMID matching and title review will consolidate repeated results and link papers to all matched candidates. Journal/ISSN and dated IF enrichment follow metadata recovery, with original article-method assessment retained separately.

Subsequent work expands identity aliases, searches additional available databases and citation networks, screens abstracts and full texts, extracts independent experimental observations, and evaluates protocol/material compatibility. The current search routes cover related assays broadly. Each assay and biological evidence type requires its own extraction scope before model inclusion. Review states and source HOLDs retain their recorded governance requirements.

## Metadata mode and initial article registers

Retrieval was switched to lightweight metadata for throughput after initial core responses. Successful earlier core responses remain available. New lightweight responses require abstract/full-text enrichment at screening. Run `build_screening_register.py` after retrieval to build Retrieved_Article_Register.csv and Candidate_Search_Hit_Links.csv. Keys prefer DOI, then PMID, then Europe PMC source/ID; cross-identifier and title near-duplicate review remains pending. Query hits represent candidate search associations. Each paper retains its originating response and record index. Journal metadata is recovered where available. IF fields remain blank pending verified dated enrichment.

## Expanded retrieval and known-source checks

Run `retrieve.py --expanded-capacity` after PubChem synonym recovery. The expanded pass applies a common top-12 short-synonym rule, plus canonical/reference names. Ambiguous unit/element symbols are filtered. Synonyms remain identity-review inputs. Query changes retain previous response snapshots under inputs/previous_queries, which are excluded from active screening registers. Run `recover_anchor_sources.py` to query known DOI references and retrieve a class/method search. Its unassigned class-route hits require candidate mapping through source screening. Run `audit_known_sources.py` after rebuilding screening registers. Known DOI anchors are reported separately from name-query recall. The all-candidate search is an initial public-database retrieval stage. Full-text screening, experimental extraction, quality assessment and institution-database reconciliation remain subsequent work.

## Current retrieval delivery

The canonical search pass has 579 successful queries across 193 candidates. The synonym-expanded capacity pass has 193 successful complete-result retrievals. Expanded capacity responses contain 42,958 candidate-hit records, including cross-candidate overlap. The class/method query contributes 16,750 metadata records requiring candidate assignment. Eighteen known DOI queries preserve reference-anchor recovery. Active screening registers exclude superseded query snapshots.

The public register has 49,906 provisional identifier groups. Linking historical and supplemental DOI/PMID records gives 87,386 provisional master groups and 106,123 candidate-article links. Journal metadata are available for 48,990 master groups. Bibliographic conflicts, title near-duplicates and related reports require review before a final PRISMA count. Known-source recall covers 18 of 95 existing candidate-DOI pairs through candidate-name routes, 71 through the broad class/method route at article level, and 93 through DOI anchors. Direct anchor recovery does not count as successful candidate-name search recall.

Start with Search_Coverage_Audit.csv and Expanded_Capacity_Coverage_Audit.csv, then Master_Article_Register.csv and Master_Candidate_Article_Links.csv. The raw query responses, PubChem snapshot and article-origin record indices preserve provenance. Screening, full-text verification, experimental extraction and article-method quality evaluation remain pending for newly retrieved records. Existing models still use their prior extracted data.

### Reproduction sequence

For fresh retrieval run fetch_synonyms.py, retrieve.py, retrieve.py --expanded-capacity, then recover_anchor_sources.py. Inspect failure states and synonym ambiguity. To regenerate the delivered tables from saved responses without network requests, run `python 02_identity_and_evidence/01_systematic_supplement/rebuild_registers.py`. Institution export requirements are in Institutional_Export_Instructions.md.

## Remaining coverage issues

The master links currently cover 191 candidate IDs. Probetanin (AFF-0150) and Vulgaxanthin II (AFF-0154) have no candidate-linked records from the current queries and historical source table; identity, spelling, synonyms and citation routes require follow-up. A zero-hit result does not establish absence of research. The unrecovered known anchor pairs belong to DOI 10.1007/s12039-019-1618-5 for AFF-0014 and AFF-0034. These remain source-recovery tasks. Full-text scientific screening, article-level quality assessment, independent-experiment extraction and subsequent model updates remain pending for the new corpus.

## First full-text recovery batch

Run `retrieve_method_fulltexts.py` after rebuilding the master register. It prioritizes article titles explicitly naming ORAC, oxygen radical absorbance, crocin bleaching or pyrogallol red and attempts public Europe PMC XML recovery when a PMCID is available. Method_Fulltext_Queue.csv records every selected article, actual recovery status, source URL and hashes. This title-priority rule schedules the first batch. The remaining corpus still needs abstract/full-text relevance screening, including multi-compound papers whose methods are absent from the title. Recovered XML remains pending scientific reading and experimental extraction.

Run `inventory_fulltexts.py` after XML recovery to generate Fulltext_Extraction_Readiness.csv and Fulltext_Table_Locators.csv. Literal body-name hits are extraction leads requiring exact-form and experiment verification. The first original-source method/provenance finding is recorded in Fulltext_Scientific_Notes.md.

## Git storage and restoration

Large generated bibliographic CSVs are stored as deterministic gzip snapshots with original SHA256 values in Snapshot_Manifest.json. After cloning, run `python 02_identity_and_evidence/01_systematic_supplement/restore_snapshots.py` to restore them. Raw query responses, the PubChem response snapshot and public full-text XML remain local caches and can be reacquired using the retrieval scripts. Coverage audits and the full-text queue retain source URLs and hashes. Fulltext_License_Inventory.csv records XML license metadata. Offline rebuilding from raw responses requires reacquiring those local caches first. Restored bibliographic snapshots can be inspected directly without rerunning retrieval.

## Original-source screening and capacity follow-up

Run `retrieve_compound_fulltexts.py` to extend the explicit-method-title route with a documented compound-comparison/SAR title expression. This retrieves all matching PMCID-linked records from the current master register, sorted by DOI and PMCID. It schedules reading without applying an IF cutoff. Compound_Comparison_Fulltext_Queue.csv records 50 selected reports, 49 recovered XMLs and one public XML failure. Together with the earlier route, 79 unique XMLs and 215 tables are inventoried. Search-hit and original-experiment counts remain separate.

Source_Scientific_Screening.csv is the current endpoint-specific screen. Thirty-five papers have targeted body/method/table text checks and 44 have abstract/method-heading screens. Each entry states its reading scope, source hash, locator and unresolved work. Screening does not establish complete visual-figure, supplement or independent dual-review coverage. Seven reviews and two secondary datasets remain useful for original-reference discovery. Other assay outcomes remain available for their own endpoints.

Run `screen_recovered_sources.py` to rebuild the assessment register and validate its source locators and hashes. The scientific assessments are explicit code inputs. Run `extract_capacity_followup.py` to reproduce 26 numeric source rows from six DOIs, with provisional parent-name mapping to nine current candidates. Original_Capacity_Followup.csv retains raw mean/error/unit, conditional molar conversion, protocol, experiment cluster and unresolved fields. A missing independent n remains blank. These rows release zero primary-model labels.

Run `recover_supplements.py` for public supplement access and Supplement_Access.json for actual attempts. BJOC supplement S1 was recovered and its ORAC section on pages S8-S9 checked as text. Public recovery of the 60-flavonoid Table S1 failed, followed by successful researcher-supplied recovery. The [current intake](../02_user_supplied_sources/README.md) contains all 60 original rows and recorded conflicts. The public-access log retains the earlier failed requests as acquisition history.

Finally run `python 03_candidate_selection/05_model_robustness/check_new_source_transfer.py`. It compares six provisional new rows from three DOIs with fixed existing estimates, then reports evidence coverage and source dependence. It preserves source qualification requirements before model expansion. Source_Expansion_and_Model_Readiness.md is the current assessment of stability and representation.

`recover_alternative_fulltexts.py` attempts NCBI BioC recovery for public XML failures. Alternative_Fulltext_Access.json records one additional recovered text pending reading and three remaining failures. This text is separate from the 79 JATS-XML screens and their 215-table inventory. Metadata_Enrichment_Audit.csv records 12 fields filled from later query responses, including three previously omitted PMCIDs. Non-query source caches are excluded from query-register rebuilding by schema.

## Minimum-20 comprehensive evidence requirement

The researcher authorized comprehensive evidence packages for every one of the 193 current candidate profiles, with a target of at least 20 relevant publications per compound. Antioxidant activity, mechanism and dietary occurrence may contribute to the package. Original ORAC capacity studies retain a separate qualification track. A documented scarcity exception requires expanded searches and screening; a low hit count from one query does not establish scarcity.

Run `audit_twenty_paper_coverage.py` to reproduce the master-register baseline. Minimum20_Candidate_Coverage.csv reports provisional associations and numeric-source counts. Minimum20_Article_Screening_Queue.csv retains all 106123 existing candidate/article associations for subsequent reading.

Run `retrieve_minimum20_abstracts.py` to recover core records and abstracts using the saved canonical broad queries for all candidates. The first page contains up to 100 records per query, expanded to 1000 for four initially undercovered compounds. Full original JSON responses are stored under the ignored local inputs/minimum20_abstracts cache with query URLs and dates. Package CSVs preserve abstracts and source hashes. Automated rules require an explicit canonical-name or documented-alias occurrence and antioxidant/redox/dietary context in the title or abstract. Their relevance decisions require scientific review. ORAC mentions schedule original-capacity checks. Query result counts, rule-screened abstracts, full-text-reviewed studies and model observations have distinct fields.

Minimum20_Abstract_Coverage.csv records the first-page limit and remaining synonym, pagination and full-text work. Minimum20_Abstract_Evidence_Packages.csv retains all passing records, including those beyond 20. Review articles remain eligible contextual references and require reference tracing for numeric observations. Duplicate reports of one experiment require source-level reconciliation. IF values remain missing until dated journal-metric verification.

Minimum20_Remaining_Gaps_and_Export_Queries.csv supplies broad Web of Science and Scopus searches for remaining gaps. These institution exports should include full records, abstracts, DOI, publication types and cited references, with all result pages retained. Scarcity decisions await synonym, citation and cross-database checks.

## Undercovered-compound source expansion

The 17 initially undercovered candidates receive chemical-name-only queries with documented aliases and up to 1000 records per response. Relevant title/abstract screening remains explicit. Minimum20_Gap_Identity_and_Alias_Audit.csv records alias inputs and unresolved identities. Probetanin has no current formula or PubChem CID and requires original-source identity resolution before chemical evidence aggregation. Miraxanthin V additionally uses dopamine-betaxanthin, supported by the original body text at PMC32006.

Run `screen_minimum20_body_mentions.py` after abstract retrieval. Remaining undercovered names are searched in Europe PMC BODY fields, and public JATS XML is checked for explicit names in body paragraphs. Existing abstract-package DOI/PMID keys are removed before recovery. Minimum20_Body_Located_Leads.csv provides exact matched paragraphs and source hashes. These are located contextual leads with scientific relevance review pending. The script records each access failure and missing body match. No whole-paper reading or new model-label approval is inferred from a paragraph match.

Body recovery uses batches of three sources and stops when combined located leads reach at least 20 or retrieved candidates are exhausted. Unchecked records remain visible in the body search audit. Run `build_minimum20_review_panel.py` after body screening to reconcile coverage and generate the next-reading panel. The panel prioritizes ORAC mentions, non-review metadata and public full text. These scheduling criteria preserve original quality-appraisal fields as pending.
