"""Build manuscript-facing descriptive results and tables; never invent experimental outcomes."""
from pathlib import Path
import sys,collections
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'00_project'))
from pipeline_io import *
discovery=read_csv(ROOT/'01_candidate_discovery/results/discovery_register.csv')
profiles=read_csv(ROOT/'02_identity_and_evidence/results/candidate_evidence_profiles.csv')
queue=read_csv(ROOT/'03_candidate_selection/results/top20_review_queue.csv')
sensitivity=read_csv(ROOT/'03_candidate_selection/results/selection_sensitivity.csv')
summary=read_json(ROOT/'03_candidate_selection/results/selection_summary.json')
identity=sum(r['identity_reference_status']=='REFERENCE_IDENTIFIERS_AND_FORMULA_PRESENT' for r in profiles)
scope=sum(r['scope_disposition']=='RETAIN_FOR_IDENTITY_AND_FOOD_VERIFICATION' for r in profiles)
id_scope=sum(r['identity_reference_status']=='REFERENCE_IDENTIFIERS_AND_FORMULA_PRESENT' and r['scope_disposition']=='RETAIN_FOR_IDENTITY_AND_FOOD_VERIFICATION' for r in profiles)
metrics=[('Discovery records',len(discovery),'191 literal legacy seed names + 12 rescreened exclusions + 1 targeted gap'),('Identity/evidence profiles',len(profiles),'191 preserved IDs + food-derived glutathione reopening + ergothioneine gap'),('Reference identity and formula present',identity,'CID, InChIKey and formula; not a lot identity certificate'),('Molecular-scope profiles',scope,'Unspecified elemental-nutrient labels retained as context only'),('Identity-complete molecular-scope profiles',id_scope,'Food occurrence still requires candidate-specific verification'),('In the existing 157-candidate framework',sum(r['framework157_scope']=='YES' for r in profiles),'Coverage boundary, not an activity exclusion'),('Review-queue eligible',summary['queue_eligible'],'At least one checked original chemical source; dietary uncertainty flags held'),('Provisional review slots',len(queue),'Administrative budget preview; not potency ranks'),('Two-confirmed-study sensitivity',next(int(r['eligible_count']) for r in sensitivity if r['scenario']=='TWO_CONFIRMED_STUDIES_ONLY'),'Reliability criterion only'),('Laboratory-ready panel',summary['formal_lab_ready'],'Actual material, food-source, interference and human decision gates')]
write_csv(ROOT/'06_manuscript/tables/Table_1_Discovery_and_Selection_Flow.csv',[{'stage':a,'count':b,'interpretation':c} for a,b,c in metrics])
fields=['review_slot','candidate_id','compound_name','molecular_formula','pubchem_cid','inchi_key','confirmed_independent_horac_studies','confirmed_horac_source_dois','shortlist_status']
write_csv(ROOT/'06_manuscript/tables/Table_2_Provisional_Review_Panel.csv',[{k:r[k] for k in fields} for r in queue])
frozen=read_csv(source('data/h_orac_stage25b/frozen/Stage25B_Frozen_Primary_HORAC_Top20.csv'));old={r['candidate_id'] for r in frozen};new={r['candidate_id'] for r in queue}
comparison=[]
names={r['candidate_id']:r['compound_name'] for r in profiles}
for cid in sorted(old|new):comparison.append({'candidate_id':cid,'compound_name':names[cid],'legacy_frozen_member':'YES' if cid in old else 'NO','current_review_preview_member':'YES' if cid in new else 'NO','interpretation':'Different purpose and gates; no modification of frozen ranking'})
write_csv(ROOT/'06_manuscript/tables/Table_3_Preview_and_Frozen_Reference.csv',comparison)
write_csv(ROOT/'06_manuscript/tables/Table_S1_Identity_and_Food_Gaps.csv',[{k:r[k] for k in ['candidate_id','compound_name','molecular_formula','identity_reference_status','food_occurrence_status','food_source_locator','chemical_form_and_lot_status']} for r in profiles])
method=read_json(ROOT/'04_absorbance_assay/inputs/primary_method_registry.json')
write_csv(ROOT/'04_absorbance_assay/results/method_comparison.csv',method)
out=ROOT/'06_manuscript';out.mkdir(exist_ok=True)
lines=['# Results: source-bounded candidate discovery and screening preparation','',f'As of {AS_OF}, the reproducible discovery register contained {len(discovery)} records: 191 names reconstructed from the original class-based enumeration, 12 preserved exclusion records rescreened under the current food-source rule, and one targeted ergothioneine addition. The register is a versioned discovery collection, not an exhaustive census of food chemicals.','',f'The workflow produced {len(profiles)} candidate identity/evidence profiles; {identity} had reference CID, InChIKey and formula, while {id_scope} also met the molecular-form scope check. The existing five-dimensional framework covered 157 preserved candidates. Other profiles were labelled outside that snapshot instead of assigned negative evidence.','',f'{summary["queue_eligible"]} candidates met the review-queue gates using preserved candidate-specific source closure. The two-confirmed-study sensitivity retained {metrics[8][1]}. A {len(queue)}-slot administrative preview was produced, with {summary["cutoff_tied_count"]} candidates in the cutoff evidence stratum; all tied candidates remain visible for researcher adjudication. Candidate IDs resolve display order only.','',f'The preview overlapped the frozen H-ORAC Top20 in {len(old&new)} candidates; {len(new-old)} preview candidates were outside the frozen set and {len(old-new)} frozen members were outside the preview. This is a comparison of different selection purposes, not a revised activity ranking.','',f'{summary["formal_lab_ready"]} profiles met all laboratory-ready gates. No new absorbance assay results, effective concentrations, causal targets or human benefits were generated.','', 'Tables 1-3 report the discovery flow, reference formulas/source-linked review panel, and comparison with the frozen reference. Table S1 records identity/food-source gaps. Figures 1-3 visualize screening preparation only.','', '## Suggested manuscript use','', 'These are descriptive workflow results suitable for a methods-development or candidate-prioritization manuscript. Laboratory efficacy, dose-response and mechanism Results remain unwritten until real data and adjudications exist.']
(out/'Results.md').write_text('\n'.join(lines)+'\n',encoding='utf8')
claims=[{'claim':'A versioned food-chemical discovery workflow was implemented','section':'Methods 1; Results 1','support':'Table 1; discovery_register.csv; original enumeration hash','status':'SUPPORTED_WITH_EXPLICIT_COVERAGE_LIMIT'}, {'claim':'Reference identity and formula are available for review candidates','section':'Methods 2; Results 2','support':'Table 2; PubChem raw responses and access log','status':'REFERENCE_IDENTITY_ONLY_NOT_REAGENT_CERTIFICATION'}, {'claim':'20 review slots are proposed','section':'Results 3','support':'Table 2; selection_rules.json; cutoff_tied_candidates.csv','status':'PROVISIONAL_ADMINISTRATIVE_PREVIEW_NOT_FINAL_TOP20'}, {'claim':'Non-fluorescent capacity endpoint candidates were compared','section':'Methods 4; Discussion','support':'Primary method registry; Step 04.1 endpoint comparison','status':'METHOD_PROPOSAL_NOT_VALIDATED_ON_USER_PLATFORM'}, {'claim':'Candidates have experimentally measured activity in the new assay','section':'Future Results','support':'No current experimental data','status':'NOT_SUPPORTED_DO_NOT_WRITE'}, {'claim':'Mechanism observations are validated direct targets','section':'Future mechanistic Results','support':'AFF0061 observations remain NOT_REVIEWED','status':'NOT_SUPPORTED_DO_NOT_WRITE'}]
write_csv(out/'tables/Manuscript_Claim_Map.csv',claims)
write_json(ROOT/'07_quality_control/descriptive_summary.json',{'metrics':[{'stage':a,'count':b} for a,b,_ in metrics],'frozen_preview_overlap':len(old&new),'new_preview_members':sorted(new-old),'omitted_frozen_reference_members':sorted(old-new),'publication_claim_limits_recorded':True})
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

route=read_json(ROOT/'04_absorbance_assay/config/platform_decisions.json')
if route.get('available_measurement_mode')=='ABSORBANCE_ONLY_RESEARCHER_CONFIRMED':
 with (out/'Results.md').open('a',encoding='utf-8') as f:
  f.write("\n## Confirmed experimental route\n\nThe researcher confirmed absorbance-only measurement availability. Future formal modelling will use a separately validated absorbance-capacity endpoint; ORAC-FL remains prior/source-model evidence. No paired numerical transfer, actual assay response or new model performance is claimed.\n")


pilot=ROOT/'04_absorbance_assay/02_pilot_design/pilot_readiness.json'
if pilot.exists():
 s=read_json(pilot)
 with (out/'Results.md').open('a',encoding='utf-8') as f:
  f.write(f"\n## Absorbance preparation status\n\nOffline source-status and synthetic formula checks passed; {len(s['unfilled_manifest_fields'])} pilot manifest fields remain unfilled. Two original 2015 method equations remain source-pending. An additional 2006 original-abstract inhibition formula was identified as a distinct endpoint; it did not release a capacity label. Synthetic matched-vehicle checks retain nonpositive responses and reject incompatible protocol, vehicle, preparation or sampling-grid assignments. The staged design is prepared, while assay execution readiness is NOT_READY. No experimental responses or formal absorbance model were generated.\n")


platform=ROOT/'04_absorbance_assay/03_platform_compatibility/platform_readiness.json'
if platform.exists():
 s=read_json(platform)
 with (out/'Results.md').open('a',encoding='utf-8') as f:
  f.write(f"\n## Identified reader feasibility\n\nThe researcher identified the Opentrons Flex Absorbance Plate Reader Module GEN1. The source-linked audit found {s['exact_channel_matches']} exact channel match among {s['source_methods_compared']} checked method readouts. This is optical compatibility, not capacity validation. Local accessories, thermal history and timing qualification remain unresolved. Execution readiness remains NOT_READY; no experimental response or formal absorbance model was generated.\n")


simulation=ROOT/'04_absorbance_assay/04_endpoint_stress_test/results/simulation_summary.json'
if simulation.exists():
 s=read_json(simulation)
 with (out/'Results.md').open('a',encoding='utf-8') as f:
  f.write(f"\n## Simulation-only method diagnostic\n\nIn the prespecified dimensionless toy model, equal synthetic capacity with different capture rates produced a {s['equal_capacity_fast_to_slow_ratio_at_start0_end4']:.3f}-fold difference in normalized-AUC slope ratios for one fixed acquisition window. Halving the integration step changed ratios by at most {s['maximum_ratio_change_when_halving_step']:.2g}. These numerical counterexamples concern interpretation under assumed kinetics, not measured crocin behavior, molar TE, candidate ranks or formal model validation. The fixed-protocol molar-protection endpoint remains a development candidate.\n")


retrieval=ROOT/'02_identity_and_evidence/01_systematic_supplement/Retrieval_Summary.json'
if retrieval.exists():
 s=read_json(retrieval)
 with (out/'Results.md').open('a',encoding='utf-8') as f:
  f.write(f"\n## Supplemental retrieval coverage\n\nPublic supplemental retrieval covered all 193 current profiles through 579 canonical-route queries and 193 expanded capacity queries. The supplemental register contained {s['supplement_identifier_groups']} provisional identifier groups. Reconciliation with historical metadata yielded {s['merged_identifier_groups']} master groups and {s['candidate_article_links']} candidate-article links. These are bibliographic retrieval counts awaiting conflict review, screening and quantitative extraction. Existing model labels were not expanded from metadata alone.\n")
