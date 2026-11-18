"""Fetch targeted PubMed results outside the two broad routes."""
import csv
import hashlib
from retrieve_pubmed import HERE, export_records

def pmids(filename):
    with (HERE/filename).open(encoding='utf8',newline='') as handle:
        return {row['PMID'] for row in csv.DictReader(handle)}

def main():
    targeted = pmids('PubMed_Compound_Hit_Links.csv') | pmids('PubMed_CID_Alias_Hit_Links.csv')
    ids = sorted(targeted - pmids('PubMed_Route_PMIDs.csv'), key=int)
    print('Targeted-only PMIDs',len(ids),flush=True)
    if ids:
        fingerprint=hashlib.sha256(','.join(ids).encode()).hexdigest()[:16]
        export_records(ids,'targeted_'+fingerprint,'PubMed_Targeted_Only_Export_Manifest.csv')

if __name__=='__main__':
    main()
