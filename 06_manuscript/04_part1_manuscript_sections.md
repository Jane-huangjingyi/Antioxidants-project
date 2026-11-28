# Literature evidence prioritizes food-derived antioxidants for aqueous testing

## Abstract

Food-derived antioxidants are often compared across assays with different reaction conditions and reporting scales. We developed a workflow that links chemical identity and original measurements to conditional rank estimates for prospective aqueous testing. Automated screening assessed 76,383 provisional literature records and generated an ORAC-focused review queue. A conditional fluorescein-based oxygen radical absorbance capacity model combined 125 observations from 14 DOI reports covering 51 compounds. On 81 matched observations scored under whole-DOI holdout, the expanded model had a log-capacity root mean squared error of 0.518, compared with 0.595 for the prior model. Twelve compounds remained within ten positions of their reference rank across model scenarios and conservative source-deletion bounds. The resulting set provides candidates for experimental qualification and shows how instability can limit prioritization even when reported capacity is high.

## Introduction

Food-derived chemicals vary in their capacity to protect a probe from oxidation, and their measured activity depends on the reaction chemistry and assay conditions. The fluorescein-based oxygen radical absorbance capacity (ORAC-FL) assay quantifies probe protection against radical-induced fluorescence decay [1]. Antioxidants can have different kinetic profiles, so assay settings and the integration procedure affect the interpretation of Trolox-equivalent results [2]. A candidate that ranks highly in a particular report can therefore be difficult to compare with a compound measured under another protocol.

We sought to prioritize chemically defined food-derived compounds for experimental qualification in a prospective aqueous absorbance assay. We combined literature retrieval, compound identity checks and original-source extraction with a report-aware conditional ORAC-FL model. We assessed whether candidate placement survived model and source changes and reported rank stability alongside the underlying activity and evidence support.

## Discussion

The evidence synthesis identified twelve compounds whose conditional ranks remained stable under the evaluated scenarios, spanning a wide range of estimated ORAC-FL capacities. Rosmarinic acid and L-ascorbic acid illustrate different experimental roles. The evidence for a high position was sensitive to the source set for rosmarinic acid, while the position of L-ascorbic acid was comparatively stable despite modest estimated capacity. This distinction allows a future experimental panel to cover a range of capacities and retain a visible record of how each candidate was prioritized. A top-down pathway framework (20 pathways × 12 candidates, 108 solid cells) showed that the retained compounds share core antioxidant defenses (NRF2/ARE, glutathione, ferroptosis/lipid-peroxidation defense) while differing in redox-linked signaling, adding biological plausibility to the chemical-capacity ranking; this participation evidence does not establish direct target binding.

The search snapshot provides broad discovery coverage, with final eligibility and independent experiment assessments incomplete. The fitted evidence network therefore reflects a targeted and conditional subset of original measurements. Report-level deletion measures dependence on the available sources and the rank bounds reflect unresolved contrasts. The ±10 rule was selected during development of this dataset and requires evaluation in subsequent evidence updates. The model estimates chemical capacity under the available ORAC-FL protocols. Validation in an absorbance-based assay, material-specific suitability and biological effects require separate measurements.

## Data availability

The source data for Fig. 1 comprise the screening counts, full-text batch summary, model validation results and compound-level ranking table. The project records original observations, units, DOI identifiers and source locators. PubMed and Europe PMC records can be recovered through their public interfaces using the documented search queries. Access to raw Web of Science exports is subject to institutional licensing. The manuscript-specific analysis snapshot and source data are available from the authors for editorial and peer review, subject to these source restrictions.

## Code availability

The analysis uses Python and R. The project repository is https://github.com/Jane-huangjingyi/Antioxidants-project. The manuscript-specific source tree contains the entry point run_pipeline.py and the R procedure 06_manuscript/code/04_render_figure1.R. The manuscript-specific version of the code and its execution instructions are available from the authors for editorial and peer review.

## References

1. Ou, B., Hampsch-Woodill, M. & Prior, R. L. Development and validation of an improved oxygen radical absorbance capacity assay using fluorescein as the fluorescent probe. J. Agric. Food Chem. 49, 4619–4626 (2001). https://doi.org/10.1021/jf010586o

2. Carvalho, J. R. B. et al. Exploiting kinetic features of ORAC assay for evaluation of radical scavenging capacity. Antioxidants 12, 505 (2023). https://doi.org/10.3390/antiox12020505

3. Page, M. J. et al. The PRISMA 2020 statement: an updated guideline for reporting systematic reviews. BMJ 372, n71 (2021). https://doi.org/10.1136/bmj.n71

## Figure legends

Fig. 1A-B | Literature evidence, conditional ORAC-FL ranks and candidate retention. A, Compound registration, screening and scoped verification together with the conditional-model cohort. The fitted cohort also used original evidence from earlier targeted reviews. B, left, median within-block ORAC-FL percentile, fraction of conditional-model reports with a typed standard deviation (SD), and conditional-model DOI count. Both panels in B show the twelve retained compounds and two examples on hold, rosmarinic acid and gallocatechin. In B, right, points are expanded conditional ranks. Segments show combined ranks across model scenarios and conservative whole-DOI deletion bounds. Shading indicates ten rank positions on either side of the reference, truncated at the ends of the ranking. Gallocatechin becomes unavailable in a deletion and therefore has no displayed interval. Source data list all 51 ranked compounds and retain the remaining profiles with unavailable ranks.

Fig. 1C | Top-down antioxidant pathway framework for the twelve retained candidates. A curated universe of 20 Reactome/KEGG-anchored pathways (8 core antioxidant/redox-defense, 12 broader redox-linked signaling) is crossed with the 12 retained compounds (240 cells). Cell colour encodes evidence grade: functional participation (loss-of-function), in vivo/ex vivo body readout, abstract-level candidate, cell-only, and searched-no-report. The right margin compares full-text-supported cells with all mapped evidence, including abstract-level and cell-only records. A cell with no qualifying report indicates a gap in the checked evidence. Shared core pathways (NRF2/ARE, glutathione, ferroptosis/lipid-peroxidation defense) and compound-specific signaling pathways are visible; a supplementary UpSet shows shared-pathway intersections. Source data: 07_pathway_framework_matrix.csv and Pathway_Fulltext_Verification record.
