import fs from 'node:fs/promises';
import path from 'node:path';
import {Workbook} from '@oai/artifact-tool';
import {root,pilot,csv,sha} from '../../governance_approval_v0.2/scripts/archive_approval.mjs';
export const dir=path.join(pilot,'batch_a_scientific_review');
export const ids=['ME-AFF0061-37482908-001','ME-AFF0061-37482908-002','ME-AFF0061-39589556-002','ME-AFF0061-41594941-001','ME-AFF0061-41594941-002','ME-AFF0061-41594941-003','ME-AFF0061-41594941-004','ME-AFF0061-42170612-002','ME-AFF0061-37025617-001'];
// Authored findings are recommendations from the specified source sections/images,
// never changes to original records or to the historical 257-proposal rehearsal.
const findings=[
{id:ids[0],relation:'OMICS_ASSOCIATION',target:'OMICS_ASSOCIATED',redox:'OTHER_BIOLOGICAL_FUNCTION',level:'TRANSCRIPTOME',
 identity:'作者报告PCA，Sigma 37580、批次BCCF0948；参考母体酸映射不是本次样品独立化学鉴定。',
 model:'7周龄雄性C57BL/6NTac小鼠全心室组织；不是后续大鼠心肌细胞实验。',
 exposure:'PCA 100 mg/kg body weight/day，每日肌内注射；ISO第6日起连续9天；ISO泵入80 mg/kg/day共14天。组织采样精确时刻和RNA-seq生物重复数未从已读材料确认。',
 comparison:'RNA-seq三组：sham+DMSO、ISO+DMSO、ISO+PCA；本行主要比较ISO+PCA vs ISO+DMSO。动物方法每组n=8不直接作为RNA-seq n。',
 object:'小鼠Kmo转录本；Q91WN4仅既有参考映射，未重做UniProt或样品蛋白鉴定。',
 actual:'Results3.4列Kmo为ISO升高、PCA降低的10个候选之一；Fig4A/C为全局组学图，不能单凭图定位Kmo独立效应量。',
 negative:'Fig4含上调、下调和未入阈值基因；不能将其解释为全基因下调。Kmo特异效应量/校正p尚未恢复。',
 locator:'Methods2.1/2.2/2.11; Results3.4; Fig4A/C; DDBJ DRA014580指针（未下载原始数据）',
 scope:'本地XML相关方法、结果、图注＋本轮PMC HTML及Fig4原图；未读取原始测序数据、补充TIFF/DataS1。',
 independence:'与同文qPCR共享研究背景；样本是否相同/独立队列未确认；不得计为第二项独立研究。',
 rationale:'高通量转录变化支持组学关联，不是蛋白实测、功能必要性或结合；不借用Fig8 DHE升级本行红氧类别。',
 issues:'Kmo独立log2FC/校正p及样本单位未核；图4图例使用raw p，正文仅给FC>2及显著p，未建立多重校正。',
 decision:'研究者决定是否在缺Kmo特异统计时暂保留OMICS_ASSOCIATED，或在分析纳入前补DRA014580/作者DEG表；不得声称已通过FDR。',
 amendments:{source_locator:'Methods2.1/2.2/2.11; Results3.4; Fig4A/C; Kmo-specific table/raw data unresolved',source_review_mode:'RELATED_TEXT_AND_FIGURE4_VISUALLY_CHECKED_NOT_RAW_DATA_AUDIT',readout_level:'TRANSCRIPTOME',statistical_correction_status:'UNRESOLVED_KMO_SPECIFIC_ADJUSTED_P_NOT_RECOVERED'}},
{id:ids[1],relation:'PATHWAY_MODULATION',target:'READOUT_ONLY',redox:'OTHER_BIOLOGICAL_FUNCTION',level:'TRANSCRIPT',
 identity:'同文Sigma PCA 37580、批次BCCF0948；不代表独立样品身份验证。',model:'相同ISO小鼠全心室组织背景；Fig5D为小鼠Kmo mRNA，不是Kmo蛋白量或酶活。',
 exposure:'100 mg/kg/day肌内给药，ISO第6日起9天；ISO80 mg/kg/day泵入14天。',comparison:'Fig5D四臂sham+DMSO、sham+PCA、ISO+DMSO、ISO+PCA；主要比较后两臂；mRNA/Gapdh，以sham背景为参照。',
 object:'Mus musculus Kmo转录本；方法2.5给2^(-ΔΔCt)，Table1列mouse Kmo及Gapdh引物。',actual:'Fig5D显示ISO提高Kmo/Gapdh、PCA在ISO下使其下降；图注### p<0.001。不从柱图估算fold change或逐点n。',
 negative:'Fig5D在无ISO时PCA与vehicle标NS；这不是等效或零效应，也不证明挑战特异交互。',locator:'Methods2.2/2.5; Table1 mouse Kmo/Gapdh; Results3.4; Fig5D',scope:'相关正文、引物表及Fig5D原图已读；未重新分析Ct或取得逐样本数据；补充S1-S5/DataS1未读。',
 independence:'与37482908-001为同一论文的正交检测层级，但不证明独立动物队列；同一研究只计一次。',rationale:'qPCR转录响应可用PATHWAY_MODULATION兼容容器＋TRANSCRIPT读数，不升级蛋白确认或结合；平行siRNA不自动赋予本行因果。',
 issues:'qPCR与RNA-seq样本复用、逐样本n、Gapdh稳定性及原始Ct未核；不能把动物每组n=8无条件填作本图n。',decision:'裁决转录响应兼容标签及需要的重复单位说明；保留NS。',amendments:{source_review_mode:'RELATED_TEXT_TABLE1_AND_FIGURE5D_VISUALLY_CHECKED',readout_level:'TRANSCRIPT',normalization:'Kmo mRNA/Gapdh; 2^(-DeltaDeltaCt)',negative_or_null_result:'No-ISO PCA vs vehicle marked NS; not equivalence'}},
{id:ids[2],relation:'OMICS_ASSOCIATION',target:'NOT_APPLICABLE_NO_PROTEIN_TARGET',redox:'INDIRECT_OXIDATIVE_STRESS_ASSOCIATION',level:'GENE_SET_ENRICHMENT',
 identity:'PCA购自MCE HY-N0294；本行PCA不是同文脂毒挑战palmitic acid（PA）。未独立测定细胞内母体浓度。',model:'人肝癌来源MHCC97-H细胞，常规培养；本RNA-seq比较未报告加入PA/erastin/sorafenib或NRF2敲除。',
 exposure:'名义培养处理5 µM、16 h；不推定细胞内游离暴露、stock或人体可达性。',comparison:'PCA处理 vs 未处理Ctrl；不是脂毒模型下PCA rescue。RNA-seq生物重复与完整基因级统计流程仍未确认。',
 object:'氧水平/氧化应激富集集合，无特定蛋白靶点；Fig2D并非全为GO，还包含Reactome Biological oxidations等。',
 actual:'Fig2D及补充Table5：GO:0070482、GO:0006979、GO:2000377等可定位；补表列#TotalGeneInLibrary=30293、#GeneInHitList=1644及Log(q-value)，图2A显示padj标签。',
 negative:'富集集合含ROS生成、代谢及负调控术语，不能统一解释为抗氧化激活；补表非所有术语均可无条件视为通过某预设FDR。',
 locator:'Methods RNA sequencing/Cell culture; Results RNA-seq段; Fig2A/D; Supplementary Table5 PDF p14/p17（p14-p37为表范围）',
 scope:'本地XML＋本轮HTML及Fig2原图；49页补充PDF做页级文本检索，视觉核对p14/p17；未逐页审核其余页或重做富集。',
 independence:'同文多种细胞/动物观察不等于独立研究；本行基因集输出彼此重叠，不把术语数量当独立机制数。',
 rationale:'组学富集而非NRF2蛋白结合或ROS实测；可补已恢复的术语与背景计数，但方向仍不赋值。',
 issues:'旧待补项“术语ID/背景/校正值”已有部分恢复；仍缺完整输入基因映射、测试背景选择、RNA-seq重复及算法版本。612+1188差异基因与1644命中数之差不能擅自解释。',
 decision:'研究者决定将多词表集合保留一行还是未来另建集合关联；本轮不新增正式观察或以NRF2命名本行蛋白。',
 amendments:{pathway_database:'MIXED_AUTHOR_ENRICHMENT_COLLECTIONS_GO_REACTOME_WIKIPATHWAYS_NOT_SINGLE_PROTEIN',pathway_ID:'MULTIPLE_SETS; GO:0070482; GO:0006979; GO:2000377; R-HSA-211859 (non-exhaustive)',source_locator:'Methods RNA sequencing; Fig2D; Supplementary Table5 PDF p14/p17',enrichment_background_reported:'TotalGeneInLibrary=30293; GeneInHitList=1644; rationale/version unresolved',enrichment_direction:'NOT_ASSIGNED',readout_level:'GENE_SET_ENRICHMENT'}},
...['HDAC1','GATA4','RELA'].map((protein,i)=>({id:ids[3+i],relation:'PATHWAY_MODULATION',target:'READOUT_ONLY',redox:'OTHER_BIOLOGICAL_FUNCTION',level:i===2?'PROTEIN_LOCALIZATION':'PROTEIN_ABUNDANCE',
 identity:'PCA Yuanye B21614，作者纯度≥98%；未独立测样品；不将100µM解释为人体暴露。',model:'人HUVEC，ECM、10%FBS、37°C/5%CO2；不移用同文AC16或动物结果。',
 exposure:'1µM AngII先处理24h，再100µM PCA处理24h；AngII对照第二阶段换正常培养液。保留本行100µM，不把25/50µM合并。',
 comparison:i===2?'Fig4E五列CON、AngII、PCA25/50/100；主要100µM vs AngII。DAPI作核位置参照，不是结合/核转位定量对照。':'Fig4I/J CON、AngII、PCA25/50/100；主要100µM vs AngII；图J分别HDAC1/GAPDH及GATA4/GAPDH；图注n=3，生物/技术重复单位未明。',
 object:i===2?'NF-κB p65对应RELA；既有UniProt参考映射保持原值，不能以名称替代抗体/细胞鉴定。':protein+'人源细胞蛋白读数；既有UniProt仅参考映射。',
 actual:i===0?'Fig4I/J支持AngII升高HDAC1丰度、PCA100降低；不是HDAC1酶活抑制或PCA结合。':i===1?'Fig4I/J支持AngII降低GATA4丰度、PCA100提高；图J低中剂量未全部标显著，不声称各剂量均显著。':'Fig4E免疫荧光及Results3.4支持作者报告的p65核定位减弱；未见专门核/胞质比值或独立转位显著性统计。',
 negative:'Fig4B作者报告500µM PCA显著细胞毒性，不能外推本行100µM有毒或所有剂量安全；方法2.8声称6组却只列5组。'+(i===2?' p65图片不是蛋白结合测量。':' 未标显著的剂量不解释为零效应。'),
 locator:i===2?'Methods2.1/2.8/2.9; Results3.4; Fig4A/E':'Methods2.1/2.8/2.11; Results3.4; Fig4A/I/J',scope:'相关正文、方法、图4原图已核；仅可视化已发表图，不做原始图完整性鉴定；补充ZIP未取得有效二进制、未读未裁切blot。',
 independence:'同文001/002共用Fig4I/J与GAPDH；003来自相同研究的IF，具体样本是否共享未明；不是三项独立研究。',
 rationale:i===2?'定位响应与结合、必要性不同；本行无redox终点或已建立干预-redox链。':'蛋白丰度变化属通路/响应读数；不能借用CoIP、siRNA或其他ROS测量升级本行。',
 issues:'6组/5组报告不一致；vehicle未明确匹配；n单位/细胞批次未核；补充原始blot未读。'+(i===2?' 缺核/胞质定量与选择区域规则。':' 比值计算和完整blot应由研究者复核。'),
 decision:i===2?'是否将核定位建议标为定性读数，并要求定量后再用于机制比较；不要求因此删除观察。':'裁决蛋白丰度方向、GAPDH归一化与重复单位，保持表达不等于结合。',
 amendments:{source_review_mode:'RELATED_TEXT_AND_FIGURE4_VISUALLY_CHECKED_NO_RAW_BLOT_AUDIT',readout_level:i===2?'PROTEIN_LOCALIZATION':'PROTEIN_ABUNDANCE',normalization:i===2?'DAPI nuclear reference; no quantitative nuclear/cytoplasmic ratio recovered':protein+'/GAPDH shown in Fig4J',source_issue:'GROUP_COUNT_TEXT_SAYS_6_LISTS_5; SUPPLEMENT_NOT_RECOVERED'}})),
{id:ids[6],relation:'COMPUTATIONAL_PREDICTION',target:'COMPUTATIONAL_ONLY',redox:'OTHER_BIOLOGICAL_FUNCTION',level:'COMPUTATIONAL_DOCKING_MD',
 identity:'计算配体来自PubChem PCA结构；不等于与湿实验样品相同质子化/构象/暴露状态已确认。',model:'HDAC1计算结构来自PDB但相关方法未给可核PDB ID/构建体/物种；保留UNRESOLVED，不借用HUVEC物种。',
 exposure:'无生物剂量；Fig6B-D时间轴0–100ns（模拟时长），不是细胞100µM/24h。',comparison:'单复合物轨迹；已读相关来源未恢复apo/已知配体/独立重复轨迹对照。',object:'作者标注HDAC1；具体结构身份/金属与配体参数仍未恢复。',
 actual:'AutoDock Vina1.2.3预测score约-5.6kcal/mol；Gromacs2022、ff14SB/TIP3P；MM-PBSA取末20ns。正文3.6写-12.21kJ/mol，但Fig6G纵轴Energy(kcal/mol)。',
 negative:'正文称40ns后RMSD约0.25nm稳定；图6B仍见波动，不能据单条轨迹宣称已证明结合/收敛/自发。能量单位冲突不换算择一。',
 locator:'Methods2.14-2.16; Results3.6; Fig6A-G（G单位与正文不一致）',scope:'相关方法、结果、Fig6原图已核；补充ZIP未取得、未读轨迹/输入参数/原始MM-PBSA输出。',
 independence:'同文docking/MD/MM-PBSA为关联计算链，不是三次独立结合实验；不能与细胞表达/CoIP混合计数。',rationale:'可定位计算方法和输出支持COMPUTATIONAL_ONLY；参数缺失与单位冲突限制定量解释，不成为DIRECT_BINDING_SUPPORTED。',
 issues:'PDB/物种/构建体未恢复；MM-PBSA单位冲突；未获apo/重复轨迹、质子化/金属处理及自由能不确定性。',decision:'建议保留定性计算关系、将能量定量比较设未解决；研究者决定是否请求作者结构和单位澄清。',
 amendments:{treatment_duration:'100 ns simulation (Fig6 axis); not biological exposure',source_review_mode:'RELATED_TEXT_AND_FIGURE6_VISUALLY_CHECKED',readout_level:'COMPUTATIONAL_DOCKING_MD',reported_energy_unit_status:'CONFLICT_TEXT_KJ_PER_MOL_FIG6G_KCAL_PER_MOL',quantitative_binding_affinity:'NOT_ESTABLISHED'}},
{id:ids[7],relation:'COMPUTATIONAL_PREDICTION',target:'COMPUTATIONAL_ONLY',redox:'OTHER_BIOLOGICAL_FUNCTION',level:'COMPUTATIONAL_MD',
 identity:'PCA作者简称PA，与黑米混合提取物/唾液实验分开；计算模型不是实测受体配体。',model:'作者标注human TAS2R16；已读方法未恢复受体结构模板/版本与膜环境明确信息，参考Q9NYV7不是模型身份确认。',
 exposure:'Desmond OPLS4/SPCE，0.15mol/L盐，300K/1bar，100ns；模拟时长非生物处理时间，不使用电子舌或唾液浓度。',comparison:'基于10受体docking筛选选中TAS2R16后单复合物MD；非10受体功能试验；未恢复apo/独立重复/功能阳性对照。',
 object:'hTAS2R16（作者命名）；不能由α-amylase PDB1JXJ推断受体结构。',actual:'Fig6 RMSD/RMSF及残基接触比例；正文称70ns后相对稳定，图A配体约50ns有明显偏移，不证明受体激活。Table4 docking只是选模型背景。',
 negative:'图A中途配体RMSD大幅变化，末段平台不能替代收敛测试；没有本行受体功能阴性/阳性结果。',locator:'Methods2.8.5; Results hTAS2R16 docking/MD段; Table4; Fig6A-C',scope:'相关XML/本轮HTML、Table4及Fig6原图；mmc1.docx链接返回HTML非文档，未读补充或轨迹。',
 independence:'同文amylase实验与TAS2R16模拟为不同对象；不把前者结合实验转移到本行，也不在本轮处理其C组HOLD。',rationale:'味觉/涩感相关预测不是受体结合/激活实验，也没有本行抗氧化测量。',issues:'结构模板/膜环境、模型质量、配体偏移解释、轨迹重复与实验受体功能未恢复。',decision:'保留预测观察价值；收窄“直接刺激/激活受体”为作者推测，后续如获实验应新建观察。',
 amendments:{source_review_mode:'RELATED_TEXT_TABLE4_AND_FIGURE6_VISUALLY_CHECKED',readout_level:'COMPUTATIONAL_MD',simulation_time:'100 ns',biological_treatment_duration:'NOT_APPLICABLE',receptor_activation_status:'NOT_ESTABLISHED'}},
{id:ids[8],relation:'PATHWAY_MODULATION',target:'READOUT_ONLY',redox:'INDIRECT_OXIDATIVE_STRESS_ASSOCIATION',level:'PROTEIN_PHOSPHORYLATION_RATIO',
 identity:'Sigma PCA37580-100g-F，PBS溶解；无独立样品分析；标题physiological不足以确认人体游离暴露可达。',model:'商业mouse brain microvascular endothelial cells，DMEM4.5g/L glucose、10%FBS；不是db/db主动脉实验。',
 exposure:'PCA100nM与IL-1β0.5ng/mL overnight；未给精确小时，按方法为共孵育背景，不编造预处理。',comparison:'Fig4B CTL、IL-1β、IL-1β+PCA1/10/100nM；主要IL-1β+100 vs IL-1β单独组；图示显著括线p<0.05。',
 object:'小鼠Nos3/eNOS Ser1177磷酸化/总eNOS，抗体9570S/32027S；参考P70313不等于直接结合。',
 actual:'Fig4B轴标p-eNOS/eNOS，Fig4D有p-eNOS/eNOS及GAPDH条带；图注总称relative to GAPDH。报告比值恢复，不能擅自定为(p-eNOS/eNOS)/GAPDH或仅p-eNOS/GAPDH。',
 negative:'1/10nM未标与IL-1β比较显著，不称无效/等效；文中pAktThr308相关叙述与补图2未独立核实，不移到本行。',
 locator:'Methods2.4/2.7/2.8; Results3.4; Fig4B/D及图注',scope:'相关XML、本轮PMC HTML、Fig4原图；Supplementary Image2链接返回HTML，未读；未取得densitometry/原始blot。',
 independence:'同文001磷酸化读数与002阻断建议共享研究/模型；本轮不审核002。n=6–7为图注报告，生物/技术单位未核。',
 rationale:'磷酸化响应不是蛋白结合或充分必要性；NO/炎症/氧化背景支持间接关联，但Fig3 DHE不能写成本行直接redox。',
 issues:'“relative to GAPDH”与比值轴标的精确算法未明确；n单位、批次/原始条带和overnight小时未恢复。',decision:'优先要求研究者确认归一化流程及比较，不重复除以GAPDH；保留READOUT_ONLY及间接红氧关联是否充分由研究者裁决。',
 amendments:{source_review_mode:'RELATED_TEXT_AND_FIGURE4_VISUALLY_CHECKED_NO_RAW_DENSITOMETRY',normalization:'p-eNOS/eNOS shown; caption also says relative to GAPDH; exact calculation UNRESOLVED',readout_level:'PROTEIN_PHOSPHORYLATION_RATIO',exposure_relevance:'UNRESOLVED_NO_HUMAN_FREE_EXPOSURE_VALIDATION'}}
];
const original=await csv(path.join(pilot,'compounds/AFF-0061_Protocatechuic_Acid_Mechanism_Evidence.csv'));
const historical=(await csv(path.join(pilot,'gate2_review/AFF-0061_Gate2_Evidence_Review_Matrix.csv'))).rows;
const approvedPath=path.join(pilot,'governance_approval_v0.2/Governance_Approved_Decision_Matrix_v0.2.csv');
const rows=[];const sourceFiles=new Map();
for(const f of findings){
 const o=original.rows.find(r=>r.evidence_id===f.id);if(!o)throw Error('Missing '+f.id);
 const h=historical.find(r=>r.evidence_id===f.id);
 const p=path.join(pilot,o.source_local_path);const sourceHash=sha(await fs.readFile(p));sourceFiles.set(p,{path:path.relative(root,p).replaceAll('\\','/'),sha256:sourceHash,role:'ORIGINAL_PMC_XML_RELATED_SECTIONS_READ',distribution:'LOCAL_ONLY_EXCLUDED'});
 const amendments={evidence_relation_type:f.relation,target_confirmation_class:f.target,antioxidant_relevance_primary:f.redox,...f.amendments};
 const changes=Object.entries(amendments).map(([field,value])=>({field,old_value_presence:Object.hasOwn(o,field)?'PRESENT':'NOT_PRESENT_IN_LEGACY_SCHEMA',old_value:Object.hasOwn(o,field)?o[field]:null,proposed_value:value,reason:f.rationale,change_applied:'NO'}));
 rows.push({evidence_id:f.id,human_review_status:'NOT_REVIEWED',change_applied:'NO',record_type:'CODEX_SCIENTIFIC_RECOMMENDATION',recommendation_status:'PENDING_RESEARCHER_ADJUDICATION',rule_version:'Governance_v0.2',rule_approval_commit:'8177aebfa22d68945254ee836ec662985e5da265',rule_approval_matrix_sha256:sha(await fs.readFile(approvedPath)),review_preparation_date:'2026-10-23',preparation_agent:'Codex',human_reviewer_name:'',human_decision:'',human_approval_date:'',source_input_commit:'8177aebfa22d68945254ee836ec662985e5da265',candidate_id:o.candidate_id,study_id:o.study_id,experiment_id_legacy:o.experiment_id,DOI:o.DOI,PMID:o.PMID,PMCID:o.PMCID,original_evidence_relation_type:o.evidence_relation_type,suggested_evidence_relation_type:f.relation,original_target_validation_status_legacy:o.target_validation_status,original_target_confirmation_class:'NOT_PRESENT_IN_LEGACY_SCHEMA',suggested_target_confirmation_class:f.target,original_antioxidant_relevance_primary:'NOT_PRESENT_IN_LEGACY_SCHEMA',suggested_antioxidant_relevance_primary:f.redox,historical_gate2_proposal_status:h.review_status,historical_gate2_relation_suggestion:h.proposed_relation_type,historical_gate2_target_suggestion:h.protein_target_confirmation_proposed,historical_gate2_redox_suggestion:h.antioxidant_relevance_proposed,readout_level_suggested:f.level,compound_identity_and_form_review:f.identity,model_species_material_review:f.model,dose_time_exposure_review:f.exposure,comparison_control_normalization_review:f.comparison,protein_or_pathway_identity_review:f.object,actual_evidence_review:f.actual,classification_rationale:f.rationale,negative_adverse_or_null_review:f.negative,source_local_path:path.relative(root,p).replaceAll('\\','/'),source_file_sha256:sourceHash,source_url:'https://pmc.ncbi.nlm.nih.gov/articles/'+o.PMCID+'/',source_locator_original:o.source_locator,source_locator_reviewed:f.locator,source_verification_scope:f.scope,independence_and_duplicates_review:f.independence,unresolved_issues:f.issues,researcher_decision_required:f.decision,suggested_field_changes_json:JSON.stringify(changes),original_record_66_fields_json:JSON.stringify(o),original_record_json_sha256:sha(JSON.stringify(o)),evidence_status_original:o.evidence_status,formal_evidence_status_change:'NO',gate1_status:'HOLD',gate2_status:'HUMAN_SCIENTIFIC_REVIEW_REQUIRED',scale_up_status:'NOT_AUTHORIZED',production_migration_status:'NOT_AUTHORIZED',release_status:'HOLD'});
}
const wb=Workbook.create();const sheet=wb.worksheets.add('BatchA');const headers=Object.keys(rows[0]);
sheet.getRangeByIndexes(0,0,10,headers.length).values=[headers,...rows.map(r=>headers.map(k=>r[k]))];wb.recalculate();
const roundtrip=sheet.getRangeByIndexes(0,0,10,headers.length).values;
if(JSON.stringify(roundtrip)!==JSON.stringify([headers,...rows.map(r=>headers.map(k=>r[k]))]))throw Error('Authoring value mismatch');
const escape=v=>/[",\r\n]/.test(String(v))?'"'+String(v).replaceAll('"','""')+'"':String(v);
await fs.writeFile(path.join(dir,'AFF0061_BatchA_Scientific_Review_Matrix.csv'),roundtrip.map(r=>r.map(escape).join(',')).join('\n')+'\n');
for(const logName of ['Source_Access_Log.json','Supplement_Access_Log.json']){
 const log=JSON.parse(await fs.readFile(path.join(dir,'qc',logName),'utf8'));
 for(const f of log.entries.filter(e=>e.local_file)){const abs=path.join(dir,f.local_file);sourceFiles.set(abs,{path:path.relative(root,abs).replaceAll('\\','/'),url:f.url,sha256:f.sha256,role:f.usable_image?'PUBLISHED_FIGURE_VISUALLY_CHECKED':'CURRENT_HTML_SELECTED_SECTIONS_MATCH_CHECKED',distribution:'LOCAL_ONLY_EXCLUDED'});}
}
const supp=path.join(pilot,'gate2_review/sources/NRF2_Supplement.pdf');sourceFiles.set(supp,{path:path.relative(root,supp).replaceAll('\\','/'),sha256:sha(await fs.readFile(supp)),url:'https://pmc.ncbi.nlm.nih.gov/articles/PMC11599353/bin/10565_2024_9953_MOESM1_ESM.pdf',url_provenance:'ARTICLE_SUPPLEMENT_FILENAME_RECONSTRUCTED_POINTER_NOT_NEW_DOWNLOAD',role:'PDF_TEXT_SCREENED_TABLE5_P14_P17_VISUALLY_CHECKED_NOT_ALL49P_AUDITED',distribution:'LOCAL_ONLY_EXCLUDED'});
await fs.writeFile(path.join(dir,'qc/Reviewed_Source_Manifest.json'),JSON.stringify({date:'2026-10-23',scope:'BATCH_A_9_ONLY',raw_distribution:'LOCAL_ONLY_EXCLUDED',sources:[...sourceFiles.values()]},null,2)+'\n');
const inspection=await wb.inspect({kind:'table',range:'BatchA!A1:C10',include:'values,formulas',tableMaxRows:10,tableMaxCols:3,maxChars:2500});
const errorScan=await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NUM!|#SPILL!|#CALC!',options:{useRegex:true,maxResults:20},summary:'final error scan'});
await fs.mkdir(path.join(dir,'qc/previews'),{recursive:true});
await fs.writeFile(path.join(dir,'qc/previews/inspection.json'),JSON.stringify({inspection,errorScan},null,2));
sheet.getRange('A:C').format.columnWidthPx=280;
const image=await wb.render({sheetName:'BatchA',range:'A1:C10',scale:1,format:'png'});
await fs.writeFile(path.join(dir,'qc/previews/BatchA.png'),new Uint8Array(await image.arrayBuffer()));
console.log(JSON.stringify({observations:rows.length,columns:headers.length,publications:new Set(rows.map(r=>r.PMID)).size,source_files:sourceFiles.size,target_counts:Object.fromEntries(['OMICS_ASSOCIATED','READOUT_ONLY','COMPUTATIONAL_ONLY','NOT_APPLICABLE_NO_PROTEIN_TARGET'].map(k=>[k,rows.filter(r=>r.suggested_target_confirmation_class===k).length]))}));
