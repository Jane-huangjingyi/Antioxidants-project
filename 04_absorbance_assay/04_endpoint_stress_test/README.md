# 04.4 Stress-test endpoint interpretation before collecting model labels

This dimensionless thought experiment tests whether the proposed normalized-AUC slope ratio can be interpreted as intrinsic radical equivalents per molecule. It does not fit crocin chemistry, predict real compounds or set robot conditions. The active development objective remains a validated, fixed-protocol molar protection response. A rate-sensitive operational response can be useful without being a stoichiometric capacity measurement.

## Mathematical assumptions

Let C be remaining probe, H available antioxidant radical-equivalent sites, J constant radical supply, r relative capture rate and s a constant competing sink. Set D = C + r H + s and define:

`dC/dt = -J C/D; dH/dt = -J r H/D; dS/dt = J s/D`

`C(0) = 1; H(0) = n * dose; S(0) = 0`

The project defined these equations as a toy allocation model. They are not recovered equations from the 2015 method. One captured radical consumes one available site or one probe unit; S accumulates consumption by the background sink. We assume steady radical supply, independent equivalent sites, constant capture parameters and linear signal proportional to C. Products, chain reactions, changing temperature, probe/solute interference and calibration noise are absent. The competition-kinetics literature motivates considering rate as well as concentration [1]; it does not supply the numerical parameters used here.

All parameters and scenarios are explicit in [simulation_scenarios.json](inputs/simulation_scenarios.json). Times and doses have arbitrary units, not minutes or micromolar concentrations. Scenario names do not represent any chemical. The synthetic reference is not measured Trolox.

## Calculation and findings

The implementation uses fourth-order Runge-Kutta integration and trapezoidal normalized AUC. It subtracts the zero-dose vehicle under the same window and fits the same dose-level slope-with-intercept function used in the conditional formula. Slopes are divided by the synthetic reference slope; outputs are diagnostic ratios, not molar TE. Curvature residuals are retained instead of declaring linearity validated. First-read normalization is repeated at each prespecified acquisition start, including delayed starts.

With acquisition start 0 and integration end 4, the two scenarios with n = 2 differ by approximately 3.067-fold in diagnostic slope ratio because their capture rates differ. Acquisition windows also change the ratios. These counterexamples show that a slope ratio alone is not a universal measure of n. They do not estimate the magnitude of bias in real crocin experiments or invalidate an assay-defined molar protection endpoint.

The [summary](results/simulation_summary.json) records numerical convergence, flux balance and input/code hashes. Halving the integration step changes the largest ratio by about 1.13e-6; maximum flux-balance error is below 1e-9. Reference divided by itself remains one. Equal zero-dose trajectories agree across scenarios; they also match the independent implicit solution `C + s ln(C) = C(0) + s ln(C(0)) - Jt` at the checked times. These checks establish numerical behavior under the toy assumptions, not chemical validity.

## Pilot consequences

Retain full kinetics and absolute first-read signal together with normalized curves. Record actual initiation, transfer and read timing and temperature history. Examine candidate common windows and delay sensitivity during development; lock the estimator and window before definitive screening. Do not select a separate favorable window for each compound or use these simulations to select experimental parameters.

Report rate and lag diagnostics separately from integrated protection. A robust order across windows is useful evidence of repeatability, but does not by itself establish stoichiometry. An intrinsic radical-equivalent claim would require independent validation of radical supply, reaction extent and relevant side reactions. Until then, develop and name a fixed-protocol molar protection endpoint, retain interference/solubility gates, and train a formal model only after actual valid labels exist. No new labels, candidate ranks or approved assay settings result from this exercise.

## Reproduce and edit

From the project root:

```sh
python 04_absorbance_assay/04_endpoint_stress_test/simulate_endpoint.py
Rscript 05_analysis/R/render_endpoint_simulation.R
```

The [sensitivity table](results/Synthetic_Endpoint_Sensitivity.csv) contains 45 scenario/window diagnostics. The [trace table](results/Synthetic_Probe_Traces.csv) contains synthetic probe/capacity trajectories for the specified display dose. All outputs carry simulation-only identifiers. The [R script](../../05_analysis/R/render_endpoint_simulation.R) exposes colors, line types, fonts, labels and image dimensions. It exports [PNG](../../06_manuscript/figures/Capacity_Kinetics_Toy_Diagnostic/simulation_v0.1/png/Capacity_Kinetics_Toy_Diagnostic.png) and [editable SVG](../../06_manuscript/figures/Capacity_Kinetics_Toy_Diagnostic/simulation_v0.1/svg/Capacity_Kinetics_Toy_Diagnostic.svg). This is a method-development illustration, not an empirical manuscript result.

## Reference

1. Tubaro F, Ghiselli A, Rapuzzi P, Maiorino M, Ursini F. Analysis of plasma antioxidant capacity by competition kinetics. *Free Radic Biol Med*. 1998;24:1228-1234. https://doi.org/10.1016/S0891-5849(97)00436-X. Original abstract checked; numerical toy equations and parameters above are project-defined.
