"""Resume fully paginated public method/class retrieval under protocolv1.1."""
from pathlib import Path
import csv,json,hashlib,urllib.request,urllib.parse,datetime,time

HERE=Path(__file__).resolve().parents[1]
ROOT=HERE.parents[1]
CACHE=ROOT/'02_identity_and_evidence/01_systematic_supplement/inputs/stage2_v1_1'
CACHE.mkdir(exist_ok=True)
WINDOW='FIRST_PDATE:[2020-01-01 TO 2026-11-17]'
METHOD='TITLE_ABS:("oxygen radical absorbance" OR "ORAC" OR "crocin bleaching" OR "CUPRAC" OR "DPPH" OR "ABTS" OR "ferric reducing antioxidant")'
QUERIES={'METHOD_ONLY':METHOD+' AND '+WINDOW,
 'COMPOUND_CLASS': 'TITLE_ABS:(phenolic OR flavonoid OR carotenoid OR lignan OR vitamin OR thiol OR alkaloid) AND TITLE_ABS:(antioxidant OR "radical scavenging") AND '+WINDOW}

def write(name,rows):
    target=(CACHE/name) if name=='Public_Article_Register.csv' else (HERE/name)
    with target.open('w',encoding='utf8',newline='') as h:
        w=csv.DictWriter(h,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)

def main():
    logs=[];manifest=[];articles={};origins=[]
    for route,query in QUERIES.items():
        cursor='*';page=0;total=0;expected=None;source_ids=set()
        while True:
            page+=1;path=CACHE/f'{route}_{page:04d}.json'
            params=dict(query=query,format='json',resultType='lite',pageSize=1000,cursorMark=cursor)
            url='https://www.ebi.ac.uk/europepmc/webservices/rest/search?'+urllib.parse.urlencode(params)
            if not path.exists():
                with urllib.request.urlopen(url,timeout=60) as response:data=response.read()
                parsed=json.loads(data)
                temporary=path.with_suffix('.tmp');temporary.write_bytes(data);temporary.replace(path)
                time.sleep(.4)
            data=path.read_bytes();parsed=json.loads(data)
            expected=parsed['hitCount'];records=parsed.get('resultList',{}).get('result',[])
            total+=len(records)
            manifest.append(dict(route=route,page=page,raw_file=path.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(data).hexdigest(),records=len(records),source_url=url))
            for r in records:
                source_ids.add(r.get('source','')+':'+r['id'])
                doi=r.get('doi','').lower();key='DOI:'+doi if doi else r.get('source','')+':'+r['id']
                articles.setdefault(key,dict(article_key=key,doi=doi,PMID=r['id'] if r.get('source')=='MED' else '',PMCID=r.get('pmcid',''),title=r.get('title',''),journal=r.get('journalTitle',''),year=r.get('pubYear',''),first_public_date=r.get('firstPublicationDate',''),formal_issue_date='',index_date='',date_evidence='PUBLIC_LITE_METADATA;CORE_DATE_REVIEW_PENDING',screening_status='PENDING',human_review_status='NOT_REVIEWED',change_applied='NO'))
                origins.append(dict(article_key=key,route=route,raw_file=path.relative_to(ROOT).as_posix(),source_record_id=r['id']))
            print(route,page,total,expected,flush=True)
            next_cursor=parsed.get('nextCursorMark','')
            if not records or not next_cursor or next_cursor==cursor:break
            cursor=next_cursor
        logs.append(dict(database='Europe PMC',route=route,query=query,cutoff='2026-11-17',execution_UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),hit_count=expected,downloaded_records=total,unique_source_records=len(source_ids),pagination_duplicate_records=total-len(source_ids),complete=len(source_ids)==expected,cursor_exhausted=True,count_consistency='RECONCILED_PAGINATION_DUPLICATES' if total!=len(source_ids) and len(source_ids)==expected else 'MATCH' if total==expected else 'HIT_COUNT_DRIFT_REVIEW_REQUIRED',syntax_test='API_ACCEPTED',food_terms_required='NO',independent_PubMed_execution='NO'))
        write('Database_Search_Log.csv',logs);write('Raw_Export_Manifest.csv',manifest)
        write('Public_Article_Register.csv',list(articles.values()));write('Public_Article_Search_Origins.csv',origins)
    known=list(csv.DictReader((ROOT/'02_identity_and_evidence/04_systematic_protocol_v1/Known_Study_Recall_Audit.csv').open(encoding='utf-8-sig')))
    dois={r['doi'] for r in articles.values() if r['doi']}
    write('Public_Query_Anchor_Recall.csv',[dict(candidate_id=r['candidate_id'],doi=r['reference_doi'],retrieved_by_revised_public_routes='YES' if r['reference_doi'].lower() in dois else 'NO',date_and_scope_eligibility='REQUIRES_ANCHOR_DATE_REVIEW',interpretation='MISS_REQUIRES_INDEX_DATE_ALIAS_AND_QUERY_AUDIT;DOI_LOOKUP_SEPARATE') for r in known])
    print('Public retrieval finished; remaining database gates require audit.',flush=True)

if __name__=='__main__':main()
