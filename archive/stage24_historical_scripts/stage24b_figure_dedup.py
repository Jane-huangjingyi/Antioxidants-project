from pathlib import Path
from datetime import date
import csv, hashlib, shutil

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures" / "aqueous_antioxidant_atlas"
ARCH = ROOT / "archive" / "figure_redundancy_stage24"
DATA = ROOT / "data"
DOCS = ROOT / "docs"
TODAY = date.today().isoformat()

archive_map = {
    "00_overview/Aqueous_Antioxidant_Class_Overview.png": ("highly_redundant", "00_overview/Aqueous_Class_Coverage_Overview.png", "Same class-level candidate/completion message; canonical coverage figure adds candidate, rankable and output counts."),
    "00_overview/Aqueous_Class_Ranking_Leaders.png": ("highly_redundant", "00_overview/Aqueous_All_Classes_Ranking_Overview.png", "Same class-leader conclusion; canonical figure uses within-panel positions and covers every rankable aqueous panel."),
    "00_overview/Aqueous_Evidence_Confidence_Overview.png": ("partially_redundant", "00_overview/Aqueous_All_Classes_Ranking_Overview.png; class Evidence_Depth figures", "Confidence is already encoded in the ranking overview and detailed evidence-depth figures; retaining this aggregate adds little decision value."),
    "01_flavonoids/Flavonoids_Evidence_Confidence.png": ("highly_redundant", "01_flavonoids/Flavonoids_Evidence_Depth.png", "Evidence Depth already encodes record count, primary H-ORAC value and confidence."),
    "02_phenolic_acids/PhenolicAcids_Evidence_Confidence.png": ("highly_redundant", "02_phenolic_acids/PhenolicAcids_Evidence_Depth.png", "Evidence Depth already encodes record count, primary H-ORAC value and confidence."),
    "03_stilbenes_lignans/Stilbenes_Lignans_Evidence_Confidence.png": ("highly_redundant", "03_stilbenes_lignans/Stilbenes_Lignans_Evidence_Depth.png", "Same points and source data; only the title differs."),
    "04_water_soluble_vitamins/VitaminC_TopN.png": ("highly_redundant", "04_water_soluble_vitamins/VitaminC_Primary_Literature_Coverage.png; 00_overview/Aqueous_All_Classes_Ranking_Overview.png", "Singleton panel: a Top1 ranking graphic is not informative; status and evidence coverage remain active."),
    "07_other_aqueous_phytochemicals/Other_Aqueous_Evidence_Confidence.png": ("highly_redundant", "07_other_aqueous_phytochemicals/Other_Aqueous_Evidence_Depth.png", "Same points and source data; Evidence Depth retains value, evidence count and confidence."),
    "08_metal_chelation/Metal_Chelation_Evidence_Overview.png": ("partially_redundant", "08_metal_chelation/Metal_Chelation_or_Fenton_Evidence_Profile.png", "The canonical profile retains compound, metal/oxidation-state context, evidence strength and mechanistic endpoint."),
    "08_metal_chelation/Metal_Redox_Mechanism_Framework.png": ("exact_duplicate", "00_overview/Aqueous_Metal_Redox_Framework.png", "Byte-identical duplicate of the overview framework."),
}

rename_map = {
    "08_metal_chelation/Fe_Cu_Fenton_Suppression_Profile.png": "08_metal_chelation/Metal_Chelation_or_Fenton_Evidence_Profile.png"
}

meta = {
    "00_overview/Aqueous_All_Classes_Ranking_Overview.png": ("Overview", "ranking", "Class leaders by within-panel position", "data/Supervisor_Aqueous_Class_Ranking_Overview.csv", "within-class percentile", "compound", "confidence; stability; panel", "supervisor/manuscript"),
    "00_overview/Aqueous_Antioxidant_Class_Overview.png": ("Overview", "coverage", "Candidate scope and completion status", "data/Aqueous_Antioxidant_Candidate_Master.csv", "candidate count", "analysis panel", "evidence status", "supervisor"),
    "00_overview/Aqueous_Class_Coverage_Overview.png": ("Overview", "coverage", "Candidate, rankable and displayed output coverage", "data/Aqueous_Antioxidant_Candidate_Master.csv; data/Supervisor_Aqueous_Class_Ranking_Overview.csv", "count", "analysis panel", "coverage type", "supervisor/QC"),
    "00_overview/Aqueous_Class_Ranking_Leaders.png": ("Overview", "ranking", "Leaders of completed aqueous rankings", "legacy class ranking CSVs", "primary construct value", "compound", "class; confidence", "supervisor"),
    "00_overview/Aqueous_Evidence_Confidence_Overview.png": ("Overview", "robustness", "Confidence distribution by ranked panel", "data/Supervisor_Aqueous_Class_Ranking_Overview.csv", "compound count", "analysis subpanel", "confidence", "supervisor/QC"),
    "00_overview/Aqueous_Metal_Redox_Framework.png": ("Metal/context", "framework", "Separate direct antioxidant, chelation, cofactor and prooxidant roles", "conceptual Stage 23 framework", "mechanism flow", "mechanism node", "metal/context relationship", "supervisor/manuscript"),
    "00_overview/Aqueous_Primary_Literature_Coverage.png": ("Overview", "literature coverage", "Core versus supporting original-paper coverage", "data/Aqueous_Antioxidant_Paper_Summary.csv", "paper units", "class coverage", "paper role", "supervisor/QC"),
}

def infer(rel):
    s = rel.as_posix()
    folder = rel.parts[0]
    cls = {
        "01_flavonoids":"Flavonoids", "02_phenolic_acids":"Phenolic acids / conjugates",
        "03_stilbenes_lignans":"Stilbenes / lignans", "04_water_soluble_vitamins":"Vitamin C aqueous",
        "05_betalains":"Betalains / nitrogen-containing", "06_organosulfur":"Organosulfur",
        "07_other_aqueous_phytochemicals":"Other aqueous phytochemicals", "08_metal_chelation":"Metal-ion mechanisms",
        "09_micronutrients":"Micronutrients", "00_overview":"Overview"
    }.get(folder, folder)
    if s in meta: return meta[s]
    if "TopN" in s:
        typ,msg,x,y,enc,aud = "ranking", "Within-class literature-derived ranking", "primary antioxidant value", "compound", "subclass; confidence; study count", "supervisor/manuscript"
    elif "Evidence_Depth" in s:
        typ,msg,x,y,enc,aud = "robustness", "Evidence depth versus primary antioxidant value", "eligible independent records", "primary antioxidant value", "compound; confidence", "supervisor/QC"
    elif "Evidence_Confidence" in s:
        typ,msg,x,y,enc,aud = "robustness", "Compound evidence confidence", "confidence/evidence count", "compound or primary value", "confidence", "QC/internal"
    elif "Primary_Literature_Coverage" in s:
        typ,msg,x,y,enc,aud = "literature coverage", "Primary-literature coverage and missingness", "candidate/paper count", "coverage status", "eligibility role", "supervisor/QC"
    elif "Profile" in s:
        typ,msg,x,y,enc,aud = "mechanism profile", "Assay- or mechanism-specific evidence profile", "evidence tier/context", "compound", "assay; evidence strength; endpoint", "supervisor/manuscript"
    elif "Enzyme_Map" in s:
        typ,msg,x,y,enc,aud = "mechanism map", "Micronutrient antioxidant-enzyme relationships", "enzyme/redox system", "micronutrient", "nutrient", "supervisor/manuscript"
    elif "Prooxidant_Context" in s:
        typ,msg,x,y,enc,aud = "risk context", "Micronutrient prooxidant and toxicity context", "risk context", "micronutrient", "evidence strength", "supervisor/QC"
    elif "Framework" in s:
        typ,msg,x,y,enc,aud = "framework", "Mechanism framework", "mechanism flow", "mechanism node", "relationships", "supervisor/manuscript"
    else:
        typ,msg,x,y,enc,aud = "other", "Class-specific evidence message", "source-specific", "source-specific", "source-specific", "QC/internal"
    source = {
        "01_flavonoids":"data/Polyphenols_Flavonoids_Top20_v1.0.csv; data/Flavonoid_Ranking_Coverage.csv",
        "02_phenolic_acids":"data/Polyphenols_PhenolicAcids_TopN_v1.0.csv; data/PhenolicAcid_Ranking_Coverage.csv",
        "03_stilbenes_lignans":"data/Stilbenes_Lignans_TopN_v1.0.csv; data/Stilbenes_Lignans_Evidence_Master.csv",
        "04_water_soluble_vitamins":"data/VitaminC_TopAvailable_v1.0.csv; data/Aqueous_Antioxidant_Paper_Summary.csv",
        "05_betalains":"data/Betalains_Nitrogen_Profile_Evidence.csv",
        "06_organosulfur":"data/Organosulfur_Redox_Profile.csv",
        "07_other_aqueous_phytochemicals":"data/Other_Aqueous_Phytochemicals_TopN_v1.0.csv; data/Other_Aqueous_Phytochemicals_Evidence_Master.csv",
        "08_metal_chelation":"data/Aqueous_Metal_Redox_Evidence.csv",
        "09_micronutrients":"data/Antioxidant_Micronutrient_Redox_Profile_v2.csv",
    }.get(folder, "see figure index")
    return cls,typ,msg,source,x,y,enc,aud

original = sorted(FIG.rglob("*.png"))
if len(original) != 33:
    raise SystemExit(f"Expected 33 Stage 24 PNGs before cleanup, found {len(original)}")

inventory = []
for path in original:
    rel = path.relative_to(FIG).as_posix()
    cls, typ, msg, source, x, y, enc, aud = infer(Path(rel))
    if rel in archive_map:
        redundancy, replacement, reason = archive_map[rel]
        action = "archive"
        dup = replacement
    elif rel in rename_map:
        redundancy, replacement, reason = "unique", rename_map[rel], "Retained and renamed to reflect both chelation and Fenton-context evidence."
        action, dup = "retain_renamed", ""
    else:
        redundancy, replacement, reason = "unique", "", "Provides a distinct scientific message in the final active package."
        action, dup = "retain", ""
    inventory.append(dict(figure_file=rel,folder=rel.split('/')[0],**{"class":cls},figure_type=typ,primary_message=msg,source_data=source,x_variable=x,y_variable=y,encoded_variables=enc,audience=aud,duplicated_with=dup,redundancy_level=redundancy,retain_or_archive=action,canonical_replacement=replacement,reason=reason,notes=f"sha256={hashlib.sha256(path.read_bytes()).hexdigest()}"))

ARCH.mkdir(parents=True, exist_ok=True)
manifest = []
for rel, (redundancy, replacement, reason) in archive_map.items():
    src, dst = FIG / rel, ARCH / rel
    if src.exists():
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src), str(dst))
    manifest.append(dict(archived_file=dst.relative_to(ROOT).as_posix(),original_location=(Path("figures/aqueous_antioxidant_atlas")/rel).as_posix(),redundancy_reason=f"{redundancy}: {reason}",canonical_replacement=(Path("figures/aqueous_antioxidant_atlas")/replacement).as_posix() if ';' not in replacement else replacement,date_archived=TODAY,reproducible_from_R="no",notes="Scientific data and CSV sources retained; ranking/evidence unchanged. Canonical R script intentionally suppresses this duplicate."))

for old, new in rename_map.items():
    src, dst = FIG / old, FIG / new
    if src.exists():
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src), str(dst))

with (FIG / "FIGURE_INVENTORY_AUDIT.csv").open("w", newline="", encoding="utf-8-sig") as f:
    w=csv.DictWriter(f,fieldnames=list(inventory[0])); w.writeheader(); w.writerows(inventory)
with (ARCH / "ARCHIVED_FIGURES_MANIFEST.csv").open("w", newline="", encoding="utf-8-sig") as f:
    w=csv.DictWriter(f,fieldnames=list(manifest[0])); w.writeheader(); w.writerows(manifest)

active = sorted(p.relative_to(FIG).as_posix() for p in FIG.rglob("*.png"))
if len(active) != 23:
    raise SystemExit(f"Expected 23 canonical PNGs after cleanup, found {len(active)}")

index_lines = ["# Aqueous Antioxidant Atlas — Canonical Figure Index（Stage 24B）", "", "本索引仅列 active canonical figures。原则为 `one scientific message → one canonical figure`；被替代图见 `archive/figure_redundancy_stage24/ARCHIVED_FIGURES_MANIFEST.csv`。所有数值仍为 class/subpanel-specific，不形成 global antioxidant score。", ""]
for rel in active:
    cls, typ, msg, source, x, y, enc, aud = infer(Path(rel))
    construct = {
        "Flavonoids":"H-ORAC-FL (mol TE/mol compound)",
        "Phenolic acids / conjugates":"H-ORAC-FL (mol TE/mol compound)",
        "Stilbenes / lignans":"H-ORAC-FL (mol TE/mol compound)",
        "Vitamin C aqueous":"H-ORAC-FL; singleton evidence summary",
        "Betalains / nitrogen-containing":"LOX-FL and MPO/HOCl assay-specific profile",
        "Organosulfur":"KEAP1/NRF2, thiol chemistry, Fenton and radical-kinetic profile",
        "Other aqueous phytochemicals":"H-ORAC-FL coherent subpanel or assay-specific profile",
        "Metal-ion mechanisms":"Chelation/reduction/Fenton-context profile",
        "Micronutrients":"Cofactor and dose-dependent redox-context profile",
        "Metal/context":"Conceptual metal-redox mechanism framework",
        "Overview":"Within-panel position or count; no shared raw construct",
    }.get(cls,"Class-specific construct")
    caveat = "Class-specific construct; do not compare raw values across incompatible panels."
    supersedes = "; ".join(k for k,v in archive_map.items() if rel in v[1]) or "None"
    index_lines += [f"## `{rel}`", "", f"- **Class：**{cls}", f"- **Scientific question：**{msg}", f"- **Source data：**{source}", f"- **Primary construct：**{construct}", f"- **Main message：**{msg}", "- **Why retained：**它提供最终交付中独立且不可由另一张 active 图完整替代的信息。", f"- **Supersedes：**{supersedes}", f"- **Major caveat：**{caveat}", f"- **Recommended use：**{aud}", ""]
(FIG / "FIGURE_INDEX_CN.md").write_text("\n".join(index_lines),encoding="utf-8")

priority1 = [
    ("docs/Supervisor_Aqueous_Ranking_Progress_CN.md","md","Stage 24 scientific summary"),
    ("data/Supervisor_Aqueous_Class_Ranking_Overview.csv","csv","Class/subpanel ranking overview"),
    ("data/Aqueous_Antioxidant_Primary_Literature_Evidence.csv","csv","Record-level DOI-traceable evidence"),
    ("data/Aqueous_Antioxidant_Paper_Summary.csv","csv","Paper-level evidence summary"),
    ("data/Stilbenes_Lignans_Evidence_Master.csv","csv","New class evidence master"),
    ("data/Stilbenes_Lignans_TopN_v1.0.csv","csv","Stilbenes/lignans Top available"),
    ("data/Betalains_Nitrogen_Profile_Evidence.csv","csv","Betalain profile evidence"),
    ("data/Organosulfur_Redox_Profile.csv","csv","Organosulfur redox profile"),
    ("data/Other_Aqueous_Phytochemicals_Evidence_Master.csv","csv","Other-aqueous evidence master"),
    ("data/Other_Aqueous_Phytochemicals_TopN_v1.0.csv","csv","Other-aqueous coherent-subpanel Top available"),
    ("data/Aqueous_Metal_Redox_Evidence.csv","csv","Metal mechanism evidence"),
    ("data/Antioxidant_Micronutrient_Redox_Profile_v2.csv","csv","Micronutrient profile"),
    ("figures/aqueous_antioxidant_atlas/FIGURE_INDEX_CN.md","md","Canonical figure definitions and caveats"),
]
priority2 = [(f"figures/aqueous_antioxidant_atlas/{p}","png","Canonical scientific figure") for p in active if p.startswith("00_overview/") or p in ["03_stilbenes_lignans/Stilbenes_Lignans_TopN.png","05_betalains/Betalains_Profile_Comparison.png","06_organosulfur/Organosulfur_Redox_Mechanism_Profile.png","07_other_aqueous_phytochemicals/Other_Aqueous_TopN.png","08_metal_chelation/Metal_Chelation_or_Fenton_Evidence_Profile.png","09_micronutrients/Micronutrient_Redox_Profile.png"]]
priority3 = [
    ("Antioxidant_Project_MASTER_HISTORY_AND_WORKFLOW_CN.md","md","Method evolution and project history"),
    ("docs/PROJECT_STAGE_INDEX_CN.md","md","Stage status audit"),
    ("R/plot_antioxidant_atlas.R","R","Canonical plotting logic"),
    ("figures/aqueous_antioxidant_atlas/FIGURE_INVENTORY_AUDIT.csv","csv","Figure-level deduplication audit"),
    ("archive/figure_redundancy_stage24/ARCHIVED_FIGURES_MANIFEST.csv","csv","Archived-figure provenance"),
]
sync_rows=[]
for pri, items, req, upload in [(1,priority1,"yes","yes"),(2,priority2,"no","optional"),(3,priority3,"no","optional")]:
    for path,typ,purpose in items:
        sync_rows.append(dict(priority=pri,file_path=path,file_type=typ,purpose=purpose,required_yes_no=req,why_needed=purpose,supersedes="See Figure Index/manifest" if typ=="png" else "NA",upload_to_chatgpt=upload))
for path in sorted(p.relative_to(ROOT).as_posix() for p in ARCH.rglob("*.png")):
    sync_rows.append(dict(priority="DO NOT SEND",file_path=path,file_type="png",purpose="Archived redundant figure",required_yes_no="no",why_needed="Superseded by canonical active figure",supersedes="NA",upload_to_chatgpt="no"))
with (DATA/"CHATGPT_SYNC_FILES_STAGE24.csv").open("w",newline="",encoding="utf-8-sig") as f:
    w=csv.DictWriter(f,fieldnames=list(sync_rows[0]));w.writeheader();w.writerows(sync_rows)

def links(items): return "\n".join(f"- `{p}` — {purpose}" for p,_,purpose in items)
sync_md = f"""# Stage 24 完成后，请把以下文件发给 ChatGPT

本清单只引用 Stage 24B 清理后实际存在的文件。已归档图不应上传。

## Priority 1 — 必须发送

{links(priority1)}

## Priority 2 — 建议发送的 canonical figures

{links(priority2)}

## Priority 3 — 方法审计时可选

{links(priority3)}

## 不需要发送

- `archive/figure_redundancy_stage24/` 下的重复图。
- 旧 lipid/global overview、intermediate search logs、temporary CSV、Zotero cache。
- raw PDFs；只有某一 HUMAN REVIEW issue 需要核对全文时再提供。

## Minimal Sync Package

上传数量受限时，发送全部 Priority 1 文件，加以下四张 overview：

- `figures/aqueous_antioxidant_atlas/00_overview/Aqueous_All_Classes_Ranking_Overview.png`
- `figures/aqueous_antioxidant_atlas/00_overview/Aqueous_Class_Coverage_Overview.png`
- `figures/aqueous_antioxidant_atlas/00_overview/Aqueous_Primary_Literature_Coverage.png`
- `figures/aqueous_antioxidant_atlas/00_overview/Aqueous_Metal_Redox_Framework.png`
"""
(DOCS/"CHATGPT_SYNC_MANIFEST_STAGE24.md").write_text(sync_md,encoding="utf-8")

counts={}
for p in active: counts[p.split('/')[0]]=counts.get(p.split('/')[0],0)+1
report=f"""# Stage 24B Figure Deduplication Report

本轮只清理 derived figure deliverables；ranking、TopN、evidence tier、primary construct、DOI、confidence、stability、candidate universe和human-review decisions均未改变。

原始 PNG 总数为 **33**；最终 active canonical PNG 为 **23**；归档重复图 **10**，其中 exact duplicate **1**、highly redundant **7**、partially redundant **2**。各目录 active PNG 数为：{'; '.join(f'{k}={v}' for k,v in counts.items())}。所有正式目录均非空；singleton Vitamin C 保留 literature-coverage figure和状态说明，不保留无信息增益的Top1图。active aqueous folder中不存在lipid-phase figure。

Overview最终保留 `Aqueous_All_Classes_Ranking_Overview.png`、`Aqueous_Class_Coverage_Overview.png`、`Aqueous_Primary_Literature_Coverage.png` 和 `Aqueous_Metal_Redox_Framework.png`。Metal层保留overview framework与更综合的`Metal_Chelation_or_Fenton_Evidence_Profile.png`。Micronutrient prooxidant-context图含profile与enzyme map没有的独立风险信息，因此继续保留。

`R/plot_antioxidant_atlas.R` 默认 `GENERATE_LEGACY_FIGURES <- FALSE`，不再生成归档图；如需重建历史Phase 2–22图必须人工显式启用。ChatGPT人类可读和机器可读sync manifests均已生成。

## HUMAN REVIEW REQUIRED — FIGURE DEDUPLICATION

本轮未发现无法确认来源的PNG、跨construct raw-value overview或“归档后导致唯一科学结果丢失”的情形，因此没有新增必须阻断清理的figure-deduplication裁决。Stage 24原有candidate identity/scope和metal/pigment方法学human-review事项保持不变。
"""
(DOCS/"Stage24B_Figure_Deduplication_Report_CN.md").write_text(report,encoding="utf-8")

print({"original_png":len(original),"canonical_png":len(active),"archived_png":len(manifest),"exact":1,"highly_redundant":7,"partially_redundant":2})
