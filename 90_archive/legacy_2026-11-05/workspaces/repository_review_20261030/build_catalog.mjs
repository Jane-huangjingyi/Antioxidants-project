import fs from 'node:fs/promises';
import path from 'node:path';
import assert from 'node:assert/strict';
import {fileURLToPath} from 'node:url';
import {Workbook,SpreadsheetFile} from '@oai/artifact-tool';
const dir=path.dirname(fileURLToPath(import.meta.url)),root=path.resolve(dir,'../..');
const input=JSON.parse(await fs.readFile(path.join(dir,'Catalog_Input.json'),'utf8'));
const actions=JSON.parse(await fs.readFile(path.join(dir,'File_Actions.json'),'utf8'));
const metrics=JSON.parse(await fs.readFile(path.join(dir,'Verified_Journal_Metrics.json'),'utf8'));
const moved=new Map(actions.filter(r=>r.action!=='PRESERVE_BEFORE_REBUILD_REVIEW_ENTRY').map(r=>[r.old_path,r.new_path]));
for(const r of input.tables){r['当前来源表']=moved.get(r['来源表'])||r['来源表'];r['源文件完整路径']=path.join(root,r['当前来源表']);}
for(const r of input.evidence){r['源文件完整路径']=path.join(root,r['来源表']);if(r['本地原文']){const p=path.join(root,'workspaces/phase1c_mechanism_evidence_pilot',r['本地原文']);try{await fs.access(p);r['本地原文']=p;r['缓存实存状态']='EXISTS_NOT_REVERIFIED_THIS_ROUND';}catch{r['缓存实存状态']='NOT_FOUND_AT_RECORDED_PATH';}}else r['缓存实存状态']='NOT_RECORDED';}
const journalRows=[];
for(const r of input.journals){const m=metrics.find(m=>m.journal===r['期刊原始名称']);if(m){for(const [cat,q]of m.categories)journalRows.push({...r,'最新JIF':m.jif,'JCR学科类别':cat,'JCR分区':q,'出版商汇总JIF分区_非逐类别':m.publisher_quartile||'','期刊指标核实状态':m.status,'指标证据链接或导出表路径':m.url,'人工核实备注':m.note});}else journalRows.push({...r,'出版商汇总JIF分区_非逐类别':'','人工核实备注':r['人工核实备注']+(r['期刊原始名称']==='unresolved'?'；先核定期刊身份':'')});}
const affected=new Set(input.conflicts.flatMap(r=>[r[1],r[2]]));const observed=new Set(input.evidence.map(r=>r['文献ID']));
for(const r of input.papers){r['建议文章章节']=observed.has(r['文献ID'])?'结果：见具体证据表（仍需逐论点裁决）':'引言/研究成熟度：仅题录候选；不能直接支持实验结论';r['文章论点支持强度']=observed.has(r['文献ID'])?'见具体观察原等级；未形成文章级批准结论':'未核实全文，不评级';r['标识符冲突状态']=affected.has(r['文献ID'])?'DOI_PMID_CONFLICT_DO_NOT_MERGE':'未发现本轮显式映射冲突；不等于身份已核实';}
input.papers.sort((a,b)=>Number(observed.has(b['文献ID']))-Number(observed.has(a['文献ID']))||a['文献ID'].localeCompare(b['文献ID']));
const wb=Workbook.create();const details=[];
function table(name,rows){assert(rows.length);const h=Object.keys(rows[0]);for(const r of rows)for(const k of Object.keys(r))if(!h.includes(k))h.push(k);const s=wb.worksheets.add(name);const matrix=[h,...rows.map(r=>h.map(k=>r[k]??''))];s.getRangeByIndexes(0,0,matrix.length,h.length).values=matrix;assert.deepEqual(s.getUsedRange().values,matrix);s.showGridLines=false;s.getUsedRange().format.font={name:'Arial',size:10};s.getUsedRange().format.rowHeight=32;s.getUsedRange().format.columnWidth=28;s.getUsedRange().format.wrapText=true;s.getRangeByIndexes(0,0,1,h.length).format={fill:'#24445C',font:{name:'Arial',size:10,bold:true,color:'#FFFFFF'},rowHeight:44,wrapText:true};s.freezePanes.freezeRows(1);s.freezePanes.freezeColumns(1);const t=s.tables.add(s.getUsedRange(),true,'CatalogTable'+details.length);t.showFilterButton=true;s.getUsedRange().format.verticalAlignment='center';s.getUsedRange().format.rowHeight=52;h.forEach((k,j)=>{if(/ID|DOI|PMID/.test(k))s.getRangeByIndexes(0,j,matrix.length,1).format.columnWidth=46;if(/题名|来源表|链接|说明|备注|理由|边界/.test(k))s.getRangeByIndexes(0,j,matrix.length,1).format.columnWidth=72;});s.getRangeByIndexes(0,0,1,h.length).format.horizontalAlignment='center';details.push({sheet:name,records:rows.length,columns:h.length});console.log('Built '+name+': '+rows.length);return s;}
const overview=[['证据核查目录','2026-10-30'],['用途','先查具体观察，再沿文献ID定位题录、来源表、原文及审核记录。'],['具体观察记录',input.evidence.length],['文献登记项（不是已验证独立研究数）',input.papers.length],['候选物—文献元数据关联',input.association.length],['筛选状态记录',input.screening.length],['来源表目录',input.tables.length],['标识符冲突行',input.conflicts.length],['期刊原始题名数',input.journals.length],['出版商可核实2025JIF的题名数',metrics.length],['最新JIF含义','2026年发布的2025年JIF；不是2026数据年IF。'],['缺失','期刊名、JIF、JCR类别或分区未核实则留空并保留状态，不填0。'],['证据强度','原等级按原表原文保留；不同构念等级不直接合并。文章级强度与章节是待人工审查建议。'],['历史版本','来源表目录包含历史/检查点/演练；不将历史快照当新增独立研究。'],['独立性','DOI去重不等于独立研究；无ID条目不按标题模糊合并。'],['机制','AFF0061所有原观察保持NOT_REVIEWED，本目录不批准科学状态。'],['期刊来源','出版商公告可作为线索；尚无机构JCR逐刊逐学科导出，未核实项不能用于正式投稿说明。'],['输入与追溯','来源数据记录号从1起（不含表头）；CSV多行单元格使记录号不等于文本行号。'],['更新方法','编辑人工裁决前先另存审核副本；本目录由源数据重建，不能反向修改原始科学表。']];
const cover=wb.worksheets.add('使用说明');cover.getRangeByIndexes(1,0,overview.length,2).values=overview;cover.showGridLines=false;cover.getUsedRange().format.font={name:'Arial',size:11};cover.getRange('A2:A20').format.columnWidth=42;cover.getRange('B2:B20').format.columnWidth=100;cover.getUsedRange().format.wrapText=true;cover.getUsedRange().format.rowHeight=36;cover.getRange('A2:B2').format.font={name:'Arial',bold:true,size:15};
table('具体证据',input.evidence);table('期刊指标',journalRows);table('最新审核线索',input.audits);
table('文献登记',input.papers);table('候选物文献关联',input.association);table('筛选记录',input.screening);table('来源表目录',input.tables);
table('标识符冲突',input.conflicts.map(r=>({'PMID':r[0],'既有DOI键':r[1],'冲突DOI键':r[2],'来源表':r[3],'来源数据记录号':r[4],'处置':'待原始文献核实；不自动合并，不计新证据'})));
wb.recalculate();const inspect=await wb.inspect({kind:'table',range:'具体证据!A1:F4',include:'values,formulas',tableMaxRows:4,tableMaxCols:6,maxChars:1800});await fs.writeFile(path.join(dir,'Workbook_Inspection.json'),inspect.ndjson);
const err=await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#NUM!',options:{useRegex:true,maxResults:10},maxChars:1500});await fs.writeFile(path.join(dir,'Workbook_Error_Scan.json'),err.ndjson);
await fs.mkdir(path.join(dir,'previews'),{recursive:true});
for(const name of ['使用说明',...details.map(r=>r.sheet)]){const blob=await wb.render({sheetName:name,range:name==='使用说明'?'A2:B8':'A1:D5',scale:1,format:'png'});await fs.writeFile(path.join(dir,'previews',name+'.png'),new Uint8Array(await blob.arrayBuffer()));}
const output=path.join(root,'outputs/review_20261030/Evidence_Catalog_2026-10-30.xlsx');await fs.mkdir(path.dirname(output),{recursive:true});await(await SpreadsheetFile.exportXlsx(wb)).save(output);
// Automatic full-cell inspection is a large temporary serialization, not a scientific process asset.
await fs.rm(output+'.inspect.ndjson',{force:true});
await fs.writeFile(path.join(dir,'Workbook_QC.json'),JSON.stringify({details,journal_metric_titles_verified:metrics.length,rows_preserved:true,output},null,2));console.log('Exported '+output);
