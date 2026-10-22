import fs from 'node:fs/promises';
import path from 'node:path';
import {execFileSync} from 'node:child_process';
import {workspace,root,pilot,ROLE,PROPOSED,DATE,json,sha,missing,readCSV,inputs,verifiedEligible} from './migration_lib.mjs';
import {build} from './build_dryrun.mjs';
import {accepted} from './policy_v02.mjs';
import {reconstruct} from './reconstruct_legacy.mjs';

const checks=[];const check=(id,pass,detail)=>checks.push({id,pass:!!pass,detail});
const contract=JSON.parse(await fs.readFile(path.join(workspace,'schema/Table_Contract_v0.2.json'),'utf8'));
const input=await inputs();const tables={};
for(const [name,def]of Object.entries(contract.tables))tables[name]=(await readCSV(path.join(workspace,def.path))).rows;
const vocab=input.vocabulary.rows.filter(r=>!['FIELD_RULE_NOT_ENUM','MULTIVALUE_CONSTRAINT'].includes(r.scope));
const allowed=field=>new Set(vocab.filter(r=>r.field===field).map(r=>r.value));
const enumFields=new Set(['evidence_relation_type','target_confirmation_class','antioxidant_relevance_primary','dose_basis','redox_measurement_level','readout_level','result_direction','result_significance','source_scope','source_issue','missing_reason','independence_relation']);

function structuralErrors(t){
 const issues=[];
 for(const [name,def]of Object.entries(contract.tables)){
  const rows=t[name];const keys=new Set();
  for(const r of rows){const k=json(def.primary_key.map(c=>r[c]));if(def.primary_key.some(c=>r[c]==='')||keys.has(k))issues.push('DUPLICATE_OR_EMPTY_PK:'+name);keys.add(k);
   if(r.dataset_role!==ROLE||r.schema_version!=='0.2_DRYRUN')issues.push('PRODUCTION_MARKER:'+name);
   for(const fk of def.foreign_keys){if(fk.nullable&&r[fk.column]==='')continue;if(!t[fk.table].some(x=>x[fk.target]===r[fk.column]))issues.push('ORPHAN_FK:'+name+'.'+fk.column);}
  }
 }
 for(const p of t.Scientific_Proposal){
  let value;try{value=JSON.parse(p.proposed_value_json);}catch{issues.push('INVALID_JSON');continue;}
  if(p.proposal_status!==PROPOSED||p.applied_to_production!=='NO'||p.approval_event_id!=='')issues.push('PROPOSAL_APPLIED_OR_APPROVED');
  if(value===null){if(!allowed('missing_reason').has(p.missing_reason))issues.push('NULL_WITHOUT_REASON');}
  else if(p.field_name==='antioxidant_relevance_secondary'){
   if(!Array.isArray(value)||new Set(value).size!==value.length||value.some(v=>!allowed('antioxidant_relevance_primary').has(v)||v==='UNRESOLVED'))issues.push('INVALID_ENUM:secondary');
   const primary=t.Scientific_Proposal.find(x=>x.evidence_id===p.evidence_id&&x.field_name==='antioxidant_relevance_primary');
   if(primary&&value.includes(JSON.parse(primary.proposed_value_json)))issues.push('SECONDARY_DUPLICATES_PRIMARY');
  }else if(enumFields.has(p.field_name)&&!allowed(p.field_name).has(value))issues.push('INVALID_ENUM:'+p.field_name);
  if(p.missing_reason&&!allowed('missing_reason').has(p.missing_reason))issues.push('INVALID_ENUM:missing_reason');
 }
 for(const s of t.Source_Check)if(!allowed('source_scope').has(s.source_scope)||!allowed('source_issue').has(s.source_issue)||s.mapping_status!==PROPOSED)issues.push('INVALID_SOURCE_MAPPING');
 for(const i of t.Independence_Assessment)if(i.independence_relation!=='UNRESOLVED_REUSE'||i.mapping_status!==PROPOSED)issues.push('UNSUPPORTED_INDEPENDENCE');
 for(const r of t.Review_Event)if(r.approval_status!=='PENDING_HUMAN_REVIEW'||r.reviewer_type!=='CODEX_ASSISTED_SCIENTIFIC_REVIEW'||r.change_applied!=='NO'||r.decision!=='PENDING'||r.signed_by||r.signoff_reference)issues.push('UNAUTHORIZED_APPROVAL');
 for(const m of t.Legacy_ID_Map){const def=contract.tables[m.new_table];if(!def||def.primary_key.length!==1||!t[m.new_table].some(r=>r[def.primary_key[0]]===m.new_id))issues.push('DYNAMIC_ORPHAN_FK');}
 for(const o of t.Observation){
  const source=input.evidence.rows.find(r=>r.evidence_id===o.evidence_id);
  if(!source){issues.push('NEW_OBSERVATION');continue;}
  if(o.raw_evidence_relation_type!==source.evidence_relation_type||o.raw_human_review_status!==source.human_review_status)issues.push('SCIENTIFIC_OVERWRITE');
  if(o.scientific_approval_status!=='PENDING_HUMAN_REVIEW'||!['HOLD','PROVISIONAL'].includes(o.sandbox_review_state))issues.push('UNAUTHORIZED_APPROVAL');
  if(o.experiment_id!==source.experiment_id||o.material_id)issues.push('AUTOMATIC_EXPERIMENT_OR_MATERIAL_MERGE');
  const exposure=t.Intervention.find(i=>i.evidence_id===o.evidence_id);
  const src=t.Source_Check.find(s=>s.source_check_id===o.source_check_id);
  const experiment=t.Experiment.find(e=>e.experiment_id===o.experiment_id);
  if(!src||src.evidence_id!==o.evidence_id||src.publication_id!==o.publication_id||!experiment||experiment.publication_id!==o.publication_id||!exposure||exposure.intervention_id!==o.intervention_id||exposure.experiment_id!==o.experiment_id)issues.push('CROSS_ENTITY_SEMANTIC_LINK');
  if(!exposure||exposure.raw_dose!==source.dose||exposure.raw_dose_unit!==source.dose_unit)issues.push('DOSE_OVERWRITE_OR_MISSING_AS_ZERO');
  if(exposure&&missing(source.dose)&&exposure.raw_dose==='0')issues.push('MISSING_AS_ZERO');
 }
 for(const view of ['Verified_Direct_Targets','Verified_Antioxidant_Mechanisms','Verified_Evidence_Support'])if(t[view].length)issues.push('UNAPPROVED_OR_HOLD_IN_VERIFIED_VIEW');
 return [...new Set(issues)];
}

for(const [name,def]of Object.entries(contract.tables)){
 const keys=tables[name].map(r=>json(def.primary_key.map(c=>r[c])));
 check('pk_'+name,new Set(keys).size===keys.length&&!tables[name].some(r=>def.primary_key.some(c=>!r[c])),{rows:keys.length,key:def.primary_key});
}
const errors=structuralErrors(tables);check('all_foreign_keys_enums_and_scientific_guards',!errors.length,{violations:errors});
check('original_ids_exact',tables.Observation.length===21&&json(tables.Observation.map(r=>r.evidence_id).sort())===json(input.evidence.rows.map(r=>r.evidence_id).sort()),'21 original IDs; no invented 22nd observation');
check('experiment_ids_preserved',tables.Experiment.length===21&&tables.Experiment.every(r=>r.experiment_id===r.legacy_experiment_id&&r.material_id===''&&r.entity_scope==='LEGACY_COMPARISON_NOT_INDEPENDENT_EXPERIMENT'),'21 legacy comparisons retained without material merging or independent-n claim');
check('publication_register_preserved',tables.Publication.length===15&&tables.Publication.filter(p=>Number(p.raw_evidence_record_count)>0).length===10&&input.studies.rows.every(r=>{const p=tables.Publication.find(x=>x.legacy_study_id===r.study_id);return p&&input.studies.headers.every(k=>p['raw_'+k]===r[k]);}),'15 complete register entries, including excluded/background/held entries, 10 with observations');
check('legacy_cell_count',tables.Legacy_Field_Value.length===21*66,'1386 legacy cells stored as exact text');
check('legacy_cells_identical',input.evidence.rows.every(r=>input.dictionary.rows.every(f=>tables.Legacy_Field_Value.find(v=>v.evidence_id===r.evidence_id&&v.field_name===f.field_name)?.raw_value===r[f.field_name])),'every original scientific relationship, identity, unit, status and locator retained');
check('missing_reason_no_false_zero',tables.Legacy_Field_Value.every(v=>v.missing_reason===missing(v.raw_value)&&!(v.missing_reason&&v.raw_value==='0')),'legacy sentinels preserved; absent normalized proposals use JSON null plus reason');
const mapping=await readCSV(path.join(workspace,'schema/Schema_Field_Mapping_v0.2.csv'));
check('66_field_mapping',mapping.rows.length===66&&mapping.rows.every((r,i)=>r.legacy_field===input.dictionary.rows[i].field_name&&r.field_order===String(i+1)&&r.restore_column==='raw_value'),'66 original dictionary fields map deterministically');
check('semantic_columns_exist',mapping.rows.every(r=>contract.tables[r.semantic_table]?.columns.includes(r.semantic_column)), 'all semantic projection references point to actual table columns; EAV remains authoritative for restoration');
check('dynamic_legacy_foreign_keys',tables.Legacy_ID_Map.every(m=>{const def=contract.tables[m.new_table];return def&&def.primary_key.length===1&&tables[m.new_table].some(r=>r[def.primary_key[0]]===m.new_id);}),'all 57 dynamic mappings point to real destination keys');
check('raw_entity_projections_exact',['Observation','Experiment','Intervention','Source_Check','Observation_Target'].every(name=>tables[name].every(row=>{const original=input.evidence.rows.find(r=>name==='Experiment'?r.experiment_id===row.experiment_id:r.evidence_id===row.evidence_id);return original&&Object.entries(row).filter(([k])=>k.startsWith('raw_')&&Object.hasOwn(original,k.slice(4))).every(([k,v])=>v===original[k.slice(4)]);})), 'raw projections match their observation source, not just the audit EAV copy');
check('candidate_and_entity_links',tables.Observation.every(o=>{const r=input.evidence.rows.find(r=>r.evidence_id===o.evidence_id);return o.candidate_id===r.candidate_id&&tables.Source_Check.find(s=>s.source_check_id===o.source_check_id)?.evidence_id===o.evidence_id&&tables.Intervention.find(i=>i.intervention_id===o.intervention_id)?.evidence_id===o.evidence_id;}),'candidate reference and observation-level source/exposure links remain unchanged');
check('source_locators_retained',tables.Source_Check.every(s=>s.raw_source_locator===input.evidence.rows.find(r=>r.evidence_id===s.evidence_id).source_locator&&s.raw_source_figure_or_table===input.evidence.rows.find(r=>r.evidence_id===s.evidence_id).source_figure_or_table&&s.check_mode==='IMPORTED_PRIOR_REVIEW_NOT_NEW_VERIFICATION'),'no new fulltext/image verification claimed');
const held=new Set(input.gate2.rows.filter(r=>r.review_status==='HOLD_SOURCE_VERIFICATION').map(r=>r.evidence_id));
check('hold_isolation',held.size===7&&tables.Observation.filter(o=>o.sandbox_review_state==='HOLD').length===7&&tables.Observation.every(o=>(o.sandbox_review_state==='HOLD')===held.has(o.evidence_id)),'Gate2 7 source holds quarantined only in sandbox; original evidence_status retained');
check('no_autoapproval',tables.Review_Event.every(r=>r.approval_status==='PENDING_HUMAN_REVIEW'&&r.change_applied==='NO')&&tables.Observation.every(o=>o.raw_human_review_status==='NOT_REVIEWED'),'zero unauthorized HUMAN_APPROVED records or signed events');
const newFields=['target_confirmation_class','antioxidant_relevance_primary','antioxidant_relevance_secondary','dose_basis','redox_measurement_level','readout_level','result_direction','result_significance','source_scope','source_issue','missing_reason','independence_relation'];
check('12_new_fields_segregated',newFields.every(field=>tables.Scientific_Proposal.filter(p=>p.field_name===field).length===21)&&tables.Scientific_Proposal.every(p=>p.proposal_status===PROPOSED&&p.applied_to_production==='NO'),'252 required field demonstrations plus 5 preserved specific proposals; none effective production facts');
check('proposal_event_bijection',tables.Scientific_Proposal.length===257&&tables.Review_Event.length===257&&tables.Scientific_Proposal.every(p=>{const e=tables.Review_Event.find(e=>e.review_event_id===p.review_event_id);return e&&e.proposal_id===p.proposal_id&&e.old_value===p.old_value_json&&e.proposed_value===p.proposed_value_json;}),'one pending event per field proposal');
check('old_value_presence_unambiguous',tables.Scientific_Proposal.every(p=>{const r=input.evidence.rows.find(r=>r.evidence_id===p.evidence_id);return Object.hasOwn(r,p.field_name)?p.old_value_presence==='LEGACY_VALUE_PRESENT'&&JSON.parse(p.old_value_json)===r[p.field_name]:p.old_value_presence==='NOT_PRESENT_IN_LEGACY_SCHEMA'&&p.old_value_json==='null';}),'new-field absence is not falsely represented as a prior measured value; legacy context is separate');
check('akt_tyr_case',['ME-AFF0061-37025617-002','ME-AFF0061-11023549-001'].every(id=>tables.Observation.find(o=>o.evidence_id===id).raw_evidence_relation_type==='FUNCTIONAL_CAUSAL'&&tables.Scientific_Proposal.some(p=>p.evidence_id===id&&p.field_name==='evidence_relation_type'&&p.proposed_value==='PATHWAY_MODULATION'&&p.proposal_status===PROPOSED)),'two original FUNCTIONAL_CAUSAL facts + separate proposed PATHWAY_MODULATION');
check('hdac_ns_case',tables.Observation_Target.find(t=>t.evidence_id==='ME-AFF0061-41594941-005').raw_target_effect_direction==='NO_ADDITIONAL_CHANGE'&&tables.Scientific_Proposal.some(p=>p.evidence_id==='ME-AFF0061-41594941-005'&&p.field_name==='result_significance'&&p.proposed_value==='NOT_STATISTICALLY_SIGNIFICANT')&&!tables.Scientific_Proposal.some(p=>p.proposed_value==='EQUIVALENCE_SUPPORTED'),'old wording retained; significance proposal not equivalence');
const nrf=tables.Observation.find(o=>o.evidence_id==='ME-AFF0061-39589556-001');
const s2=tables.Unresolved_Mapping.find(u=>u.issue_id==='UM-NRF2-S2');
check('nrf2_s2_not_6l',s2&&s2.evidence_id===''&&s2.experiment_id===''&&s2.forbidden_link.includes(nrf.experiment_id)&&tables.Experiment.find(e=>e.experiment_id===nrf.experiment_id).raw_experimental_model==='IN_VIVO'&&!tables.Observation.some(o=>/S2|SupplementaryFigure2/i.test(o.raw_observation_endpoint||'')),'S2 is a pending extraction task only; no cell rescue assigned to animal 6L');
check('no_prediction_or_readout_upgrade',input.evidence.rows.filter(r=>r.evidence_relation_type==='COMPUTATIONAL_PREDICTION').every(r=>tables.Scientific_Proposal.some(p=>p.evidence_id===r.evidence_id&&p.field_name==='target_confirmation_class'&&p.proposed_value==='COMPUTATIONAL_ONLY'))&&!tables.Scientific_Proposal.some(p=>p.field_name==='target_confirmation_class'&&p.proposed_value==='DIRECT_BINDING_SUPPORTED'),'3 computational rows remain computational; no direct-binding promotion');
check('bridge_no_count_inflation',tables.Observation_Tag.length===4&&new Set(tables.Observation_Tag.map(t=>t.evidence_id+'::'+t.tag)).size===4&&new Set(tables.Observation.map(o=>o.evidence_id)).size===21,'4 secondary tags; count DISTINCT evidence_id, never bridge rows');
const expanded=tables.Observation.flatMap(o=>{const tags=tables.Observation_Tag.filter(t=>t.evidence_id===o.evidence_id);return tags.length?tags.map(t=>({id:o.evidence_id,tag:t.tag})):[{id:o.evidence_id,tag:null}];});
const fakeExtra={...tables.Observation_Tag[0],tag_id:'FIXTURE-SECOND-TAG',tag:'OTHER_BIOLOGICAL_FUNCTION'};
const fixtureExpanded=tables.Observation.flatMap(o=>[...tables.Observation_Tag,fakeExtra].filter(t=>t.evidence_id===o.evidence_id).map(t=>({id:o.evidence_id,tag:t.tag})).concat(tables.Observation_Tag.some(t=>t.evidence_id===o.evidence_id)?[]:[{id:o.evidence_id,tag:null}]));
check('multitag_distinct_fixture',new Set(expanded.map(x=>x.id)).size===21&&new Set(fixtureExpanded.map(x=>x.id)).size===21,'synthetic extra tag changes joined-row multiplicity without changing unique evidence count; fixture not saved as evidence');
const decisions=await readCSV(path.join(workspace,'Governance_Decision_Diff_v0.1_to_v0.2.csv'));
check('all_24_decisions',decisions.rows.length===24&&new Set(decisions.rows.map(r=>r.decision_id)).size===24&&decisions.rows.every(r=>r.old_rule===input.decisions.rows.find(o=>o.decision_id===r.decision_id).recommendation),'v0.1 rule text retained; v0.2 separate file');
check('15_accepted_9_proposed',decisions.rows.filter(r=>r.recommendation_state==='SCIENTIFIC_RECOMMENDATION_ACCEPTED_PENDING_FORMAL_SIGNOFF').length===15&&decisions.rows.every(r=>accepted.has(r.decision_id)===(r.recommendation_state==='SCIENTIFIC_RECOMMENDATION_ACCEPTED_PENDING_FORMAL_SIGNOFF'))&&decisions.rows.filter(r=>r.recommendation_state==='IMPLEMENTATION_POLICY_PROPOSED_PENDING_FORMAL_SIGNOFF').length===9,'exact authorized IDs and 9 draft implementation policies');
check('governance_signoff_not_invented',decisions.rows.every(r=>r.formal_approval_status==='PENDING_FORMAL_SIGNOFF'&&!r.signed_by&&!r.signoff_date&&r.implemented_in_production==='NO'),'no formal approval or signer invented');

// Deliberate invalid in-memory copies demonstrate detection; no corrupt fixture is written to data.
const clone=()=>structuredClone(tables);
for(const [name,mutate,expected]of [
 ['duplicate_pk',t=>t.Observation.push({...t.Observation[0]}),'DUPLICATE_OR_EMPTY_PK'],
 ['orphan_fk',t=>t.Observation[0].publication_id='FIXTURE-NONEXISTENT','ORPHAN_FK'],
 ['dynamic_orphan_fk',t=>t.Legacy_ID_Map[0].new_id='FIXTURE-NONEXISTENT','DYNAMIC_ORPHAN_FK'],
 ['wrong_observation_source',t=>t.Observation[0].source_check_id=t.Observation[1].source_check_id,'CROSS_ENTITY_SEMANTIC_LINK'],
 ['illegal_enum',t=>{const p=t.Scientific_Proposal.find(p=>p.field_name==='dose_basis');p.proposed_value_json='"FIXTURE-INVALID"';},'INVALID_ENUM'],
 ['fake_approval',t=>t.Review_Event[0].approval_status='HUMAN_APPROVED','UNAUTHORIZED_APPROVAL'],
 ['missing_as_zero',t=>{t.Intervention.find(i=>i.evidence_id==='ME-AFF0061-42413844-001').raw_dose='0';},'MISSING_AS_ZERO'],
 ['overwrite_relation',t=>t.Observation.find(o=>o.evidence_id==='ME-AFF0061-37025617-002').raw_evidence_relation_type='PATHWAY_MODULATION','SCIENTIFIC_OVERWRITE'],
 ['hold_in_view',t=>t.Verified_Direct_Targets.push({dataset_role:ROLE,schema_version:'0.2_DRYRUN',evidence_id:'ME-AFF0061-42170612-001',candidate_id:'AFF-0061',view_scope:'direct'}),'UNAPPROVED_OR_HOLD_IN_VERIFIED_VIEW'],
 ['claim_shared_material',t=>t.Observation[0].material_id='FIXTURE-SHARED','AUTOMATIC_EXPERIMENT_OR_MATERIAL_MERGE']
]){const t=clone();mutate(t);const detected=structuralErrors(t);check('negative_fixture_'+name,detected.some(x=>x.startsWith(expected)),{expected_rejection:expected,detected});}

const fixtureObs={dataset_role:ROLE,evidence_id:'FIXTURE-ONLY',publication_id:'FIXTURE-PUB',sandbox_review_state:'HUMAN_APPROVED',record_version:'FIXTURE-V1'};
const fixtureSource=[{evidence_id:'FIXTURE-ONLY',source_scope:'FULL_TEXT_TEXT_LEGEND',source_issue:'NONE_IDENTIFIED_AT_REVIEW',mapping_status:'APPROVED_SCOPED'}];
const fixtureEvents=[{evidence_id:'FIXTURE-ONLY',review_event_id:'FIXTURE-SIGN',reviewer_type:'HUMAN_SCIENTIFIC_REVIEWER',approval_status:'HUMAN_APPROVED',signed_by:'SYNTHETIC_TEST_ONLY',signoff_reference:'SYNTHETIC_TEST_ONLY',decision:'APPROVE',record_version:'FIXTURE-V1'}];
const fixtureProposals=[{evidence_id:'FIXTURE-ONLY',field_name:'target_confirmation_class',proposal_status:'APPROVED_SCOPED',applied_to_production:'NO',approval_event_id:'FIXTURE-SIGN',proposed_value:'DIRECT_BINDING_SUPPORTED'}];
const fixturePub=[{publication_id:'FIXTURE-PUB',raw_retraction_status:'NO_RETRACTION_LINK_IN_RETRIEVED_PUBMED'}];
check('verified_filter_positive_fixture',verifiedEligible(fixtureObs,fixtureSource,fixtureEvents,fixtureProposals,'direct',fixturePub),'hypothetical signed exact-version/scoped approved combination works; no real HUMAN_APPROVED row created');
check('verified_filter_source_hold_fixture',!verifiedEligible(fixtureObs,[{...fixtureSource[0],source_issue:'CONFLICT'}],fixtureEvents,fixtureProposals,'direct',fixturePub),'even hypothetical signature cannot override source conflict');
check('verified_filter_proposed_only_fixture',!verifiedEligible(fixtureObs,fixtureSource,fixtureEvents,[{...fixtureProposals[0],proposal_status:PROPOSED}],'direct',fixturePub),'proposed classification cannot populate a verified view');
check('verified_filter_wrong_version_fixture',!verifiedEligible(fixtureObs,fixtureSource,[{...fixtureEvents[0],record_version:'OTHER_VERSION'}],fixtureProposals,'direct',fixturePub),'signature scoped to another version rejected');
check('verified_filter_retracted_fixture',!verifiedEligible(fixtureObs,fixtureSource,fixtureEvents,fixtureProposals,'direct',[{...fixturePub[0],raw_retraction_status:'RETRACTED'}]),'retracted publication rejected');
const antioxidantFixture=[{...fixtureProposals[0],proposed_value:'FUNCTIONAL_PARTICIPATION_SUPPORTED'},{...fixtureProposals[0],field_name:'antioxidant_relevance_primary',proposed_value:'DIRECT_REDOX_OUTCOME'},{...fixtureProposals[0],field_name:'antioxidant_relevance_secondary',proposed_value_json:'["ANTIOXIDANT_FUNCTIONAL_MECHANISM"]'}];
check('verified_antioxidant_scoped_fixture',verifiedEligible(fixtureObs,fixtureSource,fixtureEvents,antioxidantFixture,'antioxidant',fixturePub),'hypothetical signed direct-redox primary plus functional-mechanism secondary and functional participation are compatible');
check('verified_antioxidant_readout_rejected_fixture',!verifiedEligible(fixtureObs,fixtureSource,fixtureEvents,[{...antioxidantFixture[0],proposed_value:'READOUT_ONLY'},...antioxidantFixture.slice(1)],'antioxidant',fixturePub),'readout-only cannot become a verified antioxidant mechanism even with relevance labels');
const multiCandidate=[{...fixtureObs,candidate_id:'SYNTHETIC-COMPOUND-A'},{...fixtureObs,evidence_id:'FIXTURE-ONLY-B',candidate_id:'SYNTHETIC-COMPOUND-B'}];
check('multi_candidate_key_fixture',new Set(multiCandidate.map(o=>o.evidence_id)).size===2&&new Set(multiCandidate.map(o=>o.candidate_id)).size===2,'two synthetic compound contexts do not require merging evidence IDs; this is a key-design smoke test, not evidence retrieval or full scale-up validation');

const restored=await reconstruct();
check('rollback_cells_recoverable',restored.rows.length===21&&restored.headers.length===66&&restored.rows.every((r,i)=>restored.headers.every(h=>r[h]===input.evidence.rows[i][h])),'reconstruction from EAV equals every source cell in original row/column order');
check('rollback_byte_snapshot',sha(Buffer.from(restored.original_source_bytes_base64,'base64'))===sha(await fs.readFile(path.join(pilot,'compounds/AFF-0061_Protocatechuic_Acid_Mechanism_Evidence.csv'))),'byte-exact source snapshot plus semantic reconstruction; no production write');
await fs.writeFile(path.join(workspace,'qc/Rollback_Reconstruction.json'),JSON.stringify(restored,null,2)+'\n');
const rebuild=await build(path.join(workspace,'qc/rebuild_check'));
const manifest=JSON.parse(await fs.readFile(path.join(workspace,'qc/Build_Manifest.json'),'utf8'));
const alteredOutputs=[];for(const item of manifest.files){if(sha(await fs.readFile(path.join(workspace,item.path)))!==item.sha256)alteredOutputs.push(item.path);}
check('actual_output_manifest_hashes',!alteredOutputs.length,{altered:alteredOutputs});
check('deterministic_regeneration',json(manifest)===json(rebuild),'independent rebuild of 19 CSV and two JSON payloads yields identical SHA256 manifest');
check('saved_output_hashes',manifest.files.every(f=>rebuild.files.some(r=>r.path===f.path&&r.sha256===f.sha256)),'rebuild file set and content equal');
const protectedBaseline=JSON.parse(await fs.readFile(path.join(workspace,'qc/Start_Baseline.json'),'utf8'));
const changed=[];for(const r of protectedBaseline.tracked){try{if(sha(await fs.readFile(path.join(root,r.path)))!==r.sha256)changed.push(r.path);}catch{changed.push(r.path);}}
const cacheChanged=[];for(const r of protectedBaseline.local_source_cache){try{if(sha(await fs.readFile(r.path))!==r.sha256)cacheChanged.push(r.path);}catch{cacheChanged.push(r.path);}}
check('protected_tracked_sha256',!changed.length,{count:protectedBaseline.tracked.length,changed});
check('protected_cache_sha256',!cacheChanged.length,{count:protectedBaseline.local_source_cache.length,changed:cacheChanged});
const git=(...args)=>execFileSync('git',args,{cwd:root,encoding:'utf8'}).trim();
const branch=git('branch','--show-current');const head=git('rev-parse','HEAD');
check('task_branch_not_main',branch==='codex/phase1c-governance-v0.2-dryrun'&&git('rev-parse','main')===protectedBaseline.main&&git('merge-base','main','HEAD')===protectedBaseline.merge_base,{branch,head,main:git('rev-parse','main')});
const prefix='workspaces/phase1c_mechanism_evidence_pilot/governance_v0.2_dryrun/';
const status=git('status','--porcelain=v1','--untracked-files=all');
const outside=status?status.split(/\r?\n/).filter(line=>!line.slice(3).replaceAll('"','').startsWith(prefix)):[];
check('only_new_workspace_changes',!outside.length,{outside});

// Read/inspect every requested CSV; render a bounded representative range for every CSV.
const csvFiles=manifest.files.filter(f=>f.path.endsWith('.csv'));
const previewDir=path.join(workspace,'qc/previews');await fs.mkdir(previewDir,{recursive:true});
for(const file of csvFiles){
 const parsed=await readCSV(path.join(workspace,file.path));
 check('csv_role_'+file.path,parsed.headers.includes('dataset_role')&&parsed.rows.every(r=>r.dataset_role===ROLE),{rows:parsed.rows.length,columns:parsed.headers.length});
 const inspect=await parsed.wb.inspect({kind:'table',range:'Records!A1:F4',include:'values,formulas',tableMaxRows:4,tableMaxCols:6,maxChars:1800});
 const errorScan=await parsed.wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NUM!|#SPILL!|#CALC!',options:{useRegex:true,maxResults:20},summary:'literal error token scan'});
 const sheet=parsed.wb.worksheets.getItemAt(0);const n=Math.min(4,parsed.rows.length+1);
 sheet.getRangeByIndexes(0,0,n,4).format.font={name:'Arial',size:11};
 sheet.getRangeByIndexes(0,0,n,4).format.wrapText=true;
 sheet.getRangeByIndexes(0,0,n,4).format.columnWidth=42;
 sheet.getRangeByIndexes(0,0,n,4).format.rowHeight=65;
 parsed.wb.recalculate();
 const preview=await parsed.wb.render({sheetName:'Records',range:`A1:D${n}`,scale:1,format:'png'});
 const safe=file.path.replaceAll('/','__');
 await fs.writeFile(path.join(previewDir,safe+'.png'),new Uint8Array(await preview.arrayBuffer()));
 await fs.writeFile(path.join(previewDir,safe+'.json'),JSON.stringify({inspection:inspect.ndjson,error_scan:errorScan.ndjson},null,2));
}
check('csv_count',csvFiles.length===19,'16 table/view CSV plus decision diff, field mapping and vocabulary snapshot');
const requiredDocs=['Governance_Decision_Record_v0.2.md','Migration_Dry_Run_Report_v0.1.md','Sync_to_ChatGPT_Phase1C_Governance_v0.2.md','schema/Mechanism_Evidence_Schema_v0.2.md'];
const absent=[];for(const rel of requiredDocs){try{if(!(await fs.stat(path.join(workspace,rel))).size)absent.push(rel);}catch{absent.push(rel);}}
check('required_narratives_exist',!absent.length,{missing:absent});
const result={dataset_role:ROLE,date:DATE,timezone:'Asia/Shanghai',branch,head_at_validation:head,source_head:protectedBaseline.head,main_unchanged:protectedBaseline.main,table_count:13,view_count:3,csv_count:19,observation_count:21,legacy_field_count:66,legacy_cell_count:1386,proposal_count:257,review_event_count:257,unresolved_mapping_count:23,legacy_experiment_scope_count:21,independent_experiment_count:'UNRESOLVED_NOT_21',protected_tracked_count:protectedBaseline.tracked.length,protected_cache_count:protectedBaseline.local_source_cache.length,pass:checks.filter(c=>c.pass).length,fail:checks.filter(c=>!c.pass).length,checks,formal_gate1:'HOLD',formal_gate2:'HUMAN_SCIENTIFIC_REVIEW_REQUIRED',scale_up:'NOT_AUTHORIZED_ALL_FOUR',release:'HOLD',production_changes:0};
await fs.writeFile(path.join(workspace,'qc/Migration_Validation.json'),JSON.stringify(result,null,2)+'\n');
const md=`# 隔离迁移演练QC\n\n2026-10-22。NON_PRODUCTION_DRYRUN；本次最终检查${result.pass}项通过、${result.fail}项失败。详细逐项结果见Migration_Validation.json。程序结果不代表正式Gate验收。\n\n13张数据/审计表与3个验证视图；21观察、66字段/1386原始单元格、257待审提案与257待审事件。7条来源HOLD仅在隔离层标记，原状态不变；3个验证视图均为空。没有未经授权人工批准。\n\n检查包括主外键、枚举、空值/原哨兵、原关系/身份/单位/定位、事件双向关系、Akt/TYR与HDAC及NRF2三案例、桥表唯一计数、24决策及15/9状态、输出重建和回滚。8项故意损坏的内存副本均须触发预期拒绝；这些拒绝测试通过不算真实数据失败。另测已签署假设视图的正例、HOLD/提案/错版本/撤稿排除和双候选键设计。所有合成fixture仅在内存，不是新科学证据。\n\n19个CSV均经Artifact Tool读写往返、结构检查与代表范围渲染，CSV无公式或样式交付。预览位于忽略的previews，由主代理另行视觉核查；不声称检查了全部单元格视觉或原论文图像。独立重建的19个CSV及2个JSON载荷与原构建manifest完全一致；回滚同时验证1386值恢复及原字节快照SHA，未向生产路径写回。\n\n已知未决不是技术失败：真实实验/材料共享、跨文复用、对照臂解析、部分最终暴露基准、TRAF2全文、amylase身份冲突、NRF2 M/N及S2提取、具名签署均待审。本轮没有测性能或完成191候选迁移，双候选检查仅键设计smoke test。正式Gate1 HOLD；Gate2 HUMAN_SCIENTIFIC_REVIEW_REQUIRED；Scale-up四权限未授权；Release HOLD。\n\n执行时HEAD ${head}，源HEAD ${protectedBaseline.head}；提交后SHA和远端状态由最终回复报告，不伪造自指哈希。\n`;
await fs.writeFile(path.join(workspace,'qc/Migration_Dry_Run_QC_Report.md'),md.replace('8项故意损坏的内存副本',`${checks.filter(c=>c.id.startsWith('negative_fixture_')).length}项故意损坏的内存副本`));
await fs.writeFile(path.join(workspace,'qc/Protected_Asset_Integrity_Report.md'),`# 保护资产完整性\n\n2026-10-22。源HEAD ${protectedBaseline.head}，起始分支codex/phase1c-governance-v0.1，任务分支${branch}。main维持${protectedBaseline.main}，merge-base未变；v0.1未合并main。\n\n${protectedBaseline.tracked.length}个既有跟踪文件SHA256逐项复核，变更${changed.length}个；${protectedBaseline.local_source_cache.length}个既有本地来源缓存变更${cacheChanged.length}个。详细预期值在Start_Baseline.json，结果在Migration_Validation.json。范围包括原21条、66字段字典、Master/Study_Register、全部Gate2和v0.1历史文件、T002/T004/T110、Phase1B、临时Crosswalk、Frozen Top20、157×5矩阵及其他既有跟踪资产。\n\n只新增本工作区。原始事实与科学提案分表；科学源表未经写回；未检索新候选、未更新正式审核状态、未运行网络/排名/训练。来源缓存仅核hash，不上传原图或全文。Git归档不是科学签署。\n\n变化清单：${json(changed)}；缓存变化：${json(cacheChanged)}。\n`);
console.log(JSON.stringify({pass:result.pass,fail:result.fail,tables:13,views:3,observations:21,proposals:257,failed:checks.filter(c=>!c.pass)},null,2));
if(result.fail)process.exitCode=1;
