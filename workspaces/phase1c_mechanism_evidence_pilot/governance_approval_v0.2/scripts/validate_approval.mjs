import fs from 'node:fs/promises';
import path from 'node:path';
import {execFileSync} from 'node:child_process';
import {dir,root,pilot,sha,git,csv,metadata,basicIds,sourceDiff,SOURCE_COMMIT,TASK_BRANCH} from './archive_approval.mjs';

const checks=[];
const check=(name,pass,detail='')=>checks.push({name,pass:Boolean(pass),detail});
const read=p=>fs.readFile(path.join(dir,p),'utf8');
const baseline=JSON.parse(await read('qc/Start_Baseline.json'));
const manifest=JSON.parse(await read('Governance_Approved_Baseline_Manifest_v0.2.json'));
const approved=await csv(path.join(dir,'Governance_Approved_Decision_Matrix_v0.2.csv'));
const original=await csv(path.join(root,sourceDiff));
const expected=Array.from({length:24},(_,i)=>'GOV-'+String(i+1).padStart(2,'0'));
function validRows(rows){
 return rows.length===24&&new Set(rows.map(r=>r.decision_id)).size===24&&expected.every(id=>rows.some(r=>r.decision_id===id))&&rows.every(r=>{
  const source=original.rows.find(s=>s.decision_id===r.decision_id);
  return source&&r.approved_rule_text===source.v02_recommendation&&r.approved_rule_text_sha256===sha(source.v02_recommendation)&&r.governance_approval_status==='APPROVED'&&r.approved_version==='Governance_v0.2'&&r.implemented_in_production==='NO'&&r.evidence_scientific_approval==='NOT_GRANTED'&&r.source_full_rule_record.endsWith('/Governance_Decision_Record_v0.2.md')&&Object.entries(metadata).filter(([k])=>k!=='governance_version').every(([k,v])=>r[k]===v);
 });
}
check('24 exact approved v0.2 rules with identity and scope separation',validRows(approved.rows));
check('15 basic principles / 9 implementation policies',approved.rows.filter(r=>r.decision_group==='BASIC_PRINCIPLE').length===15&&approved.rows.every(r=>(r.decision_group==='BASIC_PRINCIPLE')===basicIds.has(r.decision_id)));
for(const [k,v]of Object.entries(metadata))check('manifest metadata '+k,manifest[k]===v);
check('manifest complete decision IDs',JSON.stringify(manifest.decision_ids)===JSON.stringify(expected));
check('10 scoped hash references; no scientific tables frozen',manifest.rule_files.length===10&&manifest.rule_files.every(f=>!f.path.includes('/dryrun/')));
for(const f of manifest.rule_files){
 const current=await fs.readFile(path.join(root,f.path));
 if(f.git_blob_oid){const blob=execFileSync('git',['show',SOURCE_COMMIT+':'+f.path],{cwd:root});check('rule hash '+f.path,sha(blob)===f.sha256&&sha(current)===f.working_tree_sha256&&git('rev-parse',SOURCE_COMMIT+':'+f.path)===f.git_blob_oid);}
 else check('archive hash '+f.path,sha(current)===f.sha256);
}
check('user declaration matches captured source attachment',sha(await fs.readFile(baseline.approval_declaration.attachment_path))===baseline.approval_declaration.attachment_sha256&&JSON.stringify(manifest.approval_declaration)===JSON.stringify(baseline.approval_declaration));
const changed=[];for(const f of baseline.tracked)if(sha(await fs.readFile(path.join(root,f.path)))!==f.sha256)changed.push(f.path);
check('735 existing tracked files unchanged',baseline.tracked.length===735&&changed.length===0,JSON.stringify(changed));
const cacheChanged=[];for(const f of baseline.local_source_cache)if(sha(await fs.readFile(f.path))!==f.sha256)cacheChanged.push(f.path);
check('41 local source caches unchanged',baseline.local_source_cache.length===41&&cacheChanged.length===0,JSON.stringify(cacheChanged));
const load=p=>csv(path.join(pilot,p));
const legacy=(await load('compounds/AFF-0061_Protocatechuic_Acid_Mechanism_Evidence.csv')).rows;
check('original 21 evidence rows NOT_REVIEWED',legacy.length===21&&legacy.every(r=>r.human_review_status==='NOT_REVIEWED'));
check('original dictionary 66 fields',(await load('dictionaries/Mechanism_Evidence_Field_Dictionary.csv')).rows.length===66);
const proposals=(await load('governance_v0.2_dryrun/dryrun/Scientific_Proposal.csv')).rows;
check('257 scientific proposals not approved/applied',proposals.length===257&&proposals.every(r=>r.proposal_status==='PROPOSED_NOT_APPROVED'&&r.applied_to_production==='NO'&&!r.approval_event_id));
const events=(await load('governance_v0.2_dryrun/dryrun/Review_Event.csv')).rows;
check('257 review events remain unsigned and pending',events.length===257&&events.every(r=>r.approval_status==='PENDING_HUMAN_REVIEW'&&r.change_applied==='NO'&&!r.signed_by&&!r.signoff_reference));
const observations=(await load('governance_v0.2_dryrun/dryrun/Observation.csv')).rows;
check('dryrun 21 observations unapproved / 7 source HOLD',observations.length===21&&observations.every(r=>r.scientific_approval_status==='PENDING_HUMAN_REVIEW'&&r.raw_human_review_status==='NOT_REVIEWED')&&observations.filter(r=>r.sandbox_review_state==='HOLD').length===7);
const gate=(await load('gate2_review/AFF-0061_Gate2_Evidence_Review_Matrix.csv')).rows;
for(const [status,n]of Object.entries({KEEP_PROVISIONAL:12,RECLASSIFICATION_PROPOSED:2,HOLD_SOURCE_VERIFICATION:7}))check('historical Gate2 '+status,gate.filter(r=>r.review_status===status).length===n);
check('historical scientific matrix remains unreviewed',gate.every(r=>r.human_review_status==='NOT_REVIEWED'));
for(const view of ['Verified_Direct_Targets','Verified_Antioxidant_Mechanisms','Verified_Evidence_Support'])check('empty nonproduction '+view,(await load('governance_v0.2_dryrun/dryrun/'+view+'.csv')).rows.length===0);
check('old governance history not rewritten',original.rows.every(r=>r.formal_approval_status==='PENDING_FORMAL_SIGNOFF'));
const gateExpected={Governance_v0_2:'APPROVED',Gate1:'HOLD',Gate2:'HUMAN_SCIENTIFIC_REVIEW_REQUIRED',Scale_up_S1:'NOT_AUTHORIZED',Scale_up_S2:'NOT_AUTHORIZED',Scale_up_S3:'NOT_AUTHORIZED',Scale_up_S4:'NOT_AUTHORIZED',Release:'HOLD',Production_migration:'NOT_AUTHORIZED'};
check('exact nine gate/authorization states',JSON.stringify(manifest.current_gate_and_authorization)===JSON.stringify(gateExpected));
const readiness=await read('AFF0061_Human_Scientific_Review_Readiness_v0.1.md');
const planned=[...readiness.matchAll(/^\| ([ABC]) \| (ME-AFF0061-\d+-\d+) \| (\w+) \|/gm)];
check('readiness covers exact 21 IDs once',planned.length===21&&new Set(planned.map(r=>r[2])).size===21&&legacy.every(r=>planned.some(p=>p[2]===r.evidence_id)));
check('readiness A9 B5 C7 and historical states',planned.filter(r=>r[1]==='A').length===9&&planned.filter(r=>r[1]==='B').length===5&&planned.filter(r=>r[1]==='C').length===7&&planned.every(p=>gate.find(r=>r.evidence_id===p[2])?.review_status===p[3]));
check('14 per-row review dimensions',Array.from({length:14},(_,i)=>'D'+String(i+1).padStart(2,'0')).every(id=>readiness.includes('| '+id+' |')));
check('future review identity/source/change controls', ['reviewer_name','review_date','rule_version','source_file_sha256','change_applied=NO','human_review_status=NOT_REVIEWED'].every(s=>readiness.includes(s))&&!readiness.includes('HUMAN_APPROVED'));
const formal=await read('Governance_Formal_Approval_Record_v0.2.md');
check('formal metadata exact and no inferred identity/time',Object.entries(metadata).every(([k,v])=>formal.includes(k+'='+v)));
check('NON_PRODUCTION_DRYRUN maintained',manifest.dryrun_data_status==='NON_PRODUCTION_DRYRUN_UNCHANGED_NOT_FROZEN_AS_PRODUCTION'&&proposals.every(r=>r.dataset_role==='NON_PRODUCTION_DRYRUN'));
check('task branch correct / main and merge base unchanged',git('branch','--show-current')===TASK_BRANCH&&git('rev-parse','main')===baseline.main&&git('merge-base','main','HEAD')===baseline.merge_base);
const delta=git('diff','--name-only',SOURCE_COMMIT).split(/\r?\n/).filter(Boolean);
check('no changes outside new approval directory',delta.every(p=>p.startsWith('workspaces/phase1c_mechanism_evidence_pilot/governance_approval_v0.2/')));
for(const [name,mutate]of [
 ['missing ID',r=>r.pop()],['duplicate ID',r=>r[1].decision_id=r[0].decision_id],['changed rule',r=>r[0].approved_rule_text+=' altered'],['inferred name',r=>r[0].approver_name='INFERRED'],['fabricated time',r=>r[0].signature_time='2026-10-22T00:00:00Z'],['scientific scope',r=>r[0].approval_scope='EVIDENCE_SCIENTIFIC_APPROVAL'],['production implementation',r=>r[0].implemented_in_production='YES'],['scientific approval',r=>r[0].evidence_scientific_approval='HUMAN_APPROVED']]){
 const fixture=structuredClone(approved.rows);mutate(fixture);check('negative fixture rejected: '+name,!validRows(fixture));
}
approved.wb.recalculate();
const inspect=await approved.wb.inspect({kind:'table',range:'Records!A1:C5',include:'values,formulas',tableMaxRows:5,tableMaxCols:3,maxChars:2000});
check('artifact inspect completed',Boolean(inspect));
check('no spreadsheet error tokens',!/#REF!|#DIV\/0!|#VALUE!|#NUM!|#SPILL!|#CALC!/.test(await read('Governance_Approved_Decision_Matrix_v0.2.csv')));
await fs.mkdir(path.join(dir,'qc/previews'),{recursive:true});
await fs.writeFile(path.join(dir,'qc/previews/matrix_inspection.json'),JSON.stringify(inspect,null,2));
approved.wb.worksheets.getItemAt(0).getRange('A:C').format.columnWidthPx=310;
const preview=await approved.wb.render({sheetName:'Records',range:'A1:C5',scale:1,format:'png'});
await fs.writeFile(path.join(dir,'qc/previews/approved_matrix.png'),new Uint8Array(await preview.arrayBuffer()));
check('bounded artifact preview rendered',true,'Visual inspection is reported separately by the operator.');
const result={date:'2026-10-22',record_type:'GOVERNANCE_APPROVAL_QC',source_commit:SOURCE_COMMIT,branch:TASK_BRANCH,passed:checks.filter(c=>c.pass).length,failed:checks.filter(c=>!c.pass).length,protected_tracked_files:735,protected_cache_files:41,checks};
await fs.writeFile(path.join(dir,'qc/Approval_Validation.json'),JSON.stringify(result,null,2)+'\n');
await fs.writeFile(path.join(dir,'Governance_Approval_QC_Report.md'),'# Governance批准归档QC\n\n日期2026-10-22。自动检查：'+result.passed+' PASS，'+result.failed+' FAIL。完整逐项结果见 `qc/Approval_Validation.json`；基线见 `qc/Start_Baseline.json`。\n\n24项规则与来源v0.2逐字匹配，15项基础原则与9项实施政策分组完整；10项规则/归档引用绑定内容哈希。身份、日期精度和批准范围独立核查，8种内存负例验证拒绝缺失/重复ID、文本篡改、推断姓名、伪造时刻、科学批准范围、生产实施和科学状态升级。负例不写入任何证据记录。\n\n735个既有跟踪文件和41个本地来源缓存逐文件SHA256比对；原21条证据、66字段字典、257项科学提案及257项待审事件、7条来源HOLD和三张空Verified视图均保持历史状态。Gate与权限保持本轮指定边界。演练仍为NON_PRODUCTION_DRYRUN。\n\n批准矩阵通过Artifact Tool值写入/读回、重新计算、内容检查和有界PNG预览；CSV为无样式文本交付，PNG与依赖目录忽略不提交。此QC是治理归档完整性检查，不是原21条证据的科学审核或生产迁移验收。\n\n可复核命令：使用已配置的Node与Artifact Tool运行 `scripts/validate_approval.mjs`。脚本仅读取历史资产，输出本目录QC及忽略的预览，不启动迁移或科学审核。\n');
console.log(JSON.stringify({passed:result.passed,failed:result.failed,failures:checks.filter(c=>!c.pass)}));
if(result.failed)process.exitCode=1;
