"""Make source-specific protocol constraints explicit; do not fit across methods."""
import csv,json,itertools
from pathlib import Path
P=Path(__file__).resolve().parent
# Curated original Methods/Table locations, not inferred from assay labels.
sources=[
dict(doi='10.3390/foods10081807',locator='Methods 2.5.4; Table 5',endpoint='Net-AUC concentration-slope ratio versus Trolox',pH='7',temperature_C='37',duration_minutes='55',read_interval_minutes='5',vehicle='PBS working solutions; final ethanol fraction unresolved',replication='Table caption: 3 independent experiments',error='SD explicit',variance='SD^2/3 conditional on author independence; shared calibration covariance unknown',compounds='Eugenol; Capsaicin; Vanillin'),
dict(doi='10.1039/d1ra08918h',locator='Methods 2.2; Table 1',endpoint='Molar TE; Watanabe A/B variants recovered, actual study variant unresolved',pH='7.4',temperature_C='',duration_minutes='',read_interval_minutes='',vehicle='Stock methanol/water/acetic acid 90:9.5:0.5; final well fraction unresolved',replication='Three measurements; independent batches unresolved',error='SD explicit in Table 1',variance='Not assigned',compounds='Eugenol; Gentisic acid; p-Coumaric acid; Ferulic acid; other phenols'),
dict(doi='10.3390/antiox11091784',locator='Methods 2.1 and 2.2.2; Table 2',endpoint='Dose-specific micromolar TE at 2.5 and 5 micromolar compound',pH='',temperature_C='',duration_minutes='80',read_interval_minutes='',vehicle='Stock ethanol/water 80:20; final well fraction unresolved',replication='Three replicates; independent batches unresolved',error='Plus/minus type unresolved',variance='Not assigned',compounds='Gentisic acid; Vanillic acid; Syringic acid; Gallic acid; Caffeic acid; Ferulic acid; p-Coumaric acid'),
dict(doi='10.3390/ijms150916351',locator='Methods 3.2.3; Table 2',endpoint='Trolox net-AUC calibration regression; micromolar TE per micromolar antioxidant',pH='7.40',temperature_C='37',duration_minutes='60',read_interval_minutes='1',vehicle='All ORAC solutions in 75 mM sodium phosphate buffer',replication='Four replicates per sample or standard; independent batches unresolved',error='Table 2 plus/minus type unresolved',variance='Not assigned; do not borrow ABTS or other assay error definitions',compounds='Vanillic acid; Syringic acid; p-Hydroxybenzoic acid; Gallic acid; Ferulic acid; p-Coumaric acid; vitamin C'),
dict(doi='10.3390/antiox12020505',locator='Methods ORAC and data comparison; Table 3',endpoint='AUC calibration-slope ratio versus matched Trolox',pH='7.4',temperature_C='37',duration_minutes='Up to 180 recording; common AUC cutoff unresolved',read_interval_minutes='1',vehicle='Quercetin/caffeic acid 5% ethanol; other working solutions buffer',replication='Triplicate solutions on two days; effective endpoint n unresolved',error='Table 3 plus/minus type unresolved',variance='Not assigned',compounds='Gallic acid; Caffeic acid; Quercetin; vitamin C; GSH')]
def write(name,rows):
    with (P/'results'/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
for s in sources:
    s.update(doi_url='https://doi.org/'+s['doi'],review_scope='Original article text/table check; inherited SOP and supplements not fully recovered',human_review_status='NOT_REVIEWED',change_applied='NO')
write('Bridge_Protocol_Matrix.csv',sources)
pairs=[]
for a,b in itertools.combinations(sources,2):
    overlap=sorted(set(a['compounds'].split('; '))&set(b['compounds'].split('; ')))
    if not overlap:continue
    pairs.append(dict(doi_a=a['doi'],doi_b=b['doi'],reported_shared_names='; '.join(overlap),shared_names_scope='Source-level named compounds; not all have new row-level checks',decision='DO_NOT_POOL_CURRENTLY',reason='Endpoint/timing/vehicle definitions differ or remain incomplete; independent sampling structure and covariance unresolved',identity_note='Named overlap does not establish exact material/form equivalence',human_review_status='NOT_REVIEWED',change_applied='NO'))
write('Bridge_Pairwise_Decisions.csv',pairs)
assert len(sources)==5 and all(s['change_applied']=='NO' for s in sources)
assert all(p['decision']=='DO_NOT_POOL_CURRENTLY' for p in pairs)
print(f'QC PASS: {len(sources)} source protocols; {len(pairs)} named-overlap comparisons; no pooling approved.')
