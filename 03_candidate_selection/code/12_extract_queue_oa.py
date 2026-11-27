"""Reproducible OA full-text extraction for the single-compound ORAC queue subset.
Fetches OA full texts (NCBI PMC) and extracts ORAC evidence snippets + unit/error/protocol signals
for researcher review (NOT auto-approved). Run: python 03_candidate_selection/code/12_extract_queue_oa.py
"""
import csv, json, re, sys, time, urllib.request, urllib.parse
import xml.etree.ElementTree as ET
from pathlib import Path
from collections import Counter
sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "03_candidate_selection/12_evidence_expansion"
TRI = OUT / "queue_scope_triage_2026-11-27.csv"
leads = [r for r in csv.DictReader(TRI.open(encoding="utf-8-sig", newline="")) if r["eligible_for_extraction"] == "YES"]

def get(url, tries=3):
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "research/1.0"}), timeout=45) as r:
                return r.read()
        except Exception:
            time.sleep(1 + i)
    return None

# batched EPMC DOI -> pmid/pmcid/oa
meta = {}
dois = [r["doi"] for r in leads]
for i in range(0, len(dois), 20):
    q = " OR ".join('DOI:"%s"' % d for d in dois[i:i+20])
    d = get("https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=" + urllib.parse.quote(q) + "&format=json&resultType=core&pageSize=25")
    if d:
        try:
            for r in json.loads(d).get("resultList", {}).get("result", []):
                meta[(r.get("doi") or "").lower()] = r
        except Exception: pass
    time.sleep(0.3)

ORAC = re.compile(r"ORAC|oxygen radical absorbance", re.I)
UNIT = re.compile(r"(µM|μM|uM|mmol|mol|µmol|μmol)\s*(TE|Trolox)|TE\s*/|Trolox equivalent", re.I)
ERR = re.compile(r"\bSD\b|\bSEM\b|standard deviation|standard error|n\s*=\s*\d|triplicate|independent (experiment|preparation)", re.I)
PROT = re.compile(r"fluorescein|AAPH|pH\s*7\.4|37\s*°?C|Trolox|net AUC|area under", re.I)

out = []
for r in leads:
    m = meta.get(r["doi"].lower(), {})
    pmcid = m.get("pmcid", ""); oa = m.get("inEPMC", "") == "Y"
    rec = dict(doi=r["doi"], candidate_ids=r["candidate_ids"], title=r["title"], pmid=m.get("pmid", ""),
               pmcid=pmcid, oa="YES" if oa else "NO", n_snip=0, snippets="", unit_sig="", err_sig="", prot_sig="",
               ready_for_review="NO")
    if oa and pmcid:
        raw = get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id=" + pmcid.replace("PMC", "") + "&rettype=xml&retmode=xml")
        if raw:
            try:
                doc = ET.fromstring(raw)
                texts = [" ".join("".join(p.itertext()).split()) for p in doc.iter("p")]
                texts += [" ".join("".join(c.itertext()).split()) for c in doc.iter("caption")]
                snips = [t for t in texts if ORAC.search(t) and (UNIT.search(t) or ERR.search(t) or PROT.search(t))]
                rec["n_snip"] = len(snips)
                rec["snippets"] = " || ".join(snips[:3])[:1500]
                alltxt = " ".join(texts)
                rec["unit_sig"] = "YES" if UNIT.search(alltxt) else "NO"
                rec["err_sig"] = "YES" if ERR.search(alltxt) else "NO"
                rec["prot_sig"] = "YES" if PROT.search(alltxt) else "NO"
                rec["ready_for_review"] = "YES" if snips else "NO"
            except Exception: pass
        time.sleep(0.3)
    out.append(rec)
with (OUT / "queue_oa_extraction_2026-11-27.csv").open("w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0]), lineterminator="\n"); w.writeheader(); w.writerows(out)
c = Counter(x["oa"] for x in out)
summary = dict(single_compound_leads=len(out), oa=dict(c),
               ready_for_review=sum(x["ready_for_review"] == "YES" for x in out),
               note="OA full-text ORAC snippets for researcher review; values NOT auto-extracted/approved; six-gate intake required before refit.")
(OUT / "queue_oa_extraction_2026-11-27_qc.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
print("leads:", len(out), "| OA:", dict(c), "| ready:", summary["ready_for_review"])
