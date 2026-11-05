from pathlib import Path
import csv,json,hashlib,subprocess,datetime,re,ast
ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'workspaces/phase1c_mechanism_evidence_pilot'
def load(p):
 with p.open(encoding='utf-8-sig',newline='') as f:
  r=csv.DictReader(f,strict=True);fields=r.fieldnames;rows=list(r)
 assert fields and len(fields)==len(set(fields)) and all(fields)
 assert all(None not in x and all(v is not None for v in x.values()) for x in rows)
 assert all('\ufffd' not in v for x in rows for v in x.values())
 return fields,rows
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def git(*args):return subprocess.check_output(['git','--no-optional-locks',*args],cwd=ROOT).decode('utf-8').strip()
checks={};csvcounts={}
for p in OUT.rglob('*.csv'):
 fields,rows=load(p);csvcounts[p.relative_to(OUT).as_posix()]={'rows':len(rows),'columns':len(fields),'sha256':sha(p)}
checks['all_csv_strict_utf8_and_rectangular']=True
master=OUT/'master/Compound_Mechanism_Evidence_Master.csv';compound=OUT/'compounds/AFF-0061_Protocatechuic_Acid_Mechanism_Evidence.csv'
fields,rows=load(master);_,dictionary=load(OUT/'dictionaries/Mechanism_Evidence_Field_Dictionary.csv');_,coverage=load(OUT/'indexes/Compound_Mechanism_Coverage.csv');_,registry=load(OUT/'master/Study_Register.csv')
checks['master_compound_byte_identical']=master.read_bytes()==compound.read_bytes()
checks['21_observations_10_publications']=len(rows)==21 and len({x['study_id'] for x in rows})==10
checks['all_66_fields_bilingual_dictionary']=len(fields)==66 and set(fields)=={x['field_name'] for x in dictionary} and all(x['definition_cn'] and x['definition_en'] and x['allowed_values_or_rule'] and x['missing_value_rule_cn'] and x['filling_instruction_cn'] for x in dictionary)
checks['unique_evidence_ids']=len({x['evidence_id'] for x in rows})==21
checks['190_unsearched_no_false_zero']=len(coverage)==191 and sum(x['search_status']=='NOT_SEARCHED' for x in coverage)==190 and all(x['evidence_record_count']=='' and x['included_unique_publication_count']=='' for x in coverage if x['search_status']=='NOT_SEARCHED')
checks['all_abstracts_no_fake_panels']=all(x['source_figure_or_table']=='UNRESOLVED_ABSTRACT_ONLY' for x in rows if x['source_verification_status']=='ABSTRACT_ONLY')
checks['no_fabricated_direct_validation']=all(x['direct_target_status']!='VERIFIED_DIRECT_BINDING' for x in rows)
checks['retracted_absent_from_evidence']=not {x['PMID'] for x in rows}&{'26180584','41947015'}
checks['no_derivative_or_generated_form_silently_included']=not {x['PMID'] for x in rows}&{'29129792','14705020'}
checks['single_dose_value']=all(x['dose'] in ['UNRESOLVED','NOT_APPLICABLE','NOT_REPORTED'] or bool(re.fullmatch(r'\d+(\.\d+)?',x['dose'])) for x in rows)
checks['mda_panel_conflict_not_guessed']=next(x for x in rows if x['evidence_id']=='ME-AFF0061-39589556-001')['source_figure_or_table']=='Figure 6L'
checks['no_unparsed_multi_dose_KEAP1_row']=not any(x['target_gene']=='KEAP1' for x in rows)
checks['source_local_paths_exist']=all((OUT/x['source_local_path']).is_file() for x in rows)
checks['publication_registry_counts']=sum(x['screening_decision']=='INCLUDE_PILOT_PROVISIONAL' for x in registry)==10 and sum(int(x['evidence_record_count']) for x in registry)==21
for p in (OUT/'qc').glob('*.py'):ast.parse(p.read_text(encoding='utf-8'))
checks['support_scripts_syntax']=True
baseline=json.loads((OUT/'qc/Start_Baseline.json').read_text(encoding='utf-8'));changed=[p for p,h in baseline['tracked_file_sha256'].items() if not (ROOT/p).is_file() or sha(ROOT/p)!=h]
checks['639_protected_tracked_hashes_unchanged']=len(baseline['tracked_file_sha256'])==639 and not changed
checks['HEAD_unchanged']=git('rev-parse','HEAD')==baseline['HEAD']
status=git('status','--porcelain=v1','--untracked-files=all')
checks['all_changes_in_authorized_pilot_directory']=all('workspaces/phase1c_mechanism_evidence_pilot/' in line.replace('\\','/') for line in status.splitlines())
checks['no_human_approval']=all(x['human_review_status']=='NOT_REVIEWED' for x in rows)
assert all(checks.values()),checks
result={'verified_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checks':checks,'programmatic_pass_count':len(checks),'failed_checks':[],'csv_counts':csvcounts,'final_HEAD':git('rev-parse','HEAD'),'final_branch':git('branch','--show-current'),'non_pilot_tracked_changes':changed,'git_status_before_this_validation_output':status,'scientific_review':'NOT_REVIEWED; open items in Source_Review_Open_Items.md','Gate1':'HOLD','Gate2':'HUMAN_SCIENTIFIC_REVIEW_REQUIRED','release':'HOLD','commit_push':'NOT_EXECUTED'}
with (OUT/'qc/Final_Validation.json').open('x',encoding='utf-8') as f:json.dump(result,f,ensure_ascii=False,indent=2)
print(json.dumps({'checks_passed':len(checks),'csv_counts':csvcounts,'HEAD':result['final_HEAD'],'original_tracked_files_changed':changed},ensure_ascii=False,indent=2))
