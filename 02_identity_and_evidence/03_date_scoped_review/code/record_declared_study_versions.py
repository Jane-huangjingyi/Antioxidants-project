"""Preserve publisher-declared preprint-to-publication links for study grouping."""
from reconcile_existing_work import write


def main():
    rows = []
    for preprint, publication, url in [
        ('10.20944/preprints202504.2326.v1', '10.3390/molecules30112354',
         'https://www.preprints.org/manuscript/202504.2326'),
        ('10.20944/preprints202307.1062.v1', '10.3390/foods12183401',
         'https://www.preprints.org/manuscript/202307.1062'),
    ]:
        rows.append(dict(preprint_doi=preprint, publication_doi=publication,
                         canonical_study_key='DOI:'+publication,
                         relationship='PUBLISHER_DECLARED_PEER_REVIEWED_VERSION',
                         source_url=url, checked_locator='Publisher page version/publication notice and linked article',
                         verification_scope='BROWSER_PUBLICATION_NOTICE;LOCAL_PREPRINT_PDF_FETCH_HTTP403',
                         numeric_table_equivalence='NOT_ASSESSED',
                         independence_rule='ONE_VERSION_FAMILY;DO_NOT_ADD_INDEPENDENT_STUDY_WEIGHT',
                         human_review_status='NOT_REVIEWED', change_applied='NO'))
    write('Study_Version_Link_Register.csv', rows)


if __name__=='__main__':
    main()
