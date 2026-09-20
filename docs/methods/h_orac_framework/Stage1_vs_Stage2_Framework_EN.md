# Stage 1 versus Stage 2 Framework (English)

## Core distinction

Stage 1 and Stage 2 are different inference tasks, not sequential parts of one total score.

| Item | Stage 1: Chemical Antioxidant Capacity Ranking | Stage 2: Translational Prioritization |
|---|---|---|
| Core question | Under comparable chemical conditions, which compound better interrupts AAPH-derived peroxyl-radical chain oxidation? | Which candidates deserve human, mechanistic, and target experiments? |
| Primary inputs | Tier A ORAC-FL; Tier B is supportive only | Human evidence, exposure, PK, biological redox, mechanism, targets, tractability, and safety |
| Main unit | mol TE/mol compound | Domain grades or a sensitivity-tested priority score |
| Output name | Chemical Antioxidant Capacity rank | Translational Priority |
| Missing data | `not_measured` / `insufficiently_comparable`, followed by placement on the measurement-priority list | Missing is recorded by domain and not automatically scored as zero |
| Prohibited inference | Human efficacy, bioavailability, cellular regulation, or clinical benefit | Must not rewrite the chemical ORAC value |

## Stage 1 decision flow

Candidates first pass food origin, parent-small-molecule, and unique-structure rules. ORAC-FL records are then extracted, assigned to H-ORAC or L-ORAC, and graded A/B/C/X. Tier A enters the primary numerical ranking; Tier B is supportive; Tier C and X are excluded from numerical ranking. Multiple eligible records are checked for homogeneity before reporting the median and range/IQR; the maximum is never selected. H/L arms are reported separately without bridging validation. Candidates lacking ORAC data remain eligible and enter the measurement-priority list.

## Stage 2 decision flow

Stage 2 may include high-ranking Stage 1 candidates, candidates with missing ORAC but other important evidence, and candidates needed to investigate cross-class bias. Its eight minimum domains are human evidence, dietary exposure, bioavailability/dose translation, biological redox evidence, mechanistic evidence, direct-target evidence, experimental tractability, and safety/prooxidant risk. Major human metabolites and context interactions are mandatory structured annotations.

The original 25/25/20/15/15 scheme is renamed the legacy Translational Priority Score and no longer determines the chemical Top20. v2.0 proposes 20/15/15/15/10/10/10/5 as an initial sensitivity scenario to be tested in the pilot while retaining the domain profile. Any weighted total must report missing-data handling, alternative-weight scenarios, and rank stability.

## Output and naming

Only Stage 1 can produce a `Chemical Antioxidant Capacity Top20`, labeled `provisional` when evidence coverage is incomplete. Only Stage 2 can produce a `Translational Priority Top20`. An undefined “overall antioxidant-capacity Top20” must not be published. Profiles, evidence matrices, and risk flags are preferred for multidimensional information.
