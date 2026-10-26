import fs from 'node:fs/promises';
import path from 'node:path';
import assert from 'node:assert/strict';
import {csv,P,dir,root,sha,Workbook,git} from './track_b_lib.mjs';
const baseline=JSON.parse(await fs.readFile(path.join(dir,'qc/Start_Baseline.json'),'utf8'));
for(const item of [...baseline.tracked,...baseline.local_source_cache])assert.equal(sha(await fs.readFile(path.resolve(root,item.path))),item.sha256,item.path);
const frozen=(await csv(P.freeze_manifest)).rows;for(const item of frozen)assert.equal(sha(await fs.readFile(path.join(root,item.asset_path))),item.sha256,item.asset_path);
const tri=(await csv(path.relative(root,path.join(dir,'Candidate_Multidimensional_Triage_v0.1.csv')))).rows;
const feas=(await csv(path.relative(root,path.join(dir,'Robot_Screening_Feasibility_and_Interference_Matrix.csv')))).rows;
assert.equal(tri.length,191);assert.equal(feas.length,191);assert.equal(new Set(tri.map(r=>r.candidate_id)).size,191);assert.deepEqual(tri.map(r=>r.candidate_id),feas.map(r=>r.candidate_id));
assert.equal(tri.filter(r=>r.framework157_scope==='YES').length,157);assert.equal(tri.filter(r=>r.frozen_top20_reference_rank).length,20);
const orig=new Map((await csv(P.universe)).rows.map(r=>[r.candidate_id,r]));const fr=new Map((await csv(P.frozen)).rows.map(r=>[r.candidate_id,r]));
for(const r of tri){assert.deepEqual(JSON.parse(r.original_universe_row_json),orig.get(r.candidate_id));assert.deepEqual(JSON.parse(r.frozen_reference_row_json),fr.get(r.candidate_id)||{});assert.equal(r.human_review_status,'NOT_REVIEWED');assert.equal(r.change_applied,'NO');if(r.framework157_scope==='NO')for(const k of ['D1','D2','D3','D4','D5'])assert.equal(r[k+'_snapshot_status'],'');}
for(const r of feas){assert.equal(r.human_review_status,'NOT_REVIEWED');assert.equal(r.change_applied,'NO');for(const k of ['approved_stock_concentration','approved_final_concentration_range','approved_final_vehicle_fraction','approved_plate_format'])assert.equal(r[k],'');}
const summary=JSON.parse(await fs.readFile(path.join(dir,'qc/Build_Summary.json'),'utf8'));
assert.equal(summary.counts['需要补证后再评估'],133);assert.equal(summary.counts['暂缓进入首批实验'],58);assert.equal(summary.future_year_flags.length,7);
const checked=new Map((await csv(P.eligibility)).rows.map(r=>[r.candidate_id,r]));for(const id of summary.panel6)assert(Number(checked.get(id).confirmed_independent_study_N)>=2);
await fs.mkdir(path.join(dir,'qc/previews'),{recursive:true});
for(const [label,rows,keys] of [['triage',tri,['candidate_id','candidate_name','framework157_scope','frozen_top20_reference_rank','preparation_tier']],['feasibility',feas,['candidate_id','candidate_name','current_supplier_lot_COA','current_stock_solubility_and_stability']]]){
 const wb=Workbook.create();const s=wb.worksheets.add('Preview');const matrix=[keys,...rows.slice(0,8).map(r=>keys.map(k=>r[k]))];s.getRangeByIndexes(0,0,matrix.length,keys.length).values=matrix;s.getUsedRange().format.columnWidth=28;s.getUsedRange().format.rowHeight=38;s.getUsedRange().format.wrapText=true;wb.recalculate();assert.deepEqual(s.getUsedRange().values,matrix);const img=await wb.render({sheetName:'Preview',autoCrop:'all',scale:1,format:'png'});await fs.writeFile(path.join(dir,'qc/previews',label+'.png'),new Uint8Array(await img.arrayBuffer()));
}
const report=`# Track B QC报告\n\n日期2026-10-26；结果PASS。建议状态NOT_REVIEWED，change_applied=NO。\n\n两张CSV各191行、ID唯一且集合一致；157种带ID快照集合一致且属于191全集，34种范围外不填五维原快照状态。785条五维映射保留。冻结20行整行与值保持原样，10项冻结资产SHA256均匹配历史冻结清单。P6六种均有既有6D至少2篇确认来源；本轮没有声称重新全文核查这些论文。133种补证、58种情景暂缓、0种就绪；7条未来年份已标记。\n\n全部${baseline.tracked.length}个原有Git跟踪文件及${baseline.local_source_cache.length}个原有来源缓存SHA256未变。21条AFF-0061观察、治理批准规则、257项历史提案及既有来源HOLD不受本目录新增材料影响；无迁移、排名更新或实验执行。两张CSV均由artifact-tool构建并逐字段回读相等；已生成有界预览供视觉检查，预览不涵盖全部宽列，全部列以程序回读验证。批准参数保持空白、当前采购与干扰测试保持未核实。\n\n输入/输出哈希及覆盖计数见qc/Build_Summary.json，起始784文件与76缓存基线见qc/Start_Baseline.json。复现顺序为node scripts/build_track_b.mjs，再node scripts/verify_track_b.mjs（在本目录执行，需已安装的artifact-tool）。capture_baseline.mjs只用于本轮开始时捕获，不可覆盖重建起始证据。预览与node_modules为忽略项，不提交；没有生成额外XLSX。\n\n限制：库存/设备未确认；D5主要未检索；191与无ID的Aqueous157表未做模糊名称实体合并，157覆盖界定依赖带ID三表。未逐篇更新原始来源与采购信息。正式浓度、板型、QC阈值和实验面板均待研究者裁决。\n\nGit交付基于${baseline.source_commit}，本任务仅新增本目录文件，独立分支不自动合并main。最终commit SHA及push状态由交付消息提供，避免提交内记录自身SHA的循环。\n`;
await fs.writeFile(path.join(dir,'TrackB_QC_Report.md'),report);console.log(JSON.stringify({result:'PASS',protected_tracked:baseline.tracked.length,protected_source_cache:baseline.local_source_cache.length,frozen_assets:frozen.length,branch:git('branch','--show-current')},null,2));


