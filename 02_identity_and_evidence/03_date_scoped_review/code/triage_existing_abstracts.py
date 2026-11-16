"""Reuse cached abstracts for date-scoped capacity triage with explicit review scope."""
from pathlib import Path
import collections
import csv
import json
import re
from reconcile_existing_work import HERE, ROOT, SOURCE, read, write


def main():
    register=read(HERE/'results/Date_Scoped_Article_Register.csv')
    master=read(SOURCE/'Master_Article_Register.csv')
    types={r['article_key']:r['publication_types'] for r in master}
    abstract={}
    for r in read(SOURCE/'Minimum20_Abstract_Evidence_Packages.csv'):
        for key in [r['doi'],r['PMID']]:
            if key:abstract[key]=r
    rows,queue,missing_fields=[],[],[]
    for r in register:
        if r['in_current_review_scope']!='YES':continue
        cached=abstract.get(r['doi'],abstract.get(r['PMID'],{}))
        text=r['title']+' '+cached.get('abstract','')
        pubtypes=types.get(r['article_key'],'')
        orac=bool(re.search(r'\borac\b|oxygen radical absorbance',text,re.I))
        review=bool(re.search(r'\breview\b|meta.analysis',pubtypes,re.I))
        capacity=bool(re.search(r'capacity|scaveng|antioxidant activity',text,re.I))
        reused=r['existing_review_status'].startswith('REUSE')
        role='BACKGROUND_REFERENCE_TRACING' if review else 'ORAC_ORIGINALITY_AND_MATERIAL_CHECK' if orac else 'OTHER_ACTIVITY_OR_CAPACITY_CHECK' if capacity else 'RELEVANCE_AND_METHOD_SCAN_PENDING'
        row=dict(article_key=r['article_key'],doi=r['doi'],PMID=r['PMID'],PMCID=r['PMCID'],
                 title=r['title'],journal=r['journal'],period=r['period'],linked_candidates=r['linked_candidates'],
                 publication_types=pubtypes,abstract_available='YES' if cached else 'NO',
                 abstract_source_sha256=cached.get('source_sha256',''),
                 screening_scope='REUSE_PRIOR_RECORDED_SCIENTIFIC_SCOPE' if reused else 'AUTOMATED_CACHED_TITLE_ABSTRACT_TRIAGE' if cached else 'AUTOMATED_TITLE_ONLY_TRIAGE',
                 routing_role=role,previous_review_status=r['existing_review_status'],
                 recorded_reading_scope=r['recorded_reading_scope'],
                 final_eligibility='PENDING_ARTICLE_LEVEL_SCIENTIFIC_DECISION',
                 model_label_release='NO',human_review_status='NOT_REVIEWED',change_applied='NO')
        rows.append(row)
        if reused:
            missing_fields.append(dict(**row,next_reading='FILL_UNCHECKED_METHODS_SUPPLEMENTS_MATERIALS_AND_INDEPENDENCE_ONLY'))
        if orac and not review and not reused:
            path=SOURCE/'fulltext_xml'/(r['PMCID']+'.xml') if r['PMCID'] else None
            queue.append(dict(**row,source_recovery='REUSE_LOCAL_XML' if path and path.exists() else 'PUBLIC_XML_OR_INSTITUTION_SOURCE_REQUIRED',
                              next_reading='METHODS_MATERIALS_ORIGINAL_TABLES_SUPPLEMENTS_AND_DUPLICATES'))
    write('Date_Scoped_Title_Abstract_Triage.csv',rows)
    if queue:write('Original_Capacity_Fulltext_Queue.csv',queue)
    if missing_fields:write('Prior_Review_Missing_Field_Queue.csv',missing_fields)
    counts=collections.Counter(r['screening_scope'] for r in rows)
    summary=dict(in_scope_records=len(rows),reading_scopes=dict(counts),
                 original_ORAC_fulltext_candidates=len(queue),
                 local_xml_available=sum(r['source_recovery']=='REUSE_LOCAL_XML' for r in queue),
                 final_scientific_exclusions=0,new_model_labels=0,
                 final_PRISMA_screening_counts_established=False)
    (HERE/'results/triage_summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf8')
    print(json.dumps(summary))


if __name__=='__main__':main()
