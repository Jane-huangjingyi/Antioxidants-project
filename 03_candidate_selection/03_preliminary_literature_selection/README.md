# 03.3 Preliminary literature preselection

Start with [candidate review](results/Preliminary_Candidate_Review.csv): one row per current candidate, reference chemical identity, food-source status, material/procurement gaps and links to capacity sources. Then inspect [individual capacity references](results/Linked_Capacity_Source_References.csv): DOI, original locator, value, scale, error and comparability status are retained. CSV line numbers include the header as line 1. Neither table supplies potency scores or inclusion approval.

This first view covers 193 current profiles and the existing 99-row Capacity_Analysis_Entry reference table, linked to 48 candidates. The other 145 have no link in this particular table; this is not an exhaustive search result or evidence of inactivity. The 12-profile method-development panel is flagged separately from potency selection. Legacy confirmed-study counts retain their original scope and are not recomputed as independent-study counts from these reference rows.

Coverage boundary: the [152-row analysis disposition](../01_activity_model/results/Analysis_Set_Decisions.csv), [new cross-structure source checks](../02_cross_study_expansion/results/Cross_Structure_Evidence_Expansion.csv), and single-paper structural-model diagnostics remain separate scientific records. This preliminary join is not a replacement for those records, a complete merged evidence universe or a release of model labels. Primary-source checks and protocol harmonization are still required. Formula/CID presence does not verify purchased stereochemistry, salt/hydrate, purity or lot. Food examples at class level are not candidate-specific food-occurrence verification.

Review candidate-specific food evidence and exact material form first. For source-linked candidates, inspect original values, scales, protocols, uncertainty and duplicate/data-generation relationships before assigning a comparable activity summary. Retain missing values and source HOLDs. A preliminary review order is not a potency rank; a final experimental Top20 needs validated endpoint measurements and justified comparison/model performance.

Reproduce from the project root:

```sh
python 03_candidate_selection/03_preliminary_literature_selection/build_preselection.py
```

The script checks unique candidate IDs, complete mapping of the 99 reference rows and empty potency fields. [QC](results/preselection_qc.json) records input hashes and counts. All human-review states remain NOT_REVIEWED and changes remain unapplied. No new full texts, experiments or scientific approvals were generated.

## Existing food and material follow-up

The candidate view now carries existing food follow-up for 17 candidates and source-material annotations for three candidates. No new source reading is asserted. Food follow-up statuses/DOIs are directly readable; JSON records retain each status, DOI, locator and boundary together instead of flattening them into an apparent approval. Material records retain CAS, reported purity, source DOI and scope; these describe the specified source material, not purchased lots. The linked evidence table preserves all corresponding annotation fields.

Abstract occurrence support, indexed-source leads, original-table support and failure to establish native free-aglycone occurrence remain distinct. Hydrolysis-derived detection does not automatically establish native free-compound occurrence; positional isomers require nomenclature matching. None of these annotations overrides the original food-source status or HOLDs. This is reconciliation of existing annotations, not approval of the 17 candidates.

## Form-specific review queue

Run `python 03_candidate_selection/03_preliminary_literature_selection/review_food_forms.py` for the [17-candidate form review](results/Food_Form_Review.csv). Six candidate/source links were checked against selected passages in two original sources; eleven retain prior annotations without a claim of new source reading. The enzyme-generated eriodictyol preparation does not establish native free-food occurrence (DOI 10.3177/jnsv.52.54, publisher abstract). The coffee study reports positional CQA/diCQA analytes; exact candidate-structure nomenclature remains to be matched (DOI 10.1016/j.jare.2019.01.002, reagents, preparation, Figure 1 and Table 2). No food concentration is imported as capacity, and no material eligibility is released. These scope decisions are preparation for scientific adjudication, not a new search across all 193 candidates.

## Positional identifier cross-check

The checked coffee-source CAS links 906-33-2 and 905-99-7 correspond to current reference CIDs 5280633 and 9798666. The form-review builder verifies those IDs against current profiles and exposes the source analyte, CAS and identity URL. Neochlorogenic-acid synonyms contain alternative positional naming, so source numbering and structure review remain explicit. The other three diCQA mappings still require source-to-structure correspondence. Source notes are stored in `inputs/positional_identity_check.json`. The honey publisher PDF returned HTTP 403 on this check; its complete preparation method remains pending.

## Exploratory literature reference order

Run `python 03_candidate_selection/03_preliminary_literature_selection/build_reference_order.py`. The [reference order](results/Exploratory_Literature_Reference_Order.csv) includes 44 candidates and 69 candidate-paper summaries from explicit nonnegative molar-capacity entries. The method takes the median of reference rows per candidate and DOI, then the unweighted median across those paper summaries. Ties share competition positions. This descriptive choice is project-defined and gives every paper summary equal influence. Repeated reference rows are not treated as independent experiments.

Source protocols and estimands remain heterogeneous. The cross-protocol median is an exploratory literature-navigation statistic whose biological or assay-specific predictive performance is unestablished. Interpret it alongside source count, range, food/material status and the [paper-specific order](results/Paper_Specific_Reference_Order.csv). A within-paper order also needs executed-protocol confirmation. Single-paper entries can appear high and are visible as such. Thirty records with other scales, conditional conversion or invalid/source-HOLD entries remain in the [exclusion table](results/Reference_Order_Excluded_Rows.csv). Missing candidates receive no rank. Formal screening-model performance, experimental eligibility and final Top20 require the pending scientific and experimental checks. No new measurements or approved states were generated.

## Priority-source comparability

Run `python 03_candidate_selection/03_preliminary_literature_selection/build_priority_evidence.py` after generating the detection assessment. The [priority source table](results/Priority_Source_Comparability.csv) joins the 28-candidate review subset to existing analysis dispositions through candidate ID, preserving each unique analysis record. All 28 map to 81 provenance rows, comprising 59 waiting, 12 sensitivity and 10 reference-only rows. Record counts include alternate representations and do not indicate independent measurements. Primary-eligible rows currently total zero under the existing fixed literature target gates. This extraction adds no new source reading or quality approval. It makes unresolved pH, temperature, vehicle, estimator, integration-window, identity and variance annotations directly inspectable for the candidate-selection task.

## Source influence and targeted recovery

Run `python 03_candidate_selection/03_preliminary_literature_selection/diagnose_source_influence.py` after building the reference order. The [source-omission diagnostic](results/Source_Omission_Order_Diagnostic.csv) recomputes descriptive medians and positions after omitting each DOI in turn. Candidate coverage can change between scenarios. The table records the number of scenarios without a remaining source and the position range among supported scenarios. These deterministic ranges describe source influence. Statistical confidence intervals and Top20 probabilities still require a justified uncertainty model.

Targeted source check on 2026-11-11 located Tabart et al. in the author institution repository, https://orbi.uliege.be/handle/2268/3247 (DOI 10.1016/j.foodchem.2008.08.013). The record provides a request-copy route and an abstract covering several assays. The original numeric comparison table and error definition remain unrecovered in this check. Zhang et al., DOI 10.1021/jp307746c, was checked through the original abstract at https://pubmed.ncbi.nlm.nih.gov/23343226/. It describes 13 flavonoids and both FL/PGR probes. The ACS full-page request returned 403. The underlying numerical values, error definition, exact protocol and data-generation independence still require full-text checks. No new source values or variances were released.

## Fixed-universe source sensitivity

The source-omission diagnostic now also reports possible-order bounds while retaining the original 44-candidate universe. When source omission leaves a candidate unsupported, its position can range across the full universe. For supported candidates, unobserved competitors can fall above or below them. These worst-case bounds supplement the supported-subset positions and expose the consequences of missing evidence. They represent deterministic coverage bounds. They have no statistical confidence level. The detection assessment now joins these bounds and unsupported-scenario counts by candidate ID. Reproduce in order with `diagnose_source_influence.py`, then `build_detection_queue.py`.
