import csv, json, math, statistics
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'; FIG=ROOT/'figures'; DOC=ROOT/'docs'; HAND=ROOT/'handoff'
for p in (DATA,FIG,DOC,HAND): p.mkdir(exist_ok=True)

with open(DATA/'pubchem_h_orac_phenolics.json',encoding='utf-8') as f: pub=json.load(f)
patch={
'Chlorogenic acid':dict(CID=1794427,InChIKey='CWVRJTMFETXNAD-JUHZACGLSA-N'),
'Rosmarinic acid':dict(CID=5281792,InChIKey='DOUMFZQKYFQNTF-WUTVXBCWSA-N'),
'Gentisic acid':dict(CID=3469,InChIKey='WXTMDXOMEHJXQO-UHFFFAOYSA-N'),
'4-Hydroxybenzoic acid':dict(CID=135,InChIKey='FJKROLUGYXJWQN-UHFFFAOYSA-N')}

# name, PubChem query key, subclass, form, stereochemistry, food sources, special flag
C=[
('Catechin','(+)-Catechin','flavan-3-ols','aglycone','(+); 2R,3S','tea; cocoa; apples',''),
('Epicatechin','(-)-Epicatechin','flavan-3-ols','aglycone','(-); 2R,3R','tea; cocoa; apples',''),
('EGCG','(-)-Epigallocatechin gallate','flavan-3-ols','gallate ester','defined catechin stereochemistry','green tea','no eligible ORAC-FL; classic numeric source used non-FL probe'),
('Epigallocatechin','(-)-Epigallocatechin','flavan-3-ols','aglycone','(-); 2R,3R','green tea','non-FL historical ORAC source excluded'),
('Epicatechin gallate','(-)-Epicatechin gallate','flavan-3-ols','gallate ester','defined catechin stereochemistry','tea','non-FL historical ORAC source excluded'),
('Gallocatechin','Gallocatechin','flavan-3-ols','aglycone','defined catechin stereochemistry','tea',''),
('Quercetin','Quercetin','flavonols','aglycone','achiral','onions; capers; apples','hydrate/form heterogeneity'),
('Kaempferol','Kaempferol','flavonols','aglycone','achiral','kale; tea; beans','non-FL historical ORAC source excluded'),
('Myricetin','Myricetin','flavonols','aglycone','achiral','berries; tea; wine',''),
('Isorhamnetin','Isorhamnetin','flavonols','aglycone','achiral','onions; pears; sea buckthorn',''),
('Fisetin','Fisetin','flavonols','aglycone','achiral','strawberries; apples; persimmon',''),
('Quercitrin','Quercitrin','flavonols','glycoside','quercetin-3-O-rhamnoside','buckwheat; berries; tea','kept separate from quercetin'),
('Rutin','Rutin','flavonols','glycoside','quercetin-3-O-rutinoside','buckwheat; citrus; apples','kept separate from quercetin'),
('Luteolin','Luteolin','flavones','aglycone','achiral','celery; peppers; herbs',''),
('Apigenin','Apigenin','flavones','aglycone','achiral','parsley; celery; chamomile',''),
('Naringenin','Naringenin','flavanones','aglycone','2S record identity','citrus','non-FL historical ORAC source excluded'),
('Hesperetin','Hesperetin','flavanones','aglycone','2S record identity','citrus','kept separate from hesperidin'),
('Eriodictyol','Eriodictyol','flavanones','aglycone','2S record identity','citrus; herbs',''),
('Hesperidin','Hesperidin','flavanones','glycoside','hesperetin-7-O-rutinoside','citrus peel and juice','kept separate from hesperetin'),
('Cyanidin','Cyanidin','anthocyanidins / anthocyanins','aglycone anthocyanidinium','achiral cation','berries; red cabbage','optical/color and pH interference risk'),
('Cyanidin-3-O-glucoside','Cyanidin 3-O-glucoside','anthocyanidins / anthocyanins','glycoside','defined glucoside; chloride record','berries; black rice; red cabbage','optical/color and pH interference; kept separate from cyanidin'),
('Delphinidin','Delphinidin','anthocyanidins / anthocyanins','aglycone anthocyanidinium','achiral cation','berries; purple vegetables','optical/color and pH interference risk'),
('Pelargonidin','Pelargonidin','anthocyanidins / anthocyanins','aglycone anthocyanidinium','achiral cation','strawberries; radish','optical/color and pH interference risk'),
('Malvidin','Malvidin','anthocyanidins / anthocyanins','aglycone anthocyanidinium','achiral cation','grapes; red wine; berries','optical/color and pH interference risk'),
('Genistein','Genistein','isoflavones','aglycone','achiral','soy foods; legumes','kept separate from genistin'),
('Daidzein','Daidzein','isoflavones','aglycone','achiral','soy foods; legumes','kept separate from daidzin'),
('Glycitein','Glycitein','isoflavones','aglycone','achiral','soy foods',''),
('Gallic acid','Gallic acid','phenolic acids—hydroxybenzoic','free acid','achiral','berries; grapes; tea',''),
('Protocatechuic acid','Protocatechuic acid','phenolic acids—hydroxybenzoic','free acid','achiral','berries; olives; grains',''),
('Gentisic acid','Gentisic acid','phenolic acids—hydroxybenzoic','free acid','achiral','fruits; cereals; gentian-derived foods',''),
('4-Hydroxybenzoic acid','4-Hydroxybenzoic acid','phenolic acids—hydroxybenzoic','free acid','achiral','berries; cereals; wine',''),
('Vanillic acid','Vanillic acid','phenolic acids—hydroxybenzoic','free acid','achiral','vanilla; fruits; grains',''),
('Syringic acid','Syringic acid','phenolic acids—hydroxybenzoic','free acid','achiral','grapes; olives; spices',''),
('Caffeic acid','Caffeic acid','phenolic acids—hydroxycinnamic','free acid','trans','coffee; fruits; vegetables',''),
('Ferulic acid','trans-Ferulic acid','phenolic acids—hydroxycinnamic','free acid','trans','whole grains; coffee; vegetables',''),
('p-Coumaric acid','p-Coumaric acid','phenolic acids—hydroxycinnamic','free acid','trans','grains; fruits; vegetables',''),
('Sinapic acid','Sinapic acid','phenolic acids—hydroxycinnamic','free acid','as PubChem record','mustard; canola; brassicas','graph-only ORAC-FL source not ranked'),
('Rosmarinic acid','Rosmarinic acid','phenolic acids—hydroxycinnamic','ester/conjugate','defined rosmarinic acid stereochemistry','rosemary; basil; oregano',''),
('Chlorogenic acid','Chlorogenic acid','hydroxycinnamic-acid conjugates','5-O-caffeoylquinic acid','defined caffeoylquinic isomer','coffee; apples; potatoes','isomer identity locked'),
('Neochlorogenic acid','Neochlorogenic acid','hydroxycinnamic-acid conjugates','3-O-caffeoylquinic acid','defined caffeoylquinic isomer','stone fruits; berries; coffee','isomer identity locked'),
('Cryptochlorogenic acid','Cryptochlorogenic acid','hydroxycinnamic-acid conjugates','4-O-caffeoylquinic acid','defined caffeoylquinic isomer','coffee; fruits','isomer identity locked'),
('trans-Resveratrol','trans-Resveratrol','stilbenes','aglycone','trans','grapes; peanuts; wine','photoisomerization risk'),
('Secoisolariciresinol','Secoisolariciresinol','lignans','aglycone','defined lignan stereochemistry','flaxseed; sesame; whole grains','sparse ORAC-FL coverage'),
('Sesamol','Sesamol','other phenolics','aglycone','achiral','sesame seeds and oil',''),
('Curcumin','Curcumin','other phenolics','aglycone','predominantly trans enone form','turmeric','limited water solubility; optical interference risk'),
('Capsaicin','Capsaicin','other phenolics','aglycone','trans side chain','chili peppers','limited water solubility'),
('Carvacrol','Carvacrol','other phenolics','aglycone','achiral','oregano; thyme','volatile; limited water solubility'),
('Thymol','Thymol','other phenolics','aglycone','achiral','thyme; oregano','volatile; limited water solubility'),
('Eugenol','Eugenol','other phenolics','aglycone','achiral','cloves; cinnamon; basil','volatile; limited water solubility'),
('Tyrosol','Tyrosol','other phenolics','aglycone','achiral','olives; olive oil; wine','')]

def ident(key):
    d=pub.get(key,{})
    if 'error' in d or not d: d=patch.get(key,{})
    return str(d.get('CID','')),d.get('InChIKey','')

R=[]
def rec(name,val,tier,pmid,doi,study,year,loc,zkey,notes=''):
    R.append(dict(compound_name=name,value=val,tier=tier,PMID=pmid,DOI=doi,study=study,year=year,exact_location=loc,Zotero_key=zkey,notes=notes))

# Existing adjudicated original ORAC-FL records.
with open(DATA/'ORAC_Pilot_Reclassified_A_B1_B2.csv',encoding='utf-8-sig') as f:
  for x in csv.DictReader(f):
    nm=x['compound_name']
    if nm in {'Catechin','Epicatechin','Quercetin','Gallic acid','Caffeic acid','Ferulic acid','Chlorogenic acid','Resveratrol','trans-Resveratrol'}:
      nm='trans-Resveratrol' if nm in {'Resveratrol','trans-Resveratrol'} else nm
      rec(nm,float(x['standardized_ORAC_mol_TE_per_mol']) if x['standardized_ORAC_mol_TE_per_mol'] else None,x['new_tier'],x['PMID'],x['DOI'],x['study'],x['publication_year'],x['exact_location'],x['Zotero_key'],x['notes'])

ou=('11599998','10.1021/jf010586o','Ou, Hampsch-Woodill & Prior, J Agric Food Chem 2001',2001,'Table 4, p. 4622','4FIGEV33')
for n,v in [('Quercitrin',6.47),('Genistein',5.93),('Rutin',6.01)]: rec(n,v,'B1',*ou)
pa=('36752411','10.1093/chromsci/bmad007','Paillat et al., J Chromatogr Sci 2023',2023,'Table I: microplate ORAC; value converted from µmol TE/g using molecular weight','pending_local_import')
rec('Luteolin',3.264,'B1',*pa)
sa=('','10.1039/D1RA08918H','Sakurai et al., RSC Advances 2022',2022,'Table 1; standardized H-ORAC SOP','pending_local_import')
for n,v in [('Gentisic acid',5.475),('p-Coumaric acid',3.766),('Ferulic acid',3.474),('4-Hydroxybenzoic acid',3.299),('Sesamol',2.107),('Eugenol',1.811),('Tyrosol',1.131),('Carvacrol',0.829),('Thymol',0.545)]: rec(n,v,'B1',*sa)

# Non-ranking evidence retained for audit.
hen=('12881018','10.1207/S15327914NC4502_13','Henning et al., Nutr Cancer 2003',2003,'original article numerical table; β-phycoerythrin probe, not ORAC-FL','pending_local_import')
for n,v in [('EGCG',8.2),('Epigallocatechin',4.6),('Epicatechin gallate',10.4),('Kaempferol',2.6),('Naringenin',2.4)]: rec(n,v,'C',*hen,notes='Excluded: β-phycoerythrin probe; not fluorescein ORAC-FL.')
for n in ['EGCG','Cyanidin-3-O-glucoside','Sinapic acid']:
    rec(n,None,'B2','','','Poly-acylated anthocyanin comparative ORAC-FL study',2010,'Figure 3 only; exact value not tabulated','pending_local_import','Quantitative graph only; exact original numerical value not safely extractable.')

# Vitamin C benchmark, excluded from candidate rank.
benchmark=[0.95,0.53]

def write_csv(path,rows,fields):
    with open(path,'w',newline='',encoding='utf-8-sig') as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)

write_csv(DATA/'H_ORAC_Phenolic_Literature_Records.csv',R,list(R[0]))

def quartiles(vals):
    if len(vals)<4:return ''
    q=statistics.quantiles(vals,n=4,method='inclusive'); return f'{q[0]:.3f}–{q[2]:.3f}'

universe=[]
for name,key,sub,form,stereo,foods,special in C:
    rr=[r for r in R if r['compound_name']==name]
    vals=[r['value'] for r in rr if r['tier'] in ('A','B1') and r['value'] is not None]
    cid,ik=ident(key)
    universe.append(dict(compound_name=name,synonym=key,PubChem_CID=cid,InChIKey=ik,chemical_class='Phenolic/polyphenolic compounds',subclass=sub,parent_or_glycoside=form,stereochemistry=stereo,representative_food_sources=foods,food_occurrence_verified='yes',H_ORAC_compatibility='compatible with fixed solvent/QC' if special else 'compatible',special_case_flag=special,Tier_A_count=sum(r['tier']=='A' for r in rr),Tier_B1_count=sum(r['tier']=='B1' for r in rr),Tier_B2_count=sum(r['tier']=='B2' for r in rr),Tier_C_X_count=sum(r['tier'] in ('C','X') for r in rr),standardized_ORAC_values='; '.join(f"{v:.3f}" for v in vals),median_ORAC=f'{statistics.median(vals):.3f}' if vals else '',min_ORAC=f'{min(vals):.3f}' if vals else '',max_ORAC=f'{max(vals):.3f}' if vals else '',IQR=quartiles(vals),confidence=('High' if len(vals)>=3 else 'Moderate' if len(vals)==2 else 'Low' if len(vals)==1 else 'Very low / not rankable'),ranking_eligible='yes' if vals else 'no',ranking_status=('eligible; single-study estimate' if len(vals)==1 else 'eligible; multi-study median' if len(vals)>1 else 'not eligible'),PMID='; '.join(sorted(set(r['PMID'] for r in rr if r['PMID']))),DOI='; '.join(sorted(set(r['DOI'] for r in rr if r['DOI']))),Zotero_key='; '.join(sorted(set(r['Zotero_key'] for r in rr if r['Zotero_key']))),notes='; '.join(filter(None,[special,'A/B1 only used for ranking; distinct glycosides/aglycones not pooled.']))))

uf=list(universe[0]); write_csv(DATA/'H_ORAC_Phenolic_Candidate_Universe.csv',universe,uf)
eligible=sorted([x for x in universe if x['ranking_eligible']=='yes'],key=lambda x:float(x['median_ORAC']),reverse=True)
ranking=[]
for i,x in enumerate(eligible,1):
    vals=[r['value'] for r in R if r['compound_name']==x['compound_name'] and r['tier'] in ('A','B1') and r['value'] is not None]
    sources=sorted(set(f"{r['study']} ({r['DOI']})" for r in R if r['compound_name']==x['compound_name'] and r['tier'] in ('A','B1')))
    ratio=max(vals)/min(vals) if len(vals)>1 and min(vals)>0 else 1
    ranking.append(dict(provisional_rank=i,compound_name=x['compound_name'],subclass=x['subclass'],n_eligible_studies=len(vals),median_ORAC_mol_TE_per_mol=f'{statistics.median(vals):.3f}',range=f'{min(vals):.3f}–{max(vals):.3f}',IQR=quartiles(vals),confidence=x['confidence'],single_study_flag='yes' if len(vals)==1 else 'no',heterogeneity_flag='high' if ratio>=2 else 'moderate' if ratio>=1.3 else 'low/not estimable',key_sources=' | '.join(sources),caveat='Exploratory literature-derived ORAC-FL; non-identical protocols; no inference to human efficacy.'))
write_csv(DATA/'H_ORAC_Provisional_Ranking.csv',ranking,list(ranking[0]))

FONT='C:/Windows/Fonts/arial.ttf'; BOLD='C:/Windows/Fonts/arialbd.ttf'
def font(n,b=False): return ImageFont.truetype(BOLD if b else FONT,n)
def canvas(w,h,title,subtitle):
    im=Image.new('RGB',(w,h),'white'); d=ImageDraw.Draw(im); d.text((55,28),title,font=font(32,True),fill='#16233a'); d.text((55,72),subtitle,font=font(16),fill='#526074'); return im,d
colors={'flavan-3-ols':'#2a9d8f','flavonols':'#457b9d','flavones':'#6a4c93','isoflavones':'#e76f51','phenolic acids—hydroxybenzoic':'#f4a261','phenolic acids—hydroxycinnamic':'#e9c46a','hydroxycinnamic-acid conjugates':'#8ab17d','stilbenes':'#d65a72','other phenolics':'#777777'}
im,d=canvas(1800,1250,'Provisional H-ORAC phenolic Top 20','Original ORAC-FL Tier A/B1 only · mol Trolox equivalents/mol compound')
left,top,right,bottom=330,125,1710,1130; xmax=max(r['value'] for r in R if r['tier'] in ('A','B1') and r['value'] is not None and r['compound_name'] in {x['compound_name'] for x in ranking})*1.08
d.line((left,top,left,bottom),fill='#8793a5',width=2)
for tick in range(0,19,3):
    x=left+(right-left)*tick/xmax; d.line((x,top,x,bottom),fill='#e3e7ed'); d.text((x-8,bottom+8),str(tick),font=font(14),fill='#445')
for j,x in enumerate(reversed(ranking)):
    y=top+20+j*(bottom-top-40)/(len(ranking)-1); vals=[r['value'] for r in R if r['compound_name']==x['compound_name'] and r['tier'] in ('A','B1') and r['value'] is not None]
    col=colors.get(x['subclass'],'#777'); d.text((15,y-10),f"{x['provisional_rank']:>2}. {x['compound_name']}",font=font(16),fill='#172033')
    if len(vals)>1:d.line((left+(right-left)*min(vals)/xmax,y,left+(right-left)*max(vals)/xmax,y),fill=col,width=4)
    for v in vals:d.ellipse((left+(right-left)*v/xmax-5,y-5,left+(right-left)*v/xmax+5,y+5),fill=col)
    med=float(x['median_ORAC_mol_TE_per_mol']); xx=left+(right-left)*med/xmax
    d.rectangle((xx-6,y-6,xx+6,y+6),outline='#101820',width=2,fill='white' if x['single_study_flag']=='yes' else col)
    d.text((right+8,y-9),x['confidence']+(' · single' if x['single_study_flag']=='yes' else ''),font=font(13),fill='#526074')
bx=left+(right-left)*statistics.median(benchmark)/xmax; d.line((bx,top,bx,bottom),fill='#d62828',width=3); d.text((bx+8,top+4),'Vitamin C benchmark: median 0.74 (excluded)',font=font(14,True),fill='#d62828')
d.text((55,1185),'Each circle = independent original A/B1 record; square = median. Hollow square denotes single-study evidence. Literature protocols are broadly comparable, not identical.',font=font(15),fill='#3f4d5f')
im.save(FIG/'H_ORAC_Provisional_Top20.png')

im,d=canvas(1700,1180,'H-ORAC evidence confidence','Tier counts and stability are shown separately from capacity values')
left,top=420,130
for j,x in enumerate(ranking):
    y=top+j*48; d.text((25,y),f"{x['provisional_rank']:>2}. {x['compound_name']}",font=font(15),fill='#172033')
    u=next(z for z in universe if z['compound_name']==x['compound_name']); counts=[u['Tier_A_count'],u['Tier_B1_count'],u['Tier_B2_count']]
    for k,(lab,c,col) in enumerate(zip(['A','B1','B2'],counts,['#264653','#2a9d8f','#e9c46a'])):
        xx=left+k*210; d.text((xx,y),lab,font=font(14,True),fill=col); d.rectangle((xx+35,y,xx+35+int(c)*55,y+18),fill=col); d.text((xx+45+int(c)*55,y),str(c),font=font(14),fill='#333')
    d.text((1100,y),x['confidence'],font=font(15,True),fill='#a33' if x['confidence']=='Low' else '#2b6f5c'); d.text((1280,y),'single study' if x['single_study_flag']=='yes' else x['heterogeneity_flag'],font=font(14),fill='#526074')
d.text((55,1125),'Confidence is not combined with ORAC magnitude. Tier A=0 for every candidate; most estimates remain single-study.',font=font(16),fill='#3f4d5f')
im.save(FIG/'H_ORAC_Evidence_Confidence.png')

groups=['flavan-3-ols','flavonols','flavones','flavanones','anthocyanidins / anthocyanins','isoflavones','phenolic acids—hydroxybenzoic','phenolic acids—hydroxycinnamic','hydroxycinnamic-acid conjugates','stilbenes','lignans','other phenolics']
im,d=canvas(1800,950,'H-ORAC subclass coverage','Candidate generation breadth versus A/B1 eligibility')
for i,g in enumerate(groups):
    xs=[x for x in universe if x['subclass']==g]; el=sum(x['ranking_eligible']=='yes' for x in xs); miss=len(xs)-el; y=130+i*62
    d.text((25,y),g,font=font(15),fill='#172033'); d.rectangle((440,y,440+len(xs)*45,y+16),fill='#457b9d'); d.rectangle((850,y,850+el*45,y+16),fill='#2a9d8f'); d.rectangle((1260,y,1260+miss*45,y+16),fill='#d8a25e')
    d.text((450+len(xs)*45,y-2),str(len(xs)),font=font(14),fill='#333'); d.text((860+el*45,y-2),str(el),font=font(14),fill='#333'); d.text((1270+miss*45,y-2),str(miss),font=font(14),fill='#333')
d.text((440,95),'Candidates',font=font(17,True),fill='#457b9d'); d.text((850,95),'Eligible A/B1',font=font(17,True),fill='#2a9d8f'); d.text((1260,95),'Missing A/B1',font=font(17,True),fill='#a66b20')
d.text((55,895),'Low eligibility in anthocyanins, flavanones and lignans reflects literature/method coverage and optical/solubility constraints, not proven weak antioxidant chemistry.',font=font(15),fill='#3f4d5f')
im.save(FIG/'H_ORAC_Subclass_Coverage.png')

print(json.dumps({'candidate_count':len(universe),'eligible_count':len(eligible),'ranking_count':len(ranking),'records':len(R)},ensure_ascii=False))
