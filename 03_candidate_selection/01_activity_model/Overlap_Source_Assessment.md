# Cross-paper overlap: dose-specific evidence

## Quercetin cross-paper decision

Run `build_quercetin_comparison.py` to generate `results/Quercetin_Cross_Paper_Compatibility.csv` from the two existing structured extractions. The current decision is DO_NOT_POOL_CURRENTLY. Both studies report pH 7.4 and 37 degrees C, but agreement on these two conditions does not establish a common endpoint. The 2019 table gives an experimental ln(ORAC) summary, whereas the 2023 table gives a molar calibration-slope ratio. The 2019 final acetone fraction, complete integration rule, error definition and material form are unresolved; the 2023 record specifies 5% ethanol and quercetin dihydrate. No source-adjustment coefficient can be inferred by dividing their point summaries.

The 2023 article's Results describe evidence of oxidation-product contributions above specified concentrations, while its Discussion also states that quercetin and caffeic-acid curves showed no evidence of oxidation by-products at the highest concentrations. Preserve this internal tension; do not resolve it by choosing the preferred passage. The operational AUC endpoint can include secondary-product protection and kinetic effects. Our target must therefore be described as assay-defined integrated capacity, not intrinsic parent-molecule stoichiometry. Reaction rate should be reported separately but cannot simply be assumed absent from AUC.

Remaining source tasks are to recover the exact inherited 2019 protocol/equation, clarify experimental-column errors and final conditions, and obtain any relevant supplementary definitions. Supplementary materials were not reviewed in this check. ANN repeat-training SD is explicitly unsuitable as experimental measurement error. These are source-specific gaps, not grounds to assign zero activity. No formal score, pooled capacity or new ranking is generated.

On 2026-11-06, original article text and table XML were recovered through the public NCBI BioC API for DOI 10.3390/antiox11091784 (PMC9495677) and 10.3390/ijms20092328 (PMC6539043). Access hashes are in `inputs/overlap_source_access.json`. Visual figures and supplementary files were not inspected. Local raw responses are ignored; the committed diagnostic CSV supports offline inspection. Refresh explicitly with `recover_overlap_sources.py`, then `extract_overlap_diagnostic.py`.

## Phenolic-acid overlap

[Original Table 2](https://pmc.ncbi.nlm.nih.gov/articles/PMC9495677/) supplies gallic acid and caffeic acid, both present in the rechecked 2023 source. At reported compound concentrations 2.5 and 5 micromolar, gallic acid gives 23 +/- 1 and 28 +/- 1 micromolar TE; caffeic acid gives 31 +/- 2 and 60 +/- 1. Division by the reported compound concentration yields conditional molar ratios 9.2 and 5.6 for gallic acid, and 12.4 and 12.0 for caffeic acid. This is not a calibration-slope estimate. The gallic-acid dose dependence prevents treating the two ratios as interchangeable measurements of one constant. Do not average them or treat two doses as two studies.

Methods report three replicates and an 80-minute reaction observation. The checked table and methods do not define the plus/minus statistic or establish independent experimental batches. Stock solutions use ethanol/water 80:20; final well solvent fraction and complete inherited assay parameters require further verification. No sampling variance is assigned. These rows extend overlap within the phenolic-acid group, not between that group and the Foods eugenol/capsaicin/vanillin or ellagic-acid groups. They are not yet added as approved model inputs.

## Flavonoid modelling source

[The 2019 original article](https://pmc.ncbi.nlm.nih.gov/articles/PMC6539043/) describes purchased flavonoids and an ORAC experiment in Methods 3.1, so it must not be dismissed as predictions alone. Nevertheless, predicted results and error bars over 1000 ANN training cycles are not experimental sampling errors. Its experimental capacity table, transformation and replicate definitions still require a dedicated extraction before using quercetin as an additional study contribution. No predicted value was imported here.

## Next modelling decision

### 2019 experimental-table extraction completed

`extract_flavonoid_log_capacity.py` now extracts all 36 experimental rows from Table 3 to `results/Flavonoid_Log_Capacity_Extraction.csv`. These are source-table rows, not 36 newly eligible dietary candidates or independent studies. PLS and ANN prediction columns are excluded. Table 3 explicitly reports ln(ORAC); Methods describe natural-log transformation before modelling. For quercetin, 1.970 +/- 0.003 is on that log scale. Exponentiating the reported location yields approximately 7.1707, but does not establish an arithmetic mean or a valid original-scale SD. The plus/minus statistic in the experimental column remains unresolved; ANN-training variability must not be substituted for it.

Methods 3.2 and 3.3 specify pH 7.4, 37 degrees C, one-minute fluorescence readings, triplicate measurements and acetone/water 50:50 stock diluted in buffer. Final solvent fraction, integration duration and independent-batch structure remain unresolved. Source quercetin therefore extends the overlap evidence but is not yet a fully compatible additional model input. Existing candidate IDs and food-scope decisions have not been assigned by name alone. The 36-row count, unique source-row numbers and quercetin log value are checked by the extraction script. No formal score is calculated.

The recovery establishes shared compounds but not common target conditions. Next extract the 2019 experimental table and exact ORAC protocol, and clarify dose dependence and errors in the 2022 source. Keep method families separate until calibration and overlap justify a connection. A global potency score or a new Top20 has not been fitted. Original observations, source HOLDs, human-review states and frozen rankings remain unchanged.
