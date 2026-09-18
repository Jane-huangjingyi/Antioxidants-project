# Antioxidant Screening Protocol v2.0 (English)

**Version:** 2.0  
**Status:** Pending researcher/ChatGPT review; formal ranking must not begin before approval and freezing  
**Scope:** Common food-derived, structurally defined, naturally occurring parent small molecules

## 1. Objective and unified standard

The project separates two scientific questions. Stage 1 compares chemical antioxidant capacity only. Stage 2 evaluates human relevance and experimental translation. The two outputs must be reported separately; a Stage 2 composite must not replace or be called an “antioxidant-capacity ranking.”

**Supervisor-ready standard:** Methodologically comparable ORAC-FL data are the primary basis for ranking the chemical antioxidant capacity of food-derived single compounds and are expressed as mol Trolox equivalents/mol compound (mol TE/mol); CUPRAC and related assays supplement other reaction mechanisms, while human exposure, bioavailability, mechanism, target, and safety evidence inform a separate second-stage translational priority assessment.

## 2. Inherited and frozen scope principles

1. The main list includes only structurally unique parent small molecules naturally present in foods, beverages, and common culinary spices consumed in normal diets.
2. Polyphenols are generated first but receive no class quota. Eligible classes include polyphenols, carotenoids, tocopherols/tocotrienols, organosulfur compounds, betalains, quinones, and nitrogen-containing phytochemicals.
3. Human metabolites do not compete with parent compounds on the main list, but major absorbed/circulating conjugates and gut-microbiota-derived metabolites must be recorded. Metabolites with independent exposure and activity evidence enter a secondary candidate list.
4. Evidence quality outranks publication count. The number of studies within a tier provides capped support and must not create popularity bias.
5. Direct-target evidence is not an early inclusion gate; the T1–T5 target classification is unchanged.
6. Safety/dose window is a risk and translation dimension, not an early hard exclusion gate. A severe, authoritatively established safety risk can trigger separate review.
7. Synergy, antagonism, and food-matrix interactions are second-layer contextual evidence and do not define the intrinsic chemical capacity of a single compound.
8. Human PK/bioavailability and human efficacy are recorded and graded separately.

## 3. Two-stage system

### 3.1 Stage 1: Chemical Antioxidant Capacity Ranking

Stage 1 asks: “Under comparable conditions, which structurally defined food-derived single compounds have stronger chemical antioxidant capacity?”

The primary metric is ORAC-FL. Its operational definition is: **the kinetically integrated chain-breaking capacity of a structurally defined compound against fluorescein oxidation initiated by AAPH-derived peroxyl radicals under locked or methodologically comparable ORAC-FL conditions, expressed as mol TE/mol compound.**

This is a peroxyl-radical-related, kinetic integrated capacity measured in a chemical system. It does not represent antioxidant effects in humans, clinical benefit, bioavailability, cellular redox regulation, or final experimental priority.

### 3.2 Stage 2: Translational Prioritization

Stage 2 asks: “Among candidates with strong chemical capacity or other important potential, which deserve further nutritional-intervention, mechanistic, and target-protein research?” It produces **Translational Priority** and must not be called an antioxidant-capacity ranking.

Stage 2 separately evaluates human evidence, dietary exposure, bioavailability/dose translation, biological redox evidence, mechanistic evidence, direct-target evidence, experimental tractability, and safety/prooxidant risk, while recording major human metabolites and context interactions. Stage 1 rank does not automatically determine Stage 2 rank, and Stage 2 must not rewrite Stage 1 chemical-capacity values.

## 4. Methodological boundaries of ORAC-FL

ORAC denotes oxygen radical absorbance capacity. ORAC-FL uses fluorescein as the probe, usually generates peroxyl radicals continuously through thermal decomposition of AAPH, and uses Trolox for calibration. The difference between sample and blank fluorescence-decay areas gives net AUC, which is converted to Trolox equivalents within a validated linear range.

The recommended unit is `mol Trolox equivalents/mol compound`. Mass-based units may be converted only when compound identity, molecular weight, salt/hydrate form, and stoichiometric basis are explicit. Food-level ORAC, such as µmol TE/100 g food, must not be used to rank single compounds.

H-ORAC and L-ORAC must be recorded as different assay arms. H-ORAC suits aqueous-soluble systems. L-ORAC commonly relies on acetone, cosolvents, or randomly methylated β-cyclodextrin (RMCD). Their solvent, mass-transfer, aggregation, and calibration behavior differs; without bridging validation, they must not be assumed to share a scale or be ranked together.

## 5. Literature-derived ORAC comparability framework

Each record is assessed against `config/ORAC_Literature_Eligibility_Rubric.csv` before tier assignment:

- **Tier A (highly comparable):** Compound identity, form/stereochemistry, purity, ORAC-FL type, H/L arm, AAPH, fluorescein, Trolox, buffer/pH, temperature, solvent/solubilizer, reading interval and duration, AUC calculation, concentration linearity, and unit conversion can be verified; no unresolved critical incompatibility or interference is present. Eligible for the primary numerical ranking.
- **Tier B (partly comparable):** The target compound and ORAC-FL method, arm, Trolox reference, and molar conversion are identifiable; a small number of noncritical parameters are missing or differ explainably. Provides supportive quantitative evidence but cannot decide close ranks.
- **Tier C (incomparable):** A known incompatible probe/radical/protocol, food/extract-level unit, unrecoverable mass normalization, unvalidated H/L mixing, material interference, or another unbridgeable condition is present. Retained only as qualitative literature support.
- **Tier X (insufficient information):** ORAC is reported but methods are insufficient to assign A/B/C. Retained pending information retrieval and excluded from numerical ranking.

The maximum ORAC value from each paper must not be selected. Values from different protocols must not be concatenated directly. Duplicate publications of the same experiment do not count as independent evidence.

## 6. Stage 1 aggregation and ranking rules

1. Only Tier A records enter the primary numerical ranking by default; Tier B records are listed separately as directional support.
2. Multiple Tier A records are first checked for compound form, H/L arm, protocol family, concentration linearity, and study independence.
3. When sufficiently homogeneous, the study-level median is the central estimate and the range is reported; add the IQR when enough records exist. Never use the maximum.
4. When heterogeneity is explainable, stratify by assay arm, compound form, or protocol family rather than calculating a misleading pooled value.
5. When values are close and uncertainty overlaps, report ties or rank bands; do not force separation with Tier B or lower-level assays.
6. H-ORAC and L-ORAC may be combined only when prespecified bridging studies demonstrate measurement equivalence, calibration consistency, and acceptable error. Otherwise, publish arm-specific rankings.
7. The Stage 1 table contains at least: rank, compound_name, PubChem_CID, InChIKey, chemical_class, ORAC_arm, ORAC_value_mol_TE_per_mol, ORAC_source, ORAC_comparability_tier, number_of_eligible_ORAC_studies, median_ORAC, ORAC_range, ORAC_confidence, CUPRAC_available, CUPRAC_value, secondary_assay_summary, and notes.

## 7. Missing ORAC data

Missing ORAC data must not be coded as zero, used for exclusion, or interpreted as low chemical capacity. Use `not_measured` or `insufficiently_comparable`. Retain CUPRAC, DPPH, ABTS, FRAP, human, mechanistic, food-exposure, and target evidence, and place the candidate on the **ORAC measurement priority list**. When Stage 1 coverage is inadequate, only a `provisional Chemical Antioxidant Capacity Top20` may be issued, together with coverage and missingness patterns.

## 8. Secondary and supportive assays

Different assays measure different antioxidant constructs. Simple averaging of ORAC, DPPH, ABTS, and FRAP, or default z-score weighting, is prohibited.

| Assay | Formal role | Interpretation boundary |
|---|---|---|
| CUPRAC | Preferred secondary orthogonal assay | ET/reducing power; not equivalent to peroxyl chain breaking |
| ABTS/TEAC | Secondary broad-polarity artificial-radical response | Artificial radical cation; strongly medium- and time-dependent |
| DPPH | Secondary fixed-protocol mixed ET/HAT reactivity | Nonphysiological radical; solvent-, steric-, and endpoint-time-sensitive |
| FRAP | Secondary ferric reducing power | Reducing-power endpoint; does not demonstrate radical chain breaking |
| TRAP | Secondary confirmation of peroxyl-radical trapping | Conceptually related to ORAC but not equivalent in probe, kinetics, or calculation |
| Lipid-peroxidation inhibition | Context-specific secondary evidence | Supports lipid/food settings; strongly substrate- and oxidation-condition-dependent |
| HORAC, TOSC, superoxide, hydroxyl-radical, metal-chelation assays | Supportive only | Mechanistic supplementation and outlier interpretation; excluded from primary ranking |

For multidimensional display, use radar/profiles, mechanism-specific domains, and concordance analysis. A composite may be explored only after preregistering the construct and scale and externally validating it; it cannot replace Stage 1.

## 9. Cross-class comparability and arm-specific strategy

- **Polyphenols:** Most are suitable for H-ORAC, but glycosylation, polymerization, oxidation, pH dependence, autofluorescence, and quenching require checks; poorly soluble members may require defined cosolvents.
- **Tocopherols/tocotrienols:** Their lipophilicity usually requires L-ORAC. RMCD inclusion and isomer identity can alter apparent reactivity; default mixing with H-ORAC is invalid.
- **Carotenoids:** These usually require lipid/solubilized systems and are sensitive to dissolution, aggregation, photodegradation, oxygen tension, absorbance, and fluorescence inner-filter effects. ORAC-FL may underestimate or distort their activity; blanks, spectral checks, recovery QC, and arm-specific reporting are required.
- **Organosulfur compounds:** Their main redox actions may depend on thiol exchange, electrophilicity, or enzyme regulation and need not produce strong peroxyl chain breaking. A low ORAC value does not establish low redox relevance.

If cross-arm equivalence cannot be validated, publish separate H-ORAC and L-ORAC rank tables with an explicit statement that safe cross-arm comparison is unavailable. Do not force a single Top20.

## 10. Stage 2 translational priority

The v1.0 25/25/20/15/15 framework is renamed the legacy `Translational Priority Score` and is retired from generating the chemical Top20. v2.0 first uses an eight-domain profile and freezes weights only after the pilot: human evidence; dietary exposure; bioavailability/dose translation; biological redox evidence; mechanistic evidence; direct-target evidence; experimental tractability; and safety/prooxidant risk. Initial sensitivity-analysis weights of 20/15/15/15/10/10/10/5 are proposed, not treated as ground truth. Domain scores, missingness, risk flags, and rank stability under alternative weights must be reported.

Human PK enters only the bioavailability/dose-translation domain and cannot be upgraded to efficacy. The safety domain records dose window, UL/authoritative limits, special-population risks, hormesis, metal environment, and antioxidant-to-prooxidant transition. It modifies risk and study design but ordinary missingness is not an early exclusion rule. Major metabolites are mandatory annotations for bioavailability and mechanism interpretation. Context interactions are recorded separately and do not alter intrinsic ORAC values.

## 11. Target evidence remains unchanged

T1 is direct biochemical/biophysical binding; T2 is cellular target engagement/chemical proteomics; T3 is functional target validation; T4 is a regulated/pathway-associated protein; and T5 is a predicted target. Only T1/T2 enter the high-confidence direct-target layer. T3 is labeled functional target, T4 regulated/pathway-associated, and T5 predicted. Changes in Nrf2 or NF-κB activity, expression, phosphorylation, or nuclear translocation do not establish direct binding.

## 12. Naming the two Top20 outputs

- **Chemical Antioxidant Capacity Top20:** Generated only from eligible Stage 1 ORAC-FL data; labeled `provisional` when coverage is inadequate.
- **Translational Priority Top20:** Generated from Stage 2 multidomain evidence and represents research priority, not chemical antioxidant capacity.

The lists may overlap but must not be merged into an undefined “overall antioxidant Top20.”

## 13. Provenance and quality control

Each formal record retains the original unit, conversion equation, PMID, DOI, Zotero key, exact table/figure/supplement location, extractor, and review status. A second reviewer or automated validation rule checks numerical conversions. Required checks include identity/stereochemistry, salt/hydrate form, purity, molecular weight, H/L arm, linearity, optical interference, duplicate publication, nonindependent within-study data, and selective reporting.

Before ranking is frozen, audit whether Stage 1/2 names are confused; ORAC is extrapolated to human effects; protocols or H/L arms are combined unconditionally; missingness is coded as zero; a default composite is created; T1–T5 tiers are mixed; safety, metabolites, and interactions are retained; and cross-class coverage introduces systematic bias.

## 14. Next-stage pilot (proposed, not executed here)

Conduct an **ORAC Literature Ranking Pilot** with 10–20 representative compounds across classes. It should cover representatives of catechin/EGCG, quercetin, phenolic acids, stilbenes, tocopherols, carotenoids, vitamin C, and organosulfur compounds, but the final set follows candidate-universe coverage and traceability rather than a mechanically fixed list.

The pilot sequence is: search and deduplicate; record-level extraction; A/B/C/X grading; H/L separation; conversion verification; Tier A median and heterogeneity assessment; CUPRAC coverage check; and assignment of missing candidates to the measurement-priority list. The output determines whether existing literature can support a formal Top20 and which compounds require standardized retesting. The pilot must not begin before this protocol is reviewed.

## 15. Stop condition

This round freezes only the v2.0 methodological structure and data specifications. It does not generate a Top20, batch-extract ORAC or targets, modify the knowledge graph, execute Stage 2 ranking, or perform experiments. The project waits for researcher and ChatGPT review before the pilot.
