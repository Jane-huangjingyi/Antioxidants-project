# 04.1 Define the capacity endpoint before fitting a ranking

The primary objective is expected molar chemical capacity; reaction rate is separate. An operational `mol TE/mol compound` response does not automatically equal the number of radicals trapped per molecule. Fix assay, vehicle, temperature, timing and analysis before interpreting a ranking.

Run `python 04_absorbance_assay/01_endpoint_definition/build_endpoint_comparison.py` to regenerate the [method comparison](results/Endpoint_Method_Comparison.csv). Crocin bleaching with a validated dose-time capacity endpoint is the first development candidate. ABTS provides a distinct complementary chemical response. ORAC-PGR remains a reactivity-sensitive comparator. None is approved or universally broad-spectrum.

The 2015 crocin microplate paper reports a dose-time treatment and sensitivity to assay conditions, rather than support for ignoring kinetics. Its complete model equations are not yet recovered. The protocol chapter distinguishes relative rate and total-capacity calculations. A 2002 automated crocin study demonstrates Trolox comparison but validates a plasma assay, not this robot's pure-compound panel. These sources justify method development, not adopting concentrations or thresholds without a pilot. [Microplate study](https://pubmed.ncbi.nlm.nih.gov/25148992/), [protocol](https://pubmed.ncbi.nlm.nih.gov/25323518/), [automated study](https://pmc.ncbi.nlm.nih.gov/articles/PMC128814/).

## Candidate formula to validate

For the same validated integration window and vehicle, calculate interference-corrected normalized AUC, subtract the matched vehicle AUC, and fit dose-level mean net AUC against molar concentration with an intercept. A candidate operational endpoint is:

`molar TE = slope(net AUC versus compound concentration) / slope(net AUC versus Trolox concentration)`

Concentrations must use the same molar unit and responses the same time normalization. `capacity_formula.py` makes this calculation explicit. Its synthetic checks establish ratio/intercept behavior and rejection of flat reference calibration; they do not establish that crocin response is linear, stoichiometric, or comparable to ORAC-FL. Do not force nonlinear dose-time curves into this formula. If the pilot shows nonlinearity, recover and validate a suitable dose-time model or report an explicitly defined fixed-response endpoint instead.

Dose-level means require an actual independent-batch design. Common Trolox calibration and common vehicle blanks create dependent errors; their covariance must enter uncertainty estimation. Preserve nonpositive responses rather than replacing them with zero or applying a logarithm. Formal acceptance thresholds remain unset.

Current missing platform information: reader/robot model, wavelength capability, kinetic and temperature control, mixing/addition timing and usable plate format. Before definitive screening, test interference, solubility/stability, vehicle response, probe purity and degradation, dynamic range, blank correction and between-day repeatability. No experiment has been executed and no final panel is generated here.

Instrument selection will be confirmed later by the researcher. This does not block source recovery, error-scale review, assay-specific evidence synthesis or formula validation on synthetic data. Keep device-specific settings null until the actual platform is known.
