# Compound–Target Evidence Classification

Version 1.0. The unit of classification is a compound form–protein–species–system–publication record. The same protein may receive different tiers in different contexts.

## T1: direct biochemical or biophysical binding

T1 requires attributable binding or enzyme inhibition in a purified or otherwise defined protein system: resolved crystal/cryo-EM binding, SPR, ITC, MST, BLI, equilibrium dialysis, or Ki/Kd measured after excluding aggregation, redox cycling, colloids, and readout interference. IC50 alone, docking, nonspecific precipitation, or a natural-product assay without negative and competition controls is not automatically T1. Structural evidence must identify the ligand and site; enzymology must report substrate conditions, mechanism, and reproducibility.

## T2: cellular target engagement or chemical proteomics

T2 includes adequately controlled CETSA, TPP, DARTS, ABPP, competition-based affinity capture, and chemical proteomics. It supports engagement in cells or complex matrices, but not every signal proves direct binding: intact-cell TPP can reflect metabolites, complexes, post-translational changes, or downstream protein states. Without lysate/recombinant confirmation, dose response, or competition, record `directness_qualified=ambiguous` and downgrade to T3 when appropriate. A derivatized probe must retain parent-compound activity.

## T3: functional target validation

Knockdown, knockout, overexpression, resistant mutation, or rescue establishes that a protein is necessary or important for the compound effect without showing binding. T3 is a functional target and must not be called a validated direct target. Directionally coherent controls must exclude general toxicity and nonspecific loss of cell state.

## T4: regulated or pathway-associated protein

Only expression, phosphorylation, localization, nuclear translocation, activity, or pathway readouts change. Nrf2, KEAP1, NF-κB/p65, SOD, CAT, and GPX belong here when supported only by such observations. Use `regulated_protein` or `pathway_associated`, never binding/direct target.

## T5: predicted target

Evidence comes from SwissTargetPrediction, network pharmacology, machine learning, reverse docking, docking, or another computational inference. Store algorithm, version, input structure, score, background database, and retrieval date. Predictions sharing training data are not independent validations. T5 is hypothesis-generating only.

## Output and adjudication

Only quality-qualified T1/T2 records enter the high-confidence direct-target layer; T2 records with unresolved indirectness do not. T3 is a functional target, T4 a regulated/pathway-associated protein, and T5 a predicted target. Database labels never override assay-level review: BindingDB, ChEMBL, and PubChem BioAssay records require inspection of assay descriptions and primary reports; CTD and STITCH associations are not presumed binding.

Conflicting records are retained and judged by assay quality, species, compound form, free concentration, and raw evidence rather than majority vote. Polyphenol-specific risks include PAINS behavior, colloidal aggregation, nonspecific protein binding, metal chelation, oxidative covalency, optical interference, and sample degradation. Every T1/T2 record should capture purity, construct, buffer, temperature, compound form, concentration range, quantitative value, controls, and orthogonal-validation status.

Example: reduced p65 nuclear translocation after EGCG is T4; loss of an EGCG redox phenotype after gene knockout is T3; competition-sensitive pull-down from lysate is candidate T2; reproducible ITC on purified protein with an orthogonal assay and aggregation controls is T1.
