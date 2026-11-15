document.addEventListener('DOMContentLoaded', async () => {
  const grid = document.querySelector('[data-gallery-source]');
  if (!grid) return;
  const english = document.documentElement.lang.toLowerCase().startsWith('en');
  const source = grid.dataset.gallerySource;
  const generated = new URL('content/galerija-visi.json', document.baseURI).href;
  const fallback = new URL(source, document.baseURI).href;
  try {
    let response = await fetch(generated, {cache:'no-store'});
    if (!response.ok) response = await fetch(fallback, {cache:'no-store'});
    if (!response.ok) throw new Error('HTTP ' + response.status);
    const data = await response.json();
    grid.replaceChildren();
    for (const item of (data.artworks || [])) {
      if (item.published === false) continue;
      const article = document.createElement('article');
      article.className = 'artwork';
      article.dataset.category = item.category === 'archyvas' ? 'archyvas' : 'nauji';
      const img = document.createElement('img');
      img.loading = 'lazy';
      img.decoding = 'async';
      const imagePath = item.image || '';
img.src = imagePath.startsWith('/media/')
  ? new URL(imagePath.slice(1), new URL('.', document.baseURI)).href
  : imagePath;
      img.alt = (english ? item.title_en : item.title_lt) || item.title_lt || '';
      img.addEventListener('error', () => {
        img.style.display = 'none';
        const note = document.createElement('div');
        note.className = 'image-missing';
        note.textContent = english ? 'Image temporarily unavailable' : 'Fotografija laikinai nepasiekiama';
        img.before(note);
      });
      const details = document.createElement('div');
      details.className = 'details';
      const heading = document.createElement('h3');
      heading.textContent = (english ? item.title_en : item.title_lt) || item.title_lt || '';
      const description = document.createElement('p');
      
const decodeEntities = (value) => {
  const textarea = document.createElement('textarea');
  textarea.innerHTML = value || '';
  return textarea.value;
};

description.textContent = decodeEntities(
  (english ? item.details_en : item.details_lt)
  || item.details_lt
  || ''
);

      details.append(heading, description);
      article.append(img, details);
      grid.append(article);
    }
    const active = document.querySelector('.filter.active');
    if (active && active.dataset.filter !== 'visi') {
      grid.querySelectorAll('.artwork').forEach(a => a.hidden = a.dataset.category !== active.dataset.filter);
    }
  } catch (error) {
    console.error('Gallery could not be loaded:', error);
    grid.textContent = english ? 'Gallery temporarily unavailable' : 'Galerija laikinai nepasiekiama';
  }
});
