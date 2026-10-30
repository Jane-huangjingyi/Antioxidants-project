"""Audit and repair the 2026-10-16 user-directed file reorganization.

Run once with --apply to repair metadata and script paths. Default is read-only.
Scientific tables, frozen packages and historical source files are never rewritten.
"""
import argparse
import ast
import csv
import hashlib
import io
import json
import re
import subprocess
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATE = '2026-10-16'
REPORT = ROOT / 'current_review'
BASE = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()

def digest(data):
    return hashlib.sha256(data).hexdigest()

def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)

def rows(path):
    return list(csv.DictReader(path.open(encoding='utf-8-sig', newline='')))

def write_csv(path, data, fields=None):
    with path.open('w', encoding='utf-8-sig', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=fields or list(data[0]))
        writer.writeheader()
        writer.writerows(data)

def main(apply=False):
    tracked = git('ls-files', '-z').decode().split('\0')[:-1]
    missing = [name for name in tracked if not (ROOT / name).is_file()]
    candidates = defaultdict(list)
    for folder in ('archive', 'data/h_orac_stage25b'):
        for path in (ROOT / folder).rglob('*'):
            if path.is_file() and '__pycache__' not in path.parts:
                candidates[path.name].append(path)
    moves = []
    for old in missing:
        original = git('show', f'HEAD:{old}')
        matches = [path for path in candidates[Path(old).name]
                   if path.relative_to(ROOT).as_posix() not in tracked
                   and path.read_bytes().replace(b'\r\n', b'\n') == original.replace(b'\r\n', b'\n')]
        if len(matches) != 1:
            raise RuntimeError(f'Expected one byte-identical relocation for {old}: {matches}')
        target = matches[0]
        moves.append(dict(old_path=old, current_path=target.relative_to(ROOT).as_posix(),
                          sha256=digest(target.read_bytes()), content_status='BYTE_IDENTICAL_TO_BASELINE' if target.read_bytes() == original else 'IDENTICAL_AFTER_GIT_EOL_NORMALIZATION',
                          baseline_commit=BASE, verified_date=DATE))
    mapping = {r['old_path']: r['current_path'] for r in moves}
    names = {Path(a).name: b[len('data/h_orac_stage25b/'):] for a, b in mapping.items()
             if a.startswith('data/h_orac_stage25b/')}
    protected = {}
    for name in tracked:
        path = ROOT / name
        if path.is_file() and (name.startswith(('data/', 'references/', 'methods_qc/')) or '/frozen/' in name):
            protected[name] = digest(path.read_bytes())
    changed = []
    if apply:
        # Active code and navigation only. Historical scientific reports retain
        # their original path claims, recoverable through the migration ledger.
        active = list((ROOT / 'scripts').glob('*')) + list((ROOT / 'R').rglob('*.R'))
        active += [ROOT / n for n in ('CANONICAL_ASSET_REGISTRY.csv', 'PROJECT_FILE_INDEX_CN.md',
                                     'README_CN.md', 'docs/PROJECT_STAGE_INDEX_CN.md')]
        active += list(REPORT.glob('*.md'))
        active += [REPORT / 'CURRENT_DELIVERABLES_INDEX.csv']
        for path in active:
            if not path.is_file() or path == Path(__file__).resolve():
                continue
            raw = path.read_bytes()
            bom = raw.startswith(b'\xef\xbb\xbf')
            text = raw.decode('utf-8-sig')
            original = text
            for old, new in sorted(mapping.items(), key=lambda x: -len(x[0])):
                text = text.replace(old, new)
            if path.suffix in ('.py', '.ps1'):
                for filename, new in names.items():
                    pat = r"(DATA\s*/\s*|Join-Path\s+\$(?:base|dataDir)\s+)(['\"])" + re.escape(filename) + r"\2"
                    text = re.sub(pat, lambda m: m[1] + m[2] + new + m[2], text)
            if text != original:
                path.write_bytes((b'\xef\xbb\xbf' if bom else b'') + text.encode('utf-8'))
                changed.append(path.relative_to(ROOT).as_posix())
        registry_path = ROOT / 'CANONICAL_ASSET_REGISTRY.csv'
        registry_rows = rows(registry_path)
        for row in registry_rows:
            if '/stage25b1/' in row['canonical_path'] and row['current_status'] == 'ACTIVE_WORK_IN_PROGRESS':
                row['current_status'] = 'HISTORICAL_STAGE_OUTPUT'
                row['notes'] += '; Stage25B.1 completed; retained as stage provenance; current formal ranking is frozen v1.0'
        write_csv(registry_path, registry_rows)
        write_csv(REPORT / 'File_Reorganization_Migration_2026-10-16.csv', moves)
        # Update present-day destinations in the long-running migration registry,
        # while keeping old_path and historical reasons intact.
        ledger = ROOT / 'PROJECT_FILE_MIGRATION_MAP.csv'
        existing = rows(ledger)
        for row in existing:
            for key in ('proposed_new_path', 'canonical_replacement'):
                if row.get(key) in mapping:
                    row[key] = mapping[row[key]]
            if row['original_stage'] == '2026-10-16 reorganization' and row['proposed_new_path'].startswith('data/'):
                row['status_class'] = 'ACTIVE_CANONICAL' if '/stage25b/' in row['proposed_new_path'] else 'HISTORICAL_STAGE_OUTPUT'
        for move in moves:
            if any(r['old_path'] == move['old_path'] and r['proposed_new_path'] == move['current_path'] for r in existing):
                continue
            existing.append(dict(old_path=move['old_path'], original_stage='2026-10-16 reorganization',
                                 scientific_role='Stage-specific data or historical build asset',
                                 status_class=('ACTIVE_CANONICAL' if '/stage25b/' in move['current_path'] else 'HISTORICAL_STAGE_OUTPUT') if move['old_path'].startswith('data/') else 'HISTORICAL_ARCHIVE',
                                 proposed_new_path=move['current_path'], canonical_replacement='',
                                 reason='User-directed organization; byte-identical relocation verified',
                                 dependency_risk='reviewed', renamed='no', moved='yes', dependency_updated='yes'))
        write_csv(ledger, existing)
        changed.append('PROJECT_FILE_MIGRATION_MAP.csv')
        navigation_path = REPORT / 'PROJECT_NAVIGATION.md'
        navigation = navigation_path.read_text(encoding='utf-8')
        nav_lines = navigation.splitlines(keepends=True)
        for position, line in enumerate(nav_lines):
            if line.startswith('|') and '/stage25b1/' in line:
                fields = line.split('|')
                fields[5] = ' HISTORICAL_ARCHIVE '
                nav_lines[position] = '|'.join(fields)
        navigation_path.write_text(''.join(nav_lines), encoding='utf-8')
        self_inventory = 'current_review/Repository_File_Inventory_Current.csv'
        current_names = sorted(set(git('ls-files', '-z').decode().split('\0')[:-1] +
                                   git('ls-files', '--others', '--exclude-standard', '-z').decode().split('\0')[:-1]))
        current_names = [n for n in current_names if (ROOT / n).is_file()]
        registry = {r['canonical_path']: r for r in rows(ROOT / 'CANONICAL_ASSET_REGISTRY.csv')}
        historical = []
        for name in current_names:
            if name.startswith('archive/') or '/checkpoints/' in name:
                family = name.split('/')[1] if name.startswith('archive/') else 'H-ORAC checkpoints'
                historical.append(dict(file_path=name, file_name=Path(name).name, collection=family,
                                       version_role='HISTORICAL_CHECKPOINT' if '/checkpoints/' in name else 'HISTORICAL_ARCHIVE',
                                       current_replacement=';'.join(sorted({r['canonical_replacement'] for r in existing
                                                                          if r['proposed_new_path'] == name and r['canonical_replacement']})),
                                       sha256=digest((ROOT / name).read_bytes()),
                                       usage='Historical provenance; inspect stage context before reuse', verified_date=DATE))
            elif re.search(r'/(?:stage25b[1-4]|stage25b6[abc])/', name):
                historical.append(dict(file_path=name, file_name=Path(name).name, collection=name.split('/')[-2],
                                       version_role='PREVIOUS_STAGE_AUDIT_RETAINED', current_replacement='current_review/LATEST_PROJECT_STATUS_CN.md',
                                       sha256=digest((ROOT / name).read_bytes()),
                                       usage='Stage-specific evidence; current formal ranking stays frozen v1.0', verified_date=DATE))
        write_csv(REPORT / 'HISTORICAL_VERSION_INDEX.csv', historical)
        current_names = sorted(set(current_names + ['current_review/HISTORICAL_VERSION_INDEX.csv']))
        inventory = []
        tracked_set = set(tracked)
        for name in current_names:
            if name in (self_inventory, 'current_review/CURRENT_DELIVERABLES_INDEX.csv',
                        'archive/history/2026-10-16/review_governance/2026-10-16_File_Reorganization_Validation_2026-10-16.json'):
                continue
            path = ROOT / name
            inventory.append(dict(file_path=name, file_size=path.stat().st_size, sha256=digest(path.read_bytes()),
                                  git_status='TRACKED' if name in tracked_set else 'NEW_PATH_PENDING_GIT_RECORD',
                                  scientific_status=registry.get(name, {}).get('current_status', 'SUPPORTING_OR_UNREGISTERED'),
                                  verified_date=DATE))
        write_csv(REPORT / 'Repository_File_Inventory_Current.csv', inventory)
        # Regenerate hash metadata only; never rerun scientific stage builders.
        index_path = REPORT / 'CURRENT_DELIVERABLES_INDEX.csv'
        index = rows(index_path)
        for row in index:
            if '/stage25b1/' in row['canonical_source_path']:
                row['status'] = 'HISTORICAL_ARCHIVE'
                row['notes'] += '; completed stage output, retained for provenance' if 'completed stage output' not in row['notes'] else ''
        additions = [
            ('历史版本总索引', 'Historical version index', 'current_review/HISTORICAL_VERSION_INDEX.csv'),
            ('当前文件实存清单', 'Current repository inventory', self_inventory),
            ('本轮文件迁移对照', '2026-10-16 file relocation ledger', 'archive/history/2026-10-16/review_governance/2026-10-16_File_Reorganization_Migration_2026-10-16.csv'),
            ('文件移动影响核查', 'File reorganization audit', 'archive/history/2026-10-16/review_governance/2026-10-16_File_Reorganization_Audit_2026-10-16_CN.md'),
            ('历史版本查找说明', 'Archive navigation', 'archive/HISTORY_NAVIGATION_CN.md'),
            ('H-ORAC 分阶段目录说明', 'H-ORAC data navigation', 'data/h_orac_stage25b/README_CN.md')]
        for title, english, name in additions:
            if any(r['canonical_source_path'] == name for r in index):
                continue
            row = {key: '' for key in index[0]}
            row.update(deliverable_id=f'GOV-20261016-{len(index)+1}', title_cn=title, title_en=english,
                       track='Track G', version=DATE, status='CURRENT_REPORT', canonical_source_path=name,
                       source_commit=BASE, last_verified_date=DATE, review_priority='P1',
                       notes='Working-tree location audit; baseline commit recorded separately')
            index.append(row)
        for row in index:
            source = ROOT / row['canonical_source_path']
            if source.is_file():
                row['sha256'] = digest(source.read_bytes())
                row['last_verified_date'] = DATE
        write_csv(index_path, index)

    registry_missing = [r['canonical_path'] for r in rows(ROOT / 'CANONICAL_ASSET_REGISTRY.csv')
                        if not (ROOT / r['canonical_path']).is_file()]
    frozen = rows(ROOT / 'data/h_orac_stage25b/frozen/Stage25B5_Frozen_Asset_SHA256_Manifest.csv')
    frozen_bad = [r['asset_path'] for r in frozen if digest((ROOT / r['asset_path']).read_bytes()) != r['sha256']]
    changed_science = [n for n, h in protected.items() if digest((ROOT / n).read_bytes()) != h]
    invalid_python = []
    for path in (ROOT / 'scripts').glob('*.py'):
        try:
            ast.parse(path.read_text(encoding='utf-8-sig'), filename=str(path))
        except SyntaxError as exc:
            invalid_python.append(f'{path.name}: {exc}')
    rank = rows(ROOT / 'data/h_orac_stage25b/stage25b/Stage25B_HORAC_Quantitative_Ranking.csv')
    frozen_rank = rows(ROOT / 'data/h_orac_stage25b/frozen/Stage25B_Frozen_Primary_HORAC_Top20.csv')
    ranking_consistent = [r['candidate_id'] for r in rank[:20]] == [r['candidate_id'] for r in frozen_rank]
    all_modified = git('diff', '--name-only', '--diff-filter=M', '-z').decode().split('\0')[:-1]
    result = dict(baseline=BASE, verified_moves=len(moves), changed_navigation_and_scripts=all_modified,
                  registry_missing=registry_missing, frozen_checked=len(frozen), frozen_bad=frozen_bad,
                  scientific_content_changed=changed_science, python_syntax_errors=invalid_python,
                  canonical_Top20_matches_frozen=ranking_consistent)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if apply:
        (REPORT / 'File_Reorganization_Validation_2026-10-16.json').write_text(
            json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    if registry_missing or frozen_bad or changed_science or invalid_python or not ranking_consistent:
        raise SystemExit(1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true')
    main(parser.parse_args().apply)
