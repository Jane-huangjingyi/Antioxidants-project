import csv, math, statistics
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
DATA, FIG, DOC, HAND = ROOT/'data', ROOT/'figures', ROOT/'docs', ROOT/'handoff'
for p in (DATA, FIG, DOC, HAND): p.mkdir(exist_ok=True)

def read_csv(p):
    with open(p, encoding='utf-8-sig', newline='') as f: return list(csv.DictReader(f))
def write_csv(p, rows, fields):
    with open(p,'w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)
def fnt(size,bold=False):
    candidates=[Path('C:/Windows/Fonts/arialbd.ttf' if bold else 'C:/Windows/Fonts/arial.ttf'),Path('C:/Windows/Fonts/msyhbd.ttc' if bold else 'C:/Windows/Fonts/msyh.ttc')]
    for p in candidates:
        if p.exists(): return ImageFont.truetype(str(p),size)
    return ImageFont.load_default()
def quantile(vals,q):
    if not vals:return None
    vals=sorted(vals); pos=(len(vals)-1)*q; lo=math.floor(pos); hi=math.ceil(pos)
    return vals[lo] if lo==hi else vals[lo]*(hi-pos)+vals[hi]*(pos-lo)

pilot=read_csv(DATA/'ORAC_Pilot_TierA_Analysis.csv')
raw=read_csv(DATA/'ORAC_Pilot_Raw_Extraction.csv')
cuprac={r['compound_name']:r for r in read_csv(DATA/'CUPRAC_Coverage_Summary.csv')}
ident={r['compound_name']:r for r in pilot}

# Re-adjudicate every existing Tier B record. The new B1 policy permits missing numerical
# purity and a few reading details when assay identity and major conditions remain auditable.
for r in raw:
    r.update(old_tier='B',new_tier='B1',B1_eligibility_yes_no='yes',
             missing_fields='numerical purity; compound-specific spectral QC' if 'H-ORAC' in r['ORAC_arm'] else 'numerical purity; exact AAPH/fluorescein concentrations and reading schedule not verified in accessible text',
             critical_method_fields_present='identity; ORAC-FL; arm; AAPH; fluorescein; Trolox; 37 C; major buffer/solvent; molar unit; primary source',
             interference_concern='none evident; residual untested optical effects' if 'H-ORAC' in r['ORAC_arm'] else 'RMCD/solubility dependence retained; no reported severe artifact',
             rationale='Meets B1 minimum; missing fields are noncritical for exploratory use. Formal Tier A remains unmet.',
             inclusion_in_exploratory_plot='yes')

def add(compound,value,unit,std,study,year,doi,pmid,loc,arm,form,purity,aaph,fl,trolox,buffer,ph,temp,solvent,interval,duration,auc,crange,linearity,interference,missing,rationale,zkey='pending_local_import'):
    b=ident[compound]
    raw.append({
      'compound_name':compound,'synonym':b['synonym'],'PubChem_CID':b['PubChem_CID'],'InChIKey':b['InChIKey'],
      'chemical_class':b['chemical_class'],'subclass':b['subclass'],'food_source_examples':b['food_source_examples'],
      'ORAC_arm':arm,'H_ORAC_or_L_ORAC':arm,'compound_form':form,'stereochemistry':form,'purity':purity,
      'original_ORAC_value':value,'original_unit':unit,'molar_conversion_possible':'yes','standardized_ORAC_mol_TE_per_mol':std,
      'AAPH_concentration':aaph,'fluorescein_concentration':fl,'Trolox_concentration':trolox,'buffer':buffer,'pH':ph,'temperature':temp,
      'solvent':solvent,'solubilizer_RMCD':'none','reading_interval':interval,'total_duration':duration,'AUC_method':auc,
      'concentration_range':crange,'linearity_reported':linearity,'interference_noted':interference,
      'PMID':pmid,'DOI':doi,'publication_year':str(year),'study':study,'Zotero_key':zkey,'exact_location':loc,'comparability_tier':'B1',
      'notes':rationale,'old_tier':'not_measured','new_tier':'B1','B1_eligibility_yes_no':'yes','missing_fields':missing,
      'critical_method_fields_present':'identity; ORAC-FL; H arm; AAPH; fluorescein; Trolox; 37 C; buffer/solvent; molar-convertible value; primary source',
      'interference_concern':interference,'rationale':rationale,'inclusion_in_exploratory_plot':'yes'})

common=dict(arm='H-ORAC',form='specified stereoisomer',purity='source/supplier stated; numerical purity not reported',aaph='31.7 mM added solution',fl='94.4 nM',trolox='6.25, 12.5, 25, 50 uM',buffer='75 mM Na2HPO4-NaH2PO4 phosphate',ph='7.0',temp='37 C',solvent='acetone/water/acetic acid 70:29.5:0.5 stock; diluted in buffer',interval='2 min',duration='90 min',auc='net AUC relative to Trolox',crange='compound-specific concentration not tabulated in extracted text',linearity='not compound-specific',interference='no severe artifact reported; compound-specific optical QC absent',missing='numerical purity; compound-specific concentration/linearity and optical QC')
add('Catechin','9.0','mol TE/mol compound','9.0','Ishimoto et al., Biosci Biotechnol Biochem 76:395-399',2012,'10.1271/bbb.110717','22313776','Results text, p. 397; ORAC methods, p. 395',rationale='Original ORAC-FL value and full assay identity are traceable; retained as B1 because compound-specific purity/linearity/QC are incomplete.',**common)
add('Epicatechin','10.0','mol TE/mol compound','10.0','Ishimoto et al., Biosci Biotechnol Biochem 76:395-399',2012,'10.1271/bbb.110717','22313776','Results text, p. 397; ORAC methods, p. 395',rationale='Original ORAC-FL value and full assay identity are traceable; retained as B1 because compound-specific purity/linearity/QC are incomplete.',**common)

# Paillat et al. microplate values are mass-normalized in Table I and converted using
# compound molecular weight: (umol TE/g)*(g/mol)/1e6 = mol TE/mol.
for compound,val,mw in [('Resveratrol',25462,228.24),('Ferulic acid',14272,194.18)]:
    std=round(val*mw/1_000_000,3)
    add(compound,str(val),'umol TE/g compound',str(std),'Paillat et al., J Chromatogr Sci 61:530-538',2023,'10.1093/chromsci/bmad007','36752411','Table I (microplate ORAC values); Materials/Methods and Supplementary methods',
        'H-ORAC','trans-isomer/free acid as named','supplier stated; numerical purity not reported','AAPH confirmed; exact microplate final concentration in supplementary method','fluorescein confirmed; exact microplate final concentration in supplementary method','Trolox-equivalent calibration used','phosphate buffer','7.4','37 C (reagent incubation; microplate protocol traceable)','DMSO/acetonitrile/water 10:45:45 stock','kinetic microplate; exact interval in supplementary method','complete-curve microplate assay; exact duration in supplementary method','microplate ORAC TE value; converted from mass to molar basis','12.5-50 mg/L' if compound=='Resveratrol' else '12.5-100 mg/L','R2 0.9918' if compound=='Resveratrol' else 'R2 0.9996','residual solvent/solubility concern; no severe artifact reported','numerical purity; some microplate reading details require supplement',
        'Original primary-paper Table I value, fully molar-convertible. Major assay identity is available; retained as B1 while detailed microplate schedule remains supplementary.',zkey='pending_local_import')

# Targeted-search outcomes that have quantitative reports but fail B1 are represented as B2.
def add_b2(compound,study,year,doi,pmid,arm,value,unit,reason,loc):
    b=ident[compound]
    raw.append({'compound_name':compound,'synonym':b['synonym'],'PubChem_CID':b['PubChem_CID'],'InChIKey':b['InChIKey'],'chemical_class':b['chemical_class'],'subclass':b['subclass'],'food_source_examples':b['food_source_examples'],'ORAC_arm':arm,'H_ORAC_or_L_ORAC':arm,'compound_form':b['synonym'],'stereochemistry':'as named','purity':'not adequately reported','original_ORAC_value':value,'original_unit':unit,'molar_conversion_possible':'no','standardized_ORAC_mol_TE_per_mol':'','AAPH_concentration':'reported','fluorescein_concentration':'reported','Trolox_concentration':'reported','buffer':'reported','pH':'reported/kit dependent','temperature':'37 C','solvent':'reported incompletely for compound-specific interpretation','solubilizer_RMCD':'','reading_interval':'reported','total_duration':'reported','AUC_method':'reported','concentration_range':'single/reporting basis not suitable for molar conversion','linearity_reported':'no compound-specific linearity','interference_noted':reason,'PMID':pmid,'DOI':doi,'publication_year':str(year),'study':study,'Zotero_key':'not_imported_not_formally_used','exact_location':loc,'comparability_tier':'B2','notes':reason,'old_tier':'not_measured','new_tier':'B2','B1_eligibility_yes_no':'no','missing_fields':'reliable mol TE/mol conversion; compound-specific linearity/QC','critical_method_fields_present':'compound; ORAC-FL; AAPH; fluorescein; Trolox','interference_concern':reason,'rationale':'Quantitative ORAC-FL evidence exists, but normalization/protocol or interference risk prevents B1 pooling.','inclusion_in_exploratory_plot':'no'})
add_b2('Sulforaphane','Uthaman et al., Heliyon 11:e42673',2025,'10.1016/j.heliyon.2025.e42673','40034321','Special-case','reported at 1 mM','kit-derived ORAC output; not reliably molar-normalized','Pure SFN comparison is quantitative but reported normalization is ambiguous; electrophilic Nrf2 biology is not represented by ORAC.','ORAC methods and pure-SFN comparison in Results')

fields=['compound_name','PMID','DOI','study','publication_year','ORAC_arm','H_ORAC_or_L_ORAC','original_ORAC_value','original_unit','molar_conversion_possible','standardized_ORAC_mol_TE_per_mol','old_tier','new_tier','B1_eligibility_yes_no','missing_fields','critical_method_fields_present','interference_concern','rationale','inclusion_in_exploratory_plot','synonym','PubChem_CID','InChIKey','chemical_class','subclass','food_source_examples','compound_form','stereochemistry','purity','AAPH_concentration','fluorescein_concentration','Trolox_concentration','buffer','pH','temperature','solvent','solubilizer_RMCD','reading_interval','total_duration','AUC_method','concentration_range','linearity_reported','interference_noted','comparability_tier','Zotero_key','exact_location','notes']
# remove duplicate field names while preserving order
fields=list(dict.fromkeys(fields))
write_csv(DATA/'ORAC_Pilot_Reclassified_A_B1_B2.csv',raw,fields)

summ=[]
for name,b in ident.items():
    rr=[r for r in raw if r['compound_name']==name]
    vals=[float(r['standardized_ORAC_mol_TE_per_mol']) for r in rr if r['new_tier'] in ('A','B1') and r['standardized_ORAC_mol_TE_per_mol']]
    counts={t:sum(r['new_tier']==t for r in rr) for t in ('A','B1','B2','C','X')}
    status=('multi-study exploratory estimate' if len(vals)>=2 else 'single-study exploratory estimate' if len(vals)==1 else 'supportive_only' if counts['B2'] else 'not_measured_or_not_usable')
    summ.append({'compound_name':name,'PubChem_CID':b['PubChem_CID'],'InChIKey':b['InChIKey'],'chemical_class':b['chemical_class'],'subclass':b['subclass'],'ORAC_arm':b['preferred_ORAC_arm'],'special_case_flag':'yes' if b['special_case']!='normal' else 'no','Tier_A_count':counts['A'],'Tier_B1_count':counts['B1'],'Tier_B2_count':counts['B2'],'Tier_C_count':counts['C'],'Tier_X_count':counts['X'],'eligible_n':len(vals),'median_mol_TE_per_mol':round(statistics.median(vals),3) if vals else '','min':min(vals) if vals else '','max':max(vals) if vals else '','IQR':round(quantile(vals,.75)-quantile(vals,.25),3) if len(vals)>=4 else '','analysis_status':status,'CUPRAC_available':cuprac.get(name,{}).get('CUPRAC_available','unclear'),'heterogeneity_note':('Historical protocols are broadly comparable but non-identical; interpret dispersion descriptively.' if len(vals)>=2 else 'No inter-study estimate.'),'targeted_search_outcome':('B1 found' if any(r['old_tier']=='not_measured' and r['new_tier']=='B1' for r in rr) else 'B2 only' if counts['B2'] else 'No new usable ORAC-FL record' if not rr else 'Existing record(s) reclassified')})
summary_fields=list(summ[0])
write_csv(DATA/'ORAC_Exploratory_Compound_Summary.csv',summ,summary_fields)

COLORS={'Polyphenolic / phenolic compounds':'#386CB0','Vitamins / vitamin-like dietary antioxidants':'#F28E2B','Carotenoids':'#59A14F','Organosulfur compounds':'#B07AA1'}
def chart(arm,path,title,coverage=False):
    ss=[s for s in summ if s['ORAC_arm']==arm and s['eligible_n']]
    ss.sort(key=lambda x:float(x['median_mol_TE_per_mol']))
    W,H=1800,1050; im=Image.new('RGB',(W,H),'white'); d=ImageDraw.Draw(im)
    d.text((70,35),title,font=fnt(38,True),fill='#17202A')
    d.text((70,88),'A/B1 records only; points are independent publications. Medians summarize, not standardize, heterogeneous protocols.',font=fnt(20),fill='#555')
    if not ss: d.text((100,300),'No A/B1 records available.',font=fnt(32,True),fill='#9B1C31'); im.save(path); return
    left,right,top,bottom=140,W-80,160,H-250; ymax=max(float(s['max']) for s in ss)*1.15
    d.line((left,top,left,bottom),fill='#333',width=3); d.line((left,bottom,right,bottom),fill='#333',width=3)
    for i in range(6):
        y=bottom-(bottom-top)*i/5; val=ymax*i/5; d.line((left,y,right,y),fill='#E6E6E6',width=1); d.text((40,y-12),f'{val:.1f}',font=fnt(18),fill='#444')
    step=(right-left)/len(ss)
    for i,s in enumerate(ss):
        x=left+step*(i+.5); med=float(s['median_mol_TE_per_mol']); lo=float(s['min']); hi=float(s['max']); col=COLORS[s['chemical_class']]
        yy=lambda v: bottom-(bottom-top)*v/ymax
        d.line((x,yy(lo),x,yy(hi)),fill=col,width=5); d.line((x-12,yy(lo),x+12,yy(lo)),fill=col,width=4); d.line((x-12,yy(hi),x+12,yy(hi)),fill=col,width=4)
        vals=[float(r['standardized_ORAC_mol_TE_per_mol']) for r in raw if r['compound_name']==s['compound_name'] and r['new_tier'] in ('A','B1') and r['standardized_ORAC_mol_TE_per_mol']]
        for j,v in enumerate(vals): d.ellipse((x-10+(j-len(vals)/2)*10,yy(v)-10,x+10+(j-len(vals)/2)*10,yy(v)+10),fill=col,outline='white',width=2)
        d.line((x-22,yy(med),x+22,yy(med)),fill='#111',width=5)
        label=s['compound_name']; box=d.textbbox((0,0),label,font=fnt(18)); tw=box[2]-box[0]
        d.text((x-tw/2,bottom+20),label,font=fnt(18),fill='#222')
        d.text((x-22,bottom+55),f"n={s['eligible_n']}",font=fnt(16),fill='#666')
    d.text((20,390),'ORAC (mol TE/mol compound)',font=fnt(22,True),fill='#222')
    y=H-110
    for cls,col in COLORS.items():
        if any(s['chemical_class']==cls for s in ss): d.rectangle((70,y,92,y+22),fill=col); d.text((102,y-2),cls,font=fnt(17),fill='#333'); y+=30
    d.text((550,H-75),'Exploratory historical evidence; protocols are broadly comparable but non-identical.',font=fnt(20,True),fill='#9B1C31')
    im.save(path)

chart('H-ORAC',FIG/'H_ORAC_Exploratory_Historical_Comparison.png','Exploratory literature-derived H-ORAC values of representative food-derived antioxidants')
chart('L-ORAC',FIG/'L_ORAC_Exploratory_Historical_Comparison.png','L-ORAC historical evidence coverage and reported values')

# Heterogeneity plot for compounds with >=2 independent records.
multi=[s for s in summ if int(s['eligible_n'])>=2]
W,H=1600,900; im=Image.new('RGB',(W,H),'white'); d=ImageDraw.Draw(im); d.text((70,35),'Historical ORAC-FL method heterogeneity within compounds',font=fnt(36,True),fill='#17202A'); d.text((70,88),'Each point is one publication; connecting ranges visualize protocol-dependent dispersion.',font=fnt(20),fill='#555')
left,right,top,bottom=280,W-100,160,H-100; allv=[float(r['standardized_ORAC_mol_TE_per_mol']) for r in raw if r['new_tier'] in ('A','B1') and r['standardized_ORAC_mol_TE_per_mol']]; xmax=max(allv)*1.08
for i in range(6): x=left+(right-left)*i/5; d.line((x,top,x,bottom),fill='#E6E6E6'); d.text((x-15,bottom+15),f'{xmax*i/5:.1f}',font=fnt(18),fill='#444')
for i,s in enumerate(multi):
    y=top+80+i*140; vals=[float(r['standardized_ORAC_mol_TE_per_mol']) for r in raw if r['compound_name']==s['compound_name'] and r['new_tier'] in ('A','B1') and r['standardized_ORAC_mol_TE_per_mol']]; xs=[left+(right-left)*v/xmax for v in vals]
    d.text((60,y-18),s['compound_name'],font=fnt(24,True),fill='#222'); d.line((min(xs),y,max(xs),y),fill='#777',width=5)
    for j,(x,v) in enumerate(zip(xs,vals)): d.ellipse((x-11,y-11,x+11,y+11),fill=COLORS[s['chemical_class']],outline='white',width=2); d.text((x-25,y+18),f'{v:g}',font=fnt(16),fill='#333')
d.text((650,H-55),'ORAC (mol TE/mol compound)',font=fnt(22,True),fill='#222'); im.save(FIG/'ORAC_Method_Heterogeneity.png')

# Coverage matrix.
cols=['Tier A','Tier B1','Tier B2','H arm','L arm','CUPRAC','Special case']; cw=150; rowh=45; W=520+cw*len(cols); H=170+rowh*len(summ)+80
im=Image.new('RGB',(W,H),'white'); d=ImageDraw.Draw(im); d.text((45,25),'ORAC evidence coverage matrix',font=fnt(36,True),fill='#17202A'); d.text((45,75),'Counts for evidence tiers; binary arm, CUPRAC coverage and special-case flags.',font=fnt(19),fill='#555')
x0=500;y0=135
for j,c in enumerate(cols): d.text((x0+j*cw+15,y0-35),c,font=fnt(18,True),fill='#222')
for i,s in enumerate(summ):
    y=y0+i*rowh; d.text((40,y+10),s['compound_name'],font=fnt(18),fill='#222')
    vals=[int(s['Tier_A_count']),int(s['Tier_B1_count']),int(s['Tier_B2_count']),1 if s['ORAC_arm']=='H-ORAC' else 0,1 if s['ORAC_arm']=='L-ORAC' else 0,1 if str(s['CUPRAC_available']).startswith('yes') else 0,1 if s['special_case_flag']=='yes' else 0]
    for j,v in enumerate(vals):
        fill='#2E86AB' if v else '#F1F3F5'; d.rectangle((x0+j*cw,y,x0+(j+1)*cw-4,y+rowh-4),fill=fill,outline='white'); d.text((x0+j*cw+cw/2-8,y+8),str(v),font=fnt(18,True),fill='white' if v else '#999')
im.save(FIG/'ORAC_Evidence_Coverage_Matrix.png')

print(f"records={len(raw)} B1={sum(r['new_tier']=='B1' for r in raw)} B2={sum(r['new_tier']=='B2' for r in raw)} compounds_B1={sum(int(s['Tier_B1_count'])>0 for s in summ)} multi={len(multi)}")
