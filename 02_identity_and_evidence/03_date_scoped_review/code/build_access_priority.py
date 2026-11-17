"""Prepare institutional retrieval requests from the active scientific queue."""
from reconcile_existing_work import HERE, read, write

PRIORITY={
 '10.1016/j.bbadva.2021.100030':(1,'Individual standards including ascorbic acid; original Table1 and ORAC calculation'),
 '10.1016/j.foodchem.2025.146338':(2,'Eight pure carotenoid standards; original ORAC results,vehicle,probe and units'),
 '10.1080/14786419.2025.2493187':(3,'Main article and source data for FigureS5; resolve micromol versus mol denominator'),
}

def main():
    queue=read(HERE/'results/Original_Capacity_Fulltext_Queue.csv')
    lookup={r['doi']:r for r in queue}
    register=read(HERE/'results/Date_Scoped_Article_Register.csv')
    for r in register:
        if r['doi'] in PRIORITY:lookup.setdefault(r['doi'],r)
    rows=[]
    for doi,r in lookup.items():
        priority,need=PRIORITY.get(doi,(4,'Original methods,material identity,ORAC table or source data,units,uncertainty and supplementary files'))
        rows.append(dict(priority=priority,doi=doi,title=r['title'],source_url='https://doi.org/'+doi,
                         linked_candidates=r['linked_candidates'],requested_content=need,
                         request_role='INSTITUTIONAL_RETRIEVAL_REQUEST',eligibility='SCIENTIFIC_DECISION_PENDING',
                         human_review_status='NOT_REVIEWED',change_applied='NO'))
    rows.sort(key=lambda r:(r['priority'],r['doi']))
    assert len({r['doi'] for r in rows})==len(rows)
    assert all(d in {r['doi'] for r in rows} for d in PRIORITY)
    write('Fulltext_Access_Request_Priority.csv',rows)
    print('Access requests',len(rows),'priority originals',len(PRIORITY))

if __name__=='__main__':main()
