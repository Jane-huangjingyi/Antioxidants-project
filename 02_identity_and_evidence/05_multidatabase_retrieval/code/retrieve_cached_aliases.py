"""Retrieve additional PubChem CID-linked name terms as search leads."""
import csv
import datetime as dt
import json
import re
from retrieve_pubmed import CACHE, ROOT, CUTOFF, METHOD, search, terms, write

def main():
    source=ROOT/'02_identity_and_evidence/01_systematic_supplement/PubChem_Synonym_Records.json'
    by_cid={str(record['CID']):record.get('Synonym',[]) for batch in json.loads(source.read_bytes())['batches']
            for record in batch['records']}
    with (ROOT/'02_identity_and_evidence/result/table/candidate_evidence_profiles.csv').open(encoding='utf-8-sig') as handle:
        profiles=list(csv.DictReader(handle))
    audit, links, queries = [], [], []
    for row in profiles:
        standard={row['compound_name'].casefold(),row['reference_name'].casefold()}
        aliases=[]
        if row['inchi_key']:
            for synonym in by_cid.get(row['pubchem_cid'],[]):
                if synonym.casefold() in standard or synonym.casefold() in {x.casefold() for x in aliases}:
                    continue
                if not re.fullmatch(r"[A-Za-z()'+, /-][A-Za-z0-9()'+, /-]{5,59}",synonym):
                    continue
                if synonym.upper().startswith(('DTXSID','SCHEMBL','AKOS','NCGC','UNII','CHEMBL')):
                    continue
                aliases.append(synonym)
                if len(aliases)==3:break
        cid=row['candidate_id']
        ids=search(cid+'_ALIASES',terms(aliases)+' AND '+METHOD,dt.date(2020,1,1),CUTOFF,audit) if aliases else set()
        queries.append(dict(candidate_id=cid,pubchem_cid=row['pubchem_cid'],inchi_key=row['inchi_key'],
                            terms=' | '.join(aliases),hits=len(ids),status='QUERY_ONLY_CID_LINKED_ALIAS' if aliases else 'NO_ADDITIONAL_ALIAS_SELECTED'))
        links.extend(dict(candidate_id=cid,PMID=pmid,association='CID_LINKED_ALIAS_HIT_PENDING_EXACT_FORM') for pmid in sorted(ids,key=int))
        write('PubMed_CID_Alias_Query_Status.csv',queries)
        if audit:write('PubMed_CID_Alias_Search_Partitions.csv',audit)
        if links:write('PubMed_CID_Alias_Hit_Links.csv',links)

if __name__=='__main__':
    main()
