import csv, json, urllib.parse, urllib.request, time
from pathlib import Path
from datetime import date
ROOT=Path(__file__).resolve().parent; DATA=ROOT/'data'; DATA.mkdir(exist_ok=True)
TODAY=str(date.today())

# Candidate generation is intentionally independent of antioxidant assay performance.
# name, parent class, analysis panel, subclass, structural family, state, glycoside, stereochemistry, dietary status, sources
spec=[]
def add(names,parent,panel,subclass,family,sources,gly='aglycone/non-glycoside',stereo='see PubChem',diet='dietary parent'):
 for n in names: spec.append(dict(compound=n,parent_class=parent,analysis_panel=panel,subclass=subclass,structural_family=family,representative_food_sources=sources,glycoside_or_aglycone=gly,stereochemistry=stereo,dietary_parent_or_metabolite=diet))

P='Polyphenols'
add(['Catechin','Epicatechin','Epigallocatechin gallate','Epicatechin gallate','Epigallocatechin','Gallocatechin','Gallocatechin gallate','Catechin gallate'],P,'Polyphenols–Flavonoids','Flavan-3-ols','flavan-3-ol','tea; cocoa; apples')
add(['Quercetin','Kaempferol','Myricetin','Isorhamnetin','Fisetin','Morin'],P,'Polyphenols–Flavonoids','Flavonols','flavonol','onions; leafy vegetables; berries; tea')
add(['Quercitrin','Isoquercitrin','Rutin','Hyperoside','Kaempferol 3-O-glucoside','Myricitrin'],P,'Polyphenols–Flavonoids','Flavonol glycosides','flavonol glycoside','fruit; vegetables; tea',gly='glycoside')
add(['Luteolin','Apigenin','Chrysin','Baicalein','Tricin'],P,'Polyphenols–Flavonoids','Flavones','flavone','parsley; celery; cereals; honey')
add(['Luteolin 7-O-glucoside','Apigenin 7-O-glucoside','Apigenin 6-C-glucoside','Apigenin 8-C-glucoside'],P,'Polyphenols–Flavonoids','Flavone glycosides','flavone glycoside','celery; parsley; chamomile; cereals',gly='glycoside')
add(['Naringenin','Hesperetin','Eriodictyol','Isosakuranetin'],P,'Polyphenols–Flavonoids','Flavanones','flavanone','citrus fruit; herbs')
add(['Naringin','Narirutin','Hesperidin','Eriocitrin','Neohesperidin'],P,'Polyphenols–Flavonoids','Flavanone glycosides','flavanone glycoside','citrus fruit and juice',gly='glycoside')
add(['Cyanidin','Delphinidin','Pelargonidin','Malvidin','Peonidin','Petunidin'],P,'Polyphenols–Flavonoids','Anthocyanidins','anthocyanidin','berries; grapes; colored grains',stereo='flavylium form; counterion/form must be recorded')
add(['Cyanidin 3-O-glucoside','Delphinidin 3-O-glucoside','Pelargonidin 3-O-glucoside','Malvidin 3-O-glucoside','Peonidin 3-O-glucoside','Cyanidin 3-O-rutinoside','Malvidin 3,5-diglucoside'],P,'Polyphenols–Flavonoids','Anthocyanins','anthocyanin glycoside','berries; grapes; red/purple vegetables',gly='glycoside',stereo='flavylium form; counterion/form must be recorded')
add(['Genistein','Daidzein','Glycitein','Formononetin','Biochanin A'],P,'Polyphenols–Flavonoids','Isoflavones','isoflavone','soy foods; legumes')
add(['Genistin','Daidzin','Glycitin'],P,'Polyphenols–Flavonoids','Isoflavone glycosides','isoflavone glycoside','soy foods',gly='glycoside')

add(['Gallic acid','Protocatechuic acid','4-Hydroxybenzoic acid','Vanillic acid','Syringic acid','Gentisic acid','Salicylic acid','2,3-Dihydroxybenzoic acid','3,4,5-Trimethoxybenzoic acid'],P,'Polyphenols–Phenolic acids / conjugates','Hydroxybenzoic acids','benzoic-acid phenolic','berries; tea; wine; grains')
add(['Caffeic acid','Ferulic acid','p-Coumaric acid','Sinapic acid','o-Coumaric acid','m-Coumaric acid','Isoferulic acid'],P,'Polyphenols–Phenolic acids / conjugates','Hydroxycinnamic acids','cinnamic-acid phenolic','coffee; grains; fruit; vegetables',stereo='trans form unless explicitly named')
add(['Chlorogenic acid','Neochlorogenic acid','Cryptochlorogenic acid','3,4-Dicaffeoylquinic acid','3,5-Dicaffeoylquinic acid','4,5-Dicaffeoylquinic acid','Feruloylquinic acid','p-Coumaroylquinic acid'],P,'Polyphenols–Phenolic acids / conjugates','Caffeoylquinic and related acids','hydroxycinnamate ester','coffee; potatoes; artichoke; fruit',gly='defined conjugate')
add(['Rosmarinic acid','Ellagic acid','Chicoric acid','Caftaric acid','Coutaric acid'],P,'Polyphenols–Phenolic acids / conjugates','Other defined phenolic conjugates','defined phenolic conjugate','culinary herbs; berries; grapes',gly='defined conjugate')

add(['trans-Resveratrol','cis-Resveratrol','Piceatannol','Pterostilbene','Piceid'],P,'Polyphenols–Stilbenes / lignans','Stilbenes','stilbene','grapes; wine; berries; peanuts',gly='glycoside' if False else 'aglycone/non-glycoside')
add(['Secoisolariciresinol','Matairesinol','Lariciresinol','Pinoresinol','Medioresinol','Syringaresinol','Sesamin','Sesamolin','Sesamol','Podophyllotoxin'],P,'Polyphenols–Stilbenes / lignans','Dietary parent lignans','plant lignan','flaxseed; sesame; whole grains; vegetables')

V='Vitamins / vitamin-like antioxidants'
add(['L-Ascorbic acid','Dehydroascorbic acid'],V,'Vitamins / vitamin-like','Water-soluble antioxidant vitamins','vitamin C vitamer','fruit; vegetables',stereo='defined L-vitamer',diet='dietary vitamer')
add(['alpha-Tocopherol','beta-Tocopherol','gamma-Tocopherol','delta-Tocopherol'],V,'Vitamins / vitamin-like','Tocopherols','tocopherol','plant oils; nuts; seeds',stereo='natural stereoisomer/form must be retained',diet='dietary vitamer')
add(['alpha-Tocotrienol','beta-Tocotrienol','gamma-Tocotrienol','delta-Tocotrienol'],V,'Vitamins / vitamin-like','Tocotrienols','tocotrienol','palm oil; rice bran; cereals',stereo='natural stereoisomer/form must be retained',diet='dietary vitamer')

C='Carotenoids'
add(['all-trans-beta-Carotene','alpha-Carotene','all-trans-Lycopene','Phytoene','Phytofluene'],C,'Carotenoids','Carotenes','carotene','colored fruit and vegetables; tomato products',stereo='isomer-specific identity required')
add(['Lutein','Zeaxanthin','beta-Cryptoxanthin','Astaxanthin','Canthaxanthin','Capsanthin','Capsorubin','Violaxanthin','Neoxanthin','Fucoxanthin'],C,'Carotenoids','Xanthophylls','xanthophyll','leafy greens; peppers; maize; egg; seafood; edible seaweed',stereo='isomer-specific identity required')
add(['9-cis-beta-Carotene','13-cis-beta-Carotene','9-cis-Lycopene','13-cis-Lycopene'],C,'Carotenoids','Defined cis isomers','carotenoid cis isomer','processed vegetables and human diets',stereo='specified cis isomer')

S='Organosulfur compounds'
add(['Sulforaphane','Erucin','Allyl isothiocyanate','Benzyl isothiocyanate','Phenethyl isothiocyanate','Iberin'],S,'Organosulfur compounds','Isothiocyanates','isothiocyanate','cruciferous vegetables; mustard; wasabi',diet='processing/generated from dietary glucosinolate')
add(['Allicin','Ajoene'],S,'Organosulfur compounds','Thiosulfinates and derivatives','reactive allium sulfur','fresh crushed garlic',diet='processing-generated dietary compound')
add(['Diallyl sulfide','Diallyl disulfide','Diallyl trisulfide','Methyl allyl sulfide','Dipropyl disulfide'],S,'Organosulfur compounds','Allium sulfides','organosulfide','garlic; onion; leek',diet='dietary/processing-generated compound')
add(['S-Allyl-L-cysteine','S-Allylmercaptocysteine'],S,'Organosulfur compounds','Water-soluble allium sulfur','sulfur amino-acid derivative','garlic products',diet='dietary compound; supplement dominance must be checked')

N='Betalains / nitrogen-containing phytochemicals'
add(['Betanin','Isobetanin','Probetanin','Neobetanin'],N,'Betalains / nitrogen-containing','Betacyanins','betalain pigment','beetroot; cactus fruit',gly='defined glycoside/pigment',stereo='pigment form and counterion must be retained')
add(['Indicaxanthin','Vulgaxanthin I','Vulgaxanthin II','Miraxanthin V','Dopaxanthin'],N,'Betalains / nitrogen-containing','Betaxanthins','betalain pigment','beetroot; cactus fruit; amaranth',gly='defined pigment',stereo='pigment form must be retained')
add(['Caffeine','Trigonelline'],N,'Betalains / nitrogen-containing','Other dietary nitrogen-containing phytochemicals','alkaloid/zwitterion','coffee; tea',diet='dietary parent')

O='Other food-derived redox-active phytochemicals'
add(['Curcumin','Demethoxycurcumin','Bisdemethoxycurcumin'],O,'Other food-derived redox-active phytochemicals','Curcuminoids','curcuminoid','turmeric and curry spice')
add(['Capsaicin','Dihydrocapsaicin','Nordihydrocapsaicin','Homocapsaicin','Homodihydrocapsaicin'],O,'Other food-derived redox-active phytochemicals','Capsaicinoids','capsaicinoid','chili pepper')
add(['Eugenol','Isoeugenol','Carvacrol','Thymol','Anethole','Estragole','Vanillin','Gingerol','Shogaol','Zingerone'],O,'Other food-derived redox-active phytochemicals','Culinary spice phenolics','spice phenolic/phenylpropanoid','clove; oregano; thyme; fennel; vanilla; ginger')
add(['Plumbagin','Juglone','Thymoquinone'],O,'Other food-derived redox-active phytochemicals','Dietary quinones','quinone','walnut; culinary seeds/spices',diet='dietary relevance requires strict confirmation')
add(['Hydroxytyrosol','Tyrosol','Oleuropein','Oleocanthal'],O,'Other food-derived redox-active phytochemicals','Olive phenolics','olive phenolic','olives; extra virgin olive oil')
add(['Ubiquinone-10'],O,'Other food-derived redox-active phytochemicals','Dietary quinones','coenzyme Q','meat; fish; oils',diet='dietary and endogenous; dietary role must be kept separate')

M='Antioxidant-related micronutrients / mineral cofactors'
add(['Selenium','Zinc','Manganese','Copper','Iron','Magnesium','Molybdenum'],M,'Antioxidant-related micronutrients / mineral cofactors','Mineral cofactors','element/mineral nutrient','varied foods; source depends on element',gly='not applicable',stereo='not applicable',diet='dietary micronutrient context')

# Explicit exclusions retained; these are proposed natural products/metabolites that fail the current dietary-parent gate.
exclusions=[
('Enterodiol','Polyphenols–Stilbenes / lignans','human/microbial metabolite, not dietary parent',0,0,0,0,0,1,0,'Keep in metabolite layer.'),
('Enterolactone','Polyphenols–Stilbenes / lignans','human/microbial metabolite, not dietary parent',0,0,0,0,0,1,0,'Keep in metabolite layer.'),
('Total polyphenols','Polyphenols','mixture/aggregate variable',0,0,1,1,0,0,0,'No unique chemical identity.'),
('Total carotenoids','Carotenoids','mixture/aggregate variable',0,0,1,1,0,0,0,'No unique chemical identity.'),
('Grape seed extract','Polyphenols','uncharacterized/variable mixture',1,0,0,1,0,0,0,'Extract-level material.'),
('Green tea extract','Polyphenols–Flavonoids','uncharacterized/variable mixture',1,0,0,1,0,0,0,'Individual catechins handled separately.'),
('Glutathione','Endogenous antioxidant','endogenous-only for main-source classification',0,0,0,0,1,0,0,'Can be context node, not dietary-parent main universe.'),
('Uric acid','Endogenous antioxidant','endogenous metabolite',0,0,0,0,1,1,0,'Not dietary parent.'),
('N-acetylcysteine','Other','supplement/drug dominant',1,0,0,0,0,0,1,'Not normal dietary parent.'),
('Baicalin','Polyphenols–Flavonoids','medicinal-plant dominant; normal dietary exposure not established',1,1,0,0,0,0,1,'Excluded from main dietary universe.'),
('Silymarin','Other polyphenols','mixture and supplement/medicinal dominant',1,1,0,1,0,0,1,'Not a single defined dietary entity.'),
('Resveratrol supplement blend','Other polyphenols','supplement mixture',1,0,0,1,0,0,0,'trans-Resveratrol handled separately.'),
]

def pubchem(name):
 q=urllib.parse.quote(name,safe='')
 url=f'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{q}/property/Title,IUPACName,MolecularFormula,MolecularWeight,InChIKey/JSON'
 try:
  with urllib.request.urlopen(url,timeout=25) as resp: data=json.load(resp)
  p=data['PropertyTable']['Properties'][0]
  return {'PubChem_CID':p.get('CID',''),'canonical_name':p.get('Title') or p.get('IUPACName') or name,'molecular_formula':p.get('MolecularFormula',''),'molecular_weight':p.get('MolecularWeight',''),'InChIKey':p.get('InChIKey','')}
 except Exception as e:
  return {'PubChem_CID':'','canonical_name':name,'molecular_formula':'','molecular_weight':'','InChIKey':'','_error':str(e)}

cache_path=ROOT/'archive'/'phase2_pubchem_identity_cache.json'
cache=json.loads(cache_path.read_text(encoding='utf-8')) if cache_path.exists() else {}
for i,s in enumerate(spec):
 if s['compound'] not in cache:
  cache[s['compound']]=pubchem(s['compound'])
  cache_path.parent.mkdir(exist_ok=True); cache_path.write_text(json.dumps(cache,ensure_ascii=False,indent=2),encoding='utf-8')
  if (i+1)%20==0: print(f'PubChem progress {i+1}/{len(spec)}',flush=True)
  time.sleep(.05)
cache_path.parent.mkdir(exist_ok=True); cache_path.write_text(json.dumps(cache,ensure_ascii=False,indent=2),encoding='utf-8')

fields=['candidate_id','compound','canonical_name','synonym','PubChem_CID','InChIKey','molecular_formula','molecular_weight','parent_class','analysis_panel','subclass','structural_family','parent_or_conjugate','glycoside_or_aglycone','stereochemistry','isomer_status','dietary_parent_or_metabolite','representative_food_sources','food_occurrence_reference','food_occurrence_confidence','normal_dietary_exposure_yes_no','supplement_dominant_yes_no','medicinal_plant_dominant_yes_no','candidate_eligible','eligibility_rationale','exclusion_reason','likely_primary_ranking_construct','likely_secondary_construct','major_known_assay_risk','current_review_status','review_date','reviewer','key_identity_reference','legacy_note','notes']
def constructs(s):
 p=s['analysis_panel']
 if p=='Polyphenols–Flavonoids':return ('H-ORAC-FL','CUPRAC; lipid oxidation; mechanism','glycoside/aglycone; fluorescence/colored-compound interference')
 if 'Phenolic acids' in p:return ('H-ORAC-FL','CUPRAC; metal chelation; lipid oxidation','isomer/conjugate identity; intake-definition heterogeneity')
 if 'Stilbenes' in p:return ('subclass-appropriate H-ORAC or lipid assay','CUPRAC; mechanism; PK','low exposure; parent/metabolite confusion')
 if p=='Vitamins / vitamin-like':return ('vitamer-specific: H-ORAC/regeneration or L-ORAC/lipid termination','human oxidative biomarkers','water/lipid vitamers cannot share one metric')
 if p=='Carotenoids':return ('singlet-oxygen quenching or validated lipid-phase assay','lipid peroxidation; L-ORAC when appropriate','solubility; aggregation; oxygen tension; optical interference')
 if p=='Organosulfur compounds':return ('causal KEAP1/NRF2 / thiol-redox evidence','GSH/oxidative endpoints; PK','processing generation; instability; parent exposure')
 if p=='Betalains / nitrogen-containing':return ('fixed-protocol redox assay with optical QC','biological redox endpoints','strong optical/pH/stability interference')
 if p=='Other food-derived redox-active phytochemicals':return ('subclass-specific construct','mechanism; PK; lipid oxidation','strict dietary gate; low exposure; assay-specific artifacts')
 return ('biological cofactor relevance; no capacity rank','requirement; deficiency/supplementation; toxicity','chemical form; U-shaped risk; Fe/Cu prooxidant context')

out=[]
for i,s in enumerate(spec,1):
 ident=cache[s['compound']]; pcid=ident.get('PubChem_CID',''); key=ident.get('InChIKey','')
 unresolved=not(pcid and key)
 # Podophyllotoxin and several quinones are deliberately unresolved pending a stricter food-occurrence review.
 food_weak=s['compound'] in {'Podophyllotoxin','Plumbagin','Juglone','Thymoquinone','Ajoene','S-Allylmercaptocysteine','Ubiquinone-10','Astaxanthin','Fucoxanthin','Baicalein','Chrysin'}
 eligible='unresolved' if unresolved or food_weak else 'yes'
 confidence='low / unresolved' if food_weak else ('unresolved' if unresolved else 'moderate')
 primary,secondary,risk=constructs(s)
 source_ref='Phenol-Explorer / FooDB / authoritative food-composition or primary food-chemistry source; candidate-level source verification required before Phase 3'
 if s['parent_class']==M: source_ref='NIH ODS / EFSA-DRI / national food composition and intake sources'
 out.append({**{k:'' for k in fields},'candidate_id':f'AFF-{i:04d}','compound':s['compound'],'canonical_name':ident.get('canonical_name',s['compound']),'synonym':'','PubChem_CID':pcid,'InChIKey':key,'molecular_formula':ident.get('molecular_formula',''),'molecular_weight':ident.get('molecular_weight',''),'parent_class':s['parent_class'],'analysis_panel':s['analysis_panel'],'subclass':s['subclass'],'structural_family':s['structural_family'],'parent_or_conjugate':'defined conjugate' if 'conjugate' in s['glycoside_or_aglycone'] else 'parent/defined derivative','glycoside_or_aglycone':s['glycoside_or_aglycone'],'stereochemistry':s['stereochemistry'],'isomer_status':'isomer-specific where named; otherwise verify before Phase 3','dietary_parent_or_metabolite':s['dietary_parent_or_metabolite'],'representative_food_sources':s['representative_food_sources'],'food_occurrence_reference':source_ref,'food_occurrence_confidence':confidence,'normal_dietary_exposure_yes_no':'unresolved' if food_weak else 'yes','supplement_dominant_yes_no':'unresolved' if food_weak else 'no','medicinal_plant_dominant_yes_no':'unresolved' if food_weak else 'no','candidate_eligible':eligible,'eligibility_rationale':'Defined candidate with plausible normal-food occurrence; eligibility is independent of antioxidant performance.' if eligible=='yes' else 'Retained for Phase 2 resolution; identity or normal-food occurrence requires stronger candidate-level verification.','exclusion_reason':'','likely_primary_ranking_construct':primary,'likely_secondary_construct':secondary,'major_known_assay_risk':risk,'current_review_status':'identity resolved; food occurrence screening completed at class/source level' if eligible=='yes' else 'unresolved—do not rank','review_date':TODAY,'reviewer':'Codex initial curation; requires human second review','key_identity_reference':f'https://pubchem.ncbi.nlm.nih.gov/compound/{pcid}' if pcid else 'PubChem name query unresolved','legacy_note':'Historical rank intentionally omitted; see archive if applicable.','notes':ident.get('_error','')})

with open(DATA/'Antioxidant_Class_Candidate_Master.csv','w',newline='',encoding='utf-8-sig') as f:
 w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(out)
exf=['compound','proposed_class','exclusion_reason','supplement_dominant','medicinal_only','structure_unclear','mixture','endogenous_only','metabolite_only','insufficient_food_occurrence','notes']
with open(DATA/'Antioxidant_Candidate_Exclusions.csv','w',newline='',encoding='utf-8-sig') as f:
 w=csv.writer(f);w.writerow(exf);w.writerows(exclusions)
print(json.dumps({'candidates':len(out),'eligible':sum(r['candidate_eligible']=='yes' for r in out),'unresolved':sum(r['candidate_eligible']=='unresolved' for r in out),'exclusions':len(exclusions),'identity_unresolved':sum(not r['PubChem_CID'] for r in out)},ensure_ascii=False))
