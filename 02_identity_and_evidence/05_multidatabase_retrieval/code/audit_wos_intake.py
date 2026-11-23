"""Audit WoS raw exports and identifier links. All results stay in local intake."""
import csv
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from intake_institutional import INTAKE, ROOT
from audit_identifiers import title_key

HERE = Path(__file__).resolve().parents[1]


def read(path):
    with path.open(encoding='utf-8-sig', newline='') as handle:
        return list(csv.DictReader(handle))


def index(records, doi_field, pmid_field):
    result = defaultdict(list)
    for row in records:
        for kind, field in (('DOI', doi_field), ('PMID', pmid_field)):
            if row[field]:
                result[kind, row[field].strip().lower()].append(row)
    return result


def matches(indexed, row, key):
    return {other[key]: other for kind, field in (('DOI', 'doi'), ('PMID', 'pmid'))
            for other in indexed.get((kind, row[field]), [])}


def audit_file(batch, rows):
    raw = (ROOT / batch['file']).read_bytes()
    assert hashlib.sha256(raw).hexdigest() == batch['sha256']
    lines = raw.decode('utf-8-sig').splitlines()
    chunks = re.split(r'(?m)^ER\s*$', '\n'.join(lines))
    assert len(chunks) - 1 == len(rows) and chunks[-1].strip() == 'EF'
    tags = Counter()
    years = Counter()
    reference_mismatches = 0
    reference_lines = 0
    for chunk in chunks[:-1]:
        tags.update(set(re.findall(r'(?m)^(?!FN |VR )([A-Z][A-Z0-9]) \S', chunk)))
        year = re.search(r'(?m)^PY (\d{4})\s*$', chunk)
        years[year[1] if year else 'missing'] += 1
        block = re.search(r'(?m)^CR [^\n]*(?:\n   [^\n]*)*', chunk)
        listed = len(block.group().splitlines()) if block else 0
        reference_lines += listed
        declared = re.search(r'(?m)^NR (\d+)', chunk)
        reference_mismatches += declared is None or int(declared[1]) != listed
    return dict(file=batch['file'], sha256=batch['sha256'], bytes=int(batch['bytes']),
                encoding='UTF-8 with BOM' if raw.startswith(b'\xef\xbb\xbf') else 'UTF-8',
                LF_count=raw.count(b'\n'), CRLF_count=raw.count(b'\r\n'),
                end_record_count=len(rows), field_presence=dict(sorted(tags.items())), issue_year_counts=years,
                reference_lines=reference_lines,
                reference_count_mismatches=reference_mismatches)


def main():
    manifest = [r for r in read(INTAKE / 'Institutional_Local_File_Manifest.csv') if r['database'] == 'wos']
    rows = [r for r in read(INTAKE / 'Institutional_Normalized_Records.csv') if r['database'] == 'wos']
    baseline = read(HERE / 'Deduplicated_Article_Register.csv')
    pubmed = read(HERE / 'PubMed_Identifier_Reconciliation.csv')
    baseline_index = index(baseline, 'doi', 'PMID')
    pubmed_index = index(pubmed, 'doi', 'PMID')
    titles = defaultdict(set)
    for entry in baseline:
        title = title_key(entry['title'])
        if len(title) >= 24:
            titles[title].add(entry['article_key'])
    figures = Counter()
    accessions = Counter(r['accession'] for r in rows)
    dois = Counter(r['doi'] for r in rows if r['doi'])
    report = []
    for row in rows:
        sources = matches(baseline_index, row, 'article_key')
        public = matches(pubmed_index, row, 'PMID')
        europe = any('EUROPE_PMC_V11' in r['database_origins'].split(';') for r in sources.values())
        legacy = any('LEGACY_MASTER' in r['database_origins'].split(';') for r in sources.values())
        for label, flag in [('PubMed', bool(public)), ('Europe_PMC', europe), ('legacy', legacy),
                            ('any_identifier_hit', bool(sources or public))]:
            figures[label] += flag
        linked_keys = set(sources) | {r['provisional_report_key'] for r in public.values()
                                      if r['provisional_report_key']}
        conflicting = len(linked_keys) > 1 or len(public) > 1 or any(
            r['doi'] and row['doi'] and r['doi'].lower() != row['doi'] or
            r['PMID'] and row['pmid'] and r['PMID'] != row['pmid']
            for r in [*sources.values(), *public.values()])
        title_flags = titles.get(title_key(row['title']), set()) - linked_keys
        held = conflicting or (bool(public) and any(not r['provisional_report_key'] for r in public.values()))
        if held:
            outcome = 'IDENTIFIER_REVIEW_PENDING'
        elif linked_keys:
            outcome = 'EXISTING_REPORT_KEY_LINK'
        elif title_flags:
            outcome = 'TITLE_REVIEW_PENDING'
        else:
            outcome = 'ADDITIONAL_PROVISIONAL_WOS_KEY'
        figures[outcome] += 1
        report.append(dict(accession=row['accession'], doi=row['doi'], pmid=row['pmid'],
                           source_file=row['source_file'], source_record=row['source_record'],
                           pubmed_pmids=';'.join(sorted(public)), europe_pmc_identifier_hit=europe,
                           legacy_identifier_hit=legacy, matched_keys=';'.join(sorted(linked_keys)),
                           title_review_keys=';'.join(sorted(title_flags)), status=outcome,
                           human_review_status='NOT_REVIEWED'))
    with (INTAKE / 'WoS_Local_Reconciliation.csv').open('w', encoding='utf8', newline='') as handle:
        output = csv.DictWriter(handle, fieldnames=list(report[0]))
        output.writeheader()
        output.writerows(report)
    audit = dict(files=[audit_file(batch, [r for r in rows if r['source_file'] == batch['file']])
                        for batch in manifest], imported=len(rows), distinct_accessions=len(accessions),
                 invalid_accessions=sum(n for ut, n in accessions.items() if not re.fullmatch(r'WOS:\d+', ut)),
                 duplicate_accession_rows=sum(n-1 for n in accessions.values()),
                 distinct_dois=len(dois), duplicate_doi_rows=sum(n-1 for n in dois.values()),
                 normalized_presence={field: sum(bool(r[field]) for r in rows)
                                      for field in ('doi', 'pmid', 'abstract', 'references', 'known_study_version_key')},
                 reconciliation=figures, stage2_complete=False)
    (INTAKE / 'WoS_Local_QC.json').write_text(json.dumps(audit, indent=2), encoding='utf8')
    print(json.dumps(audit, indent=2))


if __name__ == '__main__':
    main()
