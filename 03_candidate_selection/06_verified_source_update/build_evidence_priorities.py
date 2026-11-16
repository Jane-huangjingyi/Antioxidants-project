"""Join existing model sensitivities to source-level evidence for targeted retrieval.

This report adds no activity labels and introduces no fitted parameters.
Run after fit_verified_source_diagnostics.py from any working directory.
"""
from pathlib import Path
import csv
import json

HERE = Path(__file__).resolve().parent
OUT = HERE / 'results'
VARIANT = 'EXTENDED_CONFLICT_EXCLUDED'


def read(name):
    with (OUT / name).open(encoding='utf-8-sig', newline='') as handle:
        return list(csv.DictReader(handle))


def main():
    estimates = [r for r in read('Candidate_Model_Estimates.csv') if r['variant'] == VARIANT]
    selected = [r for r in estimates if r['model'] == 'SHRINK_10_EQUAL_ROW']
    deletions = [r for r in read('Source_Deletion_Order_Sensitivity.csv') if r['variant'] == VARIANT]
    evidence = [r for r in read('Analysis_Data_and_Dispositions.csv')
                if r['extended_conflict_excluded_diagnostic'] == 'YES']
    rows = []
    for candidate in sorted(selected, key=lambda r: int(r['diagnostic_component_order'])):
        cid = candidate['candidate_id']
        records = [r for r in evidence if r['candidate_id'] == cid]
        omitted = [r for r in deletions if r['candidate_id'] == cid]
        weighting = [r for r in estimates if r['candidate_id'] == cid and r['model'].startswith('SHRINK_10')]
        rank = int(candidate['diagnostic_component_order'])
        best = min([rank] + [int(r['fixed_universe_best_possible_order']) for r in omitted])
        worst = max([rank] + [int(r['fixed_universe_worst_possible_order']) for r in omitted])
        sources = sorted({r['doi'] for r in records})
        rows.append(dict(
            candidate_id=cid, compound=candidate['compound'], diagnostic_position=rank,
            conditional_geometric_location=candidate['conditional_geometric_location'],
            source_DOIs=len(sources), source_doi_list=';'.join(sources),
            single_source='YES' if len(sources) == 1 else 'NO',
            deletion_best_possible_position=best, deletion_worst_possible_position=worst,
            deletion_crosses_top20='YES' if best <= 20 < worst else 'NO',
            shrinkage_weighting_best_position=min(int(r['diagnostic_component_order']) for r in weighting),
            shrinkage_weighting_worst_position=max(int(r['diagnostic_component_order']) for r in weighting),
            missing_pH_rows=sum(not r['pH'] for r in records),
            missing_reported_error_rows=sum(not r['reported_error'] for r in records),
            source_locators=' | '.join(r['doi'] + ': ' + r['numeric_locator'] for r in records),
            followup_action=('RECOVER_ADDITIONAL_INDEPENDENT_ORAC_SOURCE' if len(sources) == 1
                             else 'RESOLVE_PROTOCOL_AND_EXACT_MATERIAL_ALIGNMENT'),
            sensitivity_scope='FIXED_41_CANDIDATE_UNIVERSE_NO_SAMPLING_INTERVAL',
            human_review_status='NOT_REVIEWED', change_applied='NO',
        ))
    assert len(rows) == 41 and len({r['candidate_id'] for r in rows}) == 41
    with (OUT / 'Candidate_Evidence_and_Stability.csv').open('w', encoding='utf8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)
    top = [r for r in rows if r['diagnostic_position'] <= 20]
    summary = dict(candidates=len(rows), top20_single_source=sum(r['single_source']=='YES' for r in top),
                   top20_deletion_crosses_cutoff=sum(r['deletion_crosses_top20']=='YES' for r in top),
                   all_single_source=sum(r['single_source']=='YES' for r in rows),
                   robust_top20_under_recorded_deletions=[r['compound'] for r in rows if r['deletion_worst_possible_position']<=20],
                   scope='DESCRIPTIVE_EXISTING_MODEL_SENSITIVITY_NO_NEW_FIT',
                   model_tuned=False, human_review_status='NOT_REVIEWED', change_applied='NO')
    (OUT / 'evidence_stability_summary.json').write_text(json.dumps(summary, indent=2)+'\n', encoding='utf8')
    paragraphs = ['# Candidate evidence and stability\n',
        'The current 41-candidate conflict-excluded diagnostic is joined to original-source locators, '
        'DOI counts, source-deletion identification bounds and equal-row versus equal-total-DOI shrinkage positions. '
        'Activity estimates and fitting settings are inherited from the recorded model.\n',
        f"Of the 20 leading diagnostic positions, {summary['top20_single_source']} rely on one DOI and "
        f"{summary['top20_deletion_crosses_cutoff']} have a source-deletion bound crossing position 20. "
        f"Across all candidates, {summary['all_single_source']} have one source DOI.\n",
        'Candidates whose worst possible position stays within 20 across the recorded whole-paper deletions are '
        + ', '.join(summary['robust_top20_under_recorded_deletions']) + '. '
        'This conclusion is conditional on the fixed candidate set and the fitted source-block model. '
        'Sampling uncertainty, compound-specific protocol effects and unseen candidates require additional evidence.\n',
        'Source-deletion bounds include non-estimable comparisons. The source DOI is the independence unit. '
        'Technical replicates and multiple rows within a paper do not add independent studies. '
        'Empty errors and missing pH are reported explicitly. No IF or sampling-precision score is assigned.\n',
        'Reproduce after model fitting with `python 03_candidate_selection/06_verified_source_update/build_evidence_priorities.py`. '
        'Inspect [the joined table](results/Candidate_Evidence_and_Stability.csv).\n']
    (HERE / 'Evidence_Stability_Assessment.md').write_text('\n'.join(paragraphs), encoding='utf8')
    print(json.dumps(summary))


if __name__ == '__main__':
    main()
