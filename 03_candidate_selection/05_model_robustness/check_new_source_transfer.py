"""Compare fixed existing estimates with newly extracted, unresolved source rows.

These are descriptive cross-protocol stress checks. Source rows never enter
training or hyperparameter selection in this script.
"""
from pathlib import Path
import collections
import csv
import hashlib
import itertools
import json
import math

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SUPPLEMENT = ROOT / '02_identity_and_evidence/01_systematic_supplement'


def read_csv(path):
    with path.open(encoding='utf-8-sig', newline='') as file:
        return list(csv.DictReader(file))


def write_csv(path, rows):
    with path.open('w', encoding='utf8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]), lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)


def run():
    model_path = HERE / 'results/Selected_Model_Component_Order.csv'
    source_path = SUPPLEMENT / 'Original_Capacity_Followup.csv'
    model = {row['candidate_id']: row for row in read_csv(model_path)}
    followup = read_csv(source_path)
    comparisons = []
    for row in followup:
        candidate = model.get(row['candidate_id'])
        capacity = row['conditional_molar_capacity']
        if not candidate or not capacity:
            continue
        observed = float(capacity)
        estimate = math.exp(float(candidate['selected_log_location']))
        comparisons.append(dict(
            candidate_id=row['candidate_id'], compound_name=row['compound_name'],
            new_source_doi=row['doi'], extraction_id=row['extraction_id'],
            prior_model='SHRINK_10_FIXED_PRE_SUPPLEMENT',
            prior_conditional_geometric_location=estimate,
            new_source_conditional_molar_capacity=observed,
            source_to_prior_ratio=observed / estimate,
            log_source_to_prior_ratio=math.log(observed) - math.log(estimate),
            pH=row['pH'], temperature_C=row['temperature_C'],
            unresolved=row['unresolved_fields'],
            interpretation='DESCRIPTIVE_CROSS_PROTOCOL_STRESS_CHECK',
            refitted_on_new_source='NO', validated_target_assay_performance='NO',
            human_review_status='NOT_REVIEWED', change_applied='NO',
        ))
    assert len(comparisons) == 6
    training_dois = {row['doi'] for row in read_csv(ROOT / '03_candidate_selection/03_preliminary_literature_selection/results/Paper_Specific_Reference_Order.csv')}
    assert not training_dois.intersection(row['new_source_doi'] for row in comparisons)
    write_csv(HERE / 'results/New_Source_Transfer_Check.csv', comparisons)
    pairs = []
    grouped = collections.defaultdict(list)
    for row in comparisons:
        grouped[row['new_source_doi']].append(row)
    for doi, rows in grouped.items():
        for first, second in itertools.combinations(rows, 2):
            observed = math.log(first['new_source_conditional_molar_capacity'] / second['new_source_conditional_molar_capacity'])
            predicted = math.log(first['prior_conditional_geometric_location'] / second['prior_conditional_geometric_location'])
            pairs.append(dict(
                doi=doi, first_candidate=first['candidate_id'], second_candidate=second['candidate_id'],
                observed_log_ratio=observed, fixed_model_log_ratio=predicted,
                direction_agreement='YES' if observed * predicted > 0 else 'NO_OR_TIE',
                interpretation='SHARED_PAPER_DEPENDENT_COMPARISONS_PROTOCOL_UNRESOLVED',
                human_review_status='NOT_REVIEWED', change_applied='NO',
            ))
    write_csv(HERE / 'results/New_Source_Within_Paper_Order.csv', pairs)
    profiles = read_csv(ROOT / '02_identity_and_evidence/results/candidate_evidence_profiles.csv')
    coverage = []
    for profile in profiles:
        cid = profile['candidate_id']
        extracted = [row for row in followup if row['candidate_id'] == cid]
        existing = model.get(cid, {})
        coverage.append(dict(
            candidate_id=cid, compound_name=profile['compound_name'],
            molecular_formula=profile['molecular_formula'],
            existing_component_estimate='YES' if existing else 'NO',
            existing_component_DOI_count=existing.get('source_DOI_count', ''),
            new_original_source_count=len({row['doi'] for row in extracted}),
            new_source_dois=';'.join(sorted({row['doi'] for row in extracted})),
            new_rows_with_unresolved_fields=len(extracted),
            new_primary_model_labels_released=0,
            human_review_status='NOT_REVIEWED', change_applied='NO',
        ))
    write_csv(HERE / 'results/Candidate_Expansion_Coverage.csv', coverage)
    nested = json.loads((HERE / 'results/nested_validation_summary.json').read_text(encoding='utf8'))
    robust = json.loads((HERE / 'results/robustness_summary.json').read_text(encoding='utf8'))
    summary = dict(
        status='SOURCE_EXPANSION_IN_PROGRESS_STABILITY_AND_REPRESENTATIVENESS_NOT_ESTABLISHED',
        indexed_candidates=len(profiles), existing_model_candidates=len(model),
        existing_model_coverage_fraction=len(model) / len(profiles),
        single_source_candidates=sum(int(row['source_DOI_count']) == 1 for row in model.values()),
        fixed_model_source_comparisons=len(comparisons), new_source_DOIs=len(grouped),
        within_paper_pairs=len(pairs), within_paper_direction_agreements=sum(row['direction_agreement'] == 'YES' for row in pairs),
        within_paper_comparison_DOIs=len({row['doi'] for row in pairs}),
        new_source_data_used_for_fitting=False, new_data_formally_compatible=False,
        existing_nested_RMSE=nested['metrics']['prediction']['RMSE'],
        existing_nested_baseline_RMSE=nested['metrics']['baseline']['RMSE'],
        stable_omission_pair_count=robust['pairs_stable_direction_every_omission'],
        total_existing_pair_count=robust['candidate_pairs'],
        model_sha256=hashlib.sha256(model_path.read_bytes()).hexdigest(),
        new_source_extraction_sha256=hashlib.sha256(source_path.read_bytes()).hexdigest(),
    )
    (HERE / 'results/new_source_transfer_summary.json').write_text(json.dumps(summary, indent=2) + '\n', encoding='utf8')
    report = f'''# Source expansion and model readiness

The original-source update in [Step 03.6](../06_verified_source_update/README.md) is the current assessment after researcher-supplied PDFs and the recovered 60-flavonoid table. The figures below describe the preceding fixed-model comparison and its original reference inputs.

The current model estimates {len(model)} of {len(profiles)} indexed candidates ({len(model) / len(profiles):.1%}). {summary['single_source_candidates']} model candidates have one contributing DOI. Food occurrence, exact form, protocol qualification and original-experiment independence remain candidate-specific requirements. Retrieval volume does not establish representation of chemical classes.

Nested leave-paper-out log RMSE is {summary['existing_nested_RMSE']:.4f}, compared with {summary['existing_nested_baseline_RMSE']:.4f} for the source-summary baseline. This modest difference supports retaining the baseline in future comparisons. Existing source-deletion checks preserve a direction for {summary['stable_omission_pair_count']} of {summary['total_existing_pair_count']} candidate pairs across every omission. These diagnostics do not establish a stable global Top20.

## Newly recovered source checks

Six mapped rows from three new DOIs can be compared numerically with fixed prior estimates. Their source units or direct molar ratios are preserved in the extraction. Missing protocol and material fields make these descriptive cross-condition checks. The four matched phenolic acids from one new paper give six dependent pair comparisons, with {summary['within_paper_direction_agreements']} agreeing directions. The unit of source replication here is one paper. Ratios to prior estimates expose magnitude differences without attributing their cause to intrinsic potency or model error.

The existing estimate is exp(log location), a conditional geometric location. Expected arithmetic molar capacity requires an adequately identified outcome distribution or a validated retransformation. That target distinction remains part of model development.

## Conditions for the next model update

Resolve exact chemical forms and dietary scope, recover original numeric endpoints and error definitions, assign experiment clusters across related reports, and document final pH, temperature, solvent and AUC rule. Evaluate a strict pH 7.4/37 C protocol-stratified analysis before broader sensitivity pooling. Keep repeated concentrations within a source rather than counting them as independent studies.

For qualified data, assess candidate-paper graph connectivity and estimability before fitting. Select tuning parameters inside study-level validation, then assess held-out papers and chemical groups. Compare capacity error, within-paper ordering, source-deletion sensitivity and cutoff membership across justified protocol/quality analyses. Report the actual changes as new sources arrive. Formal stability thresholds and a final Top20 have not been selected from these inspected results.

Article IF is bibliographic context. It does not substitute for assay compatibility, original-data provenance or experimental precision. Article-method quality can be represented through documented exclusions and sensitivity strata while quantitative bias/variance weights require a defensible measurement model.

Reproduce with `python 02_identity_and_evidence/01_systematic_supplement/extract_capacity_followup.py`, then `python 03_candidate_selection/05_model_robustness/check_new_source_transfer.py`. This script reads the existing selected estimates and never fits them to new source outcomes. All review states remain NOT_REVIEWED and change_applied=NO.
'''
    (HERE / 'Source_Expansion_and_Model_Readiness.md').write_text(report, encoding='utf8', newline='\n')
    print(json.dumps(summary))


if __name__ == '__main__':
    run()
