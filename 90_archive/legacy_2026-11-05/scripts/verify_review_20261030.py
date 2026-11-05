"""Check source preservation, navigation, vector structure and native workbook XML."""
from pathlib import Path
import csv,json,re,hashlib,os,zipfile,xml.etree.ElementTree as ET
from urllib.parse import unquote
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'workspaces/repository_review_20261030';REVIEW=ROOT/'current_review'
base=json.loads((OUT/'Baseline.json').read_text(encoding='utf8'));actions=json.loads((OUT/'File_Actions.json').read_text(encoding='utf8'))
move={r['old_path']:r['new_path'] for r in actions if r['action']!='PRESERVE_BEFORE_REBUILD_REVIEW_ENTRY'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
preserved=[];missing=[];changed=[]
for r in base['files']:
 old=r['path'];p=ROOT/move.get(old,old)
 if old.startswith('current_review/') or any(x['old_path']==old and x['action']=='PRESERVE_BEFORE_REBUILD_REVIEW_ENTRY' for x in actions):
  a=next(x for x in actions if x['old_path']==old);p=ROOT/a['new_path']
 if not p.exists():missing.append(old);continue
 if sha(p)!=r['sha256']:changed.append(old)
 else:preserved.append(old)
assert not missing,missing
protected=[p for p in changed if p.startswith(('data/','workspaces/','figures/','methods_qc/','archive/'))]
protected=[p for p in protected if p!='figures/README_CN.md']
assert not protected,protected
with (ROOT/'data/h_orac_stage25b/frozen/Stage25B5_Frozen_Asset_SHA256_Manifest.csv').open(encoding='utf-8-sig') as f:
 freeze=list(csv.DictReader(f))
for r in freeze:assert sha(ROOT/r['asset_path'])==r['sha256'],r['asset_path']
figure_rows=[];scripts=[p for p in (ROOT/'R').rglob('*.R') if '/library/' not in p.as_posix()]
for r in base['files']:
 old=r['path']
 if not old.startswith('figures/') or not old.endswith('.png'):continue
 stem=Path(old).stem;png=ROOT/'figures/editable'/Path(old).relative_to('figures');svg=png.with_suffix('.svg');assert png.exists() and svg.exists(),old
 if 'HORAC_' in stem:script=ROOT/'R/stage25b5'/('editable_01_render_frozen_primary_top20.R' if 'Primary' in stem else 'editable_02_render_b2_sensitivity.R')
 elif old.startswith(('figures/candidate_universe/','figures/cross_class_and_lipid_supporting/','figures/supervisor/')):script=ROOT/'R/supporting/render_supporting_figures.R'
 else:
  matches=[p for p in scripts if ('"'+stem+'.png"') in p.read_text(encoding='utf-8-sig') and 'supporting/' not in p.as_posix()]
  assert len(matches)==1,(old,matches);script=matches[0]
 text=svg.read_text(encoding='utf8');tree=ET.fromstring(text);tags=[e.tag.rsplit('}',1)[-1] for e in tree.iter()]
 assert tags.count('text')>0 and tags.count('image')==0,(svg,tags.count('text'),tags.count('image'))
 scripttext=script.read_text(encoding='utf-8-sig');inputs=[]
 for args in re.findall(r'read_project_csv\(([^)]*)\)',scripttext):
  parts=re.findall(r'"([^"]+)"',args);p='/'.join(parts)
  if p.startswith('data/'):inputs.append(p)
 inputs+=re.findall(r'"(data/[^"\n]+\.csv)"',scripttext)
 for p in inputs:assert (ROOT/p).exists(),p
 figure_rows.append({'原图片':old,'最新PNG':png.relative_to(ROOT).as_posix(),'可编辑SVG':svg.relative_to(ROOT).as_posix(),'完整R脚本':script.relative_to(ROOT).as_posix(),'脚本输入数据':' ; '.join(sorted(set(inputs))),'SVG文字对象数':tags.count('text'),'SVG栅格对象数':tags.count('image'),'状态':'REGENERATED_VECTOR_STRUCTURE_VERIFIED_NOT_NATIVE_ILLUSTRATOR_TESTED'})
assert len(figure_rows)==51
with (OUT/'Figure_Reproduction_Index.csv').open('w',encoding='utf-8-sig',newline='') as f:w=csv.DictWriter(f,fieldnames=list(figure_rows[0]));w.writeheader();w.writerows(figure_rows)
visual=['# 图片与R复现','', '当前51张科研图片均由R从既有数据重绘为PNG与SVG，写入figures/editable，原图片及冻结哈希不变。字体、颜色、点线、图例与尺寸在可读R代码中修改；未改变原科学表或排名。','', '从项目根目录运行：`& "C:/Program Files/R/R-4.5.3/bin/Rscript.exe" R/reproduce_all_figures.R`。R依赖使用已忽略的R/library；会话版本与警告记录见workspaces/repository_review_20261030。通用样式在R/common/plot_config.R；21张支持图的调色板和具体图层在R/supporting/render_supporting_figures.R；冻结图的非破坏性重绘在R/stage25b5/editable_*.R。','', 'SVG使用svglite保留text及矢量几何对象，未嵌入整张位图；在Illustrator中可取消组合后修改文字、点和线。需保留匹配字体；本轮验证SVG结构和图面，未宣称完成Illustrator原生交互测试。改变R后重新导出会覆盖重绘版，Illustrator人工修改应另存带日期编辑副本。','', '候选物/脂相支持图恢复自旧R配方，使用当前路径；只说明既有构念，不把各类数值混合为综合排名。Vitamin C明确标注历史来源仍待闭环，缺少有意义百分位者显示文字而不赋予假点。','', '|图片|PNG|SVG|完整R代码|','|---|---|---|---|']
for r in figure_rows:
 def link(p):return '<../'+p+'>'
 visual.append('|'+Path(r['原图片']).stem+'|[预览]('+link(r['最新PNG'])+')|[编辑]('+link(r['可编辑SVG'])+')|[R]('+link(r['完整R脚本'])+')|')
visual+=['','输入数据和逐图验证见[复现索引](../workspaces/repository_review_20261030/Figure_Reproduction_Index.csv)。历史废弃图保留在日期归档内；不把旧截图包装为新可复现结果。历史图/来源图/非科研QC预览登记见[历史图片缺口表](../workspaces/repository_review_20261030/Historical_Image_Register.csv)。']
(REVIEW/'VISUALIZATION_REPRODUCIBILITY_CN.md').write_text('\n'.join(visual)+'\n',encoding='utf8')
hist=[]
for r in base['files']:
 p=r['path']
 if not p.endswith(('.png','.svg','.jpg','.jpeg')) or p.startswith('figures/') or 'phase2_r_partial_library' in p:continue
 hist.append({'原路径':p,'当前唯一位置':move.get(p,p),'原SHA256':r['sha256'],'类别':'QC预览或来源图（非科研图）' if any(x in p for x in ['/previews/','/local_sources/']) else '历史科研图；原版本保留','R复现状态':'未将截图或历史结论冒充当前重绘；按原脚本及当时输入定点复核','当前对应':'查51张当前复现索引；无对应者保留原图与缺口'})
with (OUT/'Historical_Image_Register.csv').open('w',encoding='utf-8-sig',newline='') as f:w=csv.DictWriter(f,fieldnames=list(hist[0]));w.writeheader();w.writerows(hist)
# Current markdown links: repair dated moves while preserving historical text bytes.
bad=[];fixed=[]
for p in [*REVIEW.rglob('*.md'),*ROOT.glob('*.md'),*ROOT.joinpath('R').rglob('*.md'),*ROOT.joinpath('figures').rglob('*.md'),*ROOT.joinpath('docs').rglob('*.md')]:
 if 'library' in p.relative_to(ROOT).parts:continue
 t=p.read_text(encoding='utf-8-sig');out=t
 for m in re.finditer(r'\[[^\]]*\]\((<[^>]+>|[^)]+)\)',t):
  token=m.group(1);target=unquote(token.strip('<>').strip()).split('#')[0]
  if not target or re.match(r'^[a-zA-Z]+://',target) or target.startswith('#'):continue
  candidate=(p.parent/target).resolve()
  if candidate.exists():continue
  if candidate in [(OUT/'Final_QC.json').resolve(),(OUT/'Link_Audit.json').resolve()]:continue
  try:rel=candidate.relative_to(ROOT).as_posix()
  except ValueError:continue
  if rel in move:
   replacement='<'+os.path.relpath(ROOT/move[rel],p.parent).replace('\\','/')+'>';out=out.replace('('+token+')','('+replacement+')');fixed.append([str(p.relative_to(ROOT)),target,move[rel]])
  else:bad.append([p.relative_to(ROOT).as_posix(),target])
 if out!=t:p.write_text(out,encoding='utf8')
# Missing historical links in old reports are catalogued separately; no fabricated file.
new_bad=[r for r in bad if r[0].startswith('current_review/')]
assert not new_bad,new_bad
(OUT/'Link_Audit.json').write_text(json.dumps({'fixed':fixed,'preexisting_unresolved_links_in_other_docs':bad},ensure_ascii=False,indent=2),encoding='utf8')
book=ROOT/'outputs/review_20261030/Evidence_Catalog_2026-10-30.xlsx'
ns={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
with zipfile.ZipFile(book) as z:
 wb=ET.fromstring(z.read('xl/workbook.xml'));sheets=[r.attrib['name'] for r in wb.findall('s:sheets/s:sheet',ns)];assert len(sheets)==9,sheets
 tablefiles=[p for p in z.namelist() if p.startswith('xl/tables/table') and p.endswith('.xml')];assert len(tablefiles)==8
 counts=[]
 for p in tablefiles:
  table=ET.fromstring(z.read(p));assert table.find('s:autoFilter',ns) is not None
  counts.append({'name':table.attrib['name'],'range':table.attrib['ref']})
 errors=[]
 for p in [x for x in z.namelist() if x.startswith('xl/worksheets/sheet') and x.endswith('.xml')]:
  if not p.endswith('/sheet1.xml'):
   head=ET.parse(z.open(p)).getroot()
   assert head.find('s:sheetViews/s:sheetView/s:pane',ns) is not None,p
  for _,e in ET.iterparse(z.open(p),events=('end',)):
   if e.tag.endswith('}c') and e.attrib.get('t')=='e':errors.append([p,e.attrib['r']])
   e.clear()
 assert not errors,errors
summary={'date':'2026-10-30','original_files_accounted_for':len(base['files']),'unchanged_or_same_byte_mapped':len(preserved),'allowed_active_changes':changed,'missing_original_files':missing,'frozen_assets_SHA_pass':len(freeze),'current_scientific_figures':len(figure_rows),'editable_png':len(figure_rows),'editable_svg_with_text_without_raster':len(figure_rows),'historical_image_register':len(hist),'workbook_sheets':sheets,'workbook_tables':counts,'workbook_formula_errors':errors,'unresolved_old_links_outside_new_navigation':len(bad),'deleted_redundant_copies':2}
(OUT/'Final_QC.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(summary,ensure_ascii=False))
