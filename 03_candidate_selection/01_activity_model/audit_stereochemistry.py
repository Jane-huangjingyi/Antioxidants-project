"""Record database stereo completeness without assigning experimental stereochemistry."""
import csv,json,collections
from pathlib import Path
P=Path(__file__).resolve().parent
with (P/'results/Flavonoid_Structure_Audit.csv').open(encoding='utf-8-sig') as f:rows=list(csv.DictReader(f))
out=[]
for r in rows:
    defined=r['defined_atom_stereocentres'];undefined=r['undefined_atom_stereocentres']
    if not r['candidate_CID']:state='STRUCTURE_NOT_RECOVERED'
    elif defined=='' and undefined=='':state='DATABASE_ATOM_STEREO_COUNTS_NOT_RETRIEVED'
    elif undefined and int(undefined)>0:state='DATABASE_ATOM_STEREO_UNSPECIFIED'
    elif defined and int(defined)>0:state='DATABASE_ATOM_STEREO_SPECIFIED_SOURCE_MATCH_PENDING'
    else:state='NO_ATOM_STEREOCENTRES_REPORTED_NOT_FULL_STEREO_APPROVAL'
    out.append(dict(source_row=r['source_row'],compound=r['compound'],candidate_CID=r['candidate_CID'],InChIKey=r['candidate_InChIKey'],defined_atom_stereocentres=defined,undefined_atom_stereocentres=undefined,database_stereo_status=state,connectivity_leakage_group=r['connectivity_leakage_group'],experimental_stereo_status='UNRESOLVED_SOURCE_DRAWING_AND_MATERIAL_REQUIRED',grouping_rule='Same connectivity must remain in one validation group including stereoisomers',human_review_status='NOT_REVIEWED',change_applied='NO'))
with (P/'results/Flavonoid_Stereochemistry_Audit.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(out[0]));w.writeheader();w.writerows(out)
groups=collections.defaultdict(list)
for r in out:
    if r['connectivity_leakage_group']:groups[r['connectivity_leakage_group']].append(r['compound'])
summary=dict(records=len(out),database_stereo_counts=dict(collections.Counter(r['database_stereo_status'] for r in out)),shared_connectivity_groups=[v for v in groups.values() if len(v)>1],source_stereo_approved=0,scaffold_groups_computed=False)
(P/'results/stereochemistry_qc.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary))
