"""Reconcile four parent-name variants in an already reviewed historical table.

Original extraction files remain the raw transcription. This overlay retains
the original evidence IDs so each observation is represented once in the audit.
"""
from pathlib import Path
import csv

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
NAMES={'Kaempferol-3-O-glucoside':'Kaempferol 3-O-glucoside',
       'Myricetin-3-rhamnoside':'Myricitrin',
       'Cyanidin-3-O-rutinoside':'Cyanidin 3-O-rutinoside',
       'Delphinidin-3-O-glucoside':'Delphinidin 3-O-glucoside'}


def read(path):
    with path.open(encoding='utf-8-sig',newline='') as handle:return list(csv.DictReader(handle))


def main():
    raw=read(ROOT/'02_identity_and_evidence/02_user_supplied_sources/Original_Capacity_Extraction.csv')
    profiles={r['compound_name']:r for r in read(ROOT/'02_identity_and_evidence/result/table/candidate_evidence_profiles.csv')}
    rows=[]
    for r in raw:
        if r['doi']!='10.1016/j.foodchem.2008.08.013' or r['source_compound_name'] not in NAMES:continue
        p=profiles[NAMES[r['source_compound_name']]]
        rows.append(dict(extraction_id=r['evidence_id'],candidate_id=p['candidate_id'],compound_name=r['source_compound_name'],
                         candidate_name=p['compound_name'],candidate_mapping='CONDITIONAL_PARENT_NAME_RECONCILIATION_EXACT_FORM_PENDING',
                         doi=r['doi'],PMCID='',source_row=r['source_row'],source_locator=r['numeric_locator'],
                         raw_mean=r['mean'],raw_error=r['reported_error'],raw_units=r['raw_units'],error_type=r['error_type'],
                         reported_replication=r['reported_replication'],independent_n='',assay='ORAC_FL',pH=r['pH'],temperature_C=r['temperature_C'],
                         integration_rule=r['protocol_stratum'],reference_MW_g_mol='',conditional_molar_capacity=r['mean'],conditional_molar_error='',
                         conversion_rule='SOURCE_TROLOX_NORMALIZED_RATIO_NO_NEW_NUMERIC_CONVERSION',
                         source_experiment_cluster=r['doi'],source_independence='SAME_EXISTING_DOI_AND_EVIDENCE_ID',
                         unresolved_fields='Historical2009 source; exact salt,sugar anomer,purity and final vehicle remain unresolved. Original source spelling preserved.',
                         source_url='https://doi.org/'+r['doi'],source_file=r['source_document'],source_sha256=r['source_sha256'],
                         extraction_date='2026-11-16',model_label_release='NO',human_review_status='NOT_REVIEWED',change_applied='NO',
                         protocol_stratum=r['protocol_stratum'],source_path_relative_to='PROJECT_ROOT'))
    assert len(rows)==4 and len({r['extraction_id'] for r in rows})==4
    with (HERE/'Historical_Parent_Name_Reconciliation.csv').open('w',encoding='utf8',newline='') as handle:
        writer=csv.DictWriter(handle,fieldnames=list(rows[0]),lineterminator='\n');writer.writeheader();writer.writerows(rows)
    print('Four existing source observations reconciled by parent name; original IDs and values retained.')


if __name__=='__main__':main()
