# Protocol provenance and the next capacity dataset

Checked on 2026-11-06. No model fitting, human approval or frozen-data change is performed.

## 2019 protocol reference identified

The publisher reference list for DOI 10.3390/ijms20092328 identifies Huang et al., *High-Throughput Assay of Oxygen Radical Absorbance Capacity (ORAC) Using a Multichannel Liquid Handling System Coupled with a Microplate Fluorescence Reader in 96-Well Format*. Its DOI is [10.1021/jf0201529](https://doi.org/10.1021/jf0201529), PMID [12137457](https://pubmed.ncbi.nlm.nih.gov/12137457/). This closes the bibliographic identity, not the equation or implementation audit. The complete protocol text/equations were not recovered in this check. Do not fill 2019 integration duration, final reagent concentrations, solvent fraction or experimental-error definitions by copying assumptions from other ORAC studies. The source's own modifications must still be checked.

## Additional primary-source lead

[Sakurai et al., 2022, DOI 10.1039/d1ra08918h](https://pmc.ncbi.nlm.nih.gov/articles/PMC8981064/) is a primary H-ORAC dataset worth checking against the existing source inventory before adding observations. Methods 2.2 explicitly describe molar Trolox-equivalent reporting, an average of three measurements, and a simultaneously measured ferulic-acid quality check. Stock solvent is methanol/water/acetic acid 90:9.5:0.5, diluted with buffer; this is not the final well composition. Three measurements do not establish three independent batches. The paper includes analogues and derivatives; dietary occurrence must be assessed individually. No values from plotted figures, secondary summaries or uninspected supplementary files are imported.

This source may supply overlap beyond the current flavonoid subset, but the overlap has not yet been quantified. First determine whether it is already cached or extracted, recover its original numeric table/supplement, map molecular identities, then compare shared compounds and protocol families. A paper-wide experimental series offers a within-protocol comparison opportunity; it does not establish compatibility with the planned absorbance assay.

## Decision

### Targeted reconciliation result

`inputs/sakurai_targeted_recheck.json` records three original Table 1 rows and explicit SDs. Run `build_sakurai_recheck.py` for `results/Sakurai_Targeted_Reconciliation.csv`. Ferulic acid 3.474 and p-coumaric acid 3.766 exactly match the two canonical observations; SDs are 0.176 and 0.146 mol TE/mol. Eugenol 1.811 with SD 0.118 is absent from that canonical index but already present in the preserved Stage 24 primary-literature master as S24-013. It is therefore a recovered integration gap, not a newly discovered study. The Stage 24 DOI/name/method key must remain traceable.

Eugenol supplies a potential shared-compound link with the Foods study, while the two acids provide links to the 2022 phenolic-acid study. This is a source-overlap opportunity, not verified protocol equivalence or an approved graph merge. Three reported measurements do not establish independent batches, so no SD-squared-over-three sampling variance is assigned. No canonical record, frozen ranking or human-review status is changed. Next reconcile Stage 24 source keys across the quantitative extraction and verify protocol compatibility before enlarging model inputs.

Repository DOI search confirms that 10.1039/d1ra08918h already appears in `02_identity_and_evidence/results/chemical_observation_index.csv`, `latest_source_closure.csv` and preserved class-specific evidence masters. It is therefore an existing source to reconcile and expand, not a newly discovered independent study. Do not append another study contribution merely because the article has been accessed again. The next extraction must compare original table row identifiers with those existing records.

Keep quercetin pooling on hold. Prioritize numeric primary tables capable of connecting currently separate groups rather than repeatedly comparing the same unresolved pair. Retain log-scale experimental values, predicted values and assay-specific capacities as separate quantities. Source retrieval success alone does not authorize weighting or ranking.
