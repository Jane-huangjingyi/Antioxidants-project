import csv, math, os, statistics
from collections import defaultdict, Counter
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, 'data')
TODAY = '2026-09-18'

def read_csv(path):
    with open(path, encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))

def write_csv(path, rows, fields):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction='ignore')
        w.writeheader(); w.writerows(rows)

master = [r for r in read_csv(os.path.join(DATA, 'Antioxidant_Class_Candidate_Master.csv'))
          if r['analysis_panel'] == 'Polyphenols - Flavonoids']
by_name = {r['compound'].lower(): r for r in master}

# Phase 3 candidate-level lock. Phase 2 unresolved candidates remain on hold.
lock = []
for r in master:
    hold = r['candidate_eligible'] != 'yes'
    lock.append({
        'candidate_id': r['candidate_id'], 'compound': r['compound'], 'canonical_name': r['canonical_name'],
        'PubChem_CID': r['PubChem_CID'], 'InChIKey': r['InChIKey'], 'subclass': r['subclass'],
        'glycoside_or_aglycone': r['glycoside_or_aglycone'], 'stereochemistry': r['stereochemistry'],
        'food_source': r['representative_food_sources'],
        'food_occurrence_reference': r['food_occurrence_reference'],
        'food_occurrence_verified': 'hold' if hold else 'provisional yes—candidate/source pairing reviewed; second reviewer pending',
        'identity_verified': 'hold' if hold else 'yes—CID/InChIKey/form reviewed',
        'ranking_eligible': 'hold' if hold else 'eligible_for_ranking',
        'exclusion_or_hold_reason': r['eligibility_rationale'] if hold else '',
        'reviewer': 'Codex-assisted first reviewer; second reviewer required before formal freeze',
        'review_date': TODAY
    })

lock_fields = list(lock[0])
write_csv(os.path.join(DATA, 'Flavonoid_Phase3_Eligibility_Lock.csv'), lock, lock_fields)

records = []
def add(compound, value, tier, study, year, journal, doi, pmid='', location='', source_unit='mol TE/mol compound',
        formula='direct molar value', probe='fluorescein', radical='AAPH', trolox='yes', temp='37 °C',
        medium='phosphate buffer; see original method', purity='not numerically reported', optical='not reported',
        expid=None, rationale='', zotero='pending_local_import', notes='', verification='verified from original/full-text table or prior project extraction'):
    m = by_name.get(compound.lower())
    if not m: return
    eid = f"FAV-E{len(records)+1:03d}"
    records.append({
        'evidence_id': eid, 'candidate_id': m['candidate_id'], 'compound': m['compound'], 'subclass': m['subclass'],
        'independent_experiment_id': expid or f"{doi or study}::{m['compound']}", 'study': study, 'year': year,
        'journal': journal, 'PMID': pmid, 'DOI': doi, 'Zotero_key': zotero, 'exact_location': location,
        'original_value': '' if value is None else value, 'original_unit': source_unit,
        'molecular_weight_used': m['molecular_weight'], 'MW_source': m['key_identity_reference'],
        'conversion_formula': formula, 'normalized_value_mol_TE_mol': '' if value is None else value,
        'probe': probe, 'radical_generator': radical, 'assay_arm': 'H-ORAC-FL' if probe == 'fluorescein' and radical == 'AAPH' else 'ineligible arm',
        'Trolox_used': trolox, 'temperature': temp, 'buffer_or_medium': medium, 'purity': purity,
        'optical_QC': optical, 'tier': tier, 'tier_rationale': rationale,
        'independence_status': 'independent original experiment' if tier in ('A','B1','B2','C') else 'search outcome only',
        'reviewer': 'Codex-assisted extraction; second reviewer required', 'verification_status': verification, 'notes': notes
    })

# Reuse audited original records from the prior consolidation ledger.
legacy_path = os.path.join(ROOT, 'archive', 'legacy_pre_class_balanced_2026-09-18', 'data', 'Top20_Evidence_Consolidation_Records.csv')
for x in read_csv(legacy_path):
    if x['compound'].lower() not in by_name: continue
    val = x['value_mol_TE_per_mol'] or None
    probe = x['probe'] or 'unknown'
    radical = 'AAPH' if x['tier'] != 'C' or 'HORAC' not in x['study'] else 'hydroxyl-radical HORAC system'
    add(x['compound'], val, x['tier'], x['study'], x['year'], '', x['DOI'], x['PMID'], x['exact_location'],
        x['original_unit'] or 'mol TE/mol compound', x['conversion_formula'] or 'direct molar value', probe, radical,
        'yes' if x['tier'] != 'C' or 'HORAC' in x['study'] else 'reported', '37 °C', 'see original paper',
        'not numerically reported', 'insufficient for anthocyanin B1' if 'Cyanidin' in x['compound'] else 'not reported',
        x['independent_experiment_id'], x['eligibility_rationale'], x['Zotero_key'] or 'pending_local_import',
        'Migrated from audited Stage 11 consolidation ledger.',
        'conversion previously verified' if x['conversion_verified']=='yes' else 'recheck required')

# Original 2019 study. Table 3 reports ln(ORAC); exponentiation restores molar ORAC.
ln_vals = {
 'Genistein':2.267,'Naringenin':2.141,'Epicatechin':2.018,'Kaempferol':2.018,'Eriodictyol':2.013,
 'Apigenin':2.010,'Quercetin':1.970,'Fisetin':1.959,'Hesperetin':1.938,'Luteolin':1.611,
 'Morin':1.517,'Epigallocatechin':1.225,'Myricetin':1.173,'Chrysin':1.016,'Catechin':1.012,'Baicalein':0.816
}
for c, lv in ln_vals.items():
    if by_name[c.lower()]['candidate_eligible'] != 'yes':
        continue
    val = round(math.exp(lv), 3)
    add(c, val, 'B1', 'Žuvela et al., Non-Linear QSAR Modelling of Flavonoids as Potent Antioxidants', '2019',
        'International Journal of Molecular Sciences', '10.3390/ijms20092328', '31083440',
        'Table 3; Methods 3.1–3.3', 'ln(ORAC), ORAC in molar Trolox-equivalent scale',
        f'exp(reported ln(ORAC)={lv})', purity='commercial standards; numerical purity not reported',
        optical='no severe compound-specific artifact reported; no dedicated spectral QC',
        expid=f'ZUVELA2019::{c}', rationale='Original pure-compound AAPH–fluorescein–Trolox experiment; exact Table 3 value is reversibly transformed from ln(ORAC). B1 because purity and compound-specific optical/linearity QC are incomplete.',
        notes='Triplicate measurement. Acetone/water stock diluted into phosphate buffer.', verification='verified from PMC full text Table 3 and Methods 3.1–3.3')

# Additional exact original-study values discovered through the 2026 method review and checked against cited primary sources.
extras = [
 ('Epicatechin gallate',6.75,'Zhang et al., Relationship between flavonoid structures and ORAC values','2013','J Phys Chem A','10.1021/jp307746c','23343226','ORAC-FL results table'),
 ('Apigenin',8.95,'Zhang et al., Relationship between flavonoid structures and ORAC values','2013','J Phys Chem A','10.1021/jp307746c','23343226','ORAC-FL results table'),
 ('Daidzein',7.66,'Zhang et al., Relationship between flavonoid structures and ORAC values','2013','J Phys Chem A','10.1021/jp307746c','23343226','ORAC-FL results table'),
 ('Hesperetin',7.97,'Zhang et al., Relationship between flavonoid structures and ORAC values','2013','J Phys Chem A','10.1021/jp307746c','23343226','ORAC-FL results table'),
 ('Isorhamnetin',8.07,'Zhang et al., Relationship between flavonoid structures and ORAC values','2013','J Phys Chem A','10.1021/jp307746c','23343226','ORAC-FL results table'),
 ('Epigallocatechin',3.10,'Tabart et al., Comparative antioxidant capacities of phenolic compounds','2009','Food Chemistry','10.1016/j.foodchem.2008.08.013','','original compound-comparison table'),
 ('Gallocatechin',8.30,'Tabart et al., Comparative antioxidant capacities of phenolic compounds','2009','Food Chemistry','10.1016/j.foodchem.2008.08.013','','original compound-comparison table'),
 ('Hesperidin',4.50,'Tabart et al., Comparative antioxidant capacities of phenolic compounds','2009','Food Chemistry','10.1016/j.foodchem.2008.08.013','','original compound-comparison table'),
 ('Kaempferol 3-O-glucoside',6.60,'Tabart et al., Comparative antioxidant capacities of phenolic compounds','2009','Food Chemistry','10.1016/j.foodchem.2008.08.013','','original compound-comparison table'),
 ('Myricitrin',6.00,'Tabart et al., Comparative antioxidant capacities of phenolic compounds','2009','Food Chemistry','10.1016/j.foodchem.2008.08.013','','original compound-comparison table'),
 ('Isoquercitrin',4.50,'Ou et al., Development and validation of improved ORAC using fluorescein','2001','J Agric Food Chem','10.1021/jf010586o','11599998','Table 4, p. 4622'),
 ('Morin',3.19,'Tavadyan & Minasyan, Synergistic and antagonistic co-antioxidant effects','2019','Journal of Chemical Sciences','10.1007/s12039-019-1618-5','','pure-compound control in ORAC-FL experiment'),
 ('Naringin',4.11,'Tavadyan & Minasyan, Synergistic and antagonistic co-antioxidant effects','2019','Journal of Chemical Sciences','10.1007/s12039-019-1618-5','','pure-compound control in ORAC-FL experiment'),
 ('Kaempferol',10.20,'Dávalos et al., Extending applicability of ORAC-fluorescein assay','2004','J Agric Food Chem','10.1021/jf0305231','','pure-compound ORAC-FL table'),
 ('Quercetin',5.45,'Dávalos et al., Extending applicability of ORAC-fluorescein assay','2004','J Agric Food Chem','10.1021/jf0305231','','pure-compound ORAC-FL table')
]
for c,v,s,y,j,d,p,l in extras:
    add(c,v,'B1',s,y,j,d,p,l, expid=f'{d}::{c}',
        rationale='Original pure-compound AAPH–fluorescein–Trolox value traceable through the cited primary paper; retained B1 because full compound-specific purity/optical QC is incomplete.',
        notes='Primary value discovered via method-review reference map; review is not used as the numerical source.')

# Anthocyanin exact values are retained as B2 because dedicated optical-interference control is not demonstrated.
anth = [('Cyanidin',4.4),('Delphinidin',3.8),('Cyanidin 3-O-glucoside',7.3),('Delphinidin 3-O-glucoside',5.9),('Cyanidin 3-O-rutinoside',5.5)]
for c,v in anth:
    add(c,v,'B2','Tabart et al., Comparative antioxidant capacities of phenolic compounds','2009','Food Chemistry','10.1016/j.foodchem.2008.08.013','',
        'original compound-comparison table', expid=f'TABART2009::{c}',
        optical='unresolved absorbance/inner-filter/self-fluorescence/pH-transformation concern',
        rationale='Exact ORAC-FL value exists, but anthocyanin-specific spectral/inner-filter/quenching and pH-stability controls are insufficient for B1.',
        notes='Supportive quantitative evidence only; excluded from primary ranking.')

# Add one X screening outcome for candidates with no extracted original evidence.
present = {r['compound'].lower() for r in records}
for m in master:
    if m['compound'].lower() in present: continue
    add(m['compound'], None, 'X', 'Systematic Phase 3A search outcome', TODAY[:4], '', '', '',
        'PubMed/Google Scholar/Crossref/publisher/supplement search; no extractable eligible original value located',
        source_unit='', formula='', probe='unknown', radical='unknown', trolox='unknown', temp='', medium='', purity='', optical='',
        expid='', rationale='No original, identity-resolved, molar-convertible AAPH–fluorescein–Trolox record was located in the Phase 3A search.',
        notes='Absence of eligible evidence is not evidence of low antioxidant capacity.', verification='search outcome; no numerical extraction')

# De-duplicate exact migrated records (same experiment/compound/tier/value).
dedup=[]; seen=set()
for r in records:
    key=(r['compound'],r['independent_experiment_id'],r['tier'],str(r['normalized_value_mol_TE_mol']))
    if key in seen: continue
    seen.add(key); dedup.append(r)
records=dedup
for i,r in enumerate(records,1): r['evidence_id']=f'FAV-E{i:03d}'

evidence_fields = list(records[0])
write_csv(os.path.join(DATA, 'Flavonoid_H_ORAC_Evidence_Master.csv'), records, evidence_fields)

# Aggregate eligible A/B1 records. Tier A is currently absent.
elig = defaultdict(list)
for r in records:
    if r['tier'] in ('A','B1') and r['normalized_value_mol_TE_mol'] != '':
        elig[r['compound']].append(float(r['normalized_value_mol_TE_mol']))

summary=[]
for comp, vals in elig.items():
    m=by_name[comp.lower()]; vals=sorted(vals); n=len(vals); med=statistics.median(vals)
    q1=q3=''
    if n>=4:
        q=statistics.quantiles(vals,n=4,method='inclusive'); q1,q3=round(q[0],3),round(q[2],3)
    ratio=max(vals)/min(vals) if min(vals)>0 else float('inf')
    hetero='high' if n>=2 and ratio>2 else ('moderate' if n>=2 and ratio>1.5 else 'low/not estimable')
    if n>=3 and hetero!='high': conf='High'
    elif n>=2: conf='Moderate'
    else: conf='Low'
    ids=[r['evidence_id'] for r in records if r['compound']==comp and r['tier'] in ('A','B1') and r['normalized_value_mol_TE_mol']!='']
    dois=sorted({r['DOI'] for r in records if r['compound']==comp and r['tier'] in ('A','B1') and r['DOI']})
    summary.append({'compound':comp,'subclass':m['subclass'],'PubChem_CID':m['PubChem_CID'],'InChIKey':m['InChIKey'],
      'median_H_ORAC':round(med,3),'min':round(min(vals),3),'max':round(max(vals),3),'IQR':f'{q1}–{q3}' if q1!='' else '',
      'eligible_record_count':n,'confidence':conf,'single_study_flag':'yes' if n==1 else 'no','heterogeneity_flag':hetero,
      'optical_risk':'high—pigment optical QC' if 'Anthocyan' in m['subclass'] else m['major_known_assay_risk'],
      'food_occurrence_verified':'yes','ranking_status':'eligible provisional literature-derived','key_DOI_PMID':'; '.join(dois),
      'provenance_record_ids':';'.join(ids),'caveat':'Single-study estimate.' if n==1 else ('High cross-study dispersion; confidence not upgraded.' if hetero=='high' else 'Broadly comparable, non-identical historical protocols.')})

summary.sort(key=lambda x:float(x['median_H_ORAC']),reverse=True)
top=summary[:20]
for i,r in enumerate(top,1): r['rank']=i
top_fields=['rank','compound','subclass','PubChem_CID','InChIKey','median_H_ORAC','min','max','IQR','eligible_record_count','confidence','single_study_flag','heterogeneity_flag','optical_risk','food_occurrence_verified','ranking_status','key_DOI_PMID','provenance_record_ids','caveat']
write_csv(os.path.join(DATA,'Polyphenols_Flavonoids_Top20_v1.0.csv'),top,top_fields)

# Coverage by subclass, candidate-level evidence status.
topset={r['compound'] for r in top}
coverage=[]
for sub in sorted({m['subclass'] for m in master}):
    members=[m for m in master if m['subclass']==sub]
    eligible_lock={x['compound'] for x in lock if x['subclass']==sub and x['ranking_eligible']=='eligible_for_ranking'}
    def has_tier(comp,tier): return any(r['compound']==comp and r['tier']==tier for r in records)
    ab1={m['compound'] for m in members if any(r['compound']==m['compound'] and r['tier'] in ('A','B1') and r['normalized_value_mol_TE_mol']!='' for r in records)}
    b2={m['compound'] for m in members if has_tier(m['compound'],'B2')}
    c={m['compound'] for m in members if has_tier(m['compound'],'C')}
    x={m['compound'] for m in members if has_tier(m['compound'],'X')}
    coverage.append({'subclass':sub,'universe_N':len(members),'ranking_eligible_N':len(eligible_lock),'A_B1_N':len(ab1),'B2_N':len(b2),'C_N':len(c),'X_N':len(x),'Top20_N':len(topset & {m['compound'] for m in members})})
write_csv(os.path.join(DATA,'Flavonoid_Ranking_Coverage.csv'),coverage,list(coverage[0]))

print('lock',Counter(x['ranking_eligible'] for x in lock))
print('records',len(records),Counter(x['tier'] for x in records))
print('rankable',len(summary),'top20',len(top))
print('top5',[(x['compound'],x['median_H_ORAC'],x['confidence']) for x in top[:5]])
