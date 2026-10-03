#!/usr/bin/env python3
"""Validate the library and stage only intended public files for GitHub Pages."""
from pathlib import Path
from collections import Counter
import hashlib, json, shutil
from sharepages import render_item

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / '_site'
PUBLIC_FOLDERS = ('assets', 'data', 'infographics', 'references', 'prompts', 'disclaimers', 'spam', 'duplicates')

def safe_file(relative):
    path = ROOT / relative
    if not path.resolve().is_relative_to(ROOT) or path.is_symlink() or not path.is_file():
        raise ValueError(f'Unsafe or missing catalog file: {relative}')
    return path

def build():
    catalog = json.loads((ROOT / 'data/catalog.json').read_text())
    report = json.loads((ROOT / 'data/organization-report.json').read_text())
    ids, paths = set(), set()
    by_id = {item['id']: item for item in catalog}
    for item in catalog:
        if item['id'] in ids or item['path'] in paths:
            raise ValueError('Duplicate catalog identity or destination')
        ids.add(item['id']); paths.add(item['path'])
        original = safe_file(item['path'])
        if original.parts[len(ROOT.parts)] not in PUBLIC_FOLDERS:
            raise ValueError('Catalog references a nonpublic folder')
        if hashlib.sha256(original.read_bytes()).hexdigest() != item['sha256']:
            raise ValueError(f'Original file changed: {item["path"]}')
        if original.stat().st_size != item['bytes']:
            raise ValueError('File size mismatch')
        if item.get('thumbnail'): safe_file(item['thumbnail'])
        if item.get('duplicateOf') and by_id[item['duplicateOf']]['sha256'] != item['sha256']:
            raise ValueError('Repeated upload does not match its original')
    counts = Counter(item['collection'] for item in catalog)
    if counts != {'infographics':32,'references':3,'duplicates':3,'spam':8,'prompts':1,'disclaimers':2}:
        raise ValueError(f'Unexpected collection counts: {counts}')
    if len(catalog) != report['downloadedFiles']:
        raise ValueError('Catalog does not account for every downloaded attachment')
    originals = {str(path.relative_to(ROOT)) for folder in PUBLIC_FOLDERS[2:] for path in (ROOT / folder).rglob('*') if path.is_file()}
    if originals != paths:
        raise ValueError(f'Uncataloged or missing originals: {originals ^ paths}')
    (ROOT / 'assets/catalog.js').write_text('window.LIBRARY_CATALOG = ' + json.dumps(catalog,ensure_ascii=False) + ';\n')
    if SITE.exists(): shutil.rmtree(SITE)
    SITE.mkdir()
    shutil.copy2(ROOT / 'index.html', SITE / 'index.html')
    for folder in PUBLIC_FOLDERS:
        shutil.copytree(ROOT / folder, SITE / folder)
    safe_file('assets/social/library.jpg')
    for item in catalog:
        safe_file('assets/social/' + item['id'] + '.jpg')
        page = SITE / 'items' / item['id'] / 'index.html'
        page.parent.mkdir(parents=True, exist_ok=True)
        page.write_text(render_item(item, ROOT))
    (SITE / '.nojekyll').touch()
    print(f'Validated {len(catalog)} original files; {counts["infographics"]} infographics, {counts["spam"]} spam, {counts["duplicates"]} repeats.')
    print(f'Built {len(catalog)} static share pages with distinct Open Graph and X image previews.')
    print(f'Staged {sum(p.stat().st_size for p in SITE.rglob("*") if p.is_file()) / 1024 / 1024:.1f} MiB for GitHub Pages. Raw chat and local backup excluded.')

if __name__ == '__main__': build()
