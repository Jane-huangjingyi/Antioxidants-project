/** Optional review export. CSV files remain the authoritative research tables. */
import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {Workbook,SpreadsheetFile} from '@oai/artifact-tool';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../..');
const wb=Workbook.create();
const specs=[
 ['Capacity evidence','03_candidate_selection/01_activity_model/results/Capacity_Analysis_Entry.csv',null],
 ['Source-local order','03_candidate_selection/01_activity_model/results/Within_Source_Descriptive_Order.csv',null],
 ['Legacy source review','03_candidate_selection/01_activity_model/results/Legacy30_Verification.csv',null],
 ['Protocol constraints','03_candidate_selection/01_activity_model/results/Bridge_Protocol_Matrix.csv',null],
 ['Review panel','03_candidate_selection/results/top20_review_queue.csv',['review_slot','candidate_id','compound_name','molecular_formula','confirmed_independent_horac_studies','confirmed_horac_source_dois','food_occurrence_status','current_absorbance_compatibility','shortlist_status']],
 ['Candidate profiles','02_identity_and_evidence/results/candidate_evidence_profiles.csv',null],
 ['Capacity model inputs','03_candidate_selection/01_activity_model/results/Model_Input_Candidates.csv',['candidate_id','compound','doi','molar_mean_candidate','molar_SD_candidate','reported_plus_minus','reported_error_scale','error_type','independent_experiments_as_reported','variance_of_mean_candidate','variance_assumptions','vehicle','source_form','model_status','human_review_status']],
 ['Endpoint definitions','04_absorbance_assay/01_endpoint_definition/results/Endpoint_Method_Comparison.csv',null],
 ['Chemical observations','02_identity_and_evidence/results/chemical_observation_index.csv',null],
 ['Methods','04_absorbance_assay/results/method_comparison.csv',null],
 ['Manuscript claims','06_manuscript/tables/Manuscript_Claim_Map.csv',null],
 ['Researcher decisions','03_candidate_selection/config/researcher_decisions.csv',null],
 ['Source directory','02_identity_and_evidence/results/source_file_index.csv',null],
 ['Source documents','02_identity_and_evidence/results/source_document_index.csv',null],
 ['Mechanism observations','02_identity_and_evidence/inputs/mechanism_evidence/master/Compound_Mechanism_Evidence_Master.csv',['evidence_id','candidate_id','compound_name','DOI','target_protein','evidence_relation_type','target_validation_status','experimental_model','source_verification_status','human_review_status']]
];
const previewDir=path.join(root,'07_quality_control/previews');await fs.mkdir(previewDir,{recursive:true});
const counts=[];
for(const [name,rel,fields] of specs){
 const parsed=await Workbook.fromCSV((await fs.readFile(path.join(root,rel),'utf8')).replace(/^\uFEFF/,''),{sheetName:'Import'});
 let rows=parsed.worksheets.getItemAt(0).getUsedRange().values;
 if(fields){const ix=fields.map(f=>{const i=rows[0].indexOf(f);if(i<0)throw Error(`Missing ${f}`);return i});rows=rows.map(r=>ix.map(i=>r[i]??''));}
 const header=rows[0];
 for(let c=0;c<header.length;c++)if(/^(review_slot|confirmed_independent_horac_studies|unresolved_horac_source_count|typed_sd_record_count|record_count|year|molecular_weight_g_mol|molar_mean_candidate|molar_SD_candidate|reported_plus_minus|variance_of_mean_candidate|independent_experiments_as_reported)$/.test(header[c]))for(let r=1;r<rows.length;r++)if(rows[r][c]!==''&&rows[r][c]!==null&&Number.isFinite(Number(rows[r][c])))rows[r][c]=Number(rows[r][c]);
 const sheet=wb.worksheets.add(name);sheet.showGridLines=false;sheet.tabColor=name==='Researcher decisions'?'#C79332':'#315E78';
 const grid=sheet.getRangeByIndexes(0,0,rows.length,header.length);grid.values=rows;
 grid.format.font.name='Arial';grid.format.font.size=10;grid.format.columnWidth=27;grid.format.rowHeight=38;grid.format.verticalAlignment='center';grid.format.wrapText=true;
 if(['Source directory','Source documents','Manuscript claims','Mechanism observations','Capacity model inputs','Endpoint definitions','Capacity evidence','Source-local order','Legacy source review','Protocol constraints'].includes(name))grid.format.rowHeight=82;
 const band=sheet.getRangeByIndexes(0,0,1,header.length);band.format.fill='#24465C';band.format.font.color='#FFFFFF';band.format.font.bold=true;band.format.rowHeight=58;
 sheet.tables.add(grid,true,`ReviewData${counts.length+1}`);sheet.freezePanes.freezeRows(1);sheet.freezePanes.freezeColumns(2);
 if(name==='Researcher decisions'&&rows.length>1)sheet.getRangeByIndexes(1,1,rows.length-1,header.length-1).format.fill='#FFF3D6';
 for(let c=0;c<header.length;c++){
  const col=sheet.getRangeByIndexes(0,c,rows.length,1);
  if(/doi|source|locator|reason|path|field_names/.test(header[c]))col.format.columnWidth=55;
  if(/molecular_formula|candidate_id|review_slot/.test(header[c]))col.format.columnWidth=19;
 }
 // Bound every preview to the identifiers and first few fields.
 const image=await wb.render({sheetName:name,range:'A1:D5',scale:1,format:'png'});
 await fs.writeFile(path.join(previewDir,`${name.replaceAll(' ','_')}.png`),new Uint8Array(await image.arrayBuffer()));
 counts.push({sheet:name,records:rows.length-1,columns:header.length,source:rel});
}
const notes=wb.worksheets.add('ReadMe');
notes.getRange('A1:B7').values=[['Topic','Interpretation'],['Scope','Individually defined food or dietary chemicals.'],['Panel','20 review slots, not a final laboratory-ready Top20; inspect all cutoff ties.'],['Evidence','Capacity model inputs contain targeted source rechecks; D1-D5 fields retain dated framework snapshots. Neither upgrades human review. Repeated records are not independent studies.'],['Edits','Enter decisions in 03_candidate_selection/config/researcher_decisions.csv and rerun the pipeline; this workbook is a generated snapshot.'],['Journal metrics','No current JCR or impact factor has been independently verified in this export. Journal metrics are not study evidence strength.'],['Reproduce','python run_pipeline.py --tables-only; optional --workbook after configuring Node dependencies.']];
notes.getRange('A1:B7').format.columnWidth=65;notes.getRange('A1:B7').format.rowHeight=55;notes.getRange('A1:B7').format.wrapText=true;notes.getRange('A1:B7').format.verticalAlignment='center';notes.getRange('A1:B7').format.font.name='Arial';notes.getRange('A1:B7').format.font.size=10;notes.showGridLines=false;
notes.getRange('A1:B1').format.fill='#24465C';notes.getRange('A1:B1').format.font.color='#FFFFFF';
const image=await wb.render({sheetName:'ReadMe',range:'A1:B7',scale:1,format:'png'});await fs.writeFile(path.join(previewDir,'ReadMe.png'),new Uint8Array(await image.arrayBuffer()));
await wb.recalculate();
const inspection=await wb.inspect({kind:'sheet',include:'id,name',maxChars:2500});
const out=path.join(root,'06_manuscript/tables/Candidate_Review_Workbook.xlsx');
await(await SpreadsheetFile.exportXlsx(wb)).save(out);
await fs.rm(`${out}.inspect.ndjson`,{force:true});
await fs.writeFile(path.join(root,'07_quality_control/workbook_export_qc.json'),JSON.stringify({status:'EXPORTED',tabs:counts,inspection:inspection.ndjson,formulas:'NONE_STATIC_SOURCE_LINKED_SNAPSHOT'},null,2)+'\n');
console.log(`Exported ${out}; ${counts.length+1} worksheets.`);
