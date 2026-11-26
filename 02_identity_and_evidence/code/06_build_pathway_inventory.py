"""Build the compound x pathway evidence inventory, controlled dictionary and overlap counts
from the checked 28-row mechanism evidence CSV (step 02). Assignments are grounded ONLY in
the recorded molecular_node / pathway_or_process / redox_endpoint fields; evidence grade
derives from target_confirmation_class and source_review_scope. Run from repo root:
python 02_identity_and_evidence/code/06_build_pathway_inventory.py"""
import csv, json, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
MECH = ROOT / "02_identity_and_evidence/result/table/04_candidate_in_vivo_mechanism_evidence.csv"
RANK = ROOT / "03_candidate_selection/result/table/04_figure1_candidate_ranks.csv"
OUT_TABLE = ROOT / "02_identity_and_evidence/result/table"
OUT_AUDIT = OUT_TABLE / "audit"

DICT = [
    ("P1", "NRF2-KEAP1/ARE antioxidant response", "SIGNALING", "NFE2L2; KEAP1; SQSTM1/p62; HMOX1; NQO1; GCLC/GCLM"),
    ("P2", "NF-kB / TLR4 inflammatory signaling", "SIGNALING", "TLR4; p-NF-kB; NF-kB"),
    ("P3", "PI3K/AKT signaling", "SIGNALING", "PI3K; AKT"),
    ("P4", "MAPK stress signaling", "SIGNALING", "TAK1; p38; JNK1/2"),
    ("P5", "Ferroptosis regulation", "SIGNALING", "GPX4; ACSL4"),
    ("P6", "HIF1A hypoxia response", "SIGNALING", "HIF1A"),
    ("P7", "PGC-1alpha mitochondrial biogenesis", "SIGNALING", "PGC-1alpha (cell-only in current records)"),
    ("P8", "CFTR-dependent GSH transport/disposition", "SIGNALING", "CFTR (disposition modifier; not a binding target)"),
    ("R1", "Glutathione redox (GSH/GSSG/GCL/GPx)", "REDOX_PROCESS", "GSH; GSSG; GCL; GPx; GSH stores"),
    ("R2", "Lipid peroxidation defense", "REDOX_PROCESS", "MDA; 4-HNE; HPNE; F2-isoprostanes; oxidized LDL"),
    ("R3", "ROS/NO vascular redox balance", "REDOX_PROCESS", "DHE; DAF-2DA/NO; NADPH oxidase subunits; nitrotyrosine; FMD"),
]
SIGN = [d[0] for d in DICT if d[2] == "SIGNALING"]
ALLP = [d[0] for d in DICT]
PNAME = {d[0]: d[1] for d in DICT}

ASSIGN = {
    "ME12-01": (["P1", "R1", "R2", "R3"], ""),
    "ME12-02": (["P1"], "Functional Nrf2-KO contrast; injury endpoints only; no GSH/MDA dependence test"),
    "ME12-03": (["R1", "R2"], "No protein target tested"),
    "ME12-04": (["P1", "R1"], "Abstract-only; KEAP1 docking computational; inhibitor work in cells"),
    "ME12-05": (["P1", "R2", "R3"], "Abstract-only; Fig 8a image-similarity concern (PMID 34428482)"),
    "ME12-06": (["P1", "R1", "R2", "R3"], ""),
    "ME12-07": (["P1"], "Unfavorable context; protein carbonyls endpoint not a lipid-peroxidation family"),
    "ME12-08": (["P1", "R1", "R2", "R3"], "p62/KEAP1 levels do not establish interaction or necessity"),
    "ME12-09": (["P1", "R1", "R2"], ""),
    "ME12-10": (["P1", "R1"], "Abstract-only"),
    "ME12-11": (["P1", "R3"], "Dietary in vivo arm has no Nrf2-KO group"),
    "ME12-12": (["P1", "R3"], "Ex vivo WT vs Nrf2-KO rings; functional"),
    "ME12-13": (["P1", "R2"], "UDP-GT isoform unresolved"),
    "ME12-14": (["P1", "P3", "R1", "R2"], "Do not infer direct targeting from pathway changes"),
    "ME12-15": (["R2"], "Gulo is model genotype; no intervention protein target"),
    "ME12-16": (["P8", "R1"], "CFTR-dependent disposition; not a binding target; no injury endpoint"),
    "ME12-17": (["R1", "R2"], "Human null result; no protein target"),
    "ME12-18": (["R1"], "In vivo muscle GSH/GSSG only; PGC-1alpha/NRF2 linkage is cell-only (not assigned)"),
    "ME12-19": (["P5", "P6"], "GPX4 docking computational; severe attrition in untreated MCAO"),
    "ME12-20": (["P1", "P2", "P4"], "Benefits retained after cardiac Nrf2 knockdown; knockdown lacks matched scramble arm"),
    "ME12-21": (["R1"], "Human; within-group GSSG/GSH; no protein target"),
    "ME12-22": (["R2"], "Human biomarker-specific; no protein target"),
    "ME12-23": (["R1"], "NRF2 involvement not tested in this study"),
    "ME12-24": (["R2"], "Human; plasma ORAC is matrix measurement"),
    "ME12-25": (["R2"], "Human; redox endpoints null/narrative-only"),
    "ME12-26": (["R2"], "Abstract-only human"),
    "ME12-27": (["R3"], "Human; secondary continuous FMD only"),
    "ME12-28": (["R2"], "Abstract-only human; DNA-lesion endpoint separate from lipid family"),
}
FIG8A = {"ME12-05"}

def grade(row):
    if row["target_confirmation_class"] == "FUNCTIONAL_PARTICIPATION_SUPPORTED":
        return "FUNCTIONAL"
    if row["source_review_scope"] == "ABSTRACT_ONLY":
        return "ABSTRACT_ONLY"
    return "BODY_READOUT"

rows = list(csv.DictReader(MECH.open(encoding="utf-8-sig", newline="")))
assert len(rows) == 28
ranks = list(csv.DictReader(RANK.open(encoding="utf-8-sig", newline="")))
retained = sorted([r for r in ranks if r["validation_review_status"] == "RETAIN_STABLE_WITHIN_10"],
                  key=lambda r: int(r["conditional_rank"]))
comp_order = [r["compound"] for r in retained]
assert len(comp_order) == 12

inventory = []
for row in rows:
    oid = row["observation_id"]
    codes, note = ASSIGN[oid]
    g = grade(row)
    flag = "FIG8A_CONCERN" if oid in FIG8A else ""
    solid = g in ("FUNCTIONAL", "BODY_READOUT") and not flag
    for code in codes:
        inventory.append(dict(
            candidate_id=row["candidate_id"], compound=row["compound"],
            pathway_code=code, pathway_name=PNAME[code],
            pathway_class=next(d[2] for d in DICT if d[0] == code),
            molecular_node=row["molecular_node"], pathway_or_process=row["pathway_or_process"],
            evidence_relation_type=row["evidence_relation_type"],
            target_confirmation_class=row["target_confirmation_class"],
            evidence_grade=g, solid_included="YES" if solid else "NO", integrity_flag=flag,
            model_level=row["model_level"], species_or_population=row["species_or_population"],
            tissue=row["tissue"], challenge_or_context=row["challenge_or_context"],
            redox_endpoint=row["redox_endpoint"], observed_direction=row["observed_direction"],
            doi=row["doi"], pmid=row["pmid"], source_url=row["source_url"],
            source_locator=row["source_locator"], source_review_scope=row["source_review_scope"],
            assignment_note=note, interpretation_boundary=row["interpretation_boundary"],
            human_review_status=row["human_review_status"], change_applied=row["change_applied"],
            observation_id=oid))

fields = list(inventory[0].keys())
with (OUT_TABLE / "05_compound_pathway_inventory.csv").open("w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n"); w.writeheader(); w.writerows(inventory)
with (OUT_AUDIT / "Pathway_Dictionary.csv").open("w", encoding="utf-8", newline="") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(["pathway_code", "pathway_name", "pathway_class", "node_basis"]); w.writerows(DICT)

def build_matrix(solid_only):
    m = {p: {c: "" for c in comp_order} for p in ALLP}
    rg = {"FUNCTIONAL": 3, "BODY_READOUT": 2, "ABSTRACT_ONLY": 1}
    for r in inventory:
        if solid_only and r["solid_included"] != "YES":
            continue
        c, p = r["compound"], r["pathway_code"]
        if c not in m[p]:
            continue
        cur = m[p][c]
        if not cur or rg[r["evidence_grade"]] > rg.get(cur, 0):
            m[p][c] = r["evidence_grade"]
    return m

mat_all, mat_solid = build_matrix(False), build_matrix(True)

def setsizes(mat):
    out = []
    for p in ALLP:
        comps = [c for c in comp_order if mat[p][c]]
        out.append(dict(pathway_code=p, pathway_name=PNAME[p],
                        pathway_class=next(d[2] for d in DICT if d[0] == p),
                        n_compounds=len(comps), compounds="; ".join(comps)))
    return out

size_all, size_solid = setsizes(mat_all), setsizes(mat_solid)
with (OUT_TABLE / "06_pathway_overlap_counts.csv").open("w", encoding="utf-8", newline="") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(["pathway_code", "pathway_name", "pathway_class",
                "n_compounds_all_recorded", "compounds_all_recorded", "n_compounds_solid", "compounds_solid"])
    for a, s in zip(size_all, size_solid):
        w.writerow([a["pathway_code"], a["pathway_name"], a["pathway_class"],
                    a["n_compounds"], a["compounds"], s["n_compounds"], s["compounds"]])

comp_sets = {c: frozenset(p for p in SIGN if mat_solid[p][c]) for c in comp_order}
groups = {}
for c, s in comp_sets.items():
    groups.setdefault(s, []).append(c)
intersections = [dict(pathways=sorted(s), size=len(comps), compounds=comps)
                 for s, comps in sorted(groups.items(), key=lambda kv: (-len(kv[1]), sorted(kv[0]))) if s]
plot = dict(comp_order=comp_order, pathways=ALLP, signaling=SIGN, pnames=PNAME,
            matrix_all=mat_all, matrix_solid=mat_solid, size_all=size_all, size_solid=size_solid,
            intersections=intersections, no_signaling_solid=[c for c, s in comp_sets.items() if not s])
(OUT_AUDIT / "pathway_plot_data.json").write_text(json.dumps(plot, ensure_ascii=False, indent=2), encoding="utf-8")
print("inventory rows:", len(inventory))
for a, s in zip(size_all, size_solid):
    print(f"{a['pathway_code']} all={a['n_compounds']:2} solid={s['n_compounds']:2}  {a['pathway_name']}")
print("solid signaling intersections:", [( '+'.join(i['pathways']), i['size']) for i in intersections])
