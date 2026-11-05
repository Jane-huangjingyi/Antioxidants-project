import fs from 'node:fs/promises';
import path from 'node:path';
import crypto from 'node:crypto';
import {execFileSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
const dir=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const root=path.resolve(dir,'../../..');
const git=(...args)=>execFileSync('git',args,{cwd:root,encoding:'utf8'}).trim();
const target=path.join(dir,'qc/Start_Baseline.json');
try{await fs.access(target);throw new Error('Baseline already exists; refusing to overwrite');}catch(e){if(e.code!=='ENOENT')throw e;}
const sha=async p=>crypto.createHash('sha256').update(await fs.readFile(p)).digest('hex');
const tracked=[];
for(const file of git('ls-files').split(/\r?\n/))tracked.push({path:file,sha256:await sha(path.join(root,file))});
async function list(dir){const result=[];for(const entry of await fs.readdir(dir,{withFileTypes:true})){const p=path.join(dir,entry.name);if(entry.isFile())result.push(p);else if(entry.isDirectory())result.push(...await list(p));}return result;}
const local_source_cache=[];
for(const folder of ['search_logs/raw','gate2_review/sources'])for(const file of (await list(path.resolve(dir,'..',folder))).sort())local_source_cache.push({path:file,sha256:await sha(file)});
const baseline={date:'2026-10-22',timezone:'Asia/Shanghai',start_branch:'codex/phase1c-governance-v0.1',task_branch:git('branch','--show-current'),head:git('rev-parse','HEAD'),main:git('rev-parse','main'),merge_base:git('merge-base','main','HEAD'),initial_worktree_before_task:'CLEAN',capture_status:git('status','--short'),tracked,local_source_cache};
await fs.mkdir(path.dirname(target),{recursive:true});await fs.writeFile(target,JSON.stringify(baseline,null,2)+'\n');
console.log(JSON.stringify({tracked:tracked.length,cache:local_source_cache.length,head:baseline.head,branch:baseline.task_branch}));
