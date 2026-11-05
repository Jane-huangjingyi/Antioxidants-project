"""Phase 1B read-only audit. Standard library only; run with Python -B.
All outputs use exclusive creation. Never modifies any input or Git state.
"""
from pathlib import Path
import csv, io, json, re, math, hashlib, subprocess, os
from collections import Counter, defaultdict
from decimal import Decimal, InvalidOperation
from datetime import date, datetime, timezone

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'workspaces/phase1b_t002_readonly_audit'
PREFIX = OUT.relative_to(ROOT).as_posix() + '/'
BASE = '46a02f850ca29fefebe47081f0221475f8d2a9eb'
PATHS = {
 'T002':'data/candidate_universe/Antioxidant_Class_Candidate_Master.csv',
 'T004':'data/candidate_universe/Aqueous_Antioxidant_Candidate_Master.csv',
 'T110':'data/literature_screening/master/Literature_Screening_Candidate_Master.csv',
 'IDENTITY':'data/framework/Candidate_Identity_and_Synonym_Audit.csv',
 'DICTIONARY':'workspaces/current_deliverables_phase1/dictionaries/Database_Field_Dictionary_v0.1.csv',
 'INVENTORY':'workspaces/current_deliverables_phase1/provenance/Table_Inventory_v0.1.csv',
 'STATUS':'workspaces/current_deliverables_phase1/provenance/Scientific_Scope_and_Status_Map_v0.1.csv',
 'CODES':'workspaces/current_deliverables_phase1/dictionaries/Abbreviations_and_Codes_v0.1.csv'}
CORE = 'candidate_id canonical_name PubChem_CID InChIKey molecular_formula molecular_weight parent_class analysis_panel subclass parent_or_conjugate glycoside_or_aglycone stereochemistry isomer_status dietary_parent_or_metabolite representative_food_sources food_occurrence_reference food_occurrence_confidence normal_dietary_exposure_yes_no candidate_eligible eligibility_rationale exclusion_reason likely_primary_ranking_construct major_known_assay_risk current_review_status reviewer key_identity_reference'.split()
EXT = 'compound synonym structural_family supplement_dominant_yes_no medicinal_plant_dominant_yes_no likely_secondary_construct notes'.split()
TECH = ['review_date','legacy_note']
PRIORITY = 'candidate_eligible normal_dietary_exposure_yes_no supplement_dominant_yes_no medicinal_plant_dominant_yes_no food_occurrence_confidence parent_class analysis_panel subclass parent_or_conjugate glycoside_or_aglycone stereochemistry isomer_status dietary_parent_or_metabolite likely_primary_ranking_construct current_review_status'.split()
def j(v): return json.dumps(v,ensure_ascii=False,sort_keys=True)
def git(*args): return subprocess.check_output(['git','--no-optional-locks',*args],cwd=ROOT).decode('utf-8').strip()
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for block in iter(lambda:f.read(1024*1024),b''): h.update(block)
 return h.hexdigest()
def snapshot():
 result={}
 for folder,dirs,files in os.walk(ROOT):
  dirs[:]=[x for x in dirs if x!='.git' and (Path(folder)/x).resolve()!=OUT]
  for name in files:
   p=Path(folder)/name
   rel=p.relative_to(ROOT).as_posix()
   if not rel.startswith(PREFIX): result[rel]={'sha256':sha(p),'bytes':p.stat().st_size}
 return result
def writecsv(name,rows,fields=None):
 p=OUT/name; p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('x',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields or list(rows[0])); w.writeheader(); w.writerows(rows)
def writetext(name,value):
 p=OUT/name; p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('x',encoding='utf-8',newline='') as f: f.write(value)
def load(code):
 p=ROOT/PATHS[code]; raw=p.read_bytes(); text=raw.decode('utf-8-sig',errors='strict')
 reader=csv.reader(io.StringIO(text,newline=''),strict=True); header=next(reader); rows=[]; previous=reader.line_num
 for n,values in enumerate(reader,1):
  assert len(values)==len(header),(code,n,len(values),len(header))
  r=dict(zip(header,values)); r['_record']=n; r['_lines']=f'{previous+1}-{reader.line_num}'; rows.append(r); previous=reader.line_num
 assert len(header)==len(set(header)) and all(header),(code,'invalid headers')
 return header,rows,{'path':PATHS[code],'rows':len(rows),'columns':len(header),'header_order':header,'utf8_strict':'PASS','replacement_character_cells':sum('\ufffd' in v for r in rows for k,v in r.items() if not k.startswith('_')),'sha256':hashlib.sha256(raw).hexdigest(),'bom':raw.startswith(b'\xef\xbb\xbf')}
def raw(r): return {k:v for k,v in r.items() if not k.startswith('_')}
def cid(v):
 if not v.strip(): return ''
 try:
  d=Decimal(v)
  return str(int(d)) if d.is_finite() and d>0 and d==d.to_integral_value() else 'INVALID:'+v
 except InvalidOperation: return 'INVALID:'+v
def marker(v):
 if v=='': return 'TRUE_BLANK'
 if not v.strip(): return 'WHITESPACE_ONLY'
 z=v.strip().lower().replace('_',' ')
 if z in ['unknown','unresolved','not applicable','not reported','not searched','source inaccessible']: return 'TEXT_'+z.upper().replace(' ','_')
 if 'unresolved' in z: return 'COMPOUND_UNRESOLVED_TEXT'
 return 'POPULATED_OTHER'

assert git('rev-parse','HEAD')==BASE
existing=[p.relative_to(OUT).as_posix() for p in OUT.rglob('*') if p.is_file() and p.name!='audit_t002.py']
assert not existing,('STOP: preexisting output',existing)
started=datetime.now(timezone.utc).isoformat()
start_status=git('status','--porcelain=v1','--untracked-files=all')
assert all(PREFIX in line.replace('\\','/') for line in start_status.splitlines()),start_status
before=snapshot()
tables={}; metadata={}; headers={}
for code in PATHS: headers[code],tables[code],metadata[code]=load(code)
a=tables['T002']; b=tables['T110']; c=tables['T004']; ident=tables['IDENTITY']; header=headers['T002']
assert len(a)==191 and len(header)==35 and set(header)==set(CORE+EXT+TECH)
assert len(CORE)==26 and len(EXT)==7 and len(TECH)==2
assert len({x['candidate_id'] for x in a})==191
byid={x['candidate_id']:x for x in a}; bid={x['candidate_id']:x for x in b}
assert len(bid)==len(b)
findings=[]; risks=[]
def issue(i,priority,kind,title,scope,fields,advice,table='T002'):
 rows=list(scope)
 risks.append(dict(issue_id=i,priority=priority,issue_class=kind,title_cn=title,source_table=table,source_path=PATHS[table],affected_record_count=len(rows),count_unit='unique issue_id; affected rows overlap across issues',fields=j(fields),candidate_ids=j([r.get('candidate_id','') for r in rows]),locators=j([{'record':r['_record'],'physical_lines':r['_lines']} for r in rows]),review_direction_cn=advice,decision='HUMAN_REVIEW_REQUIRED'))
 for r in rows:
  for field in fields:
   findings.append(dict(issue_id=i,priority=priority,issue_class=kind,source_path=PATHS[table],data_record=r['_record'],physical_lines=r['_lines'],candidate_id=r.get('candidate_id',''),field_name=field,original_value=r.get(field,''),review_direction_cn=advice))
missing=[r for r in a if any(not r[f] for f in ['PubChem_CID','InChIKey','molecular_formula','molecular_weight'])]
issue('I01','P0','DATA_CONFIRMED_ISSUE','两条记录缺少四项结构属性',missing,['canonical_name','PubChem_CID','InChIKey','molecular_formula','molecular_weight','key_identity_reference'],'先核查原始身份与具体形式；保留空值，不按名称自动补齐。')
unrechecked=[r for r in ident if r['identity_status']=='IDENTIFIER_PRESENT_NOT_STRUCTURALLY_RECHECKED']
issue('I02','P0','DEFINITION_REVIEW_REQUIRED','身份已解决文字与未完成结构复核不是同一审核层级',[r for r in a if r['candidate_id'] in {x['candidate_id'] for x in unrechecked} and r['current_review_status'].startswith('identity resolved')],['current_review_status','reviewer'],'对照身份审核表区分标识存在、结构核实和独立人工复核；不得据文字自动确认化学身份。')
issue('I03','P1','DATA_CONFIRMED_ISSUE','食物来源参考均为通用数据库/资料类别而非候选物级引文',a,['food_occurrence_reference'],'补证需另行授权：保留候选物、食品、具体来源、定位及证据状态；本轮未外部检索，不判定食物存在性为假。')
third=[r for r in a if any(r[f] not in ['yes','no'] for f in ['normal_dietary_exposure_yes_no','supplement_dominant_yes_no','medicinal_plant_dominant_yes_no','candidate_eligible'])]
issue('I04','P1','DEFINITION_REVIEW_REQUIRED','yes/no相关字段存在unresolved第三状态',third,['normal_dietary_exposure_yes_no','supplement_dominant_yes_no','medicinal_plant_dominant_yes_no','candidate_eligible'],'逐字段定义状态空间及缺失规则；不得将unresolved转换成no或空白。')
issue('I05','P1','DEFINITION_REVIEW_REQUIRED','身份、来源和候选纳入混合在同一审核字段',a,['current_review_status','reviewer'],'先定义审核事件、对象、范围与责任；4条researcher inclusion决定不等于全部结构审核。')
issue('I06','P1','POTENTIAL_SCIENTIFIC_RISK','分子式分子量必须绑定具体立体/盐/糖苷/氧化还原形式',a,['canonical_name','molecular_formula','molecular_weight','stereochemistry'],'正数和语法通过不证明化学正确；核对具体形式和原始结构来源。不得用相同分子式或InChIKey前14位合并。')
issue('I07','P1','DEFINITION_REVIEW_REQUIRED','化学分类、结构族与分析面板边界需要定义',a,['parent_class','analysis_panel','subclass','structural_family','parent_or_conjugate','glycoside_or_aglycone'],'保留现有分类；defined conjugate及pigment是复合表达，需人工界定与糖苷/苷元轴关系。面板不是效力等级。')
issue('I08','P1','POTENTIAL_SCIENTIFIC_RISK','存在性、膳食暴露及摄入剂量不能互相替代',a,['representative_food_sources','food_occurrence_confidence','normal_dietary_exposure_yes_no'],'本表不含候选物级浓度、摄入量或剂量达成证据；不可从yes推导实际摄入充分或临床功效。')
issue('I09','P1','POTENTIAL_SCIENTIFIC_RISK','候选资格与预期构念不可作为实验/VSIR/排名结果',a,['candidate_eligible','eligibility_rationale','likely_primary_ranking_construct','likely_secondary_construct'],'candidate_eligible=yes仅为候选层；likely为拟用构念，不代表已实验。H-ORAC历史资格不等于VSIR GO。')
minerals=[r for r in a if 'mineral cofactors' in r['parent_class']]
issue('I10','P1','POTENTIAL_SCIENTIFIC_RISK','7条矿物辅因子记录不得混入小分子直接容量比较',minerals,['canonical_name','molecular_formula','likely_primary_ranking_construct','isomer_status'],'源表已写no capacity rank；保留此边界。元素记录不定义膳食中全部化学物种，通用isomer_status模板需复核适用性。')
drows=[r for r in tables['DICTIONARY'] if r['table_id']=='T002']
assert len(drows)==35 and {r['field_name'] for r in drows}==set(header)
dmap={r['field_name']:r for r in drows}
issue('I11','P1','DEFINITION_REVIEW_REQUIRED','字段字典覆盖完整但科学定义与规则尚未批准',drows,['field_name','definition_cn','definition_en','data_type','allowed_values','definition_status'],'逐字段修订定义、适用边界、类型与状态规则，另行人工批准；CURATED_PROJECT_DEFINITION不等于HUMAN_APPROVED。','DICTIONARY')
issue('I12','P2','DEFINITION_REVIEW_REQUIRED','synonym和exclusion_reason整列为空，需要区分未维护与不适用',a,['synonym','exclusion_reason'],'不直接判为数据错误；建立条件必填与缺失原因规则。synonym空白不等于没有同义词。')

structure=[]; domains=[]; validation=[]
categorical=set(PRIORITY+['structural_family','likely_secondary_construct'])
for pos,f in enumerate(header,1):
 values=[r[f] for r in a]; counts=Counter(values); kinds=Counter(marker(v) for v in values)
 dtype='ENUM_LIKE_UNAPPROVED' if f in categorical else 'FREE_TEXT_OR_UNSPECIFIED'
 if f in ['current_review_status','stereochemistry','isomer_status','likely_primary_ranking_construct','dietary_parent_or_metabolite']: dtype='COMPOUND_STATUS_OR_INSTRUCTION'
 if f in ['candidate_id','PubChem_CID','InChIKey']: dtype='IDENTIFIER'
 for v,n in counts.items():
  affected=[r for r in a if r[f]==v]
  domains.append(dict(source_path=PATHS['T002'],field_name=f,priority_field='YES' if f in PRIORITY else 'NO',observed_value=v,value_marker=marker(v),frequency=n,proportion=n/len(a),domain_interpretation=dtype,approved_enum='NO',semantic_status='DEFINITION_REVIEW_REQUIRED' if f in categorical else 'OBSERVED_ONLY',candidate_ids=j([r['candidate_id'] for r in affected]),record_locators=j([{'record':r['_record'],'physical_lines':r['_lines']} for r in affected])))
 structure.append(dict(source_path=PATHS['T002'],field_position=pos,field_name=f,field_stratum='CORE' if f in CORE else 'EXTENDED' if f in EXT else 'TECHNICAL_HISTORY',records=len(a),true_blank_count=counts.get('',0),true_blank_proportion=counts.get('',0)/len(a),whitespace_only_count=kinds['WHITESPACE_ONLY'],nonblank_unique_count=len([v for v in counts if v!='']),marker_counts=j(dict(kinds)),observed_type=dtype,dictionary_records=sum(r['field_name']==f for r in drows),coverage='REVIEWED',source_values_changed='NO'))
for r in a:
 checks={'candidate_id':bool(re.fullmatch(r'AFF-\d{4}',r['candidate_id'])),'PubChem_CID':not cid(r['PubChem_CID']).startswith('INVALID:'),'InChIKey':not r['InChIKey'] or bool(re.fullmatch('[A-Z]{14}-[A-Z]{10}-[A-Z]',r['InChIKey'])),'molecular_formula':not r['molecular_formula'] or bool(re.fullmatch(r'(?:[A-Z][a-z]?\d*)+(?:[+-]\d*|\d*[+-])?',r['molecular_formula']))}
 try: checks['molecular_weight']=not r['molecular_weight'] or (math.isfinite(float(r['molecular_weight'])) and float(r['molecular_weight'])>0)
 except ValueError: checks['molecular_weight']=False
 try: checks['review_date']=bool(re.fullmatch(r'\d{4}-\d{2}-\d{2}',r['review_date'])) and date.fromisoformat(r['review_date'])<=date(2026,10,16)
 except ValueError: checks['review_date']=False
 for f,ok in checks.items(): validation.append(dict(source_path=PATHS['T002'],candidate_id=r['candidate_id'],data_record=r['_record'],physical_lines=r['_lines'],field_name=f,original_value=r[f],validation_result='PASS_SYNTAX_ONLY' if ok else 'ISSUE',blank_flag='YES' if not r[f] else 'NO',interpretation_cn='语法/正数/日期诊断，不确认化学真实性；空结构值另见I01。'))
assert all(x['validation_result']=='PASS_SYNTAX_ONLY' for x in validation)
mw=sorted(float(r['molecular_weight']) for r in a if r['molecular_weight'])
q1=mw[len(mw)//4];q3=mw[3*len(mw)//4];lo=q1-1.5*(q3-q1);hi=q3+1.5*(q3-q1)
outliers=[r for r in a if r['molecular_weight'] and not lo<=float(r['molecular_weight'])<=hi]
if outliers: issue('I13','P2','POTENTIAL_SCIENTIFIC_RISK','分子量分布离群仅为复核信号',outliers,['molecular_weight','canonical_name'],'采用排序样本floor(n/4)、floor(3n/4)分位及1.5 IQR标记；跨类别数据不能据此判错或删除。')

matches=[]
def matchrow(kind,left,rightpath='',right=None,**extras):
 row=dict(record_type=kind,left_source_path=PATHS['T002'],left_record=left['_record'] if left else '',left_physical_lines=left['_lines'] if left else '',candidate_id=left.get('candidate_id','') if left else '',left_original_identity=j({f:left.get(f,'') for f in ['compound','canonical_name','PubChem_CID','InChIKey']} ) if left else '',right_source_path=rightpath,right_record=right['_record'] if right else '',right_physical_lines=right['_lines'] if right else '',right_original_record=j(raw(right)) if right else '',diagnostics=j(extras),mapping_status=extras.get('mapping_status','NOT_A_CROSSWALK'),human_approval='NOT_PERFORMED')
 matches.append(row)
name_diffs=[];cid_diffs=[];key_diffs=[];realconflicts=[]
for r in a:
 s=bid.get(r['candidate_id'])
 if not s: matchrow('T110_ID_ABSENT_SCOPE_ONLY',r,PATHS['T110']);continue
 names=r['canonical_name']!=s['canonical_name']; cs=r['PubChem_CID']!=s['PubChem_CID']; ks=r['InChIKey']!=s['InChIKey']
 if names:name_diffs.append(r)
 if cs:cid_diffs.append(r)
 if ks:key_diffs.append(r)
 conflict=bool((cid(r['PubChem_CID']) and cid(s['PubChem_CID']) and cid(r['PubChem_CID'])!=cid(s['PubChem_CID'])) or (r['InChIKey'] and s['InChIKey'] and ks))
 if conflict:realconflicts.append(r)
 matchrow('T110_ID_JOIN',r,PATHS['T110'],s,name_raw_equal=not names,name_casefold_equal=r['canonical_name'].casefold()==s['canonical_name'].casefold(),cid_raw_equal=not cs,cid_left_diagnostic=cid(r['PubChem_CID']),cid_right_diagnostic=cid(s['PubChem_CID']),cid_diagnostic_equal=cid(r['PubChem_CID'])==cid(s['PubChem_CID']),full_key_raw_equal=not ks,nonblank_structure_available=bool(r['PubChem_CID'] and r['InChIKey']),interpretation='SUBSTANTIVE_IDENTIFIER_CONFLICT_REQUIRES_REVIEW' if conflict else 'NAME_DIFFERENCE_STRUCTURE_LABELS_AGREE_NOT_HUMAN_VERIFIED' if names else 'IDENTIFIERS_PRESENT_NOT_HUMAN_VERIFIED' if r['InChIKey'] else 'IDENTITY_UNRESOLVED')
for s in b:
 if s['candidate_id'] not in byid: matchrow('T110_ORPHAN_ID',None,PATHS['T110'],s)
if name_diffs: issue('I14','P1','DEFINITION_REVIEW_REQUIRED','同ID名称不一致但不能仅据名称判化学实体冲突',name_diffs,['canonical_name','compound','PubChem_CID','InChIKey'],'对照T110原值及完整结构标识；大小写、同义名、立体及盐型限定词分别审核，不自动改名。')
if realconflicts: issue('I15','P0','DATA_CONFIRMED_ISSUE','同ID结构标识实质冲突',realconflicts,['PubChem_CID','InChIKey'],'先人工查证，不合并。')
for r in cid_diffs:
 s=bid[r['candidate_id']]
 findings.append(dict(issue_id='FORMAT_ONLY_CID',priority='INFO',issue_class='FORMAT_DIFFERENCE_NOT_ENTITY_CONFLICT',source_path=PATHS['T002'],data_record=r['_record'],physical_lines=r['_lines'],candidate_id=r['candidate_id'],field_name='PubChem_CID',original_value=r['PubChem_CID'],review_direction_cn='T110原值='+s['PubChem_CID']+'；诊断整数比较='+str(cid(r['PubChem_CID'])==cid(s['PubChem_CID']))+'；未规范化写回。'))

reverse=Counter(); proposalstats=Counter(); mapping_details=[]
for s in c:
 channels={'CID':[r['candidate_id'] for r in a if cid(s['PubChem_CID']) and cid(s['PubChem_CID'])==cid(r['PubChem_CID'])], 'FULL_INCHIKEY':[r['candidate_id'] for r in a if s['InChIKey'] and s['InChIKey']==r['InChIKey']], 'CANONICAL_NAME_EXACT':[r['candidate_id'] for r in a if s['canonical_name'] and s['canonical_name']==r['canonical_name']], 'CANONICAL_NAME_CASEFOLD':[r['candidate_id'] for r in a if s['canonical_name'] and s['canonical_name'].casefold()==r['canonical_name'].casefold()], 'SOURCE_COMPOUND_EXACT':[r['candidate_id'] for r in a if s['compound'] and s['compound']==r['compound']]}
 candidates=sorted(set(v for ids in channels.values() for v in ids)); reverse.update(candidates)
 strong=set(channels['CID']) & set(channels['FULL_INCHIKEY'])
 status='MATCH_PROVISIONAL' if len(candidates)==1 and len(strong)==1 else 'UNRESOLVED_IDENTITY_REVIEW' if len(candidates)==1 else 'AMBIGUOUS_MATCH_REVIEW' if candidates else 'NO_MATCH_REVIEW'
 proposalstats[status]+=1
 matchrow('T004_CANDIDATE_SUGGESTION',byid[candidates[0]] if len(candidates)==1 else None,PATHS['T004'],s,candidate_suggestions=candidates,independent_channels=channels,candidate_count=len(candidates),mapping_status=status,form_rule='完整InChIKey与CID仅标识比对；不凭名称/前14位/分子式合并盐型、立体、糖苷或氧化还原形式。')
 mapping_details.append({'record':s['_record'],'status':status,'channels':channels,'candidates':candidates})
for s in ident:
 r=byid.get(s['candidate_id']); t=bid.get(s['candidate_id'])
 matchrow('EXISTING_IDENTITY_AUDIT',r,PATHS['IDENTITY'],s,in_T002=r is not None,in_T110=t is not None,cid_vs_T002_diagnostic_equal=bool(r and cid(r['PubChem_CID'])==cid(s['PubChem_CID_as_recorded'])),key_vs_T002_equal=bool(r and r['InChIKey']==s['InChIKey']),name_vs_T002_equal=bool(r and r['canonical_name']==s['canonical_name_en']),cid_vs_T110_diagnostic_equal=bool(t and cid(t['PubChem_CID'])==cid(s['PubChem_CID_as_recorded'])),key_vs_T110_equal=bool(t and t['InChIKey']==s['InChIKey']),name_vs_T110_equal=bool(t and t['canonical_name']==s['canonical_name_en']),identity_status=s['identity_status'],interpretation='现有标识存在不是结构核实；中文名NOT_CURATED及同义词记录不可作为合并批准。')
for f in ['PubChem_CID','InChIKey']:
 groups=defaultdict(list)
 for r in a:
  if r[f]:groups[cid(r[f]) if f=='PubChem_CID' else r[f]].append(r)
 for val,rs in groups.items():
  if len(rs)>1:
   for r in rs:matchrow('T002_NONBLANK_DUPLICATE_IDENTIFIER_REVIEW',r,field=f,value=val,group_ids=[x['candidate_id'] for x in rs])
firstblock=defaultdict(list)
for r in a:
 if r['InChIKey']:firstblock[r['InChIKey'].split('-')[0]].append(r)
related=[rs for rs in firstblock.values() if len(rs)>1]
for rs in related:
 for r in rs:matchrow('T002_SHARED_CONNECTIVITY_BLOCK_DO_NOT_MERGE',r,group_ids=[x['candidate_id'] for x in rs],full_keys=[x['InChIKey'] for x in rs],interpretation='仅前14位相同；保留完整键差异；本轮不判断具体立体关系。')

suggestions={
'candidate_id':'定义项目稳定主键、AFF格式、唯一性、不可复用及受控跨表引用。',
'compound':'定义T002来源名称；T004特有映射陈述不能直接证明T002语义。',
'canonical_name':'定义表内首选显示名、命名来源与形式限定词；不作为独立合并键。',
'synonym':'定义同义词来源、分隔方式、审核范围及整列空白含义。',
'PubChem_CID':'明确PubChem Compound标识、正整数文本及具体形式；.0仅受控诊断。',
'InChIKey':'明确完整键、格式、结构层级、盐/电荷/立体限制和缺失处理。',
'molecular_formula':'绑定指定化学形式、元素计数、电荷/盐/水合物表达及来源版本。',
'molecular_weight':'定义平均分子量/摩尔质量、单位、精度与具体形式；与单同位素质量区分。',
'parent_class':'定义分类层级、来源、互斥性及混合化学/营养学分类的适用范围。',
'analysis_panel':'定义项目分析分组及与parent_class关系；不表示实验完成或效力。',
'subclass':'定义相对parent_class的下位分类及映射验证规则。',
'structural_family':'说明与subclass的独立信息及是否允许冗余，不自动删除字段。',
'parent_or_conjugate':'明确parent、derivative、conjugate的判据及复合值处理。',
'glycoside_or_aglycone':'界定glycoside/aglycone与conjugate/pigment等跨轴值。',
'stereochemistry':'区分实测/数据库指定构型、未指定状态和see PubChem待核查指令。',
'isomer_status':'定义异构体分辨审核状态；通用未来核实指令不是完成状态。',
'dietary_parent_or_metabolite':'分开膳食母体、代谢物、加工生成和内源来源的概念范围。',
'representative_food_sources':'定义食品名、部位、加工状态、来源与代表性，不替代含量证据。',
'food_occurrence_reference':'要求候选物级可定位引文/数据库记录；不把通用库名当已验证引文。',
'food_occurrence_confidence':'定义moderate、low/unresolved、unresolved判据及证据审核人。',
'normal_dietary_exposure_yes_no':'定义正常膳食、人群、时间和暴露证据；容纳unresolved，不推导摄入量。',
'supplement_dominant_yes_no':'界定dominant的比较基准、人群与来源证据，明确第三状态。',
'medicinal_plant_dominant_yes_no':'界定药用主导、食药边界、地域与证据规则，明确第三状态。',
'candidate_eligible':'仅候选来源纳入门槛；不等于H-ORAC/VSIR/临床资格，定义unresolved。',
'eligibility_rationale':'记录候选纳入理由、证据与决定范围，不替代下游实验判断。',
'exclusion_reason':'区分不适用、尚未判定与已排除原因，定义条件必填。',
'likely_primary_ranking_construct':'定义建议的首要比较构念及适用范围；不是已测实验或排名资格。',
'likely_secondary_construct':'定义建议次级构念及多值结构；不表明已有证据。',
'major_known_assay_risk':'区分类别通用风险与候选/协议级已确认干扰；要求证据定位。',
'current_review_status':'拆解身份、食物来源、候选资格等审核维度的语义，不直接改表。',
'review_date':'定义审核事件、ISO日期、时区/版本关系；日期不能证明人工批准。',
'reviewer':'区分初筛者、写回者、独立审核者和研究者具体决定范围。',
'key_identity_reference':'定义候选物级结构来源链接、形式、访问版本与无法检索状态。',
'legacy_note':'定义历史索引/版本指针，不恢复历史排名到本表。',
'notes':'仅非结构化补充，不作为唯一批准证据，定义空白和敏感内容规则。'}
dictreview=[]
for f in header:
 r=dmap[f]; generic=r['definition_en'].startswith('Source column '); legacy='Legacy definition requires' in r['definition_en']; scopeok=not generic and not legacy
 dictreview.append(dict(source_path=PATHS['DICTIONARY'],dictionary_data_record=r['_record'],dictionary_physical_lines=r['_lines'],table_id='T002',field_name=f,stratum='CORE' if f in CORE else 'EXTENDED' if f in EXT else 'TECHNICAL_HISTORY',entry_count=1,english_header_match='YES',original_label_cn=r['label_cn'],original_definition_cn=r['definition_cn'],original_definition_en=r['definition_en'],original_data_type=r['data_type'],original_allowed_values=r['allowed_values'],original_missing_rule=r['missing_value_rule'],original_unit=r['unit'],original_scientific_scope=r['scientific_scope'],original_definition_status=r['definition_status'],original_definition_source=r['definition_source'],original_release_status=r['release_status'],chinese_text_present='YES' if r['definition_cn'] else 'NO',chinese_definition_complete='NO_PLACEHOLDER' if generic or legacy else 'PARTIAL_REVIEW_REQUIRED',english_accuracy='UNVALIDATED_PLACEHOLDER' if generic or legacy else 'T002_SCOPE_REVIEW_REQUIRED' if f=='compound' else 'DIRECTIONALLY_CONSISTENT_NOT_APPROVED',circular_or_label_only='PLACEHOLDER_OR_LABEL_PLUS_CAVEAT' if generic or legacy else 'NO_OBVIOUS_CIRCULARITY',scientific_boundary='SUBSTANTIVE_PARTIAL' if scopeok else 'MISSING_TABLE_SPECIFIC_DEFINITION',datatype_quality='SPECIFIC_SYNTAX_UNIT_REVIEW_REQUIRED' if r['data_type']!='string_or_source_mixed' else 'GENERIC_SOURCE_MIXED_NOT_OPERATIONAL',approved_value_rule='NOT_ESTABLISHED',human_approval_attribute='MISSING_ATTRIBUTE',field_stratum_attribute='MISSING_ATTRIBUTE',confirmed_claim_check='CURATED_IS_NOT_HUMAN_APPROVED' if r['definition_status']=='CURATED_PROJECT_DEFINITION' else 'EXPLICIT_NEEDS_REVIEW',suggestion_cn=suggestions[f],review_coverage='COMPLETE',definition_decision='DEFINITION_REVIEW_REQUIRED',changes_applied='NO'))

counts={'T002_rows':len(a),'T002_fields':len(header),'strata':[26,7,2],'T110_ID_matches':len(set(byid)&set(bid)),'T002_only_ids':sorted(set(byid)-set(bid)),'T110_only_ids':sorted(set(bid)-set(byid)),'T110_name_raw_differences':len(name_diffs),'T110_name_case_only':sum(r['canonical_name'].casefold()==bid[r['candidate_id']]['canonical_name'].casefold() for r in name_diffs),'T110_CID_raw_differences':len(cid_diffs),'T110_CID_normalized_conflicts':sum(cid(r['PubChem_CID'])!=cid(bid[r['candidate_id']]['PubChem_CID']) for r in cid_diffs),'T110_full_key_differences':len(key_diffs),'substantive_identifier_conflicts':len(realconflicts),'identity_missing_ids':[r['candidate_id'] for r in missing],'existing_identity_statuses':dict(Counter(r['identity_status'] for r in ident)),'T004_suggestion_statuses':dict(proposalstats),'T004_no_candidate_count':sum(not x['candidates'] for x in mapping_details),'T004_one_to_many_rows':sum(len(x['candidates'])>1 for x in mapping_details),'T004_many_to_one_candidate_ids':[k for k,v in reverse.items() if v>1],'T002_not_suggested_from_T004':sorted(set(byid)-set(reverse)),'dictionary_statuses':dict(Counter(r['definition_status'] for r in drows)),'dictionary_placeholder_count':sum(r['definition_en'].startswith('Source column ') or 'Legacy definition requires' in r['definition_en'] for r in drows),'shared_connectivity_groups':len(related),'numeric_range':[min(mw),max(mw)],'numeric_IQR_bounds':[lo,hi],'numeric_outliers':len(outliers),'priority_counts':dict(Counter(r['priority'] for r in risks)),'issue_class_counts':dict(Counter(r['issue_class'] for r in risks)),'risk_unique_issues':len(risks),'domain_rows':len(domains),'findings_cells':len(findings)}
assert len(risks)==len({r['issue_id'] for r in risks})
assert all(sum(x['frequency'] for x in domains if x['field_name']==f)==191 for f in header)
assert all(x['mapping_status'] not in ['MATCH_CONFIRMED','HUMAN_APPROVED'] for x in matches)
assert len(dictreview)==35
after=snapshot(); changed=sorted(k for k in set(before)|set(after) if before.get(k)!=after.get(k))
assert not changed,changed
endhead=git('rev-parse','HEAD'); assert endhead==BASE
integrity={'task':'Phase1B_T002_Field_and_Data_ReadOnly_Audit_v0.1','started_utc':started,'verified_utc':datetime.now(timezone.utc).isoformat(),'start_HEAD':BASE,'end_HEAD':endhead,'first_read_git_status':'CLEAN (recorded before creation of audit script)','execution_start_status':start_status,'existing_file_sha256_count':len(before),'non_audit_changed_paths':changed,'scope':'All existing files outside .git and the authorized audit output directory; SHA256 content+size','before':before,'after':after,'Original Data Modified':'NO','Frozen Assets Modified':'NO','Git mutation':'NONE'}
writecsv('T002_Structure_and_Missingness_Audit_v0.1.csv',structure)
writecsv('T002_Observed_Value_Domain_Audit_v0.1.csv',domains)
writecsv('T002_Identity_and_CrossTable_Match_Audit_v0.1.csv',matches)
writecsv('T002_Field_Dictionary_Review_v0.1.csv',dictreview)
writecsv('T002_Scientific_Risk_Register_v0.1.csv',risks)
writecsv('supporting/Cell_Level_Findings_v0.1.csv',findings)
writecsv('supporting/Syntax_and_Numeric_Validation_v0.1.csv',validation)
writetext('supporting/Input_Parsing_and_QC_v0.1.json',j({'tables':metadata,'counts':counts,'T004_independent_channels':mapping_details}))
writetext('supporting/Integrity_Before_After_v0.1.json',j(integrity))

status='''T002 Structural Audit: ISSUES_FOUND
T002 Identity Audit: ISSUES_FOUND
Cross-table Mapping Readiness: HOLD
Field Dictionary Review: COMPLETE
Original Data Modified: NO
Frozen Assets Modified: NO
Release Readiness: HOLD
Phase 2 Reorganization: HOLD'''
pc=counts['priority_counts']
tablelines='\n'.join(f"- {k}: `{v['path']}`，{v['rows']}条、{v['columns']}字段。" for k,v in metadata.items())
summary=f'''本轮完整读取T002的191条记录、35个字段，保持26个核心、7个扩展、2个技术/历史字段。candidate_id无空白、无重复、格式有效，可唯一定位记录；191条候选记录不等于191种身份去重的独立化合物。UTF-8严格解析、表头唯一性、各行宽度、CID/InChIKey/分子式语法、非空分子量正数及日期诊断通过；分子式仅做词法检查，不做元素/结构计量科学确认。存在身份缺失及定义问题，故总体不是无问题PASS。

AFF-0082（Feruloylquinic acid）和AFF-0150（Probetanin）的CID、InChIKey、分子式及分子量均为空，每字段缺失2/191（1.0471%）；保留未解决身份，不自动补齐。synonym与exclusion_reason各191条真空白，notes有185条真空白；这不自动构成错误。空白、独立unresolved、复合unresolved、not applicable等已分开统计；全部35字段的完整原值域和频数均输出，无截断。

T002与T110按ID匹配{counts['T110_ID_matches']}条，T002独有{len(counts['T002_only_ids'])}条，T110孤儿{len(counts['T110_only_ids'])}条。名称原值差异{len(name_diffs)}条，其中仅大小写差异{counts['T110_name_case_only']}条；CID原值差异{len(cid_diffs)}条，诊断整数化后实质CID冲突{counts['T110_CID_normalized_conflicts']}条；完整InChIKey差异{len(key_diffs)}条。未观察到不同非空CID/完整键的实质冲突，但同义名、立体限定词、阳离子/盐型及形式解释仍待审核，不能从标识相同宣布结构已人工确认。T110缺席仅为表间覆盖差异，不自动判数据缺漏。

T004的157条记录只有候选建议：{j(dict(proposalstats))}；一对多{counts['T004_one_to_many_rows']}条，多对一候选{len(counts['T004_many_to_one_candidate_ids'])}个，无任何候选{counts['T004_no_candidate_count']}条。CID、完整键、规范名及来源compound各独立比较，非空两结构锚同时支持且唯一者才标MATCH_PROVISIONAL；2条缺少结构锚的名称候选保留UNRESOLVED_IDENTITY_REVIEW。没有生成获批crosswalk或回填T004。现有身份表状态：{j(counts['existing_identity_statuses'])}；标识存在未结构复核与identity resolved不是同一层审核。完整键前14位相同的{len(related)}组仅作防误合并提示，不合并记录。

字典35/35字段存在且英文名完全一致，逐项核查已完成；{counts['dictionary_placeholder_count']}项是通用占位或旧定义待确认。字典状态分布为{j(counts['dictionary_statuses'])}。CN文本均非空且未含替换字符，但非空不等于科学定义完整；所有35项操作性类型/取值/边界仍需复核。字典没有独立human approval或本次field stratum属性，本轮明确报告缺失，不把CURATED_PROJECT_DEFINITION当成人工批准。T002 compound定义含T004特定映射说明，其表内适用范围需复核。字典完整审阅不等于定义已获批准。

观察到candidate_eligible为yes182、unresolved9；normal_dietary_exposure为yes180、unresolved11，supplement/medicinal为no180、unresolved11。food_occurrence_confidence为moderate178、low / unresolved11、unresolved2；第三状态及复合状态均不是自动批准枚举。parent_class7类、analysis_panel9类、subclass36值；分类、面板及结构轴之间的边界属于DEFINITION_REVIEW_REQUIRED。current_review_status为identity resolved等复合文字178条、researcher inclusion4条、unresolved do not rank9条；4条纳入决定不代表全部结构已经人工审核。

191条food_occurrence_reference均为通用库名/资料类别，未提供候选物级定位引文，这是来源粒度的已确认问题，不是否定食物存在。分子式/分子量具体形式、食物存在与暴露/摄入、候选资格与实验/VSIR/临床、likely构念与实测证据之间均须保持边界。7条矿物辅因子源表已明确no capacity rank，不得并入小分子直接容量排名。分子量范围{min(mw)}–{max(mw)}，1.5 IQR诊断界限{lo}–{hi}，标记{len(outliers)}条分布离群，仅作为形式复核提示，不判错、不删除。

风险登记共{len(risks)}个去重issue_id：P0={pc.get('P0',0)}、P1={pc.get('P1',0)}、P2={pc.get('P2',0)}。这是独立治理问题数，不是错误候选物数；受影响记录和单元格可跨问题重叠。证据类型分别为{j(counts['issue_class_counts'])}。原值、路径、逻辑记录号和CSV物理行区间详见主表关联结果及supporting/Cell_Level_Findings_v0.1.csv。
'''
method='''本审计仅依据当前仓库数据及字典判断记录一致性和证据边界，未进行外部PubChem结构查证、文献恢复或化学形式裁决。未确认实体的名称相同不能视为结构匹配；空CID不与另一个空CID构成正匹配。诊断CID使用Decimal检验正整数等值，仅存于审计输出；所有源值逐字保留。完整InChIKey精确匹配，不以第一段代替完整键。名称大小写折叠仅为诊断，未做同义词规范化。CSV逻辑记录号从1计、表头不计；physical_lines从文件第1行计并包含多行单元格的整个区间。观察值列表是描述统计，不是获批受控词汇。

P0指阻止身份自动确认/映射批准的问题，P1指应优先人工定义/证据审核的问题，P2指维护与探索性提示；不等同科学错误严重度。DATA_CONFIRMED_ISSUE只陈述表内可直接证明的缺失/来源粒度问题；DEFINITION_REVIEW_REQUIRED不宣称已有错误；POTENTIAL_SCIENTIFIC_RISK不宣称具体化学或临床结论已经证实。
'''
order='''建议人工审查顺序：先处理AFF-0082/AFF-0150的具体身份及155条身份审核状态与下游文字的对应，再审阅名称含立体、盐、阳离子限定词的映射建议；随后决定候选物级食物来源和暴露证据标准，最后逐项审定字典定义、状态空间与审核角色。26/7/2分层本轮保持不变，建议在定义审核后再决定是否授权任何结构调整。允许进入人工审查，不允许直接发布、批准crosswalk、改字典、清洗身份或进入Phase 2；不重新计算任何排名，不判定VSIR，不commit/push。'''
integritytext=f'''开始HEAD与结束HEAD均为`{BASE}`，任务初次读取时工作树干净。写入前、后对审计目录和.git以外的全部{len(before)}个现有文件逐一做SHA-256及大小比对，变化0。审计程序先在唯一授权输出目录创建，故执行时Git已显示该目录未跟踪；与初次干净快照区别已记录。结束工作树只允许新增本审计目录。完整哈希和输入解析记录位于supporting；最终Git状态另见supporting/Final_Git_Status_v0.1.json。未修改任何原始CSV、Phase1字典、Word、历史包、冻结资产或配置，未执行Git写操作。'''
report=f'''# T002字段与数据质量只读核查 v0.1

{summary}
## 范围与方法

{tablelines}

{method}
T002独有ID完整清单：{j(counts['T002_only_ids'])}。T110孤儿ID：{j(counts['T110_only_ids'])}。

字段实际顺序：{j(header)}。分层按字段成员比较，不把分组展示顺序当作原表列顺序；未改动原表顺序。

## 人工审查与完整性

{order}

{integritytext}

```text
{status}
```

Cross-table Mapping Readiness整体HOLD来自两条未解决结构身份及未完成人工形式审核；155条结构标识支持的候选建议可送人工审阅，但不是获批crosswalk。Field Dictionary Review COMPLETE仅指35项审阅覆盖完成。
'''
writetext('T002_ReadOnly_Audit_Report_v0.1.md',report)
writetext('Sync_to_ChatGPT_Phase1B_T002_v0.1_CN.md',f'''# 同步ChatGPT：Phase1B T002只读核查 v0.1

Git基线与结束HEAD：`{BASE}`；分支main。任务完成后停止，未自动同步至其他聊天，由用户转交本文件及P0/P1附件。

{summary}
{order}

{integritytext}

```text
{status}
```
''')
names=['T002_ReadOnly_Audit_Report_v0.1.md','Sync_to_ChatGPT_Phase1B_T002_v0.1_CN.md','T002_Identity_and_CrossTable_Match_Audit_v0.1.csv','T002_Scientific_Risk_Register_v0.1.csv','T002_Field_Dictionary_Review_v0.1.csv','T002_Observed_Value_Domain_Audit_v0.1.csv','T002_Structure_and_Missingness_Audit_v0.1.csv','README_Audit_Scope_v0.1.md']
transfers='\n'.join(f"- {'P0' if i<4 else 'P1' if i<7 else 'P2'}：`{PREFIX}{name}`" for i,name in enumerate(names))
writetext('README_Audit_Scope_v0.1.md',f'''# Phase1B T002审计范围与转交清单

只读主表与关联参照；唯一新增目录为`{PREFIX}`。原始结构、191条记录、26/7/2分层及所有现有文件不变。报告CSV为机器可读审计中间结果，不创建或修改工作簿；按用户边界使用Python标准库、-B禁缓存、不安装依赖。audit_t002.py仅支持本轮核查，所有输出exclusive create，若同名文件存在立即停止，禁止直接覆盖重跑。

{method}
## 转交ChatGPT的完整相对路径

{transfers}

supporting包含逐单元格问题定位、全行语法验证、输入/匹配质控、前后完整性证据和最终Git状态。它们用于追溯，非正式crosswalk。CSV用UTF-8 BOM；JSON单元格为完整列表，无Excel显示截断带来的信息删除。

{integritytext}

```text
{status}
```
''')
finalsnapshot=snapshot();finalchanges=sorted(k for k in set(before)|set(finalsnapshot) if before.get(k)!=finalsnapshot.get(k));assert not finalchanges,finalchanges
finalstatus=git('status','--porcelain=v1','--untracked-files=all')
assert all(PREFIX in line.replace('\\','/') for line in finalstatus.splitlines()),finalstatus
writetext('supporting/Final_Git_Status_v0.1.json',j({'HEAD':git('rev-parse','HEAD'),'branch':git('branch','--show-current'),'worktree_status_before_final_status_file':finalstatus,'final_status_file_itself':'additional new untracked file in authorized audit directory','non_audit_changes':finalchanges,'existing_files_sha256_verified':len(before),'git_mutation':'NONE','counts':counts}))
print(json.dumps(counts,ensure_ascii=True,indent=2))
print(status)
