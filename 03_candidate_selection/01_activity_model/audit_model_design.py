"""Check source/compound overlap and prioritize evidence recovery, not compound potency."""
from pathlib import Path
import sys,collections,itertools
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'00_project'))
from pipeline_io import *
HERE=Path(__file__).resolve().parent
rows=read_csv(HERE/'results/Model_Input_Candidates.csv')
graph=collections.defaultdict(set)
for r in rows:
 c='compound:'+r['candidate_id'];s='paper:'+r['doi'].lower().strip()
 graph[c].add(s);graph[s].add(c)
components={};index=0
for node in sorted(graph):
 if node in components:continue
 index+=1;stack=[node]
 while stack:
  n=stack.pop()
  if n in components:continue
  components[n]=index;stack.extend(graph[n]-components.keys())
compounds=[n for n in graph if n.startswith('compound:')];papers=[n for n in graph if n.startswith('paper:')]
details=[{'candidate_id':n.split(':',1)[1],'paper_count_not_automatic_independence':len(graph[n]),'overlap_component':components[n],'design_interpretation':'No repeated source-adjusted compound comparison across components'} for n in compounds]
write_csv(HERE/'results/Model_Overlap_Design.csv',details)
rank=len(compounds)+len(papers)-index
parameter_count=len(compounds)+len(papers)-1
baseline=read_csv(HERE/'results/Observation_Readiness.csv');groups=collections.defaultdict(list)
for r in baseline:groups[r['doi']].append(r)
priority=[]
for doi,observations in groups.items():
 matched={r['candidate_id'] for r in observations if 'compound:'+r['candidate_id'] in components}
 if not matched:continue
 component_ids={components['compound:'+c] for c in matched}
 bridge_pairs=len(list(itertools.combinations(component_ids,2)))
 known=[r for r in rows if r['doi']==doi]
 resolved=bool(known) and all(r['error_type'].startswith('SD_EXPLICIT') for r in known)
 priority.append({'doi':doi,'existing_observation_rows':len(observations),'model_compounds_already_represented_in_source':len(matched),'candidate_ids':'; '.join(sorted(matched)),'distinct_current_components_represented':len(component_ids),'potential_component_pairs_for_recovery':bridge_pairs,'error_extraction_already_resolved':'YES' if resolved else 'NO','current_source_review_states':'; '.join(sorted({r['source_independence_status'] for r in observations})),'action':'NO_REPEAT_DOWNLOAD_NEEDED; retain covariance and target-method review' if resolved else 'RECOVER_OR_CLARIFY_ORIGINAL_ERROR_SCALE_AND_REPLICATION; assess method compatibility','interpretation':'Retrieval opportunity from known rows, not verified model eligibility, potency or study independence'})
priority.sort(key=lambda r:(r['error_extraction_already_resolved']=='YES',-r['potential_component_pairs_for_recovery'],-r['model_compounds_already_represented_in_source'],r['doi']))
write_csv(HERE/'results/Targeted_Recovery_Priority.csv',priority)
summary={'status':'DESIGN_CHECK_ONLY_NO_MODEL_FITTED','input_rows':len(rows),'distinct_compounds':len(compounds),'distinct_papers':len(papers),'connected_components':index,'compounds_with_multiple_papers':sum(len(graph[n])>1 for n in compounds),'additive_fixed_effect_design_rank':rank,'additive_fixed_effect_parameters_with_one_reference_constraint':parameter_count,'unidentified_dimensions':parameter_count-rank,'interpretation':'An additive compound-plus-paper adjustment is not identified across disconnected components without further constraints or modelling assumptions. Hierarchical borrowing would require explicit assumptions and validation; raw capacity values are not declared unusable.','ranked_recovery_sources':len(priority),'capacity_ranking_generated':False}
assert rank<=parameter_count and len(details)==len(compounds)
write_json(HERE/'results/model_design_summary.json',summary)
print(f'Model design: {len(rows)} rows, {len(papers)} papers, {index} overlap components; retrieval priorities generated, no capacity rank.')
