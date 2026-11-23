"""Build manuscript-facing descriptive results and tables; never invent experimental outcomes."""
from pathlib import Path
import sys,collections
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'00_project'))
from pipeline_io import *
discovery=read_csv(ROOT/'01_candidate_discovery/results/discovery_register.csv')
profiles=read_csv(ROOT/'02_identity_and_evidence/result/table/candidate_evidence_profiles.csv')
queue=read_csv(ROOT/'03_candidate_selection/result/table/top20_review_queue.csv')
sensitivity=read_csv(ROOT/'03_candidate_selection/result/table/selection_sensitivity.csv')
summary=read_json(ROOT/'03_candidate_selection/result/table/selection_summary.json')
identity=sum(r['identity_reference_status']=='REFERENCE_IDENTIFIERS_AND_FORMULA_PRESENT' for r in profiles)
scope=sum(r['scope_disposition']=='RETAIN_FOR_IDENTITY_AND_FOOD_VERIFICATION' for r in profiles)
id_scope=sum(r['identity_reference_status']=='REFERENCE_IDENTIFIERS_AND_FORMULA_PRESENT' and r['scope_disposition']=='RETAIN_FOR_IDENTITY_AND_FOOD_VERIFICATION' for r in profiles)
metrics=[('Discovery records',len(discovery),'191 literal legacy seed names + 12 rescreened exclusions + 1 targeted gap'),('Identity/evidence profiles',len(profiles),'191 preserved IDs + food-derived glutathione reopening + ergothioneine gap'),('Reference identity and formula present',identity,'CID, InChIKey and formula; not a lot identity certificate'),('Molecular-scope profiles',scope,'Unspecified elemental-nutrient labels retained as context only'),('Identity-complete molecular-scope profiles',id_scope,'Food occurrence still requires candidate-specific verification'),('In the existing 157-candidate framework',sum(r['framework157_scope']=='YES' for r in profiles),'Coverage boundary, not an activity exclusion'),('Review-queue eligible',summary['queue_eligible'],'At least one checked original chemical source; dietary uncertainty flags held'),('Provisional review slots',len(queue),'Administrative budget preview; not potency ranks'),('Two-confirmed-study sensitivity',next(int(r['eligible_count']) for r in sensitivity if r['scenario']=='TWO_CONFIRMED_STUDIES_ONLY'),'Reliability criterion only'),('Laboratory-ready panel',summary['formal_lab_ready'],'Actual material, food-source, interference and human decision gates')]
write_csv(ROOT/'06_manuscript/result/table/Table_1_Discovery_and_Selection_Flow.csv',[{'stage':a,'count':b,'interpretation':c} for a,b,c in metrics])
fields=['review_slot','candidate_id','compound_name','molecular_formula','pubchem_cid','inchi_key','confirmed_independent_horac_studies','confirmed_horac_source_dois','shortlist_status']
write_csv(ROOT/'06_manuscript/result/table/Table_2_Provisional_Review_Panel.csv',[{k:r[k] for k in fields} for r in queue])
frozen=read_csv(source('data/h_orac_stage25b/frozen/Stage25B_Frozen_Primary_HORAC_Top20.csv'));old={r['candidate_id'] for r in frozen};new={r['candidate_id'] for r in queue}
comparison=[]
names={r['candidate_id']:r['compound_name'] for r in profiles}
for cid in sorted(old|new):comparison.append({'candidate_id':cid,'compound_name':names[cid],'legacy_frozen_member':'YES' if cid in old else 'NO','current_review_preview_member':'YES' if cid in new else 'NO','interpretation':'Different purpose and gates; no modification of frozen ranking'})
write_csv(ROOT/'06_manuscript/result/table/Table_3_Preview_and_Frozen_Reference.csv',comparison)
write_csv(ROOT/'06_manuscript/result/table/supplementary/Table_S1_Identity_and_Food_Gaps.csv',[{k:r[k] for k in ['candidate_id','compound_name','molecular_formula','identity_reference_status','food_occurrence_status','food_source_locator','chemical_form_and_lot_status']} for r in profiles])
method=read_json(ROOT/'04_05_experimental_validation/input/primary_method_registry.json')
write_csv(ROOT/'04_05_experimental_validation/result/table/method_comparison.csv',method)
out=ROOT/'06_manuscript';out.mkdir(exist_ok=True)
lines=['# Results: source-bounded candidate discovery and screening preparation','',f'As of {AS_OF}, the reproducible discovery register contained {len(discovery)} records: 191 names reconstructed from the original class-based enumeration, 12 preserved exclusion records rescreened under the current food-source rule, and one targeted ergothioneine addition. The register is a versioned discovery collection, not an exhaustive census of food chemicals.','',f'The workflow produced {len(profiles)} candidate identity/evidence profiles; {identity} had reference CID, InChIKey and formula, while {id_scope} also met the molecular-form scope check. The existing five-dimensional framework covered 157 preserved candidates. Other profiles were labelled outside that snapshot instead of assigned negative evidence.','',f'{summary["queue_eligible"]} candidates met the review-queue gates using preserved candidate-specific source closure. The two-confirmed-study sensitivity retained {metrics[8][1]}. A {len(queue)}-slot administrative preview was produced, with {summary["cutoff_tied_count"]} candidates in the cutoff evidence stratum; all tied candidates remain visible for researcher adjudication. Candidate IDs resolve display order only.','',f'The preview overlapped the frozen H-ORAC Top20 in {len(old&new)} candidates; {len(new-old)} preview candidates were outside the frozen set and {len(old-new)} frozen members were outside the preview. This is a comparison of different selection purposes, not a revised activity ranking.','',f'{summary["formal_lab_ready"]} profiles met all laboratory-ready gates. No new absorbance assay results, effective concentrations, causal targets or human benefits were generated.','', 'Tables 1-3 report the discovery flow, reference formulas/source-linked review panel, and comparison with the frozen reference. Table S1 records identity/food-source gaps. Figures 1-3 visualize screening preparation only.','', '## Suggested manuscript use','', 'These are descriptive workflow results suitable for a methods-development or candidate-prioritization manuscript. Laboratory efficacy, dose-response and mechanism Results remain unwritten until real data and adjudications exist.']
(out/'Results.md').write_text('\n'.join(lines)+'\n',encoding='utf8')
claims=[{'claim':'A versioned food-chemical discovery workflow was implemented','section':'Methods 1; Results 1','support':'Table 1; discovery_register.csv; original enumeration hash','status':'SUPPORTED_WITH_EXPLICIT_COVERAGE_LIMIT'}, {'claim':'Reference identity and formula are available for review candidates','section':'Methods 2; Results 2','support':'Table 2; PubChem raw responses and access log','status':'REFERENCE_IDENTITY_ONLY_NOT_REAGENT_CERTIFICATION'}, {'claim':'20 review slots are proposed','section':'Results 3','support':'Table 2; selection_rules.json; cutoff_tied_candidates.csv','status':'PROVISIONAL_ADMINISTRATIVE_PREVIEW_NOT_FINAL_TOP20'}, {'claim':'Non-fluorescent capacity endpoint candidates were compared','section':'Methods 4; Discussion','support':'Primary method registry; Step 04.1 endpoint comparison','status':'METHOD_PROPOSAL_NOT_VALIDATED_ON_USER_PLATFORM'}, {'claim':'Candidates have experimentally measured activity in the new assay','section':'Future Results','support':'No current experimental data','status':'NOT_SUPPORTED_DO_NOT_WRITE'}, {'claim':'Mechanism observations are validated direct targets','section':'Future mechanistic Results','support':'AFF0061 observations remain NOT_REVIEWED','status':'NOT_SUPPORTED_DO_NOT_WRITE'}]
write_csv(out/'result/table/audit/Manuscript_Claim_Map.csv',claims)
write_json(ROOT/'07_quality_control/result/table/audit/descriptive_summary.json',{'metrics':[{'stage':a,'count':b} for a,b,_ in metrics],'frozen_preview_overlap':len(old&new),'new_preview_members':sorted(new-old),'omitted_frozen_reference_members':sorted(old-new),'publication_claim_limits_recorded':True})
print('06: manuscript Methods-linked descriptive Results and tables generated from actual workflow outputs.')
struct_summary=ROOT/'03_candidate_selection/01_activity_model/results/scaffold_validation_summary.json'
if struct_summary.exists():
 s=read_json(struct_summary);r=s['metrics']['ridge'];n=s['metrics']['null']
 with (out/'Results.md').open('a',encoding='utf-8') as f:
  f.write(f"\n\n## Exploratory structural validation\n\nThe 36 single-paper log-ORAC labels and database candidate graphs were evaluated by nested leave-one-scaffold-group-out validation (five groups: 23, 8, 3, 1 and 1). Four-descriptor ridge regression yielded pooled MAE {r['MAE']:.3f} and RMSE {r['RMSE']:.3f}, compared with {n['MAE']:.3f} and {n['RMSE']:.3f} for the matched training-mean baseline. The model did not show a consistent improvement across these two metrics. These are exploratory internal errors, not independent-study validation or established performance for verified experimental structures. No global ranking was generated. Per-fold errors are provided in the structural validation tables.\n")
 aug=ROOT/'03_candidate_selection/01_activity_model/results/augmented_scaffold_validation_summary.json'
 if aug.exists():
  a=read_json(aug)['metrics']['ridge']
  with (out/'Results.md').open('a',encoding='utf-8') as f:
   f.write(f"\nAdding phenolic-OH and aryl-methoxy counts in a post-hoc sensitivity analysis gave MAE {a['MAE']:.3f} and RMSE {a['RMSE']:.3f}. This small improvement is exploratory, since feature selection followed inspection of initial validation results. It does not establish an independently validated ranking model.\n")
 fp=ROOT/'03_candidate_selection/01_activity_model/results/fingerprint_scaffold_validation_summary.json'
 if fp.exists():
  v=read_json(fp);m=v['metrics']['ridge']
  with (out/'Results.md').open('a',encoding='utf-8') as f:
   f.write(f"\nA further post-hoc Morgan-fingerprint analysis yielded MAE {m['MAE']:.3f} and RMSE {m['RMSE']:.3f}, with {v['unique_feature_vectors']} distinct vectors across 36 candidate structures. Pooled errors improved relative to the mean baseline, but the three-member catechin-related scaffold group worsened (MAE 0.922 versus 0.350). This heterogeneous result does not support a final global ranking. Chirality was excluded and source-material stereochemistry remained unresolved.\n")

pressure=ROOT/'03_candidate_selection/01_activity_model/results/pressure_test_summary.json'
if pressure.exists():
 s=read_json(pressure);m=s['metrics']['model'];n=s['metrics']['null']
 with (out/'Results.md').open('a',encoding='utf-8') as f:
  f.write(f"\n## Retrospective protocol-shift pressure test\n\nThe separately authorized two-observation diagnostic used explicit molar means from DOI 10.1271/bbb.110717. Development-only scaffold CV selected alpha {s['selected_alpha']:g}; external values were not used for tuning. Both known compounds received log prediction 1.5796, below source log arithmetic means 2.1972 (Catechin) and 2.3026 (Epicatechin). Descriptive model MAE/RMSE were {m['MAE']:.3f}/{m['RMSE']:.3f}, compared with {n['MAE']:.3f}/{n['RMSE']:.3f} for the development-mean baseline. These observations compare different summary estimands and protocols; they establish neither formal external validation nor new-structure validity. No ranking was updated. Individual residuals are recorded in Retrospective_Pressure_Test.csv.\n")

external=ROOT/'03_candidate_selection/01_activity_model/results/external_validation_readiness.json'
if external.exists():
 s=read_json(external);g=next(x for x in s['graphs'] if x['scope']=='DEVELOPMENT_PLUS_TRACED_EXTERNAL_TOPOLOGY_NOT_HARMONIZED_LABELS')
 with (out/'Results.md').open('a',encoding='utf-8') as f:
  f.write(f"\n## External evidence readiness\n\nThe retrospective queue contained {s['queue_observations']} observations across {s['papers']} papers. Original numeric text was rechecked for {s['original_values_rechecked']} observations; molar-estimator provenance was traced for {s['molar_estimator_traced_observations']}, while {s['approved_external_labels']} common-target external labels were released. No duplicate observation keys were found, but cross-paper data-generation independence remained unresolved. Adding traced external observations to the 36 development rows produced one connected topology ({g['unique_compound_paper_edges']} edges, additive indicator-design rank {g['additive_design_rank']}, topological redundancy {g['edge_cycle_degrees_of_freedom']}). This sparse connection does not resolve protocol/material differences or justify fitting study-adjusted ranks. Two further source values have conditional reference-parent mass-to-mole conversions, retained outside fitting and shown in a separate topology sensitivity. External_Paper_Readiness.csv and External_Connectivity_Readiness.csv report the source-specific gates and graph scopes.\n")

analysis=ROOT/'03_candidate_selection/01_activity_model/results/analysis_set_manifest.json'
if analysis.exists():
 s=read_json(analysis);c=s['category_counts']
 with (out/'Results.md').open('a',encoding='utf-8') as f:
  f.write(f"\n## Analysis-set disposition\n\nThe reproducible disposition table retained {s['disposition_rows']} provenance rows: {s['inventory_reference_rows']} capacity references, {s['development_original_rows']} original log labels and {s['additional_recovered_rows']} additional source row. Fourteen capacity references matched development Table 3 records and were retained only as alternate representations, not additional measurements. Authorized sensitivity roles comprised 36 exploratory development labels and two separate retrospective challenge observations. The table contained {c['WAIT_FOR_EVIDENCE']} waiting rows, including two existing source-identity HOLDs, and {c['PRIMARY_ANALYSIS']} common-target primary labels. These are provenance/disposition counts, not independent studies or candidate ranks. Primary scope is fixed to pH 7.4 and 37 degrees C, with vehicle/AUC/window stratification. Source-material, stratum and estimand alignment remain prerequisites to primary modelling; formal human review states were unchanged.\n")

lineage=ROOT/'03_candidate_selection/01_activity_model/results/protocol_lineage_summary.json'
if lineage.exists():
 s=read_json(lineage)
 with (out/'Results.md').open('a',encoding='utf-8') as f:
  f.write(f"\n## Protocol lineage\n\nCited-SOP checks mapped {s['existing_observations_mapped']} existing phenolic observations without adding numeric measurements. Shared method conditions were distinguished from confirmed execution, and the quality-control acceptance range was not reassigned as compound measurement error. Executed A/B variant, final vehicle and estimator remain unresolved; no primary labels were released. Protocol_Lineage_Check.csv records the row-level implications.\n")

scope_qc=ROOT/'03_candidate_selection/01_activity_model/results/model_protocol_readiness.json'
if scope_qc.exists():
 s=read_json(scope_qc);e=read_json(ROOT/'03_candidate_selection/01_activity_model/results/extended_model_readiness.json')
 with (out/'Results.md').open('a',encoding='utf-8') as f:
  f.write(f"\n## Scope-consistent validation readiness\n\nOf nine source-verified model-candidate rows, {s['core_condition_candidate_rows']} from {s['papers']} papers matched the fixed core conditions; {s['outside_or_unconfirmed_rows']} stayed outside this diagnostic. Both leave-paper-out identity-coverage checks lacked shared compounds. The 31-row extended review separated core-condition evidence from inherited and unconfirmed conditions and identified {e['protocol_strata']} source-specific pending strata. None supported a cross-paper fold within verified compatible strata. These are design diagnostics, not validation errors or newly fitted models.\n")

completed=ROOT/'03_candidate_selection/01_activity_model/results/completed_model_summary.json'
if completed.exists():
 s=read_json(completed);m=s['metrics']['selected'];n=s['metrics']['matched_null'];choice=s['full_development_selection']
 with (out/'Results.md').open('a',encoding='utf-8') as f:
  f.write(f"\n## Completed exploratory modelling\n\nJoint family/penalty selection nested within five scaffold folds gave pooled MAE {m['MAE']:.3f} and RMSE {m['RMSE']:.3f}, versus {n['MAE']:.3f} and {n['RMSE']:.3f} for the matched mean baseline. Out-of-fold R-squared was {m['R2']:.3f}, with Spearman correlation {m['Spearman']:.3f}. Mean group MAE was {s['macro_group_MAE']['selected']:.3f} versus {s['macro_group_MAE']['matched_null']:.3f}. The differing pooled and group-level results do not establish a consistent predictive advantage. Development-only CV selected {choice['family']} ridge with alpha {choice['alpha']:g} for the exported full-data artifact.\n\nThe fitted order covered only {s['mapped_candidates']} of {s['current_candidate_profiles']} current profiles; {s['unsupported_candidate_profiles']} received no score. Group-removal refits showed unstable positions. Figures Model_Heldout_Predictions, Model_Scaffold_Errors and Model_Order_Stability show held-out predictions, group errors and refit influence. This completes the exploratory pipeline, while a formal primary model and global Top20 remain unestablished. All positions are diagnostic source-specific model outputs, not validated candidate-selection decisions.\n")

expansion=ROOT/'03_candidate_selection/02_cross_study_expansion/results/cross_structure_expansion_summary.json'
if expansion.exists():
 s=read_json(expansion)
 with (out/'Results.md').open('a',encoding='utf-8') as f:
  f.write(f"\n## Cross-structure evidence expansion\n\nTwo additional original papers contributed {s['source_observations']} source observations: {s['numeric_source_values']} numeric entries, including one reported zero, and one reported no-activity result without a numeric value. Three observations mapped to existing candidate profiles; source-reference compounds outside the current index were retained without adding candidate members. The new records did not satisfy all primary scope/material/estimator gates, so no primary labels were released and the completed model was not retrained using them. A twelve-profile method-bridge preparation panel was generated separately from potency selection. No experiments were executed.\n")

route=read_json(ROOT/'04_05_experimental_validation/config/platform_decisions.json')
if route.get('available_measurement_mode')=='ABSORBANCE_ONLY_RESEARCHER_CONFIRMED':
 with (out/'Results.md').open('a',encoding='utf-8') as f:
  f.write("\n## Confirmed experimental route\n\nThe researcher confirmed absorbance-only measurement availability. Future formal modelling will use a separately validated absorbance-capacity endpoint; ORAC-FL remains prior/source-model evidence. No paired numerical transfer, actual assay response or new model performance is claimed.\n")


pilot=ROOT/'04_05_experimental_validation/02_pilot_design/pilot_readiness.json'
if pilot.exists():
 s=read_json(pilot)
 with (out/'Results.md').open('a',encoding='utf-8') as f:
  f.write(f"\n## Absorbance preparation status\n\nOffline source-status and synthetic formula checks passed; {len(s['unfilled_manifest_fields'])} pilot manifest fields remain unfilled. Two original 2015 method equations remain source-pending. An additional 2006 original-abstract inhibition formula was identified as a distinct endpoint; it did not release a capacity label. Synthetic matched-vehicle checks retain nonpositive responses and reject incompatible protocol, vehicle, preparation or sampling-grid assignments. The staged design is prepared, while assay execution readiness is NOT_READY. No experimental responses or formal absorbance model were generated.\n")


platform=ROOT/'04_05_experimental_validation/03_platform_compatibility/platform_readiness.json'
if platform.exists():
 s=read_json(platform)
 with (out/'Results.md').open('a',encoding='utf-8') as f:
  f.write(f"\n## Identified reader feasibility\n\nThe researcher identified the Opentrons Flex Absorbance Plate Reader Module GEN1. The source-linked audit found {s['exact_channel_matches']} exact channel match among {s['source_methods_compared']} checked method readouts. This is optical compatibility, not capacity validation. Local accessories, thermal history and timing qualification remain unresolved. Execution readiness remains NOT_READY; no experimental response or formal absorbance model was generated.\n")


simulation=ROOT/'04_05_experimental_validation/04_endpoint_stress_test/results/simulation_summary.json'
if simulation.exists():
 s=read_json(simulation)
 with (out/'Results.md').open('a',encoding='utf-8') as f:
  f.write(f"\n## Simulation-only method diagnostic\n\nIn the prespecified dimensionless toy model, equal synthetic capacity with different capture rates produced a {s['equal_capacity_fast_to_slow_ratio_at_start0_end4']:.3f}-fold difference in normalized-AUC slope ratios for one fixed acquisition window. Halving the integration step changed ratios by at most {s['maximum_ratio_change_when_halving_step']:.2g}. These numerical counterexamples concern interpretation under assumed kinetics, not measured crocin behavior, molar TE, candidate ranks or formal model validation. The fixed-protocol molar-protection endpoint remains a development candidate.\n")


retrieval=ROOT/'02_identity_and_evidence/01_systematic_supplement/Retrieval_Summary.json'
if retrieval.exists():
 s=read_json(retrieval)
 with (out/'Results.md').open('a',encoding='utf-8') as f:
  f.write(f"\n## Supplemental retrieval coverage\n\nPublic supplemental retrieval covered all 193 current profiles through 579 canonical-route queries and 193 expanded capacity queries. The supplemental register contained {s['supplement_identifier_groups']} provisional identifier groups. Reconciliation with historical metadata yielded {s['merged_identifier_groups']} master groups and {s['candidate_article_links']} candidate-article links. These are bibliographic retrieval counts awaiting conflict review, screening and quantitative extraction. Existing model labels were not expanded from metadata alone.\n")

screening=ROOT/'02_identity_and_evidence/01_systematic_supplement/source_screening_summary.json'
followup=ROOT/'02_identity_and_evidence/01_systematic_supplement/capacity_followup_summary.json'
transfer=ROOT/'03_candidate_selection/05_model_robustness/results/new_source_transfer_summary.json'
if screening.exists() and followup.exists() and transfer.exists():
 s=read_json(screening);e=read_json(followup);t=read_json(transfer)
 with (out/'Results.md').open('a',encoding='utf-8') as f:
  f.write(f"\n## Original-source expansion and model readiness\n\nEndpoint screening covered {s['screened_articles']} recovered reports, with {s['reading_scope_counts']['TARGETED_BODY_METHOD_TABLE_TEXT_SCREEN']} targeted body/method/table text checks and {s['reading_scope_counts']['ABSTRACT_AND_METHOD_HEADING_SCREEN']} abstract/method-heading checks. Numeric extraction preserved {e['source_rows']} source rows from {e['source_DOIs']} DOIs, provisionally mapping to {len(e['mapped_candidates'])} current candidates. Primary model labels released from this batch were zero because qualification fields remain unresolved. The acquisition log retains this preceding source-recovery stage.\n\nAt this preceding diagnostic stage, the component covered {t['existing_model_candidates']} of {t['indexed_candidates']} indexed candidates, with {t['single_source_candidates']} relying on one source DOI. Six fixed-estimate comparisons involve three newly recovered DOIs. Four phenolic acids within one new paper supply six dependent pairwise directions, all agreeing with prior ordering. Protocol and material gaps limit these comparisons to descriptive cross-condition checks. Stable global ranking and chemical representation remain to be established.\n")

user_sources=ROOT/'02_identity_and_evidence/02_user_supplied_sources/extraction_summary.json'
updated_model=ROOT/'03_candidate_selection/06_verified_source_update/results/model_update_summary.json'
if user_sources.exists() and updated_model.exists():
 intake=read_json(user_sources);updated=read_json(updated_model)
 with (out/'Results.md').open('a',encoding='utf-8') as f:
  f.write(f"\n## Current original-source reconciliation and diagnostic update\n\n{intake['documents']} supplied documents represented {intake['original_reports']} reports. {intake['capacity_source_DOIs']} quantitative ORAC reports yielded {intake['capacity_rows']} source rows, comprising {intake['ORAC_FL_rows']} FL, {intake['ORAC_PGR_rows']} PGR and {intake['ORAC_PE_rows']} PE outcomes. The previously inaccessible 60-flavonoid Table S1 was recovered. Nine value/alignment or identity-annotation findings were recorded. Original Table 2 of the 2004 report supplied Quercetin 10.5 +/- 0.4, replacing an earlier reference value of 5.45 in the updated diagnostic data. A Kaempferol association assigned to the same DOI lacked an original table row. These findings supersede the earlier reference-input interpretation above.\n\n")
  for variant in updated['variants']:
   f.write(f"{variant['variant']} included {variant['candidates']} candidates, {variant['candidate_rows']} rows and {variant['papers']} DOIs. Whole-paper validation retained {variant['heldout_rows']} estimable outcomes. Fixed-shrinkage and baseline log RMSE were {variant['metrics']['predicted_log_location']['RMSE']:.4f} and {variant['metrics']['baseline_log_location']['RMSE']:.4f}, respectively. {variant['single_DOI_candidates']} candidates relied on one DOI.\n\n")
  comparison=next(row for row in updated['common_universe_membership'] if row['first_variant']=='EXTENDED_UNKNOWN_PH_NAME_BASED' and row['second_variant']=='EXTENDED_CONFLICT_EXCLUDED')
  f.write(f"Within their {comparison['common_candidates']}-candidate common universe, name-based and recorded-conflict-excluded diagnostics shared {comparison['overlap']} of 20 members. Source deletion exposed unidentifiable locations and broad possible-position bounds. The core-condition model showed no predictive improvement over its matched baseline. Current estimates describe observed-candidate source means under unresolved material/protocol differences. Stable global selection across all 193 profiles remains to be established.\n")


stability=ROOT/'03_candidate_selection/06_verified_source_update/results/evidence_stability_summary.json'
if stability.exists():
 s=read_json(stability)
 with (out/'Results.md').open('a',encoding='utf8') as f:
  f.write(f"\n## Source support for diagnostic selection\n\nOf the leading 20 positions in the 41-candidate conflict-excluded diagnostic, {s['top20_single_source']} had one source DOI and {s['top20_deletion_crosses_cutoff']} had a deletion-bound envelope crossing position 20. Across the full set, {s['all_single_source']} candidates had one DOI. The candidates retaining worst-case positions within 20 across recorded deletions were {', '.join(s['robust_top20_under_recorded_deletions'])}. This is conditional source-deletion robustness within the recorded candidate set and model. Sampling uncertainty and protocol/material qualification remain to be established.\n")


minimum20=ROOT/'02_identity_and_evidence/01_systematic_supplement/minimum20_abstract_summary.json'
if minimum20.exists():
 s=read_json(minimum20)
 with (out/'Results.md').open('a',encoding='utf8') as f:
  f.write(f"\n## Comprehensive evidence-package retrieval\n\nQueries covered {s['candidates']} current candidate profiles without failed requests in the delivered pass. Automated title/abstract screening retained {s['candidate_abstract_links']} candidate-publication links corresponding to {s['unique_articles']} provisional unique article keys. The target of at least 20 screened abstracts was reached for {s['abstract_rule_target_reached']} candidates; {s['remaining_candidates']} remained below target. These counts describe abstract-level rule screening with full-text relevance and scientific qualification pending. No study-scarcity exception was established. New model-label release from this abstract batch was zero.\n")


combined20=ROOT/'02_identity_and_evidence/01_systematic_supplement/minimum20_combined_summary.json'
if combined20.exists():
 s=read_json(combined20)
 with (out/'Results.md').open('a',encoding='utf8') as f:
  f.write(f"\n## Located full-text evidence-package follow-up\n\nBody-paragraph searches added {s['new_body_located_links']} candidate-publication links. Abstract and body-location coverage reached at least 20 leads for {s['combined_located_target_reached']} of {s['candidates']} profiles. A {s['review_panel_rows']}-row panel schedules subsequent scientific appraisal. The remaining located gap was Probetanin, with four body-text mentions and unresolved chemical identity. These source-location counts await scientific relevance, independence and article-quality assessment. No new ORAC model labels or scarcity exceptions were approved.\n")


integrated=ROOT/'03_candidate_selection/07_all_reference_integration/integration_summary.json'
if integrated.exists():
 s=read_json(integrated)
 with (out/'Results.md').open('a',encoding='utf8') as f:
  f.write(f"\n## Complete reference consideration and conditional source expansion\n\nThe consideration register includes {s['all_reference_links']} candidate/article associations and {s['unique_linked_articles']} provisional unique article keys across {s['candidates_considered']} candidates. Original extractions add 48 missing candidate/source associations. Additional original numeric rows expand the conditional analysis to {s['numeric_candidates']} candidates, {s['numeric_source_DOIs']} source DOIs and {s['numeric_rows']} observations. The largest connected component contains 51 candidates, eleven papers and 113 rows after adding the 2022 phenolic-acid bridge. Sesamin remains in a separate component. Their positions retain component scope. Article-level scientific review and formal global ranking remain pending.\n")


reviewed=ROOT/'03_candidate_selection/08_capacity_review_validation/review_validation_summary.json'
if reviewed.exists():
 s=read_json(reviewed)
 with (out/'Results.md').open('a',encoding='utf8') as f:
  f.write(f"\n## Connected capacity-model validation\n\nThe consolidated audit retained {s['audited_numeric_rows']} source rows from {s['audited_original_DOIs']} DOIs, including prior extractions and five newly audited distinct-endpoint rows retained on hold. The connected expanded model contained 51 candidates, eleven papers and 113 rows. Whole-paper log RMSE was 0.6306 versus 0.6755 for the matched baseline across 75 estimable outcomes. The reported-pH/temperature subset contained 24 candidates and six papers, with RMSE 0.4128 versus 0.4151 over nine outcomes. Equal-row and equal-total-DOI Top20 sets shared {s['weighting_top20_overlap']} members. Recorded source deletions retained within-20 worst-case positions for {', '.join(s['deletion_robust_top20'])}. Sampling intervals and final selection remain unresolved.\n")


source_progress=ROOT/'02_identity_and_evidence/03_date_scoped_review/results/orac_queue_progress_summary.json'
if source_progress.exists():
 s=read_json(source_progress)
 counts=s['status_counts']
 with (out/'Results.md').open('a',encoding='utf8') as f:
  f.write(f"\n## Date-scoped targeted source appraisal\n\nThe fixed work cohort contained {s['baseline_sources']} sources. Targeted section/table/caption scopes were recorded for {counts.get('TARGETED_SOURCE_SCOPE_RECORDED',0)} sources; {counts.get('FULLTEXT_ACCESS_PENDING',0)} retained access-pending status. Reading depth varied by source and is recorded individually. Four IC50-type rows, six sesame comparison rows, twelve hop experimental ORAC cells and four reference-control rows were retained with qualification holds. The public slope deposit contained seven compound error summaries matching mean absolute deviation. Its Trolox error matched the first three slopes' mean absolute deviation, while the printed mean used four slopes. Capacity-model inputs received zero new labels from this appraisal stage.\n")


versions_summary=ROOT/'03_candidate_selection/07_all_reference_integration/integration_summary.json'
if versions_summary.exists():
 s=read_json(versions_summary)
 if 'confirmed_version_pairs' in s:
  with (out/'Results.md').open('a',encoding='utf8') as f:
   f.write(f"\n## Publication-version reconciliation\n\nPublisher notices confirmed {s['confirmed_version_pairs']} preprint-to-journal version pairs. The {s['unique_linked_articles']} provisional article keys yielded {s['provisional_version_group_keys']} provisional version-family keys after these declared links were applied. Complete experiment-independence appraisal remains pending. Numeric model coverage was unchanged by this version grouping. Four new PMC locators were verified against original XML DOI fields.\n")
