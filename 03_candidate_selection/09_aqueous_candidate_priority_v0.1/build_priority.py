"""Build the scoped report and workbook inputs from original-extraction registers."""
import csv
import json
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path

from review_inputs import PANEL, PANEL_2008, PANEL_2016, PANEL_2026

HERE = Path(__file__).resolve().parent
SELECTION = HERE.parent
ROOT = SELECTION.parent
REVIEW = SELECTION / "08_capacity_review_validation"
PROFILE = ROOT / "02_identity_and_evidence/results/candidate_evidence_profiles.csv"
METHODS = ["ORAC-FL", "ORAC-PGR", "Crocin", "ABTS", "DPPH", "FRAP", "CUPRAC"]
HISTORICAL = {"10.1021/jp307746c", "10.1021/jf010586o", "10.1021/jf0305231",
              "10.1016/j.foodchem.2008.08.013", "10.3762/bjoc.11.151", "10.3390/molecules18055389"}


def read(path):
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write(name, rows):
    with (HERE / name).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def number(value):
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


def observation(cid, compound, assay, doi, value, error, unit, block, direction,
                locator, status, note, window, **details):
    molar = unit in {"micromol TE/micromol compound", "mol TE/mol compound", "reported molar capacity ratio"}
    return dict(candidate_id=cid, compound=compound, assay=assay, doi=doi,
                value=number(value), reported_error=number(error), unit=unit, protocol_block=block,
                direction=direction, locator=locator, disposition=status, unresolved=note,
                date_scope=window, pH=details.get("pH", ""), temperature_C=details.get("temp", ""),
                reported_repeats=details.get("repeats", ""), independent_n=details.get("independent_n", ""),
                error_definition=details.get("error_type", ""), material=details.get("material", ""),
                source_id=details.get("source_id", ""), source_locator=details.get("source", ""),
                prior_source_sha256=details.get("sha", ""), molar_TE_if_reported=number(value) if molar else None)


def extract(profiles):
    rows = []
    accepted = {r["evidence_id"]: r for r in read(REVIEW / "Connected_Conditional_Analysis_Input.csv")}
    for r in read(REVIEW / "Capacity_Row_Review.csv"):
        evid = r["evidence_id"]
        assay = "ORAC-PGR" if "ORAC_PGR" in evid else "ORAC-FL"
        if r["disposition"] == "OTHER_PROBE_ENDPOINT" and assay != "ORAC-PGR":
            assay = "Other probe"
        doi = r["doi"]
        window = "Historical reference" if doi in HISTORICAL else "Primary-window source; see publication provenance"
        status = "Conditional within source" if (
            evid in accepted or (assay == "ORAC-PGR" and r["disposition"] == "OTHER_PROBE_ENDPOINT")
            or (doi == "10.3390/antiox12020505" and evid.startswith("VERIFIED2023-"))
        ) else r["disposition"]
        if doi == "10.1371/journal.pone.0251534" and r["candidate_id"] == "AFF-0100":
            status = "Isolated observation; no rank"
        block = accepted[evid]["source_block"] if evid in accepted else r["protocol"]
        if doi == "10.3390/antiox12020505":
            block += " | Table 3 TE-AUC calibration slope ratio"
        rows.append(observation(r["candidate_id"], r["compound"], assay, doi, r["raw_mean"],
                                r["raw_error"], r["raw_units"], block, "Higher", r["locator"],
                                status, r["unresolved"], window, pH=r["pH"], temp=r["temperature_C"],
                                independent_n=r["independent_n"], error_type=r["error_definition"],
                                material=r["material_identity"], source_id=evid, source=r["source_document"], sha=r["source_sha256"]))
    for cid, frap, frap_sd, dpph, dpph_sd in PANEL_2026:
        for assay, val, err, unit, block, direction, pH in (
            ("FRAP", frap, frap_sd, "umol Trolox equivalents/mg standard", "593 nm; Fe-TPTZ; methanolic stocks", "Higher", "3.6"),
            ("DPPH", dpph, dpph_sd, "ug/mL SC50", "517 nm; methanolic radical and serial dilutions", "Lower", ""),
        ):
            status = "Extrapolated; no rank" if assay == "DPPH" and val > 1000 else "Conditional within source"
            rows.append(observation(cid, profiles[cid]["compound_name"], assay, "10.3390/molecules31172942",
                        val, err, unit, block, direction, "Table 1; sections 3.2-3.5", status,
                        "Exact form/lot and independent replicate hierarchy not established",
                        "Primary; 2026-08-22", pH=pH, repeats="3 reported", error_type="SD",
                        material="Named commercial standard", source_id=f"MOLECULES2026:{assay}:{cid}",
                        source="https://pmc.ncbi.nlm.nih.gov/articles/PMC13567273/"))
    for cid, abts, frap, dpph in PANEL_2016:
        for assay, val, block, pH in (
            ("ABTS", abts, "651 nm; HRP/H2O2 ABTS radical, phosphate", "6.0"),
            ("FRAP", frap, "Fe-TPTZ reduction; source protocol section 3.5", ""),
            ("DPPH", dpph, "DPPH reduction; source protocol section 3.6", ""),
        ):
            rows.append(observation(cid, profiles[cid]["compound_name"], assay, "10.3390/molecules21020208",
                        val, None, "relative to myricetin-3-O-glucoside", block, "Higher",
                        "Table 3; sections 3.4-3.6", "Conditional within source",
                        "Reference-relative endpoint; no Table 3 error; exact form and independent n pending",
                        "Evidence-gap extension; 2016", pH=pH, material="Named test standard",
                        source_id=f"MOLECULES2016:{assay}:{cid}", source="https://www.mdpi.com/1420-3049/21/2/208"))
    for cid, cuprac, abts in PANEL_2008:
        for assay, val, block in (
            ("CUPRAC", cuprac, "Normal room-temperature Cu-neocuproine; 450 nm"),
            ("ABTS", abts, "ABTS/persulfate; source section 2.3"),
        ):
            rows.append(observation(cid, profiles[cid]["compound_name"], assay, "10.1016/j.talanta.2008.06.028",
                        val, None, "Trolox-relative molar response slope", block, "Higher",
                        "Table 3, normal CUPRAC or ABTS column; sections 2 and 3.1",
                        "Conditional within source", "Historical calibration only; slope variance and material equivalence unverified",
                        "Historical reference; 2008", material="Named pure-compound standard",
                        source_id=f"TALANTA2008:{assay}:{cid}", source="https://nek.istanbul.edu.tr/ekos/MAKALE/M6210.pdf"))
    assert len({r["source_id"] for r in rows}) == len(rows)
    return rows


def rank(rows):
    groups = defaultdict(list)
    for r in rows:
        if r["value"] is not None and r["candidate_id"] and r["disposition"] == "Conditional within source":
            groups[tuple(r[k] for k in ("assay", "doi", "protocol_block", "unit", "direction"))].append(r)
    rankings, comparisons = [], []
    for (assay, doi, block, unit, direction), obs in sorted(groups.items()):
        by_cid = defaultdict(list)
        for r in obs:
            by_cid[r["candidate_id"]].append(r)
        estimates = {cid: rs[0] for cid, rs in by_cid.items() if len(rs) == 1}
        if len(estimates) < 2:
            continue
        ordered = sorted(estimates.values(), key=lambda r: (
            r["value"] * (1 if direction == "Lower" else -1), r["candidate_id"]))
        for i, r in enumerate(ordered):
            position = next(j + 1 for j, earlier in enumerate(ordered[:i+1]) if earlier["value"] == r["value"])
            rankings.append(dict(rank_in_block=position, compared_compounds=len(ordered), **r))
        comparisons.append(dict(assay=assay, doi=doi, block=block, compounds=len(ordered), excluded_multiple_rows=len(by_cid)-len(estimates)))
    return rankings, comparisons


def method_agreement(rankings, doi, first, second):
    scores = {assay: {r["candidate_id"]: r["rank_in_block"] for r in rankings
                      if r["doi"] == doi and r["assay"] == assay} for assay in (first, second)}
    shared = sorted(scores[first].keys() & scores[second].keys())
    products = [(scores[first][a]-scores[first][b]) * (scores[second][a]-scores[second][b])
                for a, b in combinations(shared, 2)]
    return len(shared), sum(n > 0 for n in products), sum(n < 0 for n in products), products.count(0)


def main():
    profiles = {r["candidate_id"]: r for r in read(PROFILE)}
    prior = {r["candidate_id"]: r for r in read(REVIEW / "Candidate_Review_and_Inclusion_Progress.csv")}
    sensitivity = {r["candidate_id"]: r for r in read(REVIEW / "Top20_Conditional_Uncertainty.csv")}
    rows = extract(profiles)
    assert all(not r["candidate_id"] or r["candidate_id"] in profiles for r in rows)
    rankings, comparisons = rank(rows)
    by_candidate = defaultdict(list)
    for row in rows:
        by_candidate[row["candidate_id"]].append(row)
    rank_counts = Counter(r["candidate_id"] for r in rankings)
    coverage, panel, queue = [], [], []
    for cid, p in profiles.items():
        obs = by_candidate[cid]
        main = [r for r in obs if r["date_scope"].startswith("Primary")]
        coverage.append(dict(candidate_id=cid, compound=p["compound_name"],
            retrieved_linked_articles=int(prior[cid]["retrieved_linked_articles"]),
            previously_located_leads=int(prior[cid]["abstract_or_body_located_leads"]),
            audited_original_DOIs=len({r["doi"] for r in obs}), original_numeric_rows=sum(r["value"] is not None for r in obs),
            primary_numeric_DOIs=len({r["doi"] for r in main if r["value"] is not None}),
            ranked_observations=rank_counts[cid], eligible_comparison_DOIs=len({r["doi"] for r in rankings if r["candidate_id"] == cid}),
            legacy_conditional_FL_DOIs=int(prior[cid]["conditional_analysis_DOIs"]),
            assays="; ".join(sorted({r["assay"] for r in obs})),
            quality_flags="; ".join(sorted({r["disposition"] for r in obs})) or "NO_ORIGINAL_NUMERIC_ROW_IN_THIS_OVERLAY",
            independent_study_count="NOT_ESTABLISHED",
            human_review_status="NOT_REVIEWED"))
    for order, (cid, tier, family, reason, risk, food_doi, food_locator) in enumerate(PANEL, 1):
        p, obs = profiles[cid], by_candidate[cid]
        old = sensitivity.get(cid, {})
        matched = [r for r in rankings if r["candidate_id"] == cid]
        source_set = {r["doi"] for r in matched}
        fl = [r for r in matched if r["assay"] == "ORAC-FL"]
        representative = next((r for r in fl if r["date_scope"].startswith("Primary")), fl[0] if fl else None)
        if cid in {"AFF-0104", "NEW-GSH", "AFF-0060"}:
            representative = next((r for r in matched if r["doi"] == "10.3390/antiox12020505"), representative)
        panel.append(dict(tier=tier, work_queue_position=order, candidate_id=cid,
            compound=p["compound_name"], formula=p["molecular_formula"], pubchem_cid=p["pubchem_cid"],
            inchi_key=p["inchi_key"], family=family, rationale=reason, material_and_assay_gate=risk,
            food_occurrence_evidence=food_locator or (p["reported_food_examples"] + " (curated lead; exact form pending)"),
            food_source_DOI=food_doi, methods="; ".join(sorted({r["assay"] for r in obs})),
            representative_reported_value=representative["value"] if representative else None,
            representative_unit=representative["unit"] if representative else "",
            representative_DOI=representative["doi"] if representative else "",
            distinct_comparison_reports=len(source_set), independent_studies="NOT_ESTABLISHED",
            source_DOIs="; ".join(sorted({r["doi"] for r in obs})),
            prior_FL_position=number(old.get("full_fit_position")), prior_FL_DOI_weighted_position=number(old.get("equal_DOI_position")),
            prior_FL_deletion_best=number(old.get("deletion_best_position")),
            prior_FL_deletion_worst=number(old.get("deletion_worst_position")),
            quality="CONDITIONAL_SOURCE_EVIDENCE" if matched else "SOURCE_OR_ENDPOINT_HOLD",
            experimental_status="NO_WATER_PHASE_MEASUREMENT_OR_LOT_APPROVAL", human_review_status="NOT_REVIEWED"))
        queue.append(dict(candidate_id=cid, compound=p["compound_name"], proposed_tier=tier,
                          decision_needed=risk, formal_state="NOT_REVIEWED", change_applied="NO"))
    for gate, message in (
        ("SCOPE", "Approve targeted decision scope and treatment of discovery-only and historical references."),
        ("ASSAY", "Approve pilot method and interference/solubility release gates."),
        ("EVIDENCE", "Adjudicate identity, exact dietary form, study independence and unresolved protocol holds.")
    ):
        queue.append(dict(candidate_id=gate, compound="", proposed_tier="", decision_needed=message,
                          formal_state="NOT_REVIEWED", change_applied="NO"))
    write("Available_Evidence_Coverage.csv", coverage)
    write("Researcher_Approval_Queue.csv", queue)
    status = [{"assay": m, "ranked_rows": sum(r["assay"] == m for r in rankings),
               "blocks": sum(r["assay"] == m for r in comparisons),
               "interpretation": "Source/condition-specific descriptive order" if any(r["assay"] == m for r in rankings)
               else "No verified comparable compound panel in this release"} for m in METHODS]
    payload = dict(methods=status, rankings=rankings, observations=rows, panel=panel, blocks=comparisons)
    (ROOT / "download_raw/antioxidants_priority_v01.json").write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    print("profiles", len(coverage), "observations", len(rows), "ranked identities", len(rank_counts),
          "panel", Counter(r["tier"] for r in panel), status)
    assert len(panel) == len({r["candidate_id"] for r in panel}) == 24
    assert all(r["formula"] and r["inchi_key"] for r in panel)
    lines = ["# Candidate evidence profiles", "",
             "Priority order is a review queue within each tier. All candidates need human release.", ""]
    for r in panel:
        old = r["prior_FL_position"]
        diagnostic = f" Prior conditional component position {int(old)} of 51." if old is not None else ""
        lines.extend([f"## {r['compound']} ({r['tier']})", "",
                      f"{r['rationale']}. {r['material_and_assay_gate']}.{diagnostic}",
                      f"Food evidence: {r['food_occurrence_evidence']}. {r['food_source_DOI'] or 'Exact occurrence source pending.'}",
                      f"Original observation DOIs: {r['source_DOIs'] or 'Pending'}.",
                      ""])
    (HERE / "Top_Candidate_Evidence_Profiles.md").write_text("\n".join(lines), encoding="utf-8")
    stable = [r for r in panel if r["tier"] == "A"]
    facts = []
    for r in stable:
        subset = [x for x in rankings if x["candidate_id"] == r["candidate_id"]]
        paper_count = len({x["doi"] for x in subset})
        strict = len({x["doi"] for x in subset if x["assay"] == "ORAC-FL" and x["pH"] == "7.4"
                      and number(x["temperature_C"]) == 37 and x["date_scope"].startswith("Primary")})
        recent = len({x["doi"] for x in subset if x["date_scope"].startswith("Primary")})
        facts.append(f"| {r['compound']} | {paper_count} | {max(0, paper_count-1)} | {recent} | {strict} |")
    robustness = """# Ranking robustness and uncertainty

Ranks use reported means in the same DOI, assay, endpoint, protocol block and raw unit. Lower SC50 is favorable. Higher values are favorable for the reported capacity/relative-response endpoints. Tied values share rank. An independent sampling variance is unavailable for most observations. These are descriptive positions and support bounds, with no inferential confidence interval.

The prior 51-compound conditional FL model gives Catechin 3 (deletion bounds 2-10), Quercetin 4 (2-12), Hesperetin 7 (3-15), and L-ascorbic acid 50 (42-50). Bounds refer to the fixed connected universe. Prior equal-row versus equal-total-DOI top-20 overlap is 17 per the generated review summary, which supersedes the conflicting narrative count. The 2.5/5 uM sensitivity gives 20/20 equal-row and 19/20 equal-DOI overlap. Rosmarinic acid and gallocatechin have single-DOI leverage. Dropping a singleton removes its evidence for that stratum.

Within the historical 2016 panel, epicatechin exceeds catechin for ABTS, while catechin exceeds epicatechin in the FRAP and DPPH columns. Myricetin performs very differently in the separate 2026 ferric reducing panel. Hesperetin's high conditional ORAC-FL position contrasts with its 0.36 PGR result in the Zhang 2013 probe stratum. These changes reflect endpoint and protocol dependence. No cross-assay mean or numerical transfer coefficient is used.

| A candidate | Distinct reports in ranked blocks | Minimum retained after deletion of one supporting DOI | Primary-window reports across assays | Primary FL pH 7.4 and 37 C reported DOIs |
|---|---:|---:|---:|---:|
"""
    robustness += "\n".join(facts) + "\n\nThe final column checks reported pH and temperature only. Dose, final vehicle and independence still differ. A placement also requires a food-occurrence source and a useful bench comparison, so removing an assay or restricting windows can remove efficacy support without assigning a zero response.\n"
    for doi, first, second in (("10.1021/jp307746c", "ORAC-FL", "ORAC-PGR"),
                               ("10.3390/molecules31172942", "FRAP", "DPPH")):
        common, same, reversed_pairs, ties = method_agreement(rankings, doi, first, second)
        robustness += (f"\nThe {doi} comparison of {first} with {second} shares {common} compounds. "
                       f"Across their pairs, {same} agree, {reversed_pairs} reverse and {ties} include ties.\n")
    (HERE / "Ranking_Robustness_and_Uncertainty.md").write_text(robustness, encoding="utf-8")
    qc = f"""# Quality control

Reconciled {len(coverage)} candidate profiles with {len(rows)} original-observation rows from {len({r['doi'] for r in rows})} distinct DOIs. {len(rankings)} observations for {len(rank_counts)} distinct candidates enter at least one conditional study block. They include {len({r['candidate_id'] for r in rankings if r['assay']=='ORAC-FL'})} ORAC-FL candidates. The research pool has 24 defined structures and no approved materials or applied evidence changes. Identifiers, row uniqueness, units, source locators and human review state are retained. Multi-row same-block comparisons are withheld where duplicate/dose structure is unclear. Censored/extrapolated values remain in the evidence sheet. No institutional record contents enter public artifacts.

Rebuild using `python build_priority.py` and `node build_workbooks.mjs` from this folder, with the bundled artifact-tool package available via local module resolution or CODEX_SPREADSHEET_MODULES. The intermediate JSON is generated in the ignored download_raw directory. For comparisons where exact powder hydration remains unresolved, original units are retained as analysis units. Independent experiments and technical replicates are separate fields. The historical freezes and WoS source export are outside the build inputs.
"""
    (HERE / "QC_Report.md").write_text(qc, encoding="utf-8")


if __name__ == "__main__":
    main()
