"""Inventory legacy numerical rows without importing them as model observations."""
import csv,json,re
from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parents[1]
def read(path):
    with path.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def norm(s):return re.sub(r'\s+',' ',s.strip().lower())
legacy_path=ROOT/'02_identity_and_evidence/inputs/reference_collection/data/class_specific_antioxidant/Aqueous_Antioxidant_Primary_Literature_Evidence.csv'
legacy=read(legacy_path)
current=read(P/'results/Traceable_Capacity_Evidence.csv')
profiles=read(ROOT/'02_identity_and_evidence/results/candidate_evidence_profiles.csv')
ids={r['candidate_id']:r for r in profiles}
keys={(norm(r['doi']),norm(r['compound'])) for r in current}
rows=[]
for i,r in enumerate(legacy,2):
    if not r['original_value'].strip():continue
    cid=r['candidate_id'];matches=[x for x in profiles if norm(x['pubchem_cid'].removesuffix('.0'))==norm(r['PubChem_CID'].removesuffix('.0'))] if r['PubChem_CID'].strip() else []
    mapped=cid if cid in ids else (matches[0]['candidate_id'] if len(matches)==1 else '')
    doi=norm(r['DOI']);name=norm(r['compound'])
    exact=(doi,name) in keys
    mapped_match=bool(mapped) and any(norm(x['doi'])==doi and x['candidate_id']==mapped for x in current)
    rows.append(dict(legacy_csv_row=i,legacy_candidate_id=cid,proposed_current_candidate_id=mapped,identity_mapping_basis='EXISTING_ID' if cid in ids else 'UNIQUE_PUBCHEM_CID_CANDIDATE_ONLY' if mapped else 'UNRESOLVED',compound=r['compound'],doi=doi,doi_url='https://doi.org/'+doi if doi else '',assay=r['assay'],original_value=r['original_value'],original_unit=r['original_unit'],normalized_value=r['normalized_value'],normalized_unit=r['normalized_unit'],source_locator='; '.join(r[k] for k in ['exact_table','exact_figure','exact_page','supplementary_location'] if r[k]),legacy_record_id=r['legacy_record_id'],source_file=str(legacy_path.relative_to(ROOT)).replace('\\','/'),coverage_status='PRESENT_BY_DOI_AND_NAME' if exact else 'POSSIBLE_PRESENT_BY_DOI_AND_ID_REVIEW_FORM' if mapped_match else 'NOT_MATCHED_IN_CURRENT_QUANTITATIVE_SUBSET',import_status='INVENTORY_ONLY_NOT_MODEL_INPUT',human_review_status='NOT_REVIEWED',change_applied='NO'))
assert len({r['legacy_csv_row'] for r in rows})==len(rows)
with (P/'results/Legacy_Quantitative_Coverage.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
summary=dict(legacy_numeric_rows=len(rows),exact_doi_name_matches=sum(r['coverage_status']=='PRESENT_BY_DOI_AND_NAME' for r in rows),possible_doi_id_matches=sum(r['coverage_status']=='POSSIBLE_PRESENT_BY_DOI_AND_ID_REVIEW_FORM' for r in rows),not_matched_rows=sum(r['coverage_status']=='NOT_MATCHED_IN_CURRENT_QUANTITATIVE_SUBSET' for r in rows),new_model_rows_imported=0,warning='Inventory rows are not unique studies or confirmed missing observations. Identity, assay, units and duplicate keys require review.')
(P/'results/legacy_coverage_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary))
