'use strict';
const imageReader = document.getElementById('item-reader');
if (imageReader) window.attachImageZoom(imageReader, imageReader.querySelector('img'), document.getElementById('item-zoom'));
const copyButton = document.getElementById('copy-link');
const linkField = document.getElementById('share-url');
copyButton.addEventListener('click', async () => {
  try {
    await navigator.clipboard.writeText(linkField.value);
    document.getElementById('copy-status').textContent = 'Link copied.';
  } catch {
    linkField.focus();
    linkField.select();
    document.getElementById('copy-status').textContent = 'Copy the selected link.';
  }
});
