"""Build a reproducible register from documented targeted source assessments.

The assessments below are scientific reading decisions. XML lookup validates
their source locators and hashes. It does not automate scientific approval.
"""
from pathlib import Path
import collections
import csv
import hashlib
import json
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent

# PMCID, disposition, XML locator or section title, reason, remaining work.
ASSESSMENTS = [
    ('PMC10706052', 'OUTSIDE_CURRENT_CANDIDATE_UNIVERSE', 'sec2dot4-foods-12-04360;foods-12-04360-t001',
     'Original free-tryptophan and peptide ORAC-FL experiments at pH 7.4 and 37 C. Free Trp is 2.5 +/- 0.3 molar TE. Current 193-candidate index has no tryptophan entry.',
     'Retain as a prospective scope-extension lead. Resolve exact stereochemical material identity before any candidate addition. At least three independent days are reported, exact day count is unavailable.'),
    ('PMC10886186', 'ENDPOINT_DEFINITION_REQUIRES_RESOLUTION', 'sec2dot4-antioxidants-13-00222;antioxidants-13-00222-t003',
     'Five hydroxycinnamic acids have original kinetic experiments. Table 3 relative AUC is defined as AUC(AH)/AUC(Trolox), while stoichiometry n is fitted. These columns represent distinct estimands.',
     'Recover exact background subtraction and experimental versus fitted uncertainty before comparing with net-AUC molar capacity. Preserve n and kinetic constants separately.'),
    ('PMC11124305', 'ORIGINAL_CAPACITY_EXTRACTION_CANDIDATE', 'sec3dot4dot1-molecules-29-02370;molecules-29-02370-t003',
     'Original ORAC-FL measurements include ascorbic acid 5982 micromol TE/g. Table 1 caption also reports standards including racemic catechin hydrate. pH 7.4, 37 C and 50-minute recording are explicit.',
     'AAPH working concentration is printed as 153 micromolar. Confirm the intended unit without substituting millimolar. Ascorbic acid exact form, final solvent, uncertainty and duplicate experimental unit require resolution.'),
    ('PMC11296029', 'MIXTURE_OUTCOME_ONLY', 'sec2.7;sec3.3',
     'ORAC-FL endpoints concern bilberry fractions and jelly. HPLC identifies constituents within mixtures.',
     'Use for food occurrence and matrix effects. Constituent concentrations cannot assign mixture ORAC to individual molecules.'),
    ('PMC11526049', 'DIFFERENT_ANALYTICAL_ENDPOINT', 'tbl1;tbl2',
     'Pyrogallol-red molybdate measures total urinary protein and nitrite interference. Ascorbate is used in an interference experiment.',
     'Exclude urinary protein outcomes from antioxidant capacity labels.'),
    ('PMC12182667', 'DIETARY_INDEX_ASSOCIATION', 'Tab1;Tab2;Tab3',
     'Cross-sectional dietary ORAC index and clinical associations. Vitamin C intake is a dietary variable.',
     'No isolated-compound molar capacity label is established by these associations.'),
    ('PMC128814', 'SEPARATE_CROCIN_METHOD', 'Colorimetric method for the determination of the TAC of human plasma;Automation of TAC method',
     'Crocin bleaching with ABAP is measured at 450 nm at 37 C. Plasma and spiking validation predominate. Fixed-time calibration differs from ORAC-FL integrated protection.',
     'Retain method and interference evidence. Do not transfer crocin outcomes onto FL capacity without assay bridging.'),
    ('PMC12940556', 'PH7_SENSITIVITY_AND_MIXTURE_INTERACTIONS', 'sec4dot4-ijms-27-01859;ijms-27-01859-t001',
     'Red cabbage and added antioxidants are measured at pH 7.0, 37 C, with 100 mM final AAPH. Tables report interaction coefficients.',
     'Keep pH 7.0 and mixture interaction endpoints separate. Inspect individual-compound curves before considering quantitative extraction.'),
    ('PMC13256772', 'REVIEW_CITATION_DISCOVERY', 'sec2-ijms-27-04825;sec4-ijms-27-04825',
     'Review summarizes assay mechanisms, variants and literature values. Table 1 explicitly adapts a previous mechanism.',
     'Follow references to original experiments. Review tables contribute no independent study labels.'),
    ('PMC13343910', 'DIETARY_INDEX_ASSOCIATION', 'abstract',
     'Geriatric cross-sectional study estimates dietary ORAC from recorded meals and nutrient software.',
     'Retain contextual dietary evidence separately from isolated chemical capacity.'),
    ('PMC3137646', 'MIXTURE_OUTCOME_ONLY', 'sec2.3;sec3.1',
     'ORAC is measured for Kampo formulas and crude herbs, including per-daily-dose results.',
     'No fixed-identity pure-compound molar label follows from formula-level measurements.'),
    ('PMC3299942', 'DIFFERENT_PROBE_AND_CITED_FL_VALUES', 'table-wrap',
     'Original experiments use ORAC-EPR and cyclodextrin-solubilized compounds. Table 1 includes cited literature ORAC-FL values.',
     'Trace each FL entry to its original DOI. Preserve EPR and FL provenance and avoid counting cited values as a new experiment.'),
    ('PMC3586850', 'SEPARATE_CROCIN_METHOD', 'sec7;sec8',
     'Crocin assay compares Bors kinetic and Tsimidou fixed-time endpoints and aqueous fractions. Ascorbate, urate and bilirubin are tested.',
     'Retain endpoint-specific values and solvent fractions. Resolve internal chemical-description errors against methods. No automatic pooling with FL.'),
    ('PMC3951540', 'ASSAY_LABEL_METHOD_CONFLICT', 'Oxygen radical absorbance capacity',
     'Section called oxygen radical absorbance capacity explicitly uses DPPH decolorization at 517 nm in methanol and percent scavenging.',
     'Classify by operational DPPH chemistry. The ORAC title/heading cannot establish an ORAC-FL outcome.'),
    ('PMC3990194', 'MIXTURE_OUTCOME_ONLY', 'sec10;sec11;sec18',
     'Sericin preparations and supplemented breads have ORAC values per material mass. Buffer description says pH 7.0 while measurement paragraph says pH 7.4.',
     'Retain the pH conflict and heterogeneous-protein material scope. No single molecular formula or pure-compound label is established.'),
    ('PMC4578382', 'ORIGINAL_CAPACITY_EXTRACTION_CANDIDATE', 'sec10;T1',
     'Original ORAC-FL relative Trolox equivalents are reported for numbered monomers/dimers. Table 1 defines net-AUC ratio times molarity ratio at 37 C. Ferulic acid is compound 5.',
     'Compound 5 RTE is 2.56 +/- 0.10. Supplement S1 section 2.3 pp S8-S9 confirms pH 7.4, 37 C, 53.6 nM fluorescein and 51.51 mM final AAPH. Final solvent, integration duration, ORAC error definition and repeats remain unresolved. Historical marks in other model columns require column-specific provenance.'),
    ('PMC4878786', 'MIXTURE_AND_COMPANION_REPORT', 's0020;t0005',
     'Rice bran phytochemical and ORAC data are linked to companion DOI 10.1016/j.foodchem.2016.04.004.',
     'Treat companion reports as one potential experiment cluster. Rice bran capacity cannot be assigned to individual constituents.'),
    ('PMC6257802', 'SEPARATE_PGR_METHOD', 'sec12;molecules-15-06152-t001',
     'Pure-compound ORAC-PGR is measured with and without Triton X-100 micelles. Table 1 includes ascorbate, gallates, quercetin and caffeic acid.',
     'Keep probe and micellar strata separate. Preserve kinetic selectivity and solubilization effects during later nonfluorescent validation.'),
    ('PMC6269878', 'DIFFERENT_OXIDANT_ENDPOINT', 'molecules-18-01638-t001',
     'PGR and pyranine measure protection towards hypochlorite, with capacity relative to gallic acid.',
     'Retain HOCl endpoint and reference identity. These values do not quantify AAPH-initiated ORAC-FL.'),
    ('PMC6270307', 'MIXTURE_OUTCOME_ONLY', '3.6. Radical Scavenging Activity by ORAC Assay;molecules-18-01528-t001',
     'Strawberry fruits/calyces have ORAC-FL measurements at pH 7.4 and 37 C per fresh mass.',
     'Use food and matrix evidence without attributing activity to separately identified compounds.'),
    ('PMC6272421', 'DIFFERENT_OXIDANT_ENDPOINT', 'abstract',
     'PGR bleaching by nitrous acid and nitric-oxide chemistry is studied under gastric conditions.',
     'No AAPH-ORAC-FL isolated-candidate capacity is established by the checked endpoint.'),
    ('PMC6523824', 'DIFFERENT_OXIDANT_ENDPOINT', 'abstract',
     'PGR bleaching quantifies carbonate radical formation from SOD-1, hydrogen peroxide and bicarbonate.',
     'Preserve radical-generation kinetics as method context. Do not assign SOD/probe measurements as candidate ORAC labels.'),
    ('PMC6597665', 'ORIGINAL_FIGURE_EXTRACTION_PENDING', 'Sec6;Sec12',
     'Curcumin and demethylated derivatives have dose-specific original ORAC-FL in Figure 2c using OxiSelect, calibrated to micromolar TE over 60 min.',
     'Graph values require explicit digitization or underlying data, exact kit conditions and material identity. Demethylcurcumin and demethoxycurcumin are different compounds.'),
    ('PMC6916041', 'MATRIX_INTERFERENCE_METHOD', 'Sec5;abstract',
     'Human plasma quenches fluorescein before radical reaction. The work adjusts fluorescein for matrix quenching.',
     'Retain interference evidence. Plasma capacity and probe adjustments do not supply isolated-candidate molar labels.'),
    ('PMC8109830', 'ORIGINAL_CAPACITY_EXTRACTION_CANDIDATE', 'sec008;sec013;pone.0251534.t001',
     'Original isolated-compound ORAC-FL includes sesamin 2319.7 +/- 132.8 micromol TE/g in 75 mM pH 7.4 buffer. Statistics identify SD and triplicates.',
     'ORAC temperature, final solvent and chemical purity remain unresolved in the checked methods. Triplicate experimental independence is unspecified. Separate original isolates from previously reported crude extracts.'),
    ('PMC8405165', 'MIXTURE_OUTCOME_ONLY', 's0002-s2004;s0003-s2002',
     'ORAC-FL outcomes belong to Solanum leaf extract and silver nanoparticle preparations. HPLC retention standards identify constituents.',
     'HPLC standard presence supplies no measured pure-standard ORAC label.'),
    ('PMC8838377', 'MIXTURE_OUTCOME_ONLY', 'sec3dot6dot1-molecules-27-00610;molecules-27-00610-t001',
     'Argylia extract ORAC-FL is measured at pH 7.4 and 37 C. Separate MS standards identify components.',
     'Retain extract context. MS identity matches cannot partition the mixture capacity.'),
    ('PMC9146784', 'BIOLOGICAL_MATRIX_ENDPOINT', 'sec2dot1-pharmaceuticals-15-00520;sec4dot5-pharmaceuticals-15-00520',
     'ORAC is applied to stratum-corneum tape-strip extracts and skin oxidative state.',
     'Keep skin assay validation separately. Biological matrix ORAC cannot be assigned as pure topical-agent molar capacity.'),
    ('PMC9495677', 'EXISTING_SOURCE_DOSE_RECHECK', 'sec2dot1-antioxidants-11-01784;sec2dot2dot2-antioxidants-11-01784;antioxidants-11-01784-t002',
     'Ten individual phenolic acids have ORAC at 2.5 and 5 micromolar in Table 2. Stocks use 80:20 ethanol/water. Three replicates and 80 min are stated.',
     'This source already has a dedicated extraction. Preserve dose-specific ratios. Final solvent, pH, temperature, error definition and replication independence need inherited-protocol resolution.'),
    ('PMC9951910', 'EXISTING_SOURCE_RECHECK', 'antioxidants-12-00505-t003',
     'Original Table 3 contains AUC and lag-time Trolox equivalents plus cited literature ranges. Existing extraction already uses the original AUC column.',
     'Reconcile exact form and final solvent. Do not duplicate the AUC column, count lag-time as another study, or import literature ranges as new experiments.'),
]

# Abstract and method-heading screens schedule endpoint-specific reading.
# Each entry was reviewed at that stated scope, which differs from extraction.
COMPARISON_SCREENS = {
    'PMC8459241': ('CELLULAR_ENDPOINT', 'Anthocyanins are tested in Caco-2 cells with DCF, viability and qPCR endpoints.'),
    'PMC6467993': ('OTHER_ASSAY_AND_MIXTURE', 'Tinctures are evaluated with DPPH-EPR, NMR and total polyphenols.'),
    'PMC7075987': ('OTHER_ASSAY', 'DPPH/ABTS-guided HPLC measures isolated phenolics and leaf extracts.'),
    'PMC11699150': ('SECONDARY_DATASET', 'Data-mining study reuses antioxidant-mixture literature. Trace each underlying experiment.'),
    'PMC4563559': ('OTHER_ASSAY', 'Isolated phenolics have DPPH, ABTS, FRAP and lipid-peroxidation endpoints.'),
    'PMC5009353': ('OTHER_ASSAY_AND_MIXTURE', 'Maillard reaction products are evaluated by DPPH, ABTS and FRAP.'),
    'PMC13279865': ('REVIEW_CITATION_DISCOVERY', 'Food-matrix antioxidant review supplies method and original-source leads.'),
    'PMC4609401': ('OTHER_ASSAY', 'One hundred pure compounds have DPPH, ABTS and online HPLC-ABTS assays.'),
    'PMC5660747': ('OTHER_ASSAY', 'Pure flavonoids and phenolics have reducing, chelating, DPPH, ABTS, DMPD and superoxide assays.'),
    'PMC7525318': ('ORIGINAL_SUPPLEMENT_RECOVERED_WITH_CONFLICTS', 'The researcher supplied original PDF and Table S1 DOCX. All 60 FL rows were extracted in Step 02.2. Nine value/alignment or identity-annotation findings are recorded. Body methods report 37 C and SD for n=3 triplicate analyses. ORAC pH and final solvent remain unresolved.'),
    'PMC3406971': ('DIETARY_INDEX_ASSOCIATION', 'Ovarian-cancer case-control study uses dietary antioxidant intake indices.'),
    'PMC3907558': ('OTHER_ASSAY', 'DPPH, ABTS and FRAP evaluate herb combinations and isolated synergistic compounds.'),
    'PMC13518190': ('REVIEW_CITATION_DISCOVERY', 'Review covers redox-exercise interactions and neurodegeneration.'),
    'PMC7914583': ('OTHER_ASSAY_AND_MIXTURE', 'Stone-fruit wastes have DPPH, FRAP, ABTS and total antioxidant capacity.'),
    'PMC8389318': ('OTHER_ASSAY', 'Selected flavonoids have hydrogen-peroxide scavenging, metal reduction, iron binding and lipid-peroxidation assays.'),
    'PMC10135960': ('OTHER_ASSAY_AND_MIXTURE', 'Rowanberry cultivars have DPPH and photochemiluminescence ACW/ACL. ORAC appears in context.'),
    'PMC10525925': ('DIFFERENT_OXIDANT_ENDPOINT', 'Carotenoids/ascorbate are assessed using singlet-oxygen, hydroxyl-radical and liposomal oxidation endpoints.'),
    'PMC10967577': ('CITED_FL_VALUES', 'Section 3.5 compares new DPPH to previously determined H-ORAC from reference 37. H-ORAC values need the earlier source key.'),
    'PMC11047381': ('REVIEW_CITATION_DISCOVERY', 'Review of natural antioxidant peptides and assay methods.'),
    'PMC11351990': ('OTHER_ASSAY', 'Synthetic dithiocarbamic flavanones have DPPH, ABTS and FRAP assays.'),
    'PMC11762797': ('OTHER_ASSAY_AND_MIXTURE', 'Rubus fruits have DPPH, ABTS and FRAP.'),
    'PMC12189461': ('OTHER_ASSAY', 'Synthesized biflavones have DPPH activity and QSAR.'),
    'PMC13603980': ('REVIEW_CITATION_DISCOVERY', 'Nanoantioxidant review supplies no new isolated-parent FL measurement.'),
    'PMC4665520': ('MIXTURE_OUTCOME_ONLY', 'Refined/whole wheat flour and bread have original ORAC and DPPH.'),
    'PMC6769521': ('LIPID_OXIDATION_METHOD', 'High-throughput linoleic-acid emulsion is evaluated by TBARS and ferric thiocyanate.'),
    'PMC9563075': ('ORIGINAL_CAPACITY_EXTRACTION_CANDIDATE', 'Fourteen original isolate capacities are listed in section 3.3.1. ORAC at 37 C uses fluorescein and micromol TE/g. Figure 2 caption identifies mean +/- SD, n=3. pH, final solvent and independent experimental unit require resolution.'),
    'PMC2672020': ('DIFFERENT_PROBE_AND_MIXTURE', 'Original plant-extract assay uses R-phycoerythrin at pH 7.0, 37 C.'),
    'PMC6413046': ('SECONDARY_DATASET', 'Tripeptide QSAR reuses activity datasets. Trace original assay and sequences.'),
    'PMC6539043': ('EXISTING_SOURCE_RECHECK', 'Original experimental Table 3 ln(ORAC) already extracted. Keep PLS/ANN predictions separate.'),
    'PMC10298513': ('OTHER_ASSAY', 'Myricetin, kaempferol and quercetin binary mixtures have ABTS/DPPH.'),
    'PMC11728272': ('OTHER_ASSAY', 'Synthetic dithiocarbamic flavanones have DPPH, ABTS and FRAP.'),
    'PMC6891513': ('OTHER_ASSAY_AND_MIXTURE', 'Co-culture peptide fractions have scavenging and cell-protection endpoints. Individual identity and original assay mapping need separate work.'),
    'PMC6268240': ('OTHER_ASSAY', 'Mango phenolic interactions are screened outside an explicitly stated FL assay. Original method details remain scheduled for assay-specific extraction.'),
    'PMC6270535': ('OTHER_ASSAY', 'Individual mate phenolic activity is evaluated by online ABTS.'),
    'PMC6270194': ('SOURCE_INTERNAL_VALUE_UNIT_CONFLICT', 'Curcumin ORAC is 1.89 +/- 0.2 mmol TE/L in Table 1 but section 2.3 attributes 5.01 to ORAC, matching the FRAP column. A 1 micromolar compound concentration and pH 7 are stated. Preserve the unit and column conflict.'),
    'PMC6270187': ('OTHER_ASSAY', 'Glutathione-flavonoid binary mixtures are assessed using DPPH.'),
    'PMC6273900': ('REVIEW_CITATION_DISCOVERY', 'Natural protein antioxidant-peptide review. Table entries refer to original studies.'),
    'PMC6274360': ('OTHER_ASSAY', 'Thirty-seven phenolic compounds have ABTS/TEAC, FRAP and DPPH.'),
    'PMC6100071': ('OTHER_ASSAY', 'Dihydrochalcones have FRAP, ABTS, DPPH and superoxide assays.'),
    'PMC6222747': ('OTHER_ASSAY', 'Daphnetin derivatives have DPPH and ABTS.'),
    'PMC6930660': ('OTHER_ASSAY', 'Carbohydrate phenolics are measured by DPPH at 520 nm.'),
    'PMC7583942': ('OTHER_ASSAY', 'Sixteen walnut phenolics use a Cu2+-reduction colorimetric kit at 570 nm. ARE activation is a separate cellular endpoint.'),
    'PMC8347205': ('OTHER_ASSAY', 'Flavonoid/caffeine/thiamine combinations have chelation, reducing power and stable-radical scavenging.'),
    'PMC9268411': ('OTHER_ASSAY', 'S-allyl-L-cysteine/polyphenol interactions use DPPH, ABTS and reducing-power endpoints.'),
    'PMC12155936': ('OTHER_ASSAY', 'Iodinated dithiocarbamic flavanones have DPPH/ABTS.'),
    'PMC13165421': ('OTHER_ASSAY', 'Harmonized phenolic profiling uses ABTS, DPPH and reducing power. ORAC is mentioned as context.'),
    'PMC13414662': ('REVIEW_CITATION_DISCOVERY', 'Review of plant-antioxidant SAR in myocardial infarction.'),
    'PMC9412878': ('OTHER_ASSAY_AND_MIXTURE', 'Humic-acid preparations have DPPH at 520 nm and cytoprotection.'),
    'PMC7813601': ('OTHER_ASSAY_AND_MIXTURE', 'Evening-primrose seed preparations have antioxidant and lipid-peroxidation endpoints.'),
}


def read_csv(path):
    with path.open(encoding='utf-8-sig', newline='') as file:
        return list(csv.DictReader(file))


def run():
    queue = {row['PMCID']: row for row in read_csv(HERE / 'Method_Fulltext_Queue.csv') if row['PMCID']}
    comparison_queue = read_csv(HERE / 'Compound_Comparison_Fulltext_Queue.csv')
    queue.update({row['PMCID']: row for row in comparison_queue})
    profiles = read_csv(HERE.parents[1] / '02_identity_and_evidence/result/table/candidate_evidence_profiles.csv')
    assert len(ASSESSMENTS) == 30
    assert len({row[0] for row in ASSESSMENTS}) == 30
    output = []
    assessments = list(ASSESSMENTS)
    for pmcid, (decision, finding) in COMPARISON_SCREENS.items():
        locator = 'sec2.2;sec2.5;sec3.1.1;supp-1' if pmcid == 'PMC7525318' else 'abstract'
        assessments.append((pmcid, decision, locator, finding,
                            'Screen disposition is specific to ORAC-FL model eligibility. Other assays remain evidence for their own endpoints. Detailed extraction and original-report independence require completion where relevant.'))
    recovered_comparisons = {row['PMCID'] for row in comparison_queue if row['source_file']}
    assert recovered_comparisons == set(COMPARISON_SCREENS)
    for pmcid, decision, locators, reason, remaining in assessments:
        row = queue[pmcid]
        source = HERE / row['source_file']
        data = source.read_bytes()
        assert hashlib.sha256(data).hexdigest() == row['sha256'], pmcid
        tree = ET.fromstring(data)
        all_ids = {node.get('id') for node in tree.iter() if node.get('id')}
        text = ' '.join(tree.itertext())
        for locator in locators.split(';'):
            assert (locator in all_ids or locator in text
                    or tree.find('.//' + locator) is not None), (pmcid, locator)
        output.append(dict(
            article_key=row['article_key'], doi=row['doi'], PMCID=pmcid, title=row['title'],
            journal=row['journal'], assessment_date='2026-11-12', disposition=decision,
            checked_locators=locators, scientific_finding=reason, unresolved=remaining,
            reading_scope=('ABSTRACT_AND_METHOD_HEADING_SCREEN' if pmcid in COMPARISON_SCREENS and pmcid not in {'PMC7525318','PMC9563075','PMC10967577','PMC6270194','PMC6539043'}
                           else 'TARGETED_BODY_METHOD_TABLE_TEXT_SCREEN'),
            visual_figures_and_supplements=('SUPPLEMENT_TEXT_S8_S9_CHECKED_VISUAL_FIGURES_NOT_CHECKED'
                                           if pmcid == 'PMC4578382' else 'USER_PDF_TABLE1_FIG1_AND_ORIGINAL_DOCX_S1_CHECKED_STEP_02_2'
                                           if pmcid == 'PMC7525318' else 'NOT_CHECKED_IN_THIS_PASS'),
            source_url=row['source_url'], source_file=row['source_file'], source_sha256=row['sha256'],
            model_label_release='NO', human_review_status='NOT_REVIEWED', change_applied='NO',
        ))
    with (HERE / 'Source_Scientific_Screening.csv').open('w', encoding='utf8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=list(output[0]), lineterminator='\n')
        writer.writeheader()
        writer.writerows(output)
    summary = dict(screened_articles=len(output),
                   reading_scope_counts=dict(collections.Counter(row['reading_scope'] for row in output)),
                   current_candidate_universe=len(profiles),
                   disposition_counts=dict(collections.Counter(row['disposition'] for row in output)),
                   newly_released_model_labels=0,
                   all_source_hashes_and_locators_verified=True)
    (HERE / 'source_screening_summary.json').write_text(json.dumps(summary, indent=2) + '\n', encoding='utf8')
    print(json.dumps(summary))


if __name__ == '__main__':
    run()
