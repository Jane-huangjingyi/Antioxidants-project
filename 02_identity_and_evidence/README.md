# 02. Resolve identity and assess the available evidence

Run `python 02_identity_and_evidence/code/build_evidence_profiles.py` after Step 01. The output is `results/candidate_evidence_profiles.csv`; chemical observations and later source closure have separate source-linked tables.

Identity requires reference CID, InChIKey and molecular formula. The committed PubChem refresh contains official property responses for the 20 review candidates and the two scope-gap compounds; other identities retain their explicitly dated legacy cache status. These are molecular references, not analytical confirmation of a purchased lot. Stereochemistry, salt/counterion, hydrate and purity must match the reagent used.

Food occurrence, identity, chemical assay evidence and biological validation are separate fields. Existing D1-D5 snapshot statuses are carried forward for the 157 covered candidates; profiles outside that snapshot are not assigned zero evidence. Confirmed independent study support comes from the latest preserved 6D closure, not metadata-deduplicated publication totals or experiment-row counts. Typed SD, unresolved sources and future-year metadata are kept visible. Missing sources and missing uncertainty are not repaired with secondary numbers.

Original mechanism relations, target confirmation, antioxidant relevance and human states remain in their original source tables. The new workflow applies none of the 257 historical proposals. AFF-0061 receives no validated-target credit from unapproved observations.

The [full source index](results/source_file_index.csv) and [preserved evidence catalogue](../90_archive/legacy_2026-11-05/outputs/review_20261030/Evidence_Catalog_2026-10-30.xlsx) locate prior stages. The old workbook preserves its original language and dates; the active English workbook is a review-oriented projection of the current selection chain. Journal metric gaps remain unverified, and journal impact factors do not enter selection.

**Manuscript link:** Methods 2, Table S1 and the observation/source registers support identity and evidence statements. No manuscript claim should exceed the checked source scope.
