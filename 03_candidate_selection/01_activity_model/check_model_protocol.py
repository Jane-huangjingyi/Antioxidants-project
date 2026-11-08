"""Check feasibility of the proposed validation before fitting or splitting labels."""
import csv,json,collections
from pathlib import Path
P=Path(__file__).resolve().parent
protocol=json.loads((P/'inputs/model_protocol_v0.1.json').read_text())
with (P/'results/Model_Input_Candidates.csv').open(encoding='utf-8-sig') as f:r=list(csv.DictReader(f))
papers={x['doi'] for x in r};folds=[]
for paper in sorted(papers):
    train=[x for x in r if x['doi']!=paper];test=[x for x in r if x['doi']==paper]
    known={x['candidate_id'] for x in train};overlap=sum(x['candidate_id'] in known for x in test)
    folds.append(dict(held_out_doi=paper,training_rows=len(train),test_rows=len(test),test_compounds_seen_in_training=overlap,test_compounds_unseen=len(test)-overlap,compound_effect_prediction_status='UNSUPPORTED_UNSEEN_COMPOUNDS' if overlap==0 else 'PARTIAL_SUPPORT_REVIEW_REQUIRED',interpretation='Design diagnostic only; structural-model predictions are a distinct future task'))
with (P/'results/Model_Validation_Feasibility.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(folds[0]));w.writeheader();w.writerows(folds)
assert len(folds)==3 and all(x['test_compounds_seen_in_training']==0 for x in folds)
out=dict(status='PROTOCOL_DEFINED_NOT_FITTED',endpoint_decision=protocol['researcher_confirmed_endpoint'],model_candidate_rows=len(r),papers=len(papers),leave_paper_out_folds=len(folds),folds_without_seen_test_compounds=len(folds),unset_target_condition_fields=[k for k,v in protocol['target_conditions'].items() if v is None],ranking_generated=False)
(P/'results/model_protocol_readiness.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))
