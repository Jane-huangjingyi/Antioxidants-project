"""Source-specific dietary occurrence leads; no human approval or ranking update."""
import csv,json
from pathlib import Path
P=Path(__file__).resolve().parent
with (P/'results/Comparison_Identity_Audit.csv').open(encoding='utf-8-sig') as f:
    compounds={r['candidate_id']:r['source_compound'] for r in csv.DictReader(f)}
rows=[]
for cid,name in sorted(compounds.items()):
    if cid in ['AFF-0077','AFF-0078','AFF-0079','AFF-0080','AFF-0081']:
        doi='10.1016/j.jare.2019.01.002';food='Commercial coffee products';locator='Figure 1; Table 2; instrumental analysis';status='PRIMARY_TABLE_FOOD_OCCURRENCE_SUPPORTED';scope='Original HTML table and methods';boundary='3/4-CQA and diCQA positions require explicit nomenclature crosswalk; no lot identity inferred'
    elif cid in ['AFF-0062','AFF-0063','AFF-0064','AFF-0065']:
        doi='10.1080/10942912.2019.1579835';food='Commercial honey';locator='Indexed Figure 1 and sample-preparation passage; full article access returned 403';status='PRIMARY_SOURCE_LEAD_PENDING_FULL_CHECK';scope='Publisher-indexed extract only';boundary='Indexed preparation includes alkaline hydrolysis; not proof of native free acid. Vanillic/caffeic co-elution also requires identity verification'
    elif cid in ['AFF-0167','AFF-0169','AFF-0170']:
        doi='10.1080/10412905.2009.9700218';food={'AFF-0167':'Clove essential oil','AFF-0169':'Oregano essential oil','AFF-0170':'Thyme essential oil'}[cid];locator='Original abstract GC/GC-MS composition';status='PRIMARY_ABSTRACT_OCCURRENCE_SUPPORT';scope='Original abstract';boundary='Culinary-source oil evidence; do not infer usual food dose, safety, purity or whole-food concentration'
    elif cid=='AFF-0162':
        doi='10.1039/C3AY41953C';food='Chili peppers and hot sauces';locator='Publisher original abstract; HPLC-ESIMS E-capsaicin';status='PRIMARY_ABSTRACT_OCCURRENCE_SUPPORT';scope='Original abstract';boundary='E-capsaicin form must match target reagent; not total capsaicinoids'
    elif cid=='AFF-0173':
        doi='10.22146/ijc.21831';food='Cured vanilla beans';locator='Publisher original abstract; ethanolic extracts HPLC';status='PRIMARY_ABSTRACT_OCCURRENCE_SUPPORT';scope='Original abstract';boundary='Vanillin is distinct from glucovanillin and ethylvanillin; no concentration imported'
    elif cid=='AFF-0102':
        doi='10.1039/C4AY00663A';food='Market sesame oil';locator='Publisher original abstract; SPE-HPLC application';status='PRIMARY_ABSTRACT_OCCURRENCE_SUPPORT';scope='Original abstract';boundary='Processing-dependent occurrence; 1982 survey DOI 10.3358/shokueishi.23.142 reported no detection, not universal absence'
    elif cid=='AFF-0181':
        doi='10.5650/jos.ess20033';food='Extra virgin olive oil';locator='Publisher original abstract; HPLC after liquid extraction';status='PRIMARY_ABSTRACT_OCCURRENCE_SUPPORT';scope='Original abstract';boundary='Free tyrosol versus hydrolysis-derived total tyrosol must remain distinct'
    else:
        doi='10.3177/jnsv.52.54';food='Lemon-derived enzyme-treated flavonoid preparation';locator='Original abstract';status='FREE_AGLYCONE_NATURAL_FOOD_OCCURRENCE_NOT_ESTABLISHED';scope='Original abstract';boundary='Eriodictyol generated from glycosides by beta-glucosidase; not direct natural free-aglycone occurrence proof'
    material={'AFF-0167':('97-53-0','>=99%'),'AFF-0162':('404-86-4','>=95%'),'AFF-0173':('121-33-5','>=97%')}.get(cid,('',''))
    rows.append(dict(candidate_id=cid,compound=name,food_matrix=food,food_doi=doi,food_url='https://doi.org/'+doi,food_locator=locator,food_evidence_status=status,checked_scope=scope,interpretation_boundary=boundary,antioxidant_source_CAS=material[0],antioxidant_source_reported_purity=material[1],material_source_doi='10.3390/foods10081807' if material[0] else '',material_source_locator='Methods phytochemical stock preparation' if material[0] else '',exact_material_and_lot='NOT_VERIFIED',food_gate='SOURCE_SUPPORTED_CANDIDATE_REQUIRES_REVIEW' if 'SUPPORT' in status else 'PENDING',human_review_status='NOT_REVIEWED',change_applied='NO',access_date='2026-11-07'))
assert len(rows)==17 and len({r['candidate_id'] for r in rows})==17
assert sum(bool(r['antioxidant_source_CAS']) for r in rows)==3
checks=json.loads((P/'inputs/additional_food_source_checks.json').read_text(encoding='utf-8'))
for r in rows:
    linked=[x for x in checks if r['candidate_id'] in x['candidate_ids']]
    r.update(additional_source_doi='; '.join(x['doi'] for x in linked),additional_source_locator='; '.join(x['locator'] for x in linked),additional_source_scope='; '.join(x['checked_scope'] for x in linked),additional_finding='; '.join(x['finding'] for x in linked),additional_decision='; '.join(x['decision'] for x in linked),next_verification='Confirm tissue/free-versus-conjugated fraction and exact isomer; obtain material form and lot documentation')
with (P/'results/Food_and_Material_Followup.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
print('QC PASS: 17 candidate dispositions; 3 source CAS/purity checks; no approvals or ranking changes.')
