"""Search identity-backed candidate names and reviewed aliases without merging forms."""
import csv
import datetime as dt
from retrieve_pubmed import CACHE, ROOT, CUTOFF, METHOD, search, terms, write

def main():
    CACHE.mkdir(parents=True, exist_ok=True)
    source = ROOT/'02_identity_and_evidence/results/candidate_evidence_profiles.csv'
    with source.open(encoding='utf-8-sig',newline='') as handle:
        profiles = list(csv.DictReader(handle))
    queries, audit, links = [], [], []
    for row in profiles:
        cid = row['candidate_id']
        names = [row['compound_name']]
        if row['reference_name'] and row['pubchem_cid'] and row['inchi_key']:
            names.append(row['reference_name'])
        names = list(dict.fromkeys(names))
        query = terms(names) + ' AND ' + METHOD
        ids = search(cid,query,dt.date(2020,1,1),CUTOFF,audit)
        queries.append(dict(candidate_id=cid,terms=' | '.join(names),pubchem_cid=row['pubchem_cid'],
                            inchi_key=row['inchi_key'],hits=len(ids),review_status='PENDING_EXACT_MATERIAL_CHECK'))
        links.extend(dict(candidate_id=cid,PMID=pmid,association='QUERY_MATCH_ONLY',human_review_status='NOT_REVIEWED')
                     for pmid in sorted(ids,key=int))
        write('PubMed_Compound_Query_Status.csv',queries)
        write('PubMed_Compound_Search_Partitions.csv',audit)
        if links:
            write('PubMed_Compound_Hit_Links.csv',links)
    print('Compound queries completed',len(queries),flush=True)

if __name__=='__main__':
    main()
