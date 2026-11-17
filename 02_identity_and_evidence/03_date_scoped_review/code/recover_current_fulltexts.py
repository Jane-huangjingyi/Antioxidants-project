"""Recover only new in-window public original-capacity full-text candidates."""
import concurrent.futures
import json
import sys
from reconcile_existing_work import HERE, SOURCE, read, write
sys.path.insert(0,str(SOURCE))
from retrieve_compound_fulltexts import recover


def main():
    queue=read(HERE/'results/Original_Capacity_Fulltext_Queue.csv')
    selected=[r for r in queue if r['PMCID']]
    rows=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        for number,result in enumerate(pool.map(recover,selected),1):
            result.pop('title_priority',None)
            rows.append(result)
            if number%10==0:print('Sources processed',number,flush=True)
    inventory_path=HERE/'results/Current_Public_Fulltext_Recovery.csv'
    existing=read(inventory_path) if inventory_path.exists() else []
    inventory={r['article_key']:r for r in existing}
    inventory.update({r['article_key']:r for r in rows})
    if inventory:write('Current_Public_Fulltext_Recovery.csv',list(inventory.values()))
    summary=dict(queued_articles=len(queue),public_PMC_candidates=len(selected),
                 recovered=sum(r['fulltext_recovery']=='PUBLIC_XML_RECOVERED_PENDING_READING' for r in rows),
                 failed=sum(r['fulltext_recovery']=='PUBLIC_XML_FETCH_FAILED' for r in rows),
                 sources_without_PMClocator=len(queue)-len(selected),scientific_reading_complete=False,
                 cumulative_public_PMC_inventory=len(inventory),
                 cumulative_recovered=sum(r['fulltext_recovery']=='PUBLIC_XML_RECOVERED_PENDING_READING' for r in inventory.values()),
                 latest_attempted_sources=len(rows),inventory_scope='CUMULATIVE_SOURCE_SNAPSHOT;LATEST_QUEUE_COUNTS_SEPARATE')
    (HERE/'results/current_recovery_summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf8')
    print(json.dumps(summary),flush=True)


if __name__=='__main__':main()
