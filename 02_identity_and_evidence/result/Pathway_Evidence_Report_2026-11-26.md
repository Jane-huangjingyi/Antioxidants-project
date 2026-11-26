# Pathway evidence report — 12 retained antioxidant candidates (2026-11-26)

**Question.** Which pathways does each of the 12 rank-stable candidates participate in, which study reports it, where is the evidence in the original report, and which pathways overlap across compounds?

**Source of truth.** The checked mechanism evidence map [04_candidate_in_vivo_mechanism_evidence.csv](table/04_candidate_in_vivo_mechanism_evidence.csv) (28 observations, 26 primary reports) and its [narrative](table/04_candidate_in_vivo_mechanism_evidence.md). Every assignment below is grounded only in the recorded `molecular_node`, `pathway_or_process` and `redox_endpoint` fields. **All 28 rows remain `NOT_REVIEWED` / `change_applied=NO`.** This report organizes existing evidence; it does not approve any claim or add new literature.

**Deliverables.**
- Compound × pathway × study inventory: [05_compound_pathway_inventory.csv](table/05_compound_pathway_inventory.csv) (55 rows; one row per observation–pathway assignment, with DOI, PMID, source locator, study type, evidence grade and boundary).
- Controlled vocabulary: [Pathway_Dictionary.csv](table/audit/Pathway_Dictionary.csv).
- Overlap counts: [06_pathway_overlap_counts.csv](table/06_pathway_overlap_counts.csv).
- Figures (PNG + editable SVG): [evidence matrix](figure/pathway_evidence_matrix.png) · [set sizes](figure/pathway_set_sizes.png) · [UpSet](figure/pathway_upset_signaling.png).
- Generator: [05_render_pathway_figures.R](../code/05_render_pathway_figures.R).

## Method and evidence grading

Pathways are normalized into 8 signaling pathways (P1–P8) and 3 redox process families (R1–R3). Each observation–pathway assignment carries an evidence grade derived from the recorded fields:

| Grade | Rule | Meaning |
|---|---|---|
| FUNCTIONAL | `target_confirmation_class = FUNCTIONAL_PARTICIPATION_SUPPORTED` | Loss-of-function (KO/knockdown/siRNA) supports pathway participation in the tested model |
| BODY_READOUT | body/figure/results scope, not functional | Expression/activity/redox readout in vivo, ex vivo or human; necessity not tested |
| ABSTRACT_ONLY | `source_review_scope = ABSTRACT_ONLY` | Abstract-level only; full text not verified |

**Solid set** = FUNCTIONAL + BODY_READOUT, excluding abstract-only rows and the hesperetin Fig. 8a image-similarity concern (ME12-05, flagged `FIG8A_CONCERN`). Overlap counts are reported both for **all recorded associations** and for the **solid set**. No row establishes direct molecular binding; "functional participation" is pathway-level necessity in a model, not a confirmed direct target.

## Pathway overlap counts (the headline answer)

| Code | Pathway | Compounds (all recorded) | Compounds (solid) |
|---|---|---:|---:|
| P1 | NRF2–KEAP1/ARE antioxidant response | **10** | **7** |
| P2 | NF-κB / TLR4 inflammatory signaling | 1 | 1 |
| P3 | PI3K/AKT signaling | 1 | 1 |
| P4 | MAPK stress signaling (TAK1/p38/JNK) | 1 | 1 |
| P5 | Ferroptosis regulation (GPX4/ACSL4) | 1 | 1 |
| P6 | HIF1A hypoxia response | 1 | 1 |
| P7 | PGC-1α mitochondrial biogenesis | 0 | 0 |
| P8 | CFTR-dependent GSH transport/disposition | 1 | 1 |
| R1 | Glutathione redox (GSH/GSSG/GCL/GPx) | 9 | 9 |
| R2 | Lipid peroxidation defense (MDA/4-HNE/HPNE) | 10 | 9 |
| R3 | ROS/NO vascular redox balance | 5 | 4 |

**The only broadly shared signaling pathway is P1 (NRF2/ARE): 10 of 12 compounds have a recorded association, 7 of 12 with solid evidence.** Every other signaling pathway is compound-specific (one compound each). The redox process families are broadly shared (R1 9, R2 10, R3 5) but are readout-level processes, not signaling targets.

Compound members per pathway (solid): P1 = Quercetin, Genistein, Hesperidin, Myricetin, Chlorogenic acid, Gallic acid, Syringic acid; P2/P4 = Myricetin; P3 = Syringic acid; P5/P6 = Hesperetin; P8 = Glutathione. P7 has no in vivo assignment (the PGC-1α/NRF2 linkage in ME12-18 is cell-only myotube evidence and is not assigned as an in vivo pathway).

## UpSet — exact shared-pathway combinations (solid signaling)

| Intersection | Compounds | Count |
|---|---|---:|
| P1 only | Quercetin, Genistein, Hesperidin, Chlorogenic acid, Gallic acid | 5 |
| P1 + P2 + P4 | Myricetin | 1 |
| P1 + P3 | Syringic acid | 1 |
| P5 + P6 | Hesperetin | 1 |
| P8 | Glutathione | 1 |
| (no solid signaling pathway) | Catechin, p-Coumaric acid, L-Ascorbic acid | 3 |

Catechin and p-Coumaric acid have NRF2 associations only at abstract level (ME12-04, ME12-10), so they fall out of the solid signaling set; L-Ascorbic acid has no protein-target pathway (Gulo is a model genotype). See the [UpSet figure](figure/pathway_upset_signaling.png) and the [full evidence matrix](figure/pathway_evidence_matrix.png) (which retains abstract-only cells in a distinct color so nothing is hidden).

## Per-compound pathway summary (solid evidence; DOIs and locators in the inventory)

| Compound | Solid signaling pathways | Key reports (DOI) | Evidence location |
|---|---|---|---|
| Quercetin | P1 (functional) | 10.1038/s41401-018-0024-8 | Fig. 7c–e (WT redox), Fig. 8a–c (WT vs Nrf2-KO injury) |
| Catechin | — (NRF2 abstract-only) | 10.1080/10715762.2018.1437914 | Abstract (nuclear NRF2); KEAP1 docking computational |
| Hesperetin | P5, P6 | 10.1038/s41598-026-51280-w | Fig. 3J–N (GPX4↑/ACSL4↓); NRF2/HO-1 report Fig. 8a excluded pending verification |
| Genistein | P1 | 10.21037/atm-21-4958 | Figs. 4A–C, 5A–B (NRF2/HO-1 readouts); unfavorable exercise context 10.3390/medicina57101028 |
| Hesperidin | P1 | 10.1039/d2fo00298a | Fig. 8A–D (p62/KEAP1/NRF2 readouts) |
| Myricetin | P1, P2, P4 | 10.1155/2019/6304058 | cardiac signaling + Nrf2-knockdown Results (benefit retained after knockdown) |
| p-Coumaric acid | — (NRF2 abstract-only) | 10.1016/j.biopha.2018.12.074 | Abstract; body study PMC7711293 Fig. 3A–C did not test NRF2 |
| Chlorogenic acid | P1 (functional, ex vivo) | 10.1177/0300060520985363 | Figs. 4–5 (WT vs Nrf2-KO rings); Figs. 6d–g, 8 (dietary readouts) |
| Gallic acid | P1 | 10.2147/DDDT.S86345 | Fig. 6 (colonic NRF2/readouts) |
| Syringic acid | P1, P3 | 10.3390/ijms26167779 | hepatic oxidative-stress/signaling sections; Table 5 |
| L-Ascorbic acid | — | 10.1016/j.brainres.2010.05.090 | Gulo-KO model; no intervention protein target |
| Glutathione | P8 (functional disposition) | 10.1152/ajplung.00365.2006 | CFTR genotype comparison; not a binding target |

## Figures

1. [Pathway evidence matrix](figure/pathway_evidence_matrix.png) ([SVG](figure/pathway_evidence_matrix.svg)) — 11 pathways × 12 compounds, colored by highest recorded grade; `*` marks the hesperetin Fig. 8a concern. Signaling and redox families are faceted.
2. [Pathway set sizes](figure/pathway_set_sizes.png) ([SVG](figure/pathway_set_sizes.svg)) — compounds per pathway, all-recorded vs solid.
3. [UpSet of shared signaling pathways](figure/pathway_upset_signaling.png) ([SVG](figure/pathway_upset_signaling.svg)) — solid intersections (sets = pathways, elements = compounds).

A classical 12-set Venn is not readable (up to 4096 regions); the UpSet plot plus the matrix is the standard readable equivalent and preserves exact per-compound membership and counts.

## Limitations (must travel with any reuse)

- All observations are `NOT_REVIEWED`; the P0 adjudication worksheet ([audit/P0_Mechanism_Adjudication_Worksheet_2026-11-26.md](table/audit/P0_Mechanism_Adjudication_Worksheet_2026-11-26.md)) proposes verdicts for quercetin, chlorogenic acid and hesperetin, pending researcher decision.
- **No direct binding target is established for any compound.** Functional participation (quercetin/NRF2 in vivo liver injury; chlorogenic acid/NRF2 ex vivo rings; glutathione/CFTR disposition) is pathway-level necessity in a model, not target confirmation.
- Myricetin ME12-20: remodeling benefit was retained after cardiac NRF2 knockdown (which lacked a matched scramble arm) — NRF2 necessity is not supported for those endpoints; do not read P1 as causal there.
- Hesperetin ME12-05 Fig. 8a is named in a separate retracted article's image-similarity concern (PMID 34428482); Fig. 8a-dependent claims stay out pending verification. The retraction applies to the melatonin article only.
- Abstract-only rows (catechin NRF2, p-coumaric NRF2, hesperetin NRF2/HO-1, human hesperidin/gallic) are excluded from the solid set but shown in the matrix.
- The historical 257 mechanism proposals in `inputs/mechanism_evidence` are not applied; AFF-0061 receives no validated-target credit. This report covers only the 12 retained candidates' checked map.
- Mechanism evidence is a separate layer from the ORAC-FL capacity model; it does not enter capacity ranking.

## Reproduce

```sh
python 02_identity_and_evidence/code/06_build_pathway_inventory.py   # rebuild inventory + dictionary + counts
Rscript 02_identity_and_evidence/code/05_render_pathway_figures.R    # rebuild PNG/SVG figures
```
