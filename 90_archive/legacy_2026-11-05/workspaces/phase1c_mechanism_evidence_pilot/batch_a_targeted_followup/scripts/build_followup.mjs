import fs from 'node:fs/promises';
import path from 'node:path';
import {Workbook} from '@oai/artifact-tool';
import {root,pilot,csv,sha} from '../../governance_approval_v0.2/scripts/archive_approval.mjs';
const dir=path.join(pilot,'batch_a_targeted_followup');
const sourceCommit='48b34a7314b1d5914c4bb70f770e7e6d2fe939fe';
const batchPath='workspaces/phase1c_mechanism_evidence_pilot/batch_a_scientific_review/AFF0061_BatchA_Scientific_Review_Matrix.csv';
const fsSyncBytes=await fs.readFile(path.join(root,batchPath));
const batch=(await csv(path.join(root,batchPath))).rows;
const ids=batch.map(r=>r.evidence_id);
const key=n=>'ME-AFF0061-'+n;
const issues=[
['U01',key('41594941-004'),'MM_PBSA_UNIT','OPEN','正文3.6=-12.21 kJ/mol；Fig6G轴Energy(kcal/mol)，补充文件无计算更正。','Methods2.16; Results3.6; Fig6G; HDAC1 supplementary inventory','暂缓MM-PBSA定量使用、单位换算和跨研究能量比较；保留双方原报告。','作者更正/原始gmx_MMPBSA输出、绘图代码及单位说明。'],
['U02',key('41594941-004'),'STRUCTURE_IDENTITY','OPEN','相关方法仅称PDB，未恢复结构编号、版本、链、蛋白物种/构建体；补充包只有blot PDF。','Methods2.14; HDAC1 supplement inventory','不能按HUVEC物种或图中残基反推结构编号/物种。','作者PDB ID/chain/版本及结构准备文件。'],
['U03',key('41594941-004'),'METAL_LIGAND_PARAMETERS','OPEN','ff14SB/TIP3P可定位；金属保留/配位参数、配体质子化/电荷、配体拓扑未恢复。','Methods2.14-2.16','不按软件默认值、HDAC1常识或其他论文补造本模型参数。','输入topology、配体与金属参数、pH/电荷/准备记录。'],
['U04',key('41594941-004'),'MD_REPEATS_CONTROLS','PARTIALLY_RESOLVED','Fig6轴0-100ns、末20ns MM-PBSA及单体系曲线可见；each trajectory措辞不提供独立重复数。','Methods2.15-2.16; Fig6B-G','允许描述作者模拟轨迹；不声明多重复、充分收敛、强亲和或自发实验结合。','种子/独立轨迹数、apo/已知配体对照和收敛/误差分析。'],
['U05',key('37025617-001'),'ENOS_NORMALIZATION_FORMULA','OPEN','Fig4B轴p-eNOS/eNOS，D含总eNOS和GAPDH；总图注relative to GAPDH，Methods2.7无densitometry计算公式。','Frontiers Methods2.7; Fig4B/D and legend','保留作者比值读数和算法歧义，不重新除GAPDH、回算柱值或声称公式已确认。','逐样本densitometry、背景扣除/曝光/配对规则、分子分母及CTL缩放公式。'],
['U06',key('37025617-001'),'ENOS_EXPERIMENTAL_UNIT','OPEN','图注n=6-7；overnight精确小时、生物/技术重复及完整原始blot未恢复。','Methods2.4/2.7; Fig4 legend','不补成24h；不把条带列数或n直接当独立动物数。','重复单位、批次、时长和原始blot记录。'],
['U07',key('37482908-001'),'KMO_GENE_SPECIFIC_STATISTICS','OPEN','Fig4为全局谱；DataS1只含S1-S5说明。未恢复Kmo特异FC、原始p、校正p或差异结果表。','Results3.4; Fig4A/C; recovered DataS1','只能保留作者报告的候选下调；不宣称Kmo已通过FDR，不从热图或qPCR反算RNA-seq。','作者DEG表、设计/对比、软件及多重校正记录；若无则另行授权重分析。'],
['U08',key('37482908-001'),'RNA_SAMPLE_UNIT_POOLING','PARTIALLY_RESOLVED','DRA014580/PRJDB14081映射三组各1个BioSample/实验/run；未给pooling、个体数或逐动物ID。','ENA project/run report and 3 sample/experiment XML','三个存档样本不是已确认三只动物；不能据一条run推断每组生物n=1，也不能填n=8。','样本-动物-文库映射、混样方案及独立生物重复说明。'],
['U09',key('37482908-002'),'QPCR_SAMPLE_REUSE','OPEN','论文动物设计n=8，Fig5D归一化及显著阈值可见；DataS1未补该图样本n/个体ID。RNA-seq与qPCR是否同样本未知。','Methods2.2/2.5; Table1; Fig5D; DataS1; ENA metadata','同论文两检测不计为独立研究；不由图上点数确认生物n，不擅认独立验证队列。','原始Ct、样本/动物ID、技术重复数与RNA-seq样本对应表。'],
['U10',key('37482908-002'),'QPCR_P_VALUE_PRECISION','PARTIALLY_RESOLVED','Fig5D ### p<0.001和无ISO时NS已核；全局方法给ANOVA/Bonferroni，未给该比较精确p或完整统计输出。','Fig5D legend; Methods2.15','报告阈值而非精确p；不称NS等效，不把Bonferroni组间比较当RNA-seq FDR。','该图比较表、统计输出及Ct数据（如需定量复核）。'],
['U11',key('39589556-002'),'ENRICHMENT_REPRODUCIBILITY','CARRIED_FORWARD_NOT_REAUDITED','Batch A已部分恢复集合ID、30293背景/1644命中与Log(q-value)，仍缺映射/重复/版本解释。','Batch A matrix and Source_Verification; no new search','只保留集合关联，不指认NRF2蛋白或激活方向，不将术语数当独立机制数。','未来定向补统计与输入映射；本轮不扩大检索。'],
['U12',key('41594941-001')+';'+key('41594941-002'),'HUVEC_REPEAT_AND_GROUPS','PARTIALLY_RESOLVED','HDAC1补充FileS1已取得并视觉核对p2 Fig4I；未再称blot全部未取得。6组/列5组、n=3单位、vehicle及样本配对仍未解。','Batch A matrix; new FileS1 PDF p2','仅支持作者蛋白丰度读数；不据取得blot认证图像真实性或生物独立性。','组别澄清、重复单位、逐蛋白配对/归一化原始记录。'],
['U13',key('41594941-003'),'P65_LOCALIZATION_QUANTIFICATION','CARRIED_FORWARD_NOT_REAUDITED','Batch A Fig4E提供定位图；未恢复专门核/胞质比和统计。','Batch A matrix/assessment','将定位陈述限定为作者报告/图像定性支持，不称已定量证明。','后续研究者决定是否需区域规则、核/胞质定量和重复。'],
['U14',key('42170612-002'),'TAS2R16_MODEL_CONVERGENCE','CARRIED_FORWARD_NOT_REAUDITED','Batch A已记录模板/膜环境未恢复及配体中段RMSD偏移；本轮不重新检索。','Batch A matrix/assessment','保留计算预测；不得称受体激活、实验结合或充分收敛。','后续若需定量用途再补模型/轨迹/对照和独立实验。'],
['U15',ids.join(';'),'INDEPENDENT_STUDY_COUNT','OPEN','9条来自5篇论文，检测/预测、样本、run与研究是不同单位。三组run映射不解决跨检测复用。','Batch A study_id; ENA metadata','不把9行当9项独立研究，不把多终点当独立样本。','按未来分析单位逐项记录材料/样本复用，不自动去重或合并原记录。']
];
const residual=issues.map(([id,evidence,topic,status,finding,locator,boundary,next])=>({uncertainty_id:id,evidence_ids:evidence,topic,resolution_status:status,latest_finding:finding,source_locator:locator,scientific_use_boundary:boundary,needed_to_resolve:next,resolution_authority:'PROJECT_DESIGNATED_RESEARCHER_OR_SOURCE_AUTHOR',human_review_status:'NOT_REVIEWED',change_applied:'NO',reviewer_name:'',approval_date:'',followup_scope:'TARGETED_A1_A2_A3_OR_EXPLICIT_CARRY_FORWARD',date_recorded:'2026-10-26'}));
const candidates={
[key('37482908-001')]:['SOURCE_PENDING_CANDIDATE','A3','元数据映射已恢复，但Kmo特异统计与独立生物重复未明；先请求DEG表/样本设计，暂缓推断统计和正式支持计数。','仅作者报告的组学候选下调；不得宣称已通过FDR或已确认样本独立。','Kmo特异FC/p/FDR、生物重复和混样说明','保留OMICS_ASSOCIATION/OMICS_ASSOCIATED，附SOURCE_PENDING建议，不改正式状态。'],
[key('37482908-002')]:['ACCEPT_PROPOSAL_CANDIDATE','A3','可接受为待人审的Kmo/Gapdh转录响应建议；n、精确p与样本复用继续开放，不扩大接受范围。','只接受阈值及方向层级，保留无ISO时NS；不接受独立验证队列、蛋白结合或RNA-seq FDR结论。','精确效应量/样本独立计数','保留TRANSCRIPT、READOUT_ONLY；精确p不从图反算。'],
[key('39589556-002')]:['ACCEPT_PROPOSAL_CANDIDATE','CARRY_FORWARD_ONLY','接受Batch A有边界的集合关联提案作为人审候选；本轮未重核该论文。','集合富集，不赋予NRF2蛋白靶点、通路方向或直接redox。','完整富集重现及独立性计数','沿用Batch A建议及未决项，不新增科学结论。'],
[key('41594941-001')]:['ACCEPT_PROPOSAL_CANDIDATE','CARRY_FORWARD_WITH_SOURCE_AVAILABILITY_UPDATE','接受100µM/24h下HDAC1丰度读数建议作为人审候选；新取得FileS1 p2只更新来源可用性。','表达变化，不是PCA结合/必要性；未对blot真实性或重复做认证。','生物重复、vehicle及原始配对计算','原“补充原始blot未读”补为本轮已看FileS1 p2，仍需样本/归一化明细。'],
[key('41594941-002')]:['ACCEPT_PROPOSAL_CANDIDATE','CARRY_FORWARD_WITH_SOURCE_AVAILABILITY_UPDATE','接受100µM/24h下GATA4丰度读数建议作为人审候选；新取得FileS1 p2只更新来源可用性。','仅原行剂量，不把所有剂量都称显著；不借CoIP升级结合。','生物重复、vehicle及原始配对计算','更新补充来源范围；不重做其他剂量或B组因果审核。'],
[key('41594941-003')]:['REVISION_REQUIRED_CANDIDATE','CARRY_FORWARD_ONLY','需把p65核转位陈述收窄为作者报告及定性定位图支持，不能称已定量证实。','定位与结合不同；保持READOUT_ONLY，无直接redox借用。','核/胞质效应量和统计','修订文字层级；原三维类别不变，本轮未重新检索该行。'],
[key('41594941-004')]:['SOURCE_PENDING_CANDIDATE','A1','单位冲突、结构身份与金属/配体参数仍阻断可复现定量解释；取得blot附件不解决MD参数。','仅docking/MD定性预测；不得择单位或升实验结合。','MM-PBSA量值、亲和常数/跨研究比较、收敛及结构特异性','保留COMPUTATIONAL_ONLY；新增能量量值暂缓使用与结构未决字段建议。'],
[key('42170612-002')]:['REVISION_REQUIRED_CANDIDATE','CARRY_FORWARD_ONLY','沿用Batch A，修订“受体激活/稳定结合”为模拟接触及作者报告的末段相对稳定。','不把100ns或末段平台当实验结合、激活或充分收敛。','受体亲和/功能、模型特异和收敛结论','保持COMPUTATIONAL_ONLY；本轮未新核该论文或amylase。'],
[key('37025617-001')]:['REVISION_REQUIRED_CANDIDATE','A2','可保留作者报告p-eNOS/eNOS方向，但需明确完整算法未恢复；Methods2.7没有足够densitometry公式。','不在比值上自行再除GAPDH，不补算柱高，不声称公式已确认。','完整公式、精确效应量和独立重复解释','保留READOUT_ONLY及间接关联建议，新增算法未决/定量使用限制。']
};
const rows=batch.map(r=>{
 const [status,scope,reason,boundary,hold,amend]=candidates[r.evidence_id];
 const links=residual.filter(u=>u.evidence_ids.split(';').includes(r.evidence_id)).map(u=>u.uncertainty_id);
 return {evidence_id:r.evidence_id,codex_adjudication_candidate:status,human_review_status:'NOT_REVIEWED',change_applied:'NO',record_type:'CODEX_HUMAN_ADJUDICATION_PREPARATION_NOT_DECISION',followup_scope:scope,candidate_reason:reason,scientific_interpretation_boundary:boundary,quantitative_use_to_defer:hold,targeted_field_amendment_suggestion:amend,unresolved_uncertainty_ids_json:JSON.stringify(links),original_evidence_relation_type:r.original_evidence_relation_type,original_target_validation_status_legacy:r.original_target_validation_status_legacy,original_target_confirmation_class:r.original_target_confirmation_class,original_antioxidant_relevance_primary:r.original_antioxidant_relevance_primary,batch_a_evidence_relation_type:r.suggested_evidence_relation_type,suggested_evidence_relation_type:r.suggested_evidence_relation_type,batch_a_target_confirmation_class:r.suggested_target_confirmation_class,suggested_target_confirmation_class:r.suggested_target_confirmation_class,batch_a_antioxidant_relevance_primary:r.suggested_antioxidant_relevance_primary,suggested_antioxidant_relevance_primary:r.suggested_antioxidant_relevance_primary,original_record_66_fields_json:r.original_record_66_fields_json,original_record_json_sha256:r.original_record_json_sha256,batch_a_record_json:JSON.stringify(r),batch_a_record_json_sha256:sha(JSON.stringify(r)),batch_a_suggested_field_changes_json:r.suggested_field_changes_json,batch_a_source_file_sha256:r.source_file_sha256,batch_a_source_locator:r.source_locator_reviewed,source_resolution_document:'BatchA_Targeted_Source_Resolution.md',residual_register:'BatchA_Residual_Uncertainty_Register.csv',source_trace_manifest:'qc/Followup_Source_Manifest.json',study_id:r.study_id,DOI:r.DOI,PMID:r.PMID,rule_version:'Governance_v0.2',source_baseline_commit:sourceCommit,batch_a_matrix_path:batchPath,batch_a_matrix_sha256:sha(fsSyncBytes),preparation_date:'2026-10-26',preparation_agent:'Codex',human_reviewer_name:'',human_decision:'',human_approval_date:'',formal_status_change:'NO',gate1:'HOLD',gate2:'HUMAN_SCIENTIFIC_REVIEW_REQUIRED',scale_up:'NOT_AUTHORIZED',production_migration:'NOT_AUTHORIZED',release:'HOLD'};
});
async function saveCSV(name,records){
 const wb=Workbook.create();const s=wb.worksheets.add('Review');const h=Object.keys(records[0]);const values=[h,...records.map(r=>h.map(k=>r[k]))];
 s.getRangeByIndexes(0,0,values.length,h.length).values=values;wb.recalculate();
 const got=s.getRangeByIndexes(0,0,values.length,h.length).values;if(JSON.stringify(got)!==JSON.stringify(values))throw Error('Value roundtrip failed '+name);
 const esc=v=>/[",\r\n]/.test(String(v))?'"'+String(v).replaceAll('"','""')+'"':String(v);
 await fs.writeFile(path.join(dir,name),got.map(row=>row.map(esc).join(',')).join('\n')+'\n');
 const inspection=await wb.inspect({kind:'table',range:'Review!A1:D5',include:'values,formulas',tableMaxRows:5,tableMaxCols:4,maxChars:2500});
 const errors=await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NUM!|#SPILL!|#CALC!',options:{useRegex:true,maxResults:20},summary:'final literal error scan'});
 await fs.mkdir(path.join(dir,'qc/previews'),{recursive:true});
 await fs.writeFile(path.join(dir,'qc/previews',name+'.json'),JSON.stringify({inspection,errors},null,2));
 s.getRange('A:A').format.columnWidthPx=270;s.getRange('B:B').format.columnWidthPx=420;s.getRange('C:D').format.columnWidthPx=200;
 if(name.includes('Uncertainty')){s.getRange('A:A').format.columnWidthPx=140;s.getRange('B:B').format.columnWidthPx=300;s.getRange('C:D').format.columnWidthPx=290;}
 const img=await wb.render({sheetName:'Review',range:name.includes('Uncertainty')?'A1:D6':'A1:D10',scale:1,format:'png'});
 await fs.writeFile(path.join(dir,'qc/previews',name+'.png'),new Uint8Array(await img.arrayBuffer()));
}
await saveCSV('BatchA_Human_Adjudication_Preparation.csv',rows);
await saveCSV('BatchA_Residual_Uncertainty_Register.csv',residual);
const sourceEntries=[];
for(const name of ['Targeted_Access_Log.json','Metadata_and_Alternative_Access_Log.json','Kmo_Final_Access_Log.json']){
 const log=JSON.parse(await fs.readFile(path.join(dir,'qc',name),'utf8'));for(const e of log.entries)if(e.local_path)sourceEntries.push({...e,role:e.name==='DRA014580_DDBJ.html'?'DDBJ_APPLICATION_SHELL_NOT_RECORD_METADATA':e.usable_response?'RECOVERED_SOURCE_CONTENT_OR_METADATA':'FAILED_RESPONSE_NOT_SOURCE_EVIDENCE',raw_distribution:'LOCAL_ONLY_EXCLUDED'});
}
for(const p of ['local_sources/HDAC1_supplement_member_0.pdf','local_sources/Kmo_DataS1_recovered.doc','local_sources/Kmo_DataS1_readonly_text.txt'])sourceEntries.push({local_path:p,sha256:sha(await fs.readFile(path.join(dir,p))),role:p.endsWith('.pdf')?'EXTRACTED_SUPPLEMENT_INVENTORY_AND_P2_VISUAL_CHECK':p.endsWith('.doc')?'EXTRACTED_DATAS1_READ_ONLY_WORD':'READ_ONLY_WORD_TEXT_EXTRACTION_NOT_GENE_TABLE',raw_distribution:'LOCAL_ONLY_EXCLUDED'});
const previous=['search_logs/raw/PMC12837532.xml','search_logs/raw/PMC10070727.xml','search_logs/raw/PMC10424289.xml','batch_a_scientific_review/local_sources/PMC12837532_biology-15-00206-g006.jpg','batch_a_scientific_review/local_sources/PMC10070727_fnut-10-1060226-g004.jpg','batch_a_scientific_review/local_sources/PMC10424289_JCMM-27-2290-g002.jpg','batch_a_scientific_review/local_sources/PMC10424289_JCMM-27-2290-g001.jpg'];
for(const p of previous)sourceEntries.push({project_relative_path:'workspaces/phase1c_mechanism_evidence_pilot/'+p,sha256:sha(await fs.readFile(path.join(pilot,p))),role:'PREVIOUS_SOURCE_RECHECKED_FOR_TARGETED_QUESTIONS',raw_distribution:'LOCAL_ONLY_EXCLUDED'});
await fs.writeFile(path.join(dir,'qc/Followup_Source_Manifest.json'),JSON.stringify({date:'2026-10-26',source_baseline_commit:sourceCommit,sources:sourceEntries,raw_sequence_downloaded:false,rna_seq_reanalysis_performed:false,scope_note:'Only A1/A2/A3 newly investigated; other A observations explicitly carried forward'},null,2)+'\n');
console.log(JSON.stringify({adjudication_rows:rows.length,residual_issues:residual.length,candidate_counts:Object.fromEntries(['ACCEPT_PROPOSAL_CANDIDATE','REVISION_REQUIRED_CANDIDATE','SOURCE_PENDING_CANDIDATE'].map(k=>[k,rows.filter(r=>r.codex_adjudication_candidate===k).length]))}));
