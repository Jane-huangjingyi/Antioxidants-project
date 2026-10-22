import fs from 'node:fs/promises';
import path from 'node:path';
import crypto from 'node:crypto';
import {fileURLToPath} from 'node:url';
import {Workbook} from '@oai/artifact-tool';
export const workspace=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
export const root=path.resolve(workspace,'../../..');
export const pilot=path.resolve(workspace,'..');
export const ROLE='NON_PRODUCTION_DRYRUN';
export const PROPOSED='PROPOSED_NOT_APPROVED';
export const DATE='2026-10-22';
export const sha=bytes=>crypto.createHash('sha256').update(bytes).digest('hex');
export const json=value=>JSON.stringify(value);
export const quote=value=>/[",\r\n]/.test(String(value??''))?'"'+String(value??'').replaceAll('"','""')+'"':String(value??'');
export const serialize=(headers,rows)=>headers.map(quote).join(',')+'\n'+rows.map(r=>headers.map(h=>quote(r[h])).join(',')).join('\n')+(rows.length?'\n':'');
export async function readCSV(file){
 const text=await fs.readFile(file,'utf8');
 const wb=await Workbook.fromCSV(text.replace(/^\uFEFF/,''),{sheetName:'Records'});
 const matrix=wb.worksheets.getItemAt(0).getUsedRange().values;
 const headers=matrix[0].map(String);
 const rows=matrix.slice(1).filter(r=>r.some(v=>v!==null&&v!==''))
  .map(r=>Object.fromEntries(headers.map((h,i)=>[h,String(r[i]??'')])));
 return {headers,rows,wb,text};
}
export async function writeCSV(file,headers,rows){
 await fs.mkdir(path.dirname(file),{recursive:true});
 const h=['dataset_role','schema_version',...headers];
 const objects=rows.map(r=>({dataset_role:ROLE,schema_version:'0.2_DRYRUN',...r}));
 // Author through documented Artifact Tool value APIs; export requested CSV only.
 const wb=Workbook.create();const sheet=wb.worksheets.add('Records');
 sheet.getRangeByIndexes(0,0,objects.length+1,h.length).values=[h,...objects.map(r=>h.map(k=>String(r[k]??'')))];
 wb.recalculate();
 const matrix=sheet.getRangeByIndexes(0,0,objects.length+1,h.length).values;
 const roundtrip=matrix.slice(1).map(r=>Object.fromEntries(h.map((k,i)=>[k,String(r[i]??'')])));
 if(json(roundtrip)!==json(objects.map(r=>Object.fromEntries(h.map(k=>[k,String(r[k]??'')])))))throw Error('Artifact value roundtrip differs: '+file);
 await fs.writeFile(file,serialize(h,roundtrip),'utf8');
 return {headers:h,rows:roundtrip};
}
export function missing(raw){
 if(raw==='NOT_APPLICABLE')return 'NOT_APPLICABLE';
 if(raw==='NOT_REPORTED')return 'NOT_REPORTED';
 if(raw==='NOT_AVAILABLE')return 'NOT_AVAILABLE';
 if(raw===''||raw.startsWith('UNRESOLVED')||raw==='NOT_RETRIEVED')return 'UNRESOLVED';
 return '';
}
export function ensureWithinWorkspace(target){
 const resolved=path.resolve(target);const rel=path.relative(workspace,resolved);
 if(rel.startsWith('..')||path.isAbsolute(rel))throw Error('Write outside task workspace forbidden: '+target);
 return resolved;
}
export const inputPaths={
 evidence:'compounds/AFF-0061_Protocatechuic_Acid_Mechanism_Evidence.csv',
 dictionary:'dictionaries/Mechanism_Evidence_Field_Dictionary.csv',
 studies:'master/Study_Register.csv',
 gate2:'gate2_review/AFF-0061_Gate2_Evidence_Review_Matrix.csv',
 decisions:'governance_v0.1/Governance_Decision_Matrix_v0.1.csv',
 vocabulary:'governance_v0.1/Mechanism_Evidence_Controlled_Vocabulary_v0.1.csv',
 er:'governance_v0.1/Mechanism_Evidence_Entity_Relationship_Design_v0.1.md',
 source_report:'gate2_review/AFF-0061_Critical_Source_Verification_Report.md'
};
export async function inputs(){
 const result={};for(const [k,p]of Object.entries(inputPaths))if(p.endsWith('.csv'))result[k]=await readCSV(path.join(pilot,p));
 return result;
}
export function verifiedEligible(observation,sourceChecks,reviewEvents,proposals,kind,publications=[]){
 if(observation.dataset_role!==ROLE||observation.sandbox_review_state!=='HUMAN_APPROVED')return false;
 const approval=reviewEvents.find(e=>e.evidence_id===observation.evidence_id&&e.reviewer_type==='HUMAN_SCIENTIFIC_REVIEWER'&&e.approval_status==='HUMAN_APPROVED'&&e.signed_by&&e.signoff_reference&&e.record_version===observation.record_version&&e.decision==='APPROVE');
 if(!approval)return false;
 const publication=publications.find(p=>p.publication_id===observation.publication_id);
 if(!publication||publication.raw_retraction_status!=='NO_RETRACTION_LINK_IN_RETRIEVED_PUBMED')return false;
 const sources=sourceChecks.filter(s=>s.evidence_id===observation.evidence_id);
 if(!sources.length||sources.some(s=>s.source_issue!=='NONE_IDENTIFIED_AT_REVIEW'||!['FULL_TEXT_TEXT_LEGEND','FIGURE_IMAGE_INSPECTED','SUPPLEMENT_INSPECTED','RAW_DATA_INSPECTED'].includes(s.source_scope)||s.mapping_status!=='APPROVED_SCOPED'))return false;
 const effective=field=>proposals.find(p=>p.evidence_id===observation.evidence_id&&p.field_name===field&&p.proposal_status==='APPROVED_SCOPED'&&p.applied_to_production==='NO'&&p.approval_event_id===approval.review_event_id);
 if(kind==='direct')return effective('target_confirmation_class')?.proposed_value==='DIRECT_BINDING_SUPPORTED';
 if(kind==='antioxidant'){
  const primary=effective('antioxidant_relevance_primary')?.proposed_value;
  const secondary=effective('antioxidant_relevance_secondary');
  const mechanism=primary==='ANTIOXIDANT_FUNCTIONAL_MECHANISM'||(primary==='DIRECT_REDOX_OUTCOME'&&secondary&&JSON.parse(secondary.proposed_value_json).includes('ANTIOXIDANT_FUNCTIONAL_MECHANISM'));
  return !!mechanism&&effective('target_confirmation_class')?.proposed_value==='FUNCTIONAL_PARTICIPATION_SUPPORTED';
 }
 return true;
}
