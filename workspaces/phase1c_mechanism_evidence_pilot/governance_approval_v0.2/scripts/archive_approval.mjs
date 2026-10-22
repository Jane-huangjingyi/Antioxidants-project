import fs from 'node:fs/promises';
import path from 'node:path';
import crypto from 'node:crypto';
import {execFileSync} from 'node:child_process';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {Workbook} from '@oai/artifact-tool';

export const dir=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
export const root=path.resolve(dir,'../../..');
export const pilot=path.resolve(dir,'..');
export const SOURCE_COMMIT='9c6be49bac03a16bab1aa49790124dbdaf7a6af0';
export const SOURCE_BRANCH='codex/phase1c-governance-v0.2-dryrun';
export const TASK_BRANCH='codex/phase1c-governance-v0.2-approval';
export const ATTACHMENT='C:/Users/JANE/.codex/attachments/1b8a9f03-07a0-4b4c-be9c-842619fb8c10/已粘贴的文本.txt';
export const QUOTE='我确认正式批准24项Governance v0.2治理规则作为Antioxidants-project的项目基准。';
export const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
export const git=(...a)=>execFileSync('git',a,{cwd:root,encoding:'utf8'}).trim();
export const rel=p=>path.relative(root,p).replaceAll('\\','/');
export const metadata={record_type:'GOVERNANCE_APPROVAL',governance_version:'Governance_v0.2',approval_date:'2026-10-22',approval_source:'USER_EXPLICIT_CHAT_CONFIRMATION_2026-10-22',approver_role:'PROJECT_OWNER',approver_name:'NOT_PROVIDED_IN_APPROVAL_MESSAGE',approval_scope:'GOVERNANCE_RULES_ONLY',signature_method:'EXPLICIT_CHAT_CONFIRMATION',identity_verification:'NOT_INDEPENDENTLY_VERIFIED',signature_time:'NOT_PROVIDED_IN_APPROVAL_MESSAGE',approval_time_precision:'DATE_ONLY'};
export const sourceDiff='workspaces/phase1c_mechanism_evidence_pilot/governance_v0.2_dryrun/Governance_Decision_Diff_v0.1_to_v0.2.csv';
export const sourceRecord='workspaces/phase1c_mechanism_evidence_pilot/governance_v0.2_dryrun/Governance_Decision_Record_v0.2.md';
export const basicIds=new Set([1,4,5,6,7,9,10,12,14,15,16,17,18,20,24].map(n=>'GOV-'+String(n).padStart(2,'0')));

export async function csv(file){
 const text=await fs.readFile(file,'utf8');const wb=await Workbook.fromCSV(text.replace(/^\uFEFF/,''),{sheetName:'Records'});
 const matrix=wb.worksheets.getItemAt(0).getUsedRange().values;const headers=matrix[0].map(String);
 return {headers,rows:matrix.slice(1).filter(r=>r.some(v=>v!==null&&v!=='')).map(r=>Object.fromEntries(headers.map((h,i)=>[h,String(r[i]??'')]))),wb};
}
const escape=v=>/[",\r\n]/.test(String(v??''))?'"'+String(v??'').replaceAll('"','""')+'"':String(v??'');
const serialize=(h,r)=>[h,...r.map(row=>h.map(k=>String(row[k]??'')))].map(row=>row.map(escape).join(',')).join('\n')+'\n';

async function captureBaseline(){
 const target=path.join(dir,'qc/Start_Baseline.json');
 try{await fs.access(target);throw Error('Refusing to overwrite existing baseline');}catch(e){if(e.code!=='ENOENT')throw e;}
 if(git('rev-parse','HEAD')!==SOURCE_COMMIT||git('branch','--show-current')!==TASK_BRANCH)throw Error('Unexpected task branch/source HEAD');
 const tracked=[];for(const p of git('ls-files').split(/\r?\n/))tracked.push({path:p,sha256:sha(await fs.readFile(path.join(root,p)))});
 const prior=JSON.parse(await fs.readFile(path.join(pilot,'governance_v0.2_dryrun/qc/Start_Baseline.json'),'utf8'));
 const local_source_cache=[];for(const r of prior.local_source_cache)local_source_cache.push({path:r.path,sha256:sha(await fs.readFile(r.path))});
 const evidence=await fs.readFile(ATTACHMENT);const text=evidence.toString('utf8');if(!text.includes(QUOTE)||!text.includes('2026-10-22'))throw Error('Expected user-declared approval not found');
 const baseline={date:'2026-10-22',source_branch:SOURCE_BRANCH,source_commit:SOURCE_COMMIT,task_branch:TASK_BRANCH,main:git('rev-parse','main'),merge_base:git('merge-base','main','HEAD'),initial_worktree_before_task:'CLEAN',capture_git_status:git('status','--short'),approval_declaration:{...metadata,declared_confirmation:QUOTE,declaration_received_via:'CURRENT_USER_TASK_ATTACHMENT_REPORTING_PRIOR_CHAT_CONFIRMATION',attachment_path:ATTACHMENT,attachment_sha256:sha(evidence),independent_chat_transcript_access:'NOT_PERFORMED',external_identity_or_signature_certificate:'NONE'},tracked,local_source_cache};
 await fs.mkdir(path.dirname(target),{recursive:true});await fs.writeFile(target,JSON.stringify(baseline,null,2)+'\n');
 console.log(JSON.stringify({baseline:target,tracked:tracked.length,cache:local_source_cache.length}));
}

export async function archive(){
 const original=await csv(path.join(root,sourceDiff));
 if(original.rows.length!==24)throw Error('Expected 24 governance decisions');
 const sourceBlob=execFileSync('git',['show',SOURCE_COMMIT+':'+sourceDiff],{cwd:root});const sourceHash=sha(sourceBlob);
 const rows=original.rows.map(r=>({decision_id:r.decision_id,governance_approval_status:'APPROVED',approval_scope:'GOVERNANCE_RULES_ONLY',approved_rule_text:r.v02_recommendation,approved_version:'Governance_v0.2',approval_date:metadata.approval_date,decision_group:basicIds.has(r.decision_id)?'BASIC_PRINCIPLE':'IMPLEMENTATION_POLICY',topic:r.topic,record_type:'GOVERNANCE_APPROVAL',approver_role:metadata.approver_role,approver_name:metadata.approver_name,approval_source:metadata.approval_source,signature_method:metadata.signature_method,identity_verification:metadata.identity_verification,signature_time:metadata.signature_time,approval_time_precision:metadata.approval_time_precision,implemented_in_production:'NO',evidence_scientific_approval:'NOT_GRANTED',effective_scope:'FUTURE_MECHANISM_EVIDENCE_DATABASE_GOVERNANCE',source_branch:SOURCE_BRANCH,source_commit:SOURCE_COMMIT,source_rule_path:sourceDiff,source_full_rule_record:sourceRecord,source_rule_file_sha256:sourceHash,approved_rule_text_sha256:sha(r.v02_recommendation),source_rule_selector:r.decision_id,prior_recommendation_state:r.recommendation_state,prior_formal_approval_status:r.formal_approval_status,implementation_preconditions:r.preconditions,applicable_scope:r.applicable_scope}));
 const headers=Object.keys(rows[0]);const wb=Workbook.create();const sheet=wb.worksheets.add('Approved_Governance');
 sheet.getRangeByIndexes(0,0,25,headers.length).values=[headers,...rows.map(r=>headers.map(h=>r[h]))];wb.recalculate();
 const matrix=sheet.getRangeByIndexes(0,0,25,headers.length).values;
 const roundtrip=matrix.slice(1).map(r=>Object.fromEntries(headers.map((h,i)=>[h,String(r[i]??'')])));
 if(JSON.stringify(roundtrip)!==JSON.stringify(rows))throw Error('Artifact authoring roundtrip changed content');
 const matrixPath=path.join(dir,'Governance_Approved_Decision_Matrix_v0.2.csv');await fs.writeFile(matrixPath,serialize(headers,roundtrip));
 const historical=[
 [sourceRecord,'V02_POLICY_TEXT_FULL_RECORD'],
 [sourceDiff,'V02_24_RULE_TEXTS_AND_HISTORY'],
 ['workspaces/phase1c_mechanism_evidence_pilot/governance_v0.1/Mechanism_Evidence_Governance_Decision_v0.1.md','INHERITED_DEFINITIONS_V02_POLICY_OVERRIDES_PREVAIL'],
 ['workspaces/phase1c_mechanism_evidence_pilot/governance_v0.1/Mechanism_Evidence_Controlled_Vocabulary_v0.1.csv','INHERITED_CONTROLLED_VOCABULARY'],
 ['workspaces/phase1c_mechanism_evidence_pilot/governance_v0.1/Mechanism_Evidence_Gate_Criteria_v0.1.md','INHERITED_GATE_CRITERIA_NOT_GATE_PASS'],
 ['workspaces/phase1c_mechanism_evidence_pilot/governance_v0.1/Mechanism_Evidence_Entity_Relationship_Design_v0.1.md','GOVERNANCE_DESIGN_REFERENCE'],
 ['workspaces/phase1c_mechanism_evidence_pilot/governance_v0.2_dryrun/schema/Mechanism_Evidence_Schema_v0.2.md','SCHEMA_DESIGN_REFERENCE_NOT_PRODUCTION_ACCEPTANCE'],
 ['workspaces/phase1c_mechanism_evidence_pilot/governance_v0.2_dryrun/schema/Table_Contract_v0.2.json','TECHNICAL_REFERENCE_ONLY_NOT_FROZEN_PRODUCTION_DATA']
 ];
 const files=[];
 for(const [p,role]of historical){
  const blob=execFileSync('git',['show',SOURCE_COMMIT+':'+p],{cwd:root});
  files.push({path:p,role,sha256:sha(blob),sha256_basis:'GIT_BLOB_BYTES_AT_SOURCE_COMMIT',git_blob_oid:git('rev-parse',SOURCE_COMMIT+':'+p),working_tree_sha256:sha(await fs.readFile(path.join(root,p))),source_commit:SOURCE_COMMIT,approval_applicability:'POLICY_OR_DESIGN_SCOPE_ONLY_NOT_HISTORICAL_EVIDENCE_ASSERTIONS'});
 }
 for(const p of ['Governance_Formal_Approval_Record_v0.2.md','Governance_Approved_Decision_Matrix_v0.2.csv'])files.push({path:rel(path.join(dir,p)),role:'CURRENT_GOVERNANCE_APPROVAL_ARCHIVE',sha256:sha(await fs.readFile(path.join(dir,p))),sha256_basis:'ARCHIVE_UTF8_BYTES_NO_SELF_REFERENTIAL_COMMIT',source_commit:'ARCHIVE_COMMIT_REPORTED_IN_FINAL_REPLY_AND_GIT_HISTORY'});
 const baseline=JSON.parse(await fs.readFile(path.join(dir,'qc/Start_Baseline.json'),'utf8'));
 const manifest={...metadata,governance_approval_status:'APPROVED',decision_ids:rows.map(r=>r.decision_id),basic_principles:rows.filter(r=>r.decision_group==='BASIC_PRINCIPLE').map(r=>r.decision_id),implementation_policies:rows.filter(r=>r.decision_group==='IMPLEMENTATION_POLICY').map(r=>r.decision_id),effective_scope:'FUTURE_MECHANISM_EVIDENCE_DATABASE_GOVERNANCE',excluded_scopes:['EVIDENCE_SCIENTIFIC_APPROVAL','PRODUCTION_MIGRATION','CANDIDATE_EXPANSION','NETWORK_MEDICINE_ANALYSIS','FORMAL_ANALYSIS_OR_RANKING','DATABASE_RELEASE'],source_branch:SOURCE_BRANCH,source_commit:SOURCE_COMMIT,archive_branch:TASK_BRANCH,approval_declaration:baseline.approval_declaration,rule_files:files,precedence:['THIS_APPROVAL_ARCHIVE_CONTROLS_GOVERNANCE_APPROVAL_STATUS_ONLY','V02_DECISION_TEXTS_AND_FULL_RECORD_CONTROL_IMPLEMENTATION_POLICY','V01_DEFINITIONS_VOCABULARY_AND_GATE_CRITERIA_APPLY_WHERE_NOT_OVERRIDDEN_BY_V02'],historical_pending_labels:'PRESERVED_AS_HISTORY_NOT_REWRITTEN; CURRENT_STATUS_IN_NEW_APPROVAL_MATRIX',dryrun_data_status:'NON_PRODUCTION_DRYRUN_UNCHANGED_NOT_FROZEN_AS_PRODUCTION',subsequent_change_requirements:['NEW_VERSION_AND_APPEND_ONLY_CHANGE_RECORD','EXPLICIT_PROJECT_OWNER_AUTHORIZATION_FOR_GOVERNANCE_CHANGE','IMPACT_ASSESSMENT_AND_NEW_CONTENT_HASHES','DO_NOT_OVERWRITE_APPROVED_V02','SEPARATE_AUTHORIZATION_FOR_PRODUCTION_MIGRATION_EVIDENCE_APPROVAL_AND_RELEASE'],current_gate_and_authorization:{Governance_v0_2:'APPROVED',Gate1:'HOLD',Gate2:'HUMAN_SCIENTIFIC_REVIEW_REQUIRED',Scale_up_S1:'NOT_AUTHORIZED',Scale_up_S2:'NOT_AUTHORIZED',Scale_up_S3:'NOT_AUTHORIZED',Scale_up_S4:'NOT_AUTHORIZED',Release:'HOLD',Production_migration:'NOT_AUTHORIZED'}};
 await fs.writeFile(path.join(dir,'Governance_Approved_Baseline_Manifest_v0.2.json'),JSON.stringify(manifest,null,2)+'\n');
 console.log(JSON.stringify({decisions:24,basic:15,implementation_policies:9,hashed_rule_references:files.length,production_implementation:'NO',evidence_approval:'NOT_GRANTED'}));
}
if(process.argv[1]&&import.meta.url===pathToFileURL(path.resolve(process.argv[1])).href){if(process.argv.includes('--capture-baseline'))await captureBaseline();else await archive();}
