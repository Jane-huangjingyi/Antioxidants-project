# Phase 0–1 Decision Log

Version 1.0, 2026-09-17.

## Frozen decisions

1. The main list covers normal diets worldwide. Exposure stays population/region-specific and is not generalized globally.
2. Generally healthy adults and diet-achievable exposure are primary; patient, high-risk, and supplement evidence is labeled separately.
3. The main list accepts uniquely structured food parent molecules only. Metabolites, endogenous substances, minerals, and medicinal/supplement-dependent entities are secondary/extended.
4. There is no polyphenol quota. Polyphenol-first is an execution order, not a ranking preference.
5. Antioxidant evidence includes direct, redox-regulatory, and indirect-redox mechanisms; indirect pathways require credible redox endpoints.
6. Evidence quality outranks volume. Publication count saturates within tier and cannot promote lower-tier evidence.
7. Human effects and human PK are separate; H5 establishes exposure and does not substitute for benefit.
8. T1/T2, T3, T4, and T5 are separate output layers; database or author terminology cannot override assay-level adjudication.
9. Safety/dose window is a risk and translation dimension, not an early hard exclusion or simple additive score.
10. Descriptive co-treatment is only possible synergy/antagonism; definitive interaction requires a null model.
11. Missing states distinguish not_searched, searched_none, conflicting, and not_applicable.
12. Scoring code, search cut-off, and missingness rules must be frozen before ranking, followed by multi-weight rank stability.

## Added refinements

- Evidence families prevent duplicate counting of multiple reports from one study.
- Assay-validity and polyphenol-interference checks reduce nonspecific target claims.
- Parent–form–metabolite links and comparable molecular species prevent comparing parent in-vitro doses with conjugate Cmax.
- Food exposure is separated into content, consumption, and estimated intake; occurrence-only evidence is capped at 0.20.
- T2 has a directness qualifier; intact-cell TPP/CETSA may be downgraded without competition or orthogonal evidence.
- Cross-class checks include betalains, quinones, and nitrogen-containing phytochemicals without guaranteeing ranking inclusion.

## Open decisions for investigator review

1. Whether to confirm 25/25/20/15/15 as the sole main scheme and accept the human-prioritized, exposure-balanced, and experimental-translation sensitivity schemes.
2. Exact food-domain subweights and a threshold for meaningful exposure. The recommendation is to calibrate against Phase 2A distributions rather than impose one global threshold.
3. Whether 10×/100× dose-gap boundaries use total Cmax, unbound Cmax, tissue exposure, or metabolite exposure separately.
4. Whether conflicting evidence and safety risk are penalties, tie-breakers, or a separate decision matrix. The current recommendation is tie-breaker plus matrix.
5. A rank-stability rule, for example Top20 inclusion in at least three of four schemes and rank IQR no greater than five.
6. Minimum regional coverage. Suggested minimum: China, North America, and Europe, adding other East Asia, South Asia, Latin America, and Africa when data permit.
7. Whether to preregister protocol/code and the resources available for dual review.

## Internal audit result

No circular definition was found: eligibility does not depend on final score, and scores do not redefine evidence tiers. Evidence-family deduplication and saturation address popularity bias. `relation_type`, directness, and T-tier prevent target mixing. Human effects, PK, biological redox assays, and cell-free chemistry are separated. Bioavailability, major metabolites, food content, and consumption have distinct fields. Most fields can be automated, but food-form mapping, assay interference, T2 directness, endpoint validity, and risk of bias need human review. The most subjective areas are food-domain subweights and quality downgrading; Phase 2 should calibrate these through duplicate pilot coding and agreement statistics. No premature hard threshold is imposed for human evidence, direct targets, or safety. The framework supports later batch generation and target extraction, but formal ranking must wait for review.
