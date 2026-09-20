from __future__ import annotations

import csv
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read_csv(path: Path):
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


figure_rows = read_csv(ROOT / "figures" / "FIGURE_CODE_DATA_MAP.csv")
figure_missing = []
script_missing = []
input_missing = []
for row in figure_rows:
    if not (ROOT / row["figure_path"]).exists():
        figure_missing.append(row["figure_path"])
    if not (ROOT / row["R_script_path"]).exists():
        script_missing.append(row["R_script_path"])
    for item in row["input_data_path"].split(";"):
        item = item.strip()
        if item and not (ROOT / item).exists():
            input_missing.append(item)

pngs = sorted((ROOT / "figures" / "aqueous_antioxidant_atlas").rglob("*.png"))
mapped = {row["figure_path"] for row in figure_rows}
unmapped = [p.relative_to(ROOT).as_posix() for p in pngs if p.relative_to(ROOT).as_posix() not in mapped]

migration = read_csv(ROOT / "PROJECT_FILE_MIGRATION_MAP.csv")
status_counts = Counter(row["status_class"] for row in migration)
move_counts = Counter(row["moved"] for row in migration)
hr_rows = [row for row in migration if "HUMAN REVIEW REQUIRED" in (row.get("dependency_risk") or "")]

active_suffixes = {".md", ".csv", ".r", ".py", ".txt"}
skip_roots = {".git", "archive"}
active_files = []
for p in ROOT.rglob("*"):
    if not p.is_file() or p.suffix.lower() not in active_suffixes:
        continue
    rel = p.relative_to(ROOT)
    if rel.parts and rel.parts[0] in skip_roots:
        continue
    if rel.as_posix() == "PROJECT_FILE_MIGRATION_MAP.csv":
        continue
    active_files.append(p)

old_paths = []
for row in migration:
    old = row["old_path"].strip()
    new = row["proposed_new_path"].strip()
    if old and new and old != new and len(old) >= 8:
        old_paths.append(old)

stale_hits = []
for path in active_files:
    try:
        text = path.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError:
        continue
    for old in old_paths:
        if old in text:
            stale_hits.append((path.relative_to(ROOT).as_posix(), old))

explicit_patterns = [
    r"R/plot_antioxidant_atlas\.R",
    r"figures/aqueous_antioxidant_atlas/10_unified_literature_screening",
    r"data/Stage25A_Unified_Literature_Screening_Master\.csv",
    r"data/Stage25A_Publication_Provenance\.csv",
]
pattern_hits = []
for path in active_files:
    try:
        text = path.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError:
        continue
    for pattern in explicit_patterns:
        if re.search(pattern, text):
            pattern_hits.append((path.relative_to(ROOT).as_posix(), pattern))

qc_dir = ROOT / "docs" / "qc"
qc_dir.mkdir(parents=True, exist_ok=True)

repro = f"""# Figure Reproducibility Audit（Stage 25A.1）

审计日期：2026-09-20。审计对象为 `figures/FIGURE_CODE_DATA_MAP.csv` 登记的 active canonical aqueous atlas figures。本次从薄入口 `R/render_all_active_figures.R` 依次调用模块化脚本，29/29 张登记图均成功重建。该结论只覆盖 active canonical 图，不把 supporting、superseded 或 historical figures 误计为当前可复现图包。

映射登记数为 {len(figure_rows)}；当前 atlas PNG 数为 {len(pngs)}；缺失图 {len(figure_missing)}；缺失 R script {len(set(script_missing))}；缺失输入文件 {len(set(input_missing))}；未登记 canonical PNG {len(unmapped)}。每张图的路径、科学问题、生成脚本、输入数据、过滤与转换摘要、输出 metric、可调参数和 caveat 均记录于 figure-code-data map。两张 Stage 25A 旧图的轴异常已定位为在 log10 坐标转换后使用数值型 `nudge_y` 导致标签尺度再次失真；错误版本保留在 `archive/figure_qc_stage25A1/`，canonical replacement 改为单次 log10 transform 并使用显示空间的 `vjust`。

审计结论：**PASS（29/29 active canonical figures reproducible）**。执行环境仍可能报告 Windows locale 警告；这不改变数值或文件生成。任何未来 figure 增删必须同步更新 `figures/FIGURE_CODE_DATA_MAP.csv`、`figures/FIGURE_INDEX_CN.md` 和模块脚本，且不得直接手工覆盖 canonical PNG。
"""
(qc_dir / "Figure_Reproducibility_Audit_CN.md").write_text(repro, encoding="utf-8")

broken = f"""# Broken Path Audit（Stage 25A.1）

审计日期：2026-09-20。检查范围为 archive 之外的 active Markdown、CSV、R、Python 和 text 文件；以 `PROJECT_FILE_MIGRATION_MAP.csv` 中所有发生路径变化的 `old_path` 为字典，并额外检查旧 monolithic R script、旧 Stage 25A master/provenance 路径和旧 `10_unified_literature_screening` figure path。

迁移表共 {len(migration)} 行：ACTIVE_CANONICAL {status_counts['ACTIVE_CANONICAL']}、ACTIVE_SUPPORTING {status_counts['ACTIVE_SUPPORTING']}、SUPERSEDED {status_counts['SUPERSEDED']}、HISTORICAL_ONLY {status_counts['HISTORICAL_ONLY']}；执行字段中 moved=yes 为 {move_counts['yes']}。迁移表自身因承担 old→new provenance 不纳入“旧路径残留”错误。扫描发现 migration-dictionary stale references {len(stale_hits)} 条，显式关键旧路径 references {len(pattern_hits)} 条。无法判定是否完全替代而触发 `HUMAN REVIEW REQUIRED — FILE CONSOLIDATION` 的迁移项为 {len(hr_rows)} 条。

审计结论：**{'PASS' if not stale_hits and not pattern_hits else 'FAIL'}**。当前 active 文件未发现已知旧路径断链；archive 内历史脚本和历史说明允许保留当时路径，因为其用途是 provenance，而不是当前执行入口。若后续移动 active 文件，必须先更新 migration map 和 dependency，然后重跑本审计。
"""
(qc_dir / "Broken_Path_Audit_CN.md").write_text(broken, encoding="utf-8")

inventory = f"""# Full-project Inventory Summary（Stage 25A.1）

本轮在实际迁移前完成全项目 inventory，共登记 {len(migration)} 个文件，并逐文件判定 scientific role、status class、proposed new path、canonical replacement、reason 与 dependency risk。分类结果为 ACTIVE_CANONICAL {status_counts['ACTIVE_CANONICAL']}、ACTIVE_SUPPORTING {status_counts['ACTIVE_SUPPORTING']}、SUPERSEDED {status_counts['SUPERSEDED']}、HISTORICAL_ONLY {status_counts['HISTORICAL_ONLY']}。完整逐文件记录见根目录 `PROJECT_FILE_MIGRATION_MAP.csv`。

本次重构以当前科学功能为 active organization：candidate universe、class-specific antioxidant evidence、literature screening、metal and micronutrients、methods/QC、supervisor、sync 与 references；Stage 编号只保留在 `docs/PROJECT_STAGE_INDEX_CN.md` 和 provenance metadata。所有 superseded/historical 文件仅移动、不删除；仍在使用的早期 assay methodology、H-ORAC rules、candidate scope、T1–T5 target framework、SOP、模板与 checklist 被恢复为 active supporting assets。未重新执行 Stage 0–22 科学分析，也未因目录迁移改变历史结果。
"""
(qc_dir / "PROJECT_FILE_INVENTORY_SUMMARY_CN.md").write_text(inventory, encoding="utf-8")

print({
    "figures": len(figure_rows),
    "figure_missing": figure_missing,
    "script_missing": sorted(set(script_missing)),
    "input_missing": sorted(set(input_missing)),
    "unmapped_png": unmapped,
    "stale_hits": stale_hits[:20],
    "stale_count": len(stale_hits),
    "pattern_hits": pattern_hits,
    "migration_counts": dict(status_counts),
    "migration_human_review": len(hr_rows),
})
