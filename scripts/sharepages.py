"""Static share pages: preview metadata is present without executing JavaScript."""
from html import escape

ORIGIN = 'https://solarfren69420.github.io/infographicmegalibrary/'

def zoom_toolbar():
    return '''<div id="item-zoom" class="zoom-toolbar" aria-label="Image zoom controls"><button type="button" data-zoom="out" aria-label="Zoom out">−</button><span data-zoom-label role="status">100%</span><button type="button" data-zoom="in" aria-label="Zoom in">+</button><button type="button" data-zoom="fit">Fit</button><button type="button" data-zoom="actual">100%</button></div>'''

def render_item(item, root):
    title, description, category = (escape(item[key], quote=True) for key in ('title', 'description', 'category'))
    url = ORIGIN + 'items/' + item['id'] + '/'
    image = ORIGIN + 'assets/social/' + item['id'] + '.jpg'
    original = '../../' + item['path']
    if item.get('thumbnail'):
        content = zoom_toolbar() + f'<div id="item-reader"><img src="{escape(original)}" alt="{title}" width="{item["width"]}" height="{item["height"]}"></div>'
        image_class = ' reader-shell'
    else:
        content = '<pre class="item-text">' + escape((root / item['path']).read_text()) + '</pre>'
        image_class = ''
    notice = ('This item is filed as spam and preserved outside the main library.' if item['collection'] == 'spam' else
              'This item is an exact repeated upload, preserved outside the main library.' if item['collection'] == 'duplicates' else
              'Archived, unverified offer or payment information. Check current details before relying on it.' if item['category'] == 'Subscriptions & offers' else
              'Archived concept or reference material. Use the zoom controls to read small text.')
    return f'''<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · Infographic Mega Library</title>
<meta name="description" content="{description}"><meta name="theme-color" content="#10151d">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website"><meta property="og:site_name" content="Infographic Mega Library">
<meta property="og:title" content="{title}"><meta property="og:description" content="{description}">
<meta property="og:url" content="{url}"><meta property="og:image" content="{image}">
<meta property="og:image:type" content="image/jpeg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{title} — {category}">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{description}"><meta name="twitter:image" content="{image}">
<meta name="twitter:image:alt" content="{title} — {category}">
<link rel="icon" href="../../assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="../../assets/styles.css"><link rel="stylesheet" href="../../assets/item.css"><link rel="stylesheet" href="../../assets/zoom.css">
<script src="../../assets/zoom.js" defer></script><script src="../../assets/share.js" defer></script>
</head><body>
<a class="skip" href="#main">Skip to infographic</a>
<header class="masthead"><a class="brand" href="../../"><img class="brand-avatar" src="../../assets/solarfren.png" alt="SolarFren"><span>INFOGRAPHIC<span class="brand-sub">MEGA LIBRARY</span></span></a><a class="repo-link" href="https://github.com/solarfren69420/infographicmegalibrary" target="_blank" rel="noopener">View on GitHub ↗</a></header>
<main id="main" class="item-main"><a class="back-link" href="../../">← Browse the library</a>
<div class="item-layout"><section class="item-image{image_class}" aria-label="Original file">{content}</section><section class="item-copy">
<p class="eyebrow">{category}</p><h1>{title}</h1><p class="item-description">{description}</p>
<p class="viewer-note">{escape(notice)}</p>
<div class="item-actions"><a class="primary-link" href="{escape(original)}" target="_blank" rel="noopener">Open original ↗</a><a href="{escape(original)}" download>Download file ↓</a><button id="copy-link" type="button">Copy share link</button></div>
<label class="share-label" for="share-url">Share this page</label><input id="share-url" type="url" readonly value="{url}"><p id="copy-status" class="copy-status" role="status"></p>
<p class="item-gallery-link"><a href="../../#{item['id']}">View in the gallery</a></p>
</section></div></main></body></html>'''
