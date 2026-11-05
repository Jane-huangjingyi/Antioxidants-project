import fs from 'node:fs/promises';
import path from 'node:path';
import {root,pilot,git,sha} from '../../governance_approval_v0.2/scripts/archive_approval.mjs';
const dir=path.join(pilot,'batch_a_scientific_review');
const target=path.join(dir,'qc/Start_Baseline.json');
try{await fs.access(target);throw Error('Baseline already exists');}catch(e){if(e.code!=='ENOENT')throw e;}
const tracked=[];for(const p of git('ls-files').split(/\r?\n/))tracked.push({path:p,sha256:sha(await fs.readFile(path.join(root,p)))});
const old=JSON.parse(await fs.readFile(path.join(pilot,'governance_approval_v0.2/qc/Start_Baseline.json'),'utf8'));
const caches=[];for(const p of old.local_source_cache)caches.push({path:p.path,sha256:sha(await fs.readFile(p.path))});
await fs.mkdir(path.dirname(target),{recursive:true});
await fs.writeFile(target,JSON.stringify({date:'2026-10-23',source_commit:git('rev-parse','HEAD'),branch:git('branch','--show-current'),main:git('rev-parse','main'),initial_worktree:'CLEAN_BEFORE_NEW_BATCH_DIRECTORY',tracked,local_source_cache:caches},null,2)+'\n');
console.log(JSON.stringify({tracked:tracked.length,caches:caches.length}));
