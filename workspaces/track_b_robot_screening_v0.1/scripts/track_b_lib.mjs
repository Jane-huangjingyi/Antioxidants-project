import fs from 'node:fs/promises';
import path from 'node:path';
import crypto from 'node:crypto';
import {execFileSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import {Workbook} from '@oai/artifact-tool';
export {Workbook};
export const dir=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
export const root=path.resolve(dir,'../..');
export const SOURCE_COMMIT='07e3adb02eac1aeb54dfbb4bf801fed09cae03ad';
export const BRANCH='codex/track-b-robot-screening-feasibility';
export const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
export const git=(...args)=>execFileSync('git',args,{cwd:root,encoding:'utf8'}).trim();
export async function csv(p){const wb=await Workbook.fromCSV((await fs.readFile(path.join(root,p),'utf8')).replace(/^\uFEFF/,''),{sheetName:'Data'});const m=wb.worksheets.getItemAt(0).getUsedRange().values;const h=m[0].map(String);return {headers:h,rows:m.slice(1).filter(r=>r.some(v=>v!==''&&v!==null)).map(r=>Object.fromEntries(h.map((k,i)=>[k,String(r[i]??'')]))),wb};}
export const P={universe:'data/candidate_universe/Antioxidant_Class_Candidate_Master.csv',aqueous:'data/candidate_universe/Aqueous_Antioxidant_Candidate_Master.csv',literature:'data/literature_screening/master/Literature_Screening_Candidate_Master.csv',dictionary:'data/framework/Comprehensive_Antioxidant_Indicator_Dictionary_v0.1.csv',availability:'data/framework/Candidate_157_Data_Availability_Matrix.csv',profile:'data/dual_track_phase1/Candidate_Multidimensional_Evidence_Profile_v0.1.csv',identity:'data/framework/Candidate_Identity_and_Synonym_Audit.csv',frozen:'data/h_orac_stage25b/frozen/Stage25B_Frozen_Primary_HORAC_Top20.csv',qualification:'data/h_orac_stage25b/frozen/Stage25B_Frozen_Top20_B2_Sensitivity_Qualification.csv',freeze_manifest:'data/h_orac_stage25b/frozen/Stage25B5_Frozen_Asset_SHA256_Manifest.csv',eligibility:'data/h_orac_stage25b/stage25b6d/Stage25B6D_Candidate_Eligibility.csv',evidence_profile:'data/h_orac_stage25b/stage25b6d/Stage25B6D_HORAC_Evidence_Profile.csv',source_closure:'data/h_orac_stage25b/stage25b6d/Stage25B6D_Source_Closure.csv',experiments:'data/h_orac_stage25b/stage25b/Stage25B_HORAC_Experiment_Evidence.csv',error_audit:'data/h_orac_stage25b/stage25b6d/Stage25B6D_Error_and_Replicate_Audit.csv',mechanism:'workspaces/phase1c_mechanism_evidence_pilot/compounds/AFF-0061_Protocatechuic_Acid_Mechanism_Evidence.csv'};
