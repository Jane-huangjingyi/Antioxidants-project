# Cross-paper overlap: dose-specific evidence

On 2026-11-06, original article text and table XML were recovered through the public NCBI BioC API for DOI 10.3390/antiox11091784 (PMC9495677) and 10.3390/ijms20092328 (PMC6539043). Access hashes are in `inputs/overlap_source_access.json`. Visual figures and supplementary files were not inspected. Local raw responses are ignored; the committed diagnostic CSV supports offline inspection. Refresh explicitly with `recover_overlap_sources.py`, then `extract_overlap_diagnostic.py`.

## Phenolic-acid overlap

[Original Table 2](https://pmc.ncbi.nlm.nih.gov/articles/PMC9495677/) supplies gallic acid and caffeic acid, both present in the rechecked 2023 source. At reported compound concentrations 2.5 and 5 micromolar, gallic acid gives 23 +/- 1 and 28 +/- 1 micromolar TE; caffeic acid gives 31 +/- 2 and 60 +/- 1. Division by the reported compound concentration yields conditional molar ratios 9.2 and 5.6 for gallic acid, and 12.4 and 12.0 for caffeic acid. This is not a calibration-slope estimate. The gallic-acid dose dependence prevents treating the two ratios as interchangeable measurements of one constant. Do not average them or treat two doses as two studies.

Methods report three replicates and an 80-minute reaction observation. The checked table and methods do not define the plus/minus statistic or establish independent experimental batches. Stock solutions use ethanol/water 80:20; final well solvent fraction and complete inherited assay parameters require further verification. No sampling variance is assigned. These rows extend overlap within the phenolic-acid group, not between that group and the Foods eugenol/capsaicin/vanillin or ellagic-acid groups. They are not yet added as approved model inputs.

## Flavonoid modelling source

[The 2019 original article](https://pmc.ncbi.nlm.nih.gov/articles/PMC6539043/) describes purchased flavonoids and an ORAC experiment in Methods 3.1, so it must not be dismissed as predictions alone. Nevertheless, predicted results and error bars over 1000 ANN training cycles are not experimental sampling errors. Its experimental capacity table, transformation and replicate definitions still require a dedicated extraction before using quercetin as an additional study contribution. No predicted value was imported here.

## Next modelling decision

The recovery establishes shared compounds but not common target conditions. Next extract the 2019 experimental table and exact ORAC protocol, and clarify dose dependence and errors in the 2022 source. Keep method families separate until calibration and overlap justify a connection. A global potency score or a new Top20 has not been fitted. Original observations, source HOLDs, human-review states and frozen rankings remain unchanged.
