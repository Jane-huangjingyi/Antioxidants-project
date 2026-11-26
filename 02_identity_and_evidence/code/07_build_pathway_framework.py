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
            register.append(dict(candidate_id=cid[comp], compound=comp, pathway_code=code,
                                 pathway_name=UNAME[code], pathway_class=UCLASS[code],
                                 status="PENDING_EXPANSION",
                                 priority="HIGH" if UCLASS[code] == "CORE_ANTIOXIDANT" else "MEDIUM",
                                 note="Universe pathway not yet systematically checked for this compound; fill in expansion batches"))

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
