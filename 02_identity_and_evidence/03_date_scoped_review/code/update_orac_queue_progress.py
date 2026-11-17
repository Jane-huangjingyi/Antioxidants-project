"""Retain the fixed 109-source work cohort while the active queue contracts."""
import collections
import json
from reconcile_existing_work import HERE, SOURCE, read, write


def main():
    output = HERE / 'results/Original_ORAC_Source_Progress.csv'
    baseline = read(output) if output.exists() else read(HERE / 'results/Original_Capacity_Fulltext_Queue.csv')
    decisions = {row['doi']: row for row in read(HERE / 'results/Current_Scientific_Source_Decisions.csv')}
    locator_path=HERE/'results/Source_Locator_Refresh.csv'
    verified_locators={r['doi']:r['PMCID'] for r in read(locator_path) if r['locator_status']=='ORIGINAL_XML_DOI_VERIFIED'} if locator_path.exists() else {}
    rows = []
    for source in baseline:
        decision = decisions.get(source['doi'], {})
        source['PMCID']=verified_locators.get(source['doi'],source['PMCID'])
        local = bool(source['PMCID'] and (SOURCE / 'fulltext_xml' / (source['PMCID']+'.xml')).exists())
        status = ('TARGETED_SOURCE_SCOPE_RECORDED' if decision else
                  'LOCAL_XML_AWAITING_SCIENTIFIC_CHECK' if local else 'FULLTEXT_ACCESS_PENDING')
        rows.append(dict(article_key=source['article_key'], doi=source['doi'], PMCID=source['PMCID'],
                         title=source['title'], baseline_cohort='2026-11-16_109_SOURCE_WORK_QUEUE',
                         progress=status, recorded_reading_scope=decision.get('reading_scope', ''),
                         capacity_disposition=decision.get('capacity_model_disposition', ''),
                         reason=decision.get('reason', ''), supplement_status=decision.get('supplement_status', 'NOT_CHECKED'),
                         source_sha256=decision.get('source_sha256', ''),
                         final_article_eligibility='PENDING_RESEARCHER_ADJUDICATION',
                         human_review_status='NOT_REVIEWED', change_applied='NO'))
    assert len(rows) == 109 and len({row['article_key'] for row in rows}) == 109
    write(output, rows)
    summary = dict(baseline_sources=len(rows), status_counts=dict(collections.Counter(r['progress'] for r in rows)),
                   targeted_source_decisions_total=len(decisions), new_model_labels=0,
                   all_109_sources_completed=False, final_PRISMA_exclusions_established=False)
    (HERE / 'results/orac_queue_progress_summary.json').write_text(json.dumps(summary, indent=2)+'\n', encoding='utf8')
    print(json.dumps(summary))


if __name__ == '__main__':
    main()
