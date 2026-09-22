import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "h_orac_stage25b"
CFG = ROOT / "methods_qc" / "config"

def read(path):
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

def write(path, rows):
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)

audit = read(DATA / "Stage25B2_TierA_Feasibility_Audit.csv")
evidence = read(DATA / "Stage25B_HORAC_Experiment_Evidence.csv")
ranking = read(DATA / "Stage25B_HORAC_Quantitative_Ranking.csv")
e_by_id = {r["independent_experiment_id"]: r for r in evidence}

rubric = [
    ("architecture", "Universal core + objective compound-risk profile + triggered enhanced QC + tier assignment + independent flags", "ESSENTIAL", "All", "Tier and flags are evaluated separately", "DRAFT; NOT YET CANONICAL"),
    ("identity_and_form", "Unique chemical identity and chemically consequential form support a molar denominator", "ESSENTIAL", "A/B1", "Unresolved material identity is X; mixture/extract is C", "Pure-compound gate"),
    ("assay_construct", "AAPH + fluorescein + Trolox in an aqueous/buffer reaction environment", "ESSENTIAL", "A/B1", "Non-FL/non-AAPH/unbridgeable arm is C; unknown construct is X", "Universal core"),
    ("reaction_conditions", "Buffer identity, pH, temperature and reagent concentrations are EXPLICITLY_REPORTED, DERIVABLE_FROM_METHOD, or exactly TRACEABLE_TO_REFERENCED_PROTOCOL", "ESSENTIAL", "A/B1", "Material unknowns prevent A; unresolved comparability may be B2/X", "A citation alone is not traceability"),
    ("candidate_exposure", "Candidate concentration/range and dose-response/linearity context are interpretable", "ESSENTIAL", "A/B1", "Saturation/nonlinearity is B2/C; missing but nonmaterial context may remain B1", "Universal core"),
    ("solvent_interpretability", "Stock solvent and final reaction solvent are explicit or unambiguously derivable", "ESSENTIAL", "A/B1", "Unknown or materially perturbing solvent without control is B2/X", "Explicit and derived values remain distinct"),
    ("kinetic_readout", "Kinetic fluorescence decay with net AUC or a scientifically equivalent kinetic ORAC calculation", "ESSENTIAL", "A/B1", "Endpoint-only/noncomparable readout is C; unknown readout is X", "Universal core"),
    ("quantitative_traceability", "Original value, unit and mol TE/mol conversion are reproducible", "ESSENTIAL", "A/B1", "Figure-only/nonrecoverable value is B2 or X and cannot enter primary ranking", "Universal core"),
    ("replication_precision", "Replicate information or precision measure is sufficiently interpretable", "IMPORTANT", "A/B1", "Missing precision prevents A but does not automatically force B2", "Independent reporting flag retained"),
    ("purity", "Numerical/certified purity preferred; grade/supplier documented separately", "IMPORTANT", "A/B1", "Missing numerical purity alone does not force B2 unless material impurity risk exists", "Independent purity flag retained"),
    ("R1_optical", "Enhanced optical QC is mandatory only when objective R1 trigger is MODERATE/HIGH", "RISK-DEPENDENT", "A", "Unaddressed material optical risk is B2", "Low-risk compounds need a general assay blank, not universal compound-only blank"),
    ("R2_solubility_aggregation", "Enhanced solubility/aggregation QC is mandatory only when objective R2 trigger is MODERATE/HIGH", "RISK-DEPENDENT", "A", "Unaddressed material precipitation/aggregation risk is B2", "DLS is not universally required"),
    ("R3_cosolvent", "Matched solvent control and kinetic comparability are required when organic cosolvent is material", "RISK-DEPENDENT", "A", "Material unmatched cosolvent is B2; incompatible arm is C", "Final percentage may be derived only without dilution ambiguity"),
    ("R4_redox", "Enhanced mechanistic controls are required for objective redox/probe-interaction triggers", "RISK-DEPENDENT", "A", "Unresolved material redox/probe interference is B2", "Quinone-like/prooxidant cases require review"),
    ("tier_A", "Universal core fully satisfied; every triggered enhanced QC addressed; quantitative traceability high", "ASSIGNMENT", "A", "No unresolved material risk", "Draft definition"),
    ("tier_B1", "Universal core sufficiently satisfied for quantitative comparison; no unresolved material risk likely to invalidate ranking; reporting limitations remain", "ASSIGNMENT", "B1", "Eligible for primary A+B1", "Draft definition"),
    ("tier_B2", "Quantitative H-ORAC-like value exists but one or more material comparability risks remain unresolved", "ASSIGNMENT", "B2", "Sensitivity only", "Draft definition"),
    ("tier_C", "Assay construct or normalization is known incompatible with H-ORAC-FL ranking", "ASSIGNMENT", "C", "Exclude from quantitative ranking", "Draft definition"),
    ("tier_X", "Information/source/provenance is insufficient to adjudicate method identity or quantitative value", "ASSIGNMENT", "X", "Hold pending evidence", "Draft definition"),
]
write(CFG / "ORAC_Literature_Eligibility_Rubric_v2_DRAFT.csv", [dict(zip(["criterion","draft_requirement","requirement_nature","applies_to","failure_consequence","notes"], x)) for x in rubric])

risk_rules = [
    ("R1 optical", "Measured absorbance overlaps 465–505 nm excitation or 500–550 nm emission; or intrinsic fluorescence is reported in those bands", "Spectrum or primary-method statement", "HIGH", "Compound-only fluorescence/absorbance correction or validated matched interference control", "Residual signal shown nonmaterial at assay concentration", "Any missing spectrum/QC when overlap is known"),
    ("R1 optical", "Anthocyanin/betalain/strong visible chromophore class, or concentration-dependent quenching is reported", "Defined structure/class plus source method", "HIGH", "Compound-only control plus inner-filter/quenching validation", "Correction/validation covers the tested range", "Always if enhanced QC absent"),
    ("R1 optical", "UV-visible chromophore without known overlap and assay concentration is above 10 µM", "Structure plus concentration", "MODERATE", "Spectrum, matched compound blank, or documented no-interference validation", "No material interference at assay concentration", "If concentration or spectrum unavailable"),
    ("R1 optical", "No visible chromophore/intrinsic fluorescence evidence and concentration ≤10 µM", "Structure plus concentration", "LOW", "General assay blank", "Standard blank/net-AUC correction present", "Escalate if contrary evidence appears"),
    ("R2 solubility/aggregation", "Visible precipitation/turbidity, nonmonotonic response, or concentration exceeds documented aqueous solubility", "Primary observation or cited solubility at assay pH", "HIGH", "Solubility demonstration and aggregation/precipitation control", "Clear solution and monotonic range below limit", "Any unresolved high-risk signal"),
    ("R2 solubility/aggregation", "Hydrophobic/poorly water-soluble compound requires organic stock or logP/solubility evidence indicates borderline exposure", "Stock solvent plus objective solubility/logP source", "MODERATE", "Concentration below plausible limit, dose response, controlled cosolvent, no precipitation evidence", "All four conditions supported", "If solubility evidence or visual/dose response check missing"),
    ("R2 solubility/aggregation", "Aqueous/buffer soluble compound tested below documented or chemically plausible solubility", "Method plus identity", "LOW", "No direct aggregation assay required", "Interpretable aqueous exposure", "Escalate on precipitation/nonlinearity"),
    ("R3 cosolvent", "Final organic cosolvent >5% v/v or RMCD/detergent materially changes assay arm", "Explicit or unambiguous volume calculation", "HIGH", "Matched solvent calibration/control plus kinetic equivalence or validated bridge", "Control demonstrates nonmaterial effect", "Missing matched control is B2; incompatible arm may be C"),
    ("R3 cosolvent", "Final organic cosolvent >1% to ≤5% v/v", "Explicit or unambiguous volume calculation", "MODERATE", "Matched solvent control for samples and Trolox/blank", "Equivalent solvent across comparison", "Missing match requires human review/B2"),
    ("R3 cosolvent", "Final organic cosolvent ≤1% v/v", "Explicit or unambiguous volume calculation", "LOW", "Record percentage; matched control preferred", "No kinetic anomaly and solvent interpretable", "Escalate if solvent identity/percentage unclear"),
    ("R4 redox", "Quinone/quinone-like electrophore, documented redox cycling, prooxidant response, probe reaction or radical generation", "Defined structure plus experimental/cited mechanistic evidence", "HIGH", "Orthogonal control or kinetic evidence separating scavenging from probe/radical perturbation", "Material interference excluded", "HUMAN REVIEW REQUIRED if evidence incomplete"),
    ("R4 redox", "No objective redox/probe-interaction trigger", "Structure and available assay behavior", "LOW", "Standard kinetic ORAC controls", "Monotonic interpretable kinetic response", "Escalate on anomalous curves"),
]
write(CFG / "H_ORAC_Compound_Risk_Trigger_Rules_v1_DRAFT.csv", [dict(zip(["risk_domain","trigger","evidence_required","risk_level","enhanced_QC_required","pass_condition","failure_consequence","human_review_condition"], x + (("YES" if "review" in x[-1].lower() or "missing" in x[-1].lower() else "CONDITIONAL"),))) for x in risk_rules])

profiles = {
    "HORAC_EXP_0065": ("B1","YES","LOW","general blank","ADEQUATE","LOW","aqueous-dose context","ADEQUATE","LOW","record derived 0.2–0.4% ethanol","ADEQUATE","LOW","standard kinetics","ADEQUATE","MODERATE","B1→B1; cited-protocol details limit A"),
    "HORAC_EXP_0026": ("B1","YES","LOW","general blank","ADEQUATE","MODERATE","solubility plus controlled cosolvent","PARTIAL","UNCLEAR","final acetone percentage","NOT_REPORTED","LOW","standard kinetics","ADEQUATE","MODERATE","B1→B1; final acetone and solubility reporting limit A"),
    "HORAC_EXP_0002": ("B1","PARTIAL","LOW","general blank","UNCLEAR","LOW","aqueous exposure","UNCLEAR","UNCLEAR","source recovery","UNCLEAR","LOW","standard kinetics","UNCLEAR","LOW","B1 retained; inaccessible full text prevents A"),
    "HORAC_EXP_0050": ("A","YES","LOW","general blank","ADEQUATE","LOW","aqueous/controlled solvent exposure","ADEQUATE","MODERATE","matched 5% ethanol control","ADEQUATE","LOW","standard kinetics","ADEQUATE","HIGH","B1→A; universal core and triggered solvent QC addressed"),
    "HORAC_EXP_0028": ("B1","YES","MODERATE","compound optical check","NOT_REPORTED","HIGH","solubility plus controlled cosolvent","PARTIAL","UNCLEAR","final acetone percentage","NOT_REPORTED","LOW","standard kinetics","ADEQUATE","MODERATE","B1→B1; unresolved but not demonstrated material risk limits A"),
    "HORAC_EXP_0059": ("B1","YES","LOW","general blank","ADEQUATE","LOW","aqueous-dose context","ADEQUATE","LOW","record derived 0.2–0.4% ethanol","ADEQUATE","LOW","standard kinetics","ADEQUATE","MODERATE","B1→B1; referenced-protocol detail limits A"),
    "HORAC_EXP_0058": ("A","YES","LOW","general blank","ADEQUATE","LOW","aqueous exposure","ADEQUATE","LOW","aqueous buffer","ADEQUATE","LOW","standard kinetics","ADEQUATE","HIGH","B1→A; core complete and no enhanced trigger"),
    "HORAC_EXP_0056": ("A","YES","LOW","general blank","ADEQUATE","LOW","aqueous exposure","ADEQUATE","LOW","aqueous buffer","ADEQUATE","LOW","standard kinetics","ADEQUATE","HIGH","B1→A; core complete and no enhanced trigger"),
    "HORAC_EXP_0057": ("A","YES","LOW","general blank","ADEQUATE","LOW","aqueous exposure","ADEQUATE","LOW","aqueous buffer","ADEQUATE","LOW","standard kinetics","ADEQUATE","HIGH","B1→A; core complete and no enhanced trigger"),
    "HORAC_EXP_0033": ("B1","YES","MODERATE","compound optical check","NOT_REPORTED","HIGH","solubility plus controlled cosolvent","PARTIAL","UNCLEAR","final acetone percentage","NOT_REPORTED","LOW","standard kinetics","ADEQUATE","MODERATE","B1→B1; high solubility risk prevents A"),
    "HORAC_EXP_0067": ("B2","PARTIAL","LOW","general blank","ADEQUATE","LOW","identity/form and solubility check","PARTIAL","HIGH","matched 10% methanol control and kinetic bridge","NOT_REPORTED","LOW","standard kinetics","ADEQUATE","MODERATE","B1→B2 simulated; material unmatched methanol and identity uncertainty"),
    "HORAC_EXP_0072": ("B1","YES","LOW","general blank","ADEQUATE","MODERATE","dose response and solubility plausibility","PARTIAL","LOW","record trace ethanol","ADEQUATE","LOW","standard kinetics","ADEQUATE","HIGH","B1→B1; direct solubility confirmation absent"),
    "HORAC_EXP_0073": ("B1","YES","LOW","general blank","ADEQUATE","HIGH","solubility/aggregation justification","PARTIAL","LOW","record trace ethanol","ADEQUATE","LOW","standard kinetics","ADEQUATE","HIGH","B1→B1; capsaicin solubility risk prevents A"),
    "HORAC_EXP_0049": ("A","YES","LOW","general blank","ADEQUATE","LOW","aqueous exposure","ADEQUATE","LOW","aqueous buffer","ADEQUATE","LOW","standard kinetics","ADEQUATE","HIGH","B1→A; core complete and no enhanced trigger"),
    "HORAC_EXP_0060": ("B1","YES","LOW","general blank","ADEQUATE","LOW","aqueous-dose context","ADEQUATE","LOW","record derived 0.2–0.4% ethanol","ADEQUATE","LOW","standard kinetics","ADEQUATE","MODERATE","B1→B1; referenced-protocol detail limits A"),
    "HORAC_EXP_0046": ("B2","YES","HIGH","anthocyanin optical/inner-filter validation","NOT_REPORTED","LOW","aqueous exposure","UNCLEAR","UNCLEAR","final solvent interpretation","UNCLEAR","MODERATE","pH/redox stability check","NOT_REPORTED","LOW","B2→B2; high optical risk remains unresolved"),
    "HORAC_EXP_0047": ("B2","YES","HIGH","anthocyanin optical/inner-filter validation","NOT_REPORTED","LOW","aqueous exposure","UNCLEAR","UNCLEAR","final solvent interpretation","UNCLEAR","MODERATE","pH/redox stability check","NOT_REPORTED","LOW","B2→B2; high optical risk remains unresolved"),
    "HORAC_EXP_0070": ("X","NO","UNCLEAR","source/value recovery","UNCLEAR","UNCLEAR","source/value recovery","UNCLEAR","UNCLEAR","source/value recovery","UNCLEAR","UNCLEAR","source/value recovery","UNCLEAR","LOW","B2→X simulated; figure-only value is not quantitatively traceable"),
    "HORAC_EXP_0071": ("B2","YES","MODERATE","compound optical validation","NOT_REPORTED","HIGH","solubility/aggregation plus solvent disclosure","NOT_REPORTED","UNCLEAR","final solvent and matched control","NOT_REPORTED","LOW","standard kinetics","ADEQUATE","MODERATE","B2→B2; optical/solubility risks remain unresolved"),
    "HORAC_EXP_0069": ("X","NO","UNCLEAR","identity/source recovery","UNCLEAR","UNCLEAR","identity/source recovery","UNCLEAR","UNCLEAR","source recovery","UNCLEAR","UNCLEAR","source recovery","UNCLEAR","LOW","X→X; positional identity and conversion remain unresolved"),
}

rows=[]
for exp_id, p in profiles.items():
    e=e_by_id[exp_id]
    sim, core, r1, r1req, r1qc, r2, r2req, r2qc, r3, r3req, r3qc, r4, r4req, r4qc, completeness, reason = p
    old=e["H_ORAC_tier"]
    rows.append({
        "candidate":e["canonical_name"], "experiment_id":exp_id, "publication_id":e["publication_id"], "DOI":e["DOI"],
        "old_tier":old, "simulated_v2_tier":sim, "universal_core_pass":core,
        "R1_optical_risk":r1, "R1_required_QC":r1req, "R1_QC_status":r1qc,
        "R2_solubility_aggregation_risk":r2, "R2_required_QC":r2req, "R2_QC_status":r2qc,
        "R3_cosolvent_risk":r3, "R3_required_QC":r3req, "R3_QC_status":r3qc,
        "R4_redox_interference_risk":r4, "R4_required_QC":r4req, "R4_QC_status":r4qc,
        "identity_flag":"PASS" if e["compound_form"] and "ambiguous" not in e["major_method_caveat"].lower() else "REVIEW",
        "purity_reporting_flag":"NUMERIC" if "%" in e["compound_purity"] else "GRADE_OR_UNREPORTED",
        "reporting_completeness":completeness, "source_access_flag":"AVAILABLE" if exp_id not in {"HORAC_EXP_0002","HORAC_EXP_0069","HORAC_EXP_0070"} else "LIMITED",
        "protocol_traceability_flag":"PASS" if core=="YES" else "REVIEW",
        "tier_change_simulated":"YES" if old!=sim else "NO", "reason_for_change":reason,
        "would_enter_or_leave_primary_A_B1_set":"LEAVE" if old in {"A","B1"} and sim not in {"A","B1"} else ("ENTER" if old not in {"A","B1"} and sim in {"A","B1"} else "NO_CHANGE"),
        "potential_rank_effect":"Chlorogenic Acid rankable evidence removed; current Top20 unaffected" if exp_id=="HORAC_EXP_0067" else "No direct primary-set change",
        "human_review_required":"YES" if old!=sim or sim in {"B2","X"} else "NO",
    })
write(DATA / "Stage25B3_Rubric_v2_Validation.csv", rows)

# Ranking simulation is deliberately performed only after tier simulation.
remove_exp={r["experiment_id"] for r in rows if r["would_enter_or_leave_primary_A_B1_set"]=="LEAVE"}
eligible=[e for e in evidence if e["H_ORAC_tier"] in {"A","B1"} and e["independent_experiment_id"] not in remove_exp and e["converted_value_mol_TE_per_mol"]]
by_candidate={}
for e in eligible:
    by_candidate.setdefault(e["candidate_id"], []).append(float(e["converted_value_mol_TE_per_mol"]))
def median(v):
    v=sorted(v); n=len(v); return v[n//2] if n%2 else (v[n//2-1]+v[n//2])/2
sim_sorted=sorted(((cid, median(vals)) for cid,vals in by_candidate.items()), key=lambda x:(-x[1],x[0]))
sim_rank={cid:i+1 for i,(cid,_) in enumerate(sim_sorted)}
sim_val=dict(sim_sorted)
current={r["candidate_id"]:r for r in ranking}
names={e["candidate_id"]:e["canonical_name"] for e in evidence}
impact=[]
for cid in sorted(set(current)|set(sim_rank), key=lambda x:(sim_rank.get(x,999), int(current.get(x,{"rank":"999"})["rank"]))):
    cr=int(current[cid]["rank"]) if cid in current else None; sr=sim_rank.get(cid)
    impact.append({"candidate_id":cid,"candidate":names.get(cid,current.get(cid,{}).get("canonical_name","")),"current_rank":cr or "","current_median":current.get(cid,{}).get("median_H_ORAC_mol_TE_per_mol",""),"current_Top20":"yes" if cr and cr<=20 else "no","simulated_v2_rank":sr or "","simulated_v2_median":sim_val.get(cid,""),"simulated_v2_Top20":"yes" if sr and sr<=20 else "no","membership_change":"none" if bool(cr and cr<=20)==bool(sr and sr<=20) else ("enter" if sr and sr<=20 else "leave"),"causal_tier_decision":"HORAC_EXP_0067 simulated B1→B2" if cid=="AFF-0076" else "none","interpretation":"SIMULATION ONLY; canonical ranking unchanged"})
write(DATA / "Stage25B3_Rubric_v2_Ranking_Impact_Simulation.csv", impact)
print(f"wrote rubric={len(rubric)}, risk_rules={len(risk_rules)}, validation={len(rows)}, impact={len(impact)}")
