"""Partition rechecked evidence by estimand; quantify validation support before fit."""
import csv,json,collections
from pathlib import Path
P=Path(__file__).resolve().parent
def read(n):
    with (P/'results'/n).open(encoding='utf-8-sig') as f:return list(csv.DictReader(f))
def write(n,r):
    with (P/'results'/n).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(r[0]));w.writeheader();w.writerows(r)
policies={
'10.3390/antiox12020505':('AUC_SLOPE_RATIO','Up to 180 min recording; integration cutoff unresolved'),
'10.3390/foods10081807':('AUC_SLOPE_RATIO','55 min; pH 7'),
'10.1039/d1ra08918h':('INHERITED_SOP_VARIANT_PENDING','Watanabe A/B assignment unresolved'),
'10.3390/antiox11091784':('DOSE_SPECIFIC_TE_RATIO','80 min; dose-specific, not a calibration slope'),
'10.3390/ijms150916351':('TROLOX_REGRESSION_TE','60 min; pH 7.4'),
'10.3390/foods10051079':('SOURCE_MOLAR_TE_PROTOCOL_REVIEW','Exact integration/calibration family still requires review'),
'10.3390/ijms20092328':('EXPERIMENTAL_LOG_ORAC','Log location, not arithmetic mean'),
'10.1016/j.foodchem.2010.11.092':('MASS_NORMALIZED_LINEAR_CONVERSION','Mean/SD linear conversion; replication independence unresolved')}
old={(r['candidate_id'],r['doi']):r for r in read('Model_Input_Candidates.csv')}
rows=[]
for i,r in enumerate(read('Capacity_Analysis_Entry.csv'),1):
    if r['comparison_scope']=='BASELINE_SOURCE_REVIEW_PENDING':continue
    fam,note=policies[r['doi']];m=old.get((r['candidate_id'],r['doi']),{})
    held=r['comparison_scope']=='SOURCE_IDENTITY_CONFLICT_DESCRIPTIVE_RANK_HELD'
    rows.append(dict(evidence_row=i,candidate_id=r['candidate_id'],compound=r['compound'],doi=r['doi'],source_locator=r['source_locator'],value=r['value'],scale=r['scale'],reported_error=r['error'],error_type=r['error_type'],dose_uM=r['dose_uM'],estimator_family=fam,protocol_constraint=note,identity_gate='SOURCE_CONFLICT_HOLD' if held else 'NO_NEW_SOURCE_CONFLICT_DETECTED_NOT_FORM_APPROVAL',conditional_variance=m.get('variance_of_mean_candidate',''),variance_scope=m.get('variance_assumptions','No sampling variance assigned'),analysis_eligibility='HOLD' if held else 'SOURCE_SPECIFIC_DESCRIPTIVE_ONLY',cross_paper_fit_status='NOT_READY_TARGET_AND_PROTOCOL_ALIGNMENT_REQUIRED',human_review_status='NOT_REVIEWED',change_applied='NO'))
assert len(rows)==31
write('Extended_Model_Input_Review.csv',rows)
folds=[]
families=collections.defaultdict(list)
for r in rows:
    if r['analysis_eligibility']!='HOLD':families[r['estimator_family']].append(r)
for family,group in sorted(families.items()):
    papers=sorted({r['doi'] for r in group})
    for paper in papers:
        train=[r for r in group if r['doi']!=paper];test=[r for r in group if r['doi']==paper]
        seen={r['candidate_id'] for r in train};known={r['candidate_id'] for r in test}&seen
        folds.append(dict(estimator_family=family,held_out_doi=paper,training_rows=len(train),test_rows=len(test),seen_test_compounds=len(known),unseen_test_compounds=len({r['candidate_id'] for r in test}-seen),status='NO_OTHER_PAPER_IN_FAMILY' if not train else 'NO_SHARED_COMPOUND_FOR_IDENTITY_EFFECT_VALIDATION' if not known else 'PROTOCOL_ALIGNMENT_STILL_REQUIRED'))
write('Extended_Validation_Feasibility.csv',folds)
out=dict(reviewed_rows=len(rows),source_identity_holds=sum(r['analysis_eligibility']=='HOLD' for r in rows),source_descriptive_rows=sum(r['analysis_eligibility']!='HOLD' for r in rows),estimator_families=len(families),source_papers=len({r['doi'] for r in rows}),conditional_variance_rows=sum(bool(r['conditional_variance']) for r in rows),cross_paper_models_fitted=0,global_ranking_generated=False,scope='31 rechecked rows in the 99-row integrated inventory; other separately extracted source leads not automatically included')
(P/'results/extended_model_readiness.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))
