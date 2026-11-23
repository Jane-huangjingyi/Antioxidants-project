"""Extract user-provided original tables with document and row provenance.

Requires pypdf. Word table extraction uses the Python standard library.
Source PDFs and DOCX remain at their unique local paths in download_raw.
"""
from pathlib import Path
import csv
import hashlib
import json
import logging
import re
import xml.etree.ElementTree as ET
import zipfile

from pypdf import PdfReader

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
RAW = ROOT / 'download_raw'
NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
logging.getLogger('pypdf').setLevel(logging.ERROR)

DOCUMENTS = {
    'TABART2009': ('Comparative antioxidant', '10.1016/j.foodchem.2008.08.013', 8),
    'ZHANG2020_MAIN': ('1. Oxidative', '10.1155/2020/4150897', 12),
    'ZHANG2020_S1': ('1. Supplementary', '10.1155/2020/4150897', None),
    'ZHANG2013': ('2.', '10.1021/jp307746c', 11),
    'SHARMA2009_DPPH': ('3.', '10.1016/j.foodchem.2008.08.008', 4),
    'OU2001': ('4.', '10.1021/jf010586o', 8),
    'DAVALOS2004': ('5.', '10.1021/jf0305231', 7),
}
REVIEWED_SHA256 = {
    'TABART2009': 'cce507ebe912b349fb10ff896b4ece31f771b6168205c91d808fafacb9e4d61b',
    'ZHANG2020_MAIN': '5b10160bbab455bdf4a81c8029846377e887123cf834b84a028fb5cf87f3db48',
    'ZHANG2020_S1': '2cf261735440ad2901b83a581e7bec84b0bc461b2d58168f3c0b60cab39f0384',
    'ZHANG2013': 'eb8d2ff85c5148c3bf90d27ff87f13cbe006a9a391b2ee7b8aa94ced456cd432',
    'SHARMA2009_DPPH': '3e041b6a12ff0c1c094c05408e89f31548100239408a249581f2124d4f132c20',
    'OU2001': '63e38a487c7083806c904bbe41904e12d6382d47c63e44586186178425606985',
    'DAVALOS2004': '1c1646b4f56ed56659a67a039cce7f255f031b6c5f3ba466cb1ea1baa78dde57',
}

# Original table numbers, separate columns and means/errors checked against page images.
ZHANG2013 = [
    ('Quercetin', 9.51, .43, 8.86, .30), ('Kaempferol', 7.87, .72, 4.99, .12),
    ('Isorhamnetin', 8.07, .13, 4.88, .35), ('Apigenin', 8.95, .73, .97, .18),
    ('Luteolin', 7.95, .53, 3.03, .23), ('Hesperetin', 7.97, .51, .36, .05),
    ('Naringenin', 8.04, .45, .54, .05), ('Genistein', 7.32, .86, .77, .09),
    ('Daidzein', 7.66, .34, .75, .05), ('Epigallocatechin gallate', 5.71, .51, 8.79, .13),
    ('Catechin', 10.59, .58, .20, .04), ('Epicatechin', 9.97, .32, .55, .04),
    ('Epicatechin gallate', 6.75, .65, 7.84, .24),
]
OU2001 = [
    ('Caffeic acid', 4.37, .24, 1.40, .09), ('Chlorogenic acid', 3.14, .19, 1.90, .12),
    ('Quercetrin', 6.47, .29, 2.70, .18), ('Genistein', 5.93, .45, 2.3, .16),
    ('Glutathione', .62, .02, .32, .01), ('Rutin', 6.01, .25, 1.95, .21),
    ('Quercetin', 7.28, .22, 2.07, .05), ('Catechin', 6.76, .22, 2.57, .18),
    ('Vitamin C', .95, .02, .43, .03),
]
DAVALOS2004 = [
    ('Quercetin', 10.5, .4), ('(+)-Catechin', 14.9, .8), ('Caffeic acid', 6.63, .24),
    ('Protocatechuic aldehyde', 6.31, .30), ('Protocatechuic acid', 6.70, .31),
    ('Chlorogenic acid', 5.70, .15), ('Ferulic acid', 4.47, .21),
    ('Coniferyl aldehyde', 4.20, .11), ('p-Coumaric acid', 4.51, .23), ('BHA', 2.43, .06),
]

ALIASES = {
    'Ascorbic acid': 'L-Ascorbic acid',
    'Vitamin C': 'L-Ascorbic acid', '(+)-Catechin': 'Catechin', 'Quercetrin': 'Quercitrin',
    'Quercetin-3-O-galactoside': 'Hyperoside', 'Quercetin-3-O-rhamnoside': 'Quercitrin',
    'Cynaroside': 'Luteolin 7-O-glucoside', 'Vitexin': 'Apigenin 8-C-glucoside',
    'Isovitexin': 'Apigenin 6-C-glucoside', 'Cyanidin chloride': 'Cyanidin',
    'Delphinidin chloride': 'Delphinidin', 'Cyanidin-3-O-glucoside chloride': 'Cyanidin 3-O-glucoside',
    'Oenin chloride': 'Malvidin 3-O-glucoside', 'Malvin': 'Malvidin 3,5-diglucoside',
}

# Issue findings are tied to source row numbers. Values remain unaltered.
ISSUES = {
    16: ('IDENTITY_ANNOTATION_CONFLICT', 'Main Table 1 labels Rutin with R3=Orha, also used for Quercitrin row 28. Reconcile the sugar annotation with the purchased standard.'),
    19: ('NUMERIC_CONFLICT', 'S1 gives 1.02 +/- 0.05. Body section 3.1.1 gives 0.21 +/- 0.01, consistent with the low point for 19 in Figure 1b.'),
    20: ('FIGURE_TABLE_ALIGNMENT_CONFLICT', 'S1 gives 2.34 +/- 0.02. Figure 1b plots compound 20 near 1 rather than the S1 value. No replacement value was digitized.'),
    21: ('FIGURE_TABLE_ALIGNMENT_CONFLICT', 'S1 gives 4.11 +/- 0.03. Body lists 21 among values <=3.97 and Figure 1b plots it near 2.3. No replacement value was digitized.'),
    24: ('IDENTITY_ANNOTATION_CONFLICT', 'Cynaroside/Luteolin-7-O-glucoside has an incomplete substitution listing in main Table 1, with R5 hydroxyl omitted under the stated R=H convention.'),
    27: ('IDENTITY_ANNOTATION_CONFLICT', 'The name says 3-O-rhamnoside, while main Table 1 places Orha at R7. Row 28 separately names Quercitrin. Keep these source rows distinct.'),
    30: ('IDENTITY_ANNOTATION_CONFLICT', 'Main Table 1 places Cglc at R5 for Vitexin, whereas the current identity reference is Apigenin 8-C-glucoside.'),
    32: ('IDENTITY_ANNOTATION_CONFLICT', 'Main Table 1 says Isoorientin and places Cglc at R4. S1 says Luteolin6-C-glucoside. The locant and name need reconciliation.'),
    43: ('IDENTITY_ANNOTATION_CONFLICT', 'Main Table 1 assigns OH at R4-prime and methoxy at R5-prime to Hesperetin. Reconcile the substitution pattern with the named standard.'),
}


def read_csv(path):
    with path.open(encoding='utf-8-sig', newline='') as file:
        return list(csv.DictReader(file))


def write_csv(name, rows):
    target = HERE / name
    temporary = target.with_suffix(target.suffix + '.tmp')
    with temporary.open('w', encoding='utf8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]), lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)
    temporary.replace(target)


def main():
    manifest = []
    pages = {}
    paths = {}
    for document_id, (prefix, doi, expected_pages) in DOCUMENTS.items():
        matches = [path for path in RAW.iterdir() if path.is_file() and path.name.startswith(prefix)]
        assert len(matches) == 1, (document_id, matches)
        path = matches[0]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == REVIEWED_SHA256[document_id], document_id + ': source version requires reassessment'
        paths[document_id] = path
        page_count = ''
        if expected_pages:
            reader = PdfReader(path)
            page_count = len(reader.pages)
            assert page_count == expected_pages, document_id
            pages[document_id] = [page.extract_text(extraction_mode='layout') or '' for page in reader.pages]
            assert doi in '\n'.join(pages[document_id]), (document_id, doi)
        manifest.append(dict(document_id=document_id, doi=doi, file=path.relative_to(ROOT).as_posix(),
                             sha256=hashlib.sha256(path.read_bytes()).hexdigest(), bytes=path.stat().st_size,
                             PDF_pages=page_count, received_assessment_date=('2026-11-13' if document_id == 'TABART2009' else '2026-11-12'),
                             storage='USER_PROVIDED_LOCAL_ORIGINAL', instructions_interpretation='SOURCE_CONTENT_ONLY'))
    write_csv('Source_Document_Manifest.csv', manifest)
    by_document = {row['document_id']: row for row in manifest}
    profiles = read_csv(ROOT / '02_identity_and_evidence/result/table/candidate_evidence_profiles.csv')
    by_name = {row['compound_name'].casefold(): row for row in profiles}
    output = []
    conflicts = []

    def add(document, source_row, compound, mean, error, assay, error_type, nominal_n,
            replication, ph, temperature, protocol, locator, flags='', notes='', ancillary=None):
        source = by_document[document]
        candidate_name = ALIASES.get(compound, compound)
        profile = by_name.get(candidate_name.casefold(), {})
        source_main = by_document['ZHANG2020_MAIN'] if document == 'ZHANG2020_S1' else source
        output.append(dict(
            evidence_id=f'USR-{document}-{source_row}-{assay}', doi=source['doi'], source_row=source_row,
            source_compound_name=compound, candidate_id=profile.get('candidate_id', ''),
            candidate_name=profile.get('compound_name', ''), molecular_formula_reference=profile.get('molecular_formula', ''),
            identity_mapping='PARENT_REFERENCE_PROVISIONAL_EXACT_FORM_RETAINED' if profile else 'OUTSIDE_CURRENT_193_INDEX',
            assay=assay, mean=mean, reported_error=error, error_type=error_type,
            raw_units='micromol TE/micromol compound', nominal_n=nominal_n,
            independent_n_for_weighting='', reported_replication=replication,
            pH=ph, temperature_C=temperature, protocol_stratum=protocol,
            numeric_locator=locator, protocol_locator=('PDF pp3-4 sections 2.2/2.5' if document == 'ZHANG2020_S1' else locator),
            source_document=source['file'], source_sha256=source['sha256'],
            main_document=source_main['file'], main_document_sha256=source_main['sha256'],
            source_conflict_flags=flags, unresolved=notes,
            ancillary_DPPH_IC50_raw=(ancillary or {}).get('DPPH', ''),
            ancillary_CAA_EC50_raw=(ancillary or {}).get('CAA', ''),
            source_experiment_cluster=source['doi'], human_review_status='NOT_REVIEWED', change_applied='NO',
        ))

    with zipfile.ZipFile(paths['ZHANG2020_S1']) as archive:
        word = ET.fromstring(archive.read('word/document.xml'))
    table = word.find('.//w:tbl', NS)
    for physical_row, row in enumerate(table.findall('w:tr', NS), start=1):
        cells = [[''.join(node.text or '' for node in paragraph.findall('.//w:t', NS)).strip()
                  for paragraph in cell.findall('w:p', NS)] for cell in row.findall('w:tc', NS)]
        numbers = [value for value in cells[0] if value.isdigit()]
        if not numbers:
            continue
        for column in cells:
            assert len(column) >= len(numbers), (physical_row, cells)
        for position, number in enumerate(numbers):
            name = cells[1][position]
            raw = cells[3][position]
            match = re.fullmatch(r'(\d+(?:\.\d+)?)\s*±\s*(\d+(?:\.\d+)?)', raw)
            assert match, (number, raw)
            flag, explanation = ISSUES.get(int(number), ('', ''))
            if flag:
                conflicts.append(dict(document_id='ZHANG2020_S1', doi='10.1155/2020/4150897',
                                      source_row=number, issue=flag, finding=explanation,
                                      handling='PRESERVE_SOURCE_VALUES_AND_TEST_EXCLUSION',
                                      human_review_status='NOT_REVIEWED', change_applied='NO'))
            add('ZHANG2020_S1', number, name, float(match[1]), float(match[2]), 'ORAC_FL', 'SD', 3,
                'Triplicate analyses; independent preparation/day unit unspecified', '', 37,
                'ZHANG2020_PH_UNREPORTED_NET_AUC_120MIN',
                f'Table S1 ORAC column, compound {number}, Word physical row {physical_row}',
                flag, 'ORAC pH; final vehicle; material catalogue/CAS; independent unit. ' + explanation,
                dict(DPPH=cells[2][position], CAA=cells[4][position]))
    supplement_rows = [row for row in output if row['doi'] == '10.1155/2020/4150897']
    assert sorted(int(row['source_row']) for row in supplement_rows) == list(range(1, 61))
    assert next(row['mean'] for row in supplement_rows if row['source_row'] == '16') == 12.85
    assert next(row['mean'] for row in supplement_rows if row['source_row'] == '19') == 1.02

    # Check the raw page text before emitting the visually verified table transcription.
    for number, (name, fl, fl_error, pgr, pgr_error) in enumerate(ZHANG2013, start=1):
        assert re.search(rf'\b{fl:.2f}\s*±\s*{fl_error:.2f}', pages['ZHANG2013'][3]), name
        for assay, mean, error in [('ORAC_FL', fl, fl_error), ('ORAC_PGR', pgr, pgr_error)]:
            add('ZHANG2013', str(number), name, mean, error, assay, 'SD', 3,
                'Table n=3; methods triplicates and at least three independent experiments; hierarchy unspecified',
                7.4, 37, 'ZHANG2013_50MM_PH74_37C_180MIN_METHANOL',
                'Table 1 PDF p4 journal p1787; methods PDF p2 sections 2.1-2.3/2.6',
                notes='Final methanol fraction; exact material catalogue/lot; hierarchy of SD and independent experiments. Catechin hydrate and quercetin dihydrate explicitly named in methods.')
    for number, (name, fl, fl_error, pe, pe_error) in enumerate(OU2001, start=1):
        assert re.search(rf'\b{fl:.2f}\s*\(\s*{fl_error:.2f}', pages['OU2001'][3]), name
        for assay, mean, error in [('ORAC_FL', fl, fl_error), ('ORAC_PE', pe, pe_error)]:
            add('OU2001', str(number), name, mean, error, assay, 'PLUS_MINUS_STATISTIC_UNRESOLVED', '>3',
                'Table 4 n>3; duplicate forward/reverse analyses; independent unit unspecified',
                7.4, 37, 'OU2001_CENTRIFUGAL_75MM_PH74_37C_ACETONE',
                'Table 4 PDF p4 journal p4622; methods PDF pp1-2 and Eq2',
                notes='Final acetone fraction; exact replicate count/error definition; methods say 30-minute readings while Eq1 includes f35. Quercetrin is the source spelling.')
    for number, (name, mean, error) in enumerate(DAVALOS2004, start=1):
        # Values include inconsistent source decimal precision and legacy PDF glyphs.
        assert str(mean) in pages['DAVALOS2004'][3], name
        add('DAVALOS2004', str(number), name, mean, error, 'ORAC_FL', 'SD', 3,
            'At least three independent assays, each prepared in duplicate; Table 2 mean n=3 +/- SD',
            7.4, 37, 'DAVALOS2004_75MM_PH74_37C_80MIN_METHANOL',
            'Table 2 PDF p4 journal p51; methods PDF p2',
            notes='Final methanol fraction and exact catalogues. Table 2 supplies original experiments; cited Ou values in discussion are a separate provenance layer.')
    tabart = [
        ('Q', 'Quercetin', 4.2), ('K', 'Kaempferol', 6.2), ('M', 'Myricetin', 3.6),
        ('Q-R', 'Rutin', 4.6), ('K-G', 'Kaempferol-3-O-glucoside', 6.6),
        ('M-R', 'Myricetin-3-rhamnoside', 6.0), ('C', 'Cyanidin', 4.4),
        ('D', 'Delphinidin', 3.8), ('C-G', 'Cyanidin 3-O-glucoside', 7.3),
        ('C-R', 'Cyanidin-3-O-rutinoside', 5.5), ('C-Ga', 'Cyanidin-3-O-galactoside', 5.8),
        ('D-G', 'Delphinidin-3-O-glucoside', 5.9), ('HE', 'Hesperidin', 4.5),
        ('NA', 'Naringenin', 5.6), ('Ca', 'Catechin', 7.9), ('ECa', 'Epicatechin', 5.1),
        ('EGCa', 'Epigallocatechin', 3.1), ('GCa', 'Gallocatechin', 8.3),
        ('EGCaG', 'Epigallocatechin gallate', 3.4), ('GA', 'Gallic acid', 1.0),
        ('CA', 'Chlorogenic acid', 5.3), ('EA', 'Ellagic acid', 2.9),
        ('AA', 'Ascorbic acid', .5), ('Gl', 'Glutathione', .5),
    ]
    for abbreviation, name, mean in tabart:
        assert re.search(rf'\b{re.escape(abbreviation)}\s+.*?\b{mean:.1f}\b', pages['TABART2009'][5]), abbreviation
        add('TABART2009', abbreviation, name, mean, '', 'ORAC_FL', 'TABLE_ERROR_NOT_REPORTED', '>=3',
            'Methods report means +/- SEM of at least three independent experiments; duplicate ORAC at three dilutions; exact n absent',
            '', 37, 'TABART2009_PH_UNREPORTED_NET_AUC_240MIN_METHANOL',
            'Table 1 PDF p6 journal p1231 ORAC column; abbreviations Fig1 PDF p3; methods PDF p2',
            notes='Table1 ratio normalized to measured Trolox. ORAC buffer pH and final methanol unreported. Figure1 error bars not digitized; exact salt/stereochemistry/catalogue unresolved.')
        output[-1]['raw_units'] = 'dimensionless ratio normalized to Trolox measurement, Table 1'
    assert len(output) == 138
    assert len({row['evidence_id'] for row in output}) == len(output)
    assert sum(row['assay'] == 'ORAC_FL' for row in output) == 116
    write_csv('Original_Capacity_Extraction.csv', output)
    write_csv('Source_Conflicts.csv', conflicts)

    original = read_csv(ROOT / '03_candidate_selection/03_preliminary_literature_selection/results/Paper_Specific_Reference_Order.csv')
    fl_lookup = {(row['candidate_id'], row['doi']): row for row in output
                 if row['assay'] == 'ORAC_FL' and row['candidate_id'] and row['source_row'] != '27'}
    reconciled = []
    received_dois = {row['doi'] for row in manifest}
    for row in original:
        if row['doi'] not in received_dois:
            continue
        match = fl_lookup.get((row['candidate_id'], row['doi']))
        old = float(row['paper_reference_median'])
        disposition = 'SOURCE_ROW_NOT_LOCATED'
        if match:
            delta = float(match['mean']) - old
            disposition = 'MATCH' if abs(delta) < 1e-12 else 'ROUNDING_DIFFERENCE' if abs(delta) <= .011 else 'VALUE_CONFLICT'
        reconciled.append(dict(candidate_id=row['candidate_id'], doi=row['doi'],
                               previous_reference_value=old, original_verified_value=match['mean'] if match else '',
                               original_evidence_id=match['evidence_id'] if match else '',
                               disposition=disposition, handling='USE_ORIGINAL_IN_UPDATED_DIAGNOSTIC' if match else 'HOLD_UNLOCATED_ASSOCIATION',
                               human_review_status='NOT_REVIEWED', change_applied='NO'))
    assert any(row['candidate_id'] == 'AFF-0009' and row['doi'] == '10.1021/jf0305231'
               and row['disposition'] == 'VALUE_CONFLICT' for row in reconciled)
    assert any(row['candidate_id'] == 'AFF-0010' and row['doi'] == '10.1021/jf0305231'
               and row['disposition'] == 'SOURCE_ROW_NOT_LOCATED' for row in reconciled)
    write_csv('Existing_Reference_Reconciliation.csv', reconciled)
    leads = [dict(evidence_id=row['evidence_id'], source_compound_name=row['source_compound_name'], doi=row['doi'],
                  source_locator=row['numeric_locator'], scope_status='FOOD_OCCURRENCE_FORMULA_AND_EXACT_IDENTITY_REVIEW_REQUIRED',
                  human_review_status='NOT_REVIEWED', change_applied='NO')
             for row in output if row['assay'] == 'ORAC_FL' and not row['candidate_id'] and row['source_compound_name'] != 'BHA']
    write_csv('Candidate_Extension_Leads.csv', leads)
    summary = dict(documents=len(manifest), original_reports=len(received_dois),
                   capacity_source_DOIs=len({row['doi'] for row in output}), capacity_rows=len(output),
                   ORAC_FL_rows=116, ORAC_PGR_rows=13, ORAC_PE_rows=9,
                   mapped_FL_candidates=len({row['candidate_id'] for row in output if row['assay'] == 'ORAC_FL' and row['candidate_id']}),
                   unmapped_FL_rows=sum(row['assay']=='ORAC_FL' and not row['candidate_id'] for row in output),
                   scope_extension_lead_rows=len(leads), source_conflicts=len(conflicts),
                   reference_value_conflicts=sum(row['disposition'] == 'VALUE_CONFLICT' for row in reconciled),
                   unlocated_reference_associations=sum(row['disposition'] == 'SOURCE_ROW_NOT_LOCATED' for row in reconciled),
                   unresolved_requested_DOI='',
                   formal_model_labels_approved=0, human_review_status='NOT_REVIEWED', change_applied='NO')
    (HERE / 'extraction_summary.json').write_text(json.dumps(summary, indent=2) + '\n', encoding='utf8')
    print(json.dumps(summary))


if __name__ == '__main__':
    main()
