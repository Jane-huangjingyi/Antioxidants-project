"""Audit shared identifiers and flag possible duplicates without merging reports."""
from collections import defaultdict, Counter
from difflib import SequenceMatcher
import re
import unicodedata
from finalize_public_snapshot import HERE, ROOT, read, write

def title_key(title):
    return re.sub(r'[^\w]', '', unicodedata.normalize('NFKC', re.sub('<[^>]+>', '', title)).casefold())

def near_title_candidates(articles):
    buckets = defaultdict(list)
    comparable = 0
    for row in articles:
        author = title_key(re.split('[,;|]', row['authors'], maxsplit=1)[0])
        title = title_key(row['title'])
        if not author or not row['year'].isdigit() or len(title) < 40:
            continue
        comparable += 1
        buckets[author, title[:12]].append((row['article_key'], int(row['year']), title))
    for bucket in buckets.values():
        bucket.sort(key=lambda record: record[1])
    candidates = []
    for bucket in buckets.values():
        for i, (first_key, first_year, first_title) in enumerate(bucket):
            for second_key, second_year, second_title in bucket[i+1:]:
                if second_year-first_year > 1:
                    break
                if first_title == second_title:
                    continue
                matcher = SequenceMatcher(None, first_title, second_title, autojunk=False)
                if matcher.real_quick_ratio() < .93 or matcher.quick_ratio() < .93:
                    continue
                score = matcher.ratio()
                if score >= .93:
                    candidates.append(dict(article_key_a=first_key, article_key_b=second_key,
                                           title_similarity=f'{score:.4f}', year_gap=second_year-first_year,
                                           status='PENDING_AUTHOR_TITLE_AND_VERSION_REVIEW'))
    return comparable, candidates

def main():
    articles=read(HERE/'Deduplicated_Article_Register.csv')
    origins=read(HERE/'Public_Article_Search_Origins.csv')
    groups=defaultdict(set)
    routes=defaultdict(set)
    for row in origins:
        routes[row['route']].add(row['article_key'])
    for row in articles:
        for field in ('doi','PMID','PMCID'):
            value=row[field].strip().casefold()
            if field=='PMID' and not value and row['article_key'].startswith('PMID:'):
                value=row['article_key'].split(':',1)[1]
            if value:
                groups[field,value].add(row['article_key'])
        normalized=title_key(row['title'])
        if len(normalized)>=24:
            groups['title',normalized].add(row['article_key'])
    flags=[dict(group_type=field,match_key=value,record_count=len(keys),article_keys=';'.join(sorted(keys)),
                status='PENDING_IDENTIFIER_OR_VERSION_REVIEW',human_review_status='NOT_REVIEWED')
           for (field,value),keys in sorted(groups.items()) if len(keys)>1]
    write('Identifier_and_Title_Conflict_Queue.csv',flags)
    comparable, near_titles=near_title_candidates(articles)
    if near_titles:
        write('Near_Title_Author_Year_Review_Queue.csv',near_titles)
    print('Near-title comparability:', comparable, 'of', len(articles), 'records. Pairs:', len(near_titles))
    doi_routes=defaultdict(set)
    for route,keys in routes.items():
        for key in keys:
            if key.startswith('DOI:'):
                doi_routes[key[4:].casefold()].add(route)
    anchors=read(HERE/'Public_Query_Anchor_Recall.csv')
    write('EuropePMC_Route_Recall_Audit.csv',[dict(**row,matched_routes=';'.join(sorted(doi_routes[row['doi'].casefold()]))) for row in anchors])
    left,right=routes['METHOD_ONLY'],routes['COMPOUND_CLASS']
    write('EuropePMC_Route_Overlap.csv',[dict(method_keys=len(left),class_keys=len(right),shared_keys=len(left&right),
                                             method_only_keys=len(left-right),class_only_keys=len(right-left),
                                             union_keys=len(left|right))])
    discovered=sorted(right-left)
    linked={r['article_key'] for r in read(HERE/'Candidate_Article_Links.csv')}
    lookup={r['article_key']:r for r in articles}
    queue=[]
    for key in discovered:
        if key in linked or key not in lookup:continue
        row=lookup[key]
        queue.append(dict(article_key=key,doi=row['doi'],title=row['title'],
                          candidate_identity='',food_occurrence_source='',
                          status='PENDING_COMPOUND_EXTRACTION_IDENTITY_AND_FOOD_VERIFICATION'))
    write('Food_Compound_Discovery_Queue.csv',queue)
    print(dict(conflicts=dict(Counter(row['group_type'] for row in flags)),shared_routes=len(left&right),discovery_leads=len(queue)))

if __name__=='__main__':
    main()
