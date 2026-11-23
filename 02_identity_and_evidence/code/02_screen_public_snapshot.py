"""Run a reproducible discovery screen on accessible Stage 2 records."""
import csv
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
import unicodedata
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
STAGE = HERE.parent / "05_multidatabase_retrieval"
CACHE = HERE.parent / "01_systematic_supplement/inputs/stage2_v1_1/pubmed_v1"
LOCAL = ROOT / "download_raw/stage2_machine_screening"
VERSION = "title_abstract_triage_v0.2"

METHODS = {
    "ORAC_FAMILY": r"\borac\b|oxygen radical absorb(?:ance|tion) capacity",
    "ORAC_PGR": r"\borac[ -]pgr\b|pyrogallol red",
    "CROCIN_BLEACHING": r"crocin.{0,18}bleach|bleach.{0,18}crocin",
    "ABTS": r"\babts\b", "DPPH": r"\bdpph\b", "FRAP": r"\bfrap\b|ferric reducing antioxidant",
    "CUPRAC": r"\bcuprac\b|cupric reducing antioxidant",
}
ACTIVITY = re.compile(r"antioxidant (?:activity|capacit|potency)|(?:radical|peroxyl).{0,12}scaveng|trolox equivalent")
NUMERIC = re.compile(r"\d\s*(?:mg|[μµu]?mol|[μµu]m\b|mmol|%)|[ies]c\s*50|trolox equivalent")
DETECTION = re.compile(r"\b(?:hplc|uplc|lc-ms|gc-ms|chromatograph\w+|spectrometr\w+|quantif\w+|detection limit|analytical method)\b")
FOOD = re.compile(r"\b(?:food|dietary|edible|fruit|vegetable|tea|coffee|cocoa|grain|wine|milk|seed|spice)\w*\b")
FACTORS = re.compile(r"\b(?:processing|storage|temperature|ripening|cultivar|stability|solvent|ph|extraction|cooking|fermentation)\b")
METHOD_PATTERNS = {tag:re.compile(expr) for tag,expr in METHODS.items()}
REFERENCE = HERE.parent/"inputs/provenance/results1_v1.0"
PROFILE_FILE = HERE.parent/"result/table/candidate_evidence_profiles.csv"
TABLE = HERE.parent/"result/table"
AUDIT = TABLE/"audit"
SEARCH_ALIASES = HERE.parent/"06_machine_screening/Search_Alias_Leads.csv"


def rows(path):
    with path.open(encoding="utf-8-sig", newline="") as source:
        return list(csv.DictReader(source))


def save(path, records):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(records[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(records)


def normalized(value):
    return re.sub(r"\s+", " ", unicodedata.normalize("NFKC", value).casefold()).strip()


def txt(node):
    return " ".join(node.itertext()) if node is not None else ""


def pubmed():
    ref = {r["PMID"]:r for r in rows(STAGE/"PubMed_Identifier_Reconciliation.csv")}
    observed = set()
    for batch in rows(STAGE/"PubMed_Export_Manifest.csv"):
        f = CACHE/batch["raw_file"]
        payload = f.read_bytes()
        if hashlib.sha256(payload).hexdigest() != batch["sha256"]:
            raise ValueError(f"Raw XML digest mismatch: {f}")
        items = ET.fromstring(payload)
        actual = 0
        for parent in items:
            article = parent.find("MedlineCitation/Article")
            pmid = parent.findtext("MedlineCitation/PMID") or parent.findtext("BookDocument/PMID")
            if pmid is None or pmid in observed or pmid not in ref:
                raise ValueError(f"Unexpected PMID: {pmid!r}")
            observed.add(pmid)
            actual += 1
            meta = ref[pmid]
            abstract_node = article if article is not None else parent.find("BookDocument")
            abstract = " ".join(txt(n) for n in abstract_node.findall("./Abstract/AbstractText")) if abstract_node is not None else ""
            pub_types = {n.text for n in parent.findall(".//PublicationTypeList/PublicationType")}
            comment_types = {n.get("RefType") for n in parent.findall(".//CommentsCorrections")}
            retracted = "Retracted Publication" in pub_types or "RetractionIn" in comment_types
            notice = "Retraction of Publication" in pub_types or "RetractionOf" in comment_types
            correction = bool(comment_types & {"ErratumIn","ErratumFor","ExpressionOfConcernIn","ExpressionOfConcernFor","UpdateIn"})
            review = bool(pub_types & {"Review","Systematic Review","Meta-Analysis"})
            yield meta, abstract, retracted, notice, correction, review
        assert actual == int(batch["PMIDs"])
    assert observed == set(ref)


def matcher(profiles):
    aliases = defaultdict(set)
    for row in profiles:
        for field in ("compound_name","reference_name"):
            term = normalized(row[field])
            if len(term)>=5 and row["inchi_key"]:
                aliases[term].add(row["candidate_id"])
    for row in rows(SEARCH_ALIASES):
        aliases[normalized(row["search_term"])].add(row["candidate_id"])
    # Longest match prevents counting catechin inside catechin gallate.
    ordered = sorted(aliases,key=lambda s:(-len(s),s))
    return aliases,re.compile(r"(?<![\w-])(?:"+"|".join(re.escape(term) for term in ordered)+r")(?![\w-])")


def make_roles(text, has_abstract):
    tags = [label for label, pattern in METHOD_PATTERNS.items() if pattern.search(text)]
    # An ORAC mention alone still needs probe and result confirmation.
    role = []
    if tags or ACTIVITY.search(text):
        role.append("ACTIVITY_QUANT_LEAD" if has_abstract and NUMERIC.search(text) else "ACTIVITY_METHOD_MENTION")
    if DETECTION.search(text):
        role.append("ANALYTICAL_DETECTION_LEAD")
    if FOOD.search(text):
        role.append("FOOD_OCCURRENCE_LEAD")
    if FACTORS.search(text) and (FOOD.search(text) or tags):
        role.append("CONDITION_OR_PROCESSING_LEAD")
    return tags, role


def main():
    LOCAL.mkdir(parents=True,exist_ok=True)
    europe = {r["article_key"]:r for r in rows(CACHE.parent/"Public_Article_Register.csv")}
    assert set(europe) == {r["article_key"] for r in rows(STAGE/"Public_Article_Search_Origins.csv")}
    profiles = rows(PROFILE_FILE)
    names = {r["candidate_id"]:r["compound_name"] for r in profiles}
    aliases, pattern = matcher(profiles)
    records = {}
    def add(key, doi, pmid, title, text, database, state, retracted=False, notice=False, correction=False, review=False):
        rec = records.setdefault(key, dict(article_key=key, doi=doi, pmid=pmid, title=title, databases=set(),
                            text="", has_abstract=False, confidence=state, retracted=False,
                            notice=False, correction=False, review=False))
        rec["databases"].add(database)
        if text:
            rec["text"] = " ".join(dict.fromkeys(filter(None,(rec["text"], text))))
            rec["has_abstract"] = True
        if pmid:
            rec["pmid"]=pmid
        rec["retracted"] |= retracted
        rec["notice"] |= notice
        rec["correction"] |= correction
        rec["review"] |= review
    for source_key, row in sorted(europe.items()):
        key = "DOI:"+row["doi"].casefold() if row["doi"] else "PMID:"+row["PMID"] if row["PMID"] else source_key
        add(key,row["doi"],row["PMID"],row["title"],"", "Europe_PMC", "EUROPE_PMC_PROVISIONAL_KEY")
    for row,abstract,linked,notice,correction,review in pubmed():
        key=row["provisional_report_key"] or "PENDING_PMID:"+row["PMID"]
        add(key,row["doi"],row["PMID"],row["title"],abstract,"PubMed",row["reconciliation_status"],
            linked,notice,correction,review)
    wos_status = {}
    intake = LOCAL.parent/"stage2_institutional"
    for row in rows(intake/"WoS_Local_Reconciliation.csv"):
        wos_status[row["accession"]] = row
    for row in rows(intake/"Institutional_Normalized_Records.csv"):
        if row["database"] != "wos":
            continue
        audit = wos_status[row["accession"]]
        matched = audit["matched_keys"]
        key = matched if audit["status"] == "EXISTING_REPORT_KEY_LINK" and matched in records else row["accession"]
        add(key,row["doi"],row["pmid"],row["title"],row["abstract"],"WoS_local",audit["status"])
        records[key]["identifier_hold"] = audit["status"] in {"IDENTIFIER_REVIEW_PENDING","TITLE_REVIEW_PENDING"}
    legacy_links = defaultdict(set)
    inherited_totals = defaultdict(set)
    for row in rows(STAGE/"Candidate_Article_Links.csv"):
        legacy_links[row["article_key"]].add(row["candidate_id"])
        if row["candidate_id"] in names:
            inherited_totals[row["candidate_id"]].add(row["article_key"])
    report, links = [], []
    counts = Counter()
    cross = defaultdict(Counter)
    audit_groups = defaultdict(list)
    for key, r in sorted(records.items()):
        text = normalized(r["title"]+" "+r["text"])
        mentions = defaultdict(set)
        ambiguous = set()
        for match in pattern.finditer(text):
            term = match.group()
            if len(aliases[term])==1:
                mentions[next(iter(aliases[term]))].add(term)
            else:
                ambiguous.add(term)
        tags,roles=make_roles(text,r["has_abstract"])
        if r["retracted"] or r["notice"]:
            disposition="RETRACTION_RECORD_HOLD"
        elif r["correction"] or r.get("identifier_hold") or key.startswith("PENDING_PMID:"):
            disposition="IDENTIFIER_OR_CORRECTION_HOLD"
        elif r["review"]:
            disposition="CONTEXT_REVIEW_OR_CITATION_CHASE"
        elif "ORAC_FAMILY" in tags and mentions:
            disposition="HIGH_PRIORITY_ORAC_FULLTEXT"
        elif roles and mentions:
            disposition="EVIDENCE_ROLE_FULLTEXT_QUEUE"
        elif not r["title"] and not r["has_abstract"]:
            disposition="METADATA_MISSING"
        elif not r["has_abstract"]:
            disposition="TITLE_ONLY_ABSTRACT_PENDING"
        else:
            disposition="LOW_PRIORITY_OR_UNRESOLVED"
        candidates= set(mentions) | (legacy_links[key] & names.keys())
        for cid in sorted(candidates):
            direct=bool(mentions[cid])
            cross[cid]["union_report_links"]+=1
            cross[cid]["direct_name_reports"]+=direct
            cross[cid]["orac_priority_name_reports"]+=bool(direct and disposition=="HIGH_PRIORITY_ORAC_FULLTEXT")
            links.append(dict(article_key=key,doi=r["doi"],candidate_id=cid,compound=names[cid],
                              matched_name_terms=";".join(sorted(mentions[cid])),
                              evidence_role_leads=";".join(roles),assay_mentions=";".join(tags),
                              association="NAME_LEAD" if direct else "INHERITED_LINK_ONLY",
                              status="PENDING_MATERIAL_AND_ELIGIBILITY"))
        row=dict(article_key=key,doi=r["doi"],pmid=r["pmid"],title=r["title"],
            databases=";".join(sorted(r["databases"])),abstract_checked="YES" if r["has_abstract"] else "NO",
            assay_mentions=";".join(tags),candidate_name_hits=len(mentions),ambiguous_names=";".join(sorted(ambiguous)),
            evidence_role_leads=";".join(roles),disposition=disposition,automated_exclusion="NO",
            final_inclusion="NOT_ADJUDICATED",screen_version=VERSION)
        counts.update([disposition])
        report.append(row)
        audit_groups[disposition].append(row)
    save(LOCAL/"Report_Screening.csv",report)
    save(LOCAL/"Candidate_Report_Links.csv",links)
    controls=[]
    for row in rows(STAGE/"Public_Database_DOI_Controls.csv"):
        matched=[r for r in report if r["doi"].lower()==row["doi"].lower()]
        controls.append(dict(doi=row["doi"],control_role=row["control_role"],screened_records=len(matched),
                             dispositions=";".join(sorted({r["disposition"] for r in matched})),
                             fulltext_verified_by_this_pass="NO"))
    save(AUDIT/"Anchor_Recall_Pilot.csv",controls)
    sample=[]
    for status, group in sorted(audit_groups.items()):
        selected=sorted(group,key=lambda r:hashlib.sha256((VERSION+r["article_key"]).encode()).digest())[:25]
        sample.extend(dict(**r,audit_outcome="PENDING") for r in selected)
    save(LOCAL/"Recall_Audit_Sample.csv",sample)
    save(TABLE/"01_candidate_report_coverage.csv",[
        dict(candidate_id=cid,compound=names[cid],historical_linked_report_keys=len(inherited_totals[cid]),
             public_union_report_links=cross[cid]["union_report_links"],direct_name_reports=cross[cid]["direct_name_reports"],
             orac_priority_name_reports=cross[cid]["orac_priority_name_reports"],final_included_reports="")
        for cid in sorted(names)])
    index = defaultdict(set)
    for item in rows(REFERENCE/"original_observations.csv"):
        index[item["doi"]].add(item["assay"])
    rank_counts = Counter(r["doi"] for r in rows(REFERENCE/"assay_specific_reference_ranks.csv"))
    model_counts = Counter(r["doi"] for r in rows(ROOT/"03_candidate_selection/result/table/01_connected_model_input.csv"))
    for doi in model_counts:
        index.setdefault(doi,set()).add("ORAC-FL")
    save(TABLE/"03_quantitative_report_crosswalk.csv",[
        dict(doi=doi,known_quantitative_assays=";".join(sorted(index[doi])),
             ranked_rows_v1=rank_counts[doi],connected_model_rows_increment=model_counts[doi],
             study_independence="VERIFY_SOURCE_EXPERIMENT",source_use="EXISTING_TARGETED_NUMERIC_EVIDENCE")
        for doi in sorted(index)])
    summary=dict(version=VERSION,pubmed_unique_pmids=sum("PubMed" in r["databases"] for r in records.values()),
                 europe_pmc_route_keys=len(europe),local_wos_accessions=len(wos_status),
                 provisional_intake_union=len(report),
                 shared_pubmed_europe_pmc_keys=sum({"PubMed","Europe_PMC"} <= r["databases"] for r in records.values()),
                 wos_linked_to_public_keys=sum("WoS_local" in r["databases"] and len(r["databases"])>1 for r in records.values()),
                 abstract_checked=sum(r["has_abstract"] for r in records.values()),
                 title_only=sum(bool(r["title"]) and not r["has_abstract"] for r in records.values()),
                 no_title_or_abstract=sum(not r["title"] and not r["has_abstract"] for r in records.values()),
                 candidate_covered=sum(bool(cross[cid]["union_report_links"]) for cid in names),
                 machine_dispositions=dict(counts),candidate_profiles=len(names),
                 candidate_report_links=len(links),audit_sample_rows=len(sample),
                 automated_exclusions=0,final_systematic_inclusion_completed=False,
                 dates="Search window 2020-01-01 to 2026-11-17; article-level first-publication eligibility pending")
    (AUDIT/"Screening_Summary.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf8")
    print(json.dumps(summary,indent=2))


if __name__ == "__main__":
    main()
