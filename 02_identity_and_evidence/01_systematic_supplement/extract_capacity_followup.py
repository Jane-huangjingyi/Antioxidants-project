"""Extract source-defined capacity rows while retaining unresolved protocol fields."""
from pathlib import Path
import csv
import hashlib
import json
import re
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def read_csv(path):
    with path.open(encoding='utf-8-sig', newline='') as file:
        return list(csv.DictReader(file))


def text(node):
    return ' '.join(' '.join(node.itertext()).split())


def run():
    profiles = read_csv(ROOT / '02_identity_and_evidence/result/table/candidate_evidence_profiles.csv')
    by_name = {row['compound_name'].casefold(): row for row in profiles}
    queues = read_csv(HERE / 'Method_Fulltext_Queue.csv') + read_csv(HERE / 'Compound_Comparison_Fulltext_Queue.csv')
    queue = {row['PMCID']: row for row in queues if row['source_file']}
    output = []

    def add(pmcid, locator, row_label, name, mean, error, units, ph, temperature,
            error_type, repeats, integration, blockers, candidate_name=None):
        source = queue[pmcid]
        data = (HERE / source['source_file']).read_bytes()
        assert hashlib.sha256(data).hexdigest() == source['sha256']
        profile = by_name.get((candidate_name or name).casefold(), {})
        mw = profile.get('molecular_weight_g_mol', '')
        converted = ''
        converted_error = ''
        conversion = 'NOT_CONVERTED'
        if units == 'mol TE/mol compound':
            converted, converted_error = mean, error
            conversion = 'SOURCE_EXPLICIT_MOLAR_RATIO'
        if units == 'micromol TE/g compound' and mw:
            converted = float(mean) * float(mw) / 1e6
            converted_error = float(error) * float(mw) / 1e6 if error != '' else ''
            conversion = 'CONDITIONAL_REFERENCE_MW_MEAN_AND_ERROR_TIMES_MW_DIV_1E6'
        output.append(dict(
            extraction_id=f'SUP-{pmcid}-{row_label}', candidate_id=profile.get('candidate_id', ''),
            compound_name=name, candidate_name=profile.get('compound_name', ''),
            candidate_mapping='PARENT_NAME_MATCH_EXACT_FORM_PENDING' if profile else 'OUTSIDE_CURRENT_INDEX',
            doi=source['doi'], PMCID=pmcid, source_row=row_label, source_locator=locator,
            raw_mean=mean, raw_error=error, raw_units=units, error_type=error_type,
            reported_replication=repeats, independent_n='', assay='ORAC_FL', pH=ph,
            temperature_C=temperature, integration_rule=integration,
            reference_MW_g_mol=mw, conditional_molar_capacity=converted,
            conditional_molar_error=converted_error, conversion_rule=conversion,
            source_experiment_cluster=source['doi'], source_independence='WITHIN_DOI_ROWS_SHARE_SOURCE',
            unresolved_fields=blockers, source_url=source['source_url'], source_file=source['source_file'],
            source_sha256=source['sha256'], extraction_date='2026-11-12',
            model_label_release='NO', human_review_status='NOT_REVIEWED', change_applied='NO',
        ))

    def tree(pmcid):
        return ET.parse(HERE / queue[pmcid]['source_file']).getroot()

    # Table rows and numeric columns are selected explicitly to prevent assay-column shifts.
    pmcid = 'PMC4578382'
    table = tree(pmcid).find('.//table-wrap[@id="T1"]')
    names = {'2': 'Dehydrozingerone', '6': 'Dehydrozingerone dimer',
             '3': 'Zingerone', '7': 'Zingerone dimer',
             '4': '(2Z,5E)-Ethyl 2-hydroxy-6-(4-hydroxy-3-methoxyphenyl)-4-oxohexa-2,5-dienoate',
             '8': 'Dimer of compound 4', '5': 'Ferulic acid', '9': 'Ferulic acid dimer'}
    for row in table.findall('.//tr'):
        cells = [text(cell) for cell in row.findall('td')]
        if cells and cells[0] in names:
            pair = re.fullmatch(r'([\d.]+)\s*±\s*([\d.]+)', cells[-1])
            assert pair, cells
            add(pmcid, 'T1, RTE column; Supplement S1 section 2.3 pp S8-S9', cells[0],
                names[cells[0]], float(pair[1]), float(pair[2]), 'mol TE/mol compound', 7.4, 37,
                'PLUS_MINUS_DEFINITION_UNRESOLVED_FOR_ORAC', 'ORAC-specific n unresolved',
                'Net protection AUC; full integration duration unresolved',
                'Exact material form/purity; final solvent; integration duration; error definition; independent n')
    assert sum(row['PMCID'] == pmcid for row in output) == 8

    pmcid = 'PMC9563075'
    root = tree(pmcid)
    section = root.find('.//sec[@id="sec3dot3dot1-foods-11-03131"]')
    pairs = re.findall(r'([\d.]+)\s*±\s*([\d.]+)\s*μmol TE/g', text(section))
    assert len(pairs) == 14
    names = ['2,3,4-Trihydroxy-5-methoxy benzoyl chloride', '2-Hydroxy-5-methoxybenzoic acid',
             'Acetyl sulfide', 'Gentisic acid', 'Isovanillic acid', 'Beta-sitosterol',
             '4-Hydroxybenzoic acid', 'Vanillic acid', '2-Methyl-6-(2,3,4-trihydroxybutyl)-pyrazine',
             '3-Hydroxy-4,5-dimethoxyphenyl-beta-D-glucopyranoside',
             '3,4-Dimethoxyphenyl-O-beta-D-glucopyranoside',
             '2,4,6-Trimethoxyphenyl-1-O-beta-D-glucopyranoside', 'Syringic acid', '1,4-Dimethoxybenzene']
    assert 'mean ± SD, n = 3' in text(root.find('.//fig[@id="foods-11-03131-f002"]'))
    for number, (name, pair) in enumerate(zip(names, pairs), start=1):
        add(pmcid, 'Section 3.3.1 ordered values; Figure 2 caption; Section 3.2 identity', str(number),
            name, float(pair[0]), float(pair[1]), 'micromol TE/g compound', '', 37,
            'SD', 'n=3; three dilutions; independent batch unit unresolved',
            '35 one-minute fluorescence cycles; full AUC definition inherited',
            'pH; final solvent; purity; independent n; calibration and integration details')

    pmcid = 'PMC8109830'
    rows = tree(pmcid).findall('.//table-wrap[@id="pone.0251534.t001"]//tr')
    cells = next([text(cell) for cell in row.findall('td')] for row in rows if 'Sesamin' in text(row))
    pair = re.search(r'([\d.]+)\s*±\s*([\d.]+)', cells[1])
    assert pair and float(pair[1]) == 2319.7
    add(pmcid, 'Table 1 sesamin; Sections 2.6 and 2.8', 'Sesamin', 'Sesamin',
        float(pair[1]), float(pair[2]), 'micromol TE/g compound', 7.4, '', 'SD',
        'Triplicate experiments; independent unit unresolved', 'Net protective fluorescein AUC',
        'ORAC temperature; final solvent; purity; independent n; integration duration')

    pmcid = 'PMC11124305'
    rows = tree(pmcid).findall('.//table-wrap[@id="molecules-29-02370-t003"]//tr')
    cells = next([text(cell) for cell in row.findall('td')] for row in rows if 'Ascorbic acid' in text(row))
    assert re.match(r'5982\b', cells[1]), cells
    add(pmcid, 'Table 3 ascorbic acid; Sections 3.4.1 and 3.8', 'Ascorbic', 'Ascorbic acid',
        5982, '', 'micromol TE/g compound', 7.4, 37, 'NOT_REPORTED_FOR_THIS_TABLE_ROW',
        'Duplicate analytical measurements; independent unit unresolved', '50-minute fluorescence AUC',
        'AAPH printed 153 micromolar working solution; exact ascorbate form; final solvent; numeric error; independent n',
        candidate_name='L-Ascorbic acid')

    pmcid = 'PMC10706052'
    table = tree(pmcid).find('.//table-wrap[@id="foods-12-04360-t001"]')
    rows = [[text(cell) for cell in row.findall('td')] for row in table.findall('.//tr')]
    cells = next(cells for cells in rows if cells and cells[0] == 'Trp')
    assert cells[2] == '2.5 ± 0.3', cells
    add(pmcid, 'Table 1 Trp; Sections 2.1, 2.4 and 2.6', 'Trp', 'Tryptophan',
        2.5, 0.3, 'mol TE/mol compound', 7.4, 37, 'SD',
        'At least three independent days, each in triplicate; exact n unavailable',
        'Net normalized fluorescence AUC to F/F0=0.2 with molar concentration ratio',
        'Outside current index; exact stereochemistry; purity; independent day count')

    pmcid = 'PMC6270194'
    table = tree(pmcid).find('.//table-wrap[@id="molecules-18-05389-t001"]')
    assert '1.89 ± 0.2' in text(table)
    add(pmcid, 'Table 1 ORAC column versus Section 2.3; Section 3.6', 'Curcumin', 'Curcumin',
        1.89, 0.2, 'mmol TE/L at reported 1 micromolar compound', 7, '', 'SD',
        'Triplicate treatments; independent batch unit unresolved', 'AUC with quadratic calibration',
        'Table/text assay-column conflict (text 5.01); capacity unit versus 1 micromolar dose; pH outside primary scope; final DMSO; temperature')

    keys = [row['extraction_id'] for row in output]
    assert len(keys) == len(set(keys)) == 26
    with (HERE / 'Original_Capacity_Followup.csv').open('w', encoding='utf8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=list(output[0]), lineterminator='\n')
        writer.writeheader()
        writer.writerows(output)
    summary = dict(source_rows=len(output), source_DOIs=len({row['doi'] for row in output}),
                   mapped_candidates=sorted({row['candidate_id'] for row in output if row['candidate_id']}),
                   primary_model_labels_released=0, human_review_status='NOT_REVIEWED', change_applied='NO')
    (HERE / 'capacity_followup_summary.json').write_text(json.dumps(summary, indent=2) + '\n', encoding='utf8')
    print(json.dumps(summary))


if __name__ == '__main__':
    run()
