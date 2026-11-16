# Original-source assessment

The researcher supplied six files representing five reports on 2026-11-12. The main 2020 PDF and original Table S1 DOCX resolve the previous supplement-access gap. The other three target ORAC articles are the 2013 Zhang study, the 2001 Ou method and the 2004 Davalos study. The remaining PDF is Sharma and Bhat's DPPH method article. Original file identity is recorded by DOI, SHA256 and page count in Source_Document_Manifest.csv.

| Report | Checked scope | Quantitative extraction |
| --- | --- | --- |
| 10.1155/2020/4150897 | Experimental and statistical methods, main Table 1 structural annotations on PDF pp2-3, Figure 1 on p5, original Table S1 cell paragraphs | 60 FL values. The original DOCX supplies compound names, ORAC means/errors and ancillary DPPH/CAA values. |
| 10.1021/jp307746c | PDF p2 experimental methods and statistics, Table 1 on p4 and its visual columns/footnotes | 13 FL and 13 PGR values. These are original measured assay outcomes. DFT descriptors and regression predictions supply separate evidence. |
| 10.1021/jf010586o | Materials and assay methods on PDF pp1-2, Table 4 and its visual footnote on p4 | Nine FL and nine PE values. Extracts, beverages and biological fluids retain their own material scope. |
| 10.1021/jf0305231 | Original methods on PDF p2, Table 2 and its visual footnotes on p4, comparison with cited data | Ten original FL values. Cited 2001 values in the discussion retain the earlier experiment's source key. |
| 10.1016/j.foodchem.2008.08.008 | DOI, title and analytical endpoint identity | DPPH method context. This file does not resolve the request for 10.1016/j.foodchem.2008.08.013. |

## Corrections to earlier references

The 2004 original Table 2 reports Quercetin 10.5 +/- 0.4 micromol TE/micromol. The earlier reference input attributed 5.45 to this candidate/DOI. It also attributed Kaempferol 10.2 to this DOI, although Kaempferol is absent from the original pure-compound table. Existing_Reference_Reconciliation.csv preserves the earlier numbers and the original-source finding. The updated diagnostic data use the original Quercetin row and exclude the unlocated Kaempferol association. The 2013 Catechin original mean is 10.59, consistent with the earlier rounded 10.6.

These corrections affect the interpretation of earlier 34-candidate reference models. Those outputs document the preceding analysis stage. The current manuscript-facing diagnostic uses the source-verified dataset in Step 03.6. Original observations and historical frozen assets retain their recorded contents.

## 2020 supplement and identity conflicts

Nine row-specific findings are in Source_Conflicts.csv. Table S1 gives Tangeretin 1.02 +/- 0.05, whereas section 3.1.1 explicitly gives 0.21 +/- 0.01 and Figure 1b shows the low value. For compounds 20 and 21, the S1 values also conflict with the visible point alignment in Figure 1b. Figure values have not been digitized or substituted. These three source rows are excluded from every updated model variant while their exact S1 numbers remain in the extraction.

Six additional issues concern structural annotations. Rutin's R3=Orha annotation overlaps with the annotation used for Quercitrin. Compound 27 is named Quercetin-3-O-rhamnoside but places Orha at R7, while compound 28 separately names Quercitrin. Vitexin places Cglc at R5 in the structural table. Isoorientin places it at R4 while S1 names Luteolin6-C-glucoside. Cynaroside's listed substituents omit a hydroxyl expected from the named reference. Hesperetin's listed hydroxyl/methoxy locants require reconciliation with the named standard. These are source-specific annotation findings. The name-based sensitivity retains the eligible named rows, and the recorded-conflict-excluded sensitivity removes all flagged source rows. Compound 27 is excluded throughout because its unresolved relationship to row 28 would create a duplicate candidate/source contribution.

The table maps provisionally to the parent references of current candidates. Chloride forms, named hydrates, sugar linkages and stereochemical details remain explicit qualification fields. Supplier catalogues, CAS or analytical material records can resolve these questions. The source's generic statement of dietary occurrence does not individually establish every proposed extension's food source.

## Protocol and replication

The 2020 ORAC method specifies 37 C and 60 two-minute cycles. The checked ORAC methods leave pH and final solvent unreported. The pH 7.5 in the cellular lysis-buffer section belongs to another experiment. Triplicate analyses and SD are reported, with independent preparation/day structure unresolved.

The 2013 methods report pH 7.4, 37 C, 50 mM phosphate, a three-hour FL recording and methanolic compound preparation. Catechin hydrate and quercetin dihydrate are named. Table 1 says mean +/- SD, n=3, while the methods describe triplicates and at least three independent experiments. The SD hierarchy and final methanol fraction remain unresolved. FL and PGR retain separate probe strata and outcome rows.

The 2001 assay uses pH 7.4 phosphate and a 37 C method with acetone/water compound stocks. Equation 2 explicitly includes the Trolox/sample molarity ratio. Table 4 says n>3 but leaves the displayed plus/minus statistic unresolved. The methods describe 30-minute readings while Equation 1 includes f35, so the integration window requires reconciliation. Vitamin C is reported as 0.95 +/- 0.02 in the FL column.

The 2004 methods specify pH 7.4, 37 C, 75 mM phosphate, 70 nM final FL, 12 mM final AAPH and an 80-minute window. Blank-normalized fluorescence is integrated, the blank AUC is subtracted, and concentration-response calibration gives molar TE values. Reactions are prepared in duplicate with at least three independent assays. Table 2 reports mean +/- SD, n=3. Final methanol fractions and exact material catalogues remain unresolved. The technical duplicates supply no additional independent n.

Across these reports, different laboratories and author groups support separate report clusters. The 2020 main article and supplement share one cluster, and the 2004 discussion's quoted 2001 values retain the 2001 cluster. Related-report and original-data reuse checks remain part of source qualification.

## References

Zhang Q et al. Identification of Six Flavonoids as Novel Cellular Antioxidants and Their Structure-Activity Relationship. Oxidative Medicine and Cellular Longevity. 2020:4150897. https://doi.org/10.1155/2020/4150897.

Zhang D et al. Relationship Between the Structures of Flavonoids and Oxygen Radical Absorbance Capacity Values. A Quantum Chemical Analysis. Journal of Physical Chemistry A. 2013;117:1784-1794. https://doi.org/10.1021/jp307746c.

Ou B, Hampsch-Woodill M, Prior RL. Development and Validation of an Improved Oxygen Radical Absorbance Capacity Assay Using Fluorescein as the Fluorescent Probe. Journal of Agricultural and Food Chemistry. 2001;49:4619-4626. https://doi.org/10.1021/jf010586o.

Davalos A, Gomez-Cordoves C, Bartolome B. Extending Applicability of the Oxygen Radical Absorbance Capacity (ORAC-Fluorescein) Assay. Journal of Agricultural and Food Chemistry. 2004;52:48-54. https://doi.org/10.1021/jf0305231.

Sharma OP, Bhat TK. DPPH antioxidant assay revisited. Food Chemistry. 2009;113:1202-1205. https://doi.org/10.1016/j.foodchem.2008.08.008.

## Tabart 2009 original-source update, 2026-11-13

DOI 10.1016/j.foodchem.2008.08.013 is recovered as an eight-page original report. Table 1 on PDF p6 (journal p1231) was visually checked against its 24 compound abbreviations and the Figure 1 legend on PDF p3. All 24 ORAC-column ratios are retained at their printed one-decimal precision. Trolox is the comparator and contributes no additional candidate row. Table 1 normalizes each assay to measured Trolox. Its ORAC ratios retain their source normalization explicitly. The four-method weighted average is a separate endpoint and supplies no ORAC model label.

Methods on PDF p2 report fluorescein/AAPH, 37 C, 200 microlitre reaction volume, 15-minute preincubation and two-minute readings over four hours. ORAC buffer pH and final methanol fraction are absent. PBS pH 7.4 belongs to the haemolysis/ESR descriptions and is not transferred to ORAC. The source states means +/- SEM from at least three independent experiments, with duplicate ORAC measurements at three dilutions. Table 1 contains no row errors and exact independent n is absent. Error fields remain empty. Figure error bars were not digitized.

Nineteen name-based mappings reach the existing candidate index and five remain identity/food-scope extension leads. Exact salt, hydration and stereochemical forms require source-material reconciliation. The 24 rows enter the original-source catalogue, with mapped rows eligible only for the expanded unknown-pH diagnostics. They do not enter the reported-pH-7.4 core. Source review remains NOT_REVIEWED and change_applied=NO.

Reference: Tabart J, Kevers C, Pincemail J, Defraigne JO, Dommes J. Comparative antioxidant capacities of phenolic compounds measured by various tests. Food Chemistry. 2009;113:1226-1233. DOI 10.1016/j.foodchem.2008.08.013.

## Tabart 2009 source update, 2026-11-13

DOI 10.1016/j.foodchem.2008.08.013 is recovered. The 24 ORAC ratios in Table 1 (PDF p6, journal p1231) were visually checked, with abbreviations from Fig1 (PDF p3). Nineteen rows map by name to the current index. Source ratios are normalized to measured Trolox and retain one-decimal precision. The four-assay weighted average is a separate endpoint.

Methods (PDF p2) report fluorescein/AAPH, 37 C, duplicate ORAC at three dilutions and two-minute readings over four hours. ORAC pH and final methanol are absent. PBS pH 7.4 refers to other assays. The source reports mean +/- SEM from at least three independent experiments, but Table 1 lacks row errors and exact n. Sampling variances remain blank. Source forms and stereochemistry remain qualification fields. Mapped rows enter the expanded diagnostics as one source block. The reported-pH core excludes this source. Review remains NOT_REVIEWED and change_applied=NO.

Reference: Tabart J et al. Comparative antioxidant capacities of phenolic compounds measured by various tests. Food Chemistry. 2009;113:1226-1233. DOI 10.1016/j.foodchem.2008.08.013.

## Targeted source follow-up, 2026-11-13

Gallocatechin currently has one independent numeric ORAC-FL source. The publisher full text for DOI 10.1155/2014/863984 was checked in sections 2.6 and 2.8. Section 2.6 reports tea-extract ORAC per gram dry tea, while section 2.8 measures individual catechins by online HPLC-DPPH at 521 nm. This source supplies no extracted independent pure-compound ORAC row in this pass. Publisher abstract DOI 10.1021/jf302477y concerns extract/film ORAC and chromatographic changes during oxidation. Pure-compound capacity extraction requires full methods and original tables; the abstract supplies no numeric model row.

Checked sources: https://onlinelibrary.wiley.com/doi/10.1155/2014/863984 and https://pubs.acs.org/doi/10.1021/jf302477y. Reading scopes were publisher full-text methods for the former and abstract for the latter.
