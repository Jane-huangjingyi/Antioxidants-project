import fs from 'node:fs/promises';
import path from 'node:path';
import {root,pilot,git,sha} from '../../governance_approval_v0.2/scripts/archive_approval.mjs';
const dir=path.join(pilot,'batch_a_targeted_followup');
const target=path.join(dir,'qc/Start_Baseline.json');
try{await fs.access(target);throw Error('Refusing to overwrite baseline');}catch(e){if(e.code!=='ENOENT')throw e;}
if(git('rev-parse','HEAD')!=='48b34a7314b1d5914c4bb70f770e7e6d2fe939fe')throw Error('Wrong baseline');
const tracked=[];for(const p of git('ls-files').split(/\r?\n/))tracked.push({path:p,sha256:sha(await fs.readFile(path.join(root,p)))});
const old=JSON.parse(await fs.readFile(path.join(pilot,'batch_a_scientific_review/qc/Start_Baseline.json'),'utf8'));
const files=new Map(old.local_source_cache.map(f=>[f.path,f]));
const reviewed=JSON.parse(await fs.readFile(path.join(pilot,'batch_a_scientific_review/qc/Reviewed_Source_Manifest.json'),'utf8'));
for(const f of reviewed.sources){const p=path.join(root,f.path);files.set(p,{path:p});}
const caches=[];for(const f of files.values())caches.push({path:f.path,sha256:sha(await fs.readFile(f.path))});
await fs.mkdir(path.dirname(target),{recursive:true});await fs.writeFile(target,JSON.stringify({date:'2026-10-26',source_commit:git('rev-parse','HEAD'),branch:git('branch','--show-current'),main:git('rev-parse','main'),initial_worktree:'CLEAN_BEFORE_NEW_DIRECTORY',tracked,local_source_cache:caches},null,2)+'\n');
console.log(JSON.stringify({tracked:tracked.length,protected_cache_files:caches.length}));
