"""Audit the deposited slope summaries without releasing capacity-model labels."""
import argparse
import csv
import hashlib
import json
import statistics
import urllib.request
from reconcile_existing_work import HERE, SOURCE, write


FILES = {
    'WWSOBP_ORAC_Results.csv': 638912,
    'WWSOBP_Calibration.csv': 637810,
    'WWSOBP_OracCurves.pdf': 639600,
    'WWSOBP_ReadmeV2.odt': 639601,
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--fetch', action='store_true')
    args = parser.parse_args()
    manifest = []
    for name, identifier in FILES.items():
        path = SOURCE / 'inputs' / name
        url = 'https://entrepot.recherche.data.gouv.fr/api/access/datafile/' + str(identifier)
        if not path.exists() and args.fetch:
            with urllib.request.urlopen(url, timeout=40) as response:
                path.write_bytes(response.read())
        if not path.exists():
            raise FileNotFoundError(str(path) + '; rerun with --fetch for public retrieval')
        manifest.append(dict(dataset_doi='10.57745/WWSOBP', article_doi='10.1002/chem.202503176',
                             file_name=name, repository_file_id=identifier, source_url=url,
                             source_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                             bytes=path.stat().st_size, model_label_release='NO'))
    write('Public_ORAC_Deposit_Manifest.csv', manifest)
    with (SOURCE / 'inputs/WWSOBP_ORAC_Results.csv').open(newline='', encoding='utf8') as handle:
        raw = list(csv.reader(handle, delimiter=';'))
    rows = []
    for column, compound in enumerate(raw[0][1:], 1):
        values = [float(row[column]) for row in raw[1:5] if row[column] != 'n.d.']
        mean = statistics.mean(values)
        printed_error = float(raw[6][column])
        deviation = statistics.mean(abs(value - mean) for value in values)
        first_three_mean = statistics.mean(values[:3])
        first_three_deviation = statistics.mean(abs(value-first_three_mean) for value in values[:3])
        assert abs(mean - float(raw[5][column])) < 1e-8
        rows.append(dict(dataset_doi='10.57745/WWSOBP', article_doi='10.1002/chem.202503176',
                         source_compound_code=compound, deposited_slopes=json.dumps(values),
                         available_slope_count=len(values), printed_average=raw[5][column],
                         recomputed_average=mean, printed_Stdev_row=printed_error,
                         recomputed_sample_SD=statistics.stdev(values),
                         recomputed_mean_absolute_deviation=deviation,
                         error_row_check='MATCHES_MEAN_ABSOLUTE_DEVIATION' if abs(deviation-printed_error)<1e-8
                                         else 'MATCHES_FIRST_THREE_MEAN_ABSOLUTE_DEVIATION' if abs(first_three_deviation-printed_error)<1e-8
                                         else 'DOES_NOT_MATCH_SD_OR_MEAN_ABSOLUTE_DEVIATION',
                         disposition='ERROR_DEFINITION_AND_MATERIAL_SCOPE_HOLD',
                         unresolved='Slope units, replicate pairing, dietary identity and raw concentration hierarchy require reconciliation; no TE ratio computed.',
                         human_review_status='NOT_REVIEWED', change_applied='NO', model_label_release='NO'))
    assert len(rows) == 8
    write('Public_ORAC_Deposit_Summary_Audit.csv', rows)
    print('Eight deposited slope summaries audited; model labels remain on hold.')


if __name__ == '__main__':
    main()
