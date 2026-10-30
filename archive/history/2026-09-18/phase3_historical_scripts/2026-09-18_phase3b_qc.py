import csv, os, math
from collections import Counter

ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data")
def read(name):
    with open(os.path.join(DATA,name),encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))

lock=read("PhenolicAcid_Phase3_Eligibility_Lock.csv")
ev=read("PhenolicAcid_H_ORAC_Evidence_Master.csv")
rank=read("Polyphenols_PhenolicAcids_TopN_v1.0.csv")
cov=read("PhenolicAcid_Ranking_Coverage.csv")
assert len(lock)==29
assert Counter(x["ranking_eligible"] for x in lock)==Counter({"eligible_for_ranking":25,"hold":4})
assert Counter(x["tier"] for x in ev)==Counter({"B1":34,"X":12,"B2":1})
assert len(rank)==18 and [int(x["rank"]) for x in rank]==list(range(1,19))
assert all(float(rank[i]["median_H_ORAC"])>=float(rank[i+1]["median_H_ORAC"]) for i in range(len(rank)-1))
ids={x["evidence_id"] for x in ev}
assert len(ids)==len(ev)
for r in rank:
    p=set(r["provenance_record_ids"].split(";")); assert p and p<=ids
    src=[x for x in ev if x["evidence_id"] in p]
    vals=sorted(float(x["normalized_value_mol_TE_mol"]) for x in src)
    assert len(vals)==int(r["eligible_record_count"])
    assert math.isclose(float(r["median_H_ORAC"]),(vals[(len(vals)-1)//2]+vals[len(vals)//2])/2,abs_tol=1e-3)
assert sum(int(x["universe_N"]) for x in cov)==29
assert sum(int(x["TopN_N"]) for x in cov)==18
dupes=[k for k,n in Counter((x["compound"],x["independent_experiment_id"],x["tier"],x["normalized_value_mol_TE_mol"]) for x in ev).items() if n>1]
assert not dupes
print("Phase 3B QC PASS: 29 lock rows; 47 evidence rows; 18 ranked compounds; provenance, medians, counts and duplicate checks passed.")
