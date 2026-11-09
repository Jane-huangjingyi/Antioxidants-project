# 04. Prepare the aqueous absorbance assay

For the capacity-primary objective, start with [endpoint definition](01_endpoint_definition/README.md). Crocin bleaching with a validated dose-time capacity endpoint is the first method-development candidate, ABTS a distinct complementary capacity response, and ORAC-PGR a reactivity-sensitive comparator. The original registry remains a source bibliography rather than an assay approval. The platform decision file keeps unapproved parameters null. No experiment is executed by this workflow.

PGR measures protection of an absorbance probe from radical-driven consumption. Probe-dependent competition and reactivity prevent direct substitution of historical ORAC-FL values. The 2011 microplate paper reports 540 nm kinetic measurement; its validation in beverages is a starting point, not proof of universal coverage of pure compounds. The 2016 flow study supports controlled automation but does not validate this robot. A 2025 implementation reports a substantially different AAPH condition, retained as a verification issue rather than copied into a protocol. Crocin and ABTS remain independently reported methods; no assay is assumed to be universally broad-spectrum. Sources and checked sections are in the registry.

Before screening, confirm instrument wavelength range, temperature control, kinetics and mixing. For each exact reagent form record supplier/lot/COA, mass/purity basis, stock preparation, dissolved concentration, vehicle fraction and stability. Pilot concentration bounds follow actual solubility, optical/reaction compatibility and dynamic range, not the old ORAC median. Use matched-dose no-probe backgrounds, probe without initiator, vehicle reactions, reagent blanks and Trolox calibration/QC. Assess color/absorbance overlap, turbidity, precipitation, adsorption, direct probe interactions, pH and radical-generator effects.

Randomize within independent preparation/day blocks; distribute shared QC and avoid confounding concentration or candidate with row/column/addition time. Technical wells are nested measurements, not independent studies or biological replicates. Lock integration window, baseline handling, calibration, valid range, QC thresholds, exclusions and repeat rules after the pilot and before definitive testing. Preserve negative and invalid results with distinct flags.

`code/analyze_kinetics.py` implements a transparent trapezoidal AUC calculation for real, interference-cleared traces, requiring one dose-matched no-probe trace on the same time grid. It rejects missing clearance, metadata mismatches and non-positive corrected initial absorbance. It does not silently interpolate, impute, force an IC50 fit or report Trolox equivalents without a separately validated calibration model. The schema CSV has no experimental rows; no experimental Result is generated now.

```sh
python 04_absorbance_assay/code/analyze_kinetics.py --input path/to/real_traces.csv --output path/to/auc_results.csv
```

Cell/function and causal mechanism experiments require later, independent designs. Chemical protection does not establish cell benefit, direct binding, causal mechanism or human efficacy.

Continue with the [formula audit and staged pilot design](02_pilot_design/README.md). The manifest is an unfilled preparation template; offline checks do not approve laboratory execution.

The [pilot design](02_pilot_design/README.md#raw-trace-metadata-and-diagnostic-contrasts) defines required protocol/preparation/vehicle IDs, elapsed-time origin and explicit vehicle assignments. `code/compare_auc.py` rejects incompatible grids or strata and preserves nonpositive diagnostic net AUCs. The raw and assignment templates contain no experimental records.

The [identified Flex reader qualification](03_platform_compatibility/README.md) now constrains the active platform plan. The crocin 450 nm route is an optical development candidate; the audited ABTS/PGR methods are not directly compatible with the default channels. No built-in reader temperature control or shaking is assumed.

Before interpreting AUC slope ratios as capacity, read the [endpoint interpretation stress test](04_endpoint_stress_test/README.md). Its dimensionless simulations are separate from experiment data and candidate rankings.
