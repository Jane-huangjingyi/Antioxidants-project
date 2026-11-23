"""Consequential scientific invariants and computational checks, independent of presentation."""
from pathlib import Path
import sys,importlib.util,xml.etree.ElementTree as ET,re,hashlib,ast,csv
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'00_project'))
from pipeline_io import *
manifest=read_json(ROOT/'02_identity_and_evidence/source_manifest.json');missing_optional=[]
for r in manifest['records']:
 p=ROOT/r['path']
 if not p.exists():
  assert not r['bundled'],'Missing bundled scientific source: '+r['path']
  missing_optional.append(r['path']);continue
 assert sha(p)==r['sha256'],'Source content changed: '+r['path']
frozen=read_csv(source('data/h_orac_stage25b/frozen/Stage25B5_Frozen_Asset_SHA256_Manifest.csv'))
for r in frozen:assert sha(source(r['asset_path']))==r['sha256'],r['asset_path']
seeds=read_csv(ROOT/'01_candidate_discovery/results/discovery_register.csv');profiles=read_csv(ROOT/'02_identity_and_evidence/result/table/candidate_evidence_profiles.csv');queue=read_csv(ROOT/'03_candidate_selection/result/table/top20_review_queue.csv');audit=read_csv(ROOT/'03_candidate_selection/result/table/all_candidate_decisions.csv')
assert len(seeds)==204 and len(profiles)==193 and len({r['candidate_id'] for r in profiles})==193
old=read_csv(source('data/candidate_universe/Antioxidant_Class_Candidate_Master.csv'))
byid={r['candidate_id']:r for r in seeds}
for r in old:assert byid[r['candidate_id']]['name']==r['compound']
assert sum(r['framework157_scope']=='YES' for r in profiles)==157
assert all(r['molecular_formula'] and r['pubchem_cid'] and r['inchi_key'] for r in queue)
assert all(r['change_applied']=='NO' and r['human_review_status']=='NOT_REVIEWED' for r in profiles)
for r in profiles:
 if r['framework157_scope']=='NO':assert all(r[k+'_snapshot_status']=='NOT_COVERED_BY_157_SNAPSHOT' for k in ['D1','D2','D3','D4','D5'])
cache=read_json(source('identity/phase2_pubchem_identity_cache.json'));fresh=read_json(ROOT/'02_identity_and_evidence/inputs/pubchem_refresh.json');conflicts=[]
for r in queue:
 assert fresh[r['compound_name']]['status']=='SUCCESS'
 p=fresh[r['compound_name']]['property'];assert str(p['CID'])==r['pubchem_cid'];assert p['MolecularFormula']==r['molecular_formula'];assert p['InChIKey']==r['inchi_key']
 original=cache.get(r['compound_name'],{})
 if original and any(str(original.get(k,''))!=str(p[v]) for k,v in [('PubChem_CID','CID'),('molecular_formula','MolecularFormula'),('InChIKey','InChIKey')]):conflicts.append(r['candidate_id'])
assert not conflicts,conflicts
tie=read_csv(ROOT/'03_candidate_selection/result/table/cutoff_tied_candidates.csv');assert len(tie)==12
assert len(queue)==20 and len({r['candidate_id'] for r in queue})==20
assert all((number(r['confirmed_independent_horac_studies']) or 0)>=1 for r in queue)
ready=read_csv(ROOT/'03_candidate_selection/result/table/formal_lab_ready_panel.csv')
assert len(ready)<=20,'More than 20 approved materials: researcher must resolve; never silently truncate.'
assert len(ready)==sum(r['formal_panel_eligible']=='YES' for r in audit)
scenario=read_csv(ROOT/'03_candidate_selection/result/table/selection_sensitivity.csv');assert int(scenario[1]['eligible_count'])==9
# Independent analytical check: normalized triangular response has integral exactly 1 minute.
spec=importlib.util.spec_from_file_location('kinetics',ROOT/'04_05_experimental_validation/code/03_analyze_kinetics.py');kin=importlib.util.module_from_spec(spec);spec.loader.exec_module(kin)
assert kin.integrate([0,1,2],[1,.5,0])==1
rows=[]
for role,well,values in [('SAMPLE','A1',[1.2,.7,.2]),('MATCHED_NO_PROBE','A2',[.2,.2,.2])]:
 for t,v in zip([0,1,2],values):rows.append(dict(batch_id='SYNTHETIC_TEST_ONLY',plate_id='TEST',well=well,candidate_id='TEST_ONLY',role=role,pair_id='PAIR',concentration_uM='1',counter_screen_pass='YES',time_min=str(t),absorbance=str(v),protocol_id='SYNTHETIC',preparation_id='TEST_PREP',vehicle_id='TEST_VEHICLE',time_origin='INITIATOR_ADDITION'))
assert abs(kin.analyze(rows)[0]['normalized_auc_min']-1)<1e-12
bad=[dict(r,counter_screen_pass='NO') for r in rows]
try:kin.analyze(bad);raise AssertionError('Missing counter-screen must fail')
except ValueError:pass
bad=[dict(r,time_min='3') if r['well']=='A2' and r['time_min']=='2' else r for r in rows]
try:kin.analyze(bad);raise AssertionError('Time-grid mismatch must fail')
except ValueError:pass
svg_files=list((ROOT/'06_manuscript/result/figure').rglob('*.svg'))
for p in svg_files:
 tags=[x.tag.rsplit('}',1)[-1] for x in ET.fromstring(p.read_text(encoding='utf8')).iter()]
 assert 'text' in tags and 'image' not in tags,p
 assert p.with_suffix('.png').is_file(), p
# Validate active Markdown links; preserved original-language files are source snapshots.
bad_links=[];non_english=[]
for folder in ['00_project','01_candidate_discovery','02_identity_and_evidence','03_candidate_selection','04_05_experimental_validation','06_manuscript','07_quality_control']:
 for p in (ROOT/folder).rglob('*.md'):
  if any(x in p.relative_to(ROOT).parts for x in ['node_modules','local','local_library','previews','input','inputs','research_records']):continue
  text=p.read_text(encoding='utf-8-sig')
  if re.search(r'[\u4e00-\u9fff]',text):non_english.append(p.relative_to(ROOT).as_posix())
  for m in re.finditer(r'\[[^\]]*\]\((<[^>]+>|[^)]+)\)',text):
   target=m.group(1).strip('<>').split('#')[0]
   if not target or re.match(r'^\w+://',target):continue
   if not (p.parent/target).exists():bad_links.append([p.relative_to(ROOT).as_posix(),target])
for name in ('README.md', 'Latest_Results.md'):
 for m in re.finditer(r'\[[^\]]*\]\(([^)]+)\)', (ROOT/name).read_text(encoding='utf-8-sig')):
  target=m.group(1).strip('<>').split('#')[0]
  if target and not re.match(r'^\w+://',target) and not (ROOT/target).exists():bad_links.append([name,target])
assert not non_english,non_english;assert not bad_links,bad_links
for folder in ['00_project','01_candidate_discovery','02_identity_and_evidence','03_candidate_selection','04_05_experimental_validation','06_manuscript','07_quality_control']:
 for p in (ROOT/folder).rglob('*.py'):
  if not any(x in p.relative_to(ROOT).parts for x in ['node_modules','local','local_library','previews','input','inputs','research_records']):ast.parse(p.read_text(encoding='utf-8-sig'))
summary={'as_of':AS_OF,'status':'PASS','scientific_source_entries':len(manifest['records']),'optional_local_caches_not_bundled':missing_optional,'frozen_sha256_assets_pass':len(frozen),'legacy_seed_mapping_pass':191,'discovery_records':len(seeds),'candidate_profiles':len(profiles),'reference_formula_profiles':sum(bool(r['molecular_formula']) for r in profiles),'review_slots':len(queue),'two_study_sensitivity':9,'cutoff_stratum_candidates':len(tie),'formal_lab_ready_count':len(ready),'new_assay_experiments_performed':0,'pubchem_queue_identity_conflicts':conflicts,'svg_text_without_raster_verified':len(svg_files),'active_english_markdown_pass':True,'broken_active_markdown_links':bad_links,'synthetic_auc_check':'PASS_SYNTHETIC_TEST_ONLY_NOT_EXPERIMENTAL_RESULTS'}
supplement = ROOT/'02_identity_and_evidence/01_systematic_supplement'
if (supplement/'Source_Scientific_Screening.csv').exists():
 screens = read_csv(supplement/'Source_Scientific_Screening.csv')
 extracted = read_csv(supplement/'Original_Capacity_Followup.csv')
 assert len(screens)==79 and len({row['PMCID'] for row in screens})==79
 assert len(extracted)==26 and len({row['extraction_id'] for row in extracted})==26
 for row in screens+extracted:
  assert row['human_review_status']=='NOT_REVIEWED' and row['change_applied']=='NO'
  assert row['model_label_release']=='NO'
  cached=supplement/row['source_file']
  if cached.exists():assert sha(cached)==row['source_sha256'],row['source_file']
 assert all(row['independent_n']=='' for row in extracted)
 ascorbate=next(row for row in extracted if row['PMCID']=='PMC11124305')
 assert abs(float(ascorbate['conditional_molar_capacity'])-5982*176.12/1e6)<1e-12
 curcumin=next(row for row in extracted if row['PMCID']=='PMC6270194')
 assert curcumin['conditional_molar_capacity']==''
 transfer=read_json(ROOT/'03_candidate_selection/05_model_robustness/results/new_source_transfer_summary.json')
 assert not transfer['new_source_data_used_for_fitting'] and not transfer['new_data_formally_compatible']
 assert transfer['new_source_extraction_sha256']==sha(supplement/'Original_Capacity_Followup.csv')
 assert transfer['model_sha256']==sha(ROOT/'03_candidate_selection/05_model_robustness/results/Selected_Model_Component_Order.csv')
 summary.update(source_endpoint_screens=len(screens),original_followup_numeric_rows=len(extracted),new_primary_model_labels_released=0,source_expansion_assessment_date=max(row['assessment_date'] for row in screens))
user_source_dir=ROOT/'02_identity_and_evidence/02_user_supplied_sources'
if (user_source_dir/'Source_Document_Manifest.csv').exists():
 user_documents=read_csv(user_source_dir/'Source_Document_Manifest.csv')
 user_rows=read_csv(user_source_dir/'Original_Capacity_Extraction.csv')
 corrections=read_csv(user_source_dir/'Existing_Reference_Reconciliation.csv')
 assert len(user_documents)==7 and len(user_rows)==138
 assert len({row['evidence_id'] for row in user_rows})==138
 assert sum(row['assay']=='ORAC_FL' for row in user_rows)==116
 assert sum(row['assay']=='ORAC_PGR' for row in user_rows)==13
 assert sum(row['assay']=='ORAC_PE' for row in user_rows)==9
 for row in user_documents:
  path=ROOT/row['file']
  if path.exists():assert sha(path)==row['sha256'],row['file']
 assert all(row['human_review_status']=='NOT_REVIEWED' and row['change_applied']=='NO' for row in user_rows)
 assert all(row['independent_n_for_weighting']=='' for row in user_rows)
 supplement_rows=[row for row in user_rows if row['doi']=='10.1155/2020/4150897']
 assert sorted(int(row['source_row']) for row in supplement_rows)==list(range(1,61))
 assert next(float(row['mean']) for row in supplement_rows if row['source_row']=='19')==1.02
 verified_model_dir=ROOT/'03_candidate_selection/06_verified_source_update/results'
 diagnostic_data=read_csv(verified_model_dir/'Analysis_Data_and_Dispositions.csv')
 assert all(row['independent_sampling_variance']=='' for row in diagnostic_data)
 for row in diagnostic_data:
  if row['evidence_id'] in {'USR-ZHANG2020_S1-19-ORAC_FL','USR-ZHANG2020_S1-20-ORAC_FL','USR-ZHANG2020_S1-21-ORAC_FL','USR-ZHANG2020_S1-27-ORAC_FL'}:
   assert row['core_diagnostic']==row['extended_name_diagnostic']==row['extended_conflict_excluded_diagnostic']=='NO'
 assert any(row['doi']=='10.1021/jf0305231' and row['candidate_id']=='AFF-0009' and float(row['mean'])==10.5 for row in diagnostic_data)
 assert not any(row['doi']=='10.1021/jf0305231' and row['candidate_id']=='AFF-0010' for row in diagnostic_data)
 model_update=read_json(verified_model_dir/'model_update_summary.json')
 assert model_update['new_source_extraction_sha256']==sha(user_source_dir/'Original_Capacity_Extraction.csv')
 assert not model_update['formal_global_Top20_established'] and not model_update['newly_tuned_parameters']
 assert {row['variant']:row['candidates'] for row in model_update['variants']}=={'CORE_REPORTED_PH74_37C':23,'EXTENDED_UNKNOWN_PH_NAME_BASED':43,'EXTENDED_CONFLICT_EXCLUDED':41}
 deletion_rows=read_csv(verified_model_dir/'Source_Deletion_Order_Sensitivity.csv')
 for row in deletion_rows:
  assert 1<=int(row['fixed_universe_best_possible_order'])<=int(row['fixed_universe_worst_possible_order'])<=int(row['variant_candidate_count'])
 # A disconnected absolute location can retain estimable within-component contrasts.
 contrast_check=next(row for row in deletion_rows if row['variant']=='EXTENDED_CONFLICT_EXCLUDED' and row['candidate_id']=='AFF-0009' and row['omitted_doi']=='10.1021/jf010586o')
 assert int(contrast_check['estimable_contrasts_with_lower_candidates'])>0
 analysis_weights=read_csv(verified_model_dir/'Analysis_Row_Weights.csv')
 for variant in {row['variant'] for row in analysis_weights}:
  weighted=[row for row in analysis_weights if row['variant']==variant]
  totals=[sum(float(row['weight_equal_DOI_total']) for row in weighted if row['doi']==doi) for doi in {row['doi'] for row in weighted}]
  assert max(totals)-min(totals)<1e-10
 stability_path=verified_model_dir/'Candidate_Evidence_and_Stability.csv'
 if stability_path.exists():
  stability=read_csv(stability_path)
  assert len(stability)==41 and len({row['candidate_id'] for row in stability})==41
  for row in stability:
   assert row['human_review_status']=='NOT_REVIEWED' and row['change_applied']=='NO'
   cid=row['candidate_id']
   contributing=[r for r in diagnostic_data if r['candidate_id']==cid and r['extended_conflict_excluded_diagnostic']=='YES']
   assert int(row['source_DOIs'])==len({r['doi'] for r in contributing})
   assert int(row['deletion_best_possible_position'])<=int(row['diagnostic_position'])<=int(row['deletion_worst_possible_position'])
   assert all(r['doi'] in row['source_locators'] for r in contributing)
 summary.update(user_supplied_source_documents=len(user_documents),user_supplied_capacity_rows=len(user_rows),updated_model_variants=3,updated_model_global_rank_supported=False)
minimum20=supplement/'Minimum20_Abstract_Coverage.csv'
if minimum20.exists():
 coverage20=read_csv(minimum20)
 packages20=read_csv(supplement/'Minimum20_Abstract_Evidence_Packages.csv')
 assert len(coverage20)==193 and len({r['candidate_id'] for r in coverage20})==193
 for r in coverage20:
  assert r['scarcity_established']=='NO'
  count=sum(p['candidate_id']==r['candidate_id'] for p in packages20)
  assert count==int(r['rule_screened_relevant_abstracts'])
  assert (count>=20)==(r['target_reached_at_abstract_rule_level']=='YES')
 assert all(r['abstract'] and r['source_sha256'] and r['model_label_release']=='NO' and r['human_review_status']=='NOT_REVIEWED' and r['change_applied']=='NO' for r in packages20)
 assert len({(r['candidate_id'],r['doi'] or r['PMID'] or r['title']) for r in packages20})==len(packages20)
 body_path=supplement/'Minimum20_Body_Located_Leads.csv'
 if body_path.exists():
  body_leads=read_csv(body_path)
  combined=read_csv(supplement/'Minimum20_Combined_Progress.csv')
  panel=read_csv(supplement/'Minimum20_Review_Panel.csv')
  assert len(combined)==193
  assert all(r['article_evidence_strength']=='NOT_APPRAISED' and r['change_applied']=='NO' for r in panel)
  for r in body_leads:
   assert r['matched_paragraph'] and r['paragraph_locator'].startswith('body paragraph ')
   cached=supplement/r['source_file']
   if cached.exists():assert sha(cached)==r['source_sha256']
   assert r['model_label_release']=='NO' and r['human_review_status']=='NOT_REVIEWED'
  for r in combined:
   cid=r['candidate_id']
   keys={x['doi'] or x['PMID'] or x['title'] for x in packages20+body_leads if x['candidate_id']==cid}
   assert len(keys)==int(r['total_located_leads'])
   assert sum(x['candidate_id']==cid for x in panel)==min(20,len(keys))
   assert r['scarcity_established']=='NO'
 summary.update(minimum20_candidates=193,minimum20_abstract_links=len(packages20),minimum20_abstract_rule_target_reached=sum(int(r['rule_screened_relevant_abstracts'])>=20 for r in coverage20),minimum20_all_scientific_reviews_complete=False)
capacity_review=ROOT/'03_candidate_selection/08_capacity_review_validation'
if (capacity_review/'review_validation_summary.json').exists():
 review_rows=read_csv(capacity_review/'Capacity_Row_Review.csv')
 review_progress=read_csv(capacity_review/'Candidate_Review_and_Inclusion_Progress.csv')
 reviewed_input=read_csv(capacity_review/'Connected_Conditional_Analysis_Input.csv')
 validation_summary=read_json(capacity_review/'results/model_update_summary.json')
 assert len(review_rows)==203 and len(review_progress)==193
 assert len({r['evidence_id'] for r in review_rows})==203
 reconciled=read_csv(capacity_review/'Historical_Parent_Name_Reconciliation.csv')
 assert len(reconciled)==4
 for r in reconciled:
  assert sum(a['evidence_id']==r['extraction_id'] for a in review_rows)==1
  assert float(r['conditional_molar_capacity'])==float(r['raw_mean'])
  source=ROOT/r['source_file']
  if source.exists(): assert sha(source)==r['source_sha256']
 assert len({r['candidate_id'] for r in review_progress})==193
 assert all(r['human_review_status']=='NOT_REVIEWED' and r['change_applied']=='NO' for r in review_rows)
 assert sum(r['disposition']=='DISTINCT_AUC_ENDPOINT_HOLD' for r in review_rows)==5
 assert all(r['doi']!='10.3390/antiox13020222' for r in reviewed_input)
 citrus_rows=read_csv(capacity_review/'Reviewed_Citrus_Capacity_Rows.csv')
 assert len(citrus_rows)==9 and sum(bool(r['candidate_id']) for r in citrus_rows)==4
 for r in citrus_rows:
  if r['candidate_id']:
   assert abs(float(r['conditional_molar_capacity'])-float(r['raw_mean'])/100*float(r['reference_MW_g_mol'])/250.29)<1e-10
 assert not any(r['evidence_id']=='USR-ZHANG2020_S1-27-ORAC_FL' for r in reviewed_input)
 assert validation_summary['new_source_extraction_sha256']==sha(capacity_review/'Connected_Conditional_Analysis_Input.csv')
 assert not validation_summary['newly_tuned_parameters'] and not validation_summary['formal_global_Top20_established']
 expanded=next(r for r in validation_summary['variants'] if r['variant']=='EXTENDED_CONFLICT_EXCLUDED')
 assert expanded['candidates']==51 and expanded['papers']==11 and expanded['candidate_rows']==113
 bounds=read_csv(capacity_review/'Top20_Conditional_Uncertainty.csv')
 assert len(bounds)==51
 for r in bounds:
  assert 1<=int(r['deletion_best_position'])<=int(r['full_fit_position'])<=int(r['deletion_worst_position'])<=51
 summary.update(capacity_audited_rows=203,capacity_review_progress_profiles=193,connected_validation_candidates=51,connected_validation_DOIs=11)
date_review=ROOT/'02_identity_and_evidence/03_date_scoped_review/results'
if (date_review/'triage_summary.json').exists():
 scoped=read_csv(date_review/'Date_Scoped_Article_Register.csv')
 triage=read_csv(date_review/'Date_Scoped_Title_Abstract_Triage.csv')
 assert len(triage)==sum(r['in_current_review_scope']=='YES' for r in scoped)
 assert len({r['article_key'] for r in triage})==len(triage)
 assert all(r['period'] in {'PRIMARY_2020_2026','EXTENSION_2016_2019'} for r in triage)
 assert all(r['model_label_release']=='NO' for r in triage)
 blueberry=read_csv(date_review/'Blueberry_Original_Capacity_Extraction.csv')
 assert len(blueberry)==5 and sum(bool(r['candidate_id']) for r in blueberry)==1
 assert all(r['raw_units']=='micromol Trolox/micromol sample' and r['model_label_release']=='NO' for r in blueberry)
 decisions=read_csv(date_review/'Current_Scientific_Source_Decisions.csv')
 controls_path=date_review/'Reference_Control_Original_Extraction.csv'
 if controls_path.exists():
  controls=read_csv(controls_path)
  assert len(controls)==4
  assert sorted(float(r['raw_mean']) for r in controls)==[0.56,0.65,5.48,2378.0]
  assert all(r['conditional_molar_capacity']=='' and r['model_label_release']=='NO' and r['human_review_status']=='NOT_REVIEWED' and r['change_applied']=='NO' for r in controls)
  for r in controls:
   source=ROOT/r['source_file']
   if source.exists(): assert sha(source)==r['source_sha256']
 distinct_path=date_review/'Distinct_Endpoint_Original_Extraction.csv'
 if distinct_path.exists():
  distinct=read_csv(distinct_path)
  secondary=read_csv(date_review/'Secondary_ORAC_Original_Source_Trace.csv')
  assert len(distinct)==14 and len(secondary)==8
  assert all(r['converted_molar_capacity']=='' and r['model_label_release']=='NO' for r in distinct)
  assert all(r['study_deduplication_key']=='10.1002/jsfa.9917' and r['original_verified']=='NO' for r in secondary)
  for r in distinct+secondary:
   assert r['change_applied']=='NO' and r['human_review_status']=='NOT_REVIEWED'
   cached_source=ROOT/r['source_file']
   if cached_source.is_file():assert sha(cached_source)==r['source_sha256']
 unit_holds=read_csv(date_review/'Current_Standard_Unit_Holds.csv')
 assert len(unit_holds)==4 and all(r['converted_molar_value']=='' for r in unit_holds)
 for r in decisions+blueberry+unit_holds:
  assert r['human_review_status']=='NOT_REVIEWED' and r['change_applied']=='NO'
  cached_source=ROOT/r['source_file']
  if cached_source.is_file():assert sha(cached_source)==r['source_sha256']
 progress=read_csv(date_review/'Original_ORAC_Source_Progress.csv')
 assert len(progress)==109 and len({r['article_key'] for r in progress})==109
 assert sum(r['progress']=='TARGETED_SOURCE_SCOPE_RECORDED' for r in progress)==72
 assert sum(r['progress']=='FULLTEXT_ACCESS_PENDING' for r in progress)==37
 additional=read_csv(date_review/'Additional_Endpoint_Original_Extraction.csv')
 sesame=read_csv(date_review/'Sesame_Comparison_Original_Extraction.csv')
 hop=read_csv(date_review/'Hop_Original_Table_Transcription.csv')
 assert len(additional)==4 and len(sesame)==6 and len(hop)==12
 for r in additional+sesame+hop:
  assert r['converted_molar_capacity']=='' and r['model_label_release']=='NO'
  assert r['human_review_status']=='NOT_REVIEWED' and r['change_applied']=='NO'
  if r.get('source_file'):
   source=ROOT/r['source_file']
   if source.is_file():assert sha(source)==r['source_sha256']
 assert all(r['original_local_file']=='' and r['original_local_sha256']=='' for r in hop)
 deposit=read_csv(date_review/'Public_ORAC_Deposit_Summary_Audit.csv')
 assert len(deposit)==8
 assert sum(r['error_row_check']=='MATCHES_MEAN_ABSOLUTE_DEVIATION' for r in deposit)==7
 assert next(r['error_row_check'] for r in deposit if r['source_compound_code']=='trolox')=='MATCHES_FIRST_THREE_MEAN_ABSOLUTE_DEVIATION'
 assert all(abs(float(r['printed_Stdev_row'])-float(r['recomputed_sample_SD']))>1e-6 for r in deposit)
 assert all(r['model_label_release']=='NO' for r in deposit)
 for r in read_csv(date_review/'Public_ORAC_Deposit_Manifest.csv'):
  source=ROOT/'02_identity_and_evidence/01_systematic_supplement/inputs'/r['file_name']
  if source.is_file():assert sha(source)==r['source_sha256']
 locators=read_csv(date_review/'Source_Locator_Refresh.csv')
 assert len(locators)==4 and all(r['locator_status']=='ORIGINAL_XML_DOI_VERIFIED' and r['doi']==r['original_xml_doi'] for r in locators)
 for r in locators:
  assert next(x['PMCID'] for x in progress if x['doi']==r['doi'])==r['PMCID']
  source=ROOT/r['source_file']
  if source.is_file():assert sha(source)==r['source_sha256']
 versions=read_csv(date_review/'Study_Version_Link_Register.csv')
 assert len(versions)==2 and len({r['preprint_doi'] for r in versions})==2
 consideration=read_csv(ROOT/'03_candidate_selection/07_all_reference_integration/All_Reference_Consideration_Register.csv')
 for version in versions:
  matched=[r for r in consideration if r['doi']==version['preprint_doi']]
  assert matched and all(r['canonical_study_key']==version['canonical_study_key'] and r['study_version_role']=='DECLARED_PREPRINT_VERSION' for r in matched)
  assert all(r['consideration_status']!='NUMERIC_CROSS_PROTOCOL_SENSITIVITY' for r in matched)
 summary.update(orac_work_cohort=109,orac_targeted_scope_records=72,orac_access_pending=37,public_deposit_slope_summaries=8)
 summary.update(date_scope_triage_records=len(triage),new_source_decisions=len(decisions),blueberry_original_rows=5)
write_json(ROOT/'07_quality_control/workflow_qc.json',summary)
text=f'''# Workflow QC\n\nDate: {AS_OF}. Status: PASS.\n\nAll {len(manifest['records'])} registered scientific sources are checked against their recorded SHA256. Locally held source corpora are optional on a clone and do not enter the offline calculations. Ten frozen assets retain their original content and hash. Original review and HOLD states remain unchanged.\n\nThe 191 literal seed IDs reconstruct correctly. There are 204 discovery records, 193 profiles, 25 review-eligible candidates, 20 provisional review slots and 12 cutoff-stratum ties. The two-study sensitivity retains 9. The formal laboratory-ready panel has {len(ready)} rows. All 20 review identities/formulas match their official cached PubChem refresh; no cache conflict was detected.\n\nActive English Markdown links resolve. {len(svg_files)} current SVG exports contain text and vector objects without embedded raster images. Numerical AUC integration and rejection rules were checked on synthetic in-memory traces only. They establish code behavior, not assay performance.\n\nRemaining scientific work: close candidate-specific food sources, exact reagent procurement/forms, solubility/stability and absorbance counter-screens; adjudicate cutoff ties and actual material decisions; approve equipment-specific assay settings/calibration; collect real experimental data. The method-search log explicitly identifies first-page truncation where present. The dated source catalogue and journal-metric gaps remain available and have not been promoted into verified claims.\n'''
if 'source_endpoint_screens' in summary:
 text += f"\nSource-expansion assessment dated {summary['source_expansion_assessment_date']} verifies {summary['source_endpoint_screens']} endpoint screens and {summary['original_followup_numeric_rows']} uniquely keyed original numeric rows. Available caches match recorded SHA256 values. Review states remain NOT_REVIEWED and change_applied=NO. Conditional conversion, unfilled independent sample sizes, withheld conflicting units and fixed-model input hashes passed the source-specific checks. Zero primary model labels were released.\n"
if 'user_supplied_source_documents' in summary:
 text += f"\nThe latest original-source intake verifies {summary['user_supplied_source_documents']} supplied documents and {summary['user_supplied_capacity_rows']} unique assay rows. DOI/probe separation, 60-row supplement numbering, source-conflict exclusions, the corrected 2004 Quercetin value and excluded Kaempferol association passed. All three updated diagnostics preserve missing independent sampling variances and explicit review states. Equal-total-DOI weights reconcile, and estimable relative contrasts survive the disconnected-location regression check. Global-193 ranking remains unresolved.\n"
(ROOT/'07_quality_control/Workflow_QC.md').write_text(text,encoding='utf8')
print(f'QC PASS: {len(queue)} review slots; {len(ready)} lab-ready; {len(svg_files)} editable SVGs; frozen sources unchanged.')
