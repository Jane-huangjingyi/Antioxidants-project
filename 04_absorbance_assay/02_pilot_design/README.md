# 04.2 Audit formulas and prepare the absorbance pilot

The active endpoint is assay-defined molar chemical protection capacity measured by absorbance. This is a development design, with no laboratory observations or formal model. Reader and robot models are identified; assay settings and local accessory inventory remain unresolved. See the [Flex platform qualification](../03_platform_compatibility/README.md). Start with the [formula audit](formula_source_audit.json), then complete the [pilot manifest](pilot_manifest_template.json) when platform and pilot information become available. The [twelve-profile preparation panel](../../03_candidate_selection/02_cross_study_expansion/results/Bridge_Panel_Preparation.csv) tests method coverage; it is not the final potency Top20.

## Formula and signal orientation

The 2002 primary paper [1] subtracts a no-initiator blank before its manual endpoint formula. This can reconcile its sign with protection: subtracting the undegraded-probe signal produces a negative bleaching difference. Replacing that observable with remaining probe absorbance reverses the interpretation. The automated implementation uses timed change and further blank signals; it is a separate readout, not an AUC formula. Neither plasma implementation establishes a pure-compound molar capacity estimator.

For example, synthetic no-initiator absorbance 1.0, oxidation vehicle 0.2 and protected sample 0.7 give blank-subtracted differences -0.8 and -0.3. The printed formula then gives 62.5%, whereas inserting remaining absorbances gives -250%. These are algebra checks, not observed results or a reconstruction of unreported instrument processing. Preserve the exact blank definition with every formula.

The 2015 microplate study [2] motivates dose-time modelling, but its complete equations remain source-pending. The author repository has been located; access currently fails certificate/web checks. The 2015 protocol [3] distinguishes relative-rate and total-capacity procedures; its full equations also remain pending. We have not substituted a secondary formula for either original method.

Our existing candidate estimator is explicitly a project proposal: subtract matched no-probe absorbance, normalize each corrected trace by its own positive initial signal, integrate on a common window, subtract matched vehicle AUC and compare compound versus Trolox concentration-response slopes with an intercept. See the [endpoint definition](../01_endpoint_definition/README.md). A larger AUC means greater retained-probe protection under this definition. Initial-signal normalization can mask immediate probe loss, so initial absolute signal and the probe-without-initiator control must pass a separately specified interference check. AUC combines kinetics and extent; molar Trolox equivalence is not a radical-trapping stoichiometry or ORAC-FL conversion. Rate summaries remain separate.

The original 2006 article abstract [4] explicitly reports `100 * (delta_A0 - delta_A) / delta_A0` at an antioxidant-to-crocin molar ratio of one. This percent-inhibition endpoint is distinct from a rate constant and from molar TE capacity. Its full signal, blank and timing definitions remain unverified; the formula is recorded without implementing it as our capacity estimator. It provides an additional original-source check without closing the two pending 2015 equation gaps.

## Stage 1: establish readable chemistry

Use the identified reader capability limits during qualification. Its discrete channels do not provide a spectral scan; a required spectral check needs a separate instrument. Measure actual temperature history, timing, mixing and optical behavior rather than assigning undocumented reader functions. Record exact probe/reagent identity, lot, purity, storage and preparation times. Evaluate buffer-only, probe-only and probe-plus-initiator kinetics to distinguish spontaneous decay from induced bleaching. Vary probe/initiator conditions to find a measurable, reproducible trajectory without saturation or floor effects. Literature conditions are reference options, not approved settings. Record actual final pH and vehicle; the ORAC-FL literature scope does not automatically set this assay's conditions.

## Stage 2: clear material and optical interference

Verify each purchased form against formula, stereochemistry, salt/hydrate, molecular weight, purity basis and COA. Record weighed mass, dilution calculation, lot and stock age. Set exploratory dose bounds using actual solubility and optical compatibility. A visible clear stock alone does not establish final-well solubility or chemical stability. Keep solvent fraction matched across doses and Trolox; otherwise validate and report separate strata rather than pool them.

For every candidate/dose, include the complete reaction, a matched no-probe reaction containing initiator, and a probe-plus-candidate reaction without initiator. Include equivalent vehicle combinations to separate probe decay, reagent background and direct interaction. Buffer/reagent blanks and a Trolox series accompany each independent preparation block. Use the oxidation vehicle as the no-added-antioxidant control; do not assume an untested compound is inactive. Assess color, scattering, precipitation, time-varying backgrounds, direct probe reaction and pH effects. Background subtraction does not remove nonlinear chemical interference or rescue a failed counter-screen. Flag failed/uncertain observations separately from valid nonpositive protection; neither becomes an imputed zero.

## Stage 3: map dose and time before fixing capacity

Measure several pilot dose levels spanning the usable response for both candidate and Trolox. The code requires at least three distinct dose-level means for a diagnostic straight line; this is a computational minimum, not a sufficient experimental design. Determine the final grid and replication from pilot range and precision. Retain complete kinetics, actual initiation/read timestamps and dead time per well. Avoid confounding dose or identity with addition order, row, column or plate. Randomize within preparation/day blocks and distribute repeat QC across positions. A future layout generator requires the real plate geometry and dispensing constraints.

Compare prespecified candidate common integration windows during development, inspect curvature, residuals, saturation and short-/long-time ordering, and keep rate/lag information separate. Freeze one compatible window and estimator before definitive screening. Do not select a different window per compound to improve its score. A slope ratio is eligible only in a jointly validated response range with positive Trolox slope. If nonlinear kinetics prevent a valid capacity estimate, retain the response curves and resolve an alternative estimator; do not force a rank or retrofit the unrecovered 2015 model.

## Stage 4: assess repeatability and lock the protocol

Repeat independent solution preparations across days to assess preparation/day effects; technical wells remain nested within preparation blocks. These are chemical experiments, not biological replicates. Select replication and acceptance limits from the required precision and pilot variability before definitive testing. Document calibration range, interference limits, within-/between-preparation precision, positional/timing effects, allowable exclusions and repeat rules. No numeric threshold is approved here. Preserve shared Trolox/vehicle dependence in uncertainty estimation, for example by resampling entire independent preparation blocks with their calibration and controls after enough blocks exist. Do not treat wells as independent samples or use source-paper SD as this assay's error.

Lock the endpoint, conditions, material eligibility, QC and analysis before generating formal training labels. Separate pilot development data from later validation data; use independent batches and structure-group validation as sample coverage allows. No model score or final experimental Top20 is released at this stage. Cell activity and mechanism require later experiments.

## Reproduce the preparation checks

Run `python 04_absorbance_assay/02_pilot_design/validate_pilot_readiness.py`. It checks source-status distinctions, synthetic signal orientation and AUC/calibration behavior, and reports the unfilled template fields in [readiness](pilot_readiness.json). It does not execute an assay or approve a completed manifest. The raw-data [schema](../inputs/experimental_data_schema.csv) remains header-only; pair it with the completed manifest, material/COA records, plate layout and actual addition log. The raw-analysis command is documented in the [assay entry point](../README.md).

## Raw-trace metadata and diagnostic contrasts

The header-only trace schema now also requires `protocol_id`, `preparation_id`, `vehicle_id` and `time_origin`. Define each ID in the completed manifest: protocol includes the exact chemistry and acquisition settings; vehicle includes identity and final fraction; preparation identifies the independent assay-preparation block within the batch, shared by its sample, matched backgrounds and vehicle controls; individual material-stock records remain separate. Do not encode all differences as one generic protocol. `time_origin` is `INITIATOR_ADDITION`; `time_min` is actual elapsed time from that event, not from the first read. For no-initiator controls use the corresponding scheduled initiation event. Preserve absolute timestamps and dead time in the addition log. No rows or assignments have been invented.

Recognized trace roles are `SAMPLE`, `TROLOX`, `VEHICLE`, `MATCHED_NO_PROBE`, `PROBE_NO_INITIATOR` and `REAGENT_BLANK`. Every recorded kinetic trace needs at least two finite, strictly increasing, nonnegative times and a finite nonnegative final candidate concentration (zero for candidate-free controls). Use an explicit control identity instead of a missing candidate ID. `pair_id` identifies the matched no-probe background; the latter must match candidate, dose, protocol, vehicle and preparation and have recorded QC clearance. `counter_screen_pass=YES` records analytical clearance against the eventual locked criteria; it is not human scientific approval. Unresolved traces must not receive YES merely to run the script.

AUC output now retains corrected initial/final/minimum/maximum absorbance, background well, number of time points and exact-grid hash. Normalization is at the first observed time, which may be later than initiation. Initial-signal loss remains a counter-screen issue; exported diagnostics do not clear it automatically.

After valid raw traces exist, explicitly assign vehicle wells using the [vehicle assignment template](vehicle_assignments_template.json) and run:

```sh
python 04_absorbance_assay/code/analyze_kinetics.py --input path/to/real_traces.csv --output path/to/diagnostic_auc.csv
python 04_absorbance_assay/code/compare_auc.py --input path/to/diagnostic_auc.csv --assignments path/to/actual_vehicle_assignments.json --output path/to/diagnostic_net_auc.csv
```

Each assignment names a sample trace and one or more vehicle traces using batch, plate and well. The contrast subtracts the arithmetic mean of those vehicle AUCs. Protocol, preparation, vehicle, plate, elapsed-time origin and exact grid/window must match. Unequal grids are rejected; interpolation or a different integration rule requires separate validation. Repeated references to the same vehicle in one contrast are rejected, while legitimate sharing across contrasts is retained by well ID. Negative net AUCs are preserved. Technical vehicle wells are not independent preparation counts. These commands generate diagnostic AUCs only, without Trolox fitting, confidence intervals or ranks.

## References

1. Kampa M et al. A new automated method for the determination of the Total Antioxidant Capacity (TAC) of human plasma, based on the crocin bleaching assay. *BMC Clin Pathol*. 2002;2:3. https://doi.org/10.1186/1472-6890-2-3. Checked: manual and automation Methods.
2. Prieto MA, Vazquez JA, Murado MA. Crocin bleaching antioxidant assay revisited: application to microplate to analyse antioxidant and pro-oxidant activities. *Food Chem*. 2015;167:299-310. https://doi.org/10.1016/j.foodchem.2014.06.114. Abstract checked; full equations pending. Author repository: https://digital.csic.es/handle/10261/100663.
3. Ordoudi SA, Tsimidou MZ. Measuring Antioxidant and Prooxidant Capacity Using the Crocin Bleaching Assay (CBA). *Methods Mol Biol*. 2015;1208:329-344. https://doi.org/10.1007/978-1-4939-1441-8_24. Abstract checked; full equations pending.

4. Ordoudi SA, Tsimidou MZ. Crocin Bleaching Assay Step by Step: Observations and Suggestions for an Alternative Validated Protocol. *J Agric Food Chem*. 2006;54:1663-1671. https://doi.org/10.1021/jf052731u. Formula checked in the original abstract; full Methods pending.

## Endpoint interpretation check

The [simulation-only stress test](../04_endpoint_stress_test/README.md) motivates retaining absolute initial signal and full kinetics, reporting rate/lag separately and evaluating common-window/delay sensitivity before locking a capacity response. Window stability does not establish radical stoichiometry. No synthetic scenario becomes a real calibration, concentration range or model label.
