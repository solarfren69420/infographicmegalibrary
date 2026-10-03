#!/usr/bin/env python3
"""Render the complete handbook in GitHub's README without changing the PDF.

Uses only Python's standard library. Handbook prose remains in guides/;
the PDF builder's coverage map supplies the same complete source index.
"""
from __future__ import annotations

import ast
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = 'https://solarfren69420.github.io/infographicmegalibrary/'
BANNERS = ROOT / 'assets/readme-book'
PARTS = {
    '01': ('01-foundations', 'PART ONE', 'Start with your computer',
           'Chapters 1–4 · Files, folders, backups, and your first commands', '#46e9ca'),
    '05': ('02-first-project', 'PART TWO', 'Choose a route. Try a project.',
           'Chapters 5–7 · Modding choices, AI tools, and a playable exercise', '#69b7ff'),
    '08': ('03-rust-and-data', 'PART THREE', 'Understand Rust and game systems',
           'Chapters 8–10 · A real program, reusable rules, and organized data', '#ffd36d'),
    '11': ('04-research-and-bridges', 'PART FOUR', 'Research, bridges, and rewrites',
           'Chapters 11–14 · Evidence, Ghidra, MCP, and integration choices', '#c6a0ff'),
    '15': ('05-ideas-and-testing', 'PART FIVE', 'Turn the brainstorm into a result',
           'Chapters 15–17 · Named game ideas, combination math, and testing', '#ff91b1'),
    '18': ('06-publish-and-continue', 'PART SIX', 'Publish, troubleshoot, and continue',
           'Chapters 18–21 · GitHub, costs, debugging, and copy-paste prompts', '#91e59b'),
    'A': ('07-reference', 'REFERENCE', 'The glossary, collection, and sources',
          'Appendices A–C · Every retained infographic and all primary references', '#69b7ff'),
}


def coverage_map():
    """Read a literal constant without importing the PDF-only dependencies."""
    tree = ast.parse((ROOT / 'scripts/build_handbook.py').read_text())
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id == 'COVERAGE'
            for target in node.targets
        ):
            return ast.literal_eval(node.value)
    raise ValueError('Missing PDF coverage map')


def banner_svg(label, title, subtitle, accent):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="166" viewBox="0 0 1200 166" role="img" aria-label="{html.escape(title, quote=True)}">
<rect width="1200" height="166" rx="16" fill="#132631"/>
<rect x="0" y="0" width="9" height="166" rx="4" fill="{accent}"/>
<text x="36" y="36" fill="{accent}" font-family="Arial,sans-serif" font-size="17" font-weight="700" letter-spacing="3">{html.escape(label)}</text>
<text x="35" y="86" fill="#f4f8fb" font-family="Arial,sans-serif" font-size="39" font-weight="700">{html.escape(title)}</text>
<text x="36" y="130" fill="#c7d6df" font-family="Arial,sans-serif" font-size="23">{html.escape(subtitle)}</text>
</svg>
'''


def make_banners():
    BANNERS.mkdir(exist_ok=True)
    for filename, label, title, subtitle, accent in PARTS.values():
        (BANNERS / (filename + '.svg')).write_text(banner_svg(label, title, subtitle, accent))
    (BANNERS / 'cover.svg').write_text('''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="420" viewBox="0 0 1200 420" role="img" aria-label="SolarFren's complete beginner handbook: from your first folder to your first tested project">
<defs><linearGradient id="bg" x2="1" y2="1"><stop stop-color="#10151d"/><stop offset="1" stop-color="#17413f"/></linearGradient></defs>
<rect width="1200" height="420" rx="22" fill="url(#bg)"/>
<rect x="2" y="2" width="1196" height="416" rx="20" fill="none" stroke="#46e9ca" stroke-width="3"/>
<path d="M1032 30v96h98M998 62v97h98" fill="none" stroke="#c6a0ff" stroke-width="6"/>
<text x="48" y="62" fill="#46e9ca" font-family="Arial,sans-serif" font-size="20" font-weight="700" letter-spacing="3">SOLARFREN · INFOGRAPHIC MEGA LIBRARY</text>
<text x="45" y="140" fill="#ffffff" font-family="Arial,sans-serif" font-size="54" font-weight="700">THE COMPLETE</text>
<text x="45" y="205" fill="#ffffff" font-family="Arial,sans-serif" font-size="54" font-weight="700">BEGINNER HANDBOOK</text>
<text x="48" y="258" fill="#d5e5ec" font-family="Arial,sans-serif" font-size="28">From your first folder to your first tested project.</text>
<rect x="48" y="290" width="207" height="44" rx="9" fill="#46e9ca"/>
<rect x="271" y="290" width="207" height="44" rx="9" fill="#69b7ff"/>
<rect x="494" y="290" width="228" height="44" rx="9" fill="#ffd36d"/>
<text x="70" y="319" fill="#10151d" font-family="Arial,sans-serif" font-size="21" font-weight="700">21 CHAPTERS</text>
<text x="291" y="319" fill="#10151d" font-family="Arial,sans-serif" font-size="21" font-weight="700">3 APPENDICES</text>
<text x="514" y="319" fill="#10151d" font-family="Arial,sans-serif" font-size="21" font-weight="700">66-PAGE PDF</text>
<text x="48" y="380" fill="#c7d6df" font-family="Arial,sans-serif" font-size="23">Windows · macOS · Linux   |   Read the entire book below.</text>
</svg>
''')


def expand_indexes(book):
    catalog = json.loads((ROOT / 'data/catalog.json').read_text())
    coverage = coverage_map()
    items = [item for item in catalog if item['collection'] == 'infographics']
    if set(coverage) != {item['id'] for item in items}:
        raise ValueError('Coverage must include every retained infographic')
    rows = ['| Original infographic | Chapters and explanation |', '| --- | --- |']
    for item in items:
        rows.append(f'| [{item["id"]} · {item["title"]}]({SITE}items/{item["id"]}/) '
                    f'| {coverage[item["id"]]} |')
    book = book.replace('<!-- COVERAGE -->', '\n'.join(rows))
    sources = json.loads((ROOT / 'guides/sources.json').read_text())
    entries = []
    for key, title, url in sources:
        entries.append(f'<a name="source-{key.lower()}"></a>\n\n'
                       f'**{key} · [{title}]({url})**\n\n<{url}>')
    book = book.replace('<!-- SOURCES -->', '\n\n'.join(entries))
    # Only bare citations, not existing Markdown labels, are converted.
    book = re.sub(r'\[(S\d{2})\](?!\()',
                  lambda match: f'[{match[1]}](#source-{match[1].lower()})', book)
    return book


def render_book(book):
    rendered = []
    headings = []
    current = None
    subsection = 0
    in_code = False
    for line in book.splitlines():
        if line.startswith('```'):
            in_code = not in_code
        if not in_code and line.startswith('# '):
            if current:
                rendered.extend(['', '[↑ Back to contents](#book-contents)', '', '---', ''])
            title = line[2:]
            current = title.split(' · ', 1)[0]
            subsection = 0
            anchor = 'book-' + current.lower()
            if current in PARTS:
                filename, _, part_title, _, _ = PARTS[current]
                rendered.extend([f'![{part_title}](assets/readme-book/{filename}.svg)', ''])
            rendered.extend([f'<a name="{anchor}"></a>', '', '## ' + title, ''])
            headings.append((0, title, anchor))
        elif not in_code and line.startswith('## '):
            subsection += 1
            anchor = f'book-{current.lower()}-section-{subsection}'
            title = line[3:]
            rendered.extend([f'<a name="{anchor}"></a>', '', '### ' + title, ''])
            headings.append((1, title, anchor))
        else:
            rendered.append(line)
    if in_code:
        raise ValueError('Unclosed code block in the handbook')
    rendered.extend(['', '[↑ Back to contents](#book-contents)'])
    return '\n'.join(rendered), headings


def build_readme():
    make_banners()
    book = expand_indexes((ROOT / 'guides/beginner-handbook.md').read_text())
    rendered, headings = render_book(book)
    if len([h for h in headings if h[0] == 0]) != 24:
        raise ValueError('Expected all 21 chapters and 3 appendices')
    quick = '\n'.join(f'- [{title}](#{anchor})' for level, title, anchor in headings if level == 0)
    detailed = '\n'.join(('  ' if level else '') + f'- [{title}](#{anchor})'
                         for level, title, anchor in headings)
    introduction = (ROOT / 'scripts/readme-introduction.md').read_text().strip()
    maintenance = (ROOT / 'scripts/readme-maintenance.md').read_text().strip()
    preface = '''
![The complete SolarFren beginner handbook](assets/readme-book/cover.svg)

<p align="center"><a href="https://solarfren69420.github.io/infographicmegalibrary/"><img src="assets/solarfren.png" width="210" alt="SolarFren"></a></p>

**The entire book is right here in this README:** all 21 chapters, the glossary, the complete infographic coverage index, 34 sources, code examples, and copy-paste AI prompts. The PDF remains available at its original link. The colorful banners group the chapters into a reading path; the text, tables, and code below are readable and selectable directly on GitHub.

**Choose how to read:** [📖 Keep reading below](#book-01) · [⬇️ Download the original PDF](https://solarfren69420.github.io/infographicmegalibrary/guides/Infographic-Mega-Library-Beginner-Handbook.pdf) · [🚨 Open the live gallery](https://solarfren69420.github.io/infographicmegalibrary/) · [🎮 Try the browser exercise](https://solarfren69420.github.io/infographicmegalibrary/guides/exercises/mechanics-playground.html)
'''
    contents = f'''<a name="book-contents"></a>

## 📚 Table of contents

{quick}

<details>
<summary><strong>Show the full contents — every chapter and section</strong></summary>

{detailed}

</details>

---
'''
    ending = '''
---

<a name="library-maintenance"></a>

## 🗂️ Library files and maintenance

[↑ Book contents](#book-contents) · [🚨 Live library](https://solarfren69420.github.io/infographicmegalibrary/) · [📖 PDF download](https://solarfren69420.github.io/infographicmegalibrary/guides/Infographic-Mega-Library-Beginner-Handbook.pdf)

The collection catalog and existing setup/update information are preserved below.
'''
    destination = ROOT / 'README.md'
    destination.write_text(introduction + '\n\n' + preface.strip() + '\n\n' + contents
                           + '\n' + rendered + '\n\n' + ending.strip() + '\n\n'
                           + maintenance + '\n')
    print(f'Built complete README book: 24 chapters/appendices, {len(headings)} contents entries, '
          f'32 infographic references, 34 sources; {destination.stat().st_size:,} bytes.')


if __name__ == '__main__':
    build_readme()
