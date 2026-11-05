# Antioxidant Assay Method Audit

Version 1.0 (2026-09-17). This audit concerns chemical antioxidant capacity. It does not measure antioxidant effects in humans, clinical benefit, or in-vivo redox regulation.

## 1. Operational constructs

Antioxidant capacity is not one physical quantity. Hydrogen atom transfer (HAT) transfers H• to a radical and combines reaction rate with trapping stoichiometry. Electron transfer (ET/SET) depends on redox potential, pH, and solvent. Radical scavenging is an observed outcome that may arise through HAT, ET, proton-coupled electron transfer, addition, or other chemistry. Reducing power is the reduction of a metal/probe and does not equal chain-breaking. Peroxyl-radical chain-breaking intercepts propagating ROO•. Metal chelation prevents Fe/Cu-driven oxidation but can also perturb assays. Lipid-oxidation inhibition depends on intrinsic reactivity, partitioning, and interface location. Total radical trapping measures how many radicals are intercepted and/or the induction period. These constructs are not interchangeable.

The project operationally defines its primary chemical capacity as the molar-equivalent chain-breaking ability of a defined compound, relative to Trolox, to inhibit AAPH-derived peroxyl-radical oxidation of fluorescein under a locked ORAC-FL protocol, with net AUC reflecting both magnitude and duration.

## 2. Principal assays

### ORAC / ORAC-FL

ORAC is Oxygen Radical Absorbance Capacity. ORAC-FL uses fluorescein rather than the older beta-phycoerythrin probe. Thermal decomposition of AAPH generates a continuing peroxyl-radical flux that oxidizes fluorescein, decreasing fluorescence. Antioxidants delay that decay. Fluorescence is integrated over time and blank-corrected: `net AUC = AUC_sample − AUC_blank`; values within the linear range are compared with a Trolox calibration.

ORAC-FL is predominantly a competitive HAT/peroxyl-chain-breaking assay. PCET, secondary radicals, and probe-specific kinetics may contribute, so AUC is not a fundamental rate constant. Trolox is a water-soluble alpha-tocopherol analogue used for calibration, not a physiological-effect standard. For pure compounds, report `mol Trolox equivalents per mol compound (mol TE/mol)`. Published pure-compound data exist as µmol TE/µmol compound or convertible µmol TE/mg values when identity, purity, and molecular weight are known.

ORAC depends on AAPH, fluorescein, and Trolox concentrations; buffer and pH; temperature; pre-incubation and addition order; oxygen; plate position; reading interval and duration; AUC truncation; blank correction; concentration linearity; solvent/solubilizer; autofluorescence, inner-filter effects, and degradation. Values called ORAC in separate papers are not automatically combinable.

H-ORAC measures hydrophilic compounds in aqueous buffer. L-ORAC generally uses randomly methylated beta-cyclodextrin (RMCD) and organic cosolvent for lipophilic compounds; an interlaboratory-validated protocol exists, but it is not inherently on the same scale as H-ORAC. Different sources may enter one ranking only when radical generator, probe, pH, temperature, time sampling, AUC algorithm, calibration, concentration range, solvent/solubilization, and QC are equivalent and common bridging standards demonstrate acceptable bias. A single central-laboratory remeasurement is preferred.

Cross-class comparisons remain technically constrained. Soluble polyphenols fit H-ORAC; tocopherols and many carotenoids require L-ORAC. Carotenoids may aggregate, absorb or fluoresce, and react through addition or ET rather than canonical HAT. Tocopherol effectiveness also depends on lipid-phase localization. H-ORAC and L-ORAC should therefore be parallel, labeled primary arms rather than unconditionally pooled values.

### DPPH

DPPH• is a persistent colored nitrogen radical absent from physiology. Decolorization near 515–520 nm in methanol, ethanol, or another organic solvent can involve ET, HAT, or PCET. Solvent, pH, hydrogen bonding, steric accessibility, radical concentration, and time strongly influence results; bulky or slow compounds may be underestimated and colored/turbid samples interfere. Even with an AOAC method for specified foods, it lacks a universal cross-paper scale for pure compounds. Role: secondary fixed-protocol mixed-mode/ET reactivity screen.

### ABTS / TEAC

ABTS•+ is an artificial radical cation, usually pre-generated with persulfate and read at 734 nm. It accommodates broad polarity and Trolox normalization, but radical-generation route, residual oxidant, solvent, pH, and time alter mechanism and rank. It is not a physiological radical, and short endpoints underestimate slow compounds. Role: secondary broad-polarity ET/mixed-mode assay using a preformed-radical protocol.

### FRAP

FRAP reduces Fe(III)-TPTZ to colored Fe(II)-TPTZ at pH 3.6 and reads absorbance at 593 nm. It is an endpoint reducing-power assay, not radical scavenging or chain-breaking. Acidic pH, time, solubility, metal chelation, and color affect results, and slow/lipophilic reducers and some thiols are missed. Role: secondary reducing-power axis only.

### CUPRAC

CUPRAC reduces Cu(II)-neocuproine to Cu(I)-neocuproine near neutral pH, read near 450 nm. It accommodates thiols and, with suitable solubilization, lipophilic antioxidants better than FRAP. It remains reducing power, and copper coordination, solvent, and time matter. Role: preferred secondary ET complement; if resources force a choice, CUPRAC can precede FRAP, while FRAP remains useful for literature continuity.

### TRAP

TRAP measures total trapping or induction time against continuously generated peroxyl radicals, classically using an oxygen electrode and later luminol/fluorescent formats. It closely reflects chain-breaking and can report radicals trapped or Trolox equivalents, but heterogeneous detection and calculation limit comparability. Role: secondary mechanistic confirmation.

### HORAC, TOSC, and ROS-specific assays

HORAC measures prevention of hydroxyl-radical-like probe damage in Co(II)/Fenton-like systems and often mixes metal chelation with probe protection. TOSC integrates KMBA oxidation to ethylene by GC under peroxyl, hydroxyl, or peroxynitrite-generating conditions but is specialized and protocol-specific. Superoxide assays require controls for generator inhibition and probe redox cycling; hydroxyl assays must separate chelation from scavenging and preferably use EPR or specific products. These are supportive assays.

### Lipid-peroxidation inhibition

Liposome, LDL, emulsion, or oil oxidation models provide functionally relevant lipid-phase protection when using lag time, propagation rate, oxygen uptake, conjugated dienes, or validated oxidation products rather than TBARS alone. Partitioning, interfaces, lipid composition, oxygen, metals, and initiator can reverse rank. Use as a prespecified context-specific secondary assay, never numerically merge it with aqueous ORAC.

## 3. Unified ranking and comparability

Pure compounds can often be tested at known molarity, but molar conversion alone does not create comparability. Chemical form, stereochemistry, purity, reference, reaction conditions, concentration range, endpoint, and algorithm must match. A Trolox equivalent is assay-specific: DPPH-TE, ABTS-TE, and ORAC-TE are not interchangeable.

The primary ranking should be generated in one laboratory with a locked ORAC-FL SOP and reported as mol TE/mol compound. Published values belong in a literature-support layer. They become poolable only with complete protocol equivalence, adequate raw/QC data, common bridging standards, and acceptable interlaboratory bias. Routine meta-analytic pooling is inappropriate.

## 4. Primary, secondary, and supportive framework

Primary: the ORAC-FL family, with H-ORAC and validated L-ORAC as separate labeled arms. It is selected because it uses a continuous peroxyl-radical flux, measures competitive chain-breaking over a kinetic curve, integrates magnitude and duration, supports molar Trolox ratios, and has classic standardization guidance plus L-ORAC interlaboratory validation. Publication volume is not the reason.

Secondary: CUPRAC, ABTS-TEAC, DPPH, FRAP, TRAP, and one prespecified lipid-peroxidation model. They explain other mechanisms, anomalies, and application contexts; their raw values are not combined with ORAC.

Supportive: HORAC, TOSC, superoxide, hydroxyl-radical, metal-chelation, and other ROS-specific assays when the hypothesis and controls justify them.

Default z-score weighting or a multi-assay composite is not recommended. Assays measure different constructs; z-scores inherit cohort composition and missingness and can give noisy assays the same influence as validated ones. If a multidimensional summary is later required, use profiles or prespecified mechanism-domain scores with missingness sensitivity. Any exploratory composite must remain beside, not replace, the ORAC primary axis.

## 5. Compounds without ORAC data

Code missing ORAC as `not_measured`, never zero, and do not exclude the candidate. Retain secondary-assay, human, biological, food-exposure, and mechanism evidence and prioritize standardized remeasurement. If measurement is technically impossible, record insolubility, fluorescence interference, or instability and use an appropriate L-ORAC, TRAP, or lipid model as mechanism-specific evidence without imputing an ORAC rank. Report coverage and complete-case, missing-category, and no-chemical-domain sensitivity analyses.

## 6. Minimum ORAC-FL metadata

Freeze and report compound identity/form/purity; H- or L-ORAC; solvent and final fraction; RMCD type/concentration; buffer/pH; AAPH, fluorescein, and Trolox concentrations; temperature; addition order; plate/instrument and excitation/emission; read interval and duration; AUC/baseline formula; blanks, no-AAPH, solvent, autofluorescence and inner-filter controls; at least three sample concentrations and linearity criterion; within/between-plate CV; Trolox-curve acceptance; shared QC compounds; batch and operator. Suggested cross-class bridges are alpha-tocopherol, ascorbate, quercetin, and a carotenoid after solubility and optical validation.

## 7. Explicit conclusions

1. ORAC-FL is recommended conditionally as the primary chemical metric for harmonized project-generated data, never as a human-effect metric.
2. It is kinetic integrated inhibition of AAPH-derived peroxyl-radical oxidation of fluorescein under fixed conditions.
3. Report mol TE/mol compound plus raw concentration–net-AUC slope, confidence interval, and CV.
4. Do not directly pool ORAC values from different papers.
5. Pool only after protocol/entity/calibration/linearity/QC equivalence and bridging-standard validation.
6. DPPH: secondary fixed-protocol mixed ET/HAT reactivity.
7. ABTS: secondary broad-polarity artificial-radical ET/mixed mode.
8. FRAP: secondary acidic ferric reducing power.
9. CUPRAC: secondary preferred near-neutral ET/reducing-power complement.
10. TRAP: secondary peroxyl total-trapping confirmation.
11. No default multi-assay composite or z-score average.
12. Use H-ORAC/L-ORAC adaptations by class but report arms separately; carotenoids may also need lipid models.
13. Keep strong candidates without ORAC and prioritize remeasurement.
14. Treat missingness as unknown, not zero; never make ORAC an eligibility gate.
15. Primary chemical antioxidant capacity is peroxyl-radical chain-breaking under one ORAC-FL protocol, expressed as mol TE/mol, and does not imply in-vivo antioxidant effect.

## 8. Core references

Ou B et al. 2001, DOI 10.1021/jf010586o; Prior RL et al. 2003, DOI 10.1021/jf0262256; Prior RL et al. 2005, DOI 10.1021/jf0502698; Huang D et al. 2005, DOI 10.1021/jf030723c; Watanabe J et al. 2016, PMID 26860561; Schaich KM et al. 2015, DOI 10.1016/j.jff.2015.01.043; Re R et al. 1999, DOI 10.1016/S0891-5849(98)00315-3; Benzie IF & Strain JJ 1996, DOI 10.1006/abio.1996.0292; Apak R et al. 2004, DOI 10.1021/jf048741x; Wayner DDM et al. 1985, DOI 10.1016/0014-5793(85)81208-4; Murphy MP et al. 2022, DOI 10.1038/s42255-022-00591-z.
