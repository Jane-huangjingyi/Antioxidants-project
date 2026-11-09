"""Audit source coverage and bipartite design connectivity; never fit audit-only labels."""
import csv, json
from pathlib import Path
P = Path(__file__).resolve().parent

def read(name):
    with (P/'results'/name).open(encoding='utf-8-sig') as f:
        return list(csv.DictReader(f))

def write(name, rows):
    with (P/'results'/name).open('w', encoding='utf-8-sig', newline='') as f:
        w=csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

queue=read('External_Source_Validation_Queue.csv')
access=json.loads((P/'inputs/external_batch_access.json').read_text(encoding='utf-8'))
papers=[]
for doi in sorted({r['doi'] for r in queue}):
    rs=[r for r in queue if r['doi']==doi]
    a=access[doi]
    papers.append(dict(doi=doi, queued_observations=len(rs), compounds=len({r['candidate_id'] for r in rs}),
        original_values_rechecked=sum(bool(r['original_value_verified']) for r in rs),
        access_status=a['status'], checked_url=a['url'], access_scope=a['scope'],
        data_generating_study_independence='NOT_CLOSED_DIFFERENT_DOI_IS_INSUFFICIENT',
        next_requirement=a['next_requirement'],human_review_status='NOT_REVIEWED',change_applied='NO'))
unresolved=sorted([r for r in papers if r['queued_observations']>r['original_values_rechecked']],
                  key=lambda r:(-(r['queued_observations']-r['original_values_rechecked']),r['doi']))
priority={r['doi']:i for i,r in enumerate(unresolved,1)}
for r in papers:
    r['unverified_numeric_rows']=r['queued_observations']-r['original_values_rechecked']
    r['original_table_recovery_priority']=priority.get(r['doi'],'')
    r['priority_interpretation']='RETRIEVAL_WORK_ORDER_BY_UNVERIFIED_QUEUE_COVERAGE_NOT_ACTIVITY_SCORE'
write('External_Paper_Readiness.csv',papers)

def graph(rows, scope):
    # Binary design X = [compound indicators, paper indicators]. For a bipartite
    # incidence design its rank is vertices minus connected components.
    edges={(r['candidate_id'],r['doi']) for r in rows}
    adj={}
    for compound,paper in edges:
        c='C:'+compound; d='P:'+paper
        adj.setdefault(c,set()).add(d);adj.setdefault(d,set()).add(c)
    seen=set(); components=[]
    for node in sorted(adj):
        if node in seen:continue
        stack=[node];part=set()
        while stack:
            x=stack.pop()
            if x in part:continue
            part.add(x);stack.extend(adj[x]-part)
        seen.update(part);components.append(part)
    rank=len(adj)-len(components)
    return dict(scope=scope,observations=len(rows),unique_compound_paper_edges=len(edges),
        compounds=len({c for c,p in edges}),papers=len({p for c,p in edges}),components=len(components),
        additive_design_rank=rank,edge_cycle_degrees_of_freedom=len(edges)-rank,
        interpretation='TOPOLOGY_ONLY_NOT_ELIGIBILITY_OR_ESTIMATED_STUDY_EFFECT',
        cross_component_ranking_identifiable='NO' if len(components)!=1 else 'CONNECTED_ONLY_OTHER_GATES_REQUIRED')

verified=[r for r in queue if r['original_value_verified']]
decisions=read('External_Comparability_Decisions.csv')
molar={(r['doi'],r['candidate_id']) for r in decisions if r['unit_gate'] in {'EXPLICIT_MOLAR_TE','MOLAR_SLOPE_RATIO_TRACED'}}
verified_molar=[r for r in verified if (r['doi'],r['candidate_id']) in molar]
eligible=[r for r in queue if r['external_validation_label']]
graphs=[graph(queue,'LEGACY_PLUS_RECOVERED_QUEUE_AUDIT_ONLY'),graph(verified,'ORIGINAL_NUMERIC_VALUE_RECHECKED_NOT_COMMON_TARGET_ELIGIBLE'),
        graph(verified_molar,'MOLAR_ESTIMATOR_TRACED_OTHER_GATES_PENDING'),graph(eligible,'APPROVED_COMMON_TARGET_EXTERNAL_LABELS')]
crosswalk={r['source_row']:r for r in read('Flavonoid_Candidate_Crosswalk.csv')}
development=[dict(candidate_id=crosswalk[r['source_row']]['candidate_id'] or 'DEV_ONLY_ROW_'+r['source_row'],
                  doi=r['doi']) for r in read('Flavonoid_Log_Capacity_Extraction.csv')]
graphs.append(graph(development+verified_molar,'DEVELOPMENT_PLUS_TRACED_EXTERNAL_TOPOLOGY_NOT_HARMONIZED_LABELS'))
conditional_keys={(r['doi'],r['candidate_id']) for r in decisions if r['unit_gate']=='CONDITIONAL_PARENT_MW_CONVERSION'}
conditional_rows=[r for r in verified if (r['doi'],r['candidate_id']) in conditional_keys]
graphs.append(graph(development+verified_molar+conditional_rows,'SENSITIVITY_WITH_CONDITIONAL_CONVERSIONS_NOT_ELIGIBLE_FOR_FITTING'))
write('External_Connectivity_Readiness.csv',graphs)
keys=[(r['doi'],r['candidate_id'],r['legacy_observation_id']) for r in queue]
assert len(keys)==len(set(keys)), 'Duplicate source-observation keys'
assert all(r['human_review_status']=='NOT_REVIEWED' and r['change_applied']=='NO' for r in queue)
assert len(queue)==29 and len(papers)==10 and not eligible
summary=dict(papers=len(papers),queue_observations=len(queue),original_values_rechecked=len(verified),
    molar_estimator_traced_observations=len(verified_molar),approved_external_labels=len(eligible),
    duplicate_observation_keys=0,shared_data_independence_closed=False,graphs=graphs,
    development_anchor_included_in_last_two_graphs=True,conditional_conversion_observations=len(conditional_rows),
    topology_does_not_resolve_protocol_or_material_gates=True,
    decision='DO_NOT_FIT_CROSS_PAPER_RANKING_FROM_THIS_QUEUE',
    next_priority='Recover original multi-compound tables and linked data-generation provenance; preserve fixed endpoint and model settings')
(P/'results/external_validation_readiness.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
print(json.dumps(summary))
