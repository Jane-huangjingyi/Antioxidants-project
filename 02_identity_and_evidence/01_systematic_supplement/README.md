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

The public register has 49,906 provisional identifier groups. Linking historical and supplemental DOI/PMID records gives 87,386 provisional master groups and 106,123 candidate-article links. Journal metadata are available for 48,987 master groups. Bibliographic conflicts, title near-duplicates and related reports require review before a final PRISMA count. Known-source recall covers 18 of 95 existing candidate-DOI pairs through candidate-name routes, 71 through the broad class/method route at article level, and 93 through DOI anchors. Direct anchor recovery does not count as successful candidate-name search recall.

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
