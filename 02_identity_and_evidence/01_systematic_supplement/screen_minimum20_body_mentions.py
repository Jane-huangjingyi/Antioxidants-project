"""Recover public body-text evidence leads for compounds under the abstract target.

Paragraph matches establish a located contextual mention. Scientific evidence
strength and original-experiment eligibility require subsequent source review.
"""
from pathlib import Path
import concurrent.futures
import csv
import hashlib
import json
import re
import urllib.request
import xml.etree.ElementTree as ET
import retrieve_minimum20_abstracts as retrieval

HERE = Path(__file__).resolve().parent
retrieval.CACHE = HERE / 'inputs/minimum20_body_queries'
retrieval.CACHE.mkdir(parents=True, exist_ok=True)
XML = HERE / 'fulltext_xml'


def write(name, rows):
    if not rows:
        return
    with (HERE/name).open('w', encoding='utf8', newline='') as handle:
        writer=csv.DictWriter(handle,fieldnames=list(rows[0]),lineterminator='\n')
        writer.writeheader();writer.writerows(rows)


def check(record, names):
    pmcid=record.get('pmcid', '')
    if not pmcid:
        return None, 'NO_PUBLIC_PMC_IDENTIFIER'
    path=XML/(pmcid+'.xml')
    url='https://www.ebi.ac.uk/europepmc/webservices/rest/'+pmcid+'/fullTextXML'
    try:
        if not path.exists():
            with urllib.request.urlopen(url,timeout=25) as response:
                data=response.read()
            ET.fromstring(data)
            temporary=path.with_suffix('.tmp');temporary.write_bytes(data);temporary.replace(path)
        root=ET.fromstring(path.read_bytes())
        body=root.find('body')
        if body is None:
            return None,'NO_BODY_ELEMENT'
        patterns=[r'(?<!\w)'+r'[-\s]*'.join(re.escape(part) for part in re.split(r'[-\s]+',name.lower()))+r'(?!\w)' for name in names]
        for index,node in enumerate(body.iter('p'),1):
            text=' '.join(node.itertext())
            if any(re.search(pattern,text.lower()) for pattern in patterns):
                return dict(doi=record.get('doi','').lower(),PMID=record.get('pmid',''),PMCID=pmcid,
                            title=retrieval.plain(record.get('title','')),year=record.get('pubYear',''),
                            source_url=url,source_file=path.relative_to(HERE).as_posix(),
                            source_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                            paragraph_locator='body paragraph '+str(index),matched_paragraph=text,
                            reading_scope='TARGETED_BODY_PARAGRAPH_NAME_LOCATION',
                            evidence_status='CONTEXTUAL_MENTION_REQUIRES_SCIENTIFIC_RELEVANCE_REVIEW',
                            model_label_release='NO',human_review_status='NOT_REVIEWED',change_applied='NO'),'LOCATED'
        return None,'NAME_NOT_LOCATED_IN_BODY_PARAGRAPHS'
    except Exception as error:
        return None,'FETCH_OR_PARSE_FAILED '+str(error)


def main():
    gaps=retrieval.read(HERE/'Minimum20_Remaining_Gaps_and_Export_Queries.csv')
    abstracts=retrieval.read(HERE/'Minimum20_Abstract_Evidence_Packages.csv')
    packages,audit,attempts=[],[],[]
    for gap in gaps:
        cid=gap['candidate_id'];compound=gap['compound']
        names=[compound]+retrieval.ALIASES.get(compound,[])
        query='('+' OR '.join('BODY:"'+name+'"' for name in names)+')'
        response=retrieval.fetch(dict(candidate_id=cid,compound=compound,query=query))
        existing={r['doi'] or r['PMID'] or r['title'] for r in abstracts if r['candidate_id']==cid}
        records=[];seen=set(existing)
        for record in response['records']:
            key=record.get('doi','').lower() or record.get('pmid') or retrieval.plain(record.get('title',''))
            if key and key not in seen:
                seen.add(key);records.append(record)
        located=[]
        checked=0
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
            for start in range(0,len(records),3):
                batch=records[start:start+3]
                results=list(pool.map(lambda r:check(r,names),batch))
                checked+=len(batch)
                for record,(result,status) in zip(batch,results):
                    attempts.append(dict(candidate_id=cid,compound=compound,doi=record.get('doi',''),PMCID=record.get('pmcid',''),status=status,query=query))
                    if result:
                        located.append(dict(candidate_id=cid,compound=compound,**result))
                if len(existing)+len(located)>=20:
                    break
        packages.extend(located)
        audit.append(dict(candidate_id=cid,compound=compound,query=query,search_status=response['status'],
                          search_hits=response.get('hits',''),retrieved=len(response['records']),
                          source_records_checked=checked,unexamined_records=len(records)-checked,
                          new_body_located_articles=len(located),abstract_rule_articles=len(existing),
                          combined_located_leads=len(existing)+len(located),
                          scarcity_established='NO',scientific_review_complete='NO'))
        print(compound,'body leads',len(located),flush=True)
    write('Minimum20_Body_Located_Leads.csv',packages)
    write('Minimum20_Body_Search_Audit.csv',audit)
    write('Minimum20_Body_Recovery_Attempts.csv',attempts)
    abstract_coverage=retrieval.read(HERE/'Minimum20_Abstract_Coverage.csv')
    body_by_candidate={r['candidate_id']:r for r in audit}
    progress=[]
    for row in abstract_coverage:
        cid=row['candidate_id'];extra=body_by_candidate.get(cid,{})
        count=int(row['rule_screened_relevant_abstracts'])
        body_count=int(extra.get('new_body_located_articles',0))
        progress.append(dict(candidate_id=cid,compound=row['compound'],abstract_rule_articles=count,
                             additional_body_located_articles=body_count,total_located_leads=count+body_count,
                             twenty_located_leads='YES' if count+body_count>=20 else 'NO',
                             scientifically_verified_twenty_papers='PENDING',
                             model_label_release='NO',scarcity_established='NO',
                             human_review_status='NOT_REVIEWED',change_applied='NO'))
    write('Minimum20_Combined_Progress.csv',progress)
    summary=dict(candidates=len(progress),abstract_target_reached=sum(r['abstract_rule_articles']>=20 for r in progress),
                 combined_located_target_reached=sum(r['twenty_located_leads']=='YES' for r in progress),
                 new_body_located_links=len(packages),remaining_located_gaps=[r['compound'] for r in progress if r['twenty_located_leads']=='NO'],
                 all_scientific_reviews_complete=False,scarcity_exceptions_established=0)
    (HERE/'minimum20_combined_summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf8')
    print(json.dumps(dict(compounds=len(audit),body_leads=len(packages))),flush=True)


if __name__=='__main__':
    main()
