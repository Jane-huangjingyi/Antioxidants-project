import csv, hashlib, shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(p):
 with (ROOT/p).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def write(p,fields,rows):
 q=ROOT/p; q.parent.mkdir(parents=True,exist_ok=True)
 with q.open('w',encoding='utf-8',newline='') as f:w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');w.writeheader();w.writerows(rows)
def append_text(p,marker,text):
 q=ROOT/p; old=q.read_text(encoding='utf-8-sig') if q.exists() else ''
 if marker not in old:q.write_text(old.rstrip()+'\n\n'+text.rstrip()+'\n',encoding='utf-8')
snapshot='data/h_orac_stage25b/frozen/Stage25B5_Canonical_Ranking_Snapshot.csv'
shutil.copyfile(ROOT/'data/h_orac_stage25b/stage25b/Stage25B_HORAC_Quantitative_Ranking.csv',ROOT/snapshot)

audit=read('figures/FIGURE_INVENTORY_AUDIT.csv'); existing={r['figure_file'] for r in audit}
audit_new=[
 {'figure_file':'HORAC_Primary_Top20_Frozen.png','folder':'aqueous_antioxidant_atlas','class':'Cross-class H-ORAC','figure_type':'ranking with heterogeneity','primary_message':'Frozen eligibility-defined Primary H-ORAC Top20 (A+B1)','source_data':'data/h_orac_stage25b/frozen/Stage25B_Frozen_Primary_HORAC_Top20.csv','x_variable':'median H-ORAC mol TE/mol','y_variable':'candidate in primary rank order','encoded_variables':'range; approximate IQR width; eligible experiment N; confidence','audience':'supervisor/downstream/QC','duplicated_with':'','redundancy_level':'unique','retain_or_archive':'retain','canonical_replacement':'','reason':'Only active canonical Stage25B.5 primary ranking figure.','notes':'R-generated; no singleton error bar'},
 {'figure_file':'HORAC_Top20_B2_Sensitivity.png','folder':'aqueous_antioxidant_atlas','class':'Cross-class H-ORAC','figure_type':'sensitivity membership change','primary_message':'B2 sensitivity changes Top20 membership by three enter/three leave','source_data':'data/h_orac_stage25b/frozen/Stage25B_Frozen_Top20_B2_Sensitivity_Qualification.csv','x_variable':'membership scenario','y_variable':'candidate','encoded_variables':'enter versus leave','audience':'supervisor/downstream/QC','duplicated_with':'','redundancy_level':'unique','retain_or_archive':'retain','canonical_replacement':'','reason':'Only active canonical B2 qualification figure; not a second ranking.','notes':'R-generated; membership changes only'}]
audit.extend(x for x in audit_new if x['figure_file'] not in existing); write('figures/FIGURE_INVENTORY_AUDIT.csv',list(audit[0]),audit)

mp=read('figures/FIGURE_CODE_DATA_MAP.csv'); mex={r['figure_path'] for r in mp}
map_new=[
 {'figure_path':'figures/aqueous_antioxidant_atlas/HORAC_Primary_Top20_Frozen.png','figure_name':'HORAC_Primary_Top20_Frozen.png','scientific_question':'Which candidates comprise the frozen eligibility-defined A+B1 H-ORAC Top20 and what are their evidence depth/heterogeneity?','stage':'Stage25B.5','canonical_status':'ACTIVE_CANONICAL','R_script_path':'R/stage25b5/01_render_frozen_primary_top20.R','input_data_path':'data/h_orac_stage25b/frozen/Stage25B_Frozen_Primary_HORAC_Top20.csv','required_columns':'primary_rank; canonical_name; median/min/max/IQR; eligible_A_B1_N; evidence_confidence','filter_summary':'exactly frozen ranks 1-20','transformation_summary':'no value transformation; range and approximate IQR displayed only when N>1','output_metric':'median H-ORAC mol TE/mol','user_editable_parameters':'image size; colors; margins','supervisor_use':'yes','notes':'Chemical capacity, not clinical/nutritional priority'},
 {'figure_path':'figures/aqueous_antioxidant_atlas/HORAC_Top20_B2_Sensitivity.png','figure_name':'HORAC_Top20_B2_Sensitivity.png','scientific_question':'Which memberships change when B2 is included only as sensitivity analysis?','stage':'Stage25B.5','canonical_status':'ACTIVE_CANONICAL','R_script_path':'R/stage25b5/02_render_b2_sensitivity.R','input_data_path':'data/h_orac_stage25b/frozen/Stage25B_Frozen_Top20_B2_Sensitivity_Qualification.csv','required_columns':'membership_change; candidate; sensitivity_rank','filter_summary':'exactly 3 ENTER and 3 LEAVE records','transformation_summary':'membership comparison only; no reranking graphic','output_metric':'Top20 membership change','user_editable_parameters':'image size; colors','supervisor_use':'yes','notes':'Qualification figure, not second formal ranking'}]
mp.extend(x for x in map_new if x['figure_path'] not in mex); write('figures/FIGURE_CODE_DATA_MAP.csv',list(mp[0]),mp)
append_text('figures/FIGURE_INDEX_CN.md','Stage25B.5 canonical H-ORAC figures','''## Stage25B.5 canonical H-ORAC figures

- `aqueous_antioxidant_atlas/HORAC_Primary_Top20_Frozen.png` / `.svg` — frozen A+B1 Top20, median H-ORAC with evidence depth and heterogeneity display.
- `aqueous_antioxidant_atlas/HORAC_Top20_B2_Sensitivity.png` / `.svg` — B2 sensitivity membership changes only (3 enter/3 leave), not a second formal ranking.

Deduplication audit found no pre-existing active Top20/ranking/sensitivity/cutoff figure carrying the same scientific message; therefore no archive move was required. Both canonical figures are reproducible from `R/stage25b5/` and the frozen CSV inputs.''')

assets=[
 'data/h_orac_stage25b/frozen/Stage25B_Frozen_Primary_HORAC_Top20.csv',
 'data/h_orac_stage25b/frozen/Stage25B_Top20_Freeze_Provenance.csv',
 'data/h_orac_stage25b/frozen/Stage25B_Frozen_Top20_B2_Sensitivity_Qualification.csv',
 'data/h_orac_stage25b/frozen/Stage25B_Final_Top20_Deliverable.csv',
 'docs/methods/h_orac_framework/H_ORAC_Evidence_Rubric_v2.0_CN.md',
 snapshot,
 'figures/aqueous_antioxidant_atlas/HORAC_Primary_Top20_Frozen.png',
 'figures/aqueous_antioxidant_atlas/HORAC_Primary_Top20_Frozen.svg',
 'figures/aqueous_antioxidant_atlas/HORAC_Top20_B2_Sensitivity.png',
 'figures/aqueous_antioxidant_atlas/HORAC_Top20_B2_Sensitivity.svg']
rows=[]
for p in assets:
 b=(ROOT/p).read_bytes(); rows.append({'asset_path':p,'sha256':hashlib.sha256(b).hexdigest(),'size_bytes':len(b),'freeze_version':'Stage25B Frozen Top20 v1.0','manifest_date':'2026-09-22'})
write('data/h_orac_stage25b/frozen/Stage25B5_Frozen_Asset_SHA256_Manifest.csv',list(rows[0]),rows)
print('Figure registry, canonical snapshot and SHA-256 manifest finalized.')
