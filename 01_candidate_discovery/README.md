# 01. Discover the food-chemical collection

**Question:** where did candidate names come from before any activity ranking?

Run `python 01_candidate_discovery/code/build_universe.py`. The code reads only literal curation declarations from the preserved original generator: class lists, names, food examples and exclusions. It does not execute legacy networking, ranking or file-writing code, and does not read the finished 191-row master as its discovery input. The source hash is written into every reconstructed seed row.

`results/discovery_register.csv` contains the original 191 named seeds, 12 preserved exclusions rescreened under the current scope, and one targeted ergothioneine gap. Glutathione's old endogenous-only exclusion is reopened because a primary food-analysis abstract reports its measurement in prepared foods ([Jones et al., 1992](https://pubmed.ncbi.nlm.nih.gov/1574445/)). The ergothioneine addition follows a primary analysis of common foods ([Ey et al., 2007](https://doi.org/10.1021/jf071328f)). These are scope/coverage corrections, not new ORAC or clinical findings.

The inherited food examples are class-level curation unless a specific source locator is supplied. The workflow does not turn a generic reference to Phenol-Explorer or FooDB into a compound-specific verification. Database design and source-tracing principles are described by [Neveu et al., 2010](https://doi.org/10.1093/database/bap024); that paper is not itself a food-occurrence certificate for every current candidate.

To extend discovery, record the database/export version, query/date, raw record identifier, compound and food identity, exact analytical source, and inclusion/exclusion reason. Review duplicate structures, isomers, mixtures, processing products and endogenous/food overlap before adding names. A source-bounded completeness claim requires those exports and adjudications; current gaps remain visible.

**Manuscript link:** Methods 1 and Table 1 describe the actual enumeration and coverage boundary. Results must distinguish discovery records, candidate profiles and independent studies.
