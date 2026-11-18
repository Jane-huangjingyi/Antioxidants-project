"""Separate public DOI indexing controls from retrieval-route recall."""
import hashlib
import json
from urllib.parse import urlencode
from urllib.request import urlopen

from audit_pubmed_export import read
from retrieve_pubmed import CACHE, HERE, cached_request, write

CONTROLS = {
    '10.1155/2020/4150897': 'PRIMARY_ORAC_FLAVONOID_PANEL',
    '10.1080/14786419.2025.2493187': 'PRIMARY_ORAC_ISOLATED_COMPOUNDS',
    '10.1016/j.bbadva.2021.100030': 'PREVIOUS_SOURCE_WORKLIST',
    '10.1016/j.foodchem.2025.146338': 'PREVIOUS_SOURCE_WORKLIST',
    '10.7506/spkx1002-6630-20200901-012': 'CHINESE_PRIMARY_ORAC_METHOD_CONTROL',
}


def main():
    CACHE.mkdir(parents=True, exist_ok=True)
    pubmed = {row['PMID']: row['routes'] for row in read(HERE / 'PubMed_Route_PMIDs.csv')}
    europe = {doi: set() for doi in CONTROLS}
    for row in read(HERE / 'Public_Article_Search_Origins.csv'):
        key = row['article_key']
        if key.startswith('DOI:') and key[4:] in europe:
            europe[key[4:]].add(row['route'])

    rows = []
    for doi, role in CONTROLS.items():
        stem = 'control_' + doi.replace('/', '_')
        pub_query = f'"{doi}"[AID]'
        pub_raw = cached_request(stem + '_pubmed.json', 'esearch', term=pub_query,
                                 retmode='json', retmax=20)
        pub_result = json.loads(pub_raw)['esearchresult']
        pmids = pub_result['idlist']
        epmc_query = f'DOI:"{doi}"'
        epmc_file = CACHE / (stem + '_epmc.json')
        if not epmc_file.exists():
            url = 'https://www.ebi.ac.uk/europepmc/webservices/rest/search?' + urlencode(
                dict(query=epmc_query, format='json', resultType='lite', pageSize=20))
            with urlopen(url, timeout=35) as response:
                epmc_file.write_bytes(response.read())
        epmc_raw = epmc_file.read_bytes()
        epmc_result = json.loads(epmc_raw)
        epmc_records = epmc_result['resultList']['result']
        rows.append(dict(
            doi=doi, control_role=role, pubmed_doi_query=pub_query,
            pubmed_doi_lookup_hits=pub_result['count'], pubmed_lookup_pmids=';'.join(pmids),
            pubmed_route_matches=';'.join(sorted({route for pmid in pmids if pmid in pubmed
                                                  for route in pubmed[pmid].split(';')})),
            epmc_doi_query=epmc_query, epmc_doi_lookup_hits=epmc_result['hitCount'],
            epmc_lookup_ids=';'.join(sorted(f"{r['source']}:{r['id']}" for r in epmc_records)),
            epmc_snapshot_route_matches=';'.join(sorted(europe[doi])),
            pubmed_response_sha256=hashlib.sha256(pub_raw).hexdigest(),
            epmc_response_sha256=hashlib.sha256(epmc_raw).hexdigest(),
            human_review_status='NOT_REVIEWED'))
    write('Public_Database_DOI_Controls.csv', rows)


if __name__ == '__main__':
    main()
