"""Join identity references, chemical records and latest source closure without applying proposals."""
from pathlib import Path
import sys,collections,re
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'00_project'))
from pipeline_io import *
discovery=read_csv(ROOT/'01_candidate_discovery/results/discovery_register.csv')
cache=read_json(source('archive/phase2_local_cache/phase2_pubchem_identity_cache.json'))
extra_path=ROOT/'02_identity_and_evidence/inputs/pubchem_refresh.json';extra=read_json(extra_path) if extra_path.exists() else {}
lit={r['candidate_id']:r for r in read_csv(source('data/literature_screening/master/Literature_Screening_Candidate_Master.csv'))}
closure={r['candidate_id']:r for r in read_csv(source('data/h_orac_stage25b/stage25b6d/Stage25B6D_Candidate_Eligibility.csv'))}
quality={r['candidate_id']:r for r in read_csv(source('data/h_orac_stage25b/stage25b6d/Stage25B6D_HORAC_Evidence_Profile.csv'))}
experiments=read_csv(source('data/h_orac_stage25b/stage25b/Stage25B_HORAC_Experiment_Evidence.csv'))
frozen={r['candidate_id']:r for r in read_csv(source('data/h_orac_stage25b/frozen/Stage25B_Frozen_Primary_HORAC_Top20.csv'))}
framework=read_csv(source('data/framework/Candidate_157_Data_Availability_Matrix.csv'))
available=collections.defaultdict(dict)
for r in framework:available[r['candidate_id']][r['evidence_dimension']]=r['availability_status']
weak={'Podophyllotoxin','Plumbagin','Juglone','Thymoquinone','Ajoene','S-Allylmercaptocysteine','Ubiquinone-10','Astaxanthin','Fucoxanthin','Baicalein','Chrysin'}
profiles=[];record_index=[]
for d in discovery:
 if not d['candidate_id']:continue
 cid=d['candidate_id'];identity=cache.get(d['name'],{});fresh=extra.get(d['name'],{})
 if fresh.get('status')=='SUCCESS':
  p=fresh['property'];identity={'PubChem_CID':p['CID'],'canonical_name':p.get('Title',d['name']),'molecular_formula':p['MolecularFormula'],'molecular_weight':p['MolecularWeight'],'InChIKey':p['InChIKey']}
 ident_ok=all(identity.get(k) for k in ['PubChem_CID','molecular_formula','InChIKey'])
 l=lit.get(cid,{});c=closure.get(cid,{});q=quality.get(cid,{});f=frozen.get(cid,{})
 ex=[r for r in experiments if r['candidate_id']==cid]
 source_dois=c.get('confirmed_source_DOIs','')
 r={'candidate_id':cid,'discovery_id':d['discovery_id'],'compound_name':d['name'],'reference_name':identity.get('canonical_name',d['name']),'pubchem_cid':identity.get('PubChem_CID',''),'inchi_key':identity.get('InChIKey',''),'molecular_formula':identity.get('molecular_formula',''),'molecular_weight_g_mol':identity.get('molecular_weight',''),'identity_reference_status':'REFERENCE_IDENTIFIERS_AND_FORMULA_PRESENT' if ident_ok else 'IDENTITY_UNRESOLVED','identity_access_mode':'PUG_REST_REFRESH_2026_11_05' if fresh.get('status')=='SUCCESS' else 'PRESERVED_PUBCHEM_REFERENCE_CACHE_NOT_LIVE_RECHECKED','identity_url':f"https://pubchem.ncbi.nlm.nih.gov/compound/{identity.get('PubChem_CID','')}" if ident_ok else '', 'food_occurrence_status':d['dietary_occurrence_status'],'food_source_locator':d['candidate_specific_food_source'],'reported_food_examples':d['reported_food_examples'],'legacy_food_occurrence_uncertain':'YES' if d['name'] in weak else 'NO_SPECIFIC_LEGACY_FLAG_NOT_INDEPENDENTLY_VERIFIED','scope_disposition':d['scope_disposition'],'chemical_form_and_lot_status':'EXACT_FORM_STEREOCHEMISTRY_SALT_HYDRATE_AND_LOT_NOT_VERIFIED','framework157_scope':'YES' if cid in lit else 'NO','confirmed_independent_horac_studies':c.get('confirmed_independent_study_N',''),'confirmed_horac_source_dois':source_dois,'unresolved_horac_source_count':c.get('unresolved_source_N',''),'typed_sd_record_count':q.get('typed_SD_record_N',''),'legacy_horac_ab1_records':q.get('canonical_A_B1_record_N',''),'legacy_horac_confidence':f.get('evidence_confidence',''),'legacy_frozen_rank_reference_only':f.get('primary_rank',''),'legacy_horac_median_reference_only':q.get('H_ORAC_median_mol_TE_per_mol',''),'measurement_ci_status':q.get('CI_status','NOT_ASSESSED'),'research_publication_proxy':l.get('metadata_deduplicated_original_publication_N',''),'latest_publication_year_raw':l.get('latest_antioxidant_publication_year',''),'future_year_metadata_flag':'YES' if (number(l.get('latest_antioxidant_publication_year')) or 0)>2026 else 'NO','reported_assay_eligibility':l.get('stage25B_ORAC_eligibility','NOT_COVERED'),'reported_assay_reason':l.get('ORAC_ineligibility_reason',''),'current_absorbance_compatibility':'NOT_TESTED','current_procurement_status':'NOT_VERIFIED','mechanism_use_limit':'AFF0061 observations and proposals remain NOT_REVIEWED; no validated-target credit' if cid=='AFF-0061' else 'No new target or mechanism approval in this workflow','human_review_status':'NOT_REVIEWED','change_applied':'NO'}
 r.update({dim+'_snapshot_status':available[cid].get(dim,'NOT_COVERED_BY_157_SNAPSHOT') for dim in ['D1','D2','D3','D4','D5']})
 profiles.append(r)
 for n,e in enumerate(ex,1):record_index.append({'candidate_id':cid,'experiment_id':e['independent_experiment_id'],'doi':e['DOI'],'legacy_tier':e['H_ORAC_tier'],'legacy_eligibility':e['eligibility_status'],'raw_value':e['raw_reported_value'],'raw_unit':e['raw_unit'],'source_locator':'; '.join(e.get(k,'') for k in ['source_page','source_table','source_figure','source_supplement']),'source_table':locator('data/h_orac_stage25b/stage25b/Stage25B_HORAC_Experiment_Evidence.csv'),'note':'Record count is not an independent-study count; later source closure applies separately.'})
assert len(profiles)==193
write_csv(ROOT/'02_identity_and_evidence/results/candidate_evidence_profiles.csv',profiles)
write_csv(ROOT/'02_identity_and_evidence/results/chemical_observation_index.csv',record_index)
write_csv(ROOT/'02_identity_and_evidence/results/latest_source_closure.csv',[dict(r,source_snapshot=locator('data/h_orac_stage25b/stage25b6d/Stage25B6D_Source_Closure.csv')) for r in read_csv(source('data/h_orac_stage25b/stage25b6d/Stage25B6D_Source_Closure.csv'))])
print('02: 193 identity/evidence profiles; independent-study closure kept distinct from publication proxies.')
