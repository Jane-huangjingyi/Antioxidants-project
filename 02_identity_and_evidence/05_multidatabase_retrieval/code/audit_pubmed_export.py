"""Verify PubMed export coverage and reconcile report identifiers with the baseline."""
from collections import Counter, defaultdict
import csv
import datetime as dt
import hashlib
import json
import xml.etree.ElementTree as ET
from retrieve_pubmed import CACHE, HERE, write
from audit_identifiers import title_key

def read(path):
    with path.open(encoding='utf-8-sig',newline='') as handle:
        return list(csv.DictReader(handle))

def date(node):
    if node is None:
        return ''
    return '-'.join(node.findtext(part,'') for part in ('Year','Month','Day')).strip('-') or node.findtext('MedlineDate','')

def main():
    baseline=read(HERE/'Deduplicated_Article_Register.csv')
    by_pmid,by_doi,by_pmcid=defaultdict(set),defaultdict(set),defaultdict(set)
    for r in baseline:
        if r['PMID']:by_pmid[r['PMID']].add(r['article_key'])
        if r['article_key'].startswith(('MED:','PMID:')):
            by_pmid[r['article_key'].split(':',1)[1]].add(r['article_key'])
        if r['doi']:by_doi[r['doi'].strip().lower()].add(r['article_key'])
        if r['PMCID']:by_pmcid[r['PMCID'].strip().upper()].add(r['article_key'])
    base_by_key={r['article_key']:r for r in baseline}
    base_titles=defaultdict(set)
    for row in baseline:
        normalized=title_key(row['title'])
        if len(normalized)>=24:
            base_titles[normalized].add(row['article_key'])
    expected={r['PMID']:r['routes'] for r in read(HERE/'PubMed_Route_PMIDs.csv')}
    targeted={r['PMID'] for r in read(HERE/'PubMed_Compound_Hit_Links.csv')} if (HERE/'PubMed_Compound_Hit_Links.csv').exists() else set()
    if (HERE/'PubMed_CID_Alias_Hit_Links.csv').exists():
        targeted.update(r['PMID'] for r in read(HERE/'PubMed_CID_Alias_Hit_Links.csv'))
    rows=[]
    for batch in read(HERE/'PubMed_Export_Manifest.csv'):
        raw=(CACHE/batch['raw_file']).read_bytes()
        assert hashlib.sha256(raw).hexdigest()==batch['sha256']
        for node in ET.fromstring(raw):
            pmid=node.findtext('MedlineCitation/PMID') or node.findtext('BookDocument/PMID')
            identifiers=node.findall('PubmedData/ArticleIdList/ArticleId')+node.findall('PubmedBookData/ArticleIdList/ArticleId')
            dois={x.text.strip().lower() for x in identifiers if x.get('IdType')=='doi' and x.text}
            doi=next(iter(dois)) if len(dois)==1 else ''
            pmcids={x.text.strip().upper() for x in identifiers if x.get('IdType')=='pmc' and x.text}
            pmcid=next(iter(pmcids)) if len(pmcids)==1 else ''
            matches=by_pmid[pmid] | by_doi.get(doi, set()) | by_pmcid.get(pmcid, set())
            conflicting_doi=any(doi and base_by_key[key]['doi'] and base_by_key[key]['doi'].strip().lower()!=doi for key in matches)
            conflicting_pmid=any(base_by_key[key]['PMID'] and base_by_key[key]['PMID']!=pmid for key in matches)
            conflicting_pmcid=any(pmcid and base_by_key[key]['PMCID'] and base_by_key[key]['PMCID'].strip().upper()!=pmcid for key in matches)
            if len(dois)>1 or len(pmcids)>1 or len(matches)>1 or conflicting_doi or conflicting_pmid or conflicting_pmcid:
                status='IDENTIFIER_CONFLICT_PENDING'
            elif matches:
                status='BASELINE_IDENTIFIER_MATCH'
            else:
                status='PUBMED_ADDITIONAL_REPORT_KEY'
            publication=date(node.find("MedlineCitation/Article/ArticleDate[@DateType='Electronic']"))
            electronic_history=date(node.find("PubmedData/History/PubMedPubDate[@PubStatus='epublish']"))
            issue=date(node.find('MedlineCitation/Article/Journal/JournalIssue/PubDate'))
            title_node=node.find('MedlineCitation/Article/ArticleTitle')
            title=''.join(title_node.itertext()) if title_node is not None else ''
            rows.append(dict(PMID=pmid,doi=doi,PMCID=pmcid,title=title,abstract_present='YES' if node.findall('MedlineCitation/Article/Abstract/AbstractText') else 'NO',query_routes=expected[pmid],targeted_query_match='YES' if pmid in targeted else 'NO',
                             electronic_article_date=publication,electronic_history_date=electronic_history,formal_issue_date=issue,
                             entrez_history_date=date(node.find("PubmedData/History/PubMedPubDate[@PubStatus='entrez']")),
                             pubmed_history_date=date(node.find("PubmedData/History/PubMedPubDate[@PubStatus='pubmed']")),
                             medline_index_history_date=date(node.find("PubmedData/History/PubMedPubDate[@PubStatus='medline']")),
                             first_publication_verified='',matched_keys=';'.join(sorted(matches)),reconciliation_status=status,
                             source_xml=batch['raw_file'],human_review_status='NOT_REVIEWED',change_applied='NO'))
    exported_dois=defaultdict(set)
    for row in rows:
        if row['doi']:
            exported_dois[row['doi']].add(row['PMID'])
    for row in rows:
        if row['doi'] and len(exported_dois[row['doi']])>1:
            row['reconciliation_status']='DOI_SHARED_BY_MULTIPLE_PMIDS_PENDING'
        title_matches=base_titles.get(title_key(row['title']), set())
        row['additional_exact_title_keys']=';'.join(sorted(title_matches-set(row['matched_keys'].split(';'))))
        if row['additional_exact_title_keys'] and row['reconciliation_status']=='PUBMED_ADDITIONAL_REPORT_KEY':
            row['reconciliation_status']='TITLE_MATCH_PENDING_IDENTIFIER_REVIEW'
        status=row['reconciliation_status']
        row['provisional_report_key']=(
            row['matched_keys'] if status=='BASELINE_IDENTIFIER_MATCH' else
            ('DOI:'+row['doi'] if row['doi'] else 'PMID:'+row['PMID'])
            if status=='PUBMED_ADDITIONAL_REPORT_KEY' else ''
        )
    seen={r['PMID'] for r in rows}
    assert len(rows)==len(seen) and seen<=set(expected)
    write('PubMed_Identifier_Reconciliation.csv',rows)
    query_audit=[]
    partitions=read(HERE/'PubMed_Search_Partitions.csv')
    for route in ('METHOD_ONLY','COMPOUND_CLASS'):
        count_path=CACHE/(route+'_whole_window_count.json')
        raw=count_path.read_bytes()
        result=json.loads(raw)['esearchresult']
        count=int(result['count'])
        observed=sum(route in labels.split(';') for labels in expected.values())
        partition_sum=sum(int(r['unique_pmids']) for r in partitions if r['route']==route)
        query_audit.append(dict(route=route,query_translation=result['querytranslation'],
                                search_utc=dt.datetime.fromtimestamp(count_path.stat().st_mtime,dt.timezone.utc).isoformat(),
                                publication_window='2020-01-01/2026-11-17',whole_window_hits=count,
                                sum_of_partition_counts=partition_sum,duplicate_partition_memberships=partition_sum-observed,
                                distinct_partition_pmids=observed,count_agreement='YES' if count==observed else 'NO',
                                sha256=hashlib.sha256(raw).hexdigest()))
    write('PubMed_Whole_Window_Count_Audit.csv',query_audit)
    anchors=read(HERE/'EuropePMC_Route_Recall_Audit.csv')
    by_export_doi=defaultdict(list)
    for row in rows:
        if row['doi']:by_export_doi[row['doi']].append(row)
    write('Cross_Database_Anchor_Recall.csv',[
        dict(candidate_id=r['candidate_id'],doi=r['doi'],EuropePMC_routes=r['matched_routes'],
             PubMed_PMIDs=';'.join(x['PMID'] for x in by_export_doi[r['doi'].lower()]),
             PubMed_routes=';'.join(sorted({route for x in by_export_doi[r['doi'].lower()] for route in x['query_routes'].split(';')})),
             date_status=r['date_and_scope_eligibility'],
             interpretation='RECORDED_RETRIEVAL_ONLY;INDEXING_AND_DATE_REVIEW_PENDING') for r in anchors])
    summary=dict(expected_pmids=len(expected),verified_xml_records=len(seen),remaining_pmids=len(set(expected)-seen),
                 broad_export_complete=seen==set(expected),targeted_unique_pmids=len(targeted),
                 targeted_pmids_outside_broad_queries=len(targeted-set(expected)),
                 reconciliation=dict(Counter(r['reconciliation_status'] for r in rows)),
                 provisional_added_keys=len({r['provisional_report_key'] for r in rows if r['reconciliation_status']=='PUBMED_ADDITIONAL_REPORT_KEY'}),
                 stage2_complete=False)
    (HERE/'PubMed_Export_Audit.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf8')
    print(summary)

if __name__=='__main__':
    main()
