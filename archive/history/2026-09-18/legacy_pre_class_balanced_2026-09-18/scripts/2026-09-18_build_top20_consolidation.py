import csv, statistics
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

R=Path(__file__).resolve().parents[1]; D=R/'data'; F=R/'figures'; DOC=R/'docs'; H=R/'handoff'
for p in (D,F,DOC,H): p.mkdir(exist_ok=True)
def read(p):
    with open(p,encoding='utf-8-sig') as f:return list(csv.DictReader(f))
def write(p,rows,fields=None):
    with open(p,'w',newline='',encoding='utf-8-sig') as f:
        w=csv.DictWriter(f,fieldnames=fields or list(rows[0]));w.writeheader();w.writerows(rows)

oldrank=read(D/'H_ORAC_Provisional_Ranking.csv'); oldrec=read(D/'H_ORAC_Phenolic_Literature_Records.csv'); universe=read(D/'H_ORAC_Phenolic_Candidate_Universe.csv')
old={x['compound_name']:x for x in oldrank}

records=[]
for r in oldrec:
    records.append(dict(compound=r['compound_name'],subclass=next((u['subclass'] for u in universe if u['compound_name']==r['compound_name']),''),value_mol_TE_per_mol=r['value'],tier=r['tier'],probe='fluorescein' if r['tier']!='C' else 'β-phycoerythrin',ORAC_arm='H-ORAC',study=r['study'],year=r['year'],PMID=r['PMID'],DOI=r['DOI'],Zotero_key=r['Zotero_key'],exact_location=r['exact_location'],independent_experiment_id=(r['DOI'] or r['study'])+'::'+r['compound_name'],original_unit='mol TE/mol compound' if r['value'] else 'not precisely extractable',molecular_weight_basis='identity-specific; existing conversion rechecked',conversion_formula='direct molar value or µmol TE/g × MW(g/mol)/10^6 as documented',conversion_verified='yes' if r['value'] else 'not applicable',identity_form='defined candidate identity; glycosides not pooled',independence_verified='yes',eligibility_rationale=r['notes']))

def add(comp,val,tier,study,year,doi,pmid,loc,exp,reason,probe='fluorescein'):
    sub=next((u['subclass'] for u in universe if u['compound_name']==comp),'')
    records.append(dict(compound=comp,subclass=sub,value_mol_TE_per_mol='' if val is None else f'{val:.3f}',tier=tier,probe=probe,ORAC_arm='H-ORAC',study=study,year=year,PMID=pmid,DOI=doi,Zotero_key='pending_local_import',exact_location=loc,independent_experiment_id=exp,original_unit='mol TE/mol compound' if val is not None else 'not precisely extractable',molecular_weight_basis='not required; original molar ratio',conversion_formula='direct molar value',conversion_verified='yes' if val is not None else 'not applicable',identity_form='pure named compound; glycoside/aglycone retained separately',independence_verified='yes',eligibility_rationale=reason))

# Tabart et al. original comparative study. Anthocyanin remains B2 because optical QC is unresolved.
tab=('Tabart et al., Food Chemistry 2009',2009,'10.1016/j.foodchem.2008.08.013','','original compound-comparison table','TABART2009')
for c,v in [('EGCG',3.4),('Kaempferol',6.2),('Myricetin',3.6),('Naringenin',5.6),('Epicatechin',5.1),('Catechin',7.9),('Quercetin',4.2)]: add(c,v,'B1',*tab,f'Pure compound; AAPH/fluorescein/Trolox method traceable; no severe compound-specific artifact reported.')
add('Cyanidin-3-O-glucoside',7.3,'B2',*tab,'Exact numerical ORAC value exists, but compound-specific inner-filter, spectral overlap, quenching and pH-transformation controls were not sufficiently documented for B1.')

# Zhang et al. original dual-probe study; only fluorescein arm retained.
zh=('Zhang et al., J Phys Chem A 2013',2013,'10.1021/jp307746c','23343226','ORAC-fluorescein results table; pyrogallol-red arm excluded','ZHANG2013')
for c,v in [('EGCG',5.71),('Kaempferol',7.87),('Naringenin',8.04),('Epicatechin',9.97),('Catechin',10.6),('Quercetin',9.51),('Genistein',7.32)]: add(c,v,'B1',*zh,'Pure compound; separate fluorescein arm, AAPH and Trolox; original molar ORAC value.')

# Rothe et al. independent rapid ORAC study of pure hop-related standards.
ro=('Rothe et al., Eur Food Res Technol 2023',2023,'10.1007/s00217-022-04135-3','','ORAC results table for pure standards','ROTHE2023')
for c,v in [('Epicatechin',9.37),('Catechin',10.8),('Rutin',7.4),('p-Coumaric acid',5.0)]: add(c,v,'B1',*ro,'Independent pure-compound ORAC-FL record with molar Trolox normalization.')

# Explicit exclusions found during reference tracing.
for c,v in [('EGCG',4.94),('Kaempferol',5.22),('Quercetin',4.38),('Catechin',6.40)]:
    add(c,v,'C','Ou et al., J Agric Food Chem 2002 HORAC paper',2002,'10.1021/jf011480w','11982397','reported in hydroxyl radical prevention assay','OU_HORAC_2002','Excluded: fluorescein probe was used in HORAC (hydroxyl-radical prevention), not AAPH peroxyl ORAC-FL.')

write(D/'Top20_Evidence_Consolidation_Records.csv',records)

def vals_for(c):
    vals=[]; ids=set()
    for r in records:
        if r['compound']==c and r['tier'] in ('A','B1') and r['value_mol_TE_per_mol']:
            if r['independent_experiment_id'] not in ids:
                vals.append(float(r['value_mol_TE_per_mol']));ids.add(r['independent_experiment_id'])
    return vals

new=[]
for u in universe:
    vs=vals_for(u['compound_name'])
    if vs:new.append((u['compound_name'],statistics.median(vs),len(vs),min(vs),max(vs)))
new.sort(key=lambda x:x[1],reverse=True); newtop=new[:20]; newpos={x[0]:i+1 for i,x in enumerate(newtop)}
allnames=list(dict.fromkeys([x['compound_name'] for x in oldrank]+[x[0] for x in newtop]))
ba=[]
for n in allnames:
    o=old.get(n); a=next((x for x in newtop if x[0]==n),None); nb=len(vals_for(n)); oldn=int(o['n_eligible_studies']) if o else 0
    ba.append(dict(compound=n,rank_before=o['provisional_rank'] if o else '',rank_after=newpos.get(n,''),rank_change=(int(o['provisional_rank'])-newpos[n]) if o and n in newpos else '',median_before=o['median_ORAC_mol_TE_per_mol'] if o else '',median_after=f'{a[1]:.3f}' if a else '',n_B1_before=oldn,n_B1_after=nb,confidence_before=o['confidence'] if o else 'Not ranked',confidence_after=('High' if nb>=3 else 'Moderate' if nb==2 else 'Low' if nb==1 else 'Not ranked'),entered_Top20='yes' if not o and a else 'no',exited_Top20='yes' if o and not a else 'no',change_driver='new independent B1 records' if nb>oldn else 'none; existing estimate retained'))
write(D/'Top20_Ranking_Before_After.csv',ba)

missing=[
('EGCG','flavan-3-ols','major dietary tea catechin; high mechanistic relevance','green tea','yes','yes','B1 found after probe-specific tracing','older β-phycoerythrin, HORAC and figure-only records excluded','high'),
('Kaempferol','flavonols','common food flavonol and structural comparator','leafy vegetables; tea; legumes','yes','yes','B1 found; cyclodextrin-dependent values require separation','limited solubility and cyclodextrin effects','high'),
('Myricetin','flavonols','tri-hydroxylated B-ring; important structure–activity comparator','berries; tea; wine','yes','yes','one B1 found; remains single-study','solubility and cyclodextrin sensitivity','high'),
('Cyanidin-3-O-glucoside','anthocyanidins / anthocyanins','major dietary anthocyanin','berries; black rice; red cabbage','yes','no','B2 exact value only; optical QC insufficient','inner-filter, spectral overlap, quenching, pH transformation','very high'),
('Naringenin','flavanones','common citrus aglycone representative','citrus foods','yes','yes','two independent B1 found','low water solubility; solvent must be locked','high'),
('Secoisolariciresinol','lignans','major dietary parent lignan','flaxseed; sesame; whole grains','yes','no','no usable original ORAC-FL value located','parent identity/solubility; do not substitute enterodiol/enterolactone','very high')]
mf=['compound','subclass','why_scientifically_important','food_relevance','search_completed','eligible_B1_found','reason_missing','method_limitation','future_retest_priority']
write(D/'High_Importance_Missing_ORAC_Candidates.csv',[dict(zip(mf,x)) for x in missing],mf)

short=[]
risk_override={'EGCG':'historical probe/arm misclassification; two eligible B1 now traced','Kaempferol':'limited solubility and cyclodextrin-dependent values','Naringenin':'limited water solubility; cosolvent must be locked','Myricetin':'limited solubility and cyclodextrin sensitivity'}
for c,med,n,lo,hi in newtop:
    risk=risk_override.get(c,next((u['special_case_flag'] for u in universe if u['compound_name']==c),'') or 'no major unresolved concern documented')
    stable='high' if n>=3 and hi/lo<2 else 'moderate' if n>=2 else 'low'
    ready='Ready for target mapping' if n>=2 and 'optical' not in risk else 'Conditionally ready'
    short.append(dict(compound=c,provisional_rank=newpos[c],ORAC_median=f'{med:.3f}',B1_count=n,confidence='High' if n>=3 else 'Moderate' if n==2 else 'Low',rank_stability=stable,assay_risk=risk,target_mapping_readiness=ready,rationale='Independent B1 depth supports shortlist freezing.' if ready.startswith('Ready') else 'Single-study ORAC-FL estimate; retain with explicit uncertainty.'))
write(D/'Target_Mapping_Shortlist_v0.1.csv',short)

# Figures
FONT='C:/Windows/Fonts/arial.ttf'; BOLD='C:/Windows/Fonts/arialbd.ttf'
def ft(n,b=False):return ImageFont.truetype(BOLD if b else FONT,n)
def base(w,h,t,s):
    im=Image.new('RGB',(w,h),'white');d=ImageDraw.Draw(im);d.text((50,25),t,font=ft(30,1),fill='#17233b');d.text((50,65),s,font=ft(15),fill='#526074');return im,d

im,d=base(1600,1400,'Top 20 before–after rank comparison','Before and after ranks; entrants and exits are retained for audit')
for i,x in enumerate(sorted(ba,key=lambda z:int(z['rank_after']) if z['rank_after'] else 99)):
    y=120+i*48; d.text((20,y),x['compound'],font=ft(14),fill='#17233b');
    if x['rank_before']: d.ellipse((430+int(x['rank_before'])*25-5,y-5,430+int(x['rank_before'])*25+5,y+5),fill='#8aa2b8')
    if x['rank_after']:
        xa=1020+int(x['rank_after'])*25; d.rectangle((xa-5,y-5,xa+5,y+5),fill='#2a9d8f')
        if x['rank_before']: d.line((430+int(x['rank_before'])*25,y,xa,y),fill='#d7dde5',width=2)
    d.text((400,y-9),str(x['rank_before'] or '-'),font=ft(13),fill='#526074'); d.text((990,y-9),str(x['rank_after'] or '-'),font=ft(13),fill='#1f7568')
d.text((430,92),'Before',font=ft(16,1),fill='#526074');d.text((1020,92),'After',font=ft(16,1),fill='#1f7568');im.save(F/'Top20_Before_After_Rank_Comparison.png')

im,d=base(1500,1120,'Top 20 B1 evidence depth','B1 count is independent from ORAC magnitude')
for i,x in enumerate(short):
    y=115+i*47;d.text((20,y),f"{x['provisional_rank']:>2}. {x['compound']}",font=ft(14),fill='#17233b');
    for j in range(x['B1_count']):d.rectangle((390+j*42,y,420+j*42,y+17),fill='#2a9d8f')
    d.text((690,y),str(x['B1_count']),font=ft(14,1),fill='#17233b');d.text((780,y),x['confidence'],font=ft(14),fill='#b02a37' if x['confidence']=='Low' else '#1f7568');d.text((1000,y),x['target_mapping_readiness'].replace(' for target mapping',''),font=ft(13),fill='#526074')
im.save(F/'Top20_B1_Evidence_Depth.png')

im,d=base(1600,650,'Missing key phenolics: ORAC-FL status','Probe identity and assay artifacts govern eligibility')
status={'EGCG':'B1 found','Kaempferol':'B1 found','Myricetin':'B1 found','Cyanidin-3-O-glucoside':'B2 only · optical concern','Naringenin':'B1 found','Secoisolariciresinol':'no usable data'}
cols={'B1 found':'#2a9d8f','B2 only · optical concern':'#e9c46a','no usable data':'#d66b5d'}
for i,(c,s) in enumerate(status.items()):
    y=120+i*78;d.text((30,y),c,font=ft(18,1),fill='#17233b');d.rounded_rectangle((430,y-5,1050,y+35),10,fill=cols[s]);d.text((455,y+3),s,font=ft(17,1),fill='white' if s!='B2 only · optical concern' else '#4b3b12')
    note=next(x[-2] for x in missing if x[0]==c);d.text((1080,y+2),note,font=ft(12),fill='#526074')
im.save(F/'Missing_Key_Phenolics_ORAC_Status.png')

print({'records':len(records),'after_eligible':len(new),'top20':len(newtop),'ready':sum(x['target_mapping_readiness'].startswith('Ready') for x in short),'conditional':sum(x['target_mapping_readiness'].startswith('Conditionally') for x in short)})
