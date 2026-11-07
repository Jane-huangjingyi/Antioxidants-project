# Legacy quantitative coverage and scale checks

Run `python 03_candidate_selection/01_activity_model/audit_legacy_coverage.py` from the root. The read-only comparison generates `results/Legacy_Quantitative_Coverage.csv` and `results/legacy_coverage_summary.json`. Each row carries DOI, original locator, legacy source row, source record ID, proposed identity match and coverage decision. Numeric legacy records are inventoried, not approved or imported.

The preserved aqueous primary-literature master contains 130 nonempty numeric rows. Against the current 77-row traceable extraction, 71 match by DOI and compound name, one has a possible DOI/current-ID match, and 58 are unmatched. These counts concern legacy rows, not unique experiments or independent studies. Exact-name matches may still conceal form, concentration or assay differences. Unique PubChem CID mappings are identity candidates and do not resolve stereochemistry, hydration or food occurrence.

Of the unmatched rows, 30 are labelled H-ORAC-FL. The other 28 include excluded arms, kinetic, cellular, chelation and other assay constructs; they must not be pooled automatically as molar capacity. Seven unmatched rows come from DOI 10.1039/d1ra08918h, including the previously rechecked eugenol row. Therefore, the present quantitative extraction is incomplete relative to existing project evidence. Completeness cannot be assessed by its row count alone.

## Scale conflict requiring quarantine

The historical row for eriodictyol, DOI 10.3390/ijms20092328, stores original value 7.486 alongside a unit string describing ln(ORAC). The original Table 3 extraction gives ln(ORAC) 2.013. Since exp(2.013) is approximately 7.486, the legacy number appears back-transformed while its unit label remains logarithmic. Do not exponentiate 7.486, import it as a log observation, or count it as a second experiment. Keep the original file unchanged and reconcile this row against the new source extraction before any integration. The exact historical conversion provenance remains to be checked.

## Next integration rules

First reconcile the 30 unmatched H-ORAC-FL rows by DOI, compound/form, original table row, endpoint and concentration. Preserve source HOLDs and exclusions. Join later source corrections rather than treating historical tiers as current approval. Investigate scale conflicts before unit conversion. Add newly source-verified rows to a derived integrated table only after duplicate and identity checks; then recalculate graph connectivity and model identifiability. Unknown errors and independent-batch counts remain missing. No score, rank, original source value or human-review state is changed by this inventory.
