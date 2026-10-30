import csv, os, statistics
from collections import defaultdict, Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
DOCS = os.path.join(ROOT, "docs")
TODAY = "2026-09-18"
PANEL = "Polyphenols - Phenolic acids / conjugates"

def read_csv(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

def write_csv(path, rows, fields):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader(); w.writerows(rows)

master = [r for r in read_csv(os.path.join(DATA, "Antioxidant_Class_Candidate_Master.csv")) if r["analysis_panel"] == PANEL]
by_name = {r["compound"].lower(): r for r in master}

holds = {
    "Feruloylquinic acid": "Generic name does not resolve acyl position; CID/InChIKey are absent.",
    "p-Coumaroylquinic acid": "Generic name/CID mapping does not state the positional isomer required for record-level matching.",
    "2,3-Dihydroxybenzoic acid": "Candidate-specific normal-food occurrence and dietary-parent status require confirmation; it is also reported as a human xenobiotic metabolite.",
    "3,4,5-Trimethoxybenzoic acid": "No free phenolic hydroxyl group; phenolic-space membership and normal-food gate require investigator confirmation."
}
position = {
    "Chlorogenic acid": "5-O-caffeoylquinic acid (current project mapping; historical naming may use 3-CQA)",
    "Neochlorogenic acid": "3-O-caffeoylquinic acid",
    "Cryptochlorogenic acid": "4-O-caffeoylquinic acid",
    "3,4-Dicaffeoylquinic acid": "3,4-di-O-caffeoylquinic acid",
    "3,5-Dicaffeoylquinic acid": "3,5-di-O-caffeoylquinic acid",
    "4,5-Dicaffeoylquinic acid": "4,5-di-O-caffeoylquinic acid",
}

lock=[]
for r in master:
    is_hold=r["compound"] in holds
    conjugated = "conjugate/ester" if ("quinic" in r["compound"].lower() or r["compound"] in {"Rosmarinic acid","Chicoric acid","Caftaric acid","Coutaric acid"}) else "free acid/defined phenolic"
    lock.append({
      "candidate_id":r["candidate_id"],"compound":r["compound"],"canonical_name":r["canonical_name"],"PubChem_CID":r["PubChem_CID"],"InChIKey":r["InChIKey"],
      "subclass":r["subclass"],"free_or_conjugated":conjugated,"positional_isomer":position.get(r["compound"],r["isomer_status"]),
      "molecular_formula":r["molecular_formula"],"molecular_weight":r["molecular_weight"],"representative_food_source":r["representative_food_sources"],
      "food_occurrence_reference":r["food_occurrence_reference"],"food_occurrence_verified":"hold—human confirmation required" if is_hold else "yes—carried forward from frozen Phase 2 candidate universe",
      "identity_verified":"hold—human confirmation required" if is_hold else "yes—CID/InChIKey/form locked for Phase 3B",
      "ranking_eligible":"hold" if is_hold else "eligible_for_ranking","hold_reason":holds.get(r["compound"],""),
      "reviewer":"Codex-assisted first review; human second review required before formal freeze","review_date":TODAY,
      "notes":"Candidate inclusion is independent of ORAC magnitude. Historical source names must still be matched at record level."
    })
write_csv(os.path.join(DATA,"PhenolicAcid_Phase3_Eligibility_Lock.csv"),lock,list(lock[0]))

records=[]
def add(compound,value,tier,study,year,journal,doi="",pmid="",location="",original_value=None,original_unit="mol TE/mol compound",formula="direct molar value",probe="fluorescein",radical="AAPH",arm="H-ORAC-FL",trolox="yes",temp="37 °C",medium="phosphate buffer; see original paper",purity="not numerically reported",optical="not reported",expid="",rationale="",zotero="pending_local_import",notes="",verification="verified from original full text/table"):
    m=by_name[compound.lower()]
    records.append({
      "evidence_id":"","candidate_id":m["candidate_id"],"compound":compound,"subclass":m["subclass"],"positional_isomer":position.get(compound,m["isomer_status"]),
      "free_or_conjugated":"conjugate/ester" if ("quinic" in compound.lower() or compound in {"Rosmarinic acid","Chicoric acid","Caftaric acid","Coutaric acid"}) else "free acid/defined phenolic",
      "independent_experiment_id":expid or f"{doi or study}::{compound}","study":study,"year":year,"journal":journal,"PMID":pmid,"DOI":doi,"Zotero_key":zotero,"exact_location":location,
      "original_value":original_value if original_value is not None else ("" if value is None else value),"original_unit":original_unit,"molecular_weight_used":m["molecular_weight"],"MW_source":m["key_identity_reference"],
      "conversion_formula":formula,"normalized_value_mol_TE_mol":"" if value is None else round(float(value),4),"probe":probe,"radical_generator":radical,"assay_arm":arm,"Trolox_used":trolox,
      "temperature":temp,"medium":medium,"purity":purity,"optical_QC":optical,"tier":tier,"tier_rationale":rationale,
      "independence_status":"independent original experiment" if tier in ("A","B1","B2","C") else "search/identity outcome only",
      "reviewer":"Codex-assisted extraction; independent human verification required","verification_status":verification,"notes":notes
    })

# Audited legacy records. The ambiguous Ou chlorogenic record is retained as X rather than mapped.
legacy = [
 ("Caffeic acid",4.37,"B1","Ou et al., Development and validation of improved ORAC using fluorescein",2001,"J Agric Food Chem","10.1021/jf010586o","11599998","Table 4, p. 4622","4.37","mol TE/mol compound","direct molar value","4FIGEV33"),
 ("Gallic acid",1.25,"B1","Carvalho et al., comparative antioxidant assay study",2023,"Antioxidants","10.3390/antiox12020505","36829987","Table 3","1.25","mol TE/mol compound","direct molar value","EHLKNP4E"),
 ("Caffeic acid",8.26,"B1","Carvalho et al., comparative antioxidant assay study",2023,"Antioxidants","10.3390/antiox12020505","36829987","Table 3","8.26","mol TE/mol compound","direct molar value","EHLKNP4E"),
 ("Ferulic acid",2.771,"B1","Paillat et al., chromatographic/ORAC comparison",2023,"Journal of Chromatographic Science","10.1093/chromsci/bmad007","36752411","Table I","2.771","mol TE/mol compound","direct molar value","pending_local_import"),
 ("Gentisic acid",5.475,"B1","Sakurai et al., phenolic-acid antioxidant comparison",2022,"RSC Advances","10.1039/D1RA08918H","","primary results table","5.475","mol TE/mol compound","direct molar value","pending_local_import"),
 ("p-Coumaric acid",3.766,"B1","Sakurai et al., phenolic-acid antioxidant comparison",2022,"RSC Advances","10.1039/D1RA08918H","","primary results table","3.766","mol TE/mol compound","direct molar value","pending_local_import"),
 ("Ferulic acid",3.474,"B1","Sakurai et al., phenolic-acid antioxidant comparison",2022,"RSC Advances","10.1039/D1RA08918H","","primary results table","3.474","mol TE/mol compound","direct molar value","pending_local_import"),
 ("4-Hydroxybenzoic acid",3.299,"B1","Sakurai et al., phenolic-acid antioxidant comparison",2022,"RSC Advances","10.1039/D1RA08918H","","primary results table","3.299","mol TE/mol compound","direct molar value","pending_local_import"),
 ("p-Coumaric acid",5.0,"B1","Rothe et al., phenolic-acid antioxidant comparison",2023,"European Food Research and Technology","10.1007/s00217-022-04135-3","","primary results table","5.000","mol TE/mol compound","direct molar value","pending_local_import")]
for c,v,t,s,y,j,d,p,l,ov,ou,fo,z in legacy:
    add(c,v,t,s,y,j,d,p,l,ov,ou,fo,expid=f"{d}::{c}",rationale="Original pure-compound AAPH–fluorescein–Trolox result; main assay identity and molar scale are traceable, but complete compound-specific QC is not reported.",zotero=z,notes="Migrated from the audited pre-class-balanced consolidation ledger.")

# Koroleva et al. 2014, Table 2: direct molar ORAC values.
for c,v in {"4-Hydroxybenzoic acid":2.17,"Vanillic acid":3.44,"Syringic acid":1.52,"Gallic acid":1.08,"p-Coumaric acid":5.02,"Ferulic acid":4.59,"Sinapic acid":2.94}.items():
    add(c,v,"B1","Koroleva et al., Evaluation of the Antiradical Properties of Phenolic Acids",2014,"International Journal of Molecular Sciences","10.3390/ijms150916351","25229820","Table 2 and ORAC methods",expid=f"KOROLEVA2014::{c}",rationale="Original pure-compound AAPH–fluorescein–Trolox experiment with linear concentration response; B1 because purity and compound-specific optical QC are incomplete.")

# Vulić et al. 2022: two concentrations in one experiment; one through-origin slope per compound prevents pseudo-replication.
two_point={"Protocatechuic acid":(30,57),"Gentisic acid":(29,53),"Gallic acid":(23,28),"Vanillic acid":(26,56),"Syringic acid":(29,40),"p-Coumaric acid":(20,33),"Caffeic acid":(31,60),"Ferulic acid":(26,45),"Sinapic acid":(25,44),"Rosmarinic acid":(50,92)}
for c,(y1,y2) in two_point.items():
    slope=(2.5*y1+5*y2)/(2.5**2+5**2)
    add(c,slope,"B1","Vulić et al., Investigation of Antioxidant Synergisms and Antagonisms among Phenolic Acids",2022,"Antioxidants","10.3390/antiox11091784","36139858","Table 2; Methods 2.2.2",f"{y1}; {y2}","µM TE at 2.5 and 5 µM compound","through-origin slope: Σ(concentration×µM TE)/Σ(concentration²)",expid=f"VULIC2022::{c}",rationale="Original pure-compound ORAC-FL experiment; AAPH/fluorescein/Trolox conditions traceable through the stated method. One slope summarizes the two within-study concentrations.",notes="The two concentrations are not counted as independent experiments.")

# Graton et al. pure protocatechuic-acid ORAC-FL result.
add("Protocatechuic acid",3.2,"B1","Graton et al., Comparative study between apocynin and protocatechuic acid",2022,"Frontiers in Physiology","10.3389/fphys.2022.1047916","36467568","Table 1; reagent list and antioxidant methods","3.2 ± 0.2","µmol Trolox/µmol compound","direct molar value",expid="GRATON2022::Protocatechuic acid",rationale="Original pure-compound AAPH–fluorescein–Trolox value with identifiable assay components; retained B1 because compound-specific linearity/optical QC is incomplete.")

# Zuo et al. 2021, Table 4, identity-resolved isolated CQA positional isomers.
cqa={"Neochlorogenic acid":1.47,"Cryptochlorogenic acid":3.54,"Chlorogenic acid":2.21,"3,4-Dicaffeoylquinic acid":3.26,"3,5-Dicaffeoylquinic acid":2.13,"4,5-Dicaffeoylquinic acid":3.70}
for c,v in cqa.items():
    add(c,v,"B1","Zuo et al., Valeriana rigida root extract: a new source of caffeoylquinic acids",2021,"Foods","10.3390/foods10051079","34068163","Table 4; Methods 2.4.3",expid=f"ZUO2021::{c}",purity="isolated and structurally assigned compound; see isolation/identification methods",rationale="Original identity-resolved pure-compound H-ORAC-FL value; explicit AAPH, fluorescein, Trolox, PBS pH 7.4, 37 °C and kinetic readout.",notes="Mapped only because the paper reports explicit 3-, 4-, 5-CQA and diCQA identities; generic historical chlorogenic records are not merged.")

# Ellagic acid mass-normalized value converted with the compound and Trolox molecular weights.
ell=(151.77/100)*(302.19/250.29)
add("Ellagic acid",ell,"B1","Hayes et al., Phenolic composition and in vitro antioxidant capacity of commercial phytochemical products",2011,"Food Chemistry","10.1016/j.foodchem.2010.11.092","","Table 1 and ORAC methods","151.77 ± 3.57","g Trolox/100 g dry compound","(151.77/100 g Trolox per g compound) × MW_compound(302.19)/MW_Trolox(250.29)",expid="HAYES2011::Ellagic acid",rationale="Original pure-compound AAPH–fluorescein–Trolox measurement, convertible from mass Trolox equivalents to molar ratio; complete optical QC is not reported.")

# Explicit non-ranking records and search outcomes.
add("Chlorogenic acid",None,"X","Ou et al., improved ORAC method—reported chlorogenic acid identity unresolved",2001,"J Agric Food Chem","10.1021/jf010586o","11599998","Table 4, p. 4622",original_value="3.14",original_unit="mol TE/mol reported chlorogenic acid",formula="not converted/mapped",expid="OU2001::ambiguous chlorogenic acid",rationale="The historical name cannot be mapped silently to a specific current-project positional isomer.",notes="HUMAN REVIEW REQUIRED—CAFFEOYLQUINIC IDENTITY. Excluded from numerical ranking pending source-form confirmation.",verification="original value traceable; candidate mapping unresolved")
add("Sinapic acid",None,"B2","Legacy figure-only sinapic-acid ORAC report",2022,"","","","figure only",original_value="figure-only",original_unit="not exactly extractable",formula="not applicable",probe="fluorescein",radical="AAPH",expid="LEGACY_FIGURE_ONLY::Sinapic acid",rationale="Figure-only result without an exact numerical value; supportive only and not pooled.",verification="non-extractable")

present={r["compound"] for r in records}
for m in master:
    if m["compound"] in present: continue
    reason=holds.get(m["compound"],"No original, identity-resolved, molar-convertible AAPH–fluorescein–Trolox value was located in the bounded Phase 3B search.")
    add(m["compound"],None,"X","Systematic Phase 3B search outcome",2026,"","","","PubMed/Google Scholar/Crossref/publisher/supplement search",original_value="",original_unit="",formula="",probe="unknown",radical="unknown",arm="not established",trolox="unknown",temp="",medium="",purity="",optical="",expid="",rationale=reason,notes="Missing eligible evidence is not evidence of low antioxidant capacity.",verification="search/eligibility outcome")

# Deduplicate and assign stable IDs.
dedup=[]; seen=set()
for r in records:
    key=(r["compound"],r["independent_experiment_id"],r["tier"],str(r["normalized_value_mol_TE_mol"]))
    if key in seen: continue
    seen.add(key); dedup.append(r)
records=dedup
for i,r in enumerate(records,1): r["evidence_id"]=f"PAC-E{i:03d}"
write_csv(os.path.join(DATA,"PhenolicAcid_H_ORAC_Evidence_Master.csv"),records,list(records[0]))

# Compound-level aggregation.
eligible=defaultdict(list)
for r in records:
    if r["tier"] in ("A","B1") and r["normalized_value_mol_TE_mol"] != "" and next(x for x in lock if x["compound"]==r["compound"])["ranking_eligible"]=="eligible_for_ranking":
        eligible[r["compound"]].append(float(r["normalized_value_mol_TE_mol"]))

rank=[]
for comp,vals in eligible.items():
    vals=sorted(vals); n=len(vals); med=statistics.median(vals); ratio=max(vals)/min(vals) if min(vals)>0 else 999
    hetero="high" if n>=2 and ratio>2 else ("moderate" if n>=2 and ratio>1.5 else "low/not estimable")
    confidence="High" if n>=3 and hetero!="high" else ("Moderate" if n>=2 else "Low")
    q=""
    if n>=4:
        qq=statistics.quantiles(vals,n=4,method="inclusive"); q=f"{qq[0]:.3f}–{qq[2]:.3f}"
    rr=[r for r in records if r["compound"]==comp and r["tier"] in ("A","B1") and r["normalized_value_mol_TE_mol"]!=""]
    m=by_name[comp.lower()]
    rank.append({"rank":"","compound":comp,"subclass":m["subclass"],"positional_isomer":position.get(comp,m["isomer_status"]),"PubChem_CID":m["PubChem_CID"],"InChIKey":m["InChIKey"],
      "median_H_ORAC":round(med,3),"min":round(min(vals),3),"max":round(max(vals),3),"IQR":q,"eligible_record_count":n,"confidence":confidence,
      "single_study_flag":"yes" if n==1 else "no","heterogeneity_flag":hetero,"identity_risk":"positional-isomer nomenclature controlled" if "quinic" in comp.lower() or comp=="Chlorogenic acid" else "low after candidate lock",
      "ranking_status":"Top available—not Top20" if len(eligible)<20 else "provisional Top20","key_DOI_PMID":"; ".join(sorted({x["DOI"] or x["PMID"] for x in rr if x["DOI"] or x["PMID"]})),
      "provenance_record_ids":";".join(x["evidence_id"] for x in rr),"caveat":"Single-study estimate." if n==1 else ("High historical dispersion; confidence not upgraded." if hetero=="high" else "Broadly comparable, non-identical historical protocols.")})
rank.sort(key=lambda x:float(x["median_H_ORAC"]),reverse=True)
for i,r in enumerate(rank,1): r["rank"]=i
rank_fields=["rank","compound","subclass","positional_isomer","PubChem_CID","InChIKey","median_H_ORAC","min","max","IQR","eligible_record_count","confidence","single_study_flag","heterogeneity_flag","identity_risk","ranking_status","key_DOI_PMID","provenance_record_ids","caveat"]
write_csv(os.path.join(DATA,"Polyphenols_PhenolicAcids_TopN_v1.0.csv"),rank,rank_fields)

# Candidate-level coverage by subclass.
rankset={r["compound"] for r in rank}
coverage=[]
for sub in sorted({m["subclass"] for m in master}):
    mm=[m for m in master if m["subclass"]==sub]; names={m["compound"] for m in mm}
    def ct(t): return len({r["compound"] for r in records if r["compound"] in names and r["tier"]==t})
    ab1=len({r["compound"] for r in records if r["compound"] in names and r["tier"] in ("A","B1") and r["normalized_value_mol_TE_mol"]!=""})
    coverage.append({"subclass":sub,"universe_N":len(mm),"ranking_eligible_N":sum(x["ranking_eligible"]=="eligible_for_ranking" for x in lock if x["subclass"]==sub),"A_B1_N":ab1,"B2_N":ct("B2"),"C_N":ct("C"),"X_N":ct("X"),"TopN_N":len(names & rankset)})
write_csv(os.path.join(DATA,"PhenolicAcid_Ranking_Coverage.csv"),coverage,list(coverage[0]))

# Lightweight human-review log; only unresolved decisions are recorded.
review_path=os.path.join(DATA,"Human_Review_Log.csv")
review_fields=["stage","compound","source","issue_type","issue_description","codex_recommendation","human_decision","reviewer","date","effect_on_ranking"]
existing=read_csv(review_path) if os.path.exists(review_path) else []
new=[]
for c,desc in holds.items():
    new.append({"stage":"Phase 3B","compound":c,"source":"Phase 2 candidate master / Phase 3B lock","issue_type":"candidate identity or food-occurrence gate","issue_description":desc,"codex_recommendation":"Keep on hold; do not rank until a unique dietary-parent structure and candidate-specific food occurrence are confirmed.","human_decision":"pending","reviewer":"","date":TODAY,"effect_on_ranking":"Candidate cannot enter current Top available list; future resolution could add a competitor."})
new.append({"stage":"Phase 3B","compound":"Chlorogenic acid","source":"Ou et al. 2001, DOI 10.1021/jf010586o","issue_type":"caffeoylquinic positional-isomer mapping","issue_description":"Reported name 'chlorogenic acid' does not by itself establish the current-project 5-O-CQA mapping.","codex_recommendation":"Retain as Tier X and exclude the 3.14 value unless supplier/CAS/structure confirms the positional isomer.","human_decision":"pending","reviewer":"","date":TODAY,"effect_on_ranking":"Including this value would change the chlorogenic-acid median and may move its rank."})
for r in rank:
    if r["heterogeneity_flag"] == "high":
        new.append({"stage":"Phase 3B","compound":r["compound"],"source":r["key_DOI_PMID"],"issue_type":"high historical heterogeneity","issue_description":f"Eligible historical range {r['min']}–{r['max']} mol TE/mol; max/min exceeds 2.","codex_recommendation":"Retain provisional median, do not upgrade confidence, and obtain second-reviewer protocol/outlier assessment before formal freeze.","human_decision":"pending","reviewer":"","date":TODAY,"effect_on_ranking":"Provisional ranking may continue because no Top20 cutoff is being frozen; sensitivity result must accompany the rank."})
seen_review={(x.get("stage"),x.get("compound"),x.get("source"),x.get("issue_type")) for x in existing}
existing.extend(x for x in new if (x["stage"],x["compound"],x["source"],x["issue_type"]) not in seen_review)
write_csv(review_path,existing,review_fields)

print("Universe",len(master),"Lock",Counter(x["ranking_eligible"] for x in lock))
print("Evidence",len(records),Counter(x["tier"] for x in records))
print("Rankable",len(rank),"Top5",[(x["compound"],x["median_H_ORAC"]) for x in rank[:5]])
