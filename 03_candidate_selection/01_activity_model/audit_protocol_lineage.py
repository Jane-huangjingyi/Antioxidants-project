"""Track shared cited-SOP conditions without inferring the executed method variant."""
import csv,json
from pathlib import Path
P=Path(__file__).resolve().parent
c=json.loads((P/'inputs/sakurai_targeted_recheck.json').read_text(encoding='utf-8'))
a=c['protocol_lineage_recheck']
assert a['source_acceptance_halfwidth_umol_TE_L']==2*a['qc_reference_reproducibility_SD_umol_TE_L']
with (P/'results/Capacity_Analysis_Entry.csv').open(encoding='utf-8-sig') as f:
    inventory=list(csv.DictReader(f))
rows=[]
for r in inventory:
    if r['doi']!=c['doi']:continue
    rows.append(dict(candidate_id=r['candidate_id'],compound=r['compound'],doi=r['doi'],
        source_locator='Methods 2.2; cited SOP pp160/162/164',cited_method_doi=a['cited_method_doi'],
        directly_reported_pH=a['direct_source_pH'],inherited_shared_temperature_C=a['shared_cited_temperature_C'],
        temperature_status=a['temperature_status'],inherited_shared_read_interval_min=a['shared_cited_read_interval_min'],
        inherited_shared_auc_window_min='8-90',executed_variant_status=a['variant_status'],
        final_vehicle_status='UNRESOLVED_DO_NOT_ASSIGN_B_MATRIX',
        final_estimator_status='A_OR_B_NOT_RESOLVED_NO_SHARED_FINAL_ESTIMATOR_ASSUMED',
        qc_range_is_compound_SD='NO',qc_reference_halfwidth_equals_2SR='YES',
        independent_preparations='UNRESOLVED',primary_label_released='NO',
        human_review_status='NOT_REVIEWED',change_applied='NO'))
assert len(rows)==9 and len({r['candidate_id'] for r in rows})==9
with (P/'results/Protocol_Lineage_Check.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
summary=dict(existing_observations_mapped=len(rows),new_observations=0,new_numeric_values_verified=0,
    source_pH_direct=7.4,cited_A_B_shared_temperature_C=37,executed_SOP_variant_confirmed=False,
    qc_reference_halfwidth_is_2SR=True,compound_error_values_changed=0,primary_labels_released=0)
(P/'results/protocol_lineage_summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
print(json.dumps(summary))
