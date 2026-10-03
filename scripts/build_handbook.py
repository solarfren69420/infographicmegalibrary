#!/usr/bin/env python3
"""Build the beginner handbook and companion examples from editable Markdown.

Requires ReportLab 5 and Pillow. The Pages build uses the checked-in PDF.
"""
from __future__ import annotations
import argparse
import html
import json
import re
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate, Flowable, Frame, KeepTogether, PageBreak, PageTemplate,
    Paragraph, Preformatted, Spacer, Table, TableStyle,
)
from reportlab.platypus.tableofcontents import TableOfContents

ROOT = Path(__file__).resolve().parents[1]
GUIDES = ROOT / 'guides'
WIDTH, HEIGHT = A4
MARGIN = 49
BODY_WIDTH = WIDTH - MARGIN * 2
NAVY = colors.HexColor('#132631')
TEAL = colors.HexColor('#08786c')
PALE = colors.HexColor('#edf6f3')
INK = colors.HexColor('#24333d')
GREY = colors.HexColor('#62717b')
SITE = 'https://solarfren69420.github.io/infographicmegalibrary/'

COVERAGE = {
    'item-01': '5, 8–9, 14–15 · Binding, modding, and reimplementation routes.',
    'item-02': '8–10, 14 · Consolidated Rust and modular data-driven design.',
    'item-03': '10–12, 14 · Evidence records, indexing, parity, and implementation.',
    'item-05': '11, 15, 17 · Archived community snapshot and project verification.',
    'item-06': '11 · Matching reconstruction versus portable rewrites; live percentages unverified.',
    'item-07': '11 · Debug artifacts as clues, with documented Bully example.',
    'item-09': '11, 16 · Open-world systems as inspiration; extraction not established.',
    'item-10': '7–10, 14–15 · Small combat/building prototype before larger systems.',
    'item-11': '6, 10–12, 14 · AI-assisted stages; garbled automation commands not reused.',
    'item-12': '5, 7, 15 · Original combat/building rules rather than merging installations.',
    'item-13': '13, 15 · GTA/Minecraft state, events, depth, timing, and platform constraints.',
    'item-16': '13, 15 · Elden Ring bridge architecture remains a conceptual adaptation.',
    'item-17': '13, 15, 21 · Avatar/HUD first slice and explicit integration limits.',
    'item-19': '9, 16 · Creative roster organized into compatible subsystem ideas.',
    'item-20': '8–14, 17 · Research → records → modules → tested runtime.',
    'item-21': '16 · Genre categories, constraints, and corrected subset counts.',
    'item-22': '16 · High-speed combat/world fusion as an inspiration menu.',
    'item-23': '16 · Many-game roster narrowed to small experiments.',
    'item-24': '5, 15–16 · Native voxel sandbox first; physics/circuits later.',
    'item-30': '5, 13–14 · Two live processes versus one newly implemented runtime.',
    'item-31': '13, 21 · Cleaned bridge prompt with staged verification.',
    'item-32': '10, 14, 21 · Cleaned rewrite prompt with specifications and tests.',
    'item-33': '2, 6, 20 · Official downloads by OS; desktop and CLI distinguished.',
    'item-34': '4, 6, 20 · Current tool entry points; archived flags not installation instructions.',
    'item-36': '11–12 · Ghidra/Gemini prerequisites, MCP, and compatible version sets.',
    'item-37': '19 · Proposed payment chain; checkout/account support not verified.',
    'item-38': '19 · Real four-month offer checked; dates and billing terms stated.',
    'item-42': '19 · Total obligation, renewal, and BNPL risk consolidated.',
    'item-43': '5, 15, 21 · Postal/Minecraft proposal and SkyCraft compatibility limits.',
    'item-44': '8–9 · Rust basics, compiler, Cargo, and subsystem boundaries.',
    'item-47': '8–9, 14 · Rust strengths and realistic engineering tradeoffs.',
    'item-48': '8–9, 14, 20 · Memory-safety and cross-target claims corrected.',
}


def inline(text: str) -> str:
    """A deliberately small Markdown subset, escaped before PDF markup."""
    placeholders = []

    def stash(value):
        placeholders.append(value)
        return f'ZZMARKUP{len(placeholders)-1}ZZ'

    text = re.sub(r'`([^`]+)`', lambda m: stash(
        '<font name="DejaVuMono" size="10.1">' + html.escape(m[1]) + '</font>'), text)
    text = re.sub(r'\[([^\]]+)\]\((https?://[^\s]+)\)', lambda m: stash(
        '<link href="' + html.escape(m[2], quote=True) + '" color="#08786c">'
        + html.escape(m[1]) + '</link>'), text)
    text = html.escape(text)
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'\[(S\d{2})\]', r'<link href="#\1" color="#08786c">[\1]</link>', text)
    for i, value in enumerate(placeholders):
        text = text.replace(f'ZZMARKUP{i}ZZ', value)
    return text


def make_styles():
    base = dict(fontName='DejaVuSans', textColor=INK, alignment=TA_LEFT)
    return {
        'body': ParagraphStyle('Body', **base, fontSize=12, leading=16,
                               spaceAfter=7, splitLongWords=True),
        'chapter': ParagraphStyle('Chapter', **{**base, 'fontName': 'DejaVuSans-Bold', 'textColor': NAVY},
                                  fontSize=25, leading=31,
                                  spaceAfter=20, keepWithNext=True),
        'section': ParagraphStyle('Section', **{**base, 'fontName': 'DejaVuSans-Bold', 'textColor': TEAL},
                                  fontSize=15, leading=19,
                                  spaceBefore=9, spaceAfter=7, keepWithNext=True),
        'bullet': ParagraphStyle('Bullet', **base, fontSize=12, leading=16,
                                 leftIndent=18, firstLineIndent=-15, spaceAfter=5),
        'code': ParagraphStyle('Code', fontName='DejaVuMono', fontSize=9.4,
                               leading=13.4, textColor=NAVY,
                               backColor=PALE, borderPadding=10,
                               spaceBefore=7, spaceAfter=12),
        'cell': ParagraphStyle('Cell', **base, fontSize=10.4, leading=14.8),
        'cellhead': ParagraphStyle('CellHead', fontName='DejaVuSans-Bold',
                                   fontSize=10.4, leading=14.8, textColor=colors.white),
        'small': ParagraphStyle('Small', **base, fontSize=10.5, leading=15,
                                spaceAfter=7),
        'url': ParagraphStyle('URL', **{**base, 'textColor': TEAL}, fontSize=8.4, leading=12,
                              splitLongWords=True, spaceAfter=12),
        'toc0': ParagraphStyle('TOCChapter', fontName='DejaVuSans-Bold', fontSize=12,
                               leading=18, textColor=NAVY, leftIndent=0,
                               firstLineIndent=0, rightIndent=24, spaceBefore=7),
        'toc1': ParagraphStyle('TOCSection', fontName='DejaVuSans', fontSize=10.4,
                               leading=14.2, textColor=GREY, leftIndent=15,
                               firstLineIndent=0, rightIndent=24, spaceBefore=0),
    }


class Cover(Flowable):
    def __init__(self):
        super().__init__()
        self.width = BODY_WIDTH
        self.height = HEIGHT - 130

    def draw(self):
        c = self.canv
        c.saveState()
        # Cover uses full page coordinates; body page frames remain separate.
        origin_x, origin_y = c.absolutePosition(0, 0)
        c.translate(-origin_x, -origin_y)
        c.setFillColor(colors.black)
        c.rect(0, 0, WIDTH, HEIGHT, fill=1, stroke=0)
        c.setFillColor(colors.HexColor('#45eed0'))
        c.rect(49, HEIGHT - 77, 52, 5, fill=1, stroke=0)
        c.setFont('DejaVuSans-Bold', 11)
        c.drawString(49, HEIGHT - 107, 'SOLARFREN’S COLLECTION')
        c.setFillColor(colors.white)
        c.setFont('DejaVuSans-Bold', 30)
        c.drawString(49, HEIGHT - 163, 'INFOGRAPHIC')
        c.drawString(49, HEIGHT - 204, 'MEGA LIBRARY')
        c.setFont('DejaVuSans-Bold', 24)
        c.setFillColor(colors.HexColor('#45eed0'))
        c.drawString(49, HEIGHT - 256, 'BEGINNER HANDBOOK')
        c.setFillColor(colors.HexColor('#c7d6df'))
        c.setFont('DejaVuSans', 13)
        for i, line in enumerate([
            'From your first folder to your first tested project.',
            'Game systems · AI prompts · Rust · Modding',
            'Research · Databases · Safe publishing',
        ]):
            c.drawString(49, HEIGHT - 294 - 23*i, line)
        c.drawImage(str(ROOT/'assets/solarfren.png'), (WIDTH-360)/2, 143,
                    width=360, height=240, preserveAspectRatio=True,
                    anchor='c', mask='auto')
        c.setFillColor(colors.HexColor('#45eed0'))
        c.setFont('DejaVuSans-Bold', 11)
        c.drawString(49, 117, 'WINDOWS  ·  macOS  ·  LINUX')
        c.setFillColor(colors.HexColor('#c7d6df'))
        c.setFont('DejaVuSans', 10)
        c.drawString(49, 90, 'Organized explanations, practical exercises, and reusable prompts.')
        c.drawString(49, 67, 'Full-size A4 edition  ·  3 October 2026')
        c.bookmarkPage('cover')
        c.addOutlineEntry('SolarFren · Beginner Handbook', 'cover', 0)
        c.restoreState()


class HandbookDoc(BaseDocTemplate):
    def __init__(self, filename, **kwargs):
        super().__init__(filename, pagesize=A4, leftMargin=MARGIN,
                         rightMargin=MARGIN, topMargin=66, bottomMargin=53,
                         title='SolarFren · Infographic Mega Library Beginner Handbook',
                         author='SolarFren', subject='Beginner computer, modding, AI and game systems guide',
                         **kwargs)
        self.current_chapter = 'Contents'
        frame = Frame(MARGIN, 53, BODY_WIDTH, HEIGHT-119,
                      leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        self.addPageTemplates(PageTemplate(id='Body', frames=[frame], onPageEnd=self.footer))

    def beforeDocument(self):
        self.current_chapter = 'Contents'

    def footer(self, c, doc):
        if doc.page == 1:
            return
        c.saveState()
        c.setStrokeColor(colors.HexColor('#d3dedf'))
        c.line(MARGIN, HEIGHT-40, WIDTH-MARGIN, HEIGHT-40)
        c.setFillColor(GREY)
        c.setFont('DejaVuSans', 8)
        title = self.current_chapter
        while pdfmetrics.stringWidth(title, 'DejaVuSans', 8) > BODY_WIDTH-10:
            title = title[:-2]
        c.drawString(MARGIN, HEIGHT-30, title)
        c.line(MARGIN, 37, WIDTH-MARGIN, 37)
        c.setFont('DejaVuSans', 8)
        c.drawString(MARGIN, 23, 'SolarFren · Beginner Handbook · 3 Oct 2026')
        c.drawRightString(WIDTH-MARGIN, 23, str(doc.page))
        c.linkURL(SITE, (MARGIN, 17, MARGIN+240, 32), relative=0)
        c.restoreState()

    def afterFlowable(self, flowable):
        if hasattr(flowable, '_bookmark'):
            key, level, title, in_toc = flowable._bookmark
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(title, key, level)
            if level == 0:
                self.current_chapter = title
            if in_toc:
                self.notify('TOCEntry', (level, html.escape(title), self.page, key))


def heading(text, style, key, level, toc=True):
    p = Paragraph(inline(text), style)
    p._bookmark = (key, level, text, toc)
    return p


def markdown_blocks(text, styles):
    lines = text.splitlines()
    story = []
    i = 0
    h1 = 0
    h2 = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        if line == '<!-- COVERAGE -->':
            items = json.loads((ROOT/'data/catalog.json').read_text())
            originals = [x for x in items if x['collection']=='infographics']
            if {x['id'] for x in originals} != set(COVERAGE):
                raise ValueError('Coverage must account for every retained infographic')
            for item in originals:
                title = f'{item["id"]} · {item["title"]}'
                desc = 'Chapters ' + COVERAGE[item['id']]
                story.append(KeepTogether([
                    Paragraph('<b><link href="'+SITE+'items/'+item['id']+'/" color="#08786c">'
                              +html.escape(title)+'</link></b>', styles['small']),
                    Paragraph(html.escape(desc), styles['small']), Spacer(1,5),
                ]))
            i += 1
        elif line == '<!-- SOURCES -->':
            for key, title, url in json.loads((GUIDES/'sources.json').read_text()):
                story.append(KeepTogether([
                    Paragraph('<a name="'+key+'"/><b>'+key+' · '+html.escape(title)+'</b>',styles['small']),
                    Paragraph('<link href="'+html.escape(url,quote=True)+'" color="#08786c">'
                              +html.escape(url)+'</link>',styles['url']),
                ]))
            i += 1
        elif line.startswith('# '):
            h1 += 1; h2 = 0
            story.extend([PageBreak(), heading(line[2:],styles['chapter'],f'ch{h1}',0)])
            i += 1
        elif line.startswith('## '):
            h2 += 1
            story.append(heading(line[3:],styles['section'],f'ch{h1}-s{h2}',1))
            i += 1
        elif line.startswith('```'):
            i += 1; code=[]
            while i < len(lines) and not lines[i].startswith('```'):
                code.append(lines[i]); i += 1
            if i == len(lines):
                raise ValueError('Unclosed code fence')
            story.append(Preformatted('\n'.join(code),styles['code']))
            i += 1
        elif line.startswith('|'):
            rows=[]
            while i < len(lines) and lines[i].strip().startswith('|'):
                row=[x.strip() for x in lines[i].strip().strip('|').split('|')]
                if not all(re.fullmatch(r'[:\-\s]+',x) for x in row):
                    rows.append(row)
                i += 1
            count=len(rows[0])
            if any(len(row)!=count for row in rows):
                raise ValueError('Inconsistent Markdown table')
            widths = ([BODY_WIDTH*.26,BODY_WIDTH*.74] if count==2
                      else [BODY_WIDTH/count]*count)
            data=[[Paragraph(inline(cell),styles['cellhead' if r==0 else 'cell'])
                   for cell in row] for r,row in enumerate(rows)]
            table=Table(data,colWidths=widths,repeatRows=1,hAlign='LEFT')
            table.setStyle(TableStyle([
                ('BACKGROUND',(0,0),(-1,0),NAVY),
                ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,PALE]),
                ('VALIGN',(0,0),(-1,-1),'TOP'),
                ('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),
                ('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8),
                ('LINEBELOW',(0,0),(-1,-1),.3,colors.HexColor('#d6e3e1')),
            ]))
            story.extend([Spacer(1,6),table,Spacer(1,15)])
        elif re.match(r'^\d+\. ',line):
            match=re.match(r'^(\d+)\. (.*)',line)
            story.append(Paragraph('<b>'+match[1]+'.</b> '+inline(match[2]),styles['bullet']))
            i += 1
        else:
            paragraph=[line]; i += 1
            while i<len(lines) and lines[i].strip() and not re.match(
                r'^(#|\||```|<!--|\d+\. )',lines[i].strip()):
                paragraph.append(lines[i].strip()); i += 1
            story.append(Paragraph(inline(' '.join(paragraph)),styles['body']))
    return story


def write_examples(markdown):
    blocks = re.findall(r'```(rust|json|sql)\n(.*?)\n```',markdown,re.S)
    names={'rust':'roll-demo.rs','json':'roll.json','sql':'mechanics.sql'}
    for language,content in blocks:
        (GUIDES/'exercises'/names[language]).write_text(content+'\n')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--font-dir',type=Path,
                        default=Path('/usr/share/fonts/truetype/dejavu'))
    args=parser.parse_args()
    for name,file in [('DejaVuSans','DejaVuSans.ttf'),
                      ('DejaVuSans-Bold','DejaVuSans-Bold.ttf'),
                      ('DejaVuMono','DejaVuSansMono.ttf')]:
        pdfmetrics.registerFont(TTFont(name,str(args.font_dir/file)))
    pdfmetrics.registerFontFamily('DejaVuSans',normal='DejaVuSans',bold='DejaVuSans-Bold',
                                  italic='DejaVuSans',boldItalic='DejaVuSans-Bold')
    styles=make_styles()
    text=(GUIDES/'beginner-handbook.md').read_text()
    write_examples(text)
    toc=TableOfContents()
    toc.levelStyles=[styles['toc0'],styles['toc1']]
    toc.dotsMinLevel=0
    toc.tableStyle=TableStyle([
        ('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0),
        ('TOPPADDING',(0,0),(-1,-1),1),('BOTTOMPADDING',(0,0),(-1,-1),1),
    ])
    story=[Cover(),PageBreak(),
           heading('Contents',styles['chapter'],'contents',0,False),
           Paragraph('Click a chapter or section to jump to it. Page numbers match the printed footer. '
                     'PDF bookmarks provide the same navigation.',styles['body']),toc]
    story.extend(markdown_blocks(text,styles))
    destination=GUIDES/'Infographic-Mega-Library-Beginner-Handbook.pdf'
    doc=HandbookDoc(str(destination))
    doc.multiBuild(story)
    print(f'Built {destination.name} · {doc.page} A4 pages · embedded fonts · clickable contents/bookmarks.')
    print(f'Source: {len(text.split()):,} words; coverage: {len(COVERAGE)} infographics.')


if __name__=='__main__':
    main()
