'use strict';
const items = window.LIBRARY_CATALOG;
const byId = new Map(items.map(item => [item.id, item]));
const mainItems = items.filter(item => !['spam', 'duplicates'].includes(item.collection));
const topics = [...new Set(items.filter(item => item.collection === 'infographics').map(item => item.category))];
const $ = id => document.getElementById(id);
let category = 'all';
let visible = [];
let current = null;
let lastFocused = null;
const buttons = [];

function element(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}
function categoryItems(key) {
  if (key === 'all') return mainItems;
  if (['spam', 'duplicates'].includes(key)) return items.filter(item => item.collection === key);
  return mainItems.filter(item => item.category === key);
}
function addCategory(container, key, label) {
  const button = element('button', 'nav-button');
  button.type = 'button';
  button.append(element('span', '', label), element('span', 'nav-count', String(categoryItems(key).length)));
  button.dataset.category = key;
  button.addEventListener('click', () => { category = key; render(); });
  container.append(button);
  buttons.push(button);
}
addCategory($('categories'), 'all', 'All library');
topics.forEach(topic => addCategory($('categories'), topic, topic));
['References', 'Text prompts', 'Disclaimers'].forEach(topic => addCategory($('categories'), topic, topic));
addCategory($('separate'), 'spam', 'Spam');
addCategory($('separate'), 'duplicates', 'Repeated uploads');

function render() {
  const query = $('search').value.trim().toLowerCase();
  const words = query.split(/\s+/).filter(Boolean);
  visible = categoryItems(category).filter(item => {
    const haystack = [item.title, item.description, item.category, ...item.tags].join(' ').toLowerCase().replaceAll('-', ' ');
    return words.every(word => haystack.includes(word));
  });
  if ($('sort').value === 'title') visible.sort((a,b) => a.title.localeCompare(b.title));
  if ($('sort').value === 'newest') visible.sort((a,b) => b.postedAt.localeCompare(a.postedAt));
  buttons.forEach(button => {
    const active = button.dataset.category === category;
    button.classList.toggle('active', active);
    button.setAttribute('aria-current', active ? 'true' : 'false');
  });
  $('heading').textContent = category === 'all' ? 'Explore the library' : category === 'spam' ? 'Spam collection' : category === 'duplicates' ? 'Repeated uploads' : category;
  $('result-count').textContent = `${visible.length} ${visible.length === 1 ? 'item' : 'items'}${query ? ' matching your search' : ''}`;
  $('reset').hidden = category === 'all' && !query;
  $('empty').hidden = visible.length !== 0;
  $('gallery').replaceChildren();
  for (const item of visible) {
    const card = element('article', 'card');
    const preview = element('button', 'preview');
    preview.type = 'button';
    preview.setAttribute('aria-label', `View ${item.title}`);
    if (item.thumbnail) {
      const img = element('img');
      img.src = item.thumbnail; img.alt = item.title; img.loading = 'lazy'; img.decoding = 'async';
      img.width = item.width; img.height = item.height;
      preview.append(img);
    } else {
      preview.classList.add('text-preview');
      preview.textContent = 'TEXT PROMPT\n\nPostal 2\n+ Minecraft\n\n↗ Read the prompt';
    }
    preview.addEventListener('click', () => openItem(item.id));
    const body = element('div', 'card-body');
    body.append(element('p', 'card-category', item.category));
    if (item.category === 'Subscriptions & offers') body.append(element('span', 'badge', 'Archived · unverified'));
    const heading = element('h2');
    const title = element('button', 'title-button', item.title);
    title.type = 'button'; title.addEventListener('click', () => openItem(item.id));
    heading.append(title); body.append(heading);
    const footer = element('div', 'card-footer');
    footer.append(element('span', '', `${item.extension.toUpperCase()} · ${(item.bytes / 1024 / 1024).toFixed(1)} MB`));
    const download = element('a', '', 'Download ↓'); download.href = item.path; download.download = item.path.split('/').pop();
    download.setAttribute('aria-label', `Download ${item.title}`);
    footer.append(download); body.append(footer); card.append(preview, body); $('gallery').append(card);
  }
}
function reset() { category = 'all'; $('search').value = ''; render(); }
$('search').addEventListener('input', render);
$('sort').addEventListener('change', render);
$('reset').addEventListener('click', reset);
$('empty-reset').addEventListener('click', reset);
$('disclaimer-link').addEventListener('click', () => { category = 'Disclaimers'; $('search').value = ''; render(); });

function navigationItems() { return visible.some(item => item.id === current?.id) ? visible : categoryItems(current.collection === 'spam' ? 'spam' : current.collection === 'duplicates' ? 'duplicates' : 'all'); }
function openItem(id, updateHash = true) {
  const item = byId.get(id);
  if (!item) return;
  current = item;
  if (!$('viewer').open) lastFocused = document.activeElement;
  $('viewer-title').textContent = item.title;
  $('viewer-description').textContent = item.description;
  $('viewer-category').textContent = item.category;
  $('viewer-note').textContent = item.collection === 'spam' ? 'Filed as spam using the image and the surrounding chat. Preserved separately from the main library.' : item.collection === 'duplicates' ? `Exact repeated upload of ${byId.get(item.duplicateOf).title}.` : item.category === 'Subscriptions & offers' ? 'Archived image. Offer details, deadlines, payment options, and terms have not been verified.' : 'View the original file to read small text. The archive’s claims and setup instructions have not been independently verified.';
  const media = $('viewer-media'); media.replaceChildren();
  if (item.thumbnail) {
    const link = element('a'); link.href = item.path; link.target = '_blank'; link.rel = 'noopener'; link.setAttribute('aria-label', `Open full-size ${item.title}`);
    const img = element('img'); img.src = item.path; img.alt = item.title; link.append(img); media.append(link);
  } else {
    const pre = element('pre', '', 'Loading prompt…'); media.append(pre);
    fetch(item.path).then(response => { if (!response.ok) throw new Error('Prompt unavailable'); return response.text(); }).then(text => { if (current.id === item.id) pre.textContent = text; }).catch(() => { pre.textContent = 'Use “Open original” to read this text file.'; });
  }
  $('viewer-meta').replaceChildren();
  for (const [label, value] of [['File', item.extension.toUpperCase()], ['Dimensions', item.width ? `${item.width} × ${item.height}` : 'Text document'], ['Posted', new Date(item.postedAt).toLocaleDateString(undefined, {year:'numeric',month:'short',day:'numeric'})], ['Folder', item.path.slice(0, item.path.lastIndexOf('/'))]]) {
    $('viewer-meta').append(element('dt', '', label), element('dd', '', value));
  }
  $('original-link').href = item.path;
  $('download-link').href = item.path;
  $('download-link').download = item.path.split('/').pop();
  const nav = navigationItems(); const index = nav.findIndex(entry => entry.id === id);
  $('previous').disabled = index <= 0; $('next').disabled = index < 0 || index >= nav.length - 1;
  if (updateHash) history.replaceState(null, '', `#${item.id}`);
  if (!$('viewer').open) $('viewer').showModal();
}
function move(direction) {
  if (!current) return;
  const nav = navigationItems(); const index = nav.findIndex(item => item.id === current.id);
  if (nav[index + direction]) openItem(nav[index + direction].id);
}
$('previous').addEventListener('click', () => move(-1));
$('next').addEventListener('click', () => move(1));
$('close-viewer').addEventListener('click', () => $('viewer').close());
$('viewer').addEventListener('click', event => { if (event.target === $('viewer')) { const r = $('viewer').getBoundingClientRect(); if (event.clientX < r.left || event.clientX > r.right || event.clientY < r.top || event.clientY > r.bottom) $('viewer').close(); } });
$('viewer').addEventListener('close', () => { history.replaceState(null, '', location.pathname + location.search); if (lastFocused?.isConnected) lastFocused.focus(); });
document.addEventListener('keydown', event => { if (!$('viewer').open || ['INPUT', 'SELECT', 'TEXTAREA'].includes(event.target.tagName)) return; if (event.key === 'ArrowLeft') { event.preventDefault(); move(-1); } if (event.key === 'ArrowRight') { event.preventDefault(); move(1); } });
window.addEventListener('hashchange', () => { const id = location.hash.slice(1); if (byId.has(id)) openItem(id, false); else if ($('viewer').open) $('viewer').close(); });
render();
if (byId.has(location.hash.slice(1))) openItem(location.hash.slice(1), false);
