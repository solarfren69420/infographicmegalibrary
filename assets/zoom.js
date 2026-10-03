'use strict';
window.attachImageZoom = function attachImageZoom(container, image, toolbar) {
  let scale = 1;
  let fitMode = true;
  let dragging = null;
  const stage = document.createElement('div');
  stage.className = 'zoom-stage';
  stage.append(image);
  container.replaceChildren(stage);
  container.classList.add('zoomable');
  container.tabIndex = 0;
  container.setAttribute('aria-label', 'Image reader. Use plus and minus to zoom, arrow keys to scroll, or drag the image.');
  const label = toolbar.querySelector('[data-zoom-label]');
  const fitScale = () => Math.min((container.clientWidth - 24) / image.naturalWidth, (container.clientHeight - 24) / image.naturalHeight, 1);
  function draw(next, preserveCenter = true) {
    if (!image.naturalWidth || !container.clientWidth) return;
    const previous = scale;
    const centerX = container.scrollLeft + container.clientWidth / 2;
    const centerY = container.scrollTop + container.clientHeight / 2;
    scale = Math.max(.05, Math.min(4, next));
    const width = image.naturalWidth * scale, height = image.naturalHeight * scale;
    image.style.width = `${width}px`;
    image.style.height = `${height}px`;
    stage.style.width = `${Math.max(container.clientWidth, width + 24)}px`;
    stage.style.height = `${Math.max(container.clientHeight, height + 24)}px`;
    label.textContent = `${Math.round(scale * 100)}%`;
    toolbar.querySelector('[data-zoom="out"]').disabled = scale <= .05;
    toolbar.querySelector('[data-zoom="in"]').disabled = scale >= 4;
    container.classList.toggle('can-pan', width > container.clientWidth || height > container.clientHeight);
    if (preserveCenter && previous) {
      container.scrollLeft = centerX * scale / previous - container.clientWidth / 2;
      container.scrollTop = centerY * scale / previous - container.clientHeight / 2;
    } else {
      container.scrollLeft = 0; container.scrollTop = 0;
    }
  }
  function action(name) {
    if (name === 'fit') { fitMode = true; draw(fitScale(), false); }
    else { fitMode = false; draw(name === 'actual' ? 1 : scale * (name === 'in' ? 1.25 : .8)); }
  }
  const onClick = event => { const button = event.target.closest('[data-zoom]'); if (button && toolbar.contains(button)) action(button.dataset.zoom); };
  const onKey = event => {
    if (event.key === '+' || event.key === '=') { event.preventDefault(); action('in'); }
    if (event.key === '-') { event.preventDefault(); action('out'); }
    if (event.key === '0') { event.preventDefault(); action('fit'); }
  };
  const onWheel = event => {
    if (event.ctrlKey || event.metaKey) { event.preventDefault(); action(event.deltaY < 0 ? 'in' : 'out'); }
  };
  const onDown = event => {
    if (event.pointerType !== 'mouse' || event.button !== 0 || !container.classList.contains('can-pan')) return;
    dragging = {x:event.clientX, y:event.clientY, left:container.scrollLeft, top:container.scrollTop};
    container.setPointerCapture(event.pointerId); container.classList.add('dragging'); event.preventDefault();
  };
  const onMove = event => {
    if (!dragging) return;
    container.scrollLeft = dragging.left + dragging.x - event.clientX;
    container.scrollTop = dragging.top + dragging.y - event.clientY;
  };
  const onUp = () => { dragging = null; container.classList.remove('dragging'); };
  const initialize = () => draw(fitMode ? fitScale() : scale, false);
  const observer = new ResizeObserver(() => draw(fitMode ? fitScale() : scale, false));
  observer.observe(container);
  image.addEventListener('load', initialize);
  image.draggable = false;
  toolbar.addEventListener('click', onClick);
  container.addEventListener('keydown', onKey);
  container.addEventListener('wheel', onWheel, {passive:false});
  container.addEventListener('pointerdown', onDown);
  container.addEventListener('pointermove', onMove);
  container.addEventListener('pointerup', onUp);
  container.addEventListener('pointercancel', onUp);
  if (image.complete) initialize();
  return () => {
    observer.disconnect(); image.removeEventListener('load', initialize);
    toolbar.removeEventListener('click', onClick); container.removeEventListener('keydown', onKey);
    container.removeEventListener('wheel', onWheel); container.removeEventListener('pointerdown', onDown);
    container.removeEventListener('pointermove', onMove); container.removeEventListener('pointerup', onUp);
    container.removeEventListener('pointercancel', onUp);
    container.classList.remove('zoomable', 'can-pan', 'dragging');
  };
};
