"""Check newly indexed PMC locators against the DOI inside original article XML."""
import argparse
import hashlib
import html
import json
import re
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from reconcile_existing_work import HERE, SOURCE, read, write


def normalized_title(value):
    return re.sub(r'[^a-z0-9]', '', re.sub(r'<[^>]+>', '', html.unescape(value)).lower())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--fetch', action='store_true')
    args = parser.parse_args()
    progress = read(HERE/'results/Original_ORAC_Source_Progress.csv')
    cache = SOURCE/'inputs/ORAC_Pending_Core_Locator_Refresh.json'
    if not cache.exists():
        if not args.fetch:
            raise FileNotFoundError('Run with --fetch to retrieve the public core metadata.')
        query = ' OR '.join('DOI:'+r['doi'] for r in progress if r['progress']=='FULLTEXT_ACCESS_PENDING')
        url = 'https://www.ebi.ac.uk/europepmc/webservices/rest/search?' + urllib.parse.urlencode(
            dict(query='('+query+')', format='json', resultType='core', pageSize=100))
        with urllib.request.urlopen(url, timeout=45) as response:
            cache.write_bytes(response.read())
    data = json.loads(cache.read_bytes())
    assert data['hitCount'] <= 100, 'Metadata pagination required before accepting refresh.'
    core = data['resultList']['result']
    rows = []
    for record in core:
        if record.get('doi') or not record.get('pmcid'):
            continue
        matches = [r for r in progress if normalized_title(r['title']) == normalized_title(record['title'])]
        if len(matches) != 1:
            continue
        expected = matches[0]['doi'].lower()
        pmc = record['pmcid']
        path = SOURCE/'fulltext_xml'/(pmc+'.xml')
        url = 'https://www.ebi.ac.uk/europepmc/webservices/rest/'+pmc+'/fullTextXML'
        status, error, actual, digest = 'TITLE_MATCH_XML_DOI_CHECK_PENDING', '', '', ''
        try:
            if not path.exists() and args.fetch:
                with urllib.request.urlopen(url, timeout=35) as response:
                    raw = response.read()
                root = ET.fromstring(raw)
                actual = next(e.text.strip().lower() for e in root.findall('.//article-id')
                              if e.attrib.get('pub-id-type') == 'doi')
                assert actual == expected, (expected, actual)
                path.write_bytes(raw)
            if path.exists():
                root = ET.fromstring(path.read_bytes())
                actual = next(e.text.strip().lower() for e in root.findall('.//article-id')
                              if e.attrib.get('pub-id-type') == 'doi')
                assert actual == expected, (expected, actual)
                status = 'ORIGINAL_XML_DOI_VERIFIED'
                digest = hashlib.sha256(path.read_bytes()).hexdigest()
        except Exception as exc:
            status, error = 'FETCH_OR_IDENTIFIER_CHECK_FAILED', str(exc)
        rows.append(dict(article_key=matches[0]['article_key'], doi=expected, PMCID=pmc,
                         locator_status=status, original_xml_doi=actual, source_url=url,
                         source_file=path.relative_to(HERE.parents[1]).as_posix() if path.exists() else '',
                         source_sha256=digest, error=error,
                         metadata_sha256=hashlib.sha256(cache.read_bytes()).hexdigest(),
                         scientific_review_status='PENDING', human_review_status='NOT_REVIEWED', change_applied='NO'))
    if rows:
        write('Source_Locator_Refresh.csv', rows)
    print(json.dumps(dict(title_matches=len(rows), verified=sum(r['locator_status']=='ORIGINAL_XML_DOI_VERIFIED' for r in rows))))


if __name__=='__main__':
    main()
