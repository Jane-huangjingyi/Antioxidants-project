# 03. Select a review panel and disclose unresolved decisions

For the researcher-selected objective of highest expected molar chemical capacity, start with [Step 03.1: activity-model preparation](01_activity_model/README.md). The queue below remains a historical preparation baseline and is not a fitted capacity ranking.

Run `python 03_candidate_selection/code/select_candidates.py`. Rules are in `config/selection_rules.json`; the researcher-editable decision table is `config/researcher_decisions.csv`. Rebuilding preserves the decision table. Empty fields remain unknown.

The review queue requires reference identity/formula, retained molecular food scope, no specific inherited food-occurrence warning, and at least one original pure-compound H-ORAC study confirmed by the preserved closure. This is evidence available in the checked collection, not proof that other candidates lack activity. The two-study sensitivity is reported separately.

Within the queue, at least two checked studies are shown first, then typed SD availability. Candidate ID orders otherwise tied records for a 20-slot budget preview. The entire cutoff stratum is exported to `results/cutoff_tied_candidates.csv`; candidate ID is not a scientific ranking criterion. There is no activity score, journal score, undocumented diversity quota, or conversion from ORAC-FL to predicted PGR activity.

`results/top20_review_queue.csv` gives formulas, identifiers, source DOIs and remaining gaps. `results/formal_lab_ready_panel.csv` stays empty until actual food-source, procurement/form, solubility/stability, counter-screen and researcher decision gates are documented. This deliberate distinction prevents a source-linked candidate preview from being represented as 20 experimentally ready materials.

For your initial screening, enter actual evidence and `INCLUDE`, `HOLD` or `EXCLUDE` decisions in the editable table. Record source, reviewer and date only when those decisions exist. Code will not invent them. Changing a decision should regenerate all affected tables, manuscript counts and figures. A formal panel larger than 20 requires researcher resolution; the code must not truncate approved materials silently.

**Manuscript link:** Methods 3, Tables 2-3, cutoff ties and selection sensitivity describe the current preparation result. The frozen reference remains unchanged.
