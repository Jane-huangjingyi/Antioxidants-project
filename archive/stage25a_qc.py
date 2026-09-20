from pathlib import Path
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
D=ROOT/'data'
master=pd.read_csv(D/'Stage25A_Unified_Literature_Screening_Master.csv')
frozen=pd.read_csv(D/'Aqueous_Antioxidant_Candidate_Master.csv')
prov=pd.read_csv(D/'Stage25A_Publication_Provenance.csv',low_memory=False)
coverage=pd.read_csv(D/'Stage25A_OpenAlex_Bulk_Coverage_By_Stratum.csv')
cut=pd.read_csv(D/'Stage25A_Shortlist_Cutoff_Sensitivity.csv')

assert len(master)==157 and master.candidate_id.nunique()==157
assert set(master.canonical_name)==set(frozen.compound)
assert master.primary_rank.nunique()==157 and set(master.primary_rank)==set(range(1,158))
assert set(prov.citation_source.dropna().unique())=={'OpenAlex'}
assert set(coverage.threshold_pass)=={'yes'}
assert set(cut.cutoff_N)=={20,30,40,50,60}
assert len(pd.read_csv(D/'Stage25A_Recommended_Stage25B_Shortlist_Top50.csv'))==50
assert not master.columns.duplicated().any()
assert {'missing DOI/PMID','OpenAlex work not found','identifier mismatch'}.issuperset(
    set(pd.read_csv(D/'Stage25A_OpenAlex_Bulk_Unmatched_Publications.csv').failure_category.unique()))

fig=ROOT/'figures'/'aqueous_antioxidant_atlas'/'10_unified_literature_screening'
expected={
 'Stage25A_Research_Evidence_Density_Ranking.png','Stage25A_Publications_vs_Citations.png',
 'Stage25A_Recent_vs_Historical_Evidence.png','Stage25A_Shortlist_Stability.png',
 'Stage25A_Class_Representation.png','Stage25A_Evidence_Domain_Breadth.png'}
assert expected=={p.name for p in fig.glob('*.png')}
for name in expected: assert (fig/name).stat().st_size>50_000

print({'master_rows':len(master),'provenance_rows':len(prov),
       'included_original':int((prov.include_primary_metric=='yes').sum()),
       'all_coverage_strata_pass':True,'recommended_shortlist_N':50,
       'figures':len(expected)})
