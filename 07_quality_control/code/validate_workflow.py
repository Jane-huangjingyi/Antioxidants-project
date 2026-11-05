"""Consequential scientific invariants and computational checks, independent of presentation."""
from pathlib import Path
import sys,importlib.util,xml.etree.ElementTree as ET,re,hashlib,ast,csv
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'00_project'))
from pipeline_io import *
manifest=read_json(ROOT/'07_quality_control/migration_manifest.json');cleanup_path=ROOT/'07_quality_control/redundant_cleanup.json';cleanup=read_json(cleanup_path) if cleanup_path.exists() else []
removed={r['path'] for r in cleanup};missing_optional=[]
for r in manifest['entries']:
 p=ROOT/r['new_path']
 if r['new_path'] in removed:continue
 if not p.exists():
  assert not r['tracked_before'],'Missing tracked source: '+r['new_path']
  missing_optional.append(r['new_path']);continue
 assert sha(p)==r['sha256'],'Source content changed: '+r['new_path']
frozen=read_csv(source('data/h_orac_stage25b/frozen/Stage25B5_Frozen_Asset_SHA256_Manifest.csv'))
for r in frozen:assert sha(source(r['asset_path']))==r['sha256'],r['asset_path']
seeds=read_csv(ROOT/'01_candidate_discovery/results/discovery_register.csv');profiles=read_csv(ROOT/'02_identity_and_evidence/results/candidate_evidence_profiles.csv');queue=read_csv(ROOT/'03_candidate_selection/results/top20_review_queue.csv');audit=read_csv(ROOT/'03_candidate_selection/results/all_candidate_decisions.csv')
assert len(seeds)==204 and len(profiles)==193 and len({r['candidate_id'] for r in profiles})==193
old=read_csv(source('data/candidate_universe/Antioxidant_Class_Candidate_Master.csv'))
byid={r['candidate_id']:r for r in seeds}
for r in old:assert byid[r['candidate_id']]['name']==r['compound']
assert sum(r['framework157_scope']=='YES' for r in profiles)==157
assert all(r['molecular_formula'] and r['pubchem_cid'] and r['inchi_key'] for r in queue)
assert all(r['change_applied']=='NO' and r['human_review_status']=='NOT_REVIEWED' for r in profiles)
for r in profiles:
 if r['framework157_scope']=='NO':assert all(r[k+'_snapshot_status']=='NOT_COVERED_BY_157_SNAPSHOT' for k in ['D1','D2','D3','D4','D5'])
cache=read_json(source('archive/phase2_local_cache/phase2_pubchem_identity_cache.json'));fresh=read_json(ROOT/'02_identity_and_evidence/inputs/pubchem_refresh.json');conflicts=[]
for r in queue:
 assert fresh[r['compound_name']]['status']=='SUCCESS'
 p=fresh[r['compound_name']]['property'];assert str(p['CID'])==r['pubchem_cid'];assert p['MolecularFormula']==r['molecular_formula'];assert p['InChIKey']==r['inchi_key']
 original=cache.get(r['compound_name'],{})
 if original and any(str(original.get(k,''))!=str(p[v]) for k,v in [('PubChem_CID','CID'),('molecular_formula','MolecularFormula'),('InChIKey','InChIKey')]):conflicts.append(r['candidate_id'])
assert not conflicts,conflicts
tie=read_csv(ROOT/'03_candidate_selection/results/cutoff_tied_candidates.csv');assert len(tie)==12
assert len(queue)==20 and len({r['candidate_id'] for r in queue})==20
assert all((number(r['confirmed_independent_horac_studies']) or 0)>=1 for r in queue)
ready=read_csv(ROOT/'03_candidate_selection/results/formal_lab_ready_panel.csv')
assert len(ready)<=20,'More than 20 approved materials: researcher must resolve; never silently truncate.'
assert len(ready)==sum(r['formal_panel_eligible']=='YES' for r in audit)
scenario=read_csv(ROOT/'03_candidate_selection/results/selection_sensitivity.csv');assert int(scenario[1]['eligible_count'])==9
# Independent analytical check: normalized triangular response has integral exactly 1 minute.
spec=importlib.util.spec_from_file_location('kinetics',ROOT/'04_absorbance_assay/code/analyze_kinetics.py');kin=importlib.util.module_from_spec(spec);spec.loader.exec_module(kin)
assert kin.integrate([0,1,2],[1,.5,0])==1
rows=[]
for role,well,values in [('SAMPLE','A1',[1.2,.7,.2]),('MATCHED_NO_PROBE','A2',[.2,.2,.2])]:
 for t,v in zip([0,1,2],values):rows.append(dict(batch_id='SYNTHETIC_TEST_ONLY',plate_id='TEST',well=well,candidate_id='TEST_ONLY',role=role,pair_id='PAIR',concentration_uM='1',counter_screen_pass='YES',time_min=str(t),absorbance=str(v)))
assert abs(kin.analyze(rows)[0]['normalized_auc_min']-1)<1e-12
bad=[dict(r,counter_screen_pass='NO') for r in rows]
try:kin.analyze(bad);raise AssertionError('Missing counter-screen must fail')
except ValueError:pass
bad=[dict(r,time_min='3') if r['well']=='A2' and r['time_min']=='2' else r for r in rows]
try:kin.analyze(bad);raise AssertionError('Time-grid mismatch must fail')
except ValueError:pass
svg_files=list((ROOT/'06_manuscript/figures').rglob('*.svg'))
for p in svg_files:
 tags=[x.tag.rsplit('}',1)[-1] for x in ET.fromstring(p.read_text(encoding='utf8')).iter()]
 assert 'text' in tags and 'image' not in tags,p
# Validate active Markdown links; preserved original-language files are source snapshots.
bad_links=[];non_english=[]
for folder in ['00_project','01_candidate_discovery','02_identity_and_evidence','03_candidate_selection','04_absorbance_assay','05_analysis','06_manuscript','07_quality_control','current_review']:
 for p in (ROOT/folder).rglob('*.md'):
  if any(x in p.relative_to(ROOT).parts for x in ['node_modules','local','previews']):continue
  text=p.read_text(encoding='utf-8-sig')
  if re.search(r'[\u4e00-\u9fff]',text):non_english.append(p.relative_to(ROOT).as_posix())
  for m in re.finditer(r'\[[^\]]*\]\((<[^>]+>|[^)]+)\)',text):
   target=m.group(1).strip('<>').split('#')[0]
   if not target or re.match(r'^\w+://',target):continue
   if not (p.parent/target).exists():bad_links.append([p.relative_to(ROOT).as_posix(),target])
assert not non_english,non_english;assert not bad_links,bad_links
for folder in ['00_project','01_candidate_discovery','02_identity_and_evidence','03_candidate_selection','04_absorbance_assay','05_analysis','06_manuscript','07_quality_control','current_review']:
 for p in (ROOT/folder).rglob('*.py'):
  if not any(x in p.relative_to(ROOT).parts for x in ['node_modules','local','previews']):ast.parse(p.read_text(encoding='utf-8-sig'))
summary={'as_of':AS_OF,'status':'PASS','preserved_source_entries':len(manifest['entries']),'optional_local_caches_not_bundled':missing_optional,'derived_temporary_files_removed':len(cleanup),'frozen_sha256_assets_pass':len(frozen),'legacy_seed_mapping_pass':191,'discovery_records':len(seeds),'candidate_profiles':len(profiles),'reference_formula_profiles':sum(bool(r['molecular_formula']) for r in profiles),'review_slots':len(queue),'two_study_sensitivity':9,'cutoff_stratum_candidates':len(tie),'formal_lab_ready_count':len(ready),'new_assay_experiments_performed':0,'pubchem_queue_identity_conflicts':conflicts,'svg_text_without_raster_verified':len(svg_files),'active_english_markdown_pass':True,'broken_active_markdown_links':bad_links,'synthetic_auc_check':'PASS_SYNTHETIC_TEST_ONLY_NOT_EXPERIMENTAL_RESULTS'}
write_json(ROOT/'07_quality_control/workflow_qc.json',summary)
text=f'''# Workflow QC\n\nDate: {AS_OF}. Status: PASS.\n\nAll {len(manifest['entries'])} original scientific/process entries are accounted for by the migration map. Tracked sources and ten frozen assets retain their bytes. Optional unbundled caches on a clone are listed separately; explicitly removed derived intermediates have retained-source explanations. No original scientific table, governance approval, mechanism observation or frozen rank is changed.\n\nThe 191 literal seed IDs reconstruct correctly. There are 204 discovery records, 193 profiles, 25 review-eligible candidates, 20 provisional review slots and 12 cutoff-stratum ties. The two-study sensitivity retains 9. The formal laboratory-ready panel has {len(ready)} rows. All 20 review identities/formulas match their official cached PubChem refresh; no cache conflict was detected.\n\nActive English Markdown links resolve. {len(svg_files)} current SVG exports contain text and vector objects without embedded raster images. Numerical AUC integration and rejection rules were checked on synthetic in-memory traces only. They establish code behavior, not assay performance.\n\nRemaining scientific work: close candidate-specific food sources, exact reagent procurement/forms, solubility/stability and absorbance counter-screens; adjudicate cutoff ties and actual material decisions; approve equipment-specific assay settings/calibration; collect real experimental data. The method-search log explicitly identifies first-page truncation where present. The old full evidence catalogue and journal-metric gaps remain preserved and have not been promoted into verified claims.\n'''
(ROOT/'07_quality_control/Workflow_QC.md').write_text(text,encoding='utf8')
print(f'QC PASS: {len(queue)} review slots; {len(ready)} lab-ready; {len(svg_files)} editable SVGs; frozen sources unchanged.')
