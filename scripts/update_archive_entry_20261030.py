"""Preserve previous archive navigation before correcting its live entry."""
from pathlib import Path
import json
root=Path(__file__).resolve().parents[1];out=root/'workspaces/repository_review_20261030';base=json.loads((out/'Baseline.json').read_text(encoding='utf8'));p=out/'File_Actions.json';actions=json.loads(p.read_text(encoding='utf8'))
for old in ['archive/HISTORY_NAVIGATION_CN.md','archive/README_CN.md']:
 if any(r['old_path']==old and r['action']=='PRESERVE_BEFORE_REBUILD_REVIEW_ENTRY' for r in actions):continue
 r=next(r for r in base['files'] if r['path']==old);new=f"archive/history/{r['last_git_date']}/review_governance/{r['last_git_date']}_{Path(old).name}"
 q=root/new;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes((root/old).read_bytes());actions.append({'old_path':old,'new_path':new,'action':'PRESERVE_BEFORE_REBUILD_REVIEW_ENTRY','sha256':r['sha256'],'date':r['last_git_date'],'date_basis':'previous navigation last Git date'})
 (root/old).write_text('# 历史归档查找入口\n\n2026-10-30：历史文件按最后可追溯内容更新日期整理到history/YYYY-MM-DD/主题/日期_原文件名。请从[日期索引](../current_review/HISTORICAL_VERSION_INDEX.csv)、[分类导航](../current_review/PROJECT_NAVIGATION.md)或[路径与哈希台账](../workspaces/repository_review_20261030/File_Actions.json)查找；[清理与命名规则](../current_review/HISTORY_AND_CLEANUP_CN.md)说明固定引用文件的例外。\n\n旧导航和重要过程记录已保留日期快照；仅清理两份相同字节历史图冗余副本。检查点和冻结资产仍在data/h_orac_stage25b的原位置。本地来源缓存保持原位置，不因内容相同而删除。历史脚本可能依赖当时布局，需复现历史结果时从相应Git版本恢复独立环境；当前绘图使用R/reproduce_all_figures.R，不直接运行归档脚本覆盖新结果。\n',encoding='utf8')
p.write_text(json.dumps(actions,ensure_ascii=False,indent=2),encoding='utf8')
