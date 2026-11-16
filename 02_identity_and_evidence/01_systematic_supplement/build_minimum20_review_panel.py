"""Assemble source-located review panels and reconcile abstract/body coverage."""
from pathlib import Path
import collections
import csv
import json

HERE=Path(__file__).resolve().parent


def read(name):
    with (HERE/name).open(encoding='utf-8-sig',newline='') as handle:
        return list(csv.DictReader(handle))


def write(name,rows):
    with (HERE/name).open('w',encoding='utf8',newline='') as handle:
        writer=csv.DictWriter(handle,fieldnames=list(rows[0]),lineterminator='\n')
        writer.writeheader();writer.writerows(rows)


def main():
    abstract=read('Minimum20_Abstract_Evidence_Packages.csv')
    body=read('Minimum20_Body_Located_Leads.csv')
    coverage=read('Minimum20_Abstract_Coverage.csv')
    groups=collections.defaultdict(dict)
    for row in abstract+body:
        key=row['doi'] or row['PMID'] or row['title']
        groups[row['candidate_id']].setdefault(key,row)
    panel,progress=[],[]
    for candidate in coverage:
        cid=candidate['candidate_id']
        rows=list(groups[cid].values())
        rows.sort(key=lambda r:(
            r.get('evidence_role')!='ORAC_MENTION_REQUIRES_ORIGINAL_CAPACITY_CHECK',
            'review' in r.get('publication_types','').lower(),
            not bool(r.get('PMCID')),r['doi'] or r['PMID'] or r['title']))
        for order,row in enumerate(rows[:20],1):
            panel.append(dict(candidate_id=cid,compound=candidate['compound'],review_order=order,
                              doi=row['doi'],PMID=row['PMID'],PMCID=row['PMCID'],title=row['title'],
                              journal=row.get('journal',''),year=row['year'],
                              reading_scope=row['reading_scope'],
                              source_text=row.get('abstract',row.get('matched_paragraph','')),
                              paragraph_locator=row.get('paragraph_locator','ABSTRACT'),
                              original_capacity_check='PENDING',article_evidence_strength='NOT_APPRAISED',
                              manuscript_use='PENDING_SCIENTIFIC_RELEVANCE_AND_ENDPOINT_REVIEW',
                              source_url=row['source_url'],source_sha256=row['source_sha256'],
                              human_review_status='NOT_REVIEWED',change_applied='NO'))
        body_count=sum(r['candidate_id']==cid for r in body)
        progress.append(dict(candidate_id=cid,compound=candidate['compound'],
                             abstract_rule_articles=int(candidate['rule_screened_relevant_abstracts']),
                             additional_body_located_articles=body_count,total_located_leads=len(rows),
                             twenty_located_leads='YES' if len(rows)>=20 else 'NO',
                             scientifically_verified_twenty_papers='PENDING',model_label_release='NO',
                             scarcity_established='NO',human_review_status='NOT_REVIEWED',change_applied='NO'))
    assert len(progress)==193
    assert len({(r['candidate_id'],r['doi'] or r['PMID'] or r['title']) for r in panel})==len(panel)
    write('Minimum20_Review_Panel.csv',panel)
    write('Minimum20_Combined_Progress.csv',progress)
    summary=dict(candidates=193,abstract_target_reached=sum(r['abstract_rule_articles']>=20 for r in progress),
                 combined_located_target_reached=sum(r['twenty_located_leads']=='YES' for r in progress),
                 new_body_located_links=len(body),review_panel_rows=len(panel),
                 remaining_located_gaps=[dict(compound=r['compound'],located_leads=r['total_located_leads']) for r in progress if r['twenty_located_leads']=='NO'],
                 all_scientific_reviews_complete=False,scarcity_exceptions_established=0)
    (HERE/'minimum20_combined_summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf8')
    paragraphs=['# Minimum-20 evidence-package progress\n',
                f"Coverage is {summary['combined_located_target_reached']} of 193 compounds at the located-lead level. "
                f"Abstract screening reaches 20 for {summary['abstract_target_reached']}; body follow-up adds {len(body)} compound/article links. "
                f"The next-reading panel contains {len(panel)} rows.\n",
                'The panel schedules at most 20 papers per candidate from all retained leads, prioritizing explicit ORAC mentions, '
                'publication metadata without a review label, and public full-text availability. DOI/PMID/title keys resolve exact duplicates. '
                'All additional records remain in the full packages. Article quality, independence and chemical form require scientific appraisal.\n',
                'Remaining located gaps are '+json.dumps(summary['remaining_located_gaps'])+'. '
                'No cross-database scarcity exception has been established. Probetanin also requires identity/formula resolution.\n',
                'Start with [combined coverage](Minimum20_Combined_Progress.csv), '
                '[the next-reading panel](Minimum20_Review_Panel.csv), and '
                '[located body paragraphs](Minimum20_Body_Located_Leads.csv). '
                'Reproduce with `python 02_identity_and_evidence/01_systematic_supplement/build_minimum20_review_panel.py`.\n']
    (HERE/'Minimum20_Progress.md').write_text('\n'.join(paragraphs),encoding='utf8')
    print(json.dumps(summary))


if __name__=='__main__':
    main()
