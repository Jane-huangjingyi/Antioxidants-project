"""Register institutional files in the ignored local intake directory."""
import csv
from collections import Counter, defaultdict
import json
import hashlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
INTAKE = ROOT/'download_raw/stage2_institutional'

def decode(raw):
    for encoding in ('utf-8-sig','gb18030'):
        try:
            return raw.decode(encoding)
        except UnicodeDecodeError:
            continue
    raise ValueError('Unknown export encoding')

def tagged(text, wos=False):
    record = {}
    field = ''
    for line in text.splitlines():
        tag = re.match(r'^([A-Z][A-Z0-9])(?:  - | )(.+)$',line)
        if wos and (not line.strip() or line.startswith(('FN ', 'VR '))):
            continue
        if line.strip() in ('ER','ER  -','EF') or not line.strip():
            if record:
                yield record
                record = {}
            field = ''
        elif tag:
            field, value = tag.groups()
            record[field] = ' | '.join(filter(None,(record.get(field,''),value.strip())))
        elif line.startswith('   ') and field:
            record[field] += ' ' + line.strip()
    if record:
        yield record

def normalize(record):
    def value(*keys):
        return next((record[key] for key in keys if record.get(key)), '')
    doi=value('DOI','DI','DO','M3').strip()
    doi=re.sub(r'^https?://(?:dx\.)?doi\.org/','',doi,flags=re.I).lower()
    if not doi.startswith('10.'):
        doi=''
    return dict(doi=doi,title=value('Title','TI','T1'),authors=value('Authors','AF','AU','A1'),
                journal=value('Source title','SO','JF','JO','T2'),issue_year=value('Year','PY','YR'),
                first_online=value('EA','Early Access Date'),issue_date=value('PD','Publication Date','Y1'),
                index_date='',abstract=value('Abstract','AB','N2'),references=value('References','CR','Cited References'),
                pmid=value('PubMed ID','PMID','PM'),accession=value('EID','UT','AN','ID'))

def main():
    rows, normalized = [], []
    for database in ('wos','scopus','cnki'):
        directory = INTAKE/database
        directory.mkdir(parents=True,exist_ok=True)
        for path in sorted(directory.iterdir()):
            if not path.is_file():
                continue
            raw=path.read_bytes()
            relative=path.relative_to(ROOT).as_posix()
            digest=hashlib.sha256(raw).hexdigest()
            status='REGISTERED_PENDING_FORMAT_AND_FIELD_VALIDATION'
            start=len(normalized)
            unparsed_records=0
            if path.suffix.lower() in ('.csv','.txt','.ris','.ref'):
                try:
                    content=decode(raw)
                except ValueError:
                    status='REGISTERED_ENCODING_REVIEW_PENDING'
                else:
                    records=csv.DictReader(content.splitlines(keepends=True)) if path.suffix.lower()=='.csv' else tagged(content,wos=database=='wos')
                    for index,record in enumerate(records,1):
                        fields=normalize(record)
                        if fields['title']:
                            normalized.append(dict(database=database,source_file=relative,source_sha256=digest,
                                                   source_record=index,**fields,review_status='PENDING_RECORD_AND_VERSION_REVIEW'))
                        elif 'FN' not in record:
                            unparsed_records+=1
                    if len(normalized)>start:
                        status='PARSED_PENDING_FIELD_AND_COVERAGE_VALIDATION'
            rows.append(dict(database=database,file=relative,bytes=len(raw),sha256=digest,
                             parsed_records=len(normalized)-start,unparsed_records=unparsed_records,status=status))
    fields=['database','file','bytes','sha256','parsed_records','unparsed_records','status']
    with (INTAKE/'Institutional_Local_File_Manifest.csv').open('w',encoding='utf8',newline='') as handle:
        writer=csv.DictWriter(handle,fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    if normalized:
        baseline=Path(__file__).resolve().parents[1]/'Deduplicated_Article_Register.csv'
        doi_index, pmid_index=defaultdict(set), defaultdict(set)
        with baseline.open(encoding='utf-8-sig',newline='') as handle:
            for entry in csv.DictReader(handle):
                if entry['doi']:
                    doi_index[entry['doi'].lower()].add(entry['article_key'])
                if entry['PMID']:
                    pmid_index[entry['PMID']].add(entry['article_key'])
        pubmed=baseline.with_name('PubMed_Identifier_Reconciliation.csv')
        if pubmed.exists():
            with pubmed.open(encoding='utf8',newline='') as handle:
                for entry in csv.DictReader(handle):
                    key=entry.get('provisional_report_key','')
                    if key:
                        pmid_index[entry['PMID']].add(key)
                        if entry['doi']:
                            doi_index[entry['doi']].add(key)
        versions=ROOT/'02_identity_and_evidence/03_date_scoped_review/results/Study_Version_Link_Register.csv'
        with versions.open(encoding='utf-8-sig',newline='') as handle:
            version_keys={r[field].lower():r['canonical_study_key'] for r in csv.DictReader(handle)
                          for field in ('preprint_doi','publication_doi') if r[field]}
        for record in normalized:
            doi=record['doi']
            matches=doi_index[doi] | pmid_index[record['pmid']]
            record['matched_baseline_keys']=';'.join(sorted(matches))
            record['report_group']='DOI:'+doi if doi else ''
            record['known_study_version_key']=version_keys.get(doi,'')
            if len(matches)>1:
                record['dedup_status']='IDENTIFIER_CONFLICT_PENDING'
            else:
                record['dedup_status']='DOI_GROUP_PENDING_CONFLICT_REVIEW' if doi else 'TITLE_AUTHOR_YEAR_REVIEW_PENDING'
        with (INTAKE/'Institutional_Normalized_Records.csv').open('w',encoding='utf8',newline='') as handle:
            writer=csv.DictWriter(handle,fieldnames=list(normalized[0]))
            writer.writeheader()
            writer.writerows(normalized)
    coverage=dict(files=len(rows),records=len(normalized),unparsed_records=sum(r['unparsed_records'] for r in rows),
                  database_records=dict(Counter(r['database'] for r in normalized)),
                  records_with_doi=sum(bool(r['doi']) for r in normalized),
                  records_with_abstract=sum(bool(r['abstract']) for r in normalized),
                  records_with_references=sum(bool(r['references']) for r in normalized),
                  distinct_doi_groups=len({r['doi'] for r in normalized if r['doi']}),
                  title_author_year_review_pending=True,coverage_complete=False)
    (INTAKE/'Institutional_Local_Coverage.json').write_text(json.dumps(coverage,indent=2),encoding='utf8')
    print('Institutional files registered:',len(rows),'parsed records:',len(normalized))

if __name__=='__main__':
    main()
