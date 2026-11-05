import fs from 'node:fs/promises';
import path from 'node:path';
import {root,dir,SOURCE_COMMIT,BRANCH,sha,git} from './track_b_lib.mjs';
const target=path.join(dir,'qc/Start_Baseline.json');
try{await fs.access(target);throw Error('Refusing to overwrite baseline');}catch(e){if(e.code!=='ENOENT')throw e;}
if(git('rev-parse','HEAD')!==SOURCE_COMMIT||git('branch','--show-current')!==BRANCH)throw Error('Unexpected base');
const tracked=[];for(const p of git('ls-files').split(/\r?\n/))tracked.push({path:p,sha256:sha(await fs.readFile(path.join(root,p)))});
const pilot=path.join(root,'workspaces/phase1c_mechanism_evidence_pilot');
const prior=JSON.parse(await fs.readFile(path.join(pilot,'batch_a_targeted_followup/qc/Start_Baseline.json'),'utf8'));
const sources=JSON.parse(await fs.readFile(path.join(pilot,'batch_a_targeted_followup/qc/Followup_Source_Manifest.json'),'utf8'));
const known=new Map(prior.local_source_cache.map(f=>[path.resolve(f.path),f]));
for(const f of sources.sources){const p=f.project_relative_path?path.join(root,f.project_relative_path):path.join(pilot,'batch_a_targeted_followup',f.local_path);known.set(path.resolve(p),{path:p});}
const caches=[];for(const f of known.values())caches.push({path:f.path,sha256:sha(await fs.readFile(f.path))});
await fs.mkdir(path.dirname(target),{recursive:true});await fs.writeFile(target,JSON.stringify({date:'2026-10-26',source_commit:SOURCE_COMMIT,branch:BRANCH,main:git('rev-parse','main'),initial_worktree:'CLEAN_BEFORE_NEW_TRACKB_DIRECTORY',track_a_directory:'READ_ONLY_PREEXISTING_NOT_MERGED_OR_MODIFIED',tracked,local_source_cache:caches},null,2)+'\n');
console.log(JSON.stringify({tracked:tracked.length,protected_local_sources:caches.length}));
