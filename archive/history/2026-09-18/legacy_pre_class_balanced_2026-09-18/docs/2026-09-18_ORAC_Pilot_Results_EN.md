# Historical ORAC Literature Pilot Results (English)

## 1. Pilot composition

The frozen pilot contains 17 compounds: 10 phenolic/polyphenolic candidates, 3 vitamin/vitamin-like candidates, 3 carotenoids, and 1 organosulfur compound. Expected assay assignment is 11 H-ORAC, 5 L-ORAC, and 1 noncanonical special case (sulforaphane). Eight candidates also carry a technical special-case flag; this flag may overlap with an H/L arm.

Identity was verified against official PubChem records. Catechin, epicatechin, EGCG, aglycones/glycosides, trans-resveratrol, L-ascorbic acid, tocopherol homologues, and carotenoid isomers were treated as distinct entities.

## 2. Literature extraction result

The pilot formally extracted 11 original ORAC-FL numerical records from three original method/compound studies: Ou et al. 2001 (H-ORAC-FL, Table 4), Huang et al. 2002 (L-ORAC-FL tocopherol values reported in the paper), and Figueroa et al. 2023 (H-ORAC-FL, Table 3). The records cover catechin (1), quercetin (2), gallic acid (1), caffeic acid (2), chlorogenic acid (1), L-ascorbic acid (2), alpha-tocopherol (1), and gamma-tocopherol (1).

Under the frozen rubric, **Tier A=0, Tier B=11, Tier C=0, and Tier X=0**. The remaining nine compounds had no completed original auditable ORAC-FL extraction in this limited pilot and are coded `not_measured`, never zero.

The Tier B assignments reflect missing methodological detail rather than absent numbers. Papers commonly omit numerical purity, complete compound-specific linear ranges, compound-specific optical/interference QC, or all reading parameters. The accessible Huang 2002 abstract confirms the L-ORAC method and numerical values, but full record-level methods still require second-pass full-text verification, preventing Tier A assignment.

| compound | Tier A | Tier B | Tier C/X | status |
|---|---:|---:|---:|---|
| EGCG | 0 | 0 | 0 | not_measured |
| Catechin | 0 | 1 | 0 | supportive_only |
| Epicatechin | 0 | 0 | 0 | not_measured |
| Quercetin | 0 | 2 | 0 | supportive_only |
| Kaempferol | 0 | 0 | 0 | not_measured |
| Gallic acid | 0 | 1 | 0 | supportive_only |
| Caffeic acid | 0 | 2 | 0 | supportive_only |
| Ferulic acid | 0 | 0 | 0 | not_measured |
| Chlorogenic acid | 0 | 1 | 0 | supportive_only |
| Resveratrol | 0 | 0 | 0 | not_measured |
| L-Ascorbic acid | 0 | 2 | 0 | supportive_only |
| alpha-Tocopherol | 0 | 1 | 0 | supportive_only |
| gamma-Tocopherol | 0 | 1 | 0 | supportive_only |
| Lycopene | 0 | 0 | 0 | not_measured |
| beta-Carotene | 0 | 0 | 0 | not_measured |
| Lutein | 0 | 0 | 0 | not_measured |
| Sulforaphane | 0 | 0 | 0 | not_measured |

## 3. Numerical and comparability interpretation

True Tier B values are retained in the raw file but do not enter median/range/IQR ranking in `ORAC_Pilot_TierA_Analysis.csv`. They illustrate methodological heterogeneity: quercetin was reported as 7.28 and 16.62 mol TE/mol, caffeic acid as 4.37 and 8.26, and L-ascorbic acid as 0.95 and 0.53. These differences support the rule against direct historical pooling rather than providing rankable central estimates.

Ou 2001 used 12.8 mM AAPH, 48 nM fluorescein, 75 mM phosphate at pH 7.4, 37 °C, and one-minute readings for 30 minutes. Figueroa 2023 used a different fluorescein/AAPH configuration and demonstrated effects of ethanol and kinetic analysis. Method differences and incomplete Tier A fields jointly prevent pooling.

## 4. Figure interpretation

`H_ORAC_Historical_Distribution.png` and `L_ORAC_Historical_Distribution.png` are arm-specific coverage diagnostics rather than invented distribution/rank plots because no Tier A records were available. `ORAC_Literature_Coverage.png` shows that current support is concentrated in selected phenolics, ascorbic acid, and tocopherols; carotenoids, EGCG, epicatechin, kaempferol, ferulic acid, resveratrol, and sulforaphane remain gaps in this pilot.

## 5. Required conclusions

1. The pilot contains 17 compounds.
2. Class counts are 10 phenolic/polyphenolic, 3 vitamin/vitamin-like, 3 carotenoid, and 1 organosulfur.
3. Eleven are expected H-ORAC candidates.
4. Five are expected L-ORAC candidates.
5. One is primarily a noncanonical special case; eight carry at least one technical special-case flag.
6. Per-compound A/B/C/X counts appear above and in the coverage CSV; totals are A=0, B=11, C/X=0, with nine compounds lacking completed records.
7. No compound currently meets the Tier A standard for stable historical ranking.
8. None of the 17 can enter a formal numerical ranking; eight have supportive Tier B data and nine have no usable completed record.
9. Formal within-arm H-ORAC ranking is not feasible because coverage is sparse, Tier B only, and strongly protocol dependent.
10. Formal within-arm L-ORAC ranking is not feasible; only alpha- and gamma-tocopherol each have one Tier B record pending full-text verification.
11. Cross-H/L ranking is invalid and was not performed.
12. Potential CUPRAC data were identified for 9/17 candidates, mainly phenolics, ascorbic acid, and alpha-tocopherol. This supports a secondary coverage program but not a unified cross-class evidence layer yet.
13. Current historical data do not support a formal Top20.
14. Main gaps are missing Tier A method fields, sparse L-ORAC/carotenoid original data, absent special-case QC, and large same-compound differences across protocols.
15. Highest standardized-retest priorities are lycopene, beta-carotene, lutein, EGCG, epicatechin, kaempferol, resveratrol, ferulic acid, and sulforaphane. Tocopherol full-text methods should be completed before deciding on retesting.

## 6. CUPRAC coverage

CUPRAC was assessed for coverage only. The comparative work by Apak et al. covers catechins, quercetin, phenolic acids, ascorbic acid, alpha-tocopherol, and other relevant candidates, supporting its value as an orthogonal ET/reducing-power assay. Comparable pilot coverage remains weak for carotenoids, gamma-tocopherol, resveratrol, chlorogenic acid, lutein, lycopene, and sulforaphane. Record-level assay and molar-unit review remains necessary before formal use.

## 7. Conclusion and stop point

The candidate scope can be frozen, but a strict historical ORAC ranking cannot yet be executed. The most informative pilot finding is that all commonly cited numerical records were downgraded to Tier B under the frozen Tier A rubric. The next step is second-pass full-method extraction for key papers and a harmonized H-ORAC/L-ORAC retesting plan for priority gaps. This round does not expand to a formal Top20, Stage 2 ranking, or target extraction.
