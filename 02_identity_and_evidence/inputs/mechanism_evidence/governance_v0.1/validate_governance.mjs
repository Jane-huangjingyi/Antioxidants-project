// Read-only checks of legacy data; writes only QC results/previews in this folder.
import fs from 'node:fs/promises';
import path from 'node:path';
import crypto from 'node:crypto';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { Workbook } from '@oai/artifact-tool';

const dir=path.dirname(fileURLToPath(import.meta.url));
const root=path.resolve(dir,'../../..');
const pilot=path.resolve(dir,'..');
const hash=bytes=>crypto.createHash('sha256').update(bytes).digest('hex');
const baseline=JSON.parse(await fs.readFile(path.join(dir,'Start_Baseline.json'),'utf8'));
const checks=[];
const check=(id,ok,detail)=>{checks.push({id,pass:!!ok,detail});};
async function csv(file){
  const raw=await fs.readFile(file,'utf8');
  const wb=await Workbook.fromCSV(raw.replace(/^\uFEFF/,''),{sheetName:'Records'});
  const values=wb.worksheets.getItemAt(0).getUsedRange().values;
  const headers=values[0].map(String);
  const rows=values.slice(1).filter(r=>r.some(v=>v!==null&&v!==''))
    .map(row=>Object.fromEntries(headers.map((k,i)=>[k,String(row[i]??'')])));
  return {wb,headers,rows};
}
const trackedDiff=[],cacheDiff=[];
for(const record of baseline.tracked){
  try{if(hash(await fs.readFile(path.join(root,record.path)))!==record.sha256)trackedDiff.push(record.path);}
  catch{trackedDiff.push(record.path);}
}
for(const record of baseline.local_source_cache){
  try{if(hash(await fs.readFile(record.path))!==record.sha256)cacheDiff.push(record.path);}
  catch{cacheDiff.push(record.path);}
}
check('legacy_tracked_hashes',!trackedDiff.length,{count:baseline.tracked.length,changed:trackedDiff});
check('legacy_source_cache_hashes',!cacheDiff.length,{count:baseline.local_source_cache.length,changed:cacheDiff});
const evidence=await csv(path.join(pilot,'compounds/AFF-0061_Protocatechuic_Acid_Mechanism_Evidence.csv'));
const dict=await csv(path.join(pilot,'dictionaries/Mechanism_Evidence_Field_Dictionary.csv'));
const review=await csv(path.join(pilot,'gate2_review/AFF-0061_Gate2_Evidence_Review_Matrix.csv'));
const studies=await csv(path.join(pilot,'master/Study_Register.csv'));
const coverage=await csv(path.join(pilot,'indexes/Compound_Mechanism_Coverage.csv'));
const oldFields=await csv(path.join(pilot,'gate2_review/Existing_66_Field_Review_Coverage.csv'));
const matrix=await csv(path.join(dir,'Governance_Decision_Matrix_v0.1.csv'));
const vocab=await csv(path.join(dir,'Mechanism_Evidence_Controlled_Vocabulary_v0.1.csv'));
const count=(rows,key)=>Object.fromEntries([...new Set(rows.map(r=>r[key]))].sort().map(k=>[k,rows.filter(r=>r[key]===k).length]));
check('legacy_counts',evidence.rows.length===21&&dict.rows.length===66&&coverage.rows.length===191,{observations:evidence.rows.length,fields:dict.rows.length,coverage:coverage.rows.length,publication_register:studies.rows.length});
check('master_byte_identity',hash(await fs.readFile(path.join(pilot,'master/Compound_Mechanism_Evidence_Master.csv')))===hash(await fs.readFile(path.join(pilot,'compounds/AFF-0061_Protocatechuic_Acid_Mechanism_Evidence.csv'))),'Master and compound CSV remain byte-identical');
check('stable_evidence_id',new Set(evidence.rows.map(r=>r.evidence_id)).size===21,'21 stable unique IDs');
check('publication_counts',studies.rows.length===15&&studies.rows.filter(r=>Number(r.evidence_record_count)>0).length===10,'15 publication register entries; 10 with included observations; not independent experiment counts');
check('unsearched_not_zero',coverage.rows.filter(r=>r.search_status==='NOT_SEARCHED').length===190&&coverage.rows.filter(r=>r.search_status==='NOT_SEARCHED').every(r=>r.included_unique_publication_count===''&&r.evidence_record_count===''&&r.evidence_count_status==='NOT_ASSESSED_NOT_ZERO'),'190 unsearched candidates keep blank counts, not zero');
check('original_json_unchanged',review.rows.length===21&&review.rows.every(r=>{
  const orig=JSON.parse(r.original_record_json);const row=evidence.rows.find(x=>x.evidence_id===r.evidence_id);
  return row&&evidence.headers.every(k=>row[k]===String(orig[k]??''));
}),'all 66 original attributes in Gate2 snapshots equal legacy evidence');
check('zero_human_approvals',evidence.rows.every(r=>r.human_review_status==='NOT_REVIEWED')&&review.rows.every(r=>r.human_review_status==='NOT_REVIEWED'&&r.proposal_applied==='NO'),'No approval or scientific writeback');
check('governance_decisions',matrix.rows.length===24&&new Set(matrix.rows.map(r=>r.decision_id)).size===24&&matrix.rows.every(r=>r.human_decision_status==='HUMAN_DECISION_REQUIRED'&&r.change_applied==='NO'),count(matrix.rows,'approval_recommendation'));
check('decision_readiness_counts',matrix.rows.filter(r=>r.approval_recommendation==='READY_FOR_HUMAN_APPROVAL').length===15&&matrix.rows.filter(r=>r.approval_recommendation==='DISCUSSION_REQUIRED').length===9,'15 ready recommendations and 9 discussions; none approved');
check('vocabulary_uniqueness',new Set(vocab.rows.map(r=>r.field+'::'+r.value)).size===vocab.rows.length&&vocab.rows.every(r=>vocab.headers.every(k=>r[k])&&r.rule_status==='PROPOSED_NOT_APPROVED'),{rows:vocab.rows.length,fields:new Set(vocab.rows.map(r=>r.field)).size});
for(const [field,n] of [['evidence_relation_type',5],['target_confirmation_class',7],['antioxidant_relevance_primary',6],['review_state',6]]){
 check('enum_'+field,vocab.rows.filter(r=>r.field===field).length===n,{expected:n});
}
check('vocabulary_primary_membership',review.rows.every(r=>vocab.rows.some(v=>v.field==='antioxidant_relevance_primary'&&v.value===r.antioxidant_relevance_proposed)),'all Gate2 proposed primary categories allowed; does not apply them');
check('vocabulary_target_membership',review.rows.every(r=>vocab.rows.some(v=>v.field==='target_confirmation_class'&&v.value===r.protein_target_confirmation_proposed)),'all Gate2 proposed target classes allowed; does not apply them');
const impact=await fs.readFile(path.join(dir,'Mechanism_Evidence_Migration_Impact_Assessment_v0.1.md'),'utf8');
const fieldMap=[...impact.matchAll(/^\| (\d+) \| ([a-zA-Z_]+) \| ([MR]) \|/gm)].map(m=>({order:Number(m[1]),field:m[2],priority:m[3]}));
check('all_66_fields_mapped',fieldMap.length===66&&dict.rows.every((r,i)=>fieldMap[i]?.field===r.field_name&&fieldMap[i]?.order===i+1),'each original field mapped once in original dictionary order');
const must=oldFields.rows.filter(r=>r.review_priority==='MUST_CHANGE_BEFORE_SCALE_UP').map(r=>r.field_name).sort();
check('17_must_fields_consistent',JSON.stringify(fieldMap.filter(r=>r.priority==='M').map(r=>r.field).sort())===JSON.stringify(must),{must_change_fields:must});
check('all_21_impact_examples',evidence.rows.every(r=>impact.includes('| '+r.evidence_id.replace('ME-AFF0061-','')+' |')),'21 stable IDs covered without reclassification writeback');
const fileNames=['Mechanism_Evidence_Governance_Decision_v0.1.md','Governance_Decision_Matrix_v0.1.csv','Sync_to_ChatGPT_Phase1C_Governance_v0.1.md','Mechanism_Evidence_Controlled_Vocabulary_v0.1.csv','Mechanism_Evidence_Entity_Relationship_Design_v0.1.md','Mechanism_Evidence_Gate_Criteria_v0.1.md','Mechanism_Evidence_Migration_Impact_Assessment_v0.1.md','Governance_QC_Report_v0.1.md'];
const missing=[];for(const name of fileNames){try{if(!(await fs.stat(path.join(dir,name))).size)missing.push(name);}catch{missing.push(name);}}
check('eight_deliverables',!missing.length,{missing});
const gate=await fs.readFile(path.join(dir,'Mechanism_Evidence_Gate_Criteria_v0.1.md'),'utf8');
check('four_permission_scopes',['S1 收集','S2 纳入','S3 分析','S4 正式'].every(t=>gate.includes(t)),'all four permissions separately proposed and not authorized');
const gitStatus=execFileSync('git',['status','--porcelain=v1','--untracked-files=all'],{cwd:root,encoding:'utf8'}).trim();
const branch=execFileSync('git',['branch','--show-current'],{cwd:root,encoding:'utf8'}).trim();
const head=execFileSync('git',['rev-parse','HEAD'],{cwd:root,encoding:'utf8'}).trim();
const outside=gitStatus?gitStatus.split(/\r?\n/).filter(line=>!line.slice(3).replaceAll('"','').startsWith('workspaces/phase1c_mechanism_evidence_pilot/governance_v0.1/')):[];
check('only_governance_changes',!outside.length,{outside});
check('task_branch',branch==='codex/phase1c-governance-v0.1',{branch,head,baseline_head:baseline.head});
await fs.mkdir(path.join(dir,'qc_previews'),{recursive:true});
for(const [name,item] of [['decision_matrix',matrix],['controlled_vocabulary',vocab]]){
 item.wb.recalculate();
 const inspect=await item.wb.inspect({kind:'table',range:'Records!A1:D4',include:'values,formulas',tableMaxRows:4,tableMaxCols:4,maxChars:1500});
 const errors=await item.wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#NUM!|#NULL!|#SPILL!|#CALC!',options:{useRegex:true,maxResults:20},summary:'CSV literal error token scan'});
 check('csv_no_error_tokens_'+name,!item.rows.some(r=>Object.values(r).some(v=>/#REF!|#DIV\/0!|#VALUE!|#NAME\?|#NUM!|#NULL!|#SPILL!|#CALC!/.test(v))),'literal cell scan and saved Artifact inspection; no spreadsheet formulas delivered');
 const sheet=item.wb.worksheets.getItemAt(0);
 sheet.getRange('A1:D6').format.font={name:'Arial',size:11};
 sheet.getRange('A1:D6').format.wrapText=true;
 sheet.getRange('A1:D6').format.columnWidth=35;
 sheet.getRange('A1:D6').format.rowHeight=100;
 sheet.getRange('A1:D1').format.font={name:'Arial',size:11,bold:true};
 const preview=await item.wb.render({sheetName:'Records',range:'A1:D6',scale:1,format:'png'});
 await fs.writeFile(path.join(dir,'qc_previews',name+'.png'),new Uint8Array(await preview.arrayBuffer()));
 await fs.writeFile(path.join(dir,'qc_previews',name+'_inspection.json'),JSON.stringify({inspection:inspect.ndjson,error_scan:errors.ndjson},null,2));
 check('artifact_csv_'+name,item.rows.length>0&&item.headers.length>0,{rows:item.rows.length,columns:item.headers.length,inspection:'qc_previews/'+name+'_inspection.json',preview:'qc_previews/'+name+'.png',note:'CSV only; no formulas or production workbook exported'});
}
const result={date:'2026-10-21',timezone:'Asia/Shanghai',phase:'GOVERNANCE_DOCUMENT_QC_NOT_GATE_APPROVAL',branch,head_at_check:head,baseline_head:baseline.head,tracked_checked:baseline.tracked.length,cache_checked:baseline.local_source_cache.length,governance_files_expected:8,decision_count:24,decision_readiness:count(matrix.rows,'approval_recommendation'),vocabulary_rows:vocab.rows.length,gate2_review_status:count(review.rows,'review_status'),gate2_target_classes:count(review.rows,'protein_target_confirmation_proposed'),gate2_antioxidant_primary:count(review.rows,'antioxidant_relevance_proposed'),checks,pass:checks.filter(c=>c.pass).length,fail:checks.filter(c=>!c.pass).length};
await fs.writeFile(path.join(dir,'Governance_Validation_v0.1.json'),JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify({pass:result.pass,fail:result.fail,tracked:result.tracked_checked,cache:result.cache_checked,vocabulary_rows:result.vocabulary_rows,decisions:result.decision_readiness,failed:checks.filter(c=>!c.pass)},null,2));
if(result.fail)process.exitCode=1;
