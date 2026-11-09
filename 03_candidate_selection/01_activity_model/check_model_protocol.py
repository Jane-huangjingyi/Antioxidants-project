"""Check feasibility of the proposed validation before fitting or splitting labels."""
import csv,json,collections
from pathlib import Path
P=Path(__file__).resolve().parent
protocol=json.loads((P/'inputs/model_protocol_v0.1.json').read_text())
with (P/'results/Model_Input_Candidates.csv').open(encoding='utf-8-sig') as f:r=list(csv.DictReader(f))
from protocol_scope import scope_index,classify
lookup=scope_index();all_rows=r
r=[x for x in all_rows if classify(x['candidate_id'],x['doi'],lookup)['status']=='MATCH_CORE_CONDITIONS_PROTOCOL_STRATUM_PENDING']
papers={x['doi'] for x in r};folds=[]
for paper in sorted(papers):
    train=[x for x in r if x['doi']!=paper];test=[x for x in r if x['doi']==paper]
    known={x['candidate_id'] for x in train};overlap=sum(x['candidate_id'] in known for x in test)
    folds.append(dict(held_out_doi=paper,training_rows=len(train),test_rows=len(test),test_compounds_seen_in_training=overlap,test_compounds_unseen=len(test)-overlap,compound_effect_prediction_status='UNSUPPORTED_UNSEEN_COMPOUNDS' if overlap==0 else 'PARTIAL_SUPPORT_REVIEW_REQUIRED',interpretation='Core-condition identity-coverage diagnostic only; protocol strata remain unresolved; not an authorized validation fold'))
with (P/'results/Model_Validation_Feasibility.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(folds[0]));w.writeheader();w.writerows(folds)
assert len(folds)==2 and all(x['test_compounds_seen_in_training']==0 for x in folds)
out=dict(status='PRIMARY_CROSS_PAPER_MODEL_NOT_FITTED',endpoint_decision=protocol['researcher_confirmed_endpoint'],active_experimental_route=protocol.get('active_experimental_route',''),literature_model_role=protocol.get('ORAC_FL_model_role',''),model_candidate_rows=len(all_rows),core_condition_candidate_rows=len(r),outside_or_unconfirmed_rows=len(all_rows)-len(r),candidate_core_match_not_fit_approval=True,papers=len(papers),leave_paper_out_folds=len(folds),folds_without_seen_test_compounds=len(folds),unset_target_condition_fields=[k for k,v in protocol['target_conditions'].items() if v is None and k not in protocol.get('stratification_fields',[])],target_conditions=protocol['target_conditions'],stratified_target_fields=protocol.get('stratification_fields',[]),ranking_generated=False)
(P/'results/model_protocol_readiness.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))
