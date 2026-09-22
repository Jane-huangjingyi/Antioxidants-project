import csv
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "h_orac_stage25b"

with (DATA / "Stage25B_HORAC_Experiment_Evidence.csv").open(encoding="utf-8-sig", newline="") as f:
    evidence = {r["independent_experiment_id"]: r for r in csv.DictReader(f)}
with (DATA / "Stage25B_HORAC_Quantitative_Ranking.csv").open(encoding="utf-8-sig", newline="") as f:
    ranking = {r["candidate_id"]: r for r in csv.DictReader(f)}

P = "CONFIRMED_PRESENT"
N = "NOT_REPORTED"
E = "CONFIRMED_ABSENT"
X = "PREVIOUSLY_NOT_EXTRACTED"
U = "UNCLEAR"
NA = "NOT_APPLICABLE"

criteria = [
    "pure_compound_identity", "compound_purity_reported", "AAPH_reported",
    "AAPH_concentration_reported", "fluorescein_reported",
    "fluorescein_concentration_reported", "Trolox_standard_reported",
    "Trolox_range_reported", "buffer_reported", "buffer_concentration_reported",
    "pH_reported", "temperature_reported", "candidate_concentration_reported",
    "solvent_reported", "final_cosolvent_percent_reported",
    "compound_specific_blank_reported", "optical_interference_control_reported",
    "aggregation_assessment_reported", "kinetic_AUC_method_reported",
    "replicate_N_reported", "quantitative_value_traceable", "unit_traceable",
]

profiles = {
    "P010": dict(
        full_text_available="YES", full_text_rechecked="YES", journal="International Journal of Molecular Sciences",
        statuses=[P,N,P,X,P,X,P,X,P,X,P,P,N,X,N,N,N,N,X,X,P,P],
        purity="Supplier reported; no numerical purity/grade for individual flavonoids",
        cosolvent="Acetone/water 50:50 stock; working solutions diluted in buffer; final acetone percentage not stated or unambiguously derivable",
        location="Sections 3.1–3.3; Table 3", table="Table 3", figure="", supplement="",
        notes="Full text adds reagent concentrations, stock solvent, blank, kinetics and triplicate detail; no compound-specific optical blank or aggregation assessment.",
        decision="RETAINS_B1; DOES_NOT_MEET_STRICT_TIER_A",
    ),
    "P015": dict(
        full_text_available="YES", full_text_rechecked="YES", journal="Antioxidants",
        statuses=[P,X,N,N,N,N,P,N,N,N,N,N,X,X,X,N,N,N,X,X,P,P],
        purity="All reagents/solvents analytical or higher grade; no compound-specific numerical purity",
        cosolvent="1000 µM stocks in ethanol/water 80:20; final 0.2% or 0.4% ethanol is derivable for 2.5 or 5 µM if direct dilution is assumed",
        location="Sections 2.1 and 2.2.2; Tables 1–2", table="Tables 1–2", figure="", supplement="",
        notes="Current article delegates core ORAC reagent details to a cited procedure. Final ethanol is DERIVABLE_FROM_METHOD but not explicitly reported.",
        decision="RETAINS_B1; DOES_NOT_MEET_STRICT_TIER_A",
    ),
    "P014": dict(
        full_text_available="YES", full_text_rechecked="YES", journal="International Journal of Molecular Sciences",
        statuses=[P,X,P,X,P,X,P,X,P,X,P,P,X,X,X,N,N,N,X,X,P,P],
        purity="Phenolic acids from Sigma-Aldrich; other reagents at least analytical grade; no compound-specific numerical purity",
        cosolvent="All ORAC solutions prepared in 75 mM sodium phosphate buffer; no organic cosolvent reported for sampled phenolic acids",
        location="Sections 3.1 and 3.2.3; Table 2", table="Table 2", figure="", supplement="",
        notes="Full text recovers assay volumes, concentrations, pH, 37 °C, 60-min kinetics and four replicates; optical/aggregation QC absent from reporting.",
        decision="RETAINS_B1; DOES_NOT_MEET_STRICT_TIER_A",
    ),
    "P002": dict(
        full_text_available="YES", full_text_rechecked="YES", journal="Antioxidants",
        statuses=[P,X,P,X,P,X,P,X,P,X,P,P,X,X,X,N,N,N,X,X,P,P],
        purity="All chemicals analytical reagent grade; supplier reported; no compound-specific numerical purity",
        cosolvent="Caffeic acid final ethanol explicitly adjusted to 5% v/v with matched control wells; gallic acid prepared in buffer (0% organic cosolvent)",
        location="Sections 2.1–2.3; Table 3", table="Tables 1–3", figure="Figures 1–2", supplement="Figure S1",
        notes="Full text explicitly reports final ethanol and matched controls, but not a compound-only optical blank or aggregation assessment.",
        decision="RETAINS_B1; DOES_NOT_MEET_STRICT_TIER_A",
    ),
    "P017": dict(
        full_text_available="YES", full_text_rechecked="YES", journal="Foods",
        statuses=[U,N,P,X,P,X,P,X,P,X,P,P,X,X,X,N,N,N,X,X,P,P],
        purity="Compound isolated from plant material; identity characterization reported elsewhere/supplement, but assay-material purity not explicit",
        cosolvent="Compound sample prepared in methanol; 20 µL sample in 200 µL final well implies 10% v/v methanol if undiluted sample solvent is retained; matched ORAC solvent control not stated",
        location="Sections 2.1, 2.3 and 2.4.3; Table 4", table="Table 4", figure="", supplement="Table S3",
        notes="Potentially material 10% methanol is DERIVABLE_FROM_METHOD, not explicitly reported as final cosolvent; identity/form and matched solvent control require human review.",
        decision="HUMAN REVIEW REQUIRED — POTENTIAL B1 DOWNGRADE",
    ),
    "S25B1": dict(
        full_text_available="YES", full_text_rechecked="YES", journal="Foods",
        statuses=[P,P,P,X,P,X,P,X,P,X,P,P,P,X,X,N,N,N,P,P,P,P],
        purity="Eugenol ≥99%; capsaicin ≥95% (compound-specific)",
        cosolvent="Eugenol stock 500 mM in 20% ethanol; capsaicin stock 125 mM in 100% ethanol; ORAC working solutions prepared in PBS. Direct-dilution upper bounds at 6 µM are ~0.00024% and 0.0048% ethanol, respectively; final percentage not explicit",
        location="Sections 2.2 and 2.5.4; Table 5", table="Table 5", figure="", supplement="Figures S4–S5",
        notes="Purity and stock solvents were already extracted; final ethanol is DERIVABLE_FROM_METHOD only under direct-dilution assumption. No enhanced optical or aggregation QC.",
        decision="RETAINS_B1; DOES_NOT_MEET_STRICT_TIER_A",
    ),
    "P001": dict(
        full_text_available="NO", full_text_rechecked="NO", journal="Journal of Agricultural and Food Chemistry",
        statuses=[P,U,P,U,P,U,P,U,U,U,U,P,U,U,U,U,U,U,U,U,P,P],
        purity="Not verifiable in the available primary full text during this audit",
        cosolvent="Not verifiable in the available primary full text during this audit",
        location="Legacy extraction cites Table 4, p. 4622; primary full text not recovered for this audit", table="Table 4 (legacy citation)", figure="", supplement="",
        notes="Early-literature access-control row. Unknown fields are UNCLEAR, not interpreted as not performed or absent.",
        decision="RETAINS_CURRENT_B1_PENDING_FULL_TEXT; NO RECLASSIFICATION",
    ),
}

sample = [
    ("HORAC_EXP_0065", "P015"), ("HORAC_EXP_0026", "P010"),
    ("HORAC_EXP_0002", "P001"), ("HORAC_EXP_0050", "P002"),
    ("HORAC_EXP_0028", "P010"), ("HORAC_EXP_0059", "P015"),
    ("HORAC_EXP_0058", "P014"), ("HORAC_EXP_0056", "P014"),
    ("HORAC_EXP_0057", "P014"), ("HORAC_EXP_0033", "P010"),
    ("HORAC_EXP_0067", "P017"), ("HORAC_EXP_0072", "S25B1"),
    ("HORAC_EXP_0073", "S25B1"), ("HORAC_EXP_0049", "P002"),
    ("HORAC_EXP_0060", "P015"),
]

rows = []
for exp_id, profile_id in sample:
    e = evidence[exp_id]
    rank = ranking[e["candidate_id"]]
    p = profiles[profile_id]
    row = {
        "candidate_id": e["candidate_id"], "canonical_name": e["canonical_name"],
        "current_H_ORAC_rank": rank["rank"], "Stage25A_rank": rank["Stage25A_primary_rank"],
        "publication_id": e["publication_id"], "DOI": e["DOI"], "PMID": e["PMID"],
        "year": e["year"], "journal": p["journal"], "independent_experiment_id": exp_id,
        "current_tier": e["H_ORAC_tier"], "full_text_available": p["full_text_available"],
        "full_text_rechecked": p["full_text_rechecked"],
    }
    row.update(dict(zip(criteria, p["statuses"])))
    row.update({
        "compound_purity_value": p["purity"],
        "final_cosolvent_percent_value_or_derivation": p["cosolvent"],
        "source_page": p["location"], "source_table": p["table"],
        "source_figure": p["figure"], "source_supplement": p["supplement"],
        "experimental_comparability_confidence": "MODERATE" if profile_id not in {"P002", "P014", "S25B1"} else "MODERATE_TO_HIGH",
        "reporting_completeness": "LOW" if profile_id in {"P001", "P015"} else "MODERATE_TO_HIGH",
        "audit_decision": p["decision"], "audit_notes": p["notes"],
    })
    rows.append(row)

audit_path = DATA / "Stage25B2_TierA_Feasibility_Audit.csv"
with audit_path.open("w", encoding="utf-8-sig", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader(); w.writerows(rows)

criterion_meta = {
    "pure_compound_identity": ("ESSENTIAL_FOR_COMPARABILITY", "high", "UNIVERSAL", "Identity errors invalidate molar comparison", "Retain as universal core"),
    "compound_purity_reported": ("IMPORTANT_BUT_REPORTING_LIMITED", "moderate", "UNIVERSAL_DOCUMENTATION", "Impurities can bias per-mole values", "Retain; distinguish certified/numeric purity from grade/supplier"),
    "AAPH_reported": ("ESSENTIAL_FOR_COMPARABILITY", "high", "UNIVERSAL", "Radical generator defines assay chemistry", "Retain as universal core"),
    "AAPH_concentration_reported": ("ESSENTIAL_FOR_COMPARABILITY", "moderate", "UNIVERSAL", "Radical flux changes kinetics", "Require explicit or exactly traceable protocol"),
    "fluorescein_reported": ("ESSENTIAL_FOR_COMPARABILITY", "high", "UNIVERSAL", "Probe defines ORAC-FL construct", "Retain as universal core"),
    "fluorescein_concentration_reported": ("ESSENTIAL_FOR_COMPARABILITY", "moderate", "UNIVERSAL", "Probe/radical ratio changes decay", "Require explicit or exactly traceable protocol"),
    "Trolox_standard_reported": ("ESSENTIAL_FOR_COMPARABILITY", "high", "UNIVERSAL", "Common calibrant required", "Retain as universal core"),
    "Trolox_range_reported": ("IMPORTANT_BUT_REPORTING_LIMITED", "moderate", "UNIVERSAL", "Calibration range supports linear comparison", "Require range or traceable calibration"),
    "buffer_reported": ("ESSENTIAL_FOR_COMPARABILITY", "moderate", "UNIVERSAL", "Reaction medium affects ionization", "Retain as universal core"),
    "buffer_concentration_reported": ("IMPORTANT_BUT_REPORTING_LIMITED", "moderate", "UNIVERSAL", "Ionic strength may affect kinetics", "Require explicit or traceable concentration"),
    "pH_reported": ("ESSENTIAL_FOR_COMPARABILITY", "high", "UNIVERSAL", "Phenolate state and reactivity are pH-dependent", "Retain as universal core"),
    "temperature_reported": ("ESSENTIAL_FOR_COMPARABILITY", "high", "UNIVERSAL", "AAPH thermolysis is temperature-dependent", "Retain as universal core"),
    "candidate_concentration_reported": ("ESSENTIAL_FOR_COMPARABILITY", "moderate", "UNIVERSAL", "Linearity and saturation require concentration context", "Retain concentration/range as universal core"),
    "solvent_reported": ("ESSENTIAL_FOR_COMPARABILITY", "moderate", "UNIVERSAL", "Solvent affects solubility and kinetics", "Retain as universal core"),
    "final_cosolvent_percent_reported": ("ESSENTIAL_FOR_COMPARABILITY", "low", "UNIVERSAL_WITH_DERIVATION", "Organic fraction can alter radical/probe kinetics", "Accept explicit or unambiguous derivation; retain a derivation flag"),
    "compound_specific_blank_reported": ("CONTEXT_DEPENDENT", "very low", "RISK_TRIGGERED", "Needed when compound signal or quenching overlaps readout", "Enhanced requirement for optical-risk compounds; general blank remains universal"),
    "optical_interference_control_reported": ("CONTEXT_DEPENDENT", "very low", "RISK_TRIGGERED", "Chromophores/fluorophores can bias fluorescence", "Make enhanced optical QC risk-triggered; document risk assessment universally"),
    "aggregation_assessment_reported": ("CONTEXT_DEPENDENT", "very low", "RISK_TRIGGERED", "Aggregation mainly threatens poorly soluble/hydrophobic compounds", "Make direct aggregation QC risk-triggered; retain universal solubility review"),
    "kinetic_AUC_method_reported": ("ESSENTIAL_FOR_COMPARABILITY", "high", "UNIVERSAL", "Endpoint-only data are not equivalent to kinetic ORAC", "Retain as universal core"),
    "replicate_N_reported": ("IMPORTANT_BUT_REPORTING_LIMITED", "moderate", "UNIVERSAL_DOCUMENTATION", "Precision cannot be assessed without replication", "Retain as reporting-quality criterion"),
    "quantitative_value_traceable": ("ESSENTIAL_FOR_COMPARABILITY", "high", "UNIVERSAL", "Ranking requires source-traceable values", "Retain as universal core"),
    "unit_traceable": ("ESSENTIAL_FOR_COMPARABILITY", "high", "UNIVERSAL", "Molar conversion must be reproducible", "Retain as universal core"),
}

summary = []
for c in criteria:
    counts = Counter(r[c] for r in rows)
    sci, freq, scope, effect, role = criterion_meta[c]
    summary.append({
        "criterion": c, "sample_N": len(rows),
        "confirmed_present_N": counts[P], "confirmed_absent_N": counts[E],
        "not_reported_N": counts[N], "previously_not_extracted_N": counts[X],
        "unclear_N": counts[U], "not_applicable_N": counts[NA],
        "scientific_importance": sci, "historical_reporting_frequency": freq,
        "universal_or_risk_triggered": scope,
        "likely_reason_for_missingness": "mixed: historical reporting plus prior consolidation; one inaccessible early full text",
        "effect_on_comparability": effect,
        "recommended_role_in_future_rubric": role,
        "human_review_required": "YES" if scope != "UNIVERSAL" or c in {"compound_purity_reported", "final_cosolvent_percent_reported"} else "NO",
    })

with (DATA / "Stage25B2_TierA_Criterion_Summary.csv").open("w", encoding="utf-8-sig", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(summary[0]))
    w.writeheader(); w.writerows(summary)

print(f"wrote {len(rows)} audit rows and {len(summary)} criterion rows")
