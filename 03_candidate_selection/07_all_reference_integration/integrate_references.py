"""Consider every candidate-linked reference and fit recoverable capacity sensitivity."""
from pathlib import Path
import collections
import csv
import json
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
SOURCE=ROOT/'02_identity_and_evidence/01_systematic_supplement'
PRIOR=ROOT/'03_candidate_selection/06_verified_source_update'
sys.path.insert(0,str(PRIOR))
from fit_verified_source_diagnostics import fit, np


def read(path):
    with path.open(encoding='utf-8-sig',newline='') as handle:
        return list(csv.DictReader(handle))


def write(name,rows):
    with (HERE/name).open('w',encoding='utf8',newline='') as handle:
        writer=csv.DictWriter(handle,fieldnames=list(rows[0]),lineterminator='\n')
        writer.writeheader();writer.writerows(rows)


def main():
    base=[r for r in read(PRIOR/'results/Analysis_Data_and_Dispositions.csv')
          if r['extended_conflict_excluded_diagnostic']=='YES']
    additional=read(SOURCE/'Original_Capacity_Followup.csv')
    bridge=ROOT/'03_candidate_selection/08_capacity_review_validation/Reviewed_Bridge_Capacity_Rows.csv'
    if bridge.exists():additional+=read(bridge)
    citrus=ROOT/'03_candidate_selection/08_capacity_review_validation/Reviewed_Citrus_Capacity_Rows.csv'
    if citrus.exists():additional+=read(citrus)
    reconciliation=ROOT/'03_candidate_selection/08_capacity_review_validation/Historical_Parent_Name_Reconciliation.csv'
    if reconciliation.exists():additional+=read(reconciliation)
    rows=list(base)
    for r in additional:
        if not r['candidate_id'] or not r['conditional_molar_capacity']:
            continue
        rows.append(dict(candidate_id=r['candidate_id'],doi=r['doi'],
                         mean=r['conditional_molar_capacity'],
                         source_block=r['doi']+'|'+r.get('protocol_stratum','ADDITIONAL_CROSS_PROTOCOL'),
                         evidence_id=r['extraction_id'],numeric_locator=r['source_locator'],
                         source_document=r['source_file'],source_sha256=r['source_sha256']))
    assert len({(r['candidate_id'],r['doi'],r['source_block']) for r in rows})==len(rows)
    # Discover disconnected evidence components before attempting global ordering.
    graph=collections.defaultdict(set)
    for r in rows:
        a='C:'+r['candidate_id'];b='S:'+r['source_block']
        graph[a].add(b);graph[b].add(a)
    unseen=set(graph);components=[]
    while unseen:
        start=min(unseen);todo=[start];members=set()
        while todo:
            node=todo.pop()
            if node in members:continue
            members.add(node);todo.extend(graph[node]-members)
        unseen-=members;components.append(members)
    components.sort(key=lambda members:(-len(members),sorted(members)))
    fitted=[];component_summary=[]
    profiles={r['candidate_id']:r['compound_name'] for r in read(ROOT/'02_identity_and_evidence/results/candidate_evidence_profiles.csv')}
    for number,members in enumerate(components,1):
        candidates=sorted(n[2:] for n in members if n.startswith('C:'))
        data=[r for r in rows if r['candidate_id'] in candidates]
        for weighting in ['EQUAL_ROW','EQUAL_DOI_TOTAL']:
            beta,matrix=fit(data,candidates,'SHRINK_10',weighting)
            order=sorted(range(len(candidates)),key=lambda i:-beta[i])
            for position,index in enumerate(order,1):
                cid=candidates[index]
                sources=sorted({r['doi'] for r in data if r['candidate_id']==cid})
                fitted.append(dict(component=number,weighting=weighting,candidate_id=cid,
                                   compound=profiles[cid],within_component_position=position,
                                   conditional_log_location=float(beta[index]),
                                   conditional_geometric_location=float(np.exp(beta[index])),
                                   source_DOIs=len(sources),doi_list=';'.join(sources),
                                   interpretation='CROSS_PROTOCOL_CONDITIONAL_SENSITIVITY',
                                   global_rank='',human_review_status='NOT_REVIEWED',change_applied='NO'))
        component_summary.append(dict(component=number,candidates=len(candidates),rows=len(data),
                                      source_DOIs=len({r['doi'] for r in data})))
    write('Expanded_Conditional_Component_Orders.csv',fitted)
    # All master reference links enter one traceable consideration register.
    articles={r['article_key']:r for r in read(SOURCE/'Master_Article_Register.csv')}
    used={(r['candidate_id'],r['doi']) for r in rows}
    known_numeric={(r['candidate_id'],r['doi']):r for r in additional if r['candidate_id']}
    dispositions=[]
    for link in read(SOURCE/'Master_Candidate_Article_Links.csv'):
        article=articles[link['article_key']]
        pair=(link['candidate_id'],article['doi'])
        role='RELEVANCE_AND_ENDPOINT_EXTRACTION_PENDING'
        reason='Candidate-linked retrieval record requires article-level scientific assessment.'
        if pair in used:
            role='NUMERIC_CROSS_PROTOCOL_SENSITIVITY'
            reason='Original numeric row is included conditionally with a separate source/protocol block.'
        elif pair in known_numeric:
            role='NUMERIC_SOURCE_CONFLICT_PENDING'
            reason=known_numeric[pair]['unresolved_fields']
        dispositions.append(dict(candidate_id=link['candidate_id'],article_key=link['article_key'],
                                 doi=article['doi'],title=article['title'],publication_types=article['publication_types'],
                                 consideration_status=role,reason=reason,
                                 article_quality='NOT_APPRAISED',numeric_potency_weight='',
                                 human_review_status='NOT_REVIEWED',change_applied='NO'))
    represented={(r['candidate_id'],r['doi']) for r in dispositions}
    article_by_doi={r['doi']:r for r in articles.values() if r['doi']}
    for cid,doi in sorted(used-represented):
        article=article_by_doi.get(doi,{})
        dispositions.append(dict(candidate_id=cid,article_key=article.get('article_key','DOI:'+doi),
                                 doi=doi,title=article.get('title','ORIGINAL_SOURCE_TABLE_EXTRACTION'),
                                 publication_types=article.get('publication_types',''),
                                 consideration_status='NUMERIC_CROSS_PROTOCOL_SENSITIVITY',
                                 reason='Verified extraction adds this candidate/source association to the master-link scope.',
                                 article_quality='NOT_APPRAISED',numeric_potency_weight='',
                                 human_review_status='NOT_REVIEWED',change_applied='NO'))
    version_path=ROOT/'02_identity_and_evidence/03_date_scoped_review/results/Study_Version_Link_Register.csv'
    versions={r['preprint_doi']:r for r in read(version_path)} if version_path.exists() else {}
    for record in dispositions:
        version=versions.get(record['doi'])
        record['canonical_study_key']=version['canonical_study_key'] if version else record['article_key']
        record['study_version_role']='DECLARED_PREPRINT_VERSION' if version else 'ARTICLE_KEY_PENDING_COMPLETE_INDEPENDENCE_REVIEW'
        record['version_relation_source']=version['source_url'] if version else ''
    write('All_Reference_Consideration_Register.csv',dispositions)
    coverage=[]
    for cid,name in profiles.items():
        linked=[r for r in dispositions if r['candidate_id']==cid]
        observations=[r for r in rows if r['candidate_id']==cid]
        coverage.append(dict(candidate_id=cid,compound=name,all_reference_links_considered=len(linked),
                             numeric_rows=len(observations),numeric_source_DOIs=len({r['doi'] for r in observations}),
                             unprocessed_article_links=sum(r['consideration_status']=='RELEVANCE_AND_ENDPOINT_EXTRACTION_PENDING' for r in linked),
                             global_rank='',human_review_status='NOT_REVIEWED',change_applied='NO'))
    write('All_Candidate_Integration_Coverage.csv',coverage)
    summary=dict(all_reference_links=len(dispositions),unique_linked_articles=len({r['article_key'] for r in dispositions}),
                 candidates_considered=len(coverage),numeric_candidates=len({r['candidate_id'] for r in rows}),
                 numeric_source_DOIs=len({r['doi'] for r in rows}),numeric_rows=len(rows),
                 components=component_summary,additional_numeric_rows=len(rows)-len(base),
                 confirmed_version_pairs=len(versions),provisional_version_group_keys=len({r['canonical_study_key'] for r in dispositions}),
                 all_articles_scientifically_reviewed=False,formal_global_rank_supported=False)
    (HERE/'integration_summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf8')
    print(json.dumps(summary))


if __name__=='__main__':
    main()
