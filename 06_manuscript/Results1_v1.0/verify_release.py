"""Check replay equality and record release provenance without private source material."""
import csv
import hashlib
import json
from pathlib import Path
import platform
import sys
import xml.etree.ElementTree as ET
from zipfile import ZipFile
from build_results1 import HERE, MODEL, ROOT, readjson, readcsv

LOCAL = ROOT / "download_raw"
REPLAY = LOCAL / "Results1_post_cleanup_replay"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def release_sha(path):
    raw = path.read_bytes()
    if path.suffix in {".csv", ".json", ".md", ".svg", ".py", ".R", ".mjs"}:
        raw = raw.replace(b"\r\n", b"\n")
    return hashlib.sha256(raw).hexdigest()


def worksheet(path):
    with ZipFile(path) as book:
        assert book.testzip() is None
        parts = {p:book.read(p) for p in book.namelist()
                 if p.startswith("xl/worksheets/sheet") and p.endswith(".xml") or p == "xl/sharedStrings.xml"}
        for name, data in parts.items():
            if name.startswith("xl/worksheets"):
                root = ET.fromstring(data)
                assert len(root.findall(".//{*}row")) == 25
                assert not any(c.get("t") == "e" for c in root.findall(".//{*}c"))
        return parts


def main():
    payload = readjson(HERE/"Evidence_Snapshot.json")
    assert len(payload["observations"])==304 and len(payload["rankings"])==225
    assert len(payload["blocks"])==20 and len(payload["panel"])==24
    before = readjson(LOCAL/"results1_before_cleanup.json")
    assert all(sha(ROOT/name)==digest for name,digest in before.items())
    files = ["Table1.csv","Figure1_Data.csv","Figure1.svg","Figure1.png","Results1.md"]
    files += [f"Supplementary_Materials/{p.name}" for p in (HERE/"Supplementary_Materials").glob("*.csv")]
    for name in files:
        assert sha(HERE/name)==sha(REPLAY/name), name
    assert worksheet(HERE/"Table1.xlsx") == worksheet(REPLAY/"Table1.xlsx")
    svg = ET.parse(HERE/"Figure1.svg")
    assert svg.findall(".//{*}text") and not svg.findall(".//{*}image")
    empty = readjson(LOCAL/"Results1_post_cleanup_update_empty/Evidence_Change_Report.json")
    synthetic = readjson(LOCAL/"Results1_post_cleanup_update_synthetic/Evidence_Change_Report.json")
    assert empty["stability_status"]=="BASELINE_REPLAY" and not empty["changed_rank_rows"]
    assert empty["old_model_metrics"]["scored"]==75
    assert synthetic["added_observations"]==2 and synthetic["added_model_rows"]==2
    assert len(synthetic["holds"])==1 and synthetic["automatic_tier_changes"]==0
    for r in readjson(LOCAL/"results1-model-before.json"):
        assert sha(Path(r["Path"])).upper()==r["Hash"]
    deleted = [r for r in readcsv(HERE/"Repository_Cleanup_Manifest.csv") if r["action"]=="DELETE_REDUNDANT"]
    assert len(deleted)==12 and all(not (ROOT/r["path"]).exists() for r in deleted)
    for row in deleted:
        if row["retained_copy"]:
            assert sha(ROOT/row["retained_copy"])==row["sha256"]
    files += ["Table1.xlsx", "Evidence_Snapshot.json", "Evidence_Update_Intake.csv"]
    baseline = [
        ROOT/"01_candidate_discovery/results/discovery_register.csv",
        ROOT/"02_identity_and_evidence/results/candidate_evidence_profiles.csv",
        MODEL/"results/model_update_summary.json", MODEL/"review_validation_summary.json",
        MODEL/"Top20_Conditional_Uncertainty.csv", MODEL/"Protocol_Dose_Sensitivity.csv",
        MODEL/"results/Analysis_Data_and_Dispositions.csv",
        MODEL/"review_and_validate.py",
        ROOT/"03_candidate_selection/06_verified_source_update/fit_verified_source_diagnostics.py",
        ROOT/"03_candidate_selection/05_model_robustness/compare_models.py",
        ROOT/"03_candidate_selection/01_activity_model/results/completed_model_summary.json",
        ROOT/"03_candidate_selection/09_aqueous_candidate_priority_v0.1/build_priority.py",
        ROOT/"03_candidate_selection/09_aqueous_candidate_priority_v0.1/review_inputs.py",
    ]
    baseline += list(HERE.glob("*.py"))+list(HERE.glob("*.R"))+list(HERE.glob("*.mjs"))
    report = dict(release="Results1_v1.0", methods_version="1.0", upstream_baseline="c69f31ca2f4e9842cfe61766744b9d2b4379288f",
        date="2026-11-20", python=platform.python_version(), R="4.5.3", numpy="2.5.4",
        spreadsheet_runtime="26.1119.11507", random_seed=None, connected_model_penalty=10,
        hash_convention="SHA-256 with LF-normalized text; binary bytes unchanged",
        inputs={p.relative_to(ROOT).as_posix():release_sha(p) for p in baseline},
        artifacts={f:release_sha(HERE/f) for f in sorted(files)},
        computational_replay="PASS", science_release="RESEARCHER_REVIEW_PENDING")
    (HERE/"Results1_Manifest.json").write_text(json.dumps(report,indent=2)+"\n", encoding="utf8")
    print("Pre/post hashes, replay SVG/PNG, worksheet cells, model refit and updates PASS")


if __name__ == "__main__":
    main()
