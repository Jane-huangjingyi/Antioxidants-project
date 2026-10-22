import fs from 'node:fs/promises';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
import {workspace,ROLE,readCSV,serialize,sha,ensureWithinWorkspace} from './migration_lib.mjs';

export async function reconstruct(){
 const values=await readCSV(path.join(workspace,'dryrun/Legacy_Field_Value.csv'));
 const observation=await readCSV(path.join(workspace,'dryrun/Observation.csv'));
 const mapping=await readCSV(path.join(workspace,'schema/Schema_Field_Mapping_v0.2.csv'));
 const headers=mapping.rows.slice().sort((a,b)=>Number(a.field_order)-Number(b.field_order)).map(r=>r.legacy_field);
 const ordered=observation.rows.slice().sort((a,b)=>Number(a.legacy_row_order)-Number(b.legacy_row_order));
 const rows=ordered.map(o=>Object.fromEntries(headers.map(field=>{
  const cells=values.rows.filter(v=>v.evidence_id===o.evidence_id&&v.field_name===field);
  if(cells.length!==1)throw Error('Missing or duplicated legacy cell '+o.evidence_id+'/'+field);
  return [field,cells[0].raw_value];
 })));
 const snapshot=JSON.parse(await fs.readFile(path.join(workspace,'qc/Input_Snapshot.json'),'utf8'));
 const original=snapshot.files.find(f=>f.key==='evidence');
 const originalBytes=Buffer.from(original.bytes_base64,'base64');
 if(sha(originalBytes)!==original.sha256)throw Error('Original byte snapshot failed integrity check');
 return {dataset_role:ROLE,method:'EAV_CELL_RECONSTRUCTION_PLUS_BYTE_EXACT_SOURCE_SNAPSHOT',headers,rows,canonical_csv_text:serialize(headers,rows),original_source_bytes_base64:original.bytes_base64,original_source_sha256:original.sha256,production_write:'FORBIDDEN'};
}
if(process.argv[1]&&import.meta.url===pathToFileURL(path.resolve(process.argv[1])).href){
 const result=await reconstruct();const target=ensureWithinWorkspace(path.join(workspace,'qc/Rollback_Reconstruction.json'));
 await fs.writeFile(target,JSON.stringify(result,null,2)+'\n');
 console.log(JSON.stringify({reconstructed_rows:result.rows.length,fields:result.headers.length,production_write:'NONE',target}));
}
