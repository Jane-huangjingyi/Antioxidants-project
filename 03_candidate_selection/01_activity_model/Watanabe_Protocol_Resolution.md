# Standardized H-ORAC protocol provenance

Sakurai reference 5 is Watanabe et al., DOI [10.2116/analsci.28.159](https://doi.org/10.2116/analsci.28.159). The [publisher PDF](https://www.jstage.jst.go.jp/article/analsci/28/2/28_2_159/_pdf) was inspected on 2026-11-06; supporting files were not inspected.

The paper distinguishes methods A and B. Page 160 specifies 37 degrees C, two-minute readings for 90 minutes, and AUC over 8–90 minutes. Method A uses a fitted Trolox calibration. Page 162 describes method B as a two-stage dilution procedure; its final result uses double-log dilution/net-AUC interpolation to the response of 20 micromolar Trolox. This is not an antioxidant/Trolox calibration-slope ratio. The PDF's net-AUC subtraction wording also requires explicit sign verification before implementation.

Sakurai cites this paper without identifying A versus B. Therefore, these are inherited-protocol alternatives, not confirmed Sakurai implementation parameters. Keep the study-specific timing and estimator unresolved. Interlaboratory precision statistics from the protocol paper cannot supply Sakurai compound-specific sampling variances or independent n.

## Consequence for integration

The missing protocol identity is closed, but the method-variant gate remains open. Do not force Sakurai's molar capacities into the slope-ratio endpoint family. Next inspect supporting SOPs or source implementation records for the variant and analysis definition. The current no-pooling decision remains justified; no negative activity inference follows.
