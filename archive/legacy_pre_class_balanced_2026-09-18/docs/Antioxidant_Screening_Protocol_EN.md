# Screening Protocol for Common Food-Derived Antioxidant Small Molecules (Phase 0–1)

Version 1.0 (2026-09-17); status: submitted for investigator review and not yet used for formal ranking.

## 1. Objective and scope

The project will identify common food-derived antioxidant small molecules with the strongest combined scientific value, human relevance, and potential for mechanistic and target research. Candidate sources cover normal diets worldwide; exposure is recorded by country, region, population, and food form. The primary reference is dietary-achievable exposure in generally healthy adults. Evidence in patients and high-risk populations is retained with explicit applicability labels. Antioxidant activity is defined broadly but separated into `direct_antioxidant`, `redox_regulatory`, and `indirect_redox_related`. An indirect pathway effect counts as antioxidant evidence only when accompanied by a credible redox or oxidative-damage endpoint.

Phase 0–1 freezes methods, fields, and source priorities only. It does not produce the Top20 or perform bulk target extraction.

## 2. Candidate entities and list layers

A main-list entity must be a parent small molecule naturally present in ordinary foods, beverages, or common spices; have a uniquely resolvable structure and a PubChem CID or an auditable equivalent structure identifier; and have at least one quantitative food-occurrence record. Compounds obtained mainly from medicinal plants or supplements, endogenous antioxidants, human metabolites, mixtures, polymers, mineral elements, and structurally unresolved entities enter an extended or secondary list. Salts, solvates, tautomers, stereoisomers, and glycoside/aglycone forms are not merged by name alone; standardized structures and explicit parent–form links are required.

Each parent compound has a metabolite subtable covering major absorbed/circulating metabolites, phase-II conjugates, and gut-microbiota-derived metabolites. Metabolites do not compete with parents in the main ranking, but may enter the secondary candidate list when human exposure, activity, and target evidence are substantial.

## 3. Candidate-universe generation

Generation uses a multi-source union followed by structure deduplication and evidence gates:

1. Extract single-structure food constituents from Phenol-Explorer, USDA flavonoid/special-interest datasets, FoodData Central, FooDB, and authoritative regional composition resources. Add cross-class candidates from carotenoids, tocopherols/tocotrienols, organosulfur compounds, betalains, quinones, nitrogen-containing phytochemicals, and other food-derived molecules with redox evidence.
2. Resolve names, synonyms, CID, InChIKey, SMILES, formula, mass, and stereochemistry with PubChem and ChEBI; retain source identifiers and mapping methods.
3. The main-candidate universe requires `structure_resolved=yes`, `normal_diet_occurrence=yes`, at least one traceable food record, and no exclusion condition. Detection without interpretable concentration may enter with `exposure_status=trace_or_unknown` but cannot receive a high exposure score.
4. Estimate realistic exposure from food concentration multiplied by region-specific consumption. When consumption is unavailable, report concentration only. Preserve food form, processing, method, wet/dry basis, and glycoside/aglycone conversions.
5. A database hit supports candidate generation only; it does not establish a biological effect, direct target, or clinical benefit.

Exclude unresolved structures, entities whose principal source is not normal food, endogenous substances and human metabolites from the main layer, entities without credible food provenance, and evidence based only on uncharacterized extracts. Lack of human evidence, lack of a direct target, and safety uncertainty are not early hard exclusions.

## 4. Search and evidence inclusion

Use separate search tracks for food occurrence/content, human effects, human PK/metabolites, animal/cellular redox evidence, mechanism, direct targets, safety, and combinations. Store database/platform, complete query, date, date range, filters, result count, and export file in accordance with PRISMA-S reproducibility principles. PubMed is the main biomedical source; Crossref completes DOI metadata but is not an effect-evidence source.

Formal evidence must trace to an original paper or authoritative database. Reviews identify studies and provide context but do not replace primary evidence except for methodological consensus. Multiple reports from one trial, cohort, or dataset form one evidence family and are not counted repeatedly.

## 5. Hierarchies and quality adjustment

Operational definitions for H1–H6, A1–A5, M1–M5, and T1–T5 are in the scoring rubric. Study design supplies a starting tier; risk of bias, endpoint validity, dose relevance, and replication may downgrade it. Use RoB 2 for RCTs, ROBINS-I V2 for non-randomized interventions, and a prespecified domain-based assessment for observational studies. Body-of-evidence confidence follows GRADE domains without mechanical numeric conversion.

Preferred endpoints include validated F2-isoprostanes, oxidative DNA/protein/lipid damage markers, GSH/GSSG, and specific ROS measured with validated methods. MDA/TBARS, total antioxidant capacity, and nonspecific fluorescent probes require downgrading. SOD/CAT/GPX expression alone does not establish antioxidant improvement. DPPH, ABTS, FRAP, and ORAC are A5 evidence only and values cannot be ranked across assays.

## 6. The 100-point framework

The baseline weights are Human relevance 25, Antioxidant biological evidence 25, Food exposure 20, Mechanistic evidence 15, and Direct-target evidence & tractability 15. Each domain produces a 0–1 score multiplied by its weight. `not_searched`, `searched_none`, `conflicting`, and `not_applicable` remain distinct states.

The highest credible tier establishes the base score. Independent replication, cross-model consistency, and exposure matching give bounded increments. Publication volume is capped: the first independent evidence family supplies the base score, families 2–3 add no more than 10% of the domain maximum, and later families add nothing. Accumulated lower-tier evidence cannot cross the minimum score of the next tier. High risk of bias, absent orthogonal validation, clearly supraphysiological dosing, or parent-compound/Cmax mismatch causes downgrading or a translation penalty.

Proposed within-domain anchors are Human 1.00/0.85/0.65/0.45/0.35/0 for H1–H6 (H5 supports exposure, not benefit); Antioxidant 1.00/0.75/0.50/0.25/0.10 for A1–A5; Mechanism 1.00/0.75/0.50/0.25/0.10 for M1–M5; and Target/tractability 1.00/0.85/0.60/0.30/0.10 for T1–T5. Food exposure combines quantitative content, consumption frequency, regional coverage, estimated intake, and data quality; occurrence-only evidence is capped at 0.20.

| Scheme | Human | Antioxidant | Food | Mechanism | Target/tractability |
|---|---:|---:|---:|---:|---:|
| Original baseline | 25 | 25 | 20 | 15 | 15 |
| Human-prioritized | 35 | 25 | 20 | 10 | 10 |
| Exposure-balanced | 25 | 20 | 30 | 15 | 10 |
| Experimental-translation-prioritized | 20 | 20 | 15 | 20 | 25 |

The original baseline is proposed as the preregistered main analysis and the other three are genuinely distinct sensitivity schemes. Later analyses report Top20 inclusion frequency, median rank/IQR, Spearman/Kendall correlation, and rank acceptability under weight perturbation, with a separate missing-data sensitivity analysis. Safety/dose window remains a risk flag and tie-breaker rather than an early score, so lack of knowledge is not mistaken for safety.

## 7. Exposure, bioavailability, and dose translation

Store original food, processing state, geography, analytical method, center/range, unit, wet/dry basis, consumption, estimated intake, and uncertainty. Food occurrence does not imply meaningful exposure. Record parent and metabolite Cmax, AUC, matrix, and time separately. The ratio between effective free in-vitro concentration and plausible human systemic exposure defines `dose_translation_gap`; a large gap retains the result but reduces translational relevance.

## 8. Safety and context interactions

Record typical dietary exposure, intervention dose, in-vitro concentration, Cmax, adverse-effect threshold, UL, special-population risk, drug interactions, metal dependence, hormesis, prooxidant transition, and safety grade. Absence of a UL is not evidence of safety. Synergy or antagonism requires a stated null model (Bliss, Loewe, CI/isobologram, ZIP, or equivalent), dose matrix, replication, and uncertainty. Descriptive co-treatment is labeled only `possible_synergy` or `possible_antagonism`.

## 9. Data management and reproducibility

Tables use UTF-8 CSV, stable snake_case fields, ISO 8601 dates, and explicit missing-reason codes. Every evidence row stores PMID, DOI, database record, retrieval date, Zotero item key, and BibTeX key. Raw exports remain read-only, cleaning scripts are versioned, and manual judgments retain reviewer, date, rationale, and second-review status. Critical inclusion and tier calls require dual review, with disagreements resolved by consensus or a third reviewer.

## 10. Phase boundary

Work stops when this protocol, the rubrics/dictionaries, source audit, decision log, handoff, and internal audit are complete. The recommended sequence is Phase 2A polyphenol-first universe; 2B cross-class expansion; 2C evidence extraction and preliminary scoring; 2D sensitivity and rank stability; 2E provisional Top20; and Phase 3 EGCG pilot target extraction. Scoring implementation, missing-data rules, and search cut-off must be frozen before ranking.

## 11. Core methodological sources

- Murphy MP et al. *Nature Metabolism* 2022;4:651–662. DOI: 10.1038/s42255-022-00591-z; PMID: 35760871.
- Rethlefsen ML et al. *Systematic Reviews* 2021;10:39. DOI: 10.1186/s13643-020-01542-z.
- Sterne JAC et al. RoB 2; ROBINS-I V2 (2025 release); GRADE/Cochrane Handbook.
- Mateus A et al. *Annual Review of Pharmacology and Toxicology* 2022;62:465–482. DOI: 10.1146/annurev-pharmtox-052120-013205.
- Ianevski A et al. *Nucleic Acids Research* 2022;50:W739–W743. DOI: 10.1093/nar/gkac382.
