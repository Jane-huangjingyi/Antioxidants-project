# Stage2 manual export handoff

The [first-batch audit and acquisition plan](WoS_Batch_Acquisition_and_Intake.md) records the completed WoS first export and researcher-reported recall tests. The observed WoS limit is 500 records per export.

First action: open [Web of Science Advanced Search](https://www.webofscience.com/wos/woscc/advanced-search) through institutional sign-in, select Core Collection, and run the DOI check below. Save the search history showing the accepted query and count. Then run the method and class routes separately.

Primary scope is 2020-01-01 through 2026-11-17 by first public publication. Search years 2020–2026 where the interface supports years only. Preserve online and issue dates for subsequent eligibility checks. Search 2016–2019 separately for documented evidence gaps. Run each anchor alone, then intersect it with each route and record the count. WoS, Scopus and CNKI queries below await authenticated platform tests.

## Web of Science Core Collection

```text
DO=("10.1016/j.bbadva.2021.100030" OR "10.1016/j.foodchem.2025.146338" OR "10.1080/14786419.2025.2493187" OR "10.1155/2020/4150897")
TS=(ORAC OR "oxygen radical absorbance capacity" OR "pyrogallol red" OR "crocin bleaching" OR ABTS OR DPPH OR FRAP OR CUPRAC) AND PY=(2020-2026)
TS=((phenolic* OR flavonoid* OR carotenoid* OR lignan* OR vitamin* OR thiol* OR alkaloid*) AND (antioxidan* OR "radical scavenging")) AND PY=(2020-2026)
```

Export Plain Text with Full Record and Cited References. The researcher observed a 500-record limit. Use 1–500, 501–1000 and subsequent contiguous ranges if the dialog accepts them, starting at the first unexported range confirmed in the saved log. Record any result-set cap. Save Search History and identify indexes selected. [Clarivate export help](https://webofscience.help.clarivate.com/en-us/Content/export-records.htm)

## Scopus

Open [Advanced Document Search](https://www.scopus.com/search/form.uri?display=advanced).

```text
DOI(10.1016/j.bbadva.2021.100030) OR DOI(10.1016/j.foodchem.2025.146338) OR DOI(10.1080/14786419.2025.2493187) OR DOI(10.1155/2020/4150897)
TITLE-ABS-KEY(ORAC OR "oxygen radical absorbance capacity" OR "pyrogallol red" OR "crocin bleaching" OR ABTS OR DPPH OR FRAP OR CUPRAC) AND PUBYEAR > 2019 AND PUBYEAR < 2027
TITLE-ABS-KEY((phenolic* OR flavonoid* OR carotenoid* OR lignan* OR vitamin* OR thiol* OR alkaloid*) AND (antioxidan* OR "radical scavenging")) AND PUBYEAR > 2019 AND PUBYEAR < 2027
```

Export CSV with citation information, bibliographic information, abstracts and keywords, and references where available. Save Search History. Record the actual range and maximum shown for the selected fields. [Elsevier export help](https://www.elsevier.support/scopus/answer/how-do-i-export-documents-from-scopus)

## CNKI

Open [CNKI Advanced Search](https://kns.cnki.net/kns8s/AdvSearch), select Chinese academic journals and Professional Search, and apply the date filter.

Copy the first two lines from [CNKI query literals](Institutional_CNKI_Query_Literals.txt) separately. Line 3 supplies the compound-route example.

Check the listed DOIs in the DOI field where available, and use exact title lookup if the DOI field is absent. English DOI checks are indexing controls. In the Chinese journals collection, additionally test `10.7506/spkx1002-6630-20200901-012` and its local title (line 4 in the query file). The publisher's abstract documents a molar ORAC result for a defined peptide. Use this as a method recall control and leave protocol eligibility for separate review. [Publisher record](https://www.spkx.net.cn/EN/abstract/abstract53454.shtml)

Export RefWorks or EndNote with the richest available metadata and preserve the displayed export range or selection limit. Where abstract or cited references are unavailable, record the omitted fields. The citation export button exports selected records and may omit their cited-reference lists.

## Compound-route templates

Use the candidate-specific terms in PubMed_Compound_Query_Status.csv for equivalent institution searches. Keep distinct candidate IDs for salts, glycosides, hydrates and stereoisomers. Replace the sample identifiers below with each candidate's documented names. Search matches require exact material review.

```text
WoS: TS=("L-ascorbic acid" OR "vitamin C") AND TS=(ORAC OR "oxygen radical absorbance capacity" OR "crocin bleaching" OR ABTS OR DPPH OR FRAP OR CUPRAC) AND PY=(2020-2026)
Scopus: TITLE-ABS-KEY("L-ascorbic acid" OR "vitamin C") AND TITLE-ABS-KEY(ORAC OR "oxygen radical absorbance capacity" OR "crocin bleaching" OR ABTS OR DPPH OR FRAP OR CUPRAC) AND PUBYEAR > 2019 AND PUBYEAR < 2027
```

## Export location and log

Place files and search-history screenshots in `D:/JANE/GitHub/antioxidants project/download_raw/stage2_institutional/`, using subfolders `wos`, `scopus` and `cnki`. Keep original exported files as received. Scopus and CNKI batch maxima require inspection of the authorized session and selected export format.

Record one line per test or batch using [the operation template](Institutional_Search_Operation_Template.csv). Retain exact queries, local execution times with timezone, publication filters, result counts, first and last exported indices, export format and fields, and account-specific limits. Use [the public DOI control table](Public_Database_DOI_Controls.csv) for comparison. For recall, intersect the saved broad query with each saved DOI result using the platform's search-history combine function. Record each result and any indexing gap separately.
