"""Check public checkpoint gates and expose PubMed query translation warnings."""
from collections import Counter
import hashlib
import json

from audit_pubmed_export import read
from retrieve_pubmed import CACHE, HERE, write


def main():
    warnings = []
    for filename in ('PubMed_Search_Partitions.csv', 'PubMed_Compound_Search_Partitions.csv',
                     'PubMed_CID_Alias_Search_Partitions.csv'):
        for row in read(HERE / filename):
            raw = (CACHE / row['raw_file']).read_bytes()
            assert hashlib.sha256(raw).hexdigest() == row['sha256'], row['raw_file']
            result = json.loads(raw)['esearchresult']
            assert int(result['count']) == len(set(result['idlist'])) == int(row['unique_pmids'])
            for field in ('warninglist', 'errorlist'):
                for code, messages in result.get(field, {}).items():
                    for message in messages:
                        warnings.append(dict(route=row['route'], source=row['raw_file'], field=field,
                                             code=code, message=message, status='QUERY_TERM_REVIEW_PENDING'))
    write('PubMed_Query_Warning_Review_Queue.csv', warnings)
    expected = {r['PMID'] for r in read(HERE / 'PubMed_Route_PMIDs.csv')}
    exported = read(HERE / 'PubMed_Identifier_Reconciliation.csv')
    assert len(exported) == len(expected) and {r['PMID'] for r in exported} == expected
    assert all(r['human_review_status'] == 'NOT_REVIEWED' and r['change_applied'] == 'NO' for r in exported)
    assert all(r['count_agreement'] == 'YES' for r in read(HERE / 'PubMed_Whole_Window_Count_Audit.csv'))
    audit = json.loads((HERE / 'PubMed_Export_Audit.json').read_bytes())
    assert audit['broad_export_complete'] and not audit['targeted_pmids_outside_broad_queries']
    assert not audit['stage2_complete']
    print('PubMed public export checkpoint QC PASS.', dict(Counter(r['code'] for r in warnings)))


if __name__ == '__main__':
    main()
