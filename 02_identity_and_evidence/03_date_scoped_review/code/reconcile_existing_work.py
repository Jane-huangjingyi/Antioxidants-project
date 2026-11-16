"""Reuse existing records for the authorized date-scoped review; no new searches."""
from pathlib import Path
import collections
import csv
import datetime
import json

HERE=Path(__file__).resolve().parents[1]
ROOT=HERE.parents[1]
SOURCE=HERE.parent/'01_systematic_supplement'
CUTOFF='2026-11-16'


def read(path):
    with path.open(encoding='utf-8-sig',newline='') as handle:
        return list(csv.DictReader(handle))


def write(name,rows):
    with (HERE/'results'/name).open('w',encoding='utf8',newline='') as handle:
        writer=csv.DictWriter(handle,fieldnames=list(rows[0]),lineterminator='\n')
        writer.writeheader();writer.writerows(rows)


def main():
    articles=read(SOURCE/'Master_Article_Register.csv')
    links=read(SOURCE/'Master_Candidate_Article_Links.csv')
    integrated=read(ROOT/'03_candidate_selection/07_all_reference_integration/All_Reference_Consideration_Register.csv')
    existing_pairs={(r['candidate_id'],r['article_key']) for r in links}
    article_keys={r['article_key'] for r in articles}
    for r in integrated:
        if (r['candidate_id'],r['article_key']) not in existing_pairs:
            links.append(dict(candidate_id=r['candidate_id'],article_key=r['article_key']))
            existing_pairs.add((r['candidate_id'],r['article_key']))
        if r['article_key'] not in article_keys:
            articles.append(dict(article_key=r['article_key'],doi=r['doi'],PMID='',PMCID='',title=r['title'],journal='',year=''))
            article_keys.add(r['article_key'])
    packages=read(SOURCE/'Minimum20_Abstract_Evidence_Packages.csv')+read(SOURCE/'Minimum20_Body_Located_Leads.csv')
    profiles=read(HERE.parent/'results/candidate_evidence_profiles.csv')
    screenings={r['doi']:r for r in read(SOURCE/'Source_Scientific_Screening.csv') if r['doi']}
    audited={r['doi'] for r in read(ROOT/'03_candidate_selection/08_capacity_review_validation/Capacity_Row_Review.csv')}
    current_decisions=HERE/'results/Current_Scientific_Source_Decisions.csv'
    current_review_map={r['doi']:r for r in read(current_decisions)} if current_decisions.exists() else {}
    current_reviewed=set(current_review_map)
    dates={}
    for path in (SOURCE/'inputs/minimum20_abstracts').glob('AFF-*.json'):
        if path.stem.endswith('_previous'):continue
        for r in json.loads(path.read_text(encoding='utf8')).get('records',[]):
            date=r.get('firstPublicationDate','')
            if date:
                for key in [r.get('doi','').lower(),r.get('pmid','')]:
                    if key:dates[key]=date
    def period(article):
        date=dates.get(article['doi'],dates.get(article.get('PMID',''),''))
        year=date[:4] if date else article.get('year','')
        if not year.isdigit():return 'DATE_UNRESOLVED',date
        if date and date>CUTOFF or int(year)>2026:return 'AFTER_CUTOFF',date
        if int(year)>=2020:return 'PRIMARY_2020_2026',date
        if int(year)>=2016:return 'EXTENSION_2016_2019',date
        return 'EARLIER_HISTORICAL',date
    lookup={r['article_key']:r for r in articles}
    primary_leads=collections.defaultdict(set)
    for r in packages:
        p,_=period(r)
        if p=='PRIMARY_2020_2026':primary_leads[r['candidate_id']].add(r['doi'] or r['PMID'] or r['title'])
    extension={r['candidate_id'] for r in profiles if len(primary_leads[r['candidate_id']])<20}
    article_candidates=collections.defaultdict(set)
    for r in links:
        article_candidates[r['article_key']].add(r['candidate_id'])
    register=[]
    for key,candidates in article_candidates.items():
        a=lookup[key];p,date=period(a)
        eligible=p=='PRIMARY_2020_2026' or p=='EXTENSION_2016_2019' and bool(candidates&extension)
        status='TITLE_ABSTRACT_SCIENTIFIC_SCREEN_PENDING'
        if a['doi'] in screenings:status='REUSE_RECORDED_SOURCE_SCREEN_SCOPE'
        if a['doi'] in audited:status='REUSE_ORIGINAL_NUMERIC_ROW_REVIEW_SCOPE'
        if a['doi'] in current_reviewed:status='REUSE_CURRENT_SOURCE_DECISION_SCOPE'
        register.append(dict(article_key=key,doi=a['doi'],PMID=a['PMID'],PMCID=a['PMCID'],title=a['title'],
                             journal=a['journal'],issue_year=a['year'],first_publication_date=date,
                             date_verification='EXACT_DATE_REUSED' if date else 'YEAR_ONLY_REQUIRES_DATE_CHECK',
                             period=p,in_current_review_scope='YES' if eligible else 'NO',
                             linked_candidates=';'.join(sorted(candidates)),existing_review_status=status,
                             recorded_reading_scope=current_review_map.get(a['doi'],{}).get('reading_scope',
                                 'ORIGINAL_NUMERIC_ROW_REVIEW' if a['doi'] in audited else screenings.get(a['doi'],{}).get('reading_scope','')),
                             next_action='REVIEW_ONLY_MISSING_FIELDS' if status.startswith('REUSE') else 'SCREEN_RELEVANCE_AND_ORIGINAL_CAPACITY',
                             human_review_status='NOT_REVIEWED',change_applied='NO'))
    write('Date_Scoped_Article_Register.csv',register)
    bykey={r['article_key']:r for r in register}
    candidate_rows=[]
    bycid=collections.defaultdict(list)
    for r in links:bycid[r['candidate_id']].append(bykey[r['article_key']])
    for p in profiles:
        cid=p['candidate_id'];records=bycid[cid]
        candidate_rows.append(dict(candidate_id=cid,compound=p['compound_name'],
                                   primary_located_leads=len(primary_leads[cid]),
                                   extend_to_2016='YES' if cid in extension else 'NO',
                                   expansion_reason='FEWER_THAN_20_PRIMARY_WINDOW_LOCATED_LEADS' if cid in extension else '',
                                   primary_retrieval_associations=sum(r['period']=='PRIMARY_2020_2026' for r in records),
                                   extension_retrieval_associations=sum(r['period']=='EXTENSION_2016_2019' for r in records),
                                   prior_screened_article_associations=sum(r['existing_review_status'].startswith('REUSE') for r in records),
                                   scientific_screening_complete='NO',scarcity_established='NO'))
    write('Candidate_Date_Window_and_Reuse.csv',candidate_rows)
    counts=collections.Counter(r['period'] for r in register)
    summary=dict(cutoff=CUTOFF,candidates=193,unique_candidate_linked_article_keys=len(register),
                 article_period_counts=dict(counts),candidate_extension_needed=len(extension),
                 in_scope_provisional_article_keys=sum(r['in_current_review_scope']=='YES' for r in register),
                 prior_scientific_screen_keys_reused=sum(r['existing_review_status'].startswith('REUSE') for r in register),
                 new_searches_executed=0,denominator_status='EXISTING_CORPUS_RECONCILIATION_MULTI_DATABASE_COMPLETION_PENDING',
                 all_screening_complete=False)
    (HERE/'results/scope_reconciliation_summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf8')
    write('Database_Coverage_Gaps.csv',[dict(database=name,status=status,remaining_work=work) for name,status,work in [
        ('PubMed/Europe PMC','REUSE_EXISTING_QUERIES_AND_CACHES','Apply date scope and complete eligibility screening; Europe PMC includes PubMed records.'),
        ('PubChem','REUSE_IDENTITY_AND_SYNONYM_CACHE','Resolve exact forms and missing Probetanin identity.'),
        ('Web of Science','INSTITUTION_EXPORT_PENDING','Obtain dated full-record and cited-reference export; deduplicate against existing corpus.'),
        ('CNKI','DATABASE_EXPORT_PENDING','Run Chinese compound/synonym searches and export all records with abstracts.'),
        ('Google Scholar','SYSTEMATIC_SEARCH_LOG_PENDING','Record exact searches, dates, inspected result ranges and citation tracing.')]])
    print(json.dumps(summary))


if __name__=='__main__':main()
