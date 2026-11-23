"""Reconcile original capacity extractions and validate the connected sensitivity set."""
from pathlib import Path
import csv
import json
import hashlib
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
SOURCE=ROOT/'02_identity_and_evidence/01_systematic_supplement'
PRIOR=ROOT/'03_candidate_selection/06_verified_source_update'
sys.path.insert(0,str(PRIOR))
import fit_verified_source_diagnostics as diagnostics


def read(path):
    with path.open(encoding='utf-8-sig',newline='') as handle:
        return list(csv.DictReader(handle))


def write(path,rows):
    with path.open('w',encoding='utf8',newline='') as handle:
        writer=csv.DictWriter(handle,fieldnames=list(rows[0]),lineterminator='\n')
        writer.writeheader();writer.writerows(rows)


def main():
    orders=read(ROOT/'03_candidate_selection/07_all_reference_integration/Expanded_Conditional_Component_Orders.csv')
    connected={r['candidate_id'] for r in orders if r['component']=='1'}
    base=read(PRIOR/'results/Analysis_Data_and_Dispositions.csv')
    rows=[r for r in base if r['extended_conflict_excluded_diagnostic']=='YES'
          and r['doi']!='10.3390/antiox12020505']
    extra=read(SOURCE/'Original_Capacity_Followup.csv')
    bridge=HERE/'Reviewed_Bridge_Capacity_Rows.csv'
    if bridge.exists():extra+=read(bridge)
    citrus=HERE/'Reviewed_Citrus_Capacity_Rows.csv'
    if citrus.exists():extra+=read(citrus)
    reconciliation=HERE/'Historical_Parent_Name_Reconciliation.csv'
    if reconciliation.exists():extra+=read(reconciliation)
    for r in extra:
        if r['candidate_id'] not in connected or not r['conditional_molar_capacity']:
            continue
        row={field:'' for field in rows[0]}
        row.update(evidence_id=r['extraction_id'],candidate_id=r['candidate_id'],doi=r['doi'],
                   source_compound_name=r['compound_name'],mean=r['conditional_molar_capacity'],
                   reported_error=r['conditional_molar_error'],error_type=r['error_type'],
                   pH=r['pH'],temperature_C=r['temperature_C'],
                   source_block=r['doi']+'|'+r.get('protocol_stratum','ADDITIONAL_CROSS_PROTOCOL'),
                   numeric_locator=r['source_locator'],source_document=(r['source_file'] if r.get('source_path_relative_to')=='PROJECT_ROOT' else str(SOURCE.relative_to(ROOT)/r['source_file'])),
                   source_sha256=r['source_sha256'],human_review_status='NOT_REVIEWED',change_applied='NO')
        rows.append(row)
    # Reuse the prior model runner, which adds its five original 2023 rows once.
    for r in rows:
        r['assay']='ORAC_FL'
        r['source_row']=r['evidence_id']
        r['protocol_stratum']=r['source_block'].split('|',1)[1]
    path=HERE/'Connected_Conditional_Analysis_Input.csv'
    write(path,rows)
    diagnostics.HERE=HERE
    diagnostics.OUT=HERE/'results'
    diagnostics.EXTRACTIONS=path
    diagnostics.run()
    profiles=read(ROOT/'02_identity_and_evidence/result/table/candidate_evidence_profiles.csv')
    links=read(SOURCE/'Minimum20_Combined_Progress.csv')
    link_lookup={r['candidate_id']:r for r in links}
    original=read(ROOT/'02_identity_and_evidence/02_user_supplied_sources/Original_Capacity_Extraction.csv')
    audit=[]
    for r in original:
        audit.append(dict(candidate_id=r['candidate_id'],doi=r['doi'],evidence_id=r['evidence_id'],
                          compound=r['source_compound_name'],raw_mean=r['mean'],raw_error=r['reported_error'],
                          raw_units=r['raw_units'],error_definition=r['error_type'],
                          material_identity=r['identity_mapping'],pH=r['pH'],temperature_C=r['temperature_C'],
                          protocol=r['protocol_stratum'],independent_n=r['independent_n_for_weighting'],
                          experiment_cluster=r['source_experiment_cluster'],locator=r['numeric_locator'],
                          disposition='OTHER_PROBE_ENDPOINT' if r['assay']!='ORAC_FL' else 'ORIGINAL_FL_CONDITIONAL_QUALIFICATION',
                          unresolved=r['source_conflict_flags']+'; '+r['unresolved'],
                          human_review_status='NOT_REVIEWED',change_applied='NO'))
    for r in extra:
        audit.append(dict(candidate_id=r['candidate_id'],doi=r['doi'],evidence_id=r['extraction_id'],
                          compound=r['compound_name'],raw_mean=r['raw_mean'],raw_error=r['raw_error'],
                          raw_units=r['raw_units'],error_definition=r['error_type'],
                          material_identity=r['candidate_mapping'],pH=r['pH'],temperature_C=r['temperature_C'],
                          protocol=r['integration_rule'],independent_n=r['independent_n'],
                          experiment_cluster=r['source_experiment_cluster'],locator=r['source_locator'],
                          disposition='CONDITIONAL_MOLAR_VALUE' if r['conditional_molar_capacity'] else 'UNIT_OR_COLUMN_CONFLICT_HOLD',
                          unresolved=r['unresolved_fields'],human_review_status='NOT_REVIEWED',change_applied='NO'))
    for r in base:
        if r['doi']!='10.3390/antiox12020505':continue
        audit.append(dict(candidate_id=r['candidate_id'],doi=r['doi'],evidence_id=r['evidence_id'],
                          compound=r['source_compound_name'],raw_mean=r['mean'],raw_error=r['reported_error'],
                          raw_units='reported molar capacity ratio',error_definition=r['error_type'],
                          material_identity='Named parent; source form unresolved',pH=r['pH'],temperature_C=r['temperature_C'],
                          protocol=r['source_block'],independent_n='',experiment_cluster=r['doi'],locator=r['numeric_locator'],
                          disposition='ORIGINAL_FL_CONDITIONAL_QUALIFICATION',
                          unresolved='Material form; uncertainty hierarchy; matched solvent block qualification',
                          human_review_status='NOT_REVIEWED',change_applied='NO'))
    # Fresh methods/Table 3 review distinguishes fitted kinetics from the AUC response.
    by_name={r['compound_name'].lower():r['candidate_id'] for r in profiles}
    for name,mean,error in [('p-Coumaric acid',4,.4),('Ferulic acid',3.3,.2),
                            ('Sinapic acid',2,.1),('Caffeic acid',3.9,.1),('Chlorogenic acid',3.8,.1)]:
        audit.append(dict(candidate_id=by_name[name.lower()],doi='10.3390/antiox13020222',
                          evidence_id='KIN2024-'+name,compound=name,raw_mean=mean,raw_error=error,
                          raw_units='AUC(AH)/AUC(Trolox)',error_definition='COLUMN_SPECIFIC_ERROR_HIERARCHY_UNRESOLVED',
                          material_identity='Named antioxidant; exact form/catalogue unresolved',pH=7.0,temperature_C=37,
                          protocol='120-minute fluorescence; 2.5 micromolar AH; methanol stock',independent_n='',
                          experiment_cluster='10.3390/antiox13020222',locator='PMC10886186 Table3; sections2.1-2.4,2.13',
                          disposition='DISTINCT_AUC_ENDPOINT_HOLD',
                          unresolved='Relative AUC definition lacks explicit net-AUC subtraction; kinetic parameter ranges are fitted. Buffer reported as 75mM and 0.1M in different sections. Final methanol and material identity unresolved.',
                          human_review_status='NOT_REVIEWED',change_applied='NO'))
    # Parent-name overlays replace the audit representation of the same source row.
    audit=list({r['evidence_id']:r for r in audit}.values())
    provenance={r['evidence_id']:(r['source_document'],r['source_sha256']) for r in original+base}
    provenance.update({r['extraction_id']:((r['source_file'] if r.get('source_path_relative_to')=='PROJECT_ROOT' else str(SOURCE.relative_to(ROOT)/r['source_file'])),r['source_sha256']) for r in extra})
    kinetic_file=SOURCE/'fulltext_xml/PMC10886186.xml'
    for r in audit:
        if r['evidence_id'].startswith('KIN2024-'):
            r['source_document']=kinetic_file.relative_to(ROOT).as_posix()
            r['source_sha256']=hashlib.sha256(kinetic_file.read_bytes()).hexdigest()
            r['reading_scope']='TARGETED_XML_METHODS_AND_TABLE3_REVIEW'
        else:
            r['source_document'],r['source_sha256']=provenance[r['evidence_id']]
            r['reading_scope']='PRIOR_ORIGINAL_EXTRACTION_RECONCILIATION'
    write(HERE/'Capacity_Row_Review.csv',audit)
    integrated=read(ROOT/'03_candidate_selection/07_all_reference_integration/All_Candidate_Integration_Coverage.csv')
    integration={r['candidate_id']:r for r in integrated}
    coverage=[]
    for p in profiles:
        cid=p['candidate_id'];a=[r for r in audit if r['candidate_id']==cid]
        q=link_lookup[cid];i=integration[cid]
        coverage.append(dict(candidate_id=cid,compound=p['compound_name'],retrieved_linked_articles=i['all_reference_links_considered'],
                             abstract_or_body_located_leads=q['total_located_leads'],
                             source_row_audited_DOIs=len({r['doi'] for r in a}),
                             extracted_numeric_rows=len(a),
                             conditional_analysis_rows=i['numeric_rows'],conditional_analysis_DOIs=i['numeric_source_DOIs'],
                             connected_validation='YES' if cid in connected else 'NO',
                             unresolved_reasons=' | '.join(sorted({r['disposition'] for r in a})),
                             remaining_review='ARTICLE_RELEVANCE_INDEPENDENCE_MATERIAL_AND_PROTOCOL_QUALIFICATION',
                             human_review_status='NOT_REVIEWED',change_applied='NO'))
    write(HERE/'Candidate_Review_and_Inclusion_Progress.csv',coverage)
    estimates=read(HERE/'results/Candidate_Model_Estimates.csv')
    deletions=read(HERE/'results/Source_Deletion_Order_Sensitivity.csv')
    variant='EXTENDED_CONFLICT_EXCLUDED'
    selected=[r for r in estimates if r['variant']==variant and r['model']=='SHRINK_10_EQUAL_ROW']
    balanced={r['candidate_id']:r for r in estimates if r['variant']==variant and r['model']=='SHRINK_10_EQUAL_DOI_TOTAL'}
    sensitivity=[]
    for r in selected:
        omitted=[d for d in deletions if d['variant']==variant and d['candidate_id']==r['candidate_id']]
        sensitivity.append(dict(candidate_id=r['candidate_id'],compound=r['compound'],
                                full_fit_position=r['diagnostic_component_order'],source_DOIs=r['source_DOIs'],
                                equal_DOI_position=balanced[r['candidate_id']]['diagnostic_component_order'],
                                deletion_best_position=min([int(r['diagnostic_component_order'])]+[int(d['fixed_universe_best_possible_order']) for d in omitted]),
                                deletion_worst_position=max([int(r['diagnostic_component_order'])]+[int(d['fixed_universe_worst_possible_order']) for d in omitted]),
                                interpretation='SOURCE_DELETION_IDENTIFICATION_BOUNDS_SAMPLING_COVERAGE_UNESTIMATED'))
    write(HERE/'Top20_Conditional_Uncertainty.csv',sensitivity)
    connected_data=read(HERE/'results/Analysis_Data_and_Dispositions.csv')
    connected_data=[r for r in connected_data if r['extended_conflict_excluded_diagnostic']=='YES']
    candidate_ids=sorted({r['candidate_id'] for r in connected_data})
    dose_results=[]
    dose_top={}
    for dose in ['2.5','5']:
        selected_data=[r for r in connected_data if r['doi']!='10.3390/antiox11091784'
                       or r['source_block'].endswith('DOSE_'+dose+'_UM')]
        for weighting in ['EQUAL_ROW','EQUAL_DOI_TOTAL']:
            beta,_=diagnostics.fit(selected_data,candidate_ids,'SHRINK_10',weighting)
            ordered=sorted(range(len(candidate_ids)),key=lambda i:-beta[i])
            dose_top[(dose,weighting)]={candidate_ids[i] for i in ordered[:20]}
            for position,index in enumerate(ordered,1):
                dose_results.append(dict(reported_dose_uM=dose,weighting=weighting,candidate_id=candidate_ids[index],
                                         compound=next(r['compound_name'] for r in profiles if r['candidate_id']==candidate_ids[index]),
                                         within_set_position=position,conditional_log_location=float(beta[index]),
                                         interpretation='SINGLE_REPORTED_DOSE_CROSS_PROTOCOL_SENSITIVITY'))
    write(HERE/'Protocol_Dose_Sensitivity.csv',dose_results)
    row_top={r['candidate_id'] for r in sensitivity if int(r['full_fit_position'])<=20}
    doi_top={r['candidate_id'] for r in sensitivity if int(r['equal_DOI_position'])<=20}
    review_summary=dict(audited_numeric_rows=len(audit),audited_original_DOIs=len({r['doi'] for r in audit}),
                        fresh_kinetic_endpoint_rows_held=5,review_progress_candidates=len(coverage),
                        connected_candidates=len(selected),weighting_top20_overlap=len(row_top&doi_top),
                        deletion_robust_top20=[r['compound'] for r in sensitivity if r['deletion_worst_position']<=20],
                        baseline_input_already_conflict_excluded=True,
                        formal_sampling_intervals_estimated=False,formal_top20_finalized=False)
    review_summary['dose_top20_overlap_equal_row']=len(dose_top[('2.5','EQUAL_ROW')]&dose_top[('5','EQUAL_ROW')])
    review_summary['dose_top20_overlap_equal_DOI']=len(dose_top[('2.5','EQUAL_DOI_TOTAL')]&dose_top[('5','EQUAL_DOI_TOTAL')])
    (HERE/'review_validation_summary.json').write_text(json.dumps(review_summary,indent=2)+'\n',encoding='utf8')
    print(json.dumps(review_summary))
    print('Original extraction audit and all-193 review/inclusion progress generated.')


if __name__=='__main__':
    main()
