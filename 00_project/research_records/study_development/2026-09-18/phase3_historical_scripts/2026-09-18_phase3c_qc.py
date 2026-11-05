import csv
from pathlib import Path

R=Path(__file__).resolve().parents[1]
def rows(p):
    with open(R/p,encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))

lock=rows('data/Carotenoid_Phase3_Eligibility_Lock.csv')
ev=rows('data/Carotenoid_Singlet_Oxygen_Evidence_Master.csv')
top=rows('data/Carotenoids_TopN_v1.0.csv')
glob=rows('data/Global_Top_Overview_Master_v0.2.csv')
assert len(lock)==19 and len({x['candidate_id'] for x in lock})==19
assert sum(x['ranking_eligible']=='yes' for x in lock)==17
assert all(x['micelle_or_liposome']=='homogeneous organic solvent' for x in ev)
assert all(x['tier'] in {'A','B1','B2','C','X'} for x in ev)
assert all(float(x['normalized_kq_value'])>=0 for x in ev)
assert len(top)==9 and [int(x['rank']) for x in top]==list(range(1,10))
assert all(float(top[i]['median_kq'])>=float(top[i+1]['median_kq']) for i in range(len(top)-1))
assert not any(x['compound'] in {'Astaxanthin','Fucoxanthin'} for x in top)
assert len(glob)==47 and sum(x['analysis_panel']=='Carotenoids' for x in glob)==9
assert all(x['overview_version']=='v0.2' for x in glob)
assert all(x['primary_unit']=='10^9 M^-1 s^-1' for x in glob if x['analysis_panel']=='Carotenoids')
assert all((R/'figures'/n).exists() and (R/'figures'/n).stat().st_size>10000 for n in [
 'Carotenoid_TopN_Primary_Construct.png','Carotenoid_Evidence_Confidence.png','Carotenoid_Environment_Coverage.png','Carotenoid_Primary_vs_LipidPhase_Profile.png','Global_Overview_With_Carotenoids.png'])
print({'lock':len(lock),'eligible':17,'evidence':len(ev),'top_available':len(top),'global_v02':len(glob),'figures':'PASS'})
