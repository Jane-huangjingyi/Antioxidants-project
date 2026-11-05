"""Rebuild discovery from the original class-based enumeration, not a finished candidate table."""
from pathlib import Path
import ast,sys
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'00_project'))
from pipeline_io import *
script='discovery/2026-09-18_build_phase2_universe.py'
tree=ast.parse(source(script).read_text(encoding='utf-8-sig'))
# Execute only the literal curation declarations; never legacy imports, I/O, HTTP or ranking code.
nodes=[]
for node in tree.body:
 if isinstance(node,ast.FunctionDef) and node.name=='add':nodes.append(node)
 elif isinstance(node,ast.Assign) and all(isinstance(t,ast.Name) for t in node.targets) and node.targets[0].id in {'spec','P','V','C','S','N','O','M','exclusions'}:nodes.append(node)
 elif isinstance(node,ast.Expr) and isinstance(node.value,ast.Call) and isinstance(node.value.func,ast.Name) and node.value.func.id=='add':nodes.append(node)
env={'__builtins__':{'dict':dict}};exec(compile(ast.Module(body=nodes,type_ignores=[]),script,'exec'),env)
assert len(env['spec'])==191 and len(env['exclusions'])==12
discovery=[]
for i,s in enumerate(env['spec'],1):
 discovery.append({'discovery_id':f'DISC-{i:04d}','candidate_id':f'AFF-{i:04d}','name':s['compound'],'parent_class':s['parent_class'],'analysis_panel':s['analysis_panel'].replace('\u2013',' - '),'subclass':s['subclass'],'reported_food_examples':s['representative_food_sources'],'origin':'LEGACY_CLASS_BASED_EXPERT_ENUMERATION','source_path':locator(script),'source_sha256':sha(source(script)),'legacy_exclusion_reason':'','dietary_occurrence_status':'CLASS_LEVEL_CURATION_ONLY','candidate_specific_food_source':'','review_status':'NOT_REVIEWED'})
for i,e in enumerate(env['exclusions'],192):
 discovery.append({'discovery_id':f'DISC-{i:04d}','candidate_id':'NEW-GSH' if e[0]=='Glutathione' else '', 'name':e[0],'parent_class':e[1],'analysis_panel':e[1],'subclass':'NOT_ASSIGNED','reported_food_examples':'','origin':'LEGACY_EXCLUSION_LOG_RESCREENED','source_path':locator(script),'source_sha256':sha(source(script)),'legacy_exclusion_reason':e[2],'dietary_occurrence_status':'REQUIRES_SCOPE_REVIEW','candidate_specific_food_source':'','review_status':'NOT_REVIEWED'})
# A documented blind spot of the legacy class enumeration, not an automatic assay nomination.
discovery.append({'discovery_id':'DISC-0204','candidate_id':'NEW-EGT','name':'L-Ergothioneine','parent_class':'Food-derived sulfur compounds','analysis_panel':'Defined dietary thiols','subclass':'Ergothioneine','reported_food_examples':'Edible mushrooms; beans; oat bran (primary abstract)','origin':'TARGETED_SCOPE_GAP_PRIMARY_LITERATURE','source_path':'https://doi.org/10.1021/jf071328f','source_sha256':'','legacy_exclusion_reason':'','dietary_occurrence_status':'PRIMARY_ABSTRACT_SUPPORTS_FOOD_OCCURRENCE','candidate_specific_food_source':'10.1021/jf071328f; abstract; LC-MS/MS analysis of common foods','review_status':'NOT_REVIEWED'})
for r in discovery:
 if r['name']=='Glutathione':
  r.update(dietary_occurrence_status='PRIMARY_ABSTRACT_SUPPORTS_FOOD_OCCURRENCE',candidate_specific_food_source='10.1080/01635589209514173; PMID1574445; abstract; HPLC analysis of prepared foods',reported_food_examples='Fruits, vegetables and freshly prepared meats (primary abstract)')
  r['origin']='LEGACY_EXCLUSION_REOPENED_UNDER_USER_FOOD_SCOPE'
 # Preserve the evidence gap rather than treating an inherited label as independently verified.
 if not r['candidate_id']:r['scope_disposition']='EXCLUDE_OR_HOLD_WITH_LEGACY_REASON'
 elif r['parent_class']=='Antioxidant-related micronutrients / mineral cofactors':r['scope_disposition']='HOLD_UNSPECIFIED_ELEMENT_FORM'
 else:r['scope_disposition']='RETAIN_FOR_IDENTITY_AND_FOOD_VERIFICATION'
write_csv(ROOT/'01_candidate_discovery/results/discovery_register.csv',discovery)
write_json(ROOT/'01_candidate_discovery/results/discovery_summary.json',{'curated_seed_names':191,'rescreened_legacy_exclusions':12,'targeted_new_name':1,'discovery_rows':len(discovery),'food_scope_reopenings':['Glutathione'],'scope_gap_additions':['L-Ergothioneine'],'not_exhaustive':True,'legacy_enumeration_sha256':sha(source(script))})
print('01: 204 auditable discovery records; legacy exclusions preserved, food-scope gaps visible.')
