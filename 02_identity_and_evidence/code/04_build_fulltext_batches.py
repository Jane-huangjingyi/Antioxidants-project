"""Route the entire priority queue to reproducible full-text work batches."""
from collections import Counter, defaultdict
import hashlib
import json
import re
import xml.etree.ElementTree as ET

from importlib import import_module

screen = import_module("02_screen_public_snapshot")
CACHE, AUDIT, LOCAL, STAGE = screen.CACHE, screen.AUDIT, screen.LOCAL, screen.STAGE
rows, save = screen.rows, screen.save

XML_CACHE = CACHE.parents[1].parent/"fulltext_xml"
BATCH_SIZE = 25
ORAC = re.compile(r"\borac\b|oxygen radical absorb(?:ance|tion) capacity", re.I)
SCALE = re.compile(r"trolox|\bte\s*/\s*(?:mol|g|mg)", re.I)


def checkpoint_ids():
    by_key, by_doi = defaultdict(set), defaultdict(set)
    for path in (STAGE/"Deduplicated_Article_Register.csv", STAGE/"PubMed_Identifier_Reconciliation.csv",
                 CACHE.parent/"Public_Article_Register.csv"):
        for row in rows(path):
            pmcid = row.get("PMCID", "").upper()
            if not re.fullmatch(r"PMC\d+", pmcid):
                continue
            for key in (row.get("article_key"),row.get("provisional_report_key")):
                if key:
                    by_key[key].add(pmcid)
            if row["doi"]:
                by_doi[row["doi"].lower()].add(pmcid)
    return by_key, by_doi


def inspect_xml(path, expected_doi, expected_pmcid):
    raw = path.read_bytes()
    try:
        document = ET.fromstring(raw)
    except ET.ParseError:
        return "XML_INVALID", "", 0, 0
    meta = document.find("./front/article-meta")
    body = document.find("./body")
    if meta is None or body is None:
        return "NO_ARTICLE_BODY", "", 0, 0
    ids = {n.get("pub-id-type"): (n.text or "").strip().lower() for n in meta.findall("./article-id")}
    article_pmcid = ids.get("pmc") or ids.get("pmcid") or ""
    if article_pmcid and article_pmcid.removeprefix("pmc") != expected_pmcid.lower().removeprefix("pmc"):
        return "SOURCE_ID_CONFLICT", "", 0, 0
    if expected_doi and ids.get("doi") and ids["doi"] != expected_doi:
        return "SOURCE_ID_CONFLICT", "", 0, 0
    if not article_pmcid and not (expected_doi and ids.get("doi") == expected_doi):
        return "SOURCE_ID_UNCONFIRMED", "", 0, 0
    content = " ".join(body.itertext())
    tables = [" ".join(tbl.itertext()) for tbl in body.iter("table-wrap")]
    hits = sum(bool(ORAC.search(t) and SCALE.search(t)) for t in tables)
    status = "XML_TABLE_PRIORITY" if hits else "XML_TEXT_PRIORITY" if ORAC.search(content) else "XML_OTHER_SCOPE"
    return status,hashlib.sha256(raw).hexdigest(),len(tables),hits


def main():
    priority = rows(LOCAL/"ORAC_Fulltext_Review_Queue.csv")
    assert len(priority) == len({r["article_key"] for r in priority}) == 567
    keys, dois = checkpoint_ids()
    review = AUDIT.parents[2]/"inputs/provenance/Fulltext_Scope_Review.csv"
    completed = {r["doi"]:r for r in rows(review)}
    assert completed.keys() <= {r["doi"] for r in priority}
    work = []
    for item in priority:
        ids = keys[item["article_key"]] | dois[item["doi"]]
        pmcid = next(iter(ids)) if len(ids) == 1 else ""
        digest, tables, hits = "", 0, 0
        path = XML_CACHE/f"{pmcid}.xml"
        if len(ids) > 1:
            route = "PMCID_CONFLICT"
        elif not pmcid:
            route = "PUBLISHER_OR_REPOSITORY_LOOKUP"
        elif not path.is_file():
            route = "PMC_XML_ACCESS_PENDING"
        else:
            route,digest,tables,hits = inspect_xml(path,item["doi"],pmcid)
        review = completed.get(item["doi"], {})
        if review:
            assert review["pmcid"] == pmcid and digest
            assert review["human_review_status"] == "NOT_REVIEWED"
            item["review_status"] = "CACHED_XML_SCOPE_RECORDED"
        work.append(dict(**item,PMCID=pmcid,access_route=route,local_xml_sha256=digest,
                         jats_table_count=tables,orac_and_trolox_table_leads=hits,
                         fulltext_scope=review.get("scope",""),
                         quantitative_disposition=review.get("quantitative_disposition",""),
                         final_eligibility="PENDING"))
    order = {name:index for index,name in enumerate(("XML_TABLE_PRIORITY","XML_TEXT_PRIORITY",
             "XML_OTHER_SCOPE","PMC_XML_ACCESS_PENDING","PUBLISHER_OR_REPOSITORY_LOOKUP"))}
    work.sort(key=lambda r:(order.get(r["access_route"],len(order)), -r["orac_and_trolox_table_leads"],
                           -int(r["names_linked"]),r["article_key"]))
    batches = Counter()
    for row in work:
        row["batch_id"] = ""
        if row["review_status"] in {"PENDING_NEW_SCOPE","EXISTING_ACCESS_OR_SCOPE_QUEUE"}:
            route = row["access_route"]
            batches[route] += 1
            row["batch_id"] = f"{route}-{1+(batches[route]-1)//BATCH_SIZE:03d}"
    assert sum(batches.values()) == sum(bool(r["batch_id"]) for r in work)
    save(LOCAL/"ORAC_Fulltext_Batches.csv",work)
    access = Counter(r["access_route"] for r in work)
    summary = dict(priority_reports=len(work),all_access_routes=dict(sorted(access.items())),
                   pending_routes=dict(sorted(batches.items())),batch_size=BATCH_SIZE,
                   number_of_pending_batches=len({r["batch_id"] for r in work if r["batch_id"]}),
                   source_identity_checked_local_xml=sum(bool(r["local_xml_sha256"]) for r in work),
                   review_status=dict(sorted(Counter(r["review_status"] for r in work).items())),
                   new_scientific_inclusions_applied=0)
    (AUDIT/"Fulltext_Batch_Summary.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(summary,indent=2))


if __name__ == "__main__":
    main()
