"""Extract experimental ln(ORAC), excluding model predictions and their errors."""
import csv,json,math,xml.etree.ElementTree as ET
from pathlib import Path
P=Path(__file__).resolve().parent
d=json.loads((P/'inputs/source_recovery/raw/PMC6539043.json').read_text(encoding='utf-8'))[0]['documents'][0]
t=next(x for x in d['passages'] if x.get('infons',{}).get('id')=='ijms-20-02328-t003' and x['infons']['type']=='table')
rows=[]
for tr in ET.fromstring(t['infons']['xml']).findall('.//tbody/tr'):
    c=[''.join(x.itertext()).strip() for x in tr.findall('td')]
    if len(c)<6:continue
    value,error=[float(s.strip().replace('−','-')) for s in c[3].split('±')]
    rows.append(dict(source_row=c[0],compound=c[1],doi='10.3390/ijms20092328',source_url='https://pmc.ncbi.nlm.nih.gov/articles/PMC6539043/',source_locator='Table 3 experimental ln(ORAC) column; Methods 3.2, 3.3, modelling transformation',reported_ln_orac=value,reported_plus_minus_log_scale=error,back_transformed_location_candidate=math.exp(value),back_transform_interpretation='EXP_OF_REPORTED_LOG_LOCATION_NOT_ESTABLISHED_ARITHMETIC_MEAN',error_type='UNRESOLVED_FOR_EXPERIMENTAL_COLUMN',replication='Triplicate measurements; independent batches unresolved',pH=7.4,temperature_C=37,stock_vehicle='Acetone/water 50:50; diluted in buffer; final fraction unresolved',read_interval_minutes=1,integration_duration='NOT_EXPLICIT_IN_CHECKED_METHODS',sampling_variance='',model_eligibility='PENDING_SCALE_ERROR_AND_PROTOCOL_REVIEW',human_review_status='NOT_REVIEWED',change_applied='NO'))
assert len(rows)==36 and len({r['source_row'] for r in rows})==36
q=next(r for r in rows if r['compound']=='Quercetin')
assert q['reported_ln_orac']==1.970 and abs(q['back_transformed_location_candidate']-math.exp(1.970))<1e-12
with (P/'results/Flavonoid_Log_Capacity_Extraction.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
print('QC PASS: 36 experimental log rows; predictions excluded; no variance or ranking assigned.')
