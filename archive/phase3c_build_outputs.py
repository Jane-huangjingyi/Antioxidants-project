import csv, math
from pathlib import Path
from datetime import date

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'; DOCS=ROOT/'docs'
TODAY='2026-09-18'

def readcsv(p):
    with open(p,encoding='utf-8-sig',newline='') as f: return list(csv.DictReader(f))
def writecsv(p, rows, fields):
    p.parent.mkdir(parents=True,exist_ok=True)
    with open(p,'w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore'); w.writeheader(); w.writerows(rows)
def md(p,s): p.write_text(s.strip()+"\n",encoding='utf-8')

master=[r for r in readcsv(DATA/'Antioxidant_Class_Candidate_Master.csv') if r['analysis_panel']=='Carotenoids']
byid={r['candidate_id']:r for r in master}

subtype=lambda r: 'Carotene' if r['subclass']=='Carotenes' else 'Xanthophyll'
lock=[]
for r in master:
    hold=[]
    if r['compound'] in {'Astaxanthin','Fucoxanthin'}: hold.append('normal dietary relevance requires investigator confirmation; marine/special-food or supplement-dominant exposure may alter the gate')
    status='hold' if hold else 'yes'
    lock.append(dict(candidate_id=r['candidate_id'],compound=r['compound'],canonical_name=r['canonical_name'],PubChem_CID=r['PubChem_CID'],InChIKey=r['InChIKey'],subclass=r['subclass'],carotene_or_xanthophyll=subtype(r),cis_trans_status=r['isomer_status'],stereochemistry=r['stereochemistry'],food_source=r['representative_food_sources'],food_occurrence_reference=r['food_occurrence_reference'],normal_dietary_relevance='unresolved' if hold else 'yes',identity_verified='yes',food_occurrence_verified='pending second review' if hold else 'candidate-level source verification required',ranking_eligible=status,hold_reason='; '.join(hold),reviewer='Codex initial curation; human second review required',review_date=TODAY,notes='Generic historical names must not be mapped to a defined cis/trans candidate unless the paper resolves the form.'))
lock_fields=list(lock[0])
writecsv(DATA/'Carotenoid_Phase3_Eligibility_Lock.csv',lock,lock_fields)

# Direct kq records. Values are normalized to 10^9 M^-1 s^-1. B1 is exploratory,
# and each row remains environment-specific. Numeric values were cross-checked against
# the original-paper metadata and accessible authoritative reproductions of the cited table.
records=[]
def rec(eid,cid,exp,study,year,journal,pmid,doi,loc,val,solvent,polarity,system,sens,temp,tier,rationale,notes='',isomer='verified'):
    c=byid[cid]
    records.append(dict(evidence_id=eid,candidate_id=cid,compound=c['compound'],subclass=c['subclass'],cis_trans_status=c['isomer_status'],independent_experiment_id=exp,study=study,year=year,journal=journal,PMID=pmid,DOI=doi,Zotero_key='pending_local_import',exact_location=loc,original_kq_value=val,original_unit='10^9 M^-1 s^-1',normalized_kq_value=val,solvent=solvent,solvent_polarity_context=polarity,micelle_or_liposome=system,membrane_model='',photosensitizer=sens,oxygen_condition='singlet oxygen; air/oxygen condition as reported',temperature=temp,carotenoid_concentration='see original article',aggregation_control='spectral/concentration behavior considered where reported',purity='see original article',optical_QC='direct/near-IR singlet-oxygen decay or validated chemical generation; inspect original details',isomer_verified=isomer,tier=tier,tier_rationale=rationale,independence_status='independent publication/experiment',reviewer='Codex extraction; human second review required',verification_status='source and value cross-checked; full-text table verification required before Tier A',notes=notes,prooxidant_context_known='yes',prooxidant_condition='oxygen partial pressure and concentration can alter carotenoid radical behavior; not measured by this kq record',prooxidant_source='Young & Lowe 2001; Böhm et al. 2012',prooxidant_relevance='translation/safety context; does not change chemical kq rank'))

common='Direct singlet-oxygen quenching value extractable; identity and homogeneous organic environment defined; no unresolved severe artifact identified; metadata insufficient for Tier A.'
rec('CAR-SO-001','AFF-0116','CAR-EXP-1989-DM','Lycopene as the most efficient biological carotenoid singlet oxygen quencher','1989','Archives of Biochemistry and Biophysics','2802626','10.1016/0003-9861(89)90467-0','Abstract/results: lycopene and beta-carotene kq',31.0,'ethanol:chloroform:water 50:50:1','mixed organic with trace water','homogeneous organic solvent','NDPO2 thermodissociation','room temperature','B1',common)
rec('CAR-SO-002','AFF-0114','CAR-EXP-1989-DM','Lycopene as the most efficient biological carotenoid singlet oxygen quencher','1989','Archives of Biochemistry and Biophysics','2802626','10.1016/0003-9861(89)90467-0','Abstract/results: lycopene and beta-carotene kq',14.0,'ethanol:chloroform:water 50:50:1','mixed organic with trace water','homogeneous organic solvent','NDPO2 thermodissociation','room temperature','B1',common)
for eid,cid,val in [('003','AFF-0115',19.0),('004','AFF-0123',21.0),('005','AFF-0120',10.0),('006','AFF-0119',8.0)]:
    rec('CAR-SO-'+eid,cid,'CAR-EXP-1990-DM','Carotenoids, tocopherols and thiols as biological singlet molecular oxygen quenchers','1990','Biochemical Society Transactions','2088803','10.1042/bst0181054','Results/rank series; numerical series cross-checked to cited original dataset',val,'ethanol:chloroform:water 50:50:1','mixed organic with trace water','homogeneous organic solvent','NDPO2 thermodissociation','37 C / verify in full text','B1',common,'Classic same-study comparative series; retain as exploratory until full-text method fields receive second review.')
for eid,cid,val in [('007','AFF-0116',17.0),('008','AFF-0114',13.0),('009','AFF-0115',12.0),('010','AFF-0120',12.6),('011','AFF-0119',6.64),('012','AFF-0129',8.99)]:
    rec('CAR-SO-'+eid,cid,'CAR-EXP-1991-CONN','The singlet oxygen and carotenoid interaction','1991','Journal of Photochemistry and Photobiology B','1791493','10.1016/1011-1344(91)80266-K','Original results/table; values reproduced in Edge et al. 2018 tables',val,'benzene/toluene','nonpolar organic solvent','homogeneous organic solvent','sensitized time-resolved luminescence','room temperature','B1',common,'Solvent viscosity affects kq; do not pool with membrane values.',isomer='verified' if cid=='AFF-0129' else 'reported form accepted; second review')
rec('CAR-SO-013','AFF-0117','CAR-EXP-2020-ASH','Phytofluene as a Highly Efficient UVA Photosensitizer of Singlet Oxygen Generation','2020','Biochemistry (Moscow)','33040721','10.1134/S0006297920070056','Abstract: dark quenching rate constant',0.004,'organic solution; verify exact solvent in full text','organic solvent','homogeneous organic solvent','photosensitized phosphorescence','verify in full text','B1',common,'Also evaluated as a UVA photosensitizer; dark kq retained, photogeneration risk flagged.')
rec('CAR-SO-014','AFF-0118','CAR-EXP-2020-ASH','Phytofluene as a Highly Efficient UVA Photosensitizer of Singlet Oxygen Generation','2020','Biochemistry (Moscow)','33040721','10.1134/S0006297920070056','Abstract: dark quenching rate constant',0.020,'organic solution; verify exact solvent in full text','organic solvent','homogeneous organic solvent','photosensitized phosphorescence','verify in full text','B1',common,'Strong UVA singlet-oxygen photosensitization was reported; dark quenching does not imply net photoprotection.')
rec('CAR-SO-015','AFF-0122','CAR-EXP-1990-DM','Carotenoids, tocopherols and thiols as biological singlet molecular oxygen quenchers','1990','Biochemical Society Transactions','2088803','10.1042/bst0181054','Results/rank series; dietary gate unresolved',24.0,'ethanol:chloroform:water 50:50:1','mixed organic with trace water','homogeneous organic solvent','NDPO2 thermodissociation','37 C / verify in full text','B1',common,'Candidate remains on dietary-gate hold and is excluded from ranking.')
fields=list(records[0])
writecsv(DATA/'Carotenoid_Singlet_Oxygen_Evidence_Master.csv',records,fields)

# Aggregate only ranking-eligible compounds, using organic-solvent A/B1.
eligible_ids={r['candidate_id'] for r in lock if r['ranking_eligible']=='yes'}
groups={}
for r in records:
    if r['candidate_id'] in eligible_ids and r['tier'] in {'A','B1'} and r['micelle_or_liposome']=='homogeneous organic solvent': groups.setdefault(r['candidate_id'],[]).append(r)
top=[]
for cid,rs in groups.items():
    vals=sorted(float(r['normalized_kq_value']) for r in rs); n=len(vals); med=(vals[(n-1)//2]+vals[n//2])/2
    q1=q3='NA'
    if n>=4:
        lo=vals[:n//2]; hi=vals[(n+1)//2:]; q1=(lo[(len(lo)-1)//2]+lo[len(lo)//2])/2; q3=(hi[(len(hi)-1)//2]+hi[len(hi)//2])/2
    ratio=max(vals)/min(vals) if min(vals)>0 else math.inf
    confidence='High' if n>=3 and ratio<=2 else ('Moderate' if n>=2 and ratio<=2 else 'Low')
    hetero='high' if ratio>2 else ('moderate' if n>=2 and ratio>1.5 else 'low/not estimable')
    c=byid[cid]
    top.append(dict(compound=c['compound'],subclass=c['subclass'],cis_trans_status=c['isomer_status'],PubChem_CID=c['PubChem_CID'],primary_construct='direct singlet-oxygen quenching rate constant',primary_environment='homogeneous organic solvent (environment-stratified)',median_kq=med,min=min(vals),max=max(vals),IQR='NA' if q1=='NA' else q3-q1,unit='10^9 M^-1 s^-1',eligible_record_count=n,confidence=confidence,single_study_flag='yes' if n==1 else 'no',heterogeneity_flag=hetero,aggregation_risk='medium: solvent-dependent; no cross-environment pooling',optical_risk='low-to-moderate for direct decay methods; verify pigment absorbance/QC',prooxidant_context='oxygen pressure, concentration and radical context may reverse net effect',ranking_status='Top available (exploratory)' ,provenance_record_ids=';'.join(r['evidence_id'] for r in rs),caveat='Chemical kq in organic solvent; not membrane efficacy, human benefit, or a cross-class score.'))
top.sort(key=lambda r:float(r['median_kq']),reverse=True)
for i,r in enumerate(top,1): r['rank']=i
top_fields=['rank']+[k for k in top[0] if k!='rank']
writecsv(DATA/'Carotenoids_TopN_v1.0.csv',top,top_fields)

lipid=[]
def lip(c,typ,sys,end,val,unit,strength,comp,ref,notes): lipid.append(dict(compound=c,lipid_assay_type=typ,lipid_system=sys,endpoint=end,value=val,unit=unit,evidence_strength=strength,direct_comparability=comp,reference=ref,notes=notes))
ref='Cantrell et al. 2003, Arch Biochem Biophys, DOI 10.1016/S0003-9861(03)00014-6'
lip('all-trans-Lycopene','singlet-oxygen quenching','unilamellar DPPC liposomes','kq with aqueous/lipid sensitizer','2.4 / 2.3','10^9 M^-1 s^-1','primary original study','within this study only',ref,'Secondary membrane-relevant profile; much lower than organic-solvent kq.')
lip('all-trans-beta-Carotene','singlet-oxygen quenching','unilamellar DPPC liposomes','kq with aqueous/lipid sensitizer','2.3 / 2.5','10^9 M^-1 s^-1','primary original study','within this study only',ref,'Secondary membrane-relevant profile.')
for c in ['Lutein','Zeaxanthin','Canthaxanthin','Astaxanthin']:
    lip(c,'singlet-oxygen quenching','unilamellar DPPC liposomes','kq / Stern-Volmer behavior','reported; exact value pending full-text extraction','10^9 M^-1 s^-1','primary original study','not numerically pooled',ref,'Xanthophyll aggregation/localization affected response; zeaxanthin showed nonlinear behavior.' if c=='Zeaxanthin' else 'Secondary profile; exact table extraction required.')
writecsv(DATA/'Carotenoid_LipidPhase_Evidence_Profile.csv',lipid,list(lipid[0]))

# Global overview v0.2 preserves v0.1 rows and appends carotenoid Top available.
g=readcsv(DATA/'Global_Top_Overview_Master_v0.1.csv'); gf=list(g[0])
for prior in g: prior['overview_version']='v0.2'
for r in top:
    c=next(x for x in master if x['compound']==r['compound'])
    n=len(top); pct=round(100*(n-int(r['rank'])+1)/n,1)
    st='Stable' if r['confidence']=='High' and r['heterogeneity_flag']!='high' else ('Moderately stable' if r['confidence']=='Moderate' else 'Fragile')
    row={k:'Not reviewed' for k in gf}; row.update(overview_version='v0.2',parent_class='Carotenoids',analysis_panel='Carotenoids',subclass=r['subclass'],compound=r['compound'],canonical_name=c['canonical_name'],PubChem_CID=c['PubChem_CID'],InChIKey=c['InChIKey'],within_class_rank=r['rank'],within_class_N_rankable=n,within_class_percentile=pct,within_class_status='Top available',primary_construct=r['primary_construct'],primary_metric_name='singlet-oxygen kq',primary_value=r['median_kq'],primary_unit=r['unit'],eligible_record_count=r['eligible_record_count'],confidence=r['confidence'],single_study_flag=r['single_study_flag'],heterogeneity_flag=r['heterogeneity_flag'],identity_risk='cis/trans form must be record-specific; generic names not mapped to defined cis isomers',assay_risk='solvent, viscosity, aggregation and membrane localization',evidence_depth_category=('Moderate (2 independent eligible records)' if int(r['eligible_record_count'])==2 else 'Limited (1 independent eligible record)'),evidence_stability=st,major_caveat=r['caveat'],provenance_record_ids=r['provenance_record_ids'],dietary_exposure_umol_day='NA',exposure_source='Not reviewed',exposure_quality='Not reviewed',bioavailability_summary='Not reviewed',human_evidence_level='Not reviewed',direct_chemical_antioxidant_profile='Direct singlet-oxygen kq profile available',endogenous_defense_profile='Not reviewed',lipid_phase_activity='Secondary DPPC/lipid profile where available',singlet_oxygen_activity='Primary class-specific construct',NRF2_GSH_GPX_profile='Not reviewed',SOD_CAT_profile='Not reviewed',NOX_mitochondrial_ROS_profile='Not reviewed',ferroptosis_lipid_profile='Not reviewed',direct_target_level='Not reviewed',safety_prooxidant_context=r['prooxidant_context'],experimental_tractability='Not reviewed')
    g.append(row)
writecsv(DATA/'Global_Top_Overview_Master_v0.2.csv',g,gf)

# Stress-test revision: preserve dimensions, update data-status language only.
cm=readcsv(DATA/'Cross_Class_Comparability_Matrix_v0.1.csv'); cmf=list(cm[0])
for r in cm:
    if r['dimension']=='Singlet-oxygen quenching rate/value':
        r['current_data_status']='Phase 3C organic-solvent kq available for 9 carotenoids; not cross-class comparable'
        r['valid_unit_or_scale']='10^9 M^-1 s^-1 within a frozen carotenoid environment stratum'
    elif r['dimension'] in {'Eligible independent study count','Evidence confidence category','Within-class percentile','Evidence stability'}:
        r['current_data_status']='Complete for Phase 3A/3B and Phase 3C Top available'
writecsv(DATA/'Cross_Class_Comparability_Matrix_v0.2.csv',cm,cmf)

# Append human-review issues without overwriting prior rows.
hr=readcsv(DATA/'Human_Review_Log.csv'); hf=list(hr[0]); hr=[r for r in hr if r.get('stage')!='Phase 3C']
issues=[
('Astaxanthin','candidate master / eligibility lock','dietary gate','Normal dietary exposure versus supplement/special-food dominance is unresolved.','Keep on hold; exclude from ranking until a second reviewer verifies ordinary-food exposure.','Could add a high-kq candidate.'),
('Fucoxanthin','candidate master / eligibility lock','dietary gate','Normal dietary exposure depends on seaweed consumption context; supplement dominance varies.','Keep on hold pending population-context food-occurrence decision.','Could enter future marine-diet subanalysis.'),
('Defined cis beta-carotene/lycopene isomers','historical kq literature','isomer ambiguity','Generic carotenoid records cannot be assigned to 9-cis/13-cis candidates.','Use only form-resolved records; hold generic records at parent-name level.','Prevents erroneous cis-isomer ranks.'),
('Primary carotenoid environment','environment coverage audit','primary environment choice','Organic-solvent kq supports 9 rankable candidates; membrane/liposome quantitative coverage is too sparse for a parallel class list.','Use organic-solvent direct kq provisionally; retain membrane data as secondary and do not pool.','No competing adequately covered environment at this stage.'),
]
for c,src,it,desc,recmd,effect in issues:
    hr.append(dict(stage='Phase 3C',compound=c,source=src,issue_type=it,issue_description=desc,codex_recommendation=recmd,human_decision='pending',reviewer='',date=TODAY,effect_on_ranking=effect))
writecsv(DATA/'Human_Review_Log.csv',hr,hf)

md(DOCS/'Carotenoid_Singlet_Oxygen_Eligibility_Rules_CN.md',r'''# Carotenoid singlet-oxygen evidence eligibility rules

本规则只评价 direct singlet-oxygen quenching `kq` 记录的可比性与排名用途，不评价期刊质量、人体获益或总体生物学重要性。每行必须对应一个 compound × independent experiment × assay environment；不同环境不得默认合并。

**Tier A** 要求异构体身份、纯度、直接 ^1O2 decay/quenching 测量、`kq` 与单位、溶剂/膜环境、温度、photosensitizer 或 ^1O2 source、氧条件、浓度区间、aggregation/optical QC、原始表格位置和独立性均可核实，并且与目标 ranking stratum 的 protocol 高度一致。**Tier B1** 可进入 exploratory class ranking：身份与 isomer 足够明确，原始 `kq` 可提取并统一为 M^-1 s^-1，环境与主要生成/检测条件可判断，无严重未解决 aggregation/interference；允许少量次要 metadata 缺失。**Tier B2** 有定量值但环境、isomer、aggregation、检测方法或原始定位限制可比性，只能支持 profile/coverage。**Tier C** 为不兼容结果，例如仅报告 chemical bleaching、percent inhibition、radical assay、混合物或无法换算为 `kq`。**Tier X** 为信息不足，尚不能判级。

环境固定为五层：homogeneous organic solvent、aqueous micelle、liposome、membrane-like system、biological membrane/lipoprotein。当前 organic-solvent direct `kq` 是唯一覆盖足以形成 exploratory Top available 的层；DPPC liposome 数据只进入 secondary profile。若未来另一环境达到至少 10 个候选且 protocol comparability 相当，必须触发 **HUMAN REVIEW REQUIRED — PRIMARY CAROTENOID ENVIRONMENT**。

异构体规则：all-trans、9-cis、13-cis 分开；generic carotenoid name 不映射到项目中的 cis candidate。聚集、viscosity、光学吸收和膜定位必须记录。Astaxanthin、fucoxanthin 等 dietary gate 未冻结者即使有高 `kq` 也不得进入榜单。Tier 表示可比性，不代表该 compound 的健康价值。''')

md(DOCS/'Phase3C_Carotenoid_TopN_Report_CN.md',f'''# Phase 3C — Carotenoids Top-N report

本阶段从 Phase 2 master 锁定 19 个 carotenoid candidates，17 个暂可进入证据审计，astaxanthin 与 fucoxanthin 因正常膳食 gate 未冻结而 hold。类胡萝卜素的 primary construct 冻结为 direct singlet-oxygen physical quenching rate constant `kq`。H-ORAC-FL 与其疏水性、长共轭多烯及经典 ^1O2 physical quenching chemistry 不匹配，因此不作为本类主指标。

环境覆盖审计显示，homogeneous organic-solvent direct `kq` 可支持 9 个 ranking-eligible compounds；DPPC liposome/micelle 数据仅覆盖少数候选并存在 xanthophyll aggregation、膜定位和 nonlinear response，尚不能产生同等覆盖的第二套排名。因此当前采用 organic-solvent `kq` 作为 provisional primary environment，明确解释为 class-specific chemical quenching construct，不代表 biological membrane efficacy。不同有机溶剂记录只有在 B1 条件下才在 compound 内聚合；跨 organic/micelle/liposome 的数值不合并。

当前输出为 **Top available 9**，未达到 10 个可比候选，故不称 Top10。按 median `kq` 排列为：{', '.join(str(r['rank'])+'. '+r['compound'] for r in top)}。只有 lycopene、all-trans-beta-carotene、alpha-carotene、zeaxanthin 和 lutein 有两条 B1；其余为 single-study。Tier A=0，B1={sum(r['tier']=='B1' for r in records)}。该列表展示的是历史有机溶剂中报告的 quenching kinetics；它不说明膳食暴露、人体效果或跨类别“最强抗氧化剂”。

cis/trans QC 仍是关键限制。只有 9-cis-beta-carotene 获得 form-resolved record；generic beta-carotene 或 lycopene 记录未映射至 13-cis/9-cis candidates。Phytofluene 虽具有暗态 quenching `kq`，原研究同时报告 UVA 下显著 ^1O2 photosensitization，故不能把其数值解释为净 photoprotection。Carotenoid prooxidant behavior 还取决于氧分压、浓度、radical chemistry 和 matrix。

Secondary lipid profile 保留 Cantrell 等人的 DPPC liposome 研究。Lycopene 与 beta-carotene 在该模型的 `kq` 接近，且明显低于有机溶剂；xanthophylls 更受聚集和定位影响。这一结果说明 environment 是 construct 的组成部分，也支持禁止把 `kq` 与 L-ORAC、lipid-peroxidation endpoint 或摄入量做 composite score。

## HUMAN REVIEW REQUIRED — pause decision

Astaxanthin 与 fucoxanthin 的正常膳食 gate 尚未由第二研究者确认，因此相关 `kq` 不改变当前榜单；generic beta-carotene/lycopene 文献也不得映射到 9-cis/13-cis candidates。organic-solvent 层内部仍含 benzene 与 ethanol/chloroform/water 条件，本版只将其作为 B1 exploratory records；升级为 formal Tier A 或在 cutoff 附近作精细名次解释前，必须完成 full-text、温度、viscosity、isomer 与 aggregation 的双人复核。当前没有第二个达到相当候选覆盖的 primary environment，因此不构成 organic-solvent 与 membrane 两套排名之间的竞争；若膜层覆盖扩展到可排名规模，必须重新暂停并由研究者选择 primary environment。

## Sync to ChatGPT

A. Universe N=19；B. ranking eligible lock=17，实际有 primary A/B1 的候选=9；C. primary construct=direct singlet-oxygen quenching `kq`；D. primary environment=homogeneous organic solvent（provisional，因唯一达到足够覆盖）；E. evidence tiers=A 0、B1 {sum(r['tier']=='B1' for r in records)}，其中1条 astaxanthin 因 dietary hold 不进榜；F. 输出 Top available 9；G. confidence 为 Moderate 5、Low 4；H. single-study=4；I. generic cis/trans 记录不映射；J. xanthophyll aggregation 是主要风险；K. direct decay method 的 optical risk 低于颜色终点法，但仍需核对吸收与 sensitizer；L. prooxidant context 已独立记录；M. lipid-phase evidence 只做 profile；N. Global schema 可容纳不同 primary unit 与 percentile，但不能生成 unified score；O. 人工待决包括 astaxanthin/fucoxanthin dietary gate、cis identity 与 full-text second review；P. 推荐下一类为 Vitamins，先拆分 vitamin C aqueous construct 与 vitamin E lipid-phase construct。''')

md(DOCS/'Why_Different_Antioxidant_Classes_Require_Different_Assays_EN.md',r'''# Why Different Dietary Antioxidant Classes Require Different Primary Assays: A Mechanism- and Matrix-Aware Framework

## Core principle

A unified screening framework does not imply a universal antioxidant assay. The Atlas standardizes candidate eligibility, identity control, provenance, evidence tiers, independent-experiment rules, aggregation, confidence, dietary exposure, human evidence, target evidence, and safety review. It preserves class-specific primary constructs because an assay value is defined jointly by the reacting species, mechanism, phase, solvent or membrane environment, concentration, and readout.

Antioxidant capacity may describe hydrogen-atom transfer, electron transfer, peroxyl-radical chain breaking, singlet-oxygen quenching, lipid-oxidation inhibition, electrophile sensing, or enzyme-dependent redox defense. Solubility, aggregation, optical absorption, and matrix localization can change the observed response. Pooling these constructs by z scores or simple averages destroys their chemical meaning and creates an arbitrary result.

## Class-specific rationale

For many aqueous phenolic compounds, H-ORAC-FL is a reasonable primary chemical construct because it integrates inhibition of AAPH-derived peroxyl-radical oxidation of fluorescein over time. Values must be protocol-audited and expressed on a molar basis. H-ORAC does not measure bioavailability, cellular signaling, or clinical efficacy, and colored phenolics still require optical quality control (Ou et al., 2001; Huang et al., 2005; Prior et al., 2005).

Vitamin C is a water-soluble reducing antioxidant and radical scavenger that also participates in antioxidant-regeneration networks. Aqueous kinetic radical assays and reducing-capacity measurements can characterize parts of its chemistry, but no single value captures its recycling, transport, or compartmental biology (Frei et al., 1989; Padayatty and Levine, 2016).

Vitamin E acts mainly as a lipid-phase chain-breaking antioxidant. Membrane or lipoprotein lipid-peroxidation kinetics and validated lipophilic ORAC approaches are more appropriate than aqueous H-ORAC. Its function also depends on regeneration by other reductants (Niki, 2014).

Carotenoids are hydrophobic, highly conjugated polyenes. A central chemical function is physical quenching of singlet oxygen; direct quenching rate constants are therefore the preferred class-specific primary construct. Solvent viscosity, aggregation, cis/trans configuration, and membrane localization materially affect the result. Organic-solvent `kq` supports a chemical ranking, whereas liposome data describe a different, more membrane-relevant environment and must not be pooled with it (Di Mascio et al., 1989; Conn et al., 1991; Cantrell et al., 2003; Edge and Truscott, 2018).

Many organosulfur compounds are weak competitors in classical radical-scavenging assays because their major redox biology is electrophilic or thiol-reactive. For isothiocyanates such as sulforaphane, causal KEAP1–NRF2 and glutathione-system evidence is more informative than ORAC alone (Dinkova-Kostova et al., 2002).

Betalains can undergo direct radical chemistry, but their intense visible absorption, pH-dependent structure, and pigment behavior can interfere with optical assays. A primary method therefore requires wavelength-specific inner-filter, self-absorption, and blank controls; a nominally common assay is not comparable when these controls differ (Gandía-Herrero et al., 2010).

Mineral micronutrients are not small-molecule capacity competitors. Selenium supports selenoenzymes including glutathione peroxidases and thioredoxin reductases; copper, zinc, and manganese participate in superoxide dismutases. Their effects depend on nutritional status, protein incorporation, dose, and possible prooxidant chemistry. ORAC-based mineral ranking is chemically invalid (Brigelius-Flohé and Maiorino, 2013; Fukai and Ushio-Fukai, 2011).

## Why no composite antioxidant score is used

The framework rejects z-score pooling, simple assay averaging, `ORAC × intake`, and journal-impact-factor weighting. These operations combine quantities with different causal meanings, hide assay-specific missingness, and can reward publication density. Cross-class comparison instead uses dietary exposure, evidence confidence and stability, human evidence, pharmacokinetics, mechanism profiles, target evidence, safety/prooxidant context, and experimental tractability. Raw assay values remain within mechanistically coherent classes.

| Class | Dominant antioxidant construct | Preferred primary method | Secondary methods | Major assay risk | Cross-class interpretation |
|---|---|---|---|---|---|
| Flavonoids | aqueous peroxyl-radical chain breaking | audited H-ORAC-FL | CUPRAC; lipid oxidation; cellular redox | protocol and optical heterogeneity | compare class rank and evidence profile |
| Phenolic acids | aqueous peroxyl-radical chain breaking | audited H-ORAC-FL | CUPRAC; radical and lipid assays | ionization, conjugate identity, protocol variation | compare class rank and evidence profile |
| Vitamin C | aqueous reducing/radical network | aqueous kinetic/reducing construct | regeneration and biological redox assays | instability and recycling context | use exposure, PK, and profile |
| Vitamin E | lipid-chain termination | lipid-peroxidation kinetics or validated L-ORAC | membrane/lipoprotein oxidation | phase and regeneration dependence | use lipid profile and translational dimensions |
| Carotenoids | physical singlet-oxygen quenching | direct `kq`, environment-stratified | liposome/LDL oxidation; L-ORAC | solvent, aggregation, cis/trans, localization | use within-environment class rank |
| Organosulfur | electrophile/thiol signaling | causal KEAP1/NRF2 or GSH-system evidence | redox biomarkers; selected chemical assays | classical assays miss regulatory chemistry | compare mechanism and human relevance |
| Betalains | pigment radical chemistry | optically controlled kinetic assay | orthogonal radical/lipid assays | inner-filter and self-absorption | compare QC-qualified profile |
| Minerals | enzyme-cofactor biology | status- and enzyme-specific evidence | human status and safety evidence | dose-dependent prooxidant effects | no chemical-capacity rank |

The aim of the Atlas is not to force chemically distinct antioxidant classes onto a single numerical scale, but to rank compounds rigorously within mechanistically coherent classes and then compare those class leaders using shared translational dimensions.

## Key Methodological References

- Ou B, Hampsch-Woodill M, Prior RL. 2001. Development and validation of an improved ORAC assay using fluorescein. *Journal of Agricultural and Food Chemistry*. DOI: 10.1021/jf010586o. PMID: 11599998. Role: ORAC-FL method.
- Huang D, Ou B, Prior RL. 2005. The chemistry behind antioxidant capacity assays. *Journal of Agricultural and Food Chemistry*. DOI: 10.1021/jf030723c. PMID: 15769103. Role: construct distinction.
- Prior RL, Wu X, Schaich K. 2005. Standardized methods for antioxidant capacity and phenolics. *Journal of Agricultural and Food Chemistry*. DOI: 10.1021/jf0502698. PMID: 15884874. Role: assay standardization limits.
- Di Mascio P, Kaiser S, Sies H. 1989. Lycopene as the most efficient biological carotenoid singlet oxygen quencher. *Archives of Biochemistry and Biophysics*. DOI: 10.1016/0003-9861(89)90467-0. PMID: 2802626. Role: direct carotenoid `kq`.
- Conn PF, Schalch W, Truscott TG. 1991. The singlet oxygen and carotenoid interaction. *Journal of Photochemistry and Photobiology B*. DOI: 10.1016/1011-1344(91)80266-K. PMID: 1791493. Role: solvent and isomer effects.
- Cantrell A et al. 2003. Singlet oxygen quenching by dietary carotenoids in a model membrane environment. *Archives of Biochemistry and Biophysics*. DOI: 10.1016/S0003-9861(03)00014-6. Role: membrane environment and aggregation.
- Edge R, Truscott TG. 2018. Singlet oxygen and free radical reactions of retinoids and carotenoids—A review. *Antioxidants*. DOI: 10.3390/antiox7010005. PMID: 29301239. Role: environment-dependent carotenoid chemistry.
- Frei B et al. 1989. Ascorbate is an outstanding antioxidant in human blood plasma. *Proceedings of the National Academy of Sciences USA*. PMID: 2762330. Role: aqueous vitamin C chemistry.
- Niki E. 2014. Role of vitamin E as a lipid-soluble peroxyl radical scavenger. *Free Radical Biology and Medicine*. DOI: 10.1016/j.freeradbiomed.2014.03.022. PMID: 24681041. Role: lipid-chain termination.
- Dinkova-Kostova AT et al. 2002. Direct evidence that sulfhydryl groups of Keap1 are the sensors regulating induction of phase 2 enzymes. *Proceedings of the National Academy of Sciences USA*. DOI: 10.1073/pnas.172398899. PMID: 12193649. Role: electrophile/KEAP1 mechanism.
- Brigelius-Flohé R, Maiorino M. 2013. Glutathione peroxidases. *Biochimica et Biophysica Acta*. DOI: 10.1016/j.bbagen.2012.11.020. PMID: 23201771. Role: selenium-dependent enzyme biology.
- Fukai T, Ushio-Fukai M. 2011. Superoxide dismutases: role in redox signaling, vascular function, and diseases. *Antioxidants & Redox Signaling*. DOI: 10.1089/ars.2011.3999. PMID: 21473702. Role: metal-dependent SOD biology.
''')

# Update schema document with a non-H-ORAC stress-test section, preserving prior text.
schema=DOCS/'Global_Top_Overview_Schema_Pilot_CN.md'
txt=schema.read_text(encoding='utf-8')
marker='## Non-H-ORAC stress test'
if marker not in txt:
    txt += r'''

## Non-H-ORAC stress test

Carotenoids 是第一个使用 direct singlet-oxygen `kq` 而不是 H-ORAC-FL 的 panel。`Global_Top_Overview_Master_v0.2.csv` 证明既有 schema 可保存不同 primary construct、value 与 unit；within-class percentile 仍然只依赖类内 rank，因此可工作；confidence 和 stability 也仍由证据深度、异质性与 identity/assay risk 产生，不要求共同 assay。需要修订的是 comparability 解释：primary raw value 与 primary unit 必须明确标记为 **not directly comparable across classes**，而 percentile 只允许并列展示，不能解释为效应大小等距。此次 stress test 进一步证明无法建立 unified antioxidant score。Carotenoid organic-solvent `kq`、polyphenol H-ORAC-FL、未来 lipid-phase 或 causal regulatory evidence 应保留各自 construct，再通过 shared translational fields 做 profile comparison。
'''
    schema.write_text(txt,encoding='utf-8')

print({'universe':len(master),'eligible_lock':sum(x['ranking_eligible']=='yes' for x in lock),'records':len(records),'top_available':len(top),'global_v02':len(g)})
