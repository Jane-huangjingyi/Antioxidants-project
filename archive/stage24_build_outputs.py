from pathlib import Path
import json, glob
import pandas as pd
import numpy as np

ROOT=Path(__file__).resolve().parents[1]; DATA=ROOT/'data'; DOCS=ROOT/'docs'; FIG=ROOT/'figures'/'aqueous_antioxidant_atlas'
candidate=pd.read_csv(DATA/'Aqueous_Antioxidant_Candidate_Master.csv')
unfinished=['Polyphenols - Stilbenes / lignans','Betalains / nitrogen-containing','Organosulfur compounds','Other food-derived redox-active phytochemicals']

# Search audit: all 157 frozen candidates are represented. Completed panels inherit Stage 23 review;
# unfinished panels use the candidate-specific Europe PMC searches downloaded during Stage 24.
searched=candidate[candidate.analysis_panel.isin(unfinished)].reset_index(drop=True)
hits=[]
for i,row in searched.iterrows():
    p=ROOT/'.tmp_stage24_search'/f'{i+1:03d}.json'
    d=json.loads(p.read_text(encoding='utf-8')) if p.exists() else {}
    hits.append(d.get('hitCount',np.nan))
log=[]
for _,r in candidate.iterrows():
    if r.analysis_panel in unfinished:
        j=searched.index[searched['compound'].eq(r.compound)][0]
        q=f'TITLE_ABS:"{r.compound}" AND (ORAC OR "oxygen radical absorbance capacity" OR antioxidant OR "radical scavenging" OR redox OR Fenton)'
        log.append([r.compound,r.analysis_panel,'Europe PMC',q,hits[j],'2026-09-18','systematic candidate-level metadata screen completed','Stage 24; full-text extraction restricted to potentially eligible/original sources'])
    else:
        log.append([r.compound,r.analysis_panel,'Stage 23 evidence masters','inherited frozen provenance review',np.nan,'2026-09-18','completed before Stage 24','No new search; completeness review only'])
pd.DataFrame(log,columns=['compound','analysis_panel','database_or_source','exact_query','results_found','search_date','search_status','notes']).to_csv(DATA/'Stage24_Literature_Search_Log.csv',index=False)

future=pd.DataFrame([
 ['Alliin','Organosulfur compounds','Found in comparative original garlic-antioxidant paper but absent from frozen universe','10.1089/jmf.2006.9.205','future candidate only'],
 ['Homovanillic alcohol','Other aqueous phytochemicals','Comparator in oleuropein/hydroxytyrosol peroxyl-radical paper','10.5650/jos.ess15042','future candidate only'],
 ['Dehydrozingerone','Other aqueous phytochemicals','ORAC-active comparator in curcumin-related original paper','10.3762/bjoc.11.151','future candidate only'],
 ['Piperine','Other aqueous phytochemicals','Spice-derived comparator found during LDL-oxidation search','NA','future candidate only'],
],columns=['candidate','suggested_panel','discovery_reason','source_DOI','stage24_action'])
future.to_csv(DATA/'Future_Candidate_Additions_Log.csv',index=False)

def class_master(panel, evidence):
    c=candidate[candidate.analysis_panel.eq(panel)][['compound','canonical_name','PubChem_CID','InChIKey','subclass','normal_dietary_relevance','food_sources']].copy()
    e=pd.DataFrame(evidence)
    return c.merge(e,on='compound',how='left')

stil_ev=[
 dict(compound='trans-Resveratrol',assay='H-ORAC-FL',primary_construct='AAPH–fluorescein–Trolox H-ORAC-FL',original_value=5.811,original_unit='mol TE/mol compound',normalized_value=5.811,normalized_unit='mol TE/mol compound',evidence_tier='B1',rank_eligible='yes',DOI='10.1093/chromsci/bmad007',PMID='36752411',exact_location='Table I; Materials/Methods and supplementary methods',independent_experiment_id='10.1093/chromsci/bmad007::trans-Resveratrol',major_caveat='single study; cosolvent/solubility-sensitive'),
 dict(compound='Sesamol',assay='H-ORAC-FL',primary_construct='AAPH–fluorescein–Trolox H-ORAC-FL',original_value=2.107,original_unit='mol TE/mol compound',normalized_value=2.107,normalized_unit='mol TE/mol compound',evidence_tier='B1',rank_eligible='yes',DOI='10.1039/D1RA08918H',PMID=np.nan,exact_location='Table 1; standardized H-ORAC SOP',independent_experiment_id='10.1039/D1RA08918H::Sesamol',major_caveat='single study'),
]
stil=class_master('Polyphenols - Stilbenes / lignans',stil_ev)
stil['systematic_search_completed']='yes'; stil['ranking_status']=np.where(stil.rank_eligible.eq('yes'),'rankable','no eligible A/B1 found'); stil['HUMAN_REVIEW_REQUIRED']=np.where(stil.compound.eq('Podophyllotoxin'),'dietary gate/aqueous-scope concern—do not modify candidate','no')
stil.to_csv(DATA/'Stilbenes_Lignans_Evidence_Master.csv',index=False)
st_rank=stil[stil.rank_eligible.eq('yes')].sort_values('normalized_value',ascending=False).copy(); st_rank.insert(0,'rank',range(1,len(st_rank)+1)); st_rank['eligible_record_count']=1;st_rank['confidence']='Low';st_rank['stability']='Fragile';st_rank['ranking_status']='Top available / all rankable'
st_rank[['rank','compound','subclass','normalized_value','normalized_unit','eligible_record_count','confidence','stability','DOI','exact_location','major_caveat','ranking_status']].to_csv(DATA/'Stilbenes_Lignans_TopN_v1.0.csv',index=False)

betalain_records=[
 dict(compound='Betanin',assay='MPO compound-I/II and HOCl kinetics',construct='mechanism-specific kinetic profile',original_value='1.5e6; 1.1e5; 1.8e4',unit='M^-1 s^-1',evidence_tier='B1-profile',rank_eligible='profile_only',DOI='10.1016/j.bbrc.2005.05.031',PMID='15913556',exact_location='Abstract; kinetic results in main text',optical_risk='high; pigment controls required',interpretation='MPO substrate and HOCl scavenger; concentration/pH-dependent dual effect'),
 dict(compound='Indicaxanthin',assay='MPO compound-I/II and HOCl kinetics',construct='mechanism-specific kinetic profile',original_value='1.1e6; 2.9e5; 7.7e4',unit='M^-1 s^-1',evidence_tier='B1-profile',rank_eligible='profile_only',DOI='10.1016/j.bbrc.2005.05.031',PMID='15913556',exact_location='Abstract; kinetic results in main text',optical_risk='high; pigment controls required',interpretation='MPO substrate and faster HOCl scavenging than betanin in this system'),
 dict(compound='Betanin',assay='LOX-FL',construct='lipoxygenase-dependent fluorescein protection',original_value='reported quantitative response',unit='method-specific',evidence_tier='B2-profile',rank_eligible='profile_only',DOI='10.1007/s11130-021-00914-7',PMID='34363561',exact_location='Figures 1–3; Supplementary Table S4',optical_risk='spectrophotometric monitoring used to reduce pigment interference',interpretation='ORAC/TEAC under-responsive relative to LOX-FL'),
 dict(compound='Indicaxanthin',assay='LOX-FL',construct='lipoxygenase-dependent fluorescein protection',original_value='reported quantitative response',unit='method-specific',evidence_tier='B2-profile',rank_eligible='profile_only',DOI='10.1007/s11130-021-00914-7',PMID='34363561',exact_location='Figures 1–3; Supplementary Table S4',optical_risk='spectrophotometric monitoring used to reduce pigment interference',interpretation='ORAC/TEAC under-responsive relative to LOX-FL'),
]
bet=class_master('Betalains / nitrogen-containing',betalain_records);bet['systematic_search_completed']='yes';bet['ranking_status']='Profile only—insufficient directly comparable evidence';bet['HUMAN_REVIEW_REQUIRED']=np.where(bet.PubChem_CID.isna(),'identity unresolved in frozen master—do not modify','no')
bet.to_csv(DATA/'Betalains_Nitrogen_Profile_Evidence.csv',index=False)

org_records=[
 dict(compound='Sulforaphane',assay='KEAP1 cysteine sensing/ARE induction',construct='causal electrophile–KEAP1–NRF2 profile',original_value='qualitative causal perturbation',unit='NA',evidence_tier='A-profile',rank_eligible='profile_only',DOI='10.1073/pnas.172398899',PMID='12193649',exact_location='Main text and figures',interpretation='Direct KEAP1 sulfhydryl sensing; not direct radical capacity'),
 dict(compound='Allicin',assay='Fenton ESR spin trapping and thiol exchange',construct='Fenton/thiol-reactivity profile',original_value='significant suppression; S-allylmercaptocysteine identified',unit='qualitative/structure-confirmed',evidence_tier='B1-profile',rank_eligible='profile_only',DOI='10.1016/S0304-4165(97)00104-9',PMID='9528659',exact_location='Abstract; main kinetic/structural results',interpretation='Antioxidant readout plus rapid protein-thiol chemistry'),
 dict(compound='Allicin',assay='peroxyl-radical chain-breaking kinetics',construct='non-aqueous kinetic support',original_value='2.6e3; 1.6e5',unit='M^-1 s^-1',evidence_tier='C for aqueous rank',rank_eligible='profile_only',DOI='10.1016/j.freeradbiomed.2006.11.008',PMID='17312965',exact_location='Abstract; kinetic results',interpretation='Quantitative chain-breaking, but chlorobenzene/lipid substrate context is not aqueous H-ORAC'),
 dict(compound='S-Allyl-L-cysteine',assay='hydroxyl-radical competitive kinetics',construct='direct radical kinetics profile',original_value='2.1–2.2e9',unit='M^-1 s^-1',evidence_tier='B1-profile',rank_eligible='profile_only',DOI='10.1089/jmf.2006.9.205',PMID='16822206',exact_location='Abstract; original results',interpretation='Hydroxyl-radical scavenging; no microsomal lipid-peroxidation protection'),
 dict(compound='Diallyl disulfide',assay='hydroxyl-radical competitive kinetics',construct='direct radical kinetics profile',original_value='0.7–1.5e10',unit='M^-1 s^-1',evidence_tier='B1-profile',rank_eligible='profile_only',DOI='10.1089/jmf.2006.9.205',PMID='16822206',exact_location='Abstract; original results',interpretation='Hydroxyl scavenger and lipid-peroxidation terminator in tested systems'),
]
org=class_master('Organosulfur compounds',org_records);org['systematic_search_completed']='yes';org['ranking_status']='Redox-mechanism profile—no defensible common direct-capacity scale';org['HUMAN_REVIEW_REQUIRED']=np.where(org.normal_dietary_relevance.eq('unresolved'),'normal dietary gate unresolved—do not modify','no')
org.to_csv(DATA/'Organosulfur_Redox_Profile.csv',index=False)

other_records=[
 dict(compound='Zingerone',assay='ORAC-FL',primary_construct='AAPH–fluorescein–Trolox ORAC',original_value=3.85,original_unit='relative Trolox equivalent',normalized_value=3.85,normalized_unit='mol TE/mol compound',evidence_tier='B1',rank_eligible='yes',DOI='10.3762/bjoc.11.151',PMID='26425195',exact_location='Table 1, compound 3; ORAC footnote c/g',major_caveat='single study'),
 dict(compound='Eugenol',assay='H-ORAC-FL',primary_construct='AAPH–fluorescein–Trolox H-ORAC-FL',original_value=1.811,original_unit='mol TE/mol compound',normalized_value=1.811,normalized_unit='mol TE/mol compound',evidence_tier='B1',rank_eligible='yes',DOI='10.1039/D1RA08918H',PMID=np.nan,exact_location='Table 1; standardized H-ORAC SOP',major_caveat='single study'),
 dict(compound='Tyrosol',assay='H-ORAC-FL',primary_construct='AAPH–fluorescein–Trolox H-ORAC-FL',original_value=1.131,original_unit='mol TE/mol compound',normalized_value=1.131,normalized_unit='mol TE/mol compound',evidence_tier='B1',rank_eligible='yes',DOI='10.1039/D1RA08918H',PMID=np.nan,exact_location='Table 1; standardized H-ORAC SOP',major_caveat='single study'),
 dict(compound='Carvacrol',assay='H-ORAC-FL',primary_construct='AAPH–fluorescein–Trolox H-ORAC-FL',original_value=.829,original_unit='mol TE/mol compound',normalized_value=.829,normalized_unit='mol TE/mol compound',evidence_tier='B1',rank_eligible='yes',DOI='10.1039/D1RA08918H',PMID=np.nan,exact_location='Table 1; standardized H-ORAC SOP',major_caveat='single study'),
 dict(compound='Thymol',assay='H-ORAC-FL',primary_construct='AAPH–fluorescein–Trolox H-ORAC-FL',original_value=.545,original_unit='mol TE/mol compound',normalized_value=.545,normalized_unit='mol TE/mol compound',evidence_tier='B1',rank_eligible='yes',DOI='10.1039/D1RA08918H',PMID=np.nan,exact_location='Table 1; standardized H-ORAC SOP',major_caveat='single study'),
 dict(compound='Hydroxytyrosol',assay='peroxyl-radical fluorescein-decay kinetics',primary_construct='mechanism profile',original_value=2.0,original_unit='radicals trapped relative to Trolox',normalized_value=np.nan,normalized_unit='NA',evidence_tier='B1-profile',rank_eligible='profile_only',DOI='10.5650/jos.ess15042',PMID='26136177',exact_location='Abstract and fluorescein-decay results',major_caveat='not the frozen H-ORAC aggregation construct'),
 dict(compound='Oleuropein',assay='peroxyl-radical fluorescein-decay kinetics',primary_construct='mechanism profile',original_value=2.0,original_unit='radicals trapped relative to Trolox',normalized_value=np.nan,normalized_unit='NA',evidence_tier='B1-profile',rank_eligible='profile_only',DOI='10.5650/jos.ess15042',PMID='26136177',exact_location='Abstract and fluorescein-decay results',major_caveat='not the frozen H-ORAC aggregation construct'),
 dict(compound='Curcumin',assay='singlet-oxygen EPR',primary_construct='mechanism profile',original_value=2.75,original_unit='µM for 50% TEMPO-adduct inhibition',normalized_value=np.nan,normalized_unit='NA',evidence_tier='B1-profile',rank_eligible='profile_only',DOI='10.1016/S0006-291X(02)00633-2',PMID='12083767',exact_location='Abstract and EPR results',major_caveat='singlet-oxygen construct; ethanol/cosolvent; not H-ORAC'),
 dict(compound='Plumbagin',assay='cellular redox cycling/GSH',primary_construct='prooxidant-risk profile',original_value='1–20',original_unit='µM exposure range',normalized_value=np.nan,normalized_unit='NA',evidence_tier='B1-profile',rank_eligible='profile_only',DOI='10.1016/j.tox.2003.11.001',PMID='14727919',exact_location='Abstract; cellular mechanistic results',major_caveat='redox cycling and cytotoxicity'),
 dict(compound='Juglone',assay='cellular redox cycling/GSH',primary_construct='prooxidant-risk profile',original_value='1–20',original_unit='µM exposure range',normalized_value=np.nan,normalized_unit='NA',evidence_tier='B1-profile',rank_eligible='profile_only',DOI='10.1016/j.tox.2003.11.001',PMID='14727919',exact_location='Abstract; cellular mechanistic results',major_caveat='redox cycling and cytotoxicity'),
]
oth=class_master('Other food-derived redox-active phytochemicals',other_records);oth['systematic_search_completed']='yes';oth['ranking_status']=np.where(oth.rank_eligible.eq('yes'),'rankable H-ORAC subpanel','profile-only or no eligible common construct');oth['HUMAN_REVIEW_REQUIRED']=np.where(oth.compound.eq('Ubiquinone-10'),'aqueous-scope concern—do not modify frozen candidate','no')
oth.to_csv(DATA/'Other_Aqueous_Phytochemicals_Evidence_Master.csv',index=False)
ot_rank=oth[oth.rank_eligible.eq('yes')].sort_values('normalized_value',ascending=False).copy();ot_rank.insert(0,'rank',range(1,len(ot_rank)+1));ot_rank['eligible_record_count']=1;ot_rank['confidence']='Low';ot_rank['stability']='Fragile';ot_rank['ranking_status']='Top available H-ORAC subpanel'
ot_rank[['rank','compound','subclass','normalized_value','normalized_unit','eligible_record_count','confidence','stability','DOI','exact_location','major_caveat','ranking_status']].to_csv(DATA/'Other_Aqueous_Phytochemicals_TopN_v1.0.csv',index=False)

def coverage(df,panel):
    ev=df[df.DOI.notna()].copy() if 'DOI' in df else df.iloc[0:0]
    return pd.DataFrame([dict(analysis_panel=panel,candidate_N=len(candidate[candidate.analysis_panel.eq(panel)]),rankable_N=int((df.get('rank_eligible',pd.Series()).eq('yes')).groupby(df['compound']).any().sum()),original_papers=ev.DOI.nunique(),core_ranking_papers=ev[ev.get('rank_eligible','').eq('yes')].DOI.nunique() if len(ev) else 0,supporting_profile_papers=ev[~ev.get('rank_eligible','').eq('yes')].DOI.nunique() if len(ev) else 0,output='ranking' if (df.get('rank_eligible',pd.Series()).eq('yes')).any() else 'profile only')])
cov=pd.concat([coverage(stil,'Polyphenols - Stilbenes / lignans'),coverage(bet,'Betalains / nitrogen-containing'),coverage(org,'Organosulfur compounds'),coverage(oth,'Other food-derived redox-active phytochemicals')],ignore_index=True)
cov.to_csv(DATA/'Stage24_New_Class_Ranking_Coverage.csv',index=False)
cov[cov.analysis_panel.eq('Polyphenols - Stilbenes / lignans')].to_csv(DATA/'Stilbenes_Lignans_Ranking_Coverage.csv',index=False)
cov[cov.analysis_panel.eq('Other food-derived redox-active phytochemicals')].to_csv(DATA/'Other_Aqueous_Phytochemicals_Ranking_Coverage.csv',index=False)

metal=pd.DataFrame([
 ['Quercetin','Polyphenols - Flavonoids','Fe-ATP','Fe(II/III) system','voltammetric Fenton suppression','chelation + net suppression','iron-ATP/H2O2 catalytic wave','complete suppression at flavonoid:Fe-ATP >=1.5:1','ratio','pH 7.4 HEPES/18.75% methanol','10.1023/A:1009229429250','10831228','Abstract/main results','Moderate','net suppression in defined system'],
 ['Luteolin','Polyphenols - Flavonoids','Fe-ATP','Fe(II/III) system','voltammetric Fenton suppression','chelation + net suppression','iron-ATP/H2O2 catalytic wave','complete suppression at flavonoid:Fe-ATP >=1.5:1','ratio','pH 7.4 HEPES/18.75% methanol','10.1023/A:1009229429250','10831228','Abstract/main results','Moderate','net suppression in defined system'],
 ['Naringenin','Polyphenols - Flavonoids','Fe-ATP','Fe(II/III) system','voltammetric Fenton suppression','chelation + partial suppression','iron-ATP/H2O2 catalytic wave','less effective than quercetin/luteolin','qualitative','pH 7.4 HEPES/18.75% methanol','10.1023/A:1009229429250','10831228','Abstract/main results','Moderate','do not infer binding alone equals net antioxidant action'],
 ['Quercetin','Polyphenols - Flavonoids','Cu','Cu(II)','EPR spin trapping/DNA damage','chelation + Fenton suppression','hydroxyl radical/DNA damage','protective only at higher quercetin:Cu ratios','context-specific','aqueous Cu-Fenton system','10.1016/j.fct.2017.10.042','29107026','Abstract/main results','Moderate','stoichiometry dependent'],
 ['Isorhamnetin','Polyphenols - Flavonoids','Fe/Cu','multiple','spectroscopy/Fenton/hemolysis','chelation + reduction + net context','iron/copper Fenton and hemolysis','iron potentiation; copper suppression acidic conditions','qualitative','multiple pH/oxidation states','10.1021/acs.jafc.1c01729','34003649','Abstract/main results','High','clear prooxidant/antioxidant reversal'],
 ['Catechin','Polyphenols - Flavonoids','Fe','cellular labile iron','iron-loaded hepatocytes','chelation/cytoprotection','lipid peroxidation/enzyme release','IC50 reported in paper','study-specific','hepatocyte culture','10.1016/0006-2952(93)90371-3','8424806','Abstract/main results','Moderate','cellular uptake contributes'],
 ['Rutin','Polyphenols - Flavonoids','Fe','iron-dependent systems','lipid peroxidation/Fenton','chelation + radical scavenging','lipid peroxidation','more chelation-dependent than quercetin','qualitative','microsomal/lipid systems','NA','2735934','Abstract/main results','Low','DOI not identified'],
 ['Allicin','Organosulfur compounds','Fe','Fe(II)','ESR Fenton spin trapping','net suppression + thiol exchange','oxygen-radical signal','significant suppression','qualitative','H2O2–Fe(II)','10.1016/S0304-4165(97)00104-9','9528659','Abstract/main results','Moderate','not conventional metal-chelation evidence'],
],columns=['compound','parent_class','metal_ion','oxidation_state','assay','chelation_or_reduction','ROS_endpoint','original_value','unit','pH_buffer_context','DOI','PMID','exact_location','evidence_strength','notes'])
metal['Fenton_or_Fenton_like']='yes';metal['metal_concentration']='see original paper';metal['compound_concentration']='see original paper';metal['net_antioxidant_or_prooxidant_interpretation']=metal.notes
metal.to_csv(DATA/'Aqueous_Metal_Redox_Evidence.csv',index=False)

micro=pd.DataFrame([
 ['Selenium','selenium-enriched yeast / selenomethionine / food forms','GPX and TXNRD cofactor','GPX1–4; TXNRD1–3','selenoprotein incorporation','low status can limit selenoproteins','dose/form/baseline-dependent; U-shaped risk','RCTs include oxidative biomarkers and selenoprotein P','8-OHdG; F2-isoprostanes; GPX','excess toxicity/U-shaped','Moderate','10.3945/ajcn.2009.28169','20181815','Healthy-adult dose-response RCT'],
 ['Zinc','zinc gluconate/sulfate/food zinc','structural/regulatory antioxidant role','SOD1; metallothionein','indirect; redox-inert structural cofactor','deficiency increases susceptibility','mixed RCTs; benefit depends on baseline/status','positive and null RCTs','SOD; MDA; TAC; GSH; F2-isoprostanes','excess can induce copper deficiency','Moderate','10.1016/j.atherosclerosis.2011.07.097','21840002','Null trial retained to avoid benefit-only bias'],
 ['Manganese','dietary Mn','mitochondrial SOD cofactor','SOD2','enzymatic cofactor','deficiency/rare disorders impair mitochondrial defense','no general antioxidant-supplement claim','mechanistic/deficiency evidence prioritized','SOD2 activity; mitochondrial ROS','excess neurotoxicity','Moderate','10.1007/s10863-017-9718-8','28616679','Profile, not rank'],
 ['Copper','dietary Cu / ceruloplasmin-bound Cu','SOD1 and ceruloplasmin context','SOD1; ceruloplasmin','cofactor with prooxidant excess','deficiency lowers Cu/Zn-SOD','replacement helps deficiency; no general antioxidant claim','case/deficiency evidence','SOD activity; oxidative damage','labile excess Cu supports Fenton-like chemistry','Moderate','10.1007/BF01846029','7439197','Dual role'],
 ['Iron','dietary/therapeutic iron','heme/catalase context; essential but not antioxidant nutrient','heme proteins; catalase context','essential/prooxidant dual role','deficiency impairs physiology','loading increases oxidative damage in context','human randomized loading/chelation evidence','MDA; labile plasma iron','overload/Fenton chemistry','High','10.1371/journal.pone.0080848','24241495','Do not label as antioxidant nutrient'],
 ['Magnesium','dietary Mg','indirect metabolic support','multiple ATP-dependent enzymes','indirect','deficiency may associate with oxidative stress','not a specific antioxidant-enzyme intervention','evidence heterogeneous','context-specific biomarkers','excess risk in renal failure','Limited','NA','NA','Retained profile; evidence gap'],
 ['Molybdenum','dietary molybdate','molybdoenzyme context','sulfite oxidase; xanthine oxidoreductase','indirect/ambiguous','rare deficiency','no general antioxidant supplementation rationale','mechanistic only','enzyme-specific endpoints','excess/toxicity context','Limited','NA','NA','Retained profile; evidence gap'],
],columns=['nutrient','chemical_form','redox_role','key_antioxidant_enzyme','cofactor_role','deficiency_evidence','supplementation_evidence','human_evidence','oxidative_endpoint','prooxidant_context','evidence_strength','original_paper_DOI','PMID','notes'])
micro['dietary_sources']='see Stage 23 micronutrient profile';micro['toxicity_context']=micro['prooxidant_context']
micro.to_csv(DATA/'Antioxidant_Micronutrient_Redox_Profile_v2.csv',index=False)

# Supervisor overview: only mechanistically coherent ranked panels receive percentiles.
rows=[]
def add_rank(path,parent,panel,subpanel,valcol,unit,rankable_total=None):
 d=pd.read_csv(path); n=rankable_total or len(d)
 for _,r in d.iterrows():
  rows.append([parent,panel,subpanel,r['compound'],int(r['rank']),n,100*(n-int(r['rank'])+1)/n,'H-ORAC-FL',r[valcol],unit,r.get('eligible_record_count',np.nan),r.get('confidence','Low'),r.get('stability','Fragile'),r.get('ranking_status','provisional'),r.get('major_caveat',r.get('caveat','')),len(set(str(r.get('DOI',r.get('key_DOI_PMID',''))).split(';'))), 'completed ranking'])
add_rank(DATA/'Polyphenols_Flavonoids_Top20_v1.0.csv','Polyphenols','Polyphenols - Flavonoids','Flavonoids','median_H_ORAC','mol TE/mol compound',25)
add_rank(DATA/'Polyphenols_PhenolicAcids_TopN_v1.0.csv','Polyphenols','Polyphenols - Phenolic acids / conjugates','Phenolic acids / conjugates','median_H_ORAC','mol TE/mol compound',18)
vc=pd.read_csv(DATA/'VitaminC_TopAvailable_v1.0.csv').iloc[0];rows.append(['Vitamins','Vitamins / vitamin-like','Vitamin C aqueous',vc.compound,1,1,np.nan,vc.primary_construct,vc.primary_value,vc.unit,vc.eligible_record_count,vc.confidence,vc.stability,'singleton / percentile not informative',vc.caveat,2,'completed ranking'])
add_rank(DATA/'Stilbenes_Lignans_TopN_v1.0.csv','Polyphenols','Polyphenols - Stilbenes / lignans','Stilbenes / lignans','normalized_value','mol TE/mol compound')
add_rank(DATA/'Other_Aqueous_Phytochemicals_TopN_v1.0.csv','Other phytochemicals','Other food-derived redox-active phytochemicals','H-ORAC-compatible subpanel','normalized_value','mol TE/mol compound')
sup=pd.DataFrame(rows,columns=['parent_class','analysis_panel','analysis_subpanel','compound','within_class_rank','rankable_N','within_class_percentile','primary_construct','primary_value','primary_unit','eligible_record_count','confidence','stability','ranking_status','major_caveat','DOI_count','current_status'])
sup.to_csv(DATA/'Supervisor_Aqueous_Class_Ranking_Overview.csv',index=False)

# Append new evidence rows to the unified master without replacing Stage 23 records.
master=pd.read_csv(DATA/'Aqueous_Antioxidant_Primary_Literature_Evidence.csv')
new=[]
for df,panel in [(stil,'Polyphenols - Stilbenes / lignans'),(bet,'Betalains / nitrogen-containing'),(org,'Organosulfur compounds'),(oth,'Other food-derived redox-active phytochemicals')]:
 for _,r in df[df.DOI.notna()].iterrows():
  new.append(dict(paper_id='S24-'+str(len(new)+1).zfill(3),first_author='see DOI metadata',year=np.nan,paper_title='see DOI metadata',journal='see DOI metadata',DOI=r.DOI,PMID=r.get('PMID',np.nan),original_research_yes_no='yes',review_or_original='original',candidate_id=r.get('PubChem_CID',np.nan),compound=r.compound,canonical_name=r.get('canonical_name',r.compound),PubChem_CID=r.get('PubChem_CID',np.nan),InChIKey=r.get('InChIKey',np.nan),parent_class=r.get('parent_class',np.nan),analysis_panel=panel,subclass=r.get('subclass',np.nan),assay=r.get('assay',np.nan),primary_or_secondary_construct=r.get('primary_construct',r.get('construct','profile')),original_value=r.get('original_value',np.nan),original_unit=r.get('original_unit',r.get('unit',np.nan)),normalized_value=r.get('normalized_value',np.nan),normalized_unit=r.get('normalized_unit',np.nan),evidence_tier=r.get('evidence_tier',np.nan),rank_eligible=r.get('rank_eligible','profile_only'),independent_experiment_id=str(r.DOI)+'::'+str(r.compound)+'::'+str(r.get('assay','profile')),quality_note='Stage 24 original-paper evidence',exact_table=r.get('exact_location',np.nan),Zotero_key='pending_local_import',paper_role='core_ranking' if r.get('rank_eligible')=='yes' else 'supporting_quantitative',notes=r.get('major_caveat',r.get('interpretation',np.nan))))
newdf=pd.DataFrame(new)
# Resolve bibliographic metadata from the frozen Europe PMC search export.
meta={}
for fp in glob.glob(str(ROOT/'.tmp_stage24_search'/'*.json'))+glob.glob(str(ROOT/'.tmp_*.json')):
 try:
  payload=json.loads(Path(fp).read_text(encoding='utf-8'))
 except Exception:
  continue
 for item in payload.get('resultList',{}).get('result',[]):
  doi=str(item.get('doi') or '').lower()
  if doi:
   ji=item.get('journalInfo') or {}; journal=(ji.get('journal') or {}).get('title') or (ji.get('journal') or {}).get('medlineAbbreviation')
   meta[doi]=dict(first_author=(item.get('authorString') or '').split(',')[0],year=item.get('pubYear'),paper_title=item.get('title'),journal=journal,PMCID=item.get('pmcid'))
meta.update({
 '10.1073/pnas.172398899':dict(first_author='Dinkova-Kostova AT',year='2002',paper_title='Direct evidence that sulfhydryl groups of Keap1 are the sensors regulating induction of phase 2 enzymes that protect against carcinogens and oxidants',journal='Proceedings of the National Academy of Sciences USA',PMCID=np.nan),
 '10.1016/j.freeradbiomed.2006.11.008':dict(first_author='Okada Y',year='2007',paper_title='Kinetic and mechanistic studies of allicin as an antioxidant',journal='Free Radical Biology and Medicine',PMCID=np.nan),
 '10.1089/jmf.2006.9.205':dict(first_author='Chung LY',year='2006',paper_title='The antioxidant properties of garlic compounds: allyl cysteine, alliin, allicin, and allyl disulfide',journal='Journal of Medicinal Food',PMCID=np.nan),
 '10.1016/s0006-291x(02)00633-2':dict(first_author='Das KC',year='2002',paper_title='Curcumin (diferuloylmethane), a singlet oxygen quencher',journal='Biochemical and Biophysical Research Communications',PMCID=np.nan),
 '10.1016/j.tox.2003.11.001':dict(first_author='Inbaraj JJ',year='2004',paper_title='Cytotoxic action of juglone and plumbagin: a mechanistic study using HaCaT keratinocytes',journal='Toxicology',PMCID=np.nan),
 '10.5650/jos.ess15042':dict(first_author='Sakurai H',year='2015',paper_title='Radical-scavenging activity and antioxidative effects of olive leaf components oleuropein and hydroxytyrosol in comparison with homovanillic alcohol',journal='Journal of Oleo Science',PMCID=np.nan),
})
for col in ['first_author','year','paper_title','journal','PMCID']:
 if col not in newdf: newdf[col]=np.nan
 newdf[col]=newdf[col].astype(object)
for idx,r in newdf.iterrows():
 m=meta.get(str(r.DOI).lower(),{})
 for col in ['first_author','year','paper_title','journal','PMCID']:
  if m.get(col): newdf.at[idx,col]=m[col]
for c in master.columns:
 if c not in newdf:newdf[c]=np.nan
newdf=newdf[master.columns]
key=lambda d:d.DOI.fillna('').astype(str).str.lower()+'|'+d['compound'].fillna('').astype(str).str.lower()+'|'+d['assay'].fillna('').astype(str).str.lower()
existing=set(key(master)); newdf=newdf[~key(newdf).isin(existing)]
pd.concat([master,newdf],ignore_index=True).to_csv(DATA/'Aqueous_Antioxidant_Primary_Literature_Evidence.csv',index=False)

# Rebuild paper summary from record-level evidence, retaining exact compound/result context.
all_ev=pd.concat([master,newdf],ignore_index=True)
for col in ['first_author','year','paper_title','journal','PMCID']:
 all_ev[col]=all_ev[col].astype(object)
for idx,r in all_ev.iterrows():
 m=meta.get(str(r.DOI).lower(),{})
 for col in ['first_author','year','paper_title','journal','PMCID']:
  if m.get(col) and col in all_ev.columns: all_ev.at[idx,col]=m[col]
all_ev.to_csv(DATA/'Aqueous_Antioxidant_Primary_Literature_Evidence.csv',index=False)
paper_rows=[]
for doi,g in all_ev.groupby('DOI',dropna=False):
 vals=pd.to_numeric(g.original_value,errors='coerce').dropna()
 high='; '.join(g.loc[pd.to_numeric(g.normalized_value,errors='coerce').idxmax(),['compound']].astype(str)) if pd.to_numeric(g.normalized_value,errors='coerce').notna().any() else 'profile-specific'
 paper_rows.append(dict(paper_id=g.paper_id.dropna().astype(str).iloc[0] if g.paper_id.notna().any() else 'unresolved',first_author=g.first_author.dropna().astype(str).iloc[0] if g.first_author.notna().any() else 'unresolved',year=g.year.dropna().iloc[0] if g.year.notna().any() else np.nan,paper_title=g.paper_title.dropna().astype(str).iloc[0] if g.paper_title.notna().any() else 'unresolved',journal=g.journal.dropna().astype(str).iloc[0] if g.journal.notna().any() else 'unresolved',DOI=doi,PMID='; '.join(sorted(set(g.PMID.dropna().astype(str)))),assay='; '.join(sorted(set(g.assay.dropna().astype(str)))),assay_phase='; '.join(sorted(set(g.assay_phase.dropna().astype(str)))),compounds_N=g.compound.nunique(),compounds_tested='; '.join(sorted(set(g.compound.dropna().astype(str)))),major_compounds='; '.join(sorted(set(g.compound.dropna().astype(str)))),highest_reported_compound=high,highest_reported_value=vals.max() if len(vals) else np.nan,value_range=(f'{vals.min():g}–{vals.max():g}' if len(vals) else 'construct-specific'),value_unit='; '.join(sorted(set(g.original_unit.dropna().astype(str)))),class_coverage='; '.join(sorted(set(g.analysis_panel.dropna().astype(str)))),primary_or_supporting='core_ranking' if g.rank_eligible.eq('yes').any() else 'supporting_quantitative',evidence_tier='; '.join(sorted(set(g.evidence_tier.dropna().astype(str)))),why_high_quality='Original research; defined compounds; traceable DOI/PMID; extractable value or explicit mechanism endpoint.',role_in_ranking='eligible records included' if g.rank_eligible.eq('yes').any() else 'profile/supporting only',major_limitation='Protocols/constructs remain class-specific; see record-level caveats.',Zotero_key='; '.join(sorted(set(g.Zotero_key.dropna().astype(str))))))
pd.DataFrame(paper_rows).to_csv(DATA/'Aqueous_Antioxidant_Paper_Summary.csv',index=False)

print({'frozen_candidates':len(candidate),'candidate_search_rows':len(log),'new_evidence_rows':len(newdf),'stilbene_rankable':len(st_rank),'other_rankable':len(ot_rank),'metal_rows':len(metal),'micronutrients':len(micro)})
