# Systematic Review Protocol v1.0

Technical execution version frozen2026-11-17. Researcher adjudication remains pending for the listed decisions. This protocol governs the new six-stage evidence workflow and references the preserved historical analysis modules.

## Research question and population

Identify individually defined food/dietary chemicals through broad discovery, integrate original assay-specific antioxidant evidence, and estimate interpretable candidate priorities for future aqueous absorbance testing. The193 profiles are a historical starting collection. Topic-driven discovery can add compounds following identity and food-occurrence review. Aqueous solubility enters later feasibility appraisal. Panel size follows evidence and feasibility.

Food occurrence requires a traceable analytical publication or a versioned food-composition entry, with food identity,chemical form and source location. FooDB and Phenol-Explorer support occurrence tracing. PubChem and ChEBI support identity. Non-food standards,synthetic controls and mechanism references retain separate roles. Processing products need a defined identity and documented food occurrence. Supplement-only or endogenous-only occurrence requires a reference-role decision.

## Time scope and legacy reuse

The primary first-publication window is2020-01-01 through2026-11-17. The prior retrieval cutoff is2026-11-16. Stage2 must execute and log the one-day update plus revised multi-assay searches. Existing snapshot counts retain their original cutoff. Unknown first-publication dates remain unresolved. Extension2016-01-01 through2019-12-31 requires a logged compound/endpoint gap,missing independent replication,structural coverage gap or missing common comparator. Fewer than20 located relevant leads triggers a coverage investigation; twenty papers is a coverage target. Eligibility and potency depend on the actual experiments. Pre2016 classic original methods are methodology references. Older numerical analyses remain historical diagnostics with their original scope.

## Search and recall validation

Use the dual topic/compound routes in Search_Strategy_By_Database.csv. Resolve aliases through Chemical_Synonym_and_Identity_Rules.csv. Expand each verified alias as a separate quoted term. CAS supports targeted recovery when indexed. Execute assay phrases separately where platform query limits apply. Chinese translations appear in the database query fields while documentation is English. Add backward/forward citations and document provenance. Preserve full queries,dates,hits,exports,limits and raw hashes. Licensed institutional records remain local according to their terms.

Recall audit reuses Known_Source_Recall_Audit.csv. Name-query,class-route and DOI-anchor recovery are separate measures. Before freezing Stage2 execution, test the revised query against in-window known originals spanning assays,chemical classes and naming forms. Record each miss and revise wording or retain an explained miss. A DOI lookup establishes retrieval of that anchor. New-query recall remains pending execution. Historical out-of-window anchors support method/identity testing with separate denominators.

## Screening and adjudication

Use stable record_id,report_id,study_family_id,experiment_id,observation_id and compound_id. Link every database occurrence to its retained report. Duplicate identifiers enter conflict review. Publisher-declared preprint versions share a family key; overlap across reports requires experiment-level checking.

Every deduplicated record receives PENDING,AI_PREDICT_INCLUDE,AI_PREDICT_EXCLUDE,AI_UNCERTAIN,HUMAN_INCLUDE,HUMAN_EXCLUDE or DISAGREEMENT. AI output retains model/rule version,input hash and actual inspected scope. Two independent researcher reviews produce final eligibility; a researcher adjudicates disagreement with reasons. Reviewer names and dates stay blank until actual review. Technical protocol adoption records no scientific approval.

Retrieve full texts and required supplements for eligible/uncertain leads. Record access route,reading scope and source hash. Pure-compound original quantitative studies enter capacity extraction. Mixtures,food matrices,cell/function and mechanism/computation enter their corresponding evidence levels. Secondary numeric claims trigger original-source tracing. Missing access or unclear methods retain PENDING/HOLD.

PRISMA counts separate database hits,exported records,duplicates,unique records screened,reports sought,reports unavailable,full texts assessed,reason-specific exclusions and included studies/reports. Only actual completed transitions enter counts. Use one primary exclusion reason per excluded report plus secondary reasons. Cohorts and version families remain distinct from report counts. Reporting references are PRISMA2020 DOI10.1136/bmj.n71 and PRISMA-S DOI10.1186/s13643-020-01542-z.

## Extraction and analysis gates

Compound→Article→Experiment→Observation links retain original materials,source values,units,mean/error,n hierarchy,protocol,comparators,calculation and locations. Raw AUC,net AUC,capacity,rate and IC50 have distinct endpoint IDs. Maintain original and standardized fields separately. Unit,identity,independence and source conflicts retain HOLD. Quality dimensions cover identity,originality/independence,methods,result completeness,comparability and aqueous applicability. Journal metrics remain dated context variables.

ORAC-FL,ORAC-PGR,crocin,ABTS,DPPH,FRAP and CUPRAC receive method-specific analysis sets. Protocol and material strata govern comparisons. D1–D5 remain available with weights pending validation. First establish simple baselines and study-level validation; structural prediction adds scaffold validation. Existing conditional models retain diagnostic status. Future absorbance validation requires actual equipment-specific data. Stage5 formal input release and Stage6 candidate approval require researcher decisions.

## Execution and handoff

Reproduce Stage1 with `python 02_identity_and_evidence/04_systematic_protocol_v1/code/build_stage1.py`, then run project QC. Existing_Module_Audit.csv and Stage1_Baseline.json document reuse. This module is the technical protocol authority for this task. Legacy00_project/Protocol.md,scope.json and earlier ORAC workflows retain their dated context. Later stages reference this version and log amendments. Stage1 completion is a technical deliverable gate. Stage2 begins after researcher stage review.
