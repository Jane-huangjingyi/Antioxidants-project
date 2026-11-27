"""Top-down pathway framework: map the checked mechanism observations onto the curated
antioxidant pathway universe (U1-U14), grade each compound x pathway cell, and mark
unchecked cells PENDING_EXPANSION. Phased approach: framework now from existing evidence,
expansion register tracks cells to fill later. Run from repo root:
python 02_identity_and_evidence/code/07_build_pathway_framework.py"""
import csv, json, re, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
TBL = ROOT / "02_identity_and_evidence/result/table"
AUDIT = TBL / "audit"
MECH = TBL / "04_candidate_in_vivo_mechanism_evidence.csv"
UNIV = AUDIT / "Pathway_Universe_Curated.csv"
RANK = ROOT / "03_candidate_selection/result/table/04_figure1_candidate_ranks.csv"

univ = list(csv.DictReader(UNIV.open(encoding="utf-8-sig", newline="")))
UCODES = [u["pathway_code"] for u in univ]
UNAME = {u["pathway_code"]: u["pathway_name"] for u in univ}
UCLASS = {u["pathway_code"]: u["pathway_class"] for u in univ}

# Keyword rules grounded in molecular_node / redox_endpoint / pathway_or_process.
# Each rule: (pathway_code, compiled regex, basis label). GPX4 excluded from U2 (ferroptosis U6).
RULES = [
    ("U1", re.compile(r"NFE2L2|NRF2|KEAP1|SQSTM1|p62|HMOX1|HO-1|NQO1|GCLC|GCLM", re.I), "NRF2/KEAP1/ARE node"),
    ("U2", re.compile(r"\bSOD\b|superoxide dismutase|\bCAT\b|catalase|\bGST\b|GPx(?!4)|glutathione peroxidase|peroxiredoxin|PRDX", re.I), "SOD/CAT/GPx/GST detox enzyme activity"),
    ("U3", re.compile(r"\bGSH\b|GSSG|glutathione|GCLC|GCLM", re.I), "GSH/GSSG content or GCL synthesis"),
    ("U4", re.compile(r"\bROS\b|DHE|superoxide|protein carbonyl|TBARS|reactive oxygen|oxidative stress", re.I), "ROS generation/scavenging or oxidative-stress readout"),
    ("U5", re.compile(r"thioredoxin|TXNRD|\bTXN\b|TXNIP", re.I), "thioredoxin system node"),
    ("U6", re.compile(r"GPX4|ACSL4|ferroptosis|\bMDA\b|malondialdehyde|4-HNE|4HNE|HPNE|isoprostane|oxidized LDL|oxLDL|lipid peroxidation", re.I), "ferroptosis (GPX4/ACSL4) or lipid-peroxidation marker"),
    ("U7", re.compile(r"ascorbate|ascorbic|vitamin C|\bGulo\b", re.I), "ascorbate metabolism/disposition"),
    ("U8", re.compile(r"p22phox|p47phox|p67phox|NADPH oxidase|\bNOX\b|CYBA|NCF1|NCF2", re.I), "NADPH oxidase subunit/NOX"),
    ("U9", re.compile(r"\bNF-κB\b|\bNF-kB\b|\bNFKB\b|\bTLR4\b|\bRELA\b", re.I), "NF-kB/TLR4 node"),
    ("U10", re.compile(r"PI3K|\bAKT\b", re.I), "PI3K/AKT node"),
    ("U11", re.compile(r"TAK1|\bp38\b|JNK|MAPK", re.I), "MAPK stress node"),
    ("U12", re.compile(r"HIF1A|HIF-1", re.I), "HIF1A node"),
    ("U13", re.compile(r"PGC-1|PPARGC1A", re.I), "PGC-1alpha node (cell-only in current records)"),
    ("U14", re.compile(r"\bCFTR\b", re.I), "CFTR disposition node"),
]
FIG8A = {"ME12-05"}
GRADE_RANK = {"FUNCTIONAL": 3, "BODY_READOUT": 2, "ABSTRACT_ONLY": 1, "CELL_ONLY": 1}

def grade(row):
    if row["target_confirmation_class"] == "FUNCTIONAL_PARTICIPATION_SUPPORTED":
        return "FUNCTIONAL"
    if row["source_review_scope"] == "ABSTRACT_ONLY":
        return "ABSTRACT_ONLY"
    return "BODY_READOUT"

rows = list(csv.DictReader(MECH.open(encoding="utf-8-sig", newline="")))
ranks = list(csv.DictReader(RANK.open(encoding="utf-8-sig", newline="")))
retained = sorted([r for r in ranks if r["validation_review_status"] == "RETAIN_STABLE_WITHIN_10"],
                  key=lambda r: int(r["conditional_rank"]))
comp_order = [r["compound"] for r in retained]
cid = {r["compound"]: r["candidate_id"] for r in retained}

# observation -> matched universe codes (with basis)
obs_map = {}
for row in rows:
    text = " | ".join([row["molecular_node"], row["redox_endpoint"]])
    hits = [(code, basis) for code, rx, basis in RULES if rx.search(text)]
    obs_map[row["observation_id"]] = hits

# compound x pathway cell aggregation
cells = {}
for row in rows:
    comp = row["compound"]
    if comp not in cid:
        continue
    g = grade(row)
    flag = "FIG8A_CONCERN" if row["observation_id"] in FIG8A else ""
    for code, basis in obs_map[row["observation_id"]]:
        key = (comp, code)
        c = cells.setdefault(key, dict(observations=[], grades=[], flags=set(), dois=set(),
                                       locators=[], bases=set()))
        c["observations"].append(row["observation_id"])
        c["grades"].append(g)
        if flag:
            c["flags"].add(flag)
        if row["doi"] and row["doi"] != "DOI_NOT_LOCATED":
            c["dois"].add(row["doi"])
        c["locators"].append(f"{row['observation_id']}:{row['source_locator']}")
        c["bases"].add(basis)

matrix = []
register = []
# U13 PGC-1alpha is cell-only context in ME12-18 (myotubes), not an in vivo measurement.
# Record it explicitly as CELL_ONLY (excluded from solid) rather than upgrading the in vivo row.
if ("Hesperetin", "U13") not in cells:
    cells[("Hesperetin", "U13")] = dict(observations=["ME12-18"], grades=["CELL_ONLY"],
                                        flags={"CELL_ONLY"}, dois={"10.1038/s41598-018-27614-8"},
                                        locators=["ME12-18:cell-only Fig. 4a-e (myotubes)"],
                                        bases={"PGC-1alpha cell-only linkage; not in vivo"})
for comp in comp_order:
    for code in UCODES:
        key = (comp, code)
        if key in cells:
            c = cells[key]
            best = max(c["grades"], key=lambda x: GRADE_RANK[x])
            flag = ";".join(sorted(c["flags"]))
            state = best
            matrix.append(dict(candidate_id=cid[comp], compound=comp, pathway_code=code,
                               pathway_name=UNAME[code], pathway_class=UCLASS[code],
                               cell_state=state, evidence_grade=best,
                               solid_included="YES" if best in ("FUNCTIONAL", "BODY_READOUT") and not flag else "NO",
                               integrity_flag=flag, n_observations=len(c["observations"]),
                               observations=";".join(c["observations"]),
                               dois=";".join(sorted(c["dois"])),
                               source_locators=";".join(c["locators"]),
                               mapping_basis=";".join(sorted(c["bases"]))))
        else:
            matrix.append(dict(candidate_id=cid[comp], compound=comp, pathway_code=code,
                               pathway_name=UNAME[code], pathway_class=UCLASS[code],
                               cell_state="PENDING_EXPANSION", evidence_grade="",
                               solid_included="NO", integrity_flag="", n_observations=0,
                               observations="", dois="", source_locators="", mapping_basis=""))

# Merge systematic expansion search results into pending cells (abstract-level candidates).
exp_path = AUDIT / "Pathway_Expansion_Search_Results.csv"
exp = {}
if exp_path.exists():
    for r in csv.DictReader(exp_path.open(encoding="utf-8-sig", newline="")):
        exp[(r["compound"], r["pathway_code"])] = r
for m in matrix:
    if m["cell_state"] != "PENDING_EXPANSION":
        continue
    e = exp.get((m["compound"], m["pathway_code"]))
    if not e:
        continue
    if e["status"] == "ABSTRACT_CANDIDATE":
        m["cell_state"] = "ABSTRACT_ONLY"; m["evidence_grade"] = "ABSTRACT_ONLY"
        m["dois"] = e["doi"]; m["observations"] = "PMID:" + e["pmid"]
        m["source_locators"] = e["title"]
        m["mapping_basis"] = "systematic expansion search; abstract-level candidate; NOT_REVIEWED; needs full-text + identity/context verification"
    else:
        m["cell_state"] = "NOT_REPORTED_IN_CHECKED_SET"
        m["mapping_basis"] = "systematic expansion search; no qualifying primary study found"

# Apply full-text verification verdicts (upgrade / reject / reassign / formulation-context).
ver_path = AUDIT / "Pathway_Fulltext_Verification_2026-11-27.csv"
if ver_path.exists():
    mdict = {(m["compound"], m["pathway_code"]): m for m in matrix}
    def _upgrade(cell, grade, doi, src, title, reason):
        cell["cell_state"] = grade; cell["evidence_grade"] = grade
        cell["solid_included"] = "YES" if grade in ("FUNCTIONAL", "BODY_READOUT") else "NO"
        cell["dois"] = doi; cell["observations"] = src; cell["source_locators"] = title
        cell["mapping_basis"] = "full-text verified 2026-11-26: " + reason; cell["integrity_flag"] = ""
    def _reject(cell, reason):
        cell["cell_state"] = "NOT_REPORTED_IN_CHECKED_SET"; cell["evidence_grade"] = ""
        cell["solid_included"] = "NO"; cell["dois"] = ""; cell["observations"] = ""
        cell["source_locators"] = ""; cell["mapping_basis"] = "full-text verified 2026-11-26 REJECTED: " + reason
    for v in csv.DictReader(ver_path.open(encoding="utf-8-sig", newline="")):
        comp = v["compound"]; sp = v["searched_pathway"]; act = v["action"]
        src = "PMID:" + v["pmid"]; doi = v["doi"]; title = v["source_title"]; reason = v["reason"]
        key = (comp, sp)
        if act == "UPGRADE" and key in mdict:
            _upgrade(mdict[key], v["grade"], doi, src, title, reason)
        elif act == "REJECT" and key in mdict:
            _reject(mdict[key], reason)
        elif act == "REASSIGN":
            if key in mdict: _reject(mdict[key], reason)
            rk = (comp, v["reassign_to"])
            if rk in mdict: _upgrade(mdict[rk], v["grade"], doi, src, title, reason)
        elif act == "FORMULATION_CONTEXT" and key in mdict:
            mdict[key]["integrity_flag"] = "FORMULATION_CONTEXT"
            mdict[key]["mapping_basis"] = "full-text reviewed 2026-11-26: formulation context; abstract pending review. " + reason
        elif act == "NO_ACCESS" and key in mdict:
            mdict[key]["integrity_flag"] = "NO_FULLTEXT_ACCESS"
            mdict[key]["mapping_basis"] = "full-text unavailable (institutional access blocked); abstract pending. " + reason

# Rebuild expansion register from the final matrix (remaining follow-up work).
register = []
for m in matrix:
    if m["cell_state"] == "ABSTRACT_ONLY":
        register.append(dict(candidate_id=m["candidate_id"], compound=m["compound"], pathway_code=m["pathway_code"],
                             pathway_name=m["pathway_name"], pathway_class=m["pathway_class"],
                             status="ABSTRACT_NEEDS_FULLTEXT",
                             priority="HIGH" if m["pathway_class"] == "CORE_ANTIOXIDANT" else "MEDIUM",
                             note="Abstract-level candidate; verify full text, compound identity, model and context (mixture/formulation/computational)"))
    elif m["cell_state"] == "NOT_REPORTED_IN_CHECKED_SET":
        register.append(dict(candidate_id=m["candidate_id"], compound=m["compound"], pathway_code=m["pathway_code"],
                             pathway_name=m["pathway_name"], pathway_class=m["pathway_class"],
                             status="NOT_REPORTED_OPTIONAL_DEEPER", priority="LOW",
                             note="Systematic search found no qualifying primary study; optional deeper search"))

with (TBL / "07_pathway_framework_matrix.csv").open("w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(matrix[0]), lineterminator="\n"); w.writeheader(); w.writerows(matrix)
with (AUDIT / "Pathway_Expansion_Register.csv").open("w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(register[0]), lineterminator="\n"); w.writeheader(); w.writerows(register)

# plot data: matrix grid + solid shared-pathway intersections
grid = {code: {comp: "" for comp in comp_order} for code in UCODES}
for m in matrix:
    grid[m["pathway_code"]][m["compound"]] = m["cell_state"]
SIGN = [u["pathway_code"] for u in univ if u["pathway_class"] == "CORE_ANTIOXIDANT"]
comp_sets = {}
for comp in comp_order:
    s = frozenset(m["pathway_code"] for m in matrix
                  if m["compound"] == comp and m["solid_included"] == "YES")
    comp_sets[comp] = s
groups = {}
for comp, s in comp_sets.items():
    groups.setdefault(s, []).append(comp)
inters = [dict(pathways=sorted(s), size=len(cs), compounds=cs)
          for s, cs in sorted(groups.items(), key=lambda kv: (-len(kv[1]), sorted(kv[0]))) if s]
plot = dict(comp_order=comp_order, ucodes=UCODES, uname=UNAME, uclass=UCLASS, grid=grid,
            intersections=inters, no_solid=[c for c, s in comp_sets.items() if not s],
            n_pending=len(register), n_cells=len(matrix))
(AUDIT / "pathway_framework_plot_data.json").write_text(json.dumps(plot, ensure_ascii=False, indent=2), encoding="utf-8")

from collections import Counter
states = Counter(m["cell_state"] for m in matrix)
print("cells:", len(matrix), "| states:", dict(states))
print("expansion register rows:", len(register))
print("\nper-pathway solid compound counts:")
for code in UCODES:
    n = sum(1 for m in matrix if m["pathway_code"] == code and m["solid_included"] == "YES")
    na = sum(1 for m in matrix if m["pathway_code"] == code and m["cell_state"] != "PENDING_EXPANSION")
    print(f"  {code:4} solid={n:2} any_evidence={na:2}  {UNAME[code][:46]}")
print("\nsolid shared-pathway intersections:")
for it in inters:
    print(f"  {'+'.join(it['pathways']):22} n={it['size']}  {', '.join(it['compounds'])}")
print("no solid pathway:", ", ".join(plot["no_solid"]))
