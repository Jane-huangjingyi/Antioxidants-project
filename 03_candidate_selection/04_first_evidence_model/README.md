# First evidence-model availability, identifiability and diagnostic fit

Run `python 03_candidate_selection/04_first_evidence_model/fit_diagnostic_model.py` from the project root. The code uses the existing `.runtime_chem` NumPy installation. Input is the explicitly molar, positive candidate/DOI median reference table from the preliminary literature workflow. These references retain unresolved original-value, protocol, error and independence issues. This exploratory input choice expands beyond currently released primary labels and requires source verification before scientific ranking claims.

## Available data and identifiable scope

The 69 candidate-paper references cover 44 candidates in five disconnected components. Components have 34/11, 6/1, 2/1, 1/1 and 1/1 candidate/paper counts. Cross-component calibration is unavailable. The largest component has 59 references. An unweighted additive model on log capacity estimates 34 candidate locations and 10 paper contrasts. Paper effects sum to zero. The design has rank 44 and 15 residual degrees of freedom. Connectedness and full rank establish algebraic estimability under this additive specification. Protocol compatibility and reliable data provenance require separate source checks.

The project selected ordinary least squares for this first diagnostic because reliable row-level sampling variances and article-level quality assessments are incomplete. This choice assumes additive paper shifts on the log scale, equally influential candidate-paper summaries and a common residual fitting criterion. Paper shifts can absorb multiple unresolved differences and are not identified causal protocol corrections. Publication counts and journal IF supply no numerical weights. Candidate estimates are conditional log locations, and their exponentials are geometric-scale locations. They are not arithmetic expected capacities. Exact material identity, study independence and heteroscedasticity remain unresolved.

## Validation and limits of prediction

Each leave-paper-out fold fits paper contrasts using training papers only, centering their effects to zero. Predicting a new paper uses an explicitly assumed mean-zero paper effect. Candidate locations are evaluated only when their contrast lies in the training design row space. The diagnostic retains unestimable rows and their status. It evaluates prediction of previously observed compound identities in another paper. Structure-held-out prediction requires a later structural model.

Thirty-five held-out rows have estimable candidate locations under this centering assumption. On the matched rows, paper-adjusted MAE/RMSE are approximately 0.318/0.408 log units, compared with 0.326/0.391 for training-only candidate means. The mixed result provides no consistent advantage across these two metrics. Training RMSE is 0.146 log units and is distinct from held-out performance. Ten candidates lie outside the largest component and retain their component assignments in Component_Coverage.csv. No interval, Top20 probability or cross-component position is estimated here.

## Deliverables

`results/Candidate_Diagnostic_Estimates.csv` contains 34 conditional candidate estimates and within-component diagnostic positions. `results/Component_Coverage.csv` shows all 44 candidates. `results/Leave_Paper_Out_Diagnostics.csv` retains all held-out rows, prediction eligibility and matched baseline. `results/Paper_Fold_Identifiability.csv` reports fold ranks. `results/model_diagnostics.json` records counts, errors, assumptions-related status and input/code hashes.

The next modelling step is to resolve original values and source quality, verify protocol strata, compare defensible alternative likelihoods and obtain uncertainty estimates under explicit variance assumptions. The detection assessment also needs actual material and assay qualification. The present fit supplies computational diagnostics for those decisions.
