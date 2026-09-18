from pathlib import Path
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]; DATA=ROOT/'data'; DOCS=ROOT/'docs'; FIG=ROOT/'figures'/'aqueous_antioxidant_atlas'
c=pd.read_csv(DATA/'Aqueous_Antioxidant_Candidate_Master.csv'); sup=pd.read_csv(DATA/'Supervisor_Aqueous_Class_Ranking_Overview.csv'); ev=pd.read_csv(DATA/'Aqueous_Antioxidant_Primary_Literature_Evidence.csv'); papers=pd.read_csv(DATA/'Aqueous_Antioxidant_Paper_Summary.csv')

reports={
'Stilbenes_Lignans_TopN_Report_CN.md':'''# Stilbenes / Lignans Top available 报告

冻结候选 15 个；逐候选检索后，只有 trans-resveratrol 与 sesamol 具有可追溯、可换算且满足 B1 的 H-ORAC-FL 数值，因此输出 Top available 2，而不是 Top20。trans-resveratrol 为 5.811、sesamol 为 2.107 mol TE/mol；二者均为 single-study、Low confidence/Fragile。其余候选未被记为零，也未用 enterolignans 替代膳食 parent lignans。Podophyllotoxin 的 normal-dietary gate/aqueous scope 触发 HUMAN REVIEW REQUIRED，但候选记录未被修改。''',
'Betalains_Nitrogen_Profile_Report_CN.md':'''# Betalains / Nitrogen-containing profile 报告

冻结候选 11 个。该 panel 不生成 raw-value TopN：候选包括强色素 betalains 以及 caffeine/trigonelline，单一 H-ORAC 构念并不适合整个 panel。Betanin 与 indicaxanthin 有可追溯 MPO/HOCl kinetics 和 LOX-FL 原始证据；历史 ORAC/TEAC 对 betalains 可能低响应，且需处理 inner-filter、self-fluorescence、pH transformation 与 quenching。Probetanin 缺 PubChem/InChIKey，触发 HUMAN REVIEW REQUIRED；本轮未静默修改 identity。输出为 assay-specific profile。''',
'Organosulfur_Redox_Profile_Report_CN.md':'''# Organosulfur Redox-Mechanism Profile 报告

冻结候选 15 个。系统检索显示，直接 capacity evidence 分散于羟自由基、Fenton、脂质链终止等不等价构念；sulforaphane 的核心为 KEAP1 cysteine sensing/NRF2，allicin 兼具 Fenton suppression、thiol exchange 与非水相 chain-breaking kinetics。因此不生成 ORAC TopN，也不平均不同 assays。S-allyl-L-cysteine 与 diallyl disulfide 的原始 hydroxyl-radical kinetics 保留为 profile。Normal dietary relevance 标为 unresolved 的候选继续触发 HUMAN REVIEW REQUIRED。''',
'Other_Aqueous_Phytochemicals_TopN_Report_CN.md':'''# Other Aqueous Phytochemicals 分层结果

冻结候选 26 个。机制异质性要求拆分：H-ORAC-compatible subpanel 输出 Top available 5，依次为 zingerone 3.85、eugenol 1.811、tyrosol 1.131、carvacrol 0.829、thymol 0.545 mol TE/mol，均为 single-study Low/Fragile。Hydroxytyrosol、oleuropein、curcumin、plumbagin 与 juglone进入 mechanism/prooxidant profile，不与 H-ORAC 数值混排。Ubiquinone-10 的 aqueous-scope 合理性触发 HUMAN REVIEW REQUIRED，本轮未修改冻结候选。'''
}
for n,t in reports.items():(DOCS/n).write_text(t+'\n',encoding='utf-8')

status={
'03_stilbenes_lignans':('15','2','H-ORAC-FL','Top available 2','13 candidates lack eligible A/B1; parent-lignan coverage is sparse.'),
'04_water_soluble_vitamins':('2','1','H-ORAC-FL','Singleton / percentile not informative','Dehydroascorbic acid is a context node, not an equivalent capacity competitor.'),
'05_betalains':('11','0','LOX-FL and MPO/HOCl kinetic profile','Profile only','Optical/pH interference and heterogeneous nitrogen-containing candidates prevent one rank.'),
'06_organosulfur':('15','0','KEAP1/NRF2, thiol and radical-kinetic profile','Profile only','Direct-capacity constructs are sparse and non-equivalent.'),
'07_other_aqueous_phytochemicals':('26','5','H-ORAC-FL subpanel plus mechanism profiles','Top available 5 + profile','Mechanistic heterogeneity and aqueous-scope risks prevent a single 26-candidate rank.'),
'08_metal_chelation':('NA','NA','chelation/reduction/Fenton/net endpoint','Evidence profile','Assay values and metal states are not a common scale.'),
'09_micronutrients':('7','NA','cofactor/deficiency/supplementation/prooxidant profile','Profile only','Minerals are not ORAC competitors.')}
for folder,(n,r,pc,out,gap) in status.items():
 p=FIG/folder/'Class_Status_Summary.md';p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text(f'# Class status\n\n- Candidate N: {n}\n- Rankable N: {r}\n- Primary construct: {pc}\n- Output: {out}\n- Main evidence gap: {gap}\n',encoding='utf-8')
(FIG/'99_methods_qc'/'Class_Status_Summary.md').write_text('# Methods/QC status\n\nContains method-governance outputs; no antioxidant ranking is generated in this folder. A/B1/B2/C/X, identity, independence, optical and conversion rules remain active.\n',encoding='utf-8')

active=['Polyphenols - Flavonoids','Polyphenols - Phenolic acids / conjugates','Polyphenols - Stilbenes / lignans','Vitamins / vitamin-like','Betalains / nitrogen-containing','Organosulfur compounds','Other food-derived redox-active phytochemicals']
rankN=sup.groupby('analysis_panel').rankable_N.max().to_dict()
summary=[]
for panel in active:
 n=len(c[c.analysis_panel.eq(panel)]); rn=rankN.get(panel,0)
 top='; '.join(sup[sup.analysis_panel.eq(panel)].sort_values('within_class_rank').compound.head(5)) or 'Profile only'
 if panel=='Betalains / nitrogen-containing': pc='LOX-FL + MPO/HOCl profile';out='Profile only';statusx='Optical/interference-limited'
 elif panel=='Organosulfur compounds':pc='causal redox/thio-reactivity profile';out='Profile only';statusx='No common direct-capacity scale'
 elif panel=='Other food-derived redox-active phytochemicals':pc='H-ORAC-FL coherent subpanel + profiles';out=f'Top available {int(rn)} + profile';statusx='Mechanistically split'
 else: pc='H-ORAC-FL';out=('Top20' if rn>=20 else f'Top available {int(rn)}');statusx='Provisional literature-derived'
 summary.append([panel,n,int(rn),out,pc,top,statusx])
tab=pd.DataFrame(summary,columns=['Class','Candidate N','Rankable N','Output','Primary construct','Top candidates','Evidence status'])
doi_n=papers.DOI.notna().sum(); total=len(papers)
headers=list(tab.columns)
table_md='| '+' | '.join(headers)+' |\n|'+ '|'.join(['---']*len(headers))+'|\n'
for _,rr in tab.iterrows(): table_md+='| '+' | '.join(str(rr[h]) for h in headers)+' |\n'
md=f'''# Supervisor Aqueous Ranking Progress — Stage 24

## 当前范围与结论

Stage 24 以 Stage 23 冻结的 157 个 aqueous candidates 为固定分母，没有新增、删除、合并或重命名候选。Flavonoids、phenolic acids/conjugates 与 vitamin C 沿用已完成排名并完成一致性复核；stilbenes/lignans 形成 Top available 2；other phytochemicals 拆出 Top available 5 H-ORAC-compatible subpanel；betalains 与 organosulfur 因构念和方法不可比而输出 profile。Metal mechanisms 与 micronutrients 单独 profile，不产生 ORAC rank。

{table_md}

统一证据主表目前 {len(ev)} 行；paper summary 为 {total} 个 DOI/source units，其中 {doi_n} 个记录 DOI。Stage 24 新类别数值排名仍全部为 B1 single-study，因此 high raw value 不等于稳定证据。现有 Flavonoid Top20、Phenolic acids Top available 18 和 Vitamin C singleton 没有因本轮检索被静默改写。

## Metal ions 与 micronutrients

Metal layer 按 binding/chelation、metal reduction、Fenton/Fenton-like suppression 和 net oxidative endpoint 分开。Quercetin/luteolin 的 iron-ATP suppression、quercetin–Cu Fenton context、isorhamnetin 的 Fe/Cu reversal 与 allicin Fenton/thiol evidence均作为 profile，不转换成 capacity score。Micronutrient v2 覆盖 Se、Zn、Mn、Cu、Fe、Mg、Mo；Se/Zn保留正、负或条件性人体证据，Fe/Cu明确记录过量促氧化风险。

## HUMAN REVIEW REQUIRED

- Podophyllotoxin：normal-dietary gate 与 aqueous scope。
- Probetanin：PubChem CID/InChIKey 缺失。
- Ubiquinone-10：aqueous-scope 合理性。
- Betalain pigment records：光学/pH QC 是否足以支持任何未来 direct rank。
- Organosulfur unresolved dietary gates：不得自动升级。
- Metal records：Fe/Cu oxidation state、chelation/reduction/net endpoint需第二研究者核对。
- 新类别全部 quantitative ranks 为 single-study，接近任何未来 cutoff 时不得冻结 Top20。

## Sync to ChatGPT

**A. active classes：**7 organic/nutrient panels plus metal and micronutrient profiles。**B. total candidate N：**157 frozen。**C. completed ranking classes/subpanels：**Flavonoids、Phenolic acids/conjugates、Vitamin C、Stilbenes/lignans H-ORAC、Other-phytochemical H-ORAC subpanel。**D. profile-only：**Betalains、Organosulfur、Metal、Micronutrients。**E/F. rankable N and outputs：**见表。**G. constructs：**class-specific；无 composite。**H. top candidates：**见表。**I/J. confidence：**新排名记录均 Low/Fragile single-study；既有三 panel 保留原 confidence。**K/L. DOI：**见 evidence master/paper summary；legacy figure-only source仍 unresolved。**M. metal：**8 条 curated mechanism records。**N. micronutrients：**7-row v2 profile。**O/P. figures：**统一目录已填充且无无说明空文件夹。**Q. human review：**见上。**R. readiness：**导师阶段汇报 package ready；不代表适合 global score 或 target mapping。
'''
(DOCS/'Supervisor_Aqueous_Ranking_Progress_CN.md').write_text(md,encoding='utf-8')

index='''# Aqueous Antioxidant Atlas Figure Index\n\n| Folder / figure | Purpose | Source data | Primary construct | Interpretation | Major caveat |\n|---|---|---|---|---|---|\n| 00_overview/Aqueous_All_Classes_Ranking_Overview.png | ranked panels side by side | Supervisor_Aqueous_Class_Ranking_Overview.csv | within-panel percentile | positional overview only | not global antioxidant magnitude |\n| 00_overview/Aqueous_Class_Coverage_Overview.png | candidate/rankable/display coverage | candidate master + overview | coverage | shows evidence gaps | count is not strength |\n| 00_overview/Aqueous_Primary_Literature_Coverage.png | paper-role coverage | paper summary | provenance | DOI/source density | popularity bias |\n| 00_overview/Aqueous_Evidence_Confidence_Overview.png | confidence distribution | supervisor overview | confidence | separates magnitude/depth | new panels mostly Fragile |\n| 00_overview/Aqueous_Metal_Redox_Framework.png | metal dual roles | metal + micronutrient profiles | mechanism | chelation/cofactor/prooxidant paths | no common numeric scale |\n| 03_stilbenes_lignans/Stilbenes_Lignans_TopN.png | Top available 2 | Stilbenes_Lignans_TopN_v1.0.csv | H-ORAC-FL | provisional within-class values | single-study |\n| 05_betalains/Betalains_Profile_Comparison.png | construct profile | Betalains_Nitrogen_Profile_Evidence.csv | LOX-FL/MPO/HOCl | assay-specific profile | pigment interference |\n| 06_organosulfur/Organosulfur_Redox_Mechanism_Profile.png | mechanism evidence | Organosulfur_Redox_Profile.csv | KEAP1/thiol/radical | no forced ORAC rank | heterogeneous constructs |\n| 07_other_aqueous_phytochemicals/Other_Aqueous_TopN.png | H-ORAC subpanel | Other_Aqueous_Phytochemicals_TopN_v1.0.csv | H-ORAC-FL | Top available 5 | single-study |\n| 08_metal_chelation/*.png | metal evidence profiles | Aqueous_Metal_Redox_Evidence.csv | metal-specific | binding/reduction/net effect | assays not pooled |\n| 09_micronutrients/*.png | cofactor and risk profiles | Antioxidant_Micronutrient_Redox_Profile_v2.csv | nutrient profile | no ORAC rank | status/dose dependent |\n'''
(FIG/'FIGURE_INDEX_CN.md').write_text(index,encoding='utf-8')
