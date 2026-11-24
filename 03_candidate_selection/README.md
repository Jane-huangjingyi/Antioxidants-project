# 03. Harmonize capacity data and prioritize candidates

Start with the [latest original-source extraction and rank diagnostics](11_orac_fulltext_followup/README.md). Candidate data move from a source-located raw observation to a molar ORAC-FL value only when chemical form, units and conditions support the intended comparison. Separate sensitivity analyses show protocol, source and reported-variance effects. The [working Methods](../06_manuscript/01_methods_working.md#numeric-analysis-and-decision-rule) specifies the primary model and the pending numeric decision rule. For underlying supplied PDF corrections, see the [source reconciliation](../02_identity_and_evidence/02_user_supplied_sources/Existing_Reference_Reconciliation.csv).

**Run and read.** Run `code/01_fit_orac_fl.py` followed by `code/02_validate_and_rank.py` after the literature screen. The [model input](result/table/01_connected_model_input.csv), [harmonized observations](result/table/02_harmonized_observations.csv) and [rank sensitivity](result/table/03_rank_sensitivity.csv) are the main tables. Read the [whole-DOI diagnostics](result/model/02_whole_doi_validation.json) before interpreting the rank. Source weights and variability details are under `result/table/audit/`.

**Handoff.** The [current ranking table](result/table/04_figure1_candidate_ranks.csv) retains compounds within ±10 positions of their expanded conditional ORAC-FL rank across model scenarios and conservative whole-DOI deletion bounds. Hold compounds beyond this limit or unavailable in a deletion. The absolute rank is unrestricted. Send the retained candidates and their evidence records to [04–05 experimental validation](../04_05_experimental_validation/README.md) for material and assay qualification.

## Reviewed evidence updates

The [compound evidence inclusion table](result/table/05_compound_evidence_inclusion.csv) lists all 193 profiles. Name-link counts describe machine-matched records, and the same report may be linked to several compounds. A logged scope records source work associated with a matched report. It does not establish that the report measured that compound. Model observations and unique DOI counts use the actual conditional fit. Historically confirmed independent H-ORAC studies are reported separately because they refer to a different evidence set.

The [rank comparison table](result/table/06_round_rank_comparison.csv) uses commit `e4c300c` as the first-round baseline. The [targeted follow-up](12_evidence_expansion/README.md) records sixteen held observations and one external single-compound diagnostic. Updated ranks and rank differences are blank until a new fit is available.

Run `python 03_candidate_selection/code/05_build_evidence_round_tables.py` from the repository root. The script uses the local queue produced by `02_identity_and_evidence/code/04_build_fulltext_batches.py` for compound-level scope counts. Those two columns are left blank when the queue is unavailable. After reviewing and fitting an updated evidence set, rebuild the Figure 1 candidate rank table, commit that snapshot and rerun with `--updated-ref <commit>`. Positive rank changes indicate movement to a lower position. Interpret changes alongside the number of ranked compounds and source-deletion status in each round.

Copy the [intake template](../02_identity_and_evidence/inputs/templates/evidence_update_intake.csv) into a working directory. Give each original measurement a stable ID, DOI, first-public date, source locator, material, unit, endpoint and protocol. Record the six scientific eligibility decisions. The comparison tool only accepts rows marked `APPROVED_FOR_NEXT_ANALYSIS` with all six gates passed. Connected ORAC-FL analysis additionally requires `APPROVED_CONNECTED_FL`, a positive molar estimate with a reviewed conversion basis, and a compound linked to the baseline.

```sh
python 03_candidate_selection/code/03_update_evidence.py --intake reviewed.csv --out download_raw/results1_next_review --cutoff 2026-11-17
```

Use a new output directory and record the cutoff for each cycle. The command compares eligible new evidence against the [frozen Results 1 reference](../02_identity_and_evidence/inputs/provenance/results1_v1.0/README.md). It writes ranks, holdout diagnostics and review flags. It does not apply panel decisions. Correction or removal of a baseline row requires a separately versioned evidence record.

## Earlier experimental review panel

For the researcher-selected objective of highest expected molar chemical capacity, start with [Step 03.1: activity-model preparation](01_activity_model/README.md). The queue below remains a historical preparation baseline and is not a fitted capacity ranking.

Run `python 03_candidate_selection/code/select_candidates.py`. Rules are in `config/selection_rules.json`; the researcher-editable decision table is `config/researcher_decisions.csv`. Rebuilding preserves the decision table. Empty fields remain unknown.

The review queue requires reference identity/formula, retained molecular food scope, no specific inherited food-occurrence warning, and at least one original pure-compound H-ORAC study confirmed by the preserved closure. This is evidence available in the checked collection, not proof that other candidates lack activity. The two-study sensitivity is reported separately.

Within the queue, at least two checked studies are shown first, then typed SD availability. Candidate ID orders otherwise tied records for a 20-slot budget preview. The entire cutoff stratum is exported to `results/cutoff_tied_candidates.csv`; candidate ID is not a scientific ranking criterion. There is no activity score, journal score, undocumented diversity quota, or conversion from ORAC-FL to predicted PGR activity.

`results/top20_review_queue.csv` gives formulas, identifiers, source DOIs and remaining gaps. `results/formal_lab_ready_panel.csv` stays empty until actual food-source, procurement/form, solubility/stability, counter-screen and researcher decision gates are documented. This deliberate distinction prevents a source-linked candidate preview from being represented as 20 experimentally ready materials.

For your initial screening, enter actual evidence and `INCLUDE`, `HOLD` or `EXCLUDE` decisions in the editable table. Record source, reviewer and date only when those decisions exist. Code will not invent them. Changing a decision should regenerate all affected tables, manuscript counts and figures. A formal panel larger than 20 requires researcher resolution; the code must not truncate approved materials silently.

**Manuscript link:** Methods 3, Tables 2-3, cutoff ties and selection sensitivity describe the current preparation result. The frozen reference remains unchanged.
