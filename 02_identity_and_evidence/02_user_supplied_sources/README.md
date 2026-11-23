# 02.2 Original articles supplied by the researcher

This is the current original-source intake after the public-recovery pass. Start with [Source_Assessment.md](Source_Assessment.md), [source documents](Source_Document_Manifest.csv), [138 capacity rows](Original_Capacity_Extraction.csv), [source conflicts](Source_Conflicts.csv), and [existing-reference reconciliation](Existing_Reference_Reconciliation.csv). The [updated model diagnostics](../../03_candidate_selection/06_verified_source_update/README.md) use these extracted facts and the previously recovered 2023 source.

Seven files at their unique `download_raw` locations represent six reports. Five reports provide 116 ORAC-FL, 13 ORAC-PGR and nine ORAC-PE source rows. One 2020 article and its Table S1 form a single source. Original file hashes, numeric table locations, chemical-name mappings and unresolved fields accompany the values. The supplied DPPH article has DOI 10.1016/j.foodchem.2008.08.008. The comparative study DOI 10.1016/j.foodchem.2008.08.013 is now recovered.

## Reproduction

Use Python with `pypdf` installed. Extraction was executed with pypdf 6.21.4. Word table parsing uses `zipfile` and `xml.etree.ElementTree` from the standard library.

```sh
python 02_identity_and_evidence/02_user_supplied_sources/extract_user_sources.py
python 03_candidate_selection/06_verified_source_update/fit_verified_source_diagnostics.py
Rscript 04_05_experimental_validation/code/figure_support/render_verified_source_diagnostics.R
python 07_quality_control/code/02_validate_workflow.py
```

The extractor checks the actual reviewed SHA256, DOI and page count before emitting numeric records. PDF table transcriptions have source-text checks and targeted visual review. Word physical rows contain multiple logical records, so paragraph positions are preserved within each cell. All compound numbers 1-60 must appear exactly once. DPPH and cellular IC50/EC50 strings remain ancillary source columns, including their inequality signs. Their values are separate endpoints.

Original PDFs and DOCX remain local and ignored by Git, with hashes and original filenames in the manifest. Retain or share a legally obtained original at that path to rerun extraction. Committed numeric tables support inspection and model reproduction from extracted data. Original-source re-extraction additionally requires the matching documents. Source content is treated as research material. It supplies no operational instructions to the agent.

[Candidate_Extension_Leads.csv](Candidate_Extension_Leads.csv) records 30 unmatched FL rows for subsequent food-occurrence, formula and exact-identity checks. BHA remains an unmatched source comparator in the original extraction. These leads extend the discovery audit while the current 193-ID index remains the analysis universe. All human review fields retain NOT_REVIEWED and change_applied=NO.

## Tabart 2009 source update, 2026-11-13

DOI 10.1016/j.foodchem.2008.08.013 is recovered. The 24 ORAC ratios in Table 1 (PDF p6, journal p1231) were visually checked, with abbreviations from Fig1 (PDF p3). Nineteen rows map by name to the current index. Source ratios are normalized to measured Trolox and retain one-decimal precision. The four-assay weighted average is a separate endpoint.

Methods (PDF p2) report fluorescein/AAPH, 37 C, duplicate ORAC at three dilutions and two-minute readings over four hours. ORAC pH and final methanol are absent. PBS pH 7.4 refers to other assays. The source reports mean +/- SEM from at least three independent experiments, but Table 1 lacks row errors and exact n. Sampling variances remain blank. Source forms and stereochemistry remain qualification fields. Mapped rows enter the expanded diagnostics as one source block. The reported-pH core excludes this source. Review remains NOT_REVIEWED and change_applied=NO.

Reference: Tabart J et al. Comparative antioxidant capacities of phenolic compounds measured by various tests. Food Chemistry. 2009;113:1226-1233. DOI 10.1016/j.foodchem.2008.08.013.
