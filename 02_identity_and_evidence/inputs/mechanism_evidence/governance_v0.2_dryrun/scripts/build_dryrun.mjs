import fs from 'node:fs/promises';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
import {workspace,pilot,ROLE,PROPOSED,DATE,sha,json,missing,inputs,inputPaths,writeCSV,ensureWithinWorkspace,verifiedEligible} from './migration_lib.mjs';
import {accepted,policies,prereq,endpointMapping} from './policy_v02.mjs';

const publicationFields=['article_title','DOI','PMID','journal','publication_date','publication_date_type','article_url','PMCID','publication_date_precision','publication_status'];
const experimentFields=['experimental_model','species','cell_line_or_tissue','experiment_independence_status'];
const interventionFields=['dose','dose_unit','treatment_duration','administration_route','pretreatment_duration','challenge_agent','challenge_dose','challenge_duration'];
const targetFields=['target_gene','target_protein','UniProt_ID','target_species','target_role','target_effect_direction','target_validation_status','target_experimental_support','direct_target_status','target_identifier_status','target_identifier_source'];
const sourceFields=['source_figure_or_table','source_verification_status','source_local_path','source_locator','source_result_paraphrase_CN','source_review_mode'];
const projection=(r,fields)=>Object.fromEntries(fields.map(k=>['raw_'+k,r[k]]));
const suffix=id=>id.replace('ME-AFF0061-','');
const scope=r=>r.source_verification_status==='ABSTRACT_ONLY'?'ABSTRACT_ONLY':'FULL_TEXT_TEXT_LEGEND';
const issue=r=>r.evidence_id==='ME-AFF0061-42170612-001'?'CONFLICT':r.source_verification_status==='ABSTRACT_ONLY'?'NOT_RECOVERED':'NONE_IDENTIFIED_AT_REVIEW';
const groups=[publicationFields,experimentFields,interventionFields,targetFields,sourceFields];
const standalone=['study_id','experiment_id'];
const observationFields=fields=>fields.filter(k=>!groups.some(g=>g.includes(k))&&!standalone.includes(k));

function doseBasis(r){
 if(r.dose==='NOT_APPLICABLE')return {value:null,reason:'NOT_APPLICABLE',note:'计算观察不涉及实际给药，原值仍保留。'};
 if(missing(r.dose))return {value:null,reason:missing(r.dose),note:'原始剂量未解决，不从模型或题名补全。'};
 const units={'mg/kg/day':'ADMINISTERED_BODY_MASS_DAILY_DOSE','mg/kg':'ADMINISTERED_BODY_MASS_DOSE','mmol/L syringe concentration':'SYRINGE_CONCENTRATION','% drinking-water concentration':'DRINKING_WATER_PERCENT','nmol topical dose':'TOPICAL_ABSOLUTE_AMOUNT'};
 if(units[r.dose_unit])return {value:units[r.dose_unit],reason:'',note:'仅根据原值明确表达的基准提出结构化映射；未计算新暴露值。'};
 return {value:null,reason:'UNRESOLVED',note:'单位与体外模型不足以证明final而非stock；待核原方法最终暴露基准，不猜填。'};
}

export async function build(output=workspace){
 output=ensureWithinWorkspace(output);
 const data=await inputs();
 const rows=data.evidence.rows;const fields=data.dictionary.rows.map(r=>r.field_name);
 if(rows.length!==21||fields.length!==66)throw Error('Unexpected source size; review before rebuilding');
 const tables={};const schema={dataset_role:ROLE,version:'0.2_DRYRUN',tables:{}};
 async function table(name,headers,values,pk,fks=[]){
  const result=await writeCSV(path.join(output,'dryrun',name+'.csv'),headers,values);
  tables[name]=result.rows;
  schema.tables[name]={path:'dryrun/'+name+'.csv',columns:result.headers,primary_key:pk,foreign_keys:fks,row_count:values.length};
 }
 const fk=(column,table,target,nullable=false)=>({column,table,target,nullable});
 const publicationId=id=>'PUB-'+id;
 const observationRaw=observationFields(fields);
 const obs=rows.map((r,i)=>({evidence_id:r.evidence_id,candidate_id:r.candidate_id,publication_id:publicationId(r.study_id),experiment_id:r.experiment_id,source_check_id:'SC-'+r.evidence_id,intervention_id:'INT-'+r.evidence_id,raw_study_id:r.study_id,raw_experiment_id:r.experiment_id,legacy_row_order:String(i+1),record_version:'LEGACY_COPY_1',scientific_approval_status:'PENDING_HUMAN_REVIEW',sandbox_review_state:data.gate2.rows.find(x=>x.evidence_id===r.evidence_id).review_status==='HOLD_SOURCE_VERIFICATION'?'HOLD':'PROVISIONAL',material_id:'',material_missing_reason:'UNRESOLVED',...projection(r,observationRaw)}));
 const pubs=data.studies.rows.map(r=>({publication_id:publicationId(r.study_id),legacy_study_id:r.study_id,...Object.fromEntries(Object.entries(r).map(([k,v])=>['raw_'+k,v])),scientific_approval_status:'PENDING_HUMAN_REVIEW'}));
 await table('Publication',['publication_id','legacy_study_id',...data.studies.headers.map(h=>'raw_'+h),'scientific_approval_status'],pubs,['publication_id']);
 await table('Experiment',['experiment_id','publication_id','legacy_experiment_id','entity_scope','identity_mapping_status','material_id','material_missing_reason',...experimentFields.map(k=>'raw_'+k)],rows.map(r=>({experiment_id:r.experiment_id,publication_id:publicationId(r.study_id),legacy_experiment_id:r.experiment_id,entity_scope:'LEGACY_COMPARISON_NOT_INDEPENDENT_EXPERIMENT',identity_mapping_status:'PENDING_DESIGN_AND_MATERIAL_REVIEW',material_id:'',material_missing_reason:'UNRESOLVED',...projection(r,experimentFields)})),['experiment_id'],[fk('publication_id','Publication','publication_id')]);
 const localFileHashes=new Map();
 for(const r of rows){const p=path.resolve(pilot,r.source_local_path);try{localFileHashes.set(r.evidence_id,sha(await fs.readFile(p)));}catch{localFileHashes.set(r.evidence_id,'');}}
 await table('Source_Check',['source_check_id','evidence_id','publication_id','source_scope','source_issue','mapping_status','check_mode','historical_check_date','date_missing_reason','import_date','source_sha256',...sourceFields.map(k=>'raw_'+k)],rows.map(r=>({source_check_id:'SC-'+r.evidence_id,evidence_id:r.evidence_id,publication_id:publicationId(r.study_id),source_scope:scope(r),source_issue:issue(r),mapping_status:PROPOSED,check_mode:'IMPORTED_PRIOR_REVIEW_NOT_NEW_VERIFICATION',historical_check_date:'',date_missing_reason:'UNRESOLVED',import_date:DATE,source_sha256:localFileHashes.get(r.evidence_id),...projection(r,sourceFields)})),['source_check_id'],[fk('evidence_id','Observation','evidence_id'),fk('publication_id','Publication','publication_id')]);
 await table('Intervention',['intervention_id','evidence_id','experiment_id','candidate_id','intervention_role','parsed_control_arm_id','control_mapping_status','raw_control_group',...interventionFields.map(k=>'raw_'+k)],rows.map(r=>({intervention_id:'INT-'+r.evidence_id,evidence_id:r.evidence_id,experiment_id:r.experiment_id,candidate_id:r.candidate_id,intervention_role:'LEGACY_COMPOUND_EXPOSURE_CONTEXT',parsed_control_arm_id:'',control_mapping_status:'PENDING_ARM_EXTRACTION',raw_control_group:r.control_group,...projection(r,interventionFields)})),['intervention_id'],[fk('evidence_id','Observation','evidence_id'),fk('experiment_id','Experiment','experiment_id')]);
 await table('Observation',['evidence_id','candidate_id','publication_id','experiment_id','source_check_id','intervention_id','raw_study_id','raw_experiment_id','legacy_row_order','record_version','scientific_approval_status','sandbox_review_state','material_id','material_missing_reason',...observationRaw.map(k=>'raw_'+k)],obs,['evidence_id'],[fk('publication_id','Publication','publication_id'),fk('experiment_id','Experiment','experiment_id'),fk('source_check_id','Source_Check','source_check_id'),fk('intervention_id','Intervention','intervention_id')]);
 await table('Observation_Target',['observation_target_id','evidence_id','target_entity_id','identity_status',...targetFields.map(k=>'raw_'+k)],rows.filter(r=>r.target_protein!=='NOT_APPLICABLE').map(r=>({observation_target_id:'OT-'+r.evidence_id,evidence_id:r.evidence_id,target_entity_id:'',identity_status:'LEGACY_OBJECT_NOT_DEDUPLICATED_OR_APPROVED',...projection(r,targetFields)})),['observation_target_id'],[fk('evidence_id','Observation','evidence_id')]);
 const legacy=rows.flatMap(r=>fields.map((field,i)=>({evidence_id:r.evidence_id,field_name:field,field_order:String(i+1),raw_value:r[field],raw_missing_token:missing(r[field])?r[field]:'',missing_reason:missing(r[field]),value_type:'LEGACY_TEXT',source_row_sha256:sha(json(r))})));
 await table('Legacy_Field_Value',['evidence_id','field_name','field_order','raw_value','raw_missing_token','missing_reason','value_type','source_row_sha256'],legacy,['evidence_id','field_name'],[fk('evidence_id','Observation','evidence_id')]);
 const maps=[...data.studies.rows.map(r=>({map_id:'MAP-PUB-'+r.study_id,legacy_entity:'STUDY_AS_PUBLICATION',legacy_id:r.study_id,new_table:'Publication',new_id:publicationId(r.study_id),mapping_status:'IDENTIFIER_COPY_NO_SCIENTIFIC_APPROVAL',reason:'旧study_id按出版物分配；不是独立实验认证。'})),...rows.map(r=>({map_id:'MAP-EXP-'+r.experiment_id,legacy_entity:'EXPERIMENT',legacy_id:r.experiment_id,new_table:'Experiment',new_id:r.experiment_id,mapping_status:'PENDING_DESIGN_AND_MATERIAL_REVIEW',reason:'原ID一对一保留，不合并，不推材料共享或独立。'})),...rows.map(r=>({map_id:'MAP-OBS-'+r.evidence_id,legacy_entity:'OBSERVATION',legacy_id:r.evidence_id,new_table:'Observation',new_id:r.evidence_id,mapping_status:'IDENTIFIER_COPY_NO_SCIENTIFIC_APPROVAL',reason:'稳定观察ID原样保留。'}))];
 await table('Legacy_ID_Map',['map_id','legacy_entity','legacy_id','new_table','new_id','mapping_status','reason'],maps,['map_id']);
 await table('Independence_Assessment',['assessment_id','evidence_id','experiment_id','independence_relation','assessment_scope','basis','mapping_status'],rows.map(r=>({assessment_id:'IA-'+r.evidence_id,evidence_id:r.evidence_id,experiment_id:r.experiment_id,independence_relation:'UNRESOLVED_REUSE',assessment_scope:'WITHIN_AND_CROSS_PUBLICATION_NOT_FULLY_ASSESSED',basis:r.experiment_independence_status,mapping_status:PROPOSED})),['assessment_id'],[fk('evidence_id','Observation','evidence_id'),fk('experiment_id','Experiment','experiment_id')]);
 const proposals=[];
 function add(r,field,value,reason='',basis='',old=null){
  const id='PROP-'+r.evidence_id+'-'+field;
  const present=Object.hasOwn(r,field);
  proposals.push({proposal_id:id,evidence_id:r.evidence_id,field_name:field,old_value_presence:present?'LEGACY_VALUE_PRESENT':'NOT_PRESENT_IN_LEGACY_SCHEMA',old_value_json:json(present?r[field]:null),legacy_related_value_json:json(old),proposed_value:value===null?'':typeof value==='string'?value:json(value),proposed_value_json:json(value),missing_reason:reason,proposal_status:PROPOSED,proposal_origin:basis.startsWith('Gate2')?'GATE2_IMPORTED_PROPOSAL':'DRYRUN_MAPPING_SUGGESTION',basis,source_reference:'compounds/AFF-0061_Protocatechuic_Acid_Mechanism_Evidence.csv#'+r.evidence_id+'; gate2_review/AFF-0061_Gate2_Evidence_Review_Matrix.csv#'+r.evidence_id,review_event_id:'RE-'+id,approval_event_id:'',applied_to_production:'NO'});
 }
 for(const r of rows){
  const g=data.gate2.rows.find(x=>x.evidence_id===r.evidence_id);const [redox,level]=endpointMapping[suffix(r.evidence_id)];
  const tags=g.antioxidant_relevance_secondary_proposed==='NONE'?[]:[g.antioxidant_relevance_secondary_proposed];
  add(r,'target_confirmation_class',g.protein_target_confirmation_proposed,'','Gate2：'+g.review_reason_CN);
  add(r,'antioxidant_relevance_primary',g.antioxidant_relevance_proposed,'','Gate2：'+g.redox_endpoint_review);
  add(r,'antioxidant_relevance_secondary',tags,'','Gate2：受控secondary原提案；不借同文其他行。');
  const dose=doseBasis(r);add(r,'dose_basis',dose.value,dose.reason,dose.note);
  add(r,'redox_measurement_level',redox,'','隔离映射：原endpoint及Gate2 redox_endpoint_review；不是新测量。');
  add(r,'readout_level',level,'','隔离映射：'+r.observation_endpoint+'；对象与层级仅作待审建议。');
  let direction=null;let directionReason='NOT_APPLICABLE';
  if(r.target_effect_direction.startsWith('INCREASED')){direction='INCREASED';directionReason='';}
  else if(r.target_effect_direction.startsWith('DECREASED')){direction='DECREASED';directionReason='';}
  else if(r.target_effect_direction==='UNRESOLVED'||r.target_effect_direction==='NO_ADDITIONAL_CHANGE'){directionReason='UNRESOLVED';}
  add(r,'result_direction',direction,directionReason,'原target_effect_direction含结合/依赖等非数值方向，不强行改成增减或零。',r.target_effect_direction);
  add(r,'result_significance',r.evidence_id==='ME-AFF0061-41594941-005'?'NOT_STATISTICALLY_SIGNIFICANT':null,r.evidence_id==='ME-AFF0061-41594941-005'?'':'UNRESOLVED','Gate2：仅HDAC1-005明确未检出显著增量；其他行未结构化提取p/区间，不从方向猜显著。');
  add(r,'source_scope',scope(r),'','历史来源状态的范围映射；本轮不重新检索或核原图。',r.source_verification_status);
  add(r,'source_issue',issue(r),'','Gate2来源限制/冲突范围映射；NRF2 M/N另列未决项，不写入6L值。');
  add(r,'missing_reason',missing(r.dose)||null,missing(r.dose)?'':'NOT_APPLICABLE','演示剂量missing_reason；全部66字段的原因在Legacy_Field_Value，不将空值变零。');
  add(r,'independence_relation','UNRESOLVED_REUSE','','未核共享材料与跨文复用，不把旧experiment_id数当独立实验数。');
  if(r.evidence_relation_type!==g.proposed_relation_type)add(r,'evidence_relation_type',g.proposed_relation_type,'','Gate2：'+g.review_reason_CN,r.evidence_relation_type);
  if(r.evidence_id==='ME-AFF0061-41594941-005')add(r,'target_effect_direction',g.proposed_effect_direction,'','Gate2：措辞修订与result_significance分开；不是零效应或等效。',r.target_effect_direction);
  if(r.evidence_id==='ME-AFF0061-32520409-002'){
   add(r,'target_species',g.proposed_target_species,'','Gate2：RCSB3GLS模型物种元数据提案，不更改计算性质。',r.target_species);
   add(r,'UniProt_ID',g.proposed_UniProt_ID,'','Gate2：结构模型参考accession元数据提案，不成为实验结合。',r.UniProt_ID);
  }
 }
 await table('Scientific_Proposal',['proposal_id','evidence_id','field_name','old_value_presence','old_value_json','legacy_related_value_json','proposed_value','proposed_value_json','missing_reason','proposal_status','proposal_origin','basis','source_reference','review_event_id','approval_event_id','applied_to_production'],proposals,['proposal_id'],[fk('evidence_id','Observation','evidence_id'),fk('review_event_id','Review_Event','review_event_id')]);
 const events=proposals.map(p=>({review_event_id:p.review_event_id,evidence_id:p.evidence_id,proposal_id:p.proposal_id,reviewer_type:'CODEX_ASSISTED_SCIENTIFIC_REVIEW',reviewer:'Codex — imported Gate2 suggestion / dry-run mapping',review_date:DATE,review_action:'PROPOSE_CHANGE',field_name:p.field_name,old_value_presence:p.old_value_presence,old_value:p.old_value_json,legacy_related_value_json:p.legacy_related_value_json,proposed_value:p.proposed_value_json,decision:'PENDING',decision_reason:p.basis,source_reference:p.source_reference,approval_status:'PENDING_HUMAN_REVIEW',change_applied:'NO',record_version:'LEGACY_COPY_1',signed_by:'',signoff_reference:'',rule_version:'0.2_PENDING_FORMAL_SIGNOFF'}));
 await table('Review_Event',['review_event_id','evidence_id','proposal_id','reviewer_type','reviewer','review_date','review_action','field_name','old_value_presence','old_value','legacy_related_value_json','proposed_value','decision','decision_reason','source_reference','approval_status','change_applied','record_version','signed_by','signoff_reference','rule_version'],events,['review_event_id'],[fk('evidence_id','Observation','evidence_id'),fk('proposal_id','Scientific_Proposal','proposal_id')]);
 const tags=proposals.filter(p=>p.field_name==='antioxidant_relevance_secondary').flatMap(p=>JSON.parse(p.proposed_value_json).map((tag,i)=>({tag_id:'TAG-'+p.evidence_id+'-'+String(i+1),evidence_id:p.evidence_id,tag,proposal_id:p.proposal_id,proposal_status:PROPOSED,applied_to_production:'NO'})));
 await table('Observation_Tag',['tag_id','evidence_id','tag','proposal_id','proposal_status','applied_to_production'],tags,['tag_id'],[fk('evidence_id','Observation','evidence_id'),fk('proposal_id','Scientific_Proposal','proposal_id')]);
 const unresolved=rows.map(r=>({issue_id:'UM-'+r.evidence_id,publication_id:publicationId(r.study_id),evidence_id:r.evidence_id,experiment_id:r.experiment_id,issue_type:'DESIGN_MATERIAL_IDENTITY',status:'PENDING_HUMAN_REVIEW',source_reference:r.source_locator,detail:'保留旧比较ID；未确认哪些观察同设计/同材料，原论文或同剂量不能证明共享。',required_action:'核实验分配/样本批次/方法后形成有据映射；禁止自动合并。',forbidden_link:'AUTOMATIC_EXPERIMENT_MERGE_OR_SHARED_MATERIAL'}));
 unresolved.push({issue_id:'UM-NRF2-S2',publication_id:publicationId('ST-PMID-39589556'),evidence_id:'',experiment_id:'',issue_type:'PENDING_EXTRACTION_NOT_OBSERVATION',status:'PENDING_HUMAN_REVIEW',source_reference:'gate2_review/AFF-0061_Critical_Source_Verification_Report.md#NRF2; Supplement S2 page3',detail:'S2细胞补回尚未提取为正式观察；若后续获权提取，必须使用不同于动物6L的实验和材料实体。',required_action:'另行授权核细胞背景/载体/剂量/时序/比较后分配新ID；本轮不创建第22条。',forbidden_link:'ME-AFF0061-39589556-001;EXP-39589556-001;ANIMAL_6L_RESCUE_UPGRADE'});
 unresolved.push({issue_id:'UM-NRF2-MN',publication_id:publicationId('ST-PMID-39589556'),evidence_id:'',experiment_id:'',issue_type:'SOURCE_LABEL_CONFLICT',status:'PENDING_HUMAN_REVIEW',source_reference:'gate2_review/AFF-0061_Critical_Source_Verification_Report.md#NRF2',detail:'Figure6M/N正文/图注/原图标签冲突；原6L不猜改，M/N未提取数值。',required_action:'作者/底层数据澄清后再决定是否提取。',forbidden_link:'INVENTED_MDA_4HNE_VALUES_OR_NEW_OBSERVATION'});
 await table('Unresolved_Mapping',['issue_id','publication_id','evidence_id','experiment_id','issue_type','status','source_reference','detail','required_action','forbidden_link'],unresolved,['issue_id'],[fk('publication_id','Publication','publication_id'),fk('evidence_id','Observation','evidence_id',true),fk('experiment_id','Experiment','experiment_id',true)]);
 for(const [name,kind]of [['Verified_Direct_Targets','direct'],['Verified_Antioxidant_Mechanisms','antioxidant'],['Verified_Evidence_Support','support']]){
  const selected=tables.Observation.filter(o=>verifiedEligible(o,tables.Source_Check,tables.Review_Event,tables.Scientific_Proposal,kind,tables.Publication));
  await table(name,['evidence_id','candidate_id','view_scope'],selected.map(o=>({evidence_id:o.evidence_id,candidate_id:o.candidate_id,view_scope:kind})),['evidence_id'],[fk('evidence_id','Observation','evidence_id')]);
 }
 const decisions=data.decisions.rows.map(r=>({decision_id:r.decision_id,topic:r.topic,old_rule:r.recommendation,v02_recommendation:policies[r.decision_id]?.rule||r.recommendation,chatgpt_review_opinion:policies[r.decision_id]?.review||'依据本轮用户提供的ChatGPT审查建议接受基础原则，等待正式签署。',scientific_basis:r.basis+'；既有v0.1治理文档/Gate2及本轮授权附件，未开展新文献复核。',applicable_scope:r.impact_scope,preconditions:policies[r.decision_id]?.pre||prereq,recommendation_state:accepted.has(r.decision_id)?'SCIENTIFIC_RECOMMENDATION_ACCEPTED_PENDING_FORMAL_SIGNOFF':'IMPLEMENTATION_POLICY_PROPOSED_PENDING_FORMAL_SIGNOFF',formal_approval_status:'PENDING_FORMAL_SIGNOFF',signed_by:'',signoff_date:'',implemented_in_production:'NO',dryrun_implementation:'STRUCTURE_ONLY_OR_QC_RULE',review_provenance:'USER_SUPPLIED_CHATGPT_REVIEW_IN_TASK_ATTACHMENT'}));
 await writeCSV(path.join(output,'Governance_Decision_Diff_v0.1_to_v0.2.csv'),Object.keys(decisions[0]),decisions);
 const mapped=fields.map((field,i)=>{
  let table='Observation',col='raw_'+field;
  if(publicationFields.includes(field)){table='Publication';col=field==='publication_status'?'raw_retraction_status':'raw_'+field;}
  if(experimentFields.includes(field))table='Experiment';
  if(interventionFields.includes(field))table='Intervention';
  if(targetFields.includes(field))table='Observation_Target';
  if(sourceFields.includes(field))table='Source_Check';
  if(field==='study_id')col='raw_study_id';if(field==='experiment_id')col='raw_experiment_id';
  return {field_order:String(i+1),legacy_field:field,definition_original:data.dictionary.rows[i].definition_cn,semantic_table:table,semantic_column:col,restore_table:'Legacy_Field_Value',restore_key:'evidence_id + field_name',restore_column:'raw_value',lossless_rule:'EXACT_LEGACY_TEXT_NO_RECLASSIFICATION',null_rule:'原哨兵逐字保存；规范空值和missing_reason并列，不填0。',mapping_caveat:table==='Publication'?'Publication保存Study_Register原值；若观察元数据与登记差异，以本观察Legacy_Field_Value恢复，不覆盖。':table==='Observation_Target'?'无蛋白对象的三行不造Target记录，原NOT_APPLICABLE由Legacy_Field_Value恢复。':'仅物理投影，不代表科学批准。'};
 });
 await writeCSV(path.join(output,'schema/Schema_Field_Mapping_v0.2.csv'),Object.keys(mapped[0]),mapped);
 await writeCSV(path.join(output,'schema/Controlled_Vocabulary_Snapshot_v0.1.csv'),data.vocabulary.headers,data.vocabulary.rows);
 await fs.mkdir(path.join(output,'schema'),{recursive:true});
 await fs.writeFile(path.join(output,'schema/Table_Contract_v0.2.json'),JSON.stringify(schema,null,2)+'\n');
 const snapshots=[];for(const [key,rel]of Object.entries(inputPaths)){const bytes=await fs.readFile(path.join(pilot,rel));snapshots.push({key,pilot_relative_path:rel,sha256:sha(bytes),bytes_base64:bytes.toString('base64')});}
 await fs.mkdir(path.join(output,'qc'),{recursive:true});
 await fs.writeFile(path.join(output,'qc/Input_Snapshot.json'),JSON.stringify({dataset_role:ROLE,source_head:'7e62d3b6fcebda2d4941d8e93631d96959fc9581',files:snapshots},null,2)+'\n');
 const fileList=[...Object.values(schema.tables).map(t=>t.path),'Governance_Decision_Diff_v0.1_to_v0.2.csv','schema/Schema_Field_Mapping_v0.2.csv','schema/Controlled_Vocabulary_Snapshot_v0.1.csv','schema/Table_Contract_v0.2.json','qc/Input_Snapshot.json'];
 const manifest={dataset_role:ROLE,build_date:DATE,source_head:'7e62d3b6fcebda2d4941d8e93631d96959fc9581',table_count:13,view_count:3,observations:21,scientific_proposals:proposals.length,files:[]};
 for(const rel of fileList)manifest.files.push({path:rel,sha256:sha(await fs.readFile(path.join(output,rel)))});
 await fs.writeFile(path.join(output,'qc/Build_Manifest.json'),JSON.stringify(manifest,null,2)+'\n');
 console.log(json({output,table_count:13,view_count:3,observations:obs.length,proposals:proposals.length,tags:tags.length,unresolved:unresolved.length,csv_count:19}));
 return manifest;
}
if(process.argv[1]&&import.meta.url===pathToFileURL(path.resolve(process.argv[1])).href)await build(process.argv[2]||workspace);
