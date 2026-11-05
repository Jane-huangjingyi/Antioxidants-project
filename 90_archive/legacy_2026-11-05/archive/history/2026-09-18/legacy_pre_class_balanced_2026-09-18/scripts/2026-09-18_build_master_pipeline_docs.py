import csv, textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

R=Path(__file__).resolve().parents[1]
for x in ['docs','templates','checklists','figures','handoff','logs','references','archive','raw','extracted','processed']:(R/x).mkdir(exist_ok=True)

def put(path,text):
    (R/path).write_text(text.strip()+"\n",encoding='utf-8')
def csv_template(path,fields):
    with open(R/path,'w',newline='',encoding='utf-8-sig') as f:csv.writer(f).writerow(fields)

master=r'''# MASTER H-ORAC SCREENING PIPELINE v1.0

版本：1.0；状态：组内执行标准；适用对象：未参与本项目、需要独立完成人工筛选的研究生。本文是总入口。科学规则以 `Antioxidant_Screening_Protocol_v2.0_CN.md`、`Antioxidant_Screening_Protocol_v2.1_Addendum_CN.md` 和本 MASTER 为顺序解释；发生冲突时采用更新且范围更具体的文件，并将冲突登记到 `Pipeline_Gaps_and_Inconsistencies_CN.md`，禁止静默合并。

## 1. 目的、范围与边界

本流程比较正常膳食来源、结构明确、适用于 H-ORAC-FL 的食源性 phenolic/polyphenolic 单体的 literature-derived chemical antioxidant capacity。操作性定义为：单体在可比的 AAPH–fluorescein–Trolox H-ORAC 条件下，对 AAPH 衍生过氧自由基引起的 fluorescein 氧化所表现的 kinetic integrated chain-breaking capacity，以 mol Trolox equivalents/mol compound 表示。

本流程不回答人体抗氧化疗效、临床获益、生物利用度、疾病预防、细胞 redox regulation 或最终实验价值。L-ORAC、tocopherols、tocotrienols、carotenoids、organosulfur compounds 和 target mapping 不在当前 SOP 范围。维生素 C只能作为非多酚 benchmark，不占酚类排名名额。

核心术语：record 指一个化合物在一个独立实验和一个 assay arm 中的一项结果；eligible record 指 Tier A 或 B1；candidate universe 是先于结果建立的候选全集；provisional ranking 是历史文献探索性排名；confidence 描述证据深度，不描述容量大小；readiness 描述是否适合交接下游研究，不等同于排名。

## 2. 总流程

Scientific question → candidate universe → literature search → assay identity check → compound identity QC → record extraction → unit normalization → tier adjudication → independent experiment QC → compound aggregation → confidence → provisional ranking → evidence consolidation → before/after stability → Ready/Conditional/Not ready → downstream target-mapping handoff。

每一步实行“输入冻结—人工操作—规则判定—结构化输出—QC签名—停止条件”六段式。原始值永不覆盖；排除记录保留；任何影响名次的改动必须双人复核并写 change log。

## 3. 顺序化执行规范

### Step 0 — Define the scientific question

输入：研究目的和 protocol。操作：把比较对象、assay construct、单位和非目标写入项目说明。判断：若问题包含人体功效或跨 H/L 混排，停止并拆分问题。输出：带版本号的 scope statement。QC：第二人确认 chemical capacity 与 biological effect 已分开。自动化：manual only。下一步条件：一句话问题可被不同成员一致复述。

### Step 1 — Build candidate universe

输入：冻结范围、食品成分数据库和化学结构数据库。操作：逐项记录 canonical name、synonym、PubChem CID、InChIKey、subclass、food occurrence、parent/glycoside 和 stereochemistry。候选生成不得由 ORAC 高低反向决定。输出：candidate universe CSV。QC：结构唯一、膳食来源可追溯、糖苷/苷元不合并。脚本：`fetch_h_orac_pubchem.py`只辅助 PubChem 字段；人工确认仍必需。下一步条件：所有候选都有唯一结构或明确标为待解决。

### Step 2 — Literature search

输入：候选全集。人工检索模板：`"compound name" AND ORAC`；`"compound name" AND "oxygen radical absorbance capacity"`；`"compound name" AND AAPH AND fluorescein`；`"compound name" AND ORAC-FL`。依次查 PubMed、Google Scholar、Crossref/DOI、期刊页面和 supplement。Review 只用于发现原始来源：沿参考文献号定位 original article，再在原文核对数值和方法。输出：`Literature_Search_Log_Template.csv`。QC：每个候选留下检索日期、原式、筛选数和排除原因。自动化：manual only。下一步条件：能证明“未找到”来自已执行检索。

### Step 3 — Verify assay identity

输入：原文方法和 supplement。逐项确认 pure compound、AAPH、fluorescein、Trolox、H-arm。β-phycoerythrin、HORAC、L-ORAC、food/extract ORAC、figure-only无法精确提取、review-only 数值均不能成为 B1。输出：eligibility checklist 与 exclusion log。QC：探针名、radical generator、arm和样品类型必须从原文定位。自动化：manual only。下一步条件：assay identity 可明确判定或进入 X。

### Step 4 — Verify compound identity

输入：原文试剂信息、PubChem/ChEBI。核对 canonical name、synonym、CID、InChIKey、MW、salt/hydrate、stereochemistry、glycoside/aglycone。典型禁止合并：quercetin/quercitrin/rutin；catechin/epicatechin；genistein/genistin；cyanidin/cyanidin-3-O-glucoside。输出：身份字段和 identity QC 结论。QC：第二人逐项复核。下一步条件：可唯一映射；否则 C 或 X。

### Step 5 — Extract record-level evidence

输入：通过初筛的原文。规则：one independent experiment = one row，不是 one compound = one row；同论文不同化合物可各一行，同化合物不同 arm 或实质独立实验分行。完整字段使用 `ORAC_Record_Extraction_Template.csv`。必须记录 DOI/PMID、exact location、原值、原单位、关键方法、提取者和日期。输出：record-level CSV。QC：原值与原文逐字符复核。自动化：manual extraction；脚本不读取论文。

### Step 6 — Unit normalization

标准单位为 mol TE/mol compound。若原值为 µmol TE/g：`mol TE/mol = (µmol TE/g × MW g/mol) / 1,000,000`。例：14,272 µmol TE/g ferulic acid，MW 194.18 g/mol，结果为 14,272×194.18/1,000,000=2.771 mol TE/mol。始终保留 original value、unit、MW source、formula、converted value、reviewer 和 `conversion_verified`。盐/水合物必须使用实验所用 form 的MW。输出：标准化字段。QC：独立复算并控制有效数字。下一步条件：转换可解释；否则 B2/C/X。

### Step 7 — Evidence tier adjudication

Tier A：身份、ORAC-FL、H-arm、AAPH、fluorescein、Trolox、介质、温度、读数/AUC、线性、纯度、干扰和单位足以支持高置信正式比较。Tier B1：满足 pure defined compound、original ORAC-FL、H-arm、Trolox、可提取且可转换的原值、主要条件可识别、无明显未解决严重干扰、原文可追溯；可缺少少量非关键参数。Tier B2：有定量值但 metadata、兼容性或干扰控制不足，不进入主排名。Tier C：已知不兼容，例如错误探针、错误 arm、extract/food value 或不可统一单位。Tier X：信息不足，尚不能判定。Tier 衡量 comparability/eligibility，不是期刊质量。输出：tier+rationale。QC：双人独立判级。

### Step 8 — Independent experiment adjudication

输入：全部候选记录及引用链。same experiment reused、review citation、same dataset、同一表格重复发表均不独立；真正分开的实验研究才独立。创建稳定的 `independent_experiment_id`，建议 `FIRSTAUTHOR_YEAR_DOI_ASSAYARM_EXPERIMENT`。同一 ID 对同一 compound 只计一次。输出：independence 字段和排重日志。QC：比较作者、实验室、批次、方法、数值和引用来源。下一步条件：每项 eligible record 有经复核的ID。

### Step 9 — Compound-level aggregation

输入：去重后的 A/B1。一个候选有≥2项时报告 n、median、min、max；n≥4时报告 IQR；一项时标记 single-study。禁止最大值、选择“最好看”数值或对不兼容 protocol 任意均值。输出：compound summary。脚本：现有 `build_h_orac_top20.py` 和 `build_top20_consolidation.py`含项目特定聚合逻辑，运行前必须审查输入和硬编码来源。QC：人工用 Excel 抽查至少3项。

### Step 10 — Evidence confidence

High：≥3 independent A/B1 且无高异质性或重大方法冲突；Moderate：2 independent A/B1；Low：1 A/B1；Very low：只有 B2，不进入主榜。若≥3但异质性高，不能自动 High，须降级或人工说明。Confidence 与 ORAC magnitude 不合成总分。输出：confidence 与理由。

### Step 11 — Provisional ranking

按 median mol TE/mol 降序。保留 rank、A/B1数、confidence、single-study、heterogeneity和special-case flag。相同中位数不得用论文数量伪造差异，可并列或按预设稳定规则并记录。输出：版本化排名 CSV 和图。脚本：`build_h_orac_top20.py`；当前实现含项目数据硬编码，仅适合复现本项目版本，不是通用引擎。QC：重新排序、检查20项、确认 benchmark不占名额。

### Step 12 — Evidence consolidation

触发条件：Top candidate仅一篇；重要候选缺失；subclass低覆盖；异常值；排名不稳定。执行定向原始文献追溯，不降低B1标准。记录新增、排除、纠错和未找到。输出：consolidation records、missing-important list和change log。脚本：`build_top20_consolidation.py`可复现当前 consolidation，但文献判断是人工的。

### Step 13 — Before/after stability check

输入：两个冻结排名版本。输出 rank_before、rank_after、rank_change、B1 count change、confidence change、entered/exited Top20；说明变化来自新增独立证据、纠错还是补强。QC：新旧文件只读，禁止覆盖。脚本：`build_top20_consolidation.py`。

### Step 14 — Freeze shortlist

Ready：Top20内，≥2 independent B1或有明确稳定性证据，身份清楚，无重大未解决 assay concern。Conditionally ready：single-study B1、排名合理但证据薄。Not ready：无B1、重大光学/溶解/身份问题。Ranking 与 readiness 是两种输出，绝不合成。输出：版本化 shortlist 与签字冻结记录。

### Step 15 — Handoff to downstream target mapping

交接前必须具备 canonical name、CID、InChIKey、form/stereochemistry、rank、median、eligible count、confidence、assay risk、readiness、key DOI/PMID、Zotero key或明确 pending 状态、record IDs和provenance路径。本 SOP 到此停止，不执行 target extraction。

## 4. QC、人工复核与常见错误

身份、tier、原始数值、换算、独立性及任何改名次的纠错必须双人复核。常见错误详见 `Common_Failure_Modes_H_ORAC_CN.md`；可打印筛查表为 `ORAC_Eligibility_Checklist_CN.md`。程序可以进行单位计算、分组统计、排序、制图和字段完整性检查；assay identity、光学干扰、化合物 form、文献独立性和 tier 必须人工判断。

## 5. 文件、命名与版本

原始文件进入 `raw/`，人工抽取进入 `extracted/`，派生结果进入 `processed/`，正式发布副本进入 `data/`。推荐命名：`H_ORAC_<artifact>_vMAJOR.MINOR_YYYYMMDD.csv`。Protocol科学规则变化升 major；数据追加且规则不变升 minor；排版修订升 patch。禁止 silent overwrite；旧版移入 `archive/`但不删除。每个派生文件记录生成脚本版本、输入文件哈希或文件名、时间、提取者和复核者。

## 6. 数据溯源与进入下一阶段

最终 rank 必须能够逆向到 compound summary → eligible record → independent experiment ID → original paper → DOI/PMID → exact table/page → original value/unit → MW与公式 → standardized value。任何一环缺失都必须标为 gap。只有完成双人复核、排除日志、change log、before/after稳定性和shortlist冻结，才能移交 target mapping。详细逆向示例见 `Data_Provenance_Chain_CN.md`。
'''
put('docs/MASTER_H_ORAC_SCREENING_PIPELINE_v1.0_CN.md',master)

sops={
'01_Candidate_Generation':('建立与结果无关的候选全集','冻结的H-arm食源性酚类范围','scope文件；食品来源；PubChem/ChEBI','浏览器、PubChem、候选模板','按subclass列候选；核对膳食来源；锁定CID/InChIKey；分开苷元/糖苷及立体异构体','不得按ORAC结果反向纳入；混合物、提取物及主要药用来源不入主榜','每项有唯一结构；food occurrence有来源；第二人复核身份','把quercetin、quercitrin、rutin合并；先看ORAC再决定候选','版本化candidate universe CSV','所有候选身份已解决或标记待解决','Quercetin、quercitrin、rutin分别建行。'),
'02_Literature_Search':('形成可审计、可复查的检索记录','candidate universe中的每个候选','候选名称、同义词和检索日志模板','PubMed、Google Scholar、Crossref、期刊网站','逐一运行四个标准检索式；记录日期和命中；从review追到original；检查supplement','Review只做线索；无法获取原文不得当B1','检索式原样保存；排除原因成组统计；第二人抽查高重要性缺失项','只记录找到的文献而不记录没找到；用综述表格代替原文','完整search log和候选文献清单','每个候选有可证明的检索记录','EGCG检索必须同时查AAPH、fluorescein并排除β-PE。'),
'03_ORAC_Assay_Eligibility':('判定记录是否属于当前H-ORAC-FL构念','所有候选原始全文','方法、结果、supplement及checklist','PDF阅读器、eligibility rubric','确认pure compound、AAPH、fluorescein、Trolox、H-arm；定位原值；记录排除项','β-PE、HORAC、L-ORAC、extract/food、review-only和不可读图不能B1','每项判断有页码；探针和radical generator不可凭标题推断','看到ORAC就纳入；把fluorescein-HORAC误当ORAC-FL','tier候选和exclusion log','能够判A/B1/B2/C或X','Ou 2002 fluorescein HORAC仍是C。'),
'04_Compound_Identity_QC':('确保每条数值对应唯一化学实体','通过assay初筛的记录','原文试剂、PubChem、CID/InChIKey','PubChem/ChEBI、结构查看器','核对名称、form、盐/水合物、MW、立体化学和糖苷位置','结构不同即分行；实验form决定MW','CID和InChIKey匹配；两人复核','用aglycone MW换算glycoside；忽略hydrate','身份已确认的record字段','无法唯一识别时停止换算并判C/X','Cyanidin与C3G不可合并。'),
'05_Record_Level_Data_Extraction':('把原文证据变成可审计记录','通过身份与assay初筛的原文','ORAC record模板','PDF、Excel或CSV编辑器','一项独立实验一行；录入书目信息、exact location、原值、条件、身份、提取者','技术重复不拆行；不同arm分行','双人逐字符复核原值和单位；必填字段不得空白','一化合物一行；只保留换算值','record-level CSV','原值、来源位置和关键方法齐全','同论文的quercetin与catechin分别成行。'),
'06_Unit_Normalization':('统一为mol TE/mol compound','身份确认且单位可解释的记录','原值、单位、MW及来源','Excel或计算器；Python/R可选','识别单位；写公式；计算；保留足够精度；第二人独立复算','µmol TE/g×MW/1e6；直接mol/mol不再换算；form-specific MW','original不覆盖；conversion_verified签名；有效数字合理','忘除1e6；用错误盐型MW；把food µmol/100g换成单体值','带完整换算链的record','换算可复现，否则B2/C/X','14,272×194.18/1e6=2.771。'),
'07_Evidence_Tiering':('按可比性而非期刊声望分层','完成提取和换算的record','v2.1、rubric、checklist','人工审阅表','两人独立判A/B1/B2/C/X；写rationale；解决分歧','A正式；A+B1探索排名；B2支持；C不兼容；X信息不足','不得用分数投票替代关键门槛；保留初判与终判','为凑数据降B1；把高影响因子当A','tier和理由','两位复核者一致或第三人裁决','C3G有数值但光学QC不足，判B2。'),
'08_Independent_Experiment_QC':('防止同一数据被重复计权','全部A/B1及引用链','作者、DOI、数值、方法、批次信息','文献管理器、Excel','建立experiment ID；比较数据来源；标记复用、review和重复出版','同数据集只计一次；不同化合物可各有record但各自ID','同一compound+ID唯一；疑似重复由第二人复核','把review引用算新研究；把技术重复算独立','去重记录及ID','所有eligible记录完成独立性判断','同论文同一ORAC表中的同化合物只有一个experiment ID。'),
'09_Aggregation_Ranking_Confidence':('从record生成compound summary与排名','去重A/B1 records','compound summary模板','Excel、R/Python；现有build脚本','分组；计算n/median/range/IQR；赋confidence；按median排序；输出图','一条=Low；两条=Moderate；≥3且异质性可接受=High；只有B2=Very low','抽查公式；不取最大；confidence与数值分开','用mean掩盖异质性；热门分子因论文多加分','summary、ranking和confidence图','记录数与summary一致，排序复算通过','Quercetin多记录以median而非maximum排序。'),
'10_Evidence_Consolidation':('验证高位单研究候选和关键缺失项','provisional ranking、coverage和missing list','targeted search log、exclusion/change templates','同SOP02工具','按触发条件定向检索；不降低tier；复算；更新before/after','只添加真正独立B1；所有变化写change log','重点审查outlier、类别缺失和figure-only记录','无差别扩大候选池；静默替换旧值','consolidation records和稳定性表','target list和未解决风险可明确陈述','EGCG通过探针追溯排除错误来源后补入B1。'),
'11_Shortlist_Freeze_and_Handoff':('冻结分层的下游候选清单','consolidated ranking和assay risk','shortlist模板、provenance、双人签字','Excel/CSV、版本控制','按Ready/Conditional/Not ready分层；核对必备身份和来源字段；冻结版本','排名不等于readiness；单研究可conditional但不可伪装stable','20项逐行检查；交接字段无空白或有明确pending理由','要求所有20项都Ready；直接开始靶点抓取','版本化shortlist和handoff','负责人签字并发布只读版本','两项B1且无重大assay concern可Ready。')}

for key,v in sops.items():
    title=key.replace('_',' ')
    sections=['Purpose','Scope','Required input','Required tools','Step-by-step procedure','Decision rules','QC checklist','Common mistakes','Required output','Stop condition','Example']
    body='# SOP '+title+'\n\n版本：1.0；所有判断须遵循 MASTER v1.0，冲突进入 gap audit。\n\n'
    for h,txt in zip(sections,v):body+=f'## {h}\n\n{txt}\n\n'
    put(f'docs/SOP_{key}_CN.md',body)

csv_template('templates/ORAC_Record_Extraction_Template.csv',['record_id','compound_name','canonical_name','PubChem_CID','InChIKey','chemical_class','subclass','parent_or_glycoside','stereochemistry','study','year','PMID','DOI','journal','exact_location','original_value','original_unit','ORAC_probe','radical_generator','Trolox_reference','H_or_L_arm','buffer','pH','temperature','solvent','cosolvent','cyclodextrin','AAPH_concentration','fluorescein_concentration','reading_interval','total_duration','AUC_method','purity','concentration_range','linearity','optical_interference_QC','molecular_weight','MW_source','conversion_formula','standardized_mol_TE_per_mol','conversion_verified','evidence_tier','eligibility_rationale','independent_experiment_id','independence_verified','extractor','reviewer','extraction_date','notes'])
csv_template('templates/ORAC_Compound_Summary_Template.csv',['compound','PubChem_CID','InChIKey','subclass','eligible_record_count','Tier_A_count','Tier_B1_count','Tier_B2_count','median_ORAC','min_ORAC','max_ORAC','IQR','confidence','single_study_flag','heterogeneity_flag','assay_risk','provisional_rank','readiness','key_sources','notes'])
csv_template('templates/Literature_Search_Log_Template.csv',['compound','database','search_date','exact_query','results_found','records_screened','fulltexts_checked','included_B1','excluded','exclusion_reason','reviewer','notes'])
csv_template('templates/ORAC_Exclusion_Log_Template.csv',['compound','source','DOI','PMID','exclusion_category','exclusion_reason','probe_issue','arm_issue','compound_identity_issue','unit_issue','optical_issue','duplicate_issue','reviewer','date'])
csv_template('templates/Ranking_Change_Log_Template.csv',['version','date','compound','old_rank','new_rank','old_value','new_value','old_B1_count','new_B1_count','change_type','reason','source_added_or_removed','reviewer'])

put('checklists/ORAC_Eligibility_Checklist_CN.md',r'''# ORAC Eligibility Checklist（可打印）

记录ID：________  化合物：________  文献：________  Reviewer：________  日期：________

- [ ] pure compound
- [ ] food-derived
- [ ] identity confirmed
- [ ] PubChem matched
- [ ] H-arm
- [ ] AAPH
- [ ] fluorescein
- [ ] Trolox
- [ ] original value available
- [ ] unit interpretable
- [ ] mol TE/mol conversion possible
- [ ] no severe unresolved optical interference
- [ ] not β-PE
- [ ] not HORAC
- [ ] not L-ORAC
- [ ] not food/extract ORAC
- [ ] independent experiment verified
- [ ] source traceable
- [ ] exact table/figure/location recorded
- [ ] glycoside/aglycone, salt/hydrate and stereochemistry checked
- [ ] original value and conversion independently verified

初判：A / B1 / B2 / C / X。理由：________________。第二复核者：________。终判：________。
''')

put('docs/Common_Failure_Modes_H_ORAC_CN.md',r'''# H-ORAC 常见错误手册

1. ORAC ≠ ORAC-FL：必须核对探针。2. H-ORAC ≠ L-ORAC：未经桥接不混排。3. HORAC ≠ ORAC：即使使用 fluorescein，羟自由基防护也不是AAPH过氧自由基ORAC。4. β-phycoerythrin ≠ fluorescein。5. extract/food ORAC ≠ pure-compound ORAC。6. review value ≠ original record，综述只用于追索。7. glycoside ≠ aglycone，结构和MW均不同。8. same paper ≠ independent evidence，同一数据复用只计一次。9. maximum ≠ representative value，聚合用median。10. ranking magnitude ≠ confidence。11. missing data ≠ low capacity。12. publication density ≠ biological importance。13. colored compounds可产生inner-filter、自发荧光、quenching及光谱重叠。14. cyclodextrin/cosolvent可改变溶解度、自由基可及性和表观反应。15. figure-only估读不是精确值，除非作者提供数字或有预先批准的数字化规则，否则最多B2。16. 技术重复不是独立研究。17. 直接mol/mol值不要重复乘MW。18. 盐、水合物或异构体MW不可互换。19. 缺参数不能自动判C：信息不足通常先判X。20. 旧排名不可被新版本静默覆盖。
''')

put('docs/Pipeline_Script_Map_CN.md',r'''# Pipeline Script Map

| pipeline step | manual task | script file | input file | output file | editable parameters | expected runtime | QC output | manual review required |
|---|---|---|---|---|---|---|---|---|
| Step 0 scope | 冻结问题 | manual only | protocol | scope statement | none | 30–60 min | scope签字 | yes |
| Step 1 candidate | 食物与结构核对 | scripts/fetch_h_orac_pubchem.py | 脚本内候选名 | data/pubchem_h_orac_phenolics.json | query names | 数分钟，受网络影响 | error字段 | yes |
| Step 2 search | 检索及追原文 | manual only | candidate universe | search log | search dates/queries | 每候选30–90 min | 检索日志 | yes |
| Steps 3–8 | assay、身份、抽取、换算、tier、独立性 | manual only | 原文全文 | extraction/exclusion records | rubric | 每篇20–60 min | 双人checklist | yes |
| Pilot | 早期pilot重建 | scripts/build_orac_pilot.py | 脚本内数据和PubChem JSON | pilot CSV/figures/docs | embedded records | <1 min | count/figure | yes |
| Exploratory | B1/B2探索输出 | scripts/build_orac_exploratory.py | pilot CSV | exploratory CSV/figures | embedded adjudication | <1 min | count/figure | yes |
| Steps 9–11 | 候选聚合和provisional榜 | scripts/build_h_orac_top20.py | PubChem JSON、pilot reclassification | candidate/ranking CSV及图 | embedded candidate/source records | <1 min | candidate/eligible counts | yes；脚本非通用 |
| Steps 12–14 | consolidation、稳定性、shortlist | scripts/build_top20_consolidation.py | provisional data、candidate universe | consolidation records、before/after、shortlist及图 | embedded added records/rules | <1 min | records/top20/readiness counts | yes；脚本非通用 |
| SOP文档 | 生成本套文档和模板 | scripts/build_master_pipeline_docs.py | 冻结规则 | docs/templates/checklists/flowchart | SOP文本 | <1 min | 文件清单 | yes |

现有构建脚本含硬编码研究记录和候选定义，适合复现对应版本，不应被当作自动文献抽取或通用排名引擎。运行前必须备份输出，禁止覆盖冻结版本。
''')

put('docs/Recommended_Project_Folder_Structure_CN.md',r'''# 推荐项目目录结构

```text
project/
  README_H_ORAC_PIPELINE.md
  docs/          # protocol、MASTER、SOP、教程、审计说明
  config/        # rubric、字段字典、固定参数
  raw/           # 原始下载数据和只读原文索引
  extracted/     # 人工逐记录抽取；未聚合
  processed/     # 标准化、去重、聚合中间表
  data/          # 冻结发布的数据表
  figures/       # 可由processed/data重建的图
  scripts/       # 有版本的可执行脚本
  templates/     # 空白人工模板
  checklists/    # 可打印QC表
  logs/          # search、exclusion、run和review日志
  references/    # BibTeX/RIS、Zotero导出及文献清单
  handoff/       # 阶段同步和上传清单
  archive/       # 旧版只读快照；禁止删除
```

`raw/`永不被脚本改写；`extracted/`保留原值；`processed/`允许重建；`data/`只有通过复核的冻结版本；`figures/`不得成为数据源。每次发布同时归档输入、脚本版本、run log和change log。
''')

put('docs/Versioning_and_Audit_Rules_CN.md',r'''# Versioning and Audit Rules

Protocol 使用 `vMAJOR.MINOR`：科学构念、tier门槛或范围变化升MAJOR；澄清和兼容补丁升MINOR。Ranking 使用 `ranking_vMAJOR.MINOR_YYYYMMDD`：eligibility/aggregation规则变化升MAJOR；新增合格记录升MINOR。Record 数据集和 shortlist 各自独立版本，不继承文件修改时间作为版本。

禁止 silent overwrite。发布新文件前把旧版复制到 `archive/<artifact>/<version>/`，并保持只读。Changelog 必须列出新增/删除记录、旧/新数值、旧/新名次、B1计数、原因、来源和复核者。Excluded records 保留在exclusion log，raw values永不删除或被标准化值覆盖。所有derived values必须能由冻结record文件和脚本重算。日期采用ISO 8601；人员使用固定 initials，同时在组内受控人员表映射全名。任何 rank-changing correction 要求两人签字；脚本运行记录命令、Python版本、输入文件名/哈希、输出和时间。
''')

put('docs/Data_Provenance_Chain_CN.md',r'''# Data Provenance Chain

逆向链固定为：rank → compound summary → eligible records → independent_experiment_id → original paper → DOI/PMID → exact table/page/supplement → original numerical value/unit → molecular weight source与conversion formula → standardized mol TE/mol → compound median → confidence/rank。

真实示例 quercetin：排名文件中的 quercetin 中位数必须回到 `Top20_Evidence_Consolidation_Records.csv` 中的多个 B1 行；每行包含 experiment ID、study、DOI/PMID、exact location、原始单位、换算状态和理由。例如 Ou 2001（DOI 10.1021/jf010586o，Table 4）直接报告7.28 mol TE/mol，无MW换算；Carvalho 2023（DOI 10.3390/antiox12020505，Table 3）报告16.62并注明quercetin dihydrate form风险；新增独立研究分别保留自己的experiment ID。去重后的值排序并取median，记录数决定confidence。审计者不能从图反推数值，必须沿CSV回到原文。

最小provenance要求：DOI或PMID至少一个；精确位置；原值和单位；身份form；experiment ID；换算公式与复核；tier理由。缺一项即在gap字段说明，不得用“已核对”笼统替代。
''')

put('docs/Two_Reviewer_QC_Rules_CN.md',r'''# 双人复核规则

必须双人复核：compound identity；eligibility tier；original numerical extraction；unit conversion；duplicate/independence；任何rank-changing correction。Reviewer 1完成抽取并签名，Reviewer 2在不看R1结论时优先独立核对原文，再记录agree/disagree。不得由同一人用两个缩写完成。

分歧处理：先定位争议字段和原文页码；双方分别写一行理由；以冻结rubric逐条判定。仍不能一致时交第三位资深研究者裁决，保留R1、R2和final三个值以及裁决日期。信息不足优先判X，不以多数投票降低门槛。Rank-changing纠错发布前必须重跑聚合、before/after和图，并由未参与修正者抽查至少受影响候选及相邻两名。严重错误应发布勘误而不是覆盖旧文件。
''')

put('docs/H_ORAC_Pipeline_Tutorial_CN.md',r'''# H-ORAC Pipeline 教学版

先理解问题：我们比较的是试管中纯酚类分子对AAPH产生的过氧自由基保护fluorescein的能力，不是人体疗效。第一天先建立候选表，不看谁的ORAC高；第二天开始逐个检索并留下搜索日志。看到“ORAC”不能立即抄数值，必须打开方法确认AAPH、fluorescein、Trolox、H-arm和纯单体。

案例1 quercetin：它有多项独立B1。每项原值分别成行并有experiment ID，去重后取median；研究数量和异质性决定confidence，再按median进入排名。不能取16.62这一最大值代表quercetin。

案例2 EGCG：早期搜索同时出现β-phycoerythrin、HORAC、L-ORAC和只有图形的结果。这些不能成为H-ORAC-FL B1。继续沿参考文献追到使用AAPH–fluorescein–Trolox且报告精确数值的原始研究后，才形成合格记录。缺数据期间不能写“EGCG能力低”。

案例3 cyanidin-3-O-glucoside：原文可以有精确数值，但它是有色分子；若未处理inner-filter、光谱重叠、自发荧光、quenching和pH结构转化，仍只能B2，不进入主排名。

案例4 secoisolariciresinol：没有可用膳食parent lignan ORAC-FL时，记录“检索完成、未找到”，不可用人体代谢物enterodiol或enterolactone替代。Missing不是零，也不是低活性。

做完抽取后，第二个人复核身份、原值、单位、tier和独立性。Excel按compound筛选A/B1，计算MEDIAN、MIN、MAX和COUNT；n≥4再报告IQR。排序后检查benchmark未占名额，再做consolidation和before/after。最后按Ready、Conditionally ready、Not ready分层，至此停止并交接下游。
''')

put('docs/NO_AI_MANUAL_EXECUTION_GUIDE_CN.md',r'''# 无 AI 人工执行指南

假设只有浏览器、PubMed/Google Scholar、Excel，R/Python可选。Day 1上午阅读README、MASTER、SOP01–04，复制五个空白模板并冻结scope；下午建立候选表，逐项核对CID/InChIKey、form、food occurrence。Day 2开始按候选运行四个检索式，每次把数据库、日期、原式、命中和筛选数写入search log；用review发现原文，但不抄review数值。后续每天以“一个候选完成一个闭环”为单位：全文→assay checklist→身份QC→一实验一行→换算→tier→独立性。

Excel建议工作簿含五张表：Candidates、Search_Log、Records、Exclusions、Compound_Summary；Change_Log单独保存并版本化。每录入一个数值立即记录exact page/table，不要留到最后。可以程序化的内容：单位算术、字段完整性、分组n/median/range/IQR、排序、制图和重复ID报警。必须人工判断：probe、HORAC/ORAC差异、H/L arm、化学form、光学干扰、原始/二手来源、独立实验和tier。

停止点：身份无法唯一确定时停止换算；probe或arm不明时判X并停止排名使用；只有图无数字时进入B2/exclusion；完成一个候选检索且所有线索有去向后才可写“未找到”。必须请第二人复核的时点是身份锁定、tier终判、原始数值、每个换算、experiment ID及任何会改变名次的修正。完成所有候选、生成summary和before/after、填完exclusion/change log并得到双签后，才可冻结shortlist。

若不使用R/Python，Excel公式示例：标准化值=`original_umol_per_g*MW/1000000`；中位数=`MEDIAN(FILTER(values,compound=current))`；计数=`COUNTIFS(compound,current,tier,"B1")+COUNTIFS(compound,current,tier,"A")`。公式列锁定后由第二人抽查至少10%和全部rank-changing行。
''')

put('docs/Pipeline_Gaps_and_Inconsistencies_CN.md',r'''# Pipeline Gaps and Inconsistencies Audit

已完全可复现的部分：在给定结构化record和硬编码来源的前提下，现有脚本可重建pilot、exploratory图、50项candidate表、provisional ranking、consolidation before/after、confidence图和shortlist。单位公式、median/range、排名方向和输出文件均可检查。

依赖人工判断的部分：文献检索完整性、ORAC构念识别、H/L分臂、化合物form、光学/溶解干扰、A/B1/B2/C/X、独立性和outlier解释。当前没有自动化全文解析，也不应把这些判断完全自动化。

冲突与最新冻结解释：v2.0的A/B/C/X被v2.1的A/B1/B2/C/X补充替代；旧`ORAC_Literature_Eligibility_Rubric.csv`仍以`Tier_B_requirement`单列B，未结构化拆成B1/B2，执行时以v2.1为准。早期Candidate Scope覆盖H/L和非酚类；当前MASTER仅适用H-arm phenolic/polyphenolic。`H_ORAC_Provisional_Ranking.csv`是consolidation前版本；当前结果见`Top20_Ranking_Before_After.csv`，旧文件不得覆盖。High confidence的科学定义包含“≥3且低/中等异质性”，但当前`build_top20_consolidation.py`实现按n≥3直接赋High，尚未把异质性降级自动写入confidence；正式发布须人工复核，这是最重要的未自动化差异。

结构化不足：部分早期记录的exact location、purity、linearity、optical QC和完整assay参数缺失；consolidation文件的新增记录使用概括性exact location，未全部保存页码/表号的PDF证据副本。检索日志、exclusion log、reviewer initials和第二复核签名此前不完整。本次创建空白模板但没有回填历史全过程，因为本轮禁止自动重分类旧记录。

脚本缺失：没有通用的模板验证器、CSV schema validator、独立性重复报警、文件哈希/run manifest、通用聚合CLI或自动版本归档。现有构建脚本硬编码候选与文献，不能直接用于新项目。

Zotero缺口：本地API此前不可用；Tabart 2009、Zhang 2013、Rothe 2023、Sakurai 2022、Ishimoto 2012和Paillat 2023等存在`pending_local_import`，未取得真实item key。不能将pending当已入库。

未来需要补充：结构化B1/B2 rubric；明确heterogeneity阈值或只保留人工判定；anthocyanin optical QC最低标准；cyclodextrin/共溶剂桥接规则；通用脚本schema；完整历史search/exclusion日志；Zotero回填；原文文件哈希和受控存档。

无AI执行的最大困难是从二手综述追到原始实验并正确辨认probe/arm，以及判断相似数值是否来自同一数据集。其次是有色、低溶解度化合物的干扰判断。这些需要训练、双人复核和可访问全文，不应由简单脚本替代。
''')

put('README_H_ORAC_PIPELINE.md',r'''# H-ORAC Screening Pipeline

新成员先读 `docs/MASTER_H_ORAC_SCREENING_PIPELINE_v1.0_CN.md`，再读 `docs/H_ORAC_Pipeline_Tutorial_CN.md`。实际执行依次使用 SOP_01 至 SOP_11；无AI环境直接按 `docs/NO_AI_MANUAL_EXECUTION_GUIDE_CN.md` 安排工作。

开始前复制五个模板：record extraction、compound summary、literature search log、exclusion log和ranking change log。每篇文献同时使用 `checklists/ORAC_Eligibility_Checklist_CN.md`。身份、tier、原值、换算、独立性和排名变更必须遵守 `docs/Two_Reviewer_QC_Rules_CN.md`。

脚本与输入输出对应关系见 `docs/Pipeline_Script_Map_CN.md`。现有脚本用于复现本项目历史版本，不能替代检索与人工判级。目录放置、版本和归档分别见 `Recommended_Project_Folder_Structure_CN.md` 与 `Versioning_and_Audit_Rules_CN.md`。

最终必须产生：candidate universe、search log、record table、exclusion log、compound summary、provisional ranking、confidence、consolidation records、before/after、change log和分层shortlist。自检标准：每个rank能沿 `Data_Provenance_Chain_CN.md` 回到原文；所有排除有原因；旧值未覆盖；派生值可重算；双人复核完成。已知缺口先查 `Pipeline_Gaps_and_Inconsistencies_CN.md`，不得自行静默修复。
''')

# Flowchart
steps=['Scientific question','Candidate universe','Literature search','Assay identity check','Compound identity QC','Record extraction','Unit normalization','Tier adjudication','Independent experiment QC','Compound aggregation','Evidence confidence','Provisional ranking','Evidence consolidation','Before/after stability','Ready / Conditional / Not ready','Downstream target mapping']
W,H=1500,1800; im=Image.new('RGB',(W,H),'white');d=ImageDraw.Draw(im); font='C:/Windows/Fonts/arial.ttf';bold='C:/Windows/Fonts/arialbd.ttf'
f=lambda n,b=False:ImageFont.truetype(bold if b else font,n)
d.text((70,35),'MASTER H-ORAC SCREENING PIPELINE v1.0',font=f(36,1),fill='#17233b');d.text((70,82),'Manual-first · traceable · versioned · two-reviewer QC',font=f(19),fill='#526074')
y=140
for i,s in enumerate(steps):
    col='#2a9d8f' if i not in (3,4,7,8,14) else '#457b9d';
    d.rounded_rectangle((280,y,1220,y+70),18,fill=col);d.text((330,y+18),f'{i}. {s}',font=f(23,1),fill='white')
    if i<len(steps)-1:d.line((750,y+70,750,y+100),fill='#6b7688',width=5);d.polygon([(740,y+92),(760,y+92),(750,y+105)],fill='#6b7688')
    y+=102
d.text((70,1760),'A/B1 enter ranking · B2 supportive · C incompatible · X unresolved · H/L never pooled without bridging',font=f(18),fill='#3f4d5f')
im.save(R/'figures/H_ORAC_SCREENING_PIPELINE_FLOWCHART.png')

put('handoff/H_ORAC_Master_Pipeline_Sync_to_ChatGPT_CN.md',r'''# H-ORAC Master Pipeline 同步

A. MASTER pipeline 已完成，主入口为 `docs/MASTER_H_ORAC_SCREENING_PIPELINE_v1.0_CN.md`。B. 共11份统一格式中文SOP。C. 共5个CSV人工模板。D. 已建立可打印eligibility checklist。E. 已建立无AI、按工作日和Excel工作表执行的manual guide。F. 脚本覆盖聚合、排名、图和现有版本复现；检索、身份、tier、独立性仍为manual only。G. provenance链已定义到DOI/PMID、exact location、原值、换算和rank。H. 主要缺口是历史search/exclusion日志未完整回填、部分exact location不够精细、缺少通用schema validator。I. 未解决冲突包括v2.0 B与v2.1 B1/B2、旧宽candidate scope与当前H-arm范围，以及脚本High confidence未自动结合异质性。J. 文档已具备组内使用条件，但首次执行应由资深成员带教并抽查。K. 无AI可执行；最大难点为原文追溯、probe/arm识别和独立性判断。L. 下一改进优先级：回填历史检索/排除日志；修订结构化B1/B2 rubric；建立通用CSV验证与run manifest；恢复Zotero并回填item keys。
''')

files=['README_H_ORAC_PIPELINE.md','docs/MASTER_H_ORAC_SCREENING_PIPELINE_v1.0_CN.md','docs/NO_AI_MANUAL_EXECUTION_GUIDE_CN.md','docs/Pipeline_Gaps_and_Inconsistencies_CN.md','docs/Two_Reviewer_QC_Rules_CN.md','docs/Data_Provenance_Chain_CN.md','docs/Pipeline_Script_Map_CN.md','docs/H_ORAC_Pipeline_Tutorial_CN.md','checklists/ORAC_Eligibility_Checklist_CN.md','figures/H_ORAC_SCREENING_PIPELINE_FLOWCHART.png']
rows=['# H-ORAC Master Pipeline files to upload','', '## Priority 1','', '| filename | path | purpose | why needed | priority |','|---|---|---|---|---|']
for p in files[:5]:rows.append(f'| {Path(p).name} | {p} | 核心执行/审计文件 | 决定流程能否独立执行 | Priority 1 |')
rows+=['','## Priority 2','', '| filename | path | purpose | why needed | priority |','|---|---|---|---|---|']
for p in files[5:]:rows.append(f'| {Path(p).name} | {p} | QC、教学或可视化 | 核查方法与培训 | Priority 2 |')
rows+=['','## Priority 3','', '| filename | path | purpose | why needed | priority |','|---|---|---|---|---|','| SOP_01–SOP_11 | docs/SOP_*_CN.md | 分步骤作业指导 | 实际执行时按步骤上传 | Priority 3 |','| CSV templates | templates/*.csv | 空白记录表 | 建立新批次时使用 | Priority 3 |','| build_master_pipeline_docs.py | scripts/build_master_pipeline_docs.py | 文档与模板生成脚本 | 审核可复现性 | Priority 3 |']
put('handoff/H_ORAC_Master_Pipeline_Files_to_Upload_to_ChatGPT.md','\n'.join(rows))

print('master pipeline artifacts generated')
