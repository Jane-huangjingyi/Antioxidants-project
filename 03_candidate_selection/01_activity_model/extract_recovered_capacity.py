"""Extract targeted original tables from locally recovered NCBI BioC JSON.

Run explicitly after recover_sources.py. Normal offline reproduction uses the
committed structured extraction, not the optional full article text.
"""
from pathlib import Path
import sys,json,re,hashlib,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'00_project'))
from pipeline_io import *
HERE=Path(__file__).resolve().parent;RAW=HERE/'inputs/source_recovery/raw'
def article(pmc):return read_json(RAW/(pmc+'.json'))[0]['documents'][0]['passages']
def table(pmc,suffix):
 p=next(x for x in article(pmc) if x['infons'].get('type')=='table' and x['infons'].get('id','').endswith(suffix))
 root=ET.fromstring(p['infons']['xml'])
 return p,[[''.join(c.itertext()).strip() for c in row.findall('td')] for row in root.findall('.//tbody/tr')]
def pair(s):
 m=re.search(r'(\d+(?:\.\d+)?)\s*\u00b1\s*(\d+(?:\.\d+)?)',s);assert m,s
 return float(m[1]),float(m[2])
baseline=read_csv(HERE/'results/Observation_Readiness.csv')
records=[]
sources=[('PMC9951910','10.3390/antiox12020505','t003',{'Ascorbic acid':('AFF-0104','L-Ascorbic acid'),'GSH':('NEW-GSH','Glutathione'),'Gallic acid':('AFF-0060','Gallic acid'),'Quercetin':('AFF-0009','Quercetin'),'Caffeic acid':('AFF-0069','Caffeic acid')}),('PMC8392586','10.3390/foods10081807','t005',{'Eugenol':('AFF-0167','Eugenol'),'Capsaicin':('AFF-0162','Capsaicin'),'Vanillin':('AFF-0173','Vanillin')})]
for pmc,doi,suffix,mapping in sources:
 passage,rows=table(pmc,suffix);raw_hash=sha(RAW/(pmc+'.json'))
 caption=next(p['text'] for p in article(pmc) if p['infons'].get('type')=='table_caption' and p['infons'].get('id','').endswith(suffix))
 is_foods=pmc=='PMC8392586'
 if is_foods:assert 'standard deviation' in caption and 'three independent experiments' in caption
 for row in rows:
  if not row or row[0] not in mapping:continue
  cid,name=mapping[row[0]];mean,err=pair(row[2] if is_foods else row[1]);existing=[r for r in baseline if r['candidate_id']==cid and r['doi']==doi]
  assert len(existing)<=1,(cid,doi)
  old_id=existing[0]['observation_id'] if existing else ''
  records.append({'candidate_id':cid,'compound':name,'doi':doi,'source_observation_id':old_id,'row_relationship':'RECHECK_OF_EXISTING_OBSERVATION_NOT_NEW_STUDY' if old_id else 'NEW_SOURCE_ROW_OUTSIDE_PRIOR_EXTRACTION','endpoint':'ORAC_FL_AUC_SLOPE_RATIO_TO_TROLOX','reported_mean':mean,'reported_plus_minus':err,'unit_interpretation':'mol TE/mol compound, molar calibration-slope ratio','error_type':'SD_EXPLICIT_IN_ORIGINAL_TABLE_CAPTION' if is_foods else 'PLUS_MINUS_STATISTIC_NOT_DEFINED_FOR_THIS_TABLE','independent_experiments_as_reported':3 if is_foods else None,'replication_structure':'Three independent experiments as stated in Table 5' if is_foods else 'Triplicate solutions on two days; effective n for Table 3 TE ratios unresolved','pH':7.0 if is_foods else 7.4,'temperature_C':37,'maximum_reported_recording_min':55 if is_foods else 180,'vehicle':'Stock ethanol diluted in PBS; final ethanol fraction unresolved' if is_foods else ('5% ethanol in final wells with matched Trolox' if name in ['Quercetin','Caffeic acid'] else 'Working solutions in phosphate buffer; inspect stock-solvent statements'),'source_form':'Quercetin dihydrate reported; parent mapping needs review' if name=='Quercetin' else 'As specified in original reagents section; exact form/purity remains a separate gate','source_url':f'https://pmc.ncbi.nlm.nih.gov/articles/{pmc}/','source_locator':passage['infons']['id']+'; Methods','source_BioC_sha256':raw_hash,'source_BioC_offset':passage['offset'],'human_review_status':'NOT_REVIEWED','change_applied':'NO'})
assert len(records)==8 and len({(r['candidate_id'],r['doi'],r['endpoint']) for r in records})==8
write_json(HERE/'inputs/recovered_capacity_rows.json',{'extraction_date':AS_OF,'records':records,'scope':'Original article text and XML-encoded tables, not visual figures or supplementary files'})
# Update only this follow-up extraction; the original evidence and frozen rubric are untouched.
path=HERE/'inputs/source_resolution.json';resolution=read_json(path)
for r in resolution['records']:
 match=next((x for x in records if x['source_observation_id']==r['observation_id']),None)
 if not match:continue
 r['access_status']='ORIGINAL_TABLE_AND_METHODS_RECHECKED_FROM_NCBI_BIOC'
 r['url']=match['source_url'];r['locator']=match['source_locator'];r['source_BioC_sha256']=match['source_BioC_sha256']
 if match['error_type'].startswith('SD_EXPLICIT'):
  r.update(raw_mean=match['reported_mean'],raw_SD=match['reported_plus_minus'],unit='umol TE per umol compound',determinations=3,replication_interpretation=match['replication_structure'],remaining_issue='Common-calibration covariance, final solvent fraction and applicability to target assay need review; human approval not applied')
 else:
  r['recovered_mean']=match['reported_mean'];r['recovered_plus_minus']=match['reported_plus_minus'];r['recovered_error_type']=match['error_type'];r['remaining_issue']='AUC value and reported plus/minus recovered; its statistical definition and effective n are unresolved. Do not infer them from beverage-table footnotes or count triplicates across two days as n=6.'
write_json(path,resolution)
print('Extracted 8 original AUC rows: 7 existing-observation rechecks and 1 added GSH source candidate; no study-count inflation.')
