"""Compare source-specific endpoints; do not estimate a pooled chemical effect."""
import csv,math
from pathlib import Path
P=Path(__file__).resolve().parent
def read(name):
    with (P/'results'/name).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
a=next(r for r in read('Flavonoid_Log_Capacity_Extraction.csv') if r['compound']=='Quercetin')
b=next(r for r in read('Model_Input_Candidates.csv') if r['compound']=='Quercetin')
rows=[]
for doi,locator,scale,value,error,vehicle,form,estimator in [
    (a['doi'],'Table 3; Methods 3.2, 3.3 and modelling transformation','ln(ORAC)',a['reported_ln_orac'],a['reported_plus_minus_log_scale'],a['stock_vehicle'],'Material purity/hydration form unresolved','Reported experimental log location; molar endpoint formula needs inherited-protocol verification'),
    (b['doi'],'Table 3; Methods ORAC and data comparison','Molar TE calibration-slope ratio',b['molar_mean_candidate'],b['reported_plus_minus'],b['vehicle'],b['source_form'],'Slope AUC versus molar antioxidant concentration divided by matched Trolox slope')]:
    rows.append(dict(candidate_id='AFF-0009',compound='Quercetin',doi=doi,doi_url='https://doi.org/'+doi,source_locator=locator,reported_scale=scale,reported_location=value,reported_plus_minus=error,estimator=estimator,pH=7.4,temperature_C=37,vehicle=vehicle,chemical_form=form,error_definition='UNRESOLVED_FOR_REPORTED_EXPERIMENTAL_ENDPOINT',batch_independence='UNRESOLVED',pooling_decision='DO_NOT_POOL_CURRENTLY',decision_reason='Different endpoint definitions; unresolved log summary/error, vehicle/form and integration compatibility',human_review_status='NOT_REVIEWED',change_applied='NO'))
assert len(rows)==2 and len({r['doi'] for r in rows})==2
assert math.isclose(math.exp(float(a['reported_ln_orac'])),float(a['back_transformed_location_candidate']))
with (P/'results/Quercetin_Cross_Paper_Compatibility.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
print('QC PASS: two DOI-linked source endpoints; pooling prohibited; no invented variance.')
