"""Extract two shared phenolic-acid rows at each reported dose, without pooling."""
from pathlib import Path
import json,csv,xml.etree.ElementTree as ET
P=Path(__file__).resolve().parent
d=json.loads((P/'inputs/source_recovery/raw/PMC9495677.json').read_text(encoding='utf-8'))[0]['documents'][0]
t=next(x for x in d['passages'] if x.get('infons',{}).get('id')=='antioxidants-11-01784-t002' and x['infons']['type']=='table')
rows=[]
for tr in ET.fromstring(t['infons']['xml']).findall('.//tbody/tr'):
    cells=[''.join(x.itertext()).strip() for x in tr.findall('td')]
    if cells and cells[0] in ['Gallic acid','Caffeic acid']:
        for dose,cell in zip([2.5,5],cells[-2:]):
            mean,error=[float(x.strip()) for x in cell.split('±')]
            rows.append(dict(candidate_id={'Gallic acid':'AFF-0060','Caffeic acid':'AFF-0069'}[cells[0]],compound=cells[0],doi='10.3390/antiox11091784',source_url='https://pmc.ncbi.nlm.nih.gov/articles/PMC9495677/',source_locator='Table 2; Methods 2.1 and 2.2.2',compound_uM=dose,reported_uM_TE=mean,reported_plus_minus_uM_TE=error,conditional_molar_ratio=mean/dose,conditional_plus_minus_ratio=error/dose,error_type='NOT_DEFINED_IN_CHECKED_METHODS_OR_TABLE',replicates_as_reported=3,independence='UNRESOLVED',integration_minutes=80,status='DOSE_SPECIFIC_DIAGNOSTIC_NOT_POOLED',human_review_status='NOT_REVIEWED',change_applied='NO'))
assert len(rows)==4
with (P/'results/Overlap_Dose_Diagnostic.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
print('PASS: four dose-specific rows, two compounds, one paper; no variance or rank assigned.')
