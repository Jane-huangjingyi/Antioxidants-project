"""Audit the requested minimum across all current candidates, without equating hits to evidence."""
from pathlib import Path
import csv
import collections
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def read(path):
    with path.open(encoding='utf-8-sig', newline='') as handle:
        return list(csv.DictReader(handle))


def write(name, rows):
    with (HERE / name).open('w', encoding='utf8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)


def main():
    profiles = read(ROOT / '02_identity_and_evidence/results/candidate_evidence_profiles.csv')
    articles = {r['article_key']: r for r in read(HERE / 'Master_Article_Register.csv')}
    links = collections.defaultdict(set)
    for row in read(HERE / 'Master_Candidate_Article_Links.csv'):
        links[row['candidate_id']].add(row['article_key'])
    extracted = read(HERE.parent / '02_user_supplied_sources/Original_Capacity_Extraction.csv')
    extracted += read(HERE / 'Original_Capacity_Followup.csv')
    verified = collections.defaultdict(set)
    for row in extracted:
        if row['candidate_id']:
            verified[row['candidate_id']].add(row['doi'])
    audits = []
    association_count = 0
    for profile in profiles:
        cid = profile['candidate_id']
        records = [articles[key] for key in links[cid] if key in articles]
        # Schedule source reading by explicit ORAC title, original-report metadata,
        # and access. No IF score or activity outcome enters scheduling.
        records.sort(key=lambda r: (
            not any(term in r['title'].lower() for term in ['orac', 'oxygen radical absorbance']),
            'review' in r['publication_types'].lower(), not bool(r['PMCID']), r['article_key']))
        association_count += len(records)
        audits.append(dict(candidate_id=cid, compound=profile['compound_name'],
                           minimum_requested=20, provisional_linked_articles=len(records),
                           original_numeric_source_DOIs=len(verified[cid]),
                           numeric_source_gap_to_20=max(0, 20-len(verified[cid])),
                           fewer_than_20_studies_established='NO',
                           coverage_status='RELEVANCE_AND_EVIDENCE_SCREENING_REQUIRED',
                           scope='ALL_193_CURRENT_PROFILES',
                           human_review_status='NOT_REVIEWED', change_applied='NO'))
    assert len(audits) == 193 and len({r['candidate_id'] for r in audits}) == 193
    write('Minimum20_Candidate_Coverage.csv', audits)
    summary = dict(candidates=193, linked_article_associations=association_count,
                   candidates_with_20_provisional_links=sum(r['provisional_linked_articles']>=20 for r in audits),
                   candidates_with_20_numeric_source_DOIs=sum(r['original_numeric_source_DOIs']>=20 for r in audits),
                   scarcity_exceptions_established=0, requirements_fulfilled=False)
    (HERE / 'minimum20_summary.json').write_text(json.dumps(summary, indent=2)+'\n', encoding='utf8')
    print(json.dumps(summary))


if __name__ == '__main__':
    main()
