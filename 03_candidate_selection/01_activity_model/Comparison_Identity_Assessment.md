# Reference identity and experimental-panel eligibility

Run `audit_comparison_identity.py` after `build_analysis_entry.py`. The 25 source-local observations map to 17 current candidate IDs. All 25 match reference names and have a formula, CID and InChIKey in the existing identity profiles. This is a database crosswalk check; it is not an independent structure confirmation for each experimental material.

All 25 linked food-occurrence fields remain CLASS_LEVEL_CURATION_ONLY, and exact form/lot has not been verified. Consequently, no record is upgraded to approved experimental-panel eligibility. Source-local values remain available for descriptive analysis. Source nomenclature, stereochemistry, salt/hydrate state, purity and candidate-specific food provenance must be resolved before a purchased material is treated as equivalent to the source material.

The existing within-source order is unchanged. Its key (paper, scale, dose) is a descriptive partition, not proof that every material and solvent is interchangeable. The five caffeoylquinic-acid records especially require positional identity and source-compound-number verification; names and formula alone cannot distinguish positional isomers. The next focused work should close food-source and exact-form evidence for these 17 substances rather than treating another graph calculation as scientific validation.

`results/Comparison_Identity_Audit.csv` gives each observation's source location and reference-identity URL beside the unresolved fields. `results/comparison_identity_qc.json` records counts. Human review remains NOT_REVIEWED and change_applied=NO. No original records, frozen assets or scientific approvals are modified.
