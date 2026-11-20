# Evidence update guide

Copy [the intake header](Evidence_Update_Intake.csv) into a new working area. Register each original observation by stable ID, DOI, first-public date and source locator. Preserve exact candidate ID, material and native food occurrence. Record assay, original value and unit, endpoint direction, protocol, error/replicate scope and all six scientific gates. The six fields take PASS only after identity, food, original experiment, protocol, independence and quality adjudication. The next-version release decision is APPROVED_FOR_NEXT_ANALYSIS. A candidate absent from the identity registry needs prior identity registration and a separate scope decision. Corrections or removals of frozen observations require a new audited version rather than a second row for the same locator.

For model use, approve only harmonized positive molar ORAC-FL as APPROVED_CONNECTED_FL. Record the molar value and reviewed conversion basis and use a block with a documented connection to the existing FL component. The next-version comparator uses the frozen shrinkage method and whole-report holdout, with no automatic choice of a new penalty. Reports from disconnected chemistry remain available for within-source comparisons.

```sh
python 06_manuscript/Results1_v1.0/update_evidence.py --intake <reviewed.csv> --out download_raw/Results1_next_review --cutoff 2026-11-17
```

Use a new output directory. Update the cutoff explicitly for the next search cycle. The script deduplicates observation IDs and the compound/DOI/assay/locator tuple, records holds, reruns within-stratum ranks and the connected diagnostic, and exports candidate positions, report and row additions, matched score coverage, top-set entry/exit and a candidate re-review queue. New DOI counts and independent study adjudication remain separate. The default change trigger is review whenever eligible evidence or ranks change. A/B/C decisions, data removals, new analytical rules and experimental release require human adjudication and a separately published version. The baseline stays read-only.
