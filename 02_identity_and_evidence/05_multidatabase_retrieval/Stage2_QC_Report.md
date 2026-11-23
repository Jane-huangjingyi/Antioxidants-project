# Stage2 public retrieval QC

## WoS first-batch intake checkpoint

First-batch structural and field QC PASS. Raw SHA-256 verified, 500 ER markers and a closing EF, 500 parsed records, 500 distinct valid UT values, 489 distinct DOIs, 139 supplied PMIDs, 500 abstracts and 500 cited-reference lists. All per-record reference counts reconcile. The real file required preserving WoS records across embedded blank lines and reading the PM tag as PMID.

Cross-database identifier hits cover 269 of the batch in the current PubMed export, 271 in the Europe PMC baseline route union, and 228 in the historical library, with overlap across sources. The union of exact identifier hits is 277. Reconciliation gives 271 existing report-key links, 202 additional provisional WoS keys, six held identifier cases and 21 title-only review cases. There were zero duplicate UT or DOI rows within this batch. All rows are pending screening or prior-decision mapping. WoS-linked reports and experiments remain distinct units. This is a partial acquisition checkpoint.

## Historical public checkpoint

Public retrieval snapshot PASS. Stage2 completion gate OPEN. Two public cursor chains exhausted. Three category-route pagination duplicates reconcile the difference between downloaded and reported counts. Consolidated identifier keys 132369; existing candidate associations 106171. Exact identifier grouping preserves provenance. Known anchors are audited separately. Title/author/year near-duplicate and conflicting identifier adjudication remain pending. Institutional exports,independent PubMed export,Scholar inspection,revised compound queries and new-compound assignment remain pending. Human review status remains NOT_REVIEWED.
