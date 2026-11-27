"""Release the Carthamus capacity update after researcher tier confirmation (2026-11-27).
Unaffected candidates keep prior tier; AFF-0019 -> B (high capacity, 2 sources), AFF-0062 -> C (single new study).
Top20 membership unchanged. Run: python 03_candidate_selection/code/25_release_carthamus.py
"""
import csv, json, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
RUN = ROOT / "03_candidate_selection/12_evidence_expansion/run_carthamus_2026-11-27"
rows = list(csv.DictReader((RUN / "Candidate_Membership_Review.csv").open(encoding="utf-8-sig", newline="")))
NEW_TIER = {"AFF-0019": "B", "AFF-0062": "C"}
out = []
for r in rows:
    cid = r["candidate_id"]
    if r["affected_by_new_direct_evidence"] == "True":
        tier = NEW_TIER[cid]; dec = "APPROVED_ADD_TIER_" + tier
    else:
        tier = r["prior_tier"]; dec = "APPROVED_KEEP_TIER"
    out.append(dict(candidate_id=cid, prior_tier=r["prior_tier"], affected_by_new_direct_evidence=r["affected_by_new_direct_evidence"],
                    proposed_next_tier=tier, decision=dec))
with (RUN / "Candidate_Membership_Review_RELEASED.csv").open("w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0]), lineterminator="\n"); w.writeheader(); w.writerows(out)
rep = json.loads((RUN / "Evidence_Change_Report.json").read_text(encoding="utf-8"))
release = dict(released=True, release_date="2026-11-27", reviewer="researcher",
               top20_membership_changed=bool(rep["model_entry"] or rep["model_exit"]),
               tier_assignments=NEW_TIER, kept_tiers=sum(r["decision"] == "APPROVED_KEEP_TIER" for r in out),
               added_observations=rep["added_observations"], model_rows="113->115",
               note="Researcher confirmed release 2026-11-27; existing tiers kept; AFF-0019=B, AFF-0062=C; Top20 unchanged.")
(RUN / "Release_Record.json").write_text(json.dumps(release, ensure_ascii=False, indent=2), encoding="utf-8")
print("released:", release["released"], "| kept:", release["kept_tiers"], "| new tiers:", NEW_TIER, "| top20 changed:", release["top20_membership_changed"])
