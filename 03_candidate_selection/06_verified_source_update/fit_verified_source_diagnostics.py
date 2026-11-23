"""Refit descriptive models from original-source extractions and explicit strata.

Fixed lambda=10 reuses the prior exploratory setting. No new tuning is done.
All available outcome means are positive. Missing sampling variances remain absent.
"""
from pathlib import Path
import collections
import csv
import hashlib
import json
import math
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / '03_candidate_selection/05_model_robustness'))
from compare_models import fit_shrunk_paper_effects, np

OUT = HERE / 'results'
EXTRACTIONS = ROOT / '02_identity_and_evidence/02_user_supplied_sources/Original_Capacity_Extraction.csv'


def read_csv(path):
    with path.open(encoding='utf-8-sig', newline='') as file:
        return list(csv.DictReader(file))


def write_csv(name, rows):
    if not rows:
        return
    with (OUT / name).open('w', encoding='utf8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]), lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)


def design(rows, candidates, blocks):
    matrix = np.zeros((len(rows), len(candidates) + len(blocks) - 1))
    candidate_index = {candidate: index for index, candidate in enumerate(candidates)}
    block_index = {block: index for index, block in enumerate(blocks)}
    for index, row in enumerate(rows):
        matrix[index, candidate_index[row['candidate_id']]] = 1
        block = block_index[row['source_block']]
        if block == len(blocks) - 1:
            matrix[index, len(candidates):] = -1
        else:
            matrix[index, len(candidates) + block] = 1
    return matrix


def weights_for(rows, weighting):
    weights = np.ones(len(rows))
    if weighting == 'EQUAL_DOI_TOTAL':
        counts = collections.Counter(row['doi'] for row in rows)
        weights = np.array([1 / counts[row['doi']] for row in rows])
        weights *= len(weights) / weights.sum()
    return weights


def fit(rows, candidates, model, weighting='EQUAL_ROW'):
    blocks = sorted({row['source_block'] for row in rows})
    matrix = design(rows, candidates, blocks)
    outcomes = np.log([float(row['mean']) for row in rows])
    weights = weights_for(rows, weighting)
    if model == 'SHRINK_10':
        coefficients = fit_shrunk_paper_effects(matrix * np.sqrt(weights[:, None]),
                                              outcomes * np.sqrt(weights), len(candidates), 10)
    else:
        coefficients = np.linalg.lstsq(matrix * np.sqrt(weights[:, None]), outcomes * np.sqrt(weights), rcond=None)[0]
    return coefficients, matrix


def run():
    OUT.mkdir(exist_ok=True)
    original = read_csv(EXTRACTIONS)
    rows = []
    for row in original:
        if row['assay'] != 'ORAC_FL' or not row['candidate_id']:
            continue
        row = dict(row)
        row['source_block'] = row['doi'] + '|' + row['protocol_stratum']
        rows.append(row)
    prior_path = ROOT / '03_candidate_selection/01_activity_model/inputs/recovered_capacity_rows.json'
    for row in json.loads(prior_path.read_text(encoding='utf8'))['records']:
        if row['doi'] != '10.3390/antiox12020505':
            continue
        vehicle = 'ETHANOL5_MATCHED_TROLOX' if row['candidate_id'] in {'AFF-0009', 'AFF-0069'} else 'BUFFER'
        rows.append(dict(
            evidence_id='VERIFIED2023-' + row['candidate_id'], doi=row['doi'],
            source_row=row['candidate_id'], source_compound_name=row['compound'], candidate_id=row['candidate_id'],
            candidate_name=row['compound'], mean=row['reported_mean'], reported_error=row['reported_plus_minus'],
            error_type=row['error_type'], pH=row['pH'], temperature_C=row['temperature_C'],
            protocol_stratum='2023_SLOPE_RATIO_' + vehicle,
            source_block=row['doi'] + '|2023_SLOPE_RATIO_' + vehicle,
            source_conflict_flags='', numeric_locator=row['source_locator'],
            source_document='03_candidate_selection/01_activity_model/inputs/recovered_capacity_rows.json',
            source_sha256=hashlib.sha256(prior_path.read_bytes()).hexdigest(),
        ))
    profiles = {row['candidate_id']: row for row in read_csv(ROOT / '02_identity_and_evidence/result/table/candidate_evidence_profiles.csv')}
    decisions = []
    datasets = collections.defaultdict(list)
    for row in rows:
        numeric_conflict = ('NUMERIC_CONFLICT' in row['source_conflict_flags']
                            or 'FIGURE_TABLE_ALIGNMENT_CONFLICT' in row['source_conflict_flags'])
        duplicate_ambiguous = row['doi'] == '10.1155/2020/4150897' and row['source_row'] == '27'
        valid = not numeric_conflict and not duplicate_ambiguous
        core = valid and str(row['pH']) == '7.4' and str(row['temperature_C']) == '37'
        concordant = valid and not row['source_conflict_flags']
        for label, included in [('CORE_REPORTED_PH74_37C', core),
                                ('EXTENDED_UNKNOWN_PH_NAME_BASED', valid),
                                ('EXTENDED_CONFLICT_EXCLUDED', concordant)]:
            if included:
                datasets[label].append(row)
        decisions.append(dict(
            evidence_id=row['evidence_id'], candidate_id=row['candidate_id'], doi=row['doi'],
            source_compound_name=row['source_compound_name'], mean=row['mean'], reported_error=row['reported_error'],
            error_type=row['error_type'], source_block=row['source_block'], pH=row['pH'], temperature_C=row['temperature_C'],
            source_conflict_flags=row['source_conflict_flags'],
            core_diagnostic='YES' if core else 'NO',
            extended_name_diagnostic='YES' if valid else 'NO',
            extended_conflict_excluded_diagnostic='YES' if concordant else 'NO',
            numeric_locator=row['numeric_locator'], source_document=row['source_document'], source_sha256=row['source_sha256'],
            formal_primary_qualification='UNRESOLVED_MATERIAL_AND_PROTOCOL_ALIGNMENT',
            independent_sampling_variance='', human_review_status='NOT_REVIEWED', change_applied='NO',
        ))
    write_csv('Analysis_Data_and_Dispositions.csv', decisions)
    estimates = []
    validations = []
    fold_diagnostics = []
    summaries = []
    source_counts = []
    deletion_orders = []
    row_weights = []
    for variant, data in datasets.items():
        keys = [(row['candidate_id'], row['doi'], row['source_block']) for row in data]
        assert len(keys) == len(set(keys)), (variant, 'Duplicate candidate/source block')
        candidates = sorted({row['candidate_id'] for row in data})
        papers = sorted({row['doi'] for row in data})
        blocks = sorted({row['source_block'] for row in data})
        full_matrix = design(data, candidates, blocks)
        balanced_weights = weights_for(data, 'EQUAL_DOI_TOTAL')
        for index, row in enumerate(data):
            row_weights.append(dict(variant=variant, evidence_id=row['evidence_id'],
                                    candidate_id=row['candidate_id'], doi=row['doi'],
                                    weight_equal_row=1.0, weight_equal_DOI_total=float(balanced_weights[index]),
                                    numeric_measurement_precision_weight='', numeric_IF_weight='',
                                    interpretation='OBSERVATION_VERSUS_DOI_INFLUENCE_SENSITIVITY'))
        for doi in papers:
            source_counts.append(dict(variant=variant, doi=doi, candidate_rows=sum(row['doi'] == doi for row in data),
                                      reported_protocol_blocks=len({row['source_block'] for row in data if row['doi'] == doi})))
        for model, weighting in [('BASELINE', 'EQUAL_ROW'), ('OLS', 'EQUAL_ROW'),
                                 ('SHRINK_10', 'EQUAL_ROW'), ('SHRINK_10', 'EQUAL_DOI_TOTAL')]:
            name = model + '_' + weighting
            if model == 'BASELINE':
                locations = np.array([np.mean([math.log(float(row['mean'])) for row in data
                                               if row['candidate_id'] == candidate]) for candidate in candidates])
                _, matrix = fit(data, candidates, 'OLS')
            else:
                coefficients, matrix = fit(data, candidates, model, weighting)
                locations = coefficients[:len(candidates)]
            for index, candidate in enumerate(candidates):
                candidate_papers = {row['doi'] for row in data if row['candidate_id'] == candidate}
                vector = np.eye(matrix.shape[1])[index]
                projection = matrix.T @ np.linalg.lstsq(matrix.T, vector, rcond=None)[0]
                estimable = np.linalg.norm(projection - vector) < 1e-8
                estimates.append(dict(
                    variant=variant, model=name, candidate_id=candidate, compound=profiles[candidate]['compound_name'],
                    conditional_log_location=float(locations[index]), conditional_geometric_location=float(np.exp(locations[index])),
                    diagnostic_component_order=1 + int(sum(locations > locations[index] + 1e-10)),
                    source_DOIs=len(candidate_papers), source_doi_list=';'.join(sorted(candidate_papers)),
                    estimable_in_unpenalized_design='YES' if estimable else 'NO',
                    interpretation='SOURCE_STRATIFIED_DESCRIPTIVE_MODEL_MATERIAL_AND_PROTOCOL_GAPS',
                    human_review_status='NOT_REVIEWED', change_applied='NO',
                ))
        variant_predictions = []
        for omitted in papers:
            train = [row for row in data if row['doi'] != omitted]
            test = [row for row in data if row['doi'] == omitted]
            training_candidates = sorted({row['candidate_id'] for row in train})
            coefficients, matrix = fit(train, training_candidates, 'SHRINK_10')
            row_space_projection = np.linalg.pinv(matrix, rcond=1e-12) @ matrix
            identifiable_locations = {}
            for index, candidate in enumerate(training_candidates):
                vector = np.eye(matrix.shape[1])[index]
                projection = matrix.T @ np.linalg.lstsq(matrix.T, vector, rcond=None)[0]
                if np.linalg.norm(projection - vector) < 1e-8:
                    identifiable_locations[candidate] = float(coefficients[index])
            for candidate in candidates:
                location = identifiable_locations.get(candidate)
                position = (1 + sum(value > location + 1e-10 for value in identifiable_locations.values())
                            if location is not None else '')
                higher = 0
                lower = 0
                if candidate in training_candidates:
                    first_index = training_candidates.index(candidate)
                    for second_index, other in enumerate(training_candidates):
                        if candidate == other:
                            continue
                        contrast = np.zeros(matrix.shape[1])
                        contrast[first_index] = 1
                        contrast[second_index] = -1
                        if np.linalg.norm(row_space_projection @ contrast - contrast) < 1e-8:
                            difference = coefficients[first_index] - coefficients[second_index]
                            higher += int(difference < -1e-10)
                            lower += int(difference > 1e-10)
                deletion_orders.append(dict(
                    variant=variant, omitted_doi=omitted, candidate_id=candidate,
                    training_log_location=location if location is not None else '',
                    estimable='YES' if location is not None else 'NO',
                    order_among_estimable=position,
                    estimable_contrasts_with_higher_candidates=higher,
                    estimable_contrasts_with_lower_candidates=lower,
                    fixed_universe_best_possible_order=higher+1,
                    fixed_universe_worst_possible_order=len(candidates)-lower,
                    variant_candidate_count=len(candidates),
                    human_review_status='NOT_REVIEWED', change_applied='NO',
                ))
            supported = 0
            for row in test:
                candidate = row['candidate_id']
                status = 'CANDIDATE_ABSENT_FROM_TRAINING'
                prediction = ''
                baseline = ''
                if candidate in training_candidates:
                    index = training_candidates.index(candidate)
                    vector = np.eye(matrix.shape[1])[index]
                    projection = matrix.T @ np.linalg.lstsq(matrix.T, vector, rcond=None)[0]
                    if np.linalg.norm(projection - vector) < 1e-8:
                        prediction = float(coefficients[index])
                        baseline = float(np.mean([math.log(float(item['mean'])) for item in train if item['candidate_id'] == candidate]))
                        status = 'ESTIMABLE_TRAINING_CENTERED_SOURCE_BLOCK_TARGET'
                        supported += 1
                    else:
                        status = 'UNPENALIZED_DESIGN_NOT_ESTIMABLE'
                result = dict(variant=variant, heldout_doi=omitted, candidate_id=candidate,
                              source_block=row['source_block'], observed_log_mean=math.log(float(row['mean'])),
                              predicted_log_location=prediction, baseline_log_location=baseline, estimability=status,
                              human_review_status='NOT_REVIEWED', change_applied='NO')
                validations.append(result)
                if prediction != '':
                    variant_predictions.append(result)
            fold_diagnostics.append(dict(variant=variant, heldout_doi=omitted, training_rows=len(train),
                                         training_candidates=len(training_candidates), training_design_rank=int(np.linalg.matrix_rank(matrix)),
                                         training_parameters=matrix.shape[1], test_rows=len(test), estimable_test_rows=supported))
        metrics = {}
        for field in ['predicted_log_location', 'baseline_log_location']:
            errors = [row[field] - row['observed_log_mean'] for row in variant_predictions]
            metrics[field] = dict(MAE=float(np.mean(np.abs(errors))) if errors else None,
                                  RMSE=float(np.sqrt(np.mean(np.square(errors)))) if errors else None)
        summaries.append(dict(variant=variant, candidate_rows=len(data), candidates=len(candidates),
                              papers=len(papers), reported_protocol_blocks=len(blocks),
                              full_design_rank=int(np.linalg.matrix_rank(full_matrix)), full_parameters=full_matrix.shape[1],
                              single_DOI_candidates=sum(len({row['doi'] for row in data if row['candidate_id'] == candidate}) == 1 for candidate in candidates),
                              heldout_rows=len(variant_predictions), total_heldout_rows=len(data), metrics=metrics))
    write_csv('Candidate_Model_Estimates.csv', estimates)
    write_csv('Leave_DOI_Out_Predictions.csv', validations)
    write_csv('Leave_DOI_Out_Design.csv', fold_diagnostics)
    write_csv('Source_Coverage.csv', source_counts)
    write_csv('Analysis_Row_Weights.csv', row_weights)
    write_csv('Source_Deletion_Order_Sensitivity.csv', deletion_orders)
    selected = [row for row in estimates if row['model'] == 'SHRINK_10_EQUAL_ROW']
    membership = []
    for variant in datasets:
        ordered = sorted([row for row in selected if row['variant'] == variant], key=lambda row: row['diagnostic_component_order'])
        for row in ordered:
            membership.append(dict(row, within_variant_top20='YES' if row['diagnostic_component_order'] <= 20 else 'NO',
                                   global_193_rank='', final_selection_status='UNRESOLVED'))
    write_csv('Diagnostic_Orders_and_Coverage.csv', membership)
    coverage = []
    for candidate, profile in profiles.items():
        candidate_data = [row for row in decisions if row['candidate_id'] == candidate]
        coverage.append(dict(candidate_id=candidate, compound=profile['compound_name'],
                             verified_numeric_source_DOIs=len({row['doi'] for row in candidate_data}),
                             core_diagnostic_rows=sum(row['core_diagnostic']=='YES' for row in candidate_data),
                             extended_conflict_excluded_rows=sum(row['extended_conflict_excluded_diagnostic']=='YES' for row in candidate_data),
                             current_model_estimate='YES' if any(row['candidate_id']==candidate for row in selected) else 'NO',
                             global_193_rank='', human_review_status='NOT_REVIEWED', change_applied='NO'))
    write_csv('All_Candidate_Coverage.csv', coverage)
    membership_changes = []
    for index, first in enumerate(datasets):
        for second in list(datasets)[index+1:]:
            first_rows = {row['candidate_id']:row for row in selected if row['variant']==first}
            second_rows = {row['candidate_id']:row for row in selected if row['variant']==second}
            common = first_rows.keys() & second_rows.keys()
            first_top = set(sorted(common, key=lambda cid:-first_rows[cid]['conditional_log_location'])[:20])
            second_top = set(sorted(common, key=lambda cid:-second_rows[cid]['conditional_log_location'])[:20])
            membership_changes.append(dict(first_variant=first, second_variant=second, common_candidates=len(common),
                                           top_set_size=min(20,len(common)), overlap=len(first_top & second_top),
                                           jaccard=len(first_top & second_top)/len(first_top | second_top),
                                           first_only=';'.join(sorted(first_top-second_top)),
                                           second_only=';'.join(sorted(second_top-first_top)),
                                           interpretation='COMMON_CANDIDATE_UNIVERSE_DIAGNOSTIC_MEMBERSHIP'))
    write_csv('Common_Universe_Membership_Sensitivity.csv', membership_changes)
    summary = dict(status='ORIGINAL_SOURCE_DIAGNOSTICS_PROTOCOL_ALIGNMENT_PENDING',
                   variants=summaries, fixed_shrinkage_lambda=10, newly_tuned_parameters=False,
                   predictor='CANDIDATE_IDENTITY_PLUS_REPORTED_SOURCE_PROTOCOL_BLOCK',
                   unseen_chemical_or_scaffold_prediction_supported=False,
                   formal_global_Top20_established=False, formal_sampling_CIs_estimated=False,
                   source_omission_order_rows=len(deletion_orders),
                   common_universe_membership=membership_changes,
                   new_source_extraction_sha256=hashlib.sha256(EXTRACTIONS.read_bytes()).hexdigest(),
                   original2023_extraction_sha256=hashlib.sha256(prior_path.read_bytes()).hexdigest())
    (OUT / 'model_update_summary.json').write_text(json.dumps(summary, indent=2) + '\n', encoding='utf8')
    print(json.dumps(summary))


if __name__ == '__main__':
    run()
