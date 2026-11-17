"""Consolidate the completed public retrieval snapshot; institutional gate stays open."""
from pathlib import Path
import csv,json,hashlib,collections
HERE=Path(__file__).resolve().parents[1]
ROOT=HERE.parents[1]
SOURCE=ROOT/'02_identity_and_evidence/01_systematic_supplement'
def read(p):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def write(name,rows):
    with (HERE/name).open('w',encoding='utf8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
def main():
    logs=read(HERE/'Database_Search_Log.csv')
    assert len(logs)==2 and all(r['cursor_exhausted']=='True' for r in logs)
    old=read(SOURCE/'Master_Article_Register.csv');new=read(SOURCE/'inputs/stage2_v1_1/Public_Article_Register.csv')
    records={};duplicates=[];aliases={}
    cached_metadata={}
    for path in (SOURCE/'inputs/stage2_v1_1').glob('*_[0-9][0-9][0-9][0-9].json'):
        for raw in json.loads(path.read_bytes()).get('resultList',{}).get('result',[]):
            cached_metadata[raw.get('doi','').lower() or raw.get('id','')]=raw
    versions={r['preprint_doi']:r for r in read(ROOT/'02_identity_and_evidence/03_date_scoped_review/results/Study_Version_Link_Register.csv')}
    for origin,items in [('LEGACY_MASTER',old),('EUROPE_PMC_V11',new)]:
        for r in items:
            doi=r.get('doi','').lower().strip();key='DOI:'+doi if doi else 'PMID:'+r['PMID'] if r.get('PMID') else r['article_key']
            aliases[r['article_key']]=key
            if key in records:
                existing=records[key]
                duplicates.append(dict(record_key=key,incoming_article_key=r['article_key'],retained_key=existing['article_key'],rule='EXACT_DOI_OR_PMID_KEY',origin=origin,decision='BIBLIOGRAPHIC_KEY_MERGE;EXPERIMENT_INDEPENDENCE_PENDING'))
                existing['database_origins']=';'.join(sorted(set(existing['database_origins'].split(';'))|{origin}))
                if r.get('first_public_date'):existing['first_public_date']=r['first_public_date']
                continue
            records[key]=dict(article_key=key,doi=doi,PMID=r.get('PMID',''),PMCID=r.get('PMCID',''),title=r['title'],journal=r.get('journal',''),year=r.get('year',''),first_public_date=r.get('first_public_date',''),formal_issue_date='',index_date='',database_origins=origin,source_article_key=r['article_key'],canonical_study_key=versions[doi]['canonical_study_key'] if doi in versions else key,date_review_status='FIRST_ISSUE_INDEX_DATES_REQUIRE_RECONCILIATION',screening_status='PENDING_OR_REUSE_RECORDED_SCOPE',human_review_status='NOT_REVIEWED',change_applied='NO')
    for record in records.values():
        raw=cached_metadata.get(record['doi'] or record['PMID'],{})
        record['authors']=raw.get('authorString','')
        record['first_public_date']=record['first_public_date'] or raw.get('firstPublicationDate','')
    for r in versions.values():duplicates.append(dict(record_key='DOI:'+r['preprint_doi'],incoming_article_key='DOI:'+r['preprint_doi'],retained_key=r['canonical_study_key'],rule=r['relationship'],origin=r['source_url'],decision='VERSION_FAMILY_GROUPING;NUMERIC_EQUIVALENCE_PENDING'))
    write('Duplicate_and_Version_Link_Register.csv',duplicates)
    links=read(ROOT/'03_candidate_selection/07_all_reference_integration/All_Reference_Consideration_Register.csv')
    link_rows=[]
    for r in links:
        key=aliases.get(r['article_key'],'DOI:'+r['doi'].lower() if r['doi'] else r['article_key'])
        if key not in records:
            stub=dict.fromkeys(next(iter(records.values())).keys(),'')
            stub.update(article_key=key,doi=r['doi'],title=r['title'],source_article_key=r['article_key'],database_origins='ORIGINAL_EXTRACTION_REFERENCE_STUB',canonical_study_key=key,date_review_status='PENDING',screening_status='REUSE_SOURCE_SPECIFIC_EXTRACTION_SCOPE',human_review_status='NOT_REVIEWED',change_applied='NO')
            records[key]=stub
        link_rows.append(dict(candidate_id=r['candidate_id'],article_key=key,original_article_key=r['article_key'],doi=r['doi'],origin_register='Step03.7 All_Reference_Consideration_Register.csv',association_status='REUSE_EXISTING;NEW_DISCOVERY_COMPOUND_ASSIGNMENT_PENDING',human_review_status='NOT_REVIEWED',change_applied='NO'))
    assert all(r['article_key'] in records for r in link_rows)
    prior_scopes={r['doi']:r for r in read(ROOT/'02_identity_and_evidence/03_date_scoped_review/results/Current_Scientific_Source_Decisions.csv')}
    for record in records.values():
        prior=prior_scopes.get(record['doi'],{})
        record['screening_status']='REUSE_TARGETED_SCOPE_RESIDUAL_REVIEW_PENDING' if prior else 'PENDING'
        record['prior_reading_scope']=prior.get('reading_scope','')
        record['prior_scope_register']='Step02.3 Current_Scientific_Source_Decisions.csv' if prior else ''
    write('Candidate_Article_Links.csv',link_rows)
    write('Deduplicated_Article_Register.csv',list(records.values()))
    bydoi={r['doi']:r for r in records.values() if r['doi']}
    recall=read(HERE/'Public_Query_Anchor_Recall.csv')
    for row in recall:
        source=bydoi.get(row['doi'].lower(),{});date=source.get('first_public_date','')
        row['available_first_public_date']=date;row['available_issue_year']=source.get('year','')
        row['date_and_scope_eligibility']='PRIMARY_DATE_CANDIDATE_REQUIRES_SCOPE_REVIEW' if date and '2020-01-01'<=date<='2026-11-17' else 'OUTSIDE_PRIMARY_BY_AVAILABLE_DATE' if date else 'DATE_REVIEW_PENDING'
    write('Public_Query_Anchor_Recall.csv',recall)
    n=len(records);assert n==len({r['article_key'] for r in records.values()})
    summary=dict(status='IN_PROGRESS_INSTITUTIONAL_EXPORTS_AND_OTHER_DATABASE_GATES_PENDING',legacy_master_rows=len(old),public_unique_keys=len(new),consolidated_identifier_keys=n,public_hit_associations=sum(int(r['hit_count']) for r in logs),public_downloaded_associations=sum(int(r['downloaded_records']) for r in logs),candidate_article_links=len(links),institutional_complete=False,stage2_complete=False,public_hit_count_consistency=[dict(route=r['route'],status=r['count_consistency']) for r in logs],new_candidate_identity_assignment='PENDING',revised_compound_query_update='PENDING',pubmed_full_export='PENDING',scholar_access='UNAVAILABLE_IN_CHECKED_WEB_TOOL')
    (HERE/'stage2_public_summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf8')
    text=f"# Stage2 public retrieval QC\n\nPublic retrieval snapshot PASS. Stage2 completion gate OPEN. Two public cursor chains exhausted. Three category-route pagination duplicates reconcile the difference between downloaded and reported counts. Consolidated identifier keys {n}; existing candidate associations {len(links)}. Exact identifier grouping preserves provenance. Known anchors are audited separately. Title/author/year near-duplicate and conflicting identifier adjudication remain pending. Institutional exports,independent PubMed export,Scholar inspection,revised compound queries and new-compound assignment remain pending. Human review status remains NOT_REVIEWED.\n"
    (HERE/'Stage2_QC_Report.md').write_text(text,encoding='utf8')
    (HERE/'Database_Coverage_Audit.md').write_text('# Database coverage audit\n\nEurope PMC method/class cursor chains were exhausted. Three repeated source IDs reconcile the category-route pagination count. PubMed method query accepted by API with25,806hits and zero exported records in that syntax test. Europe PMC includes PubMed records; independent PubMed retrieval remains distinct. WoS,CNKI and Scopus await researcher exports and actual platform syntax/recall tests. Google Scholar query was inaccessible in the checked browser tool; inspected result count remains zero. Existing193-compound caches and prior source scopes are reused; revised compound-route updates remain pending. Stage2 remains in progress.\n',encoding='utf8')
    dictionary=[]
    for path in sorted(HERE.glob('*.csv')):
        if path.name=='Stage2_Field_Dictionary.csv':continue
        with path.open(encoding='utf-8-sig',newline='') as f:fields=next(csv.reader(f))
        for field in fields:dictionary.append(dict(table=path.name,field=field,meaning=field.replace('_',' '),missing_rule='Blank means unavailable or pending; preserve explicit status',scope='Public checkpoint; all scientific decisions pending'))
    write('Stage2_Field_Dictionary.csv',dictionary)
    print(json.dumps(summary))
if __name__=='__main__':main()
