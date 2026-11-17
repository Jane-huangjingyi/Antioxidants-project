"""Validate the public checkpoint independently of the Stage2 completion gate."""
from finalize_public_snapshot import HERE, ROOT, read
import hashlib,json

summary=json.loads((HERE/'stage2_public_summary.json').read_bytes())
articles=read(HERE/'Deduplicated_Article_Register.csv')
links=read(HERE/'Candidate_Article_Links.csv')
keys={r['article_key'] for r in articles}
assert len(keys)==len(articles)==summary['consolidated_identifier_keys']
assert len(links)==summary['candidate_article_links']
assert all(r['article_key'] in keys for r in links)
assert all(r['human_review_status']=='NOT_REVIEWED' and r['change_applied']=='NO' for r in articles+links)
logs=read(HERE/'Database_Search_Log.csv')
assert all(r['cursor_exhausted']=='True' and r['complete']=='True' for r in logs)
assert all(int(r['hit_count'])==int(r['unique_source_records']) for r in logs)
assert all(int(r['downloaded_records'])-int(r['unique_source_records'])==int(r['pagination_duplicate_records']) for r in logs)
for r in read(HERE/'Raw_Export_Manifest.csv'):
    path=ROOT/r['raw_file']
    if path.is_file():assert hashlib.sha256(path.read_bytes()).hexdigest()==r['sha256']
assert not summary['stage2_complete'] and not summary['institutional_complete']
print('Public snapshot QC PASS; Stage2 completion remains pending.')
