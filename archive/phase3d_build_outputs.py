import csv, statistics
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]; DATA=ROOT/'data'; DOCS=ROOT/'docs'; TODAY='2026-09-18'
def readcsv(p):
    with open(p,encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def writecsv(p,rows,fields):
    p.parent.mkdir(parents=True,exist_ok=True)
    with open(p,'w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');w.writeheader();w.writerows(rows)
def md(p,s):p.write_text(s.strip()+"\n",encoding='utf-8')

master=[r for r in readcsv(DATA/'Antioxidant_Class_Candidate_Master.csv') if r['parent_class']=='Vitamins / vitamin-like antioxidants']
byid={r['candidate_id']:r for r in master}

lock=[]
for r in master:
    aq=r['subclass']=='Water-soluble antioxidant vitamins'; sub='Vitamins–aqueous antioxidant' if aq else 'Vitamins–lipid-phase antioxidant'
    hold=''
    eligible='yes'
    dietary_form='L-ascorbic acid dietary vitamer' if r['compound']=='L-Ascorbic acid' else ('oxidized vitamin C vitamer; not interchangeable with ascorbate' if r['compound']=='Dehydroascorbic acid' else 'natural dietary R-configured vitamer; exact stereochemistry must match source')
    nat='natural dietary form; synthetic/all-rac records excluded unless mapped separately'
    if r['compound']=='Dehydroascorbic acid':
        eligible='hold';hold='No comparable primary aqueous-capacity record and oxidized form is not interchangeable with L-ascorbic acid; retain as mechanistic/dietary vitamer context.'
    lock.append(dict(candidate_id=r['candidate_id'],compound=r['compound'],canonical_name=r['canonical_name'],PubChem_CID=r['PubChem_CID'],InChIKey=r['InChIKey'],vitamin_subpanel=sub,natural_or_synthetic=nat,stereochemistry=r['stereochemistry'],dietary_form=dietary_form,representative_food_sources=r['representative_food_sources'],food_occurrence_reference=r['food_occurrence_reference'],normal_dietary_relevance='yes',identity_verified='yes; second-review pending for record-level stereochemistry',food_occurrence_verified='candidate-level second review pending',ranking_eligible=eligible,hold_reason=hold,reviewer='Codex initial curation; human second review required',review_date=TODAY,notes='Generic vitamin E records and synthetic all-rac-alpha-tocopherol are not mapped to natural vitamer candidates.'))
writecsv(DATA/'Vitamin_Phase3_Eligibility_Lock.csv',lock,list(lock[0]))

vc=[]
def vcr(eid,exp,study,year,journal,pmid,doi,zotero,loc,val,aaph,fl,trox,buffer,temp,solvent,notes):
    vc.append(dict(evidence_id=eid,compound='L-Ascorbic acid',chemical_form='free L-ascorbic acid',independent_experiment_id=exp,study=study,year=year,journal=journal,PMID=pmid,DOI=doi,Zotero_key=zotero,exact_location=loc,primary_construct_candidate='H-ORAC-FL kinetic peroxyl-radical chain-breaking capacity',original_value=val,original_unit='mol TE/mol compound',normalized_value=val,assay='H-ORAC-FL',radical_or_redox_system='AAPH-derived peroxyl radical / fluorescein oxidation',solvent=solvent,pH='7.4',temperature=temp,Trolox_or_reference=trox,purity='supplier/reagent grade; numerical purity not reported',interference_QC='method-level fluorescence controls; no unresolved compound optical concern',tier='B1',tier_rationale='Defined pure compound; original ORAC-FL value; AAPH/fluorescein/Trolox and major conditions identifiable; molar unit directly comparable for exploratory use.',reviewer='Codex extraction; human second review required',verification_status='original paper and exact table location verified',notes=notes,AAPH_concentration=aaph,fluorescein_concentration=fl,buffer=buffer,concentration_range='see exact source location',linearity='reported at method/compound level'))
vcr('VTC-E001','VTC-EXP-2001-OU','Development and validation of an improved ORAC assay using fluorescein as the fluorescent probe','2001','Journal of Agricultural and Food Chemistry','11599998','10.1021/jf010586o','4FIGEV33','Table 4 p.4622; methods pp.4619-4620',0.95,'12.8 mM final','48 nM','Trolox 12.5–100 µM','75 mM potassium phosphate','37 C','50:50 acetone/water stock diluted with buffer','Historical B1 value; formal Tier A not claimed.')
vcr('VTC-E002','VTC-EXP-2023-CARVALHO','Exploiting kinetic features of ORAC assay for evaluation of radical scavenging capacity','2023','Antioxidants','36829987','10.3390/antiox12020505','EHLKNP4E','Table 3; Methods 2.1–2.3; Table 1',0.53,'12 mM final well','35 nM','Trolox 2–10 µM','75 mM phosphate','37 C','buffer','Historical B1 value; protocol duration differs from Ou 2001.')
writecsv(DATA/'VitaminC_Aqueous_Evidence_Master.csv',vc,list(vc[0]))
vals=[float(x['normalized_value']) for x in vc]; med=statistics.median(vals)
vcrank=[dict(rank=1,compound='L-Ascorbic acid',chemical_form='defined L-vitamer',primary_construct='H-ORAC-FL kinetic peroxyl-radical chain-breaking capacity',primary_value=med,unit='mol TE/mol compound',eligible_record_count=2,confidence='Moderate',stability='Moderately stable',within_subpanel_percentile='NA',percentile_status='single eligible candidate / percentile not informative',caveat='Two broadly comparable historical protocols; value is chemical capacity, not human efficacy. Dehydroascorbic acid is not substituted or assigned zero.',provenance_record_ids='VTC-E001;VTC-E002')]
writecsv(DATA/'VitaminC_TopAvailable_v1.0.csv',vcrank,list(vcrank[0]))

# Vitamin E: primary values are direct peroxyl-radical trapping rate constants in homogeneous organic solution.
# Corresponding tocopherol/tocotrienol homologues were shown to have the same radical reactivity by Yoshida et al. 2003.
kinh={'alpha':3.2e6,'beta':1.3e6,'gamma':1.4e6,'delta':4.4e5}
ve=[]
for r in master:
    if r['subclass'] not in {'Tocopherols','Tocotrienols'}:continue
    vit=r['compound'].split('-')[0].lower(); is_t3=r['subclass']=='Tocotrienols'
    eid='VTE-E'+str(len(ve)+1).zfill(3)
    ve.append(dict(evidence_id=eid,compound=r['compound'],vitamer=vit,stereochemistry=r['stereochemistry'],independent_experiment_id='VTE-EXP-1983-BURTON+2003-YOSHIDA' if is_t3 else 'VTE-EXP-1983-BURTON',study='Comparative radical-trapping kinetics; corresponding tocopherol/tocotrienol reactivity confirmation' if is_t3 else 'Vitamin E as an antioxidant in vitro and in vivo',year='1983; 2003' if is_t3 else '1983',journal='Ciba Foundation Symposium; Chemistry and Physics of Lipids' if is_t3 else 'Ciba Foundation Symposium',PMID='6557906;12637165' if is_t3 else '6557906',DOI='10.1002/9780470720820.ch2;10.1016/S0009-3084(02)00164-0' if is_t3 else '10.1002/9780470720820.ch2',Zotero_key='pending_local_import',exact_location='Burton absolute-rate-constant table, cross-checked in Niki 2023 Table 2; Yoshida 2003 Fig.1 and pp.65–66 for corresponding tocotrienol equivalence' if is_t3 else 'Absolute-rate-constant results; cross-checked in Niki 2023 Table 2',assay_type='inhibited autoxidation / direct radical-trapping kinetics',primary_construct_candidate='peroxyl-radical chain-breaking rate constant k_inh',original_value=kinh[vit],original_unit='M^-1 s^-1',normalized_value=kinh[vit],lipid_system='styrene autoxidation homogeneous organic solution',solvent='nonpolar homogeneous solution; exact original conditions required for Tier A',oxygen_condition='oxygenated/autoxidation system',temperature='30 C',concentration='see original paper',chain_initiator='peroxyl radicals from autoxidation / radical initiator',endpoint='absolute second-order rate constant for H-atom transfer to peroxyl radical',aggregation_or_partition_issue='minimal in homogeneous solution; does not model membrane partition',tier='B1',tier_rationale='Defined natural vitamer; quantitative k_inh and unit traceable; homogeneous environment defined. Tocotrienol value uses experimentally supported corresponding-homologue equivalence and remains exploratory.',reviewer='Codex extraction; human second review required',verification_status='numeric rate cross-checked; tocotrienol homolog mapping requires second review' if is_t3 else 'numeric rate cross-checked; original full-text table second review pending',notes='Natural dietary form only. This chemical kinetic value must not be interpreted as in-vivo vitamin activity or membrane uptake.',prooxidant_context_known='yes',prooxidant_condition='Cu(II)/methyl-linoleate SDS micelles for alpha forms; regeneration-poor lipid systems may permit tocopheroxyl propagation',prooxidant_evidence_type='direct model-system experiment / mechanistic literature',prooxidant_relevance='context field; does not alter primary k_inh rank',prooxidant_source='Yoshida et al. 2003; Mukai 2005'))
writecsv(DATA/'VitaminE_LipidPhase_Evidence_Master.csv',ve,list(ve[0]))

ve_top=[]
for r in ve:
    c=next(x for x in master if x['compound']==r['compound'])
    ve_top.append(dict(compound=r['compound'],vitamer=r['vitamer'],tocopherol_or_tocotrienol='tocotrienol' if c['subclass']=='Tocotrienols' else 'tocopherol',primary_construct='peroxyl-radical chain-breaking rate constant k_inh',primary_environment='homogeneous organic autoxidation system',primary_value=float(r['normalized_value']),unit='M^-1 s^-1',eligible_record_count=1,confidence='Low',single_study_flag='yes',heterogeneity_flag='not estimable',identity_risk='natural dietary stereochemistry required; generic vitamin E/all-rac records excluded',environment_risk='homogeneous kinetics do not measure membrane partition or regeneration',caveat='Exploratory chemical chain-breaking kinetics; corresponding tocotrienol values rely on homolog-equivalence evidence.' if c['subclass']=='Tocotrienols' else 'Exploratory chemical chain-breaking kinetics; not in-vivo vitamin activity.',provenance_record_ids=r['evidence_id']))
ve_top.sort(key=lambda x:(-x['primary_value'],x['compound']))
first_rank={}
for i,r in enumerate(ve_top,1):
    first_rank.setdefault(r['primary_value'],i); r['rank']=first_rank[r['primary_value']]
    r['within_subpanel_percentile']=round(100*(len(ve_top)-r['rank']+1)/len(ve_top),1);r['stability']='Fragile'
ve_fields=['rank']+[k for k in ve_top[0] if k!='rank']
writecsv(DATA/'VitaminE_TopN_v1.0.csv',ve_top,ve_fields)

# Secondary L-ORAC records are deliberately not used to alter primary rank.
sec=[]
for compound,val in [('alpha-Tocopherol',0.50),('gamma-Tocopherol',0.74),('delta-Tocopherol',1.36)]:
    sec.append(dict(compound=compound,assay='ORAC(FL-LIPO)',environment='7% RMCD in 50% acetone-water; phosphate buffer pH 7.4',value=val,unit='mol Trolox equivalent/mol compound',evidence_role='secondary standardized profile',PMID='11902917',DOI='10.1021/jf0113732',exact_location='Abstract/results',notes='Not combined with k_inh.'))
sec.append(dict(compound='tocotrienols (unresolved mixture/form)',assay='ORAC(FL-LIPO)',environment='7% RMCD in 50% acetone-water; phosphate buffer pH 7.4',value=0.91,unit='mol Trolox equivalent/mol compound',evidence_role='secondary only; no vitamer mapping',PMID='11902917',DOI='10.1021/jf0113732',exact_location='Abstract/results',notes='Generic tocotrienols value cannot be assigned to alpha/beta/gamma/delta candidates.'))
writecsv(DATA/'VitaminE_LORAC_Secondary_Profile.csv',sec,list(sec[0]))

regen=[
dict(node_A='L-Ascorbic acid',node_B='alpha-Tocopherol/tocopheroxyl radical',interaction='antioxidant regeneration',assay_type='radical recycling kinetics / membrane and solution models',directness='direct chemical regeneration evidence',model_system='lipid/aqueous interface and model membranes',source='Packer et al. 1979; Niki 2014 reviews primary evidence',PMID='',DOI='',Zotero_key='pending_local_import',evidence_strength='mechanistically established; exact record-level expansion pending',notes='Profile only; does not change either subpanel rank.'),
dict(node_A='L-Ascorbic acid',node_B='alpha-Tocotrienol/chromanoxyl radical',interaction='antioxidant regeneration',assay_type='microsomal membrane recycling',directness='functional recycling evidence',model_system='rat liver microsomal membranes',source='Serbinova et al. 1991',PMID='1649783',DOI='10.1016/0891-5849(91)90033-Y',Zotero_key='pending_local_import',evidence_strength='primary comparative study',notes='Profile only; membrane mobility and recycling are distinct from homogeneous k_inh.')]
writecsv(DATA/'Vitamin_Antioxidant_Regeneration_Profile.csv',regen,list(regen[0]))

overview=[]
overview.append(dict(compound='L-Ascorbic acid',vitamin_subpanel='Vitamins–aqueous antioxidant',within_subpanel_rank=1,within_subpanel_percentile='NA',percentile_status='single eligible candidate / percentile not informative',primary_construct=vcrank[0]['primary_construct'],primary_value=med,unit='mol TE/mol compound',confidence='Moderate',stability='Moderately stable',major_caveat=vcrank[0]['caveat']))
for r in ve_top:
    overview.append(dict(compound=r['compound'],vitamin_subpanel='Vitamins–lipid-phase antioxidant',within_subpanel_rank=r['rank'],within_subpanel_percentile=r['within_subpanel_percentile'],percentile_status='informative within 8-candidate mechanistically coherent subpanel',primary_construct=r['primary_construct'],primary_value=r['primary_value'],unit=r['unit'],confidence=r['confidence'],stability=r['stability'],major_caveat=r['caveat']))
writecsv(DATA/'Vitamins_ParentClass_Overview_v1.0.csv',overview,list(overview[0]))

# Global v0.3 adds explicit analysis_subpanel and never computes a vitamin parent-class percentile.
g=readcsv(DATA/'Global_Top_Overview_Master_v0.2.csv')
base_fields=list(g[0]); new_fields=base_fields[:3]+['analysis_subpanel']+base_fields[3:]
for r in g:r['overview_version']='v0.3';r['analysis_subpanel']=r['analysis_panel']
for o in overview:
    c=next(x for x in master if x['compound']==o['compound'])
    row={k:'Not reviewed' for k in new_fields}
    row.update(overview_version='v0.3',parent_class='Vitamins / vitamin-like antioxidants',analysis_panel='Vitamins / vitamin-like',analysis_subpanel=o['vitamin_subpanel'],subclass=c['subclass'],compound=o['compound'],canonical_name=c['canonical_name'],PubChem_CID=c['PubChem_CID'],InChIKey=c['InChIKey'],within_class_rank=o['within_subpanel_rank'],within_class_N_rankable=1 if o['compound']=='L-Ascorbic acid' else 8,within_class_percentile=o['within_subpanel_percentile'],within_class_status=o['percentile_status'],primary_construct=o['primary_construct'],primary_metric_name='H-ORAC-FL' if o['compound']=='L-Ascorbic acid' else 'peroxyl-radical k_inh',primary_value=o['primary_value'],primary_unit=o['unit'],eligible_record_count=2 if o['compound']=='L-Ascorbic acid' else 1,confidence=o['confidence'],single_study_flag='no' if o['compound']=='L-Ascorbic acid' else 'yes',heterogeneity_flag='moderate' if o['compound']=='L-Ascorbic acid' else 'not estimable',identity_risk='defined L-vitamer' if o['compound']=='L-Ascorbic acid' else 'natural stereochemistry required; generic vitamin E/all-rac records excluded',assay_risk='historical H-ORAC protocol heterogeneity' if o['compound']=='L-Ascorbic acid' else 'homogeneous kinetics do not encode membrane partition/regeneration',evidence_depth_category='Moderate (2 independent eligible records)' if o['compound']=='L-Ascorbic acid' else 'Limited (1 eligible kinetic evidence chain)',evidence_stability=o['stability'],major_caveat=o['major_caveat'],provenance_record_ids='VTC-E001;VTC-E002' if o['compound']=='L-Ascorbic acid' else next(x['provenance_record_ids'] for x in ve_top if x['compound']==o['compound']),dietary_exposure_umol_day='NA',exposure_source='Not reviewed',exposure_quality='Not reviewed',bioavailability_summary='Not reviewed',human_evidence_level='Not reviewed',direct_chemical_antioxidant_profile='Aqueous H-ORAC-FL profile' if o['compound']=='L-Ascorbic acid' else 'Lipid-phase chain-breaking kinetic profile',endogenous_defense_profile='Not reviewed',lipid_phase_activity='Not primary' if o['compound']=='L-Ascorbic acid' else 'Primary construct; secondary L-ORAC where available',singlet_oxygen_activity='Not reviewed',NRF2_GSH_GPX_profile='Not reviewed',SOD_CAT_profile='Not reviewed',NOX_mitochondrial_ROS_profile='Not reviewed',ferroptosis_lipid_profile='Not reviewed',direct_target_level='Not reviewed',safety_prooxidant_context='Fe/Cu can shift ascorbate chemistry toward prooxidant reactions' if o['compound']=='L-Ascorbic acid' else 'tocopheroxyl regeneration and Cu(II)/micelle context reviewed separately',experimental_tractability='Not reviewed')
    g.append(row)
writecsv(DATA/'Global_Top_Overview_Master_v0.3.csv',g,new_fields)

# Human review log: preserve older entries and replace Phase 3D rows idempotently.
hr=readcsv(DATA/'Human_Review_Log.csv'); hf=list(hr[0]); hr=[r for r in hr if r.get('stage')!='Phase 3D']
issues=[
('Vitamin E vitamers','candidate master / primary papers','vitamer identity','Natural RRR/R-configured vitamers must remain distinct from all-rac or generic vitamin E records.','Exclude generic/synthetic records until stereochemical mapping is explicit.','May remove or add evidence but does not merge candidates.'),
('Dehydroascorbic acid','candidate lock','vitamer identity','Oxidized vitamin C form has no comparable H-ORAC-FL record and is not interchangeable with ascorbate.','Hold from capacity rank; retain as mechanistic/dietary context.','Prevents an artificial second aqueous rank.'),
('Vitamin C aqueous','construct audit','primary construct choice','Two original H-ORAC-FL records are available for L-ascorbic acid; reducing/kinetic metrics do not add candidate discrimination.','Use H-ORAC-FL provisionally; regeneration remains a separate profile.','Produces all-eligible output for one candidate, not a competitive rank.'),
('Vitamin E lipid-phase','construct audit','primary construct choice','Researcher approved vitamer-specific lipid-peroxidation chain-breaking kinetics; L-ORAC is secondary.','Use direct peroxyl-radical k_inh in one homogeneous environment; do not pool membrane/L-ORAC values.','Defines Top available 8.'),
('Vitamin E environment','construct audit','primary environment choice','The approved primary construct requires a single comparable environment; membrane, micelle, LDL and L-ORAC results encode partition and regeneration effects.','Use homogeneous organic autoxidation for the primary kinetic panel and retain other environments as secondary profiles.','Prevents environment-driven rank mixing.'),
('Vitamin E rank-changing records','evidence audit','rank-change review','No additional eligible record changed the approved primary ordering in this build; L-ORAC gives a different order but remains secondary.','Record the discordance without altering the k_inh ranking.','No primary rank change; flags construct sensitivity.'),
('Vitamins percentile','Global schema stress test II','percentile level','Researcher approved mechanistically coherent subpanel percentiles and rejected parent-class percentile.','Vitamin C percentile=NA because only one eligible candidate; Vitamin E percentile calculated within N=8.','Prevents misleading 100% for a singleton and cross-construct percentile mixing.')]
for c,src,it,desc,recmd,effect in issues:hr.append(dict(stage='Phase 3D',compound=c,source=src,issue_type=it,issue_description=desc,codex_recommendation=recmd,human_decision='approved' if c in {'Vitamin E lipid-phase','Vitamin E environment','Vitamins percentile'} else 'pending second-review implementation',reviewer='Researcher/Codex' if c in {'Vitamin E lipid-phase','Vitamin E environment','Vitamins percentile'} else '',date=TODAY,effect_on_ranking=effect))
writecsv(DATA/'Human_Review_Log.csv',hr,hf)

print({'vitamin_universe':len(master),'aqueous':sum(x['vitamin_subpanel'].startswith('Vitamins–aqueous') for x in lock),'lipid':sum(x['vitamin_subpanel'].startswith('Vitamins–lipid') for x in lock),'vitaminE_top':len(ve_top),'global_v03':len(g)})
