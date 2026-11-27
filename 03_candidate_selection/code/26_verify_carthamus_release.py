"""Verify the Carthamus release. Run from root."""
import csv, json, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
RUN = ROOT / "03_candidate_selection/12_evidence_expansion/run_carthamus_2026-11-27"
ok = True
def check(n, c):
    global ok; print(("PASS " if c else "FAIL ") + n); ok = ok and c
m = list(csv.DictReader((RUN / "Candidate_Membership_Review.csv").open(encoding="utf-8-sig", newline="")))
r = list(csv.DictReader((RUN / "Candidate_Membership_Review_RELEASED.csv").open(encoding="utf-8-sig", newline="")))
rel = json.loads((RUN / "Release_Record.json").read_text(encoding="utf-8"))
check("released rows == membership rows", len(r) == len(m))
check("all decisions APPROVED", all(x["decision"].startswith("APPROVED") for x in r))
check("unaffected keep prior tier", all(x["proposed_next_tier"] == x["prior_tier"] for x in r if x["affected_by_new_direct_evidence"] == "False"))
check("release flag True", rel["released"] is True)
check("Top20 unchanged", rel["top20_membership_changed"] is False)
check("new tiers assigned", {"AFF-0019", "AFF-0062"} <= {x["candidate_id"] for x in r if x["affected_by_new_direct_evidence"] == "True"})
print("VERIFY", "PASS" if ok else "FAIL"); sys.exit(0 if ok else 1)
