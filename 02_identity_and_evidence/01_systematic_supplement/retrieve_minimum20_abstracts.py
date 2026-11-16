"""Recover abstract-level evidence packages for all candidates, with explicit reading scope."""
from pathlib import Path
import concurrent.futures
import csv
import datetime
import hashlib
import json
import re
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
CACHE = HERE / 'inputs/minimum20_abstracts'
ALIASES = {
    'Miraxanthin V': ['Miraxanthin-V', 'Dopamine-betaxanthin'],
    '3,4,5-Trimethoxybenzoic acid': ['Eudesmic acid', 'Gallic acid trimethyl ether', 'Trimethylgallic acid'],
    'Coutaric acid': ['trans-p-Coumaroyltartaric acid'],
    '9-cis-beta-Carotene': ['9-cis-β-carotene', '(9Z)-beta-Carotene', '9-cis-b-Carotene'],
    '13-cis-beta-Carotene': ['13-cis-β-carotene', '(13Z)-beta-Carotene', '13-cis-beta,beta-Carotene'],
    '9-cis-Lycopene': ['(9Z)-Lycopene', '(9Z)-psi,psi-carotene'],
    '13-cis-Lycopene': ['(13Z)-Lycopene', 'Neolycopene A'],
    'Iberin': ['3-Methylsulfinylpropyl isothiocyanate'],
    'Methyl allyl sulfide': ['Allyl methyl sulfide', 'Allyl methyl sulphide'],
    'Dipropyl disulfide': ['Propyl disulfide', 'Di-n-propyl disulfide'],
    'Vulgaxanthin I': ['Vulgaxanthin-I'],
    'Vulgaxanthin II': ['Vulgaxanthin-II'],
    'Homocapsaicin': ['Homocapsaicin I', 'E-Homocapsaicin'],
    'Homodihydrocapsaicin': ['Homodihydrocapsaicin I'],
    'trans-Resveratrol': ['(E)-Resveratrol'],
    'Piceid': ['Polydatin'],
    'all-trans-beta-Carotene': ['all-trans-β-Carotene', 'all-trans-β,β-Carotene'],
    'all-trans-Lycopene': ['all-E-Lycopene'],
    'Kaempferol 3-O-glucoside': ['Astragalin'],
    'Luteolin 7-O-glucoside': ['Cynaroside', 'Luteoloside'],
    'Apigenin 6-C-glucoside': ['Isovitexin'],
    'Apigenin 8-C-glucoside': ['Vitexin'],
    'Cyanidin 3-O-glucoside': ['Chrysanthemin', 'Cyanidin-3-glucoside'],
    'Delphinidin 3-O-glucoside': ['Myrtillin', 'Delphinidin-3-glucoside'],
    'Pelargonidin 3-O-glucoside': ['Callistephin', 'Pelargonidin-3-glucoside'],
    'Malvidin 3-O-glucoside': ['Oenin', 'Malvidin-3-glucoside'],
    'Peonidin 3-O-glucoside': ['Peonidin-3-glucoside'],
    'Cyanidin 3-O-rutinoside': ['Keracyanin', 'Cyanidin-3-rutinoside'],
    'Malvidin 3,5-diglucoside': ['Malvin'],
    'beta-Tocotrienol': ['β-Tocotrienol'],
    'beta-Cryptoxanthin': ['β-Cryptoxanthin'],
    'Ubiquinone-10': ['Coenzyme Q10', 'Coenzyme Q-10', 'Ubiquinone 10'],
}
GAP_NAMES = {'3,4,5-Trimethoxybenzoic acid','Coutaric acid','9-cis-beta-Carotene',
             '13-cis-beta-Carotene','9-cis-Lycopene','13-cis-Lycopene','Iberin',
             'Methyl allyl sulfide','Dipropyl disulfide','Probetanin','Vulgaxanthin I',
             'Vulgaxanthin II','Miraxanthin V','Dopaxanthin','Nordihydrocapsaicin',
             'Homocapsaicin','Homodihydrocapsaicin'}


def read(path):
    with path.open(encoding='utf-8-sig', newline='') as handle:
        return list(csv.DictReader(handle))


def fetch(item):
    path = CACHE / (item['candidate_id']+'.json')
    query = item['query']
    if path.exists():
        old = json.loads(path.read_text(encoding='utf8'))
        if old.get('query') == query and old.get('status') == 'SUCCESS':
            return old
        if old.get('query') != query:
            previous=path.with_name(path.stem+'_'+hashlib.sha256(old['query'].encode()).hexdigest()[:12]+'_previous.json')
            if not previous.exists():
                previous.write_bytes(path.read_bytes())
    size = 1000 if item['compound'] in GAP_NAMES | {'trans-Resveratrol','Piceid','all-trans-beta-Carotene','all-trans-Lycopene'} else 100
    url = 'https://www.ebi.ac.uk/europepmc/webservices/rest/search?' + urllib.parse.urlencode(
        dict(query=query, format='json', resultType='core', pageSize=size))
    result = dict(candidate_id=item['candidate_id'], compound=item['compound'], query=query,
                  url=url, date_UTC=datetime.datetime.now(datetime.timezone.utc).isoformat())
    for attempt in range(3):
        try:
            with urllib.request.urlopen(url, timeout=35) as response:
                data = json.load(response)
            result.update(status='SUCCESS', hits=data['hitCount'], records=data.get('resultList', {}).get('result', []))
            break
        except Exception as error:
            result.update(status='FAILED', error=str(error), records=[])
            time.sleep(attempt+1)
    temporary = path.with_suffix('.tmp')
    temporary.write_text(json.dumps(result, ensure_ascii=False)+'\n', encoding='utf8')
    temporary.replace(path)
    return result


def plain(text):
    try:
        return ' '.join(ET.fromstring('<root>'+text+'</root>').itertext())
    except ET.ParseError:
        return re.sub('<[^>]+>', ' ', text)


def main():
    CACHE.mkdir(parents=True, exist_ok=True)
    items = [r for r in read(HERE/'Search_Coverage_Audit.csv') if r['route']=='broad']
    for item in items:
        names=[item['compound']]+ALIASES.get(item['compound'], [])
        if len(names)>1:
            item['query']='('+' OR '.join('TITLE_ABS:"'+name+'"' for name in names)+') AND (antioxidant OR antioxidative OR redox OR radical OR dietary OR food)'
        if item['compound'] in GAP_NAMES:
            item['query']='('+' OR '.join('TITLE_ABS:"'+name+'"' for name in names)+')'
    packages, audit = [], []
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        for number, response in enumerate(pool.map(fetch, items), 1):
            cid = response['candidate_id']
            path = CACHE/(cid+'.json')
            seen, accepted = set(), []
            for record in response['records']:
                doi = record.get('doi', '').lower()
                key = doi or record.get('pmid') or plain(record.get('title', ''))
                if not key or key in seen:
                    continue
                seen.add(key)
                abstract = plain(record.get('abstractText', ''))
                title = plain(record.get('title', ''))
                text = (title+' '+abstract).lower()
                names=[response['compound']]+ALIASES.get(response['compound'], [])
                patterns=[r'(?<!\w)'+r'[-\s]*'.join(re.escape(part) for part in re.split(r'[-\s]+', name.lower()))+r'(?!\w)' for name in names]
                explicit_name = any(re.search(pattern, text) for pattern in patterns)
                related = bool(re.search(r'antiox|oxidative|redox|radical|dietary|food', text))
                if not abstract or not explicit_name or not related:
                    continue
                scope = 'ORAC_MENTION_REQUIRES_ORIGINAL_CAPACITY_CHECK' if re.search(r'\borac\b|oxygen radical absorbance', text) else 'ANTIOXIDANT_OR_DIETARY_CONTEXT'
                row = dict(candidate_id=cid, compound=response['compound'], doi=doi,
                           PMID=record.get('pmid', ''), PMCID=record.get('pmcid', ''), title=title,
                           year=record.get('pubYear', ''),
                           journal=record.get('journalInfo', {}).get('journal', {}).get('title', ''),
                           abstract=abstract, reading_scope='AUTOMATED_TITLE_ABSTRACT_RULE_SCREEN',
                           publication_types=';'.join(record.get('pubTypeList', {}).get('pubType', [])),
                           evidence_role=scope, fulltext_scientific_check='PENDING',
                           candidate_relevance='EXPLICIT_NAME_OR_DOCUMENTED_ALIAS_AND_CONTEXT_MATCH_PENDING_REVIEW',
                           query=response['query'], source_url=response['url'],
                           source_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                           model_label_release='NO', human_review_status='NOT_REVIEWED', change_applied='NO')
                accepted.append(row)
            # Keep every qualifying record from this first page, including evidence beyond 20.
            packages.extend(accepted)
            audit.append(dict(candidate_id=cid, compound=response['compound'], status=response['status'],
                              hit_count=response.get('hits', ''), records_retrieved=len(response['records']),
                              rule_screened_relevant_abstracts=len(accepted), target=20,
                              target_reached_at_abstract_rule_level='YES' if len(accepted)>=20 else 'NO',
                              complete_search=response.get('hits', 0)<=len(response['records']) if response['status']=='SUCCESS' else False,
                              scarcity_established='NO', remaining='ALIAS_EXPANSION_PAGINATION_FULLTEXT_AND_SCIENTIFIC_REVIEW',
                              query=response['query'], source_url=response['url']))
            if number%20==0:
                print('Candidates processed', number, flush=True)
    for name, rows in [('Minimum20_Abstract_Evidence_Packages.csv', packages), ('Minimum20_Abstract_Coverage.csv', audit)]:
        if rows:
            with (HERE/name).open('w', encoding='utf8', newline='') as handle:
                writer=csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator='\n')
                writer.writeheader(); writer.writerows(rows)
    print(json.dumps(dict(candidates=len(audit), abstracts=len(packages), reached20=sum(r['target_reached_at_abstract_rule_level']=='YES' for r in audit), failed=sum(r['status']!='SUCCESS' for r in audit))), flush=True)
    gaps=[]
    for row in audit:
        if row['target_reached_at_abstract_rule_level']=='YES':
            continue
        names=[row['compound']]+ALIASES.get(row['compound'], [])
        terms=' OR '.join('"'+name+'"' for name in names)
        gaps.append(dict(candidate_id=row['candidate_id'],compound=row['compound'],
                         current_abstract_rule_count=row['rule_screened_relevant_abstracts'],
                         gap_to_20=max(0,20-row['rule_screened_relevant_abstracts']),
                         Web_of_Science_query='TS=('+terms+')',
                         Scopus_query='TITLE-ABS-KEY('+terms+')',
                         scope='BROAD_CHEMICAL_NAME_SEARCH_FOR_SCARCITY_AND_MISSED_CONTEXT',
                         alias_review='REQUIRED_BEFORE_SCARCITY_EXCEPTION',scarcity_established='NO'))
    if gaps:
        with (HERE/'Minimum20_Remaining_Gaps_and_Export_Queries.csv').open('w',encoding='utf8',newline='') as handle:
            writer=csv.DictWriter(handle,fieldnames=list(gaps[0]),lineterminator='\n')
            writer.writeheader();writer.writerows(gaps)
    summary=dict(candidates=len(audit),candidate_abstract_links=len(packages),
                 unique_articles=len({r['doi'] or r['PMID'] or r['title'] for r in packages}),
                 abstract_rule_target_reached=sum(r['target_reached_at_abstract_rule_level']=='YES' for r in audit),
                 remaining_candidates=len(gaps),failures=sum(r['status']!='SUCCESS' for r in audit),
                 scarcity_exceptions_established=0,fulltext_review_complete=False,
                 minimum20_scientifically_verified_for_all_candidates=False)
    (HERE/'minimum20_abstract_summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf8')


if __name__ == '__main__':
    main()
