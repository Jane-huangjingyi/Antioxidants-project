# 03.2 Cross-study evidence and measurement bridge

Read `results/Cross_Structure_Evidence_Expansion.csv` for the new original-source observations and `Bridge_Measurement_Plan.md` for the proposed next measurements. `results/Bridge_Panel_Preparation.csv` contains twelve existing candidate profiles and their specific bridge roles; it is not an efficacy ranking or final experimental Top20.

From the project root, run:

```sh
python 03_candidate_selection/02_cross_study_expansion/build_cross_structure_evidence.py
python 03_candidate_selection/02_cross_study_expansion/build_bridge_panel.py
python 03_candidate_selection/01_activity_model/run_model_checks.py
```

The complete model runner also invokes both builders. The original Suzuki BioC response is bundled once in `inputs/PMC12534199_original_BioC.json` with title/author/DOI and CC-BY metadata; its source endpoint is `https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/pmcoa.cgi/BioC_json/PMC12534199/unicode`. Its SHA256 is recorded in the result summary. Carrasco extraction is scoped to original PDF text and locators in `inputs/carrasco_source_check.json`. Access-only leads are recorded separately and contribute no numeric labels.

All original source values, reported zeros and nonnumeric no-activity outcomes remain distinct. No default variance, missing pH, unreported stereochemistry or peptide termini are imputed. Existing candidate membership, formal evidence states, frozen rankings and the completed exploratory model remain unchanged. New source observations appear in the Step 03.1 analysis-disposition table as waiting records until their specific gates close.
