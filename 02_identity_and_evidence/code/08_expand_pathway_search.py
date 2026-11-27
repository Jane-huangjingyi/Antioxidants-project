"""Systematic expansion search for pending compound x pathway cells via NCBI E-utilities.
Run from repo root: python 02_identity_and_evidence/code/08_expand_pathway_search.py all
Writes audit/Pathway_Expansion_Search_Results.csv; then run 07_build_pathway_framework.py to merge.
Abstract-level candidate evidence (ABSTRACT_ONLY) or NOT_REPORTED; all NOT_REVIEWED.
Incremental save + flushed progress for robustness."""
import csv, json, re, sys, time, urllib.request, urllib.parse
import xml.etree.ElementTree as ET
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
TBL = ROOT / "02_identity_and_evidence/result/table"

COMPOUND = {
 "Quercetin": ["quercetin"], "Catechin": ["catechin"], "Hesperetin": ["hesperetin"],
 "Genistein": ["genistein"], "Hesperidin": ["hesperidin"], "Myricetin": ["myricetin"],
 "p-Coumaric acid": ['"p-coumaric"', '"4-coumaric"', '"para-coumaric"', '"p-coumarate"'],
 "Chlorogenic acid": ['"chlorogenic acid"', '"5-caffeoylquinic"', '"5-CQA"'],
 "Gallic acid": ['"gallic acid"'], "Syringic acid": ['"syringic acid"'],
 "L-Ascorbic acid": ['"ascorbic acid"', "ascorbate", '"vitamin C"'],
 "Glutathione": ["glutathione", "GSH"],
}
PATHWAY = {
 "U1": ["NRF2", "NFE2L2", "KEAP1", '"antioxidant response element"'],
 "U2": ['"superoxide dismutase"', "SOD", "catalase", '"glutathione peroxidase"', "peroxiredoxin"],
 "U3": ["glutathione", "GSH", "GSSG", '"glutamate-cysteine ligase"'],
 "U4": ['"oxidative stress"', '"reactive oxygen species"', "ROS"],
 "U5": ["thioredoxin", "TXN", "peroxiredoxin", "PRDX", "TXNRD"],
 "U6": ["ferroptosis", "GPX4", "ACSL4", '"lipid peroxidation"', "malondialdehyde", '"4-hydroxynonenal"'],
 "U7": ["ascorbate", '"vitamin C"', '"ascorbic acid"'],
 "U8": ['"NADPH oxidase"', "NOX1", "NOX2", "NOX4", "p22phox", "p47phox", "NCF1"],
 "U9": ['"NF-kappa B"', "NFKB", "TLR4", '"nuclear factor kappa"'],
 "U10": ["PI3K", "AKT", '"phosphatidylinositol 3-kinase"'],
 "U11": ["MAPK", "JNK", "ERK", '"mitogen-activated protein"', "TAK1"],
 "U12": ["HIF1A", '"HIF-1"', '"hypoxia-inducible factor"'],
 "U13": ['"PGC-1"', "PPARGC1A", '"mitochondrial biogenesis"'],
 "U14": ["CFTR", '"cystic fibrosis transmembrane"'],
 "U15": ["AMPK", "PRKAA", "STK11", "LKB1"],
 "U16": ["FoxO", "FOXO1", "FOXO3"],
 "U17": ["apoptosis", "Bcl-2", "BAX", "caspase-3", "cleaved caspase"],
 "U18": ["autophagy", "mitophagy", "LC3", "Beclin", "PINK1", "Parkin"],
 "U19": ["NLRP3", "inflammasome", "caspase-1"],
 "U20": ["endoplasmic reticulum stress", "ER stress", "unfolded protein", "XBP1", "PERK", "ATF6", "GRP78"],
}
MODEL = re.compile(r"\b(cell|cells|mice|mouse|rat|rats|in vivo|in vitro|neuron|hepatocyte|macrophage|endotheli|hippocamp|cortex|zebrafish|C\. elegans|animal|murine)\b", re.I)

def ncbi_get(url, tries=4):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "research-workflow/1.0"})
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read()
        except Exception:
            time.sleep(1 + i)
    return None

EXCLUDE = {
 "Catechin": "NOT epicatechin NOT epigallocatechin NOT gallocatechin",
 "Quercetin": "NOT dihydroquercetin",
}

def search(compound, code, page_size=15):
    cq = " OR ".join(COMPOUND[compound]); pq = " OR ".join(PATHWAY[code])
    term = f"({cq}) AND ({pq})"
    if compound in EXCLUDE:
        term += " " + EXCLUDE[compound]
    es = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&retmode=json&retmax=%d&term=%s" % (page_size, urllib.parse.quote(term))
    d = ncbi_get(es); ids = []
    if d:
        try: ids = json.loads(d).get("esearchresult", {}).get("idlist", [])
        except Exception: pass
    if not ids: return term, []
    time.sleep(0.4)
    ef = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&retmode=xml&id=" + ",".join(ids)
    x = ncbi_get(ef); hits = []
    if x:
        try:
            root = ET.fromstring(x)
            for art in root.iter("PubmedArticle"):
                pmid = art.findtext(".//PMID", "")
                title = art.findtext(".//ArticleTitle", "") or ""
                ab = " ".join((t.text or "") for t in art.iter("AbstractText"))
                ptypes = [p.text for p in art.iter("PublicationType") if p.text]
                doi_el = art.find(".//ArticleIdList/ArticleId[@IdType='doi']")
                doi = doi_el.text if doi_el is not None else ""
                hits.append(dict(pmid=pmid, doi=doi, title=title, abstractText=ab,
                                 pubTypeList={"pubType": ptypes}, citedByCount=""))
        except Exception: pass
    return term, hits

def _match(term, text):
    t = term.strip('"').lower()
    return re.search(r'(?<![a-z])' + re.escape(t) + r'(?![a-z])', text) is not None

def screen(hit, compound, code):
    title = hit.get("title", "") or ""; ab = hit.get("abstractText", "") or ""
    text = (title + " " + ab).lower(); title_l = title.lower()
    comp_in_title = any(_match(t, title_l) for t in COMPOUND[compound])
    path_ok = any(_match(t, text) for t in PATHWAY[code])
    plist = [p.strip().lower() for p in hit.get("pubTypeList", {}).get("pubType", [])]
    is_review = any(p in ("review", "review-article") for p in plist)
    model_ok = bool(MODEL.search(ab))
    return comp_in_title and path_ok and model_ok and not is_review

def best_hit(compound, code):
    query, hits = search(compound, code)
    passed = [h for h in hits if screen(h, compound, code)]
    return query, hits, passed

FIELDS = ["compound","pathway_code","status","doi","pmid","title","cited_by","pub_type","abstract","query","n_hits","n_passed"]

def row_for(compound, code):
    query, hits, passed = best_hit(compound, code)
    if passed:
        h = passed[0]
        return dict(compound=compound, pathway_code=code, status="ABSTRACT_CANDIDATE",
                    doi=h.get("doi",""), pmid=h.get("pmid",""), title=h.get("title",""),
                    cited_by=h.get("citedByCount",""), pub_type=";".join(h.get("pubTypeList",{}).get("pubType",[])),
                    abstract=(h.get("abstractText","") or "")[:1200], query=query, n_hits=len(hits), n_passed=len(passed))
    return dict(compound=compound, pathway_code=code, status="NOT_REPORTED_IN_CHECKED_SET",
                doi="", pmid="", title="", cited_by="", pub_type="", abstract="", query=query, n_hits=len(hits), n_passed=0)

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "pilot"
    if mode == "pilot":
        for compound, code in [("Quercetin","U9"),("Quercetin","U6"),("Glutathione","U10"),("Genistein","U10"),("Myricetin","U11")]:
            query, hits, passed = best_hit(compound, code)
            print("\n" + "="*90, flush=True)
            print(f"{compound} x {code} | hits={len(hits)} passed={len(passed)}", flush=True)
            for h in (passed or hits)[:2]:
                print(f"  [{h.get('pmid')}] {h.get('doi')} | type={h.get('pubTypeList',{}).get('pubType')}", flush=True)
                print(f"    {h.get('title','')[:130]}", flush=True)
                print(f"    AB: {(h.get('abstractText','') or '')[:240]}", flush=True)
    elif mode == "all":
        mat = list(csv.DictReader((TBL / "07_pathway_framework_matrix.csv").open(encoding="utf-8-sig", newline="")))
        pending = [(m["compound"], m["pathway_code"]) for m in mat if m["cell_state"] == "PENDING_EXPANSION"]
        print("pending cells:", len(pending), flush=True)
        out = []; dest = TBL / "audit" / "Pathway_Expansion_Search_Results.csv"
        existing = {}
        if dest.exists():
            for r in csv.DictReader(dest.open(encoding="utf-8-sig", newline="")):
                existing[(r["compound"], r["pathway_code"])] = r
        for i, (compound, code) in enumerate(pending, 1):
            existing[(compound, code)] = row_for(compound, code)
            if i % 10 == 0 or i == len(pending):
                with dest.open("w", encoding="utf-8", newline="") as f:
                    w = csv.DictWriter(f, fieldnames=FIELDS, lineterminator="\n"); w.writeheader(); w.writerows(list(existing.values()))
                print(f"  {i}/{len(pending)} saved", flush=True)
            time.sleep(0.35)
        out = list(existing.values())
        from collections import Counter
        print("status counts:", dict(Counter(r["status"] for r in out)), flush=True)
        print("wrote expansion_results.csv", flush=True)
