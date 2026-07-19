(() => {
  document.documentElement.classList.add('js');
  const toggle = document.querySelector('.menu-toggle');
  const nav = document.querySelector('.mobile-nav');
  if (!toggle || !nav) return;

  const close = () => {
    toggle.setAttribute('aria-expanded', 'false');
    nav.classList.remove('open');
  };

  toggle.addEventListener('click', () => {
    const open = toggle.getAttribute('aria-expanded') === 'true';
    toggle.setAttribute('aria-expanded', String(!open));
    nav.classList.toggle('open', !open);
  });

  nav.addEventListener('click', (event) => {
    if (event.target.closest('a')) close();
  });

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') {
      close();
      toggle.focus();
    }
  });

  const outline = document.querySelector('#page-outline');
  const content = document.querySelector('.docs-content');
  if (outline && content) {
    const headings = [...content.querySelectorAll('h2, h3')];
    headings.forEach((heading, index) => {
      if (!heading.id) heading.id = `section-${index + 1}`;
      const link = document.createElement('a');
      link.href = `#${heading.id}`;
      link.textContent = heading.textContent;
      if (heading.tagName === 'H3') link.className = 'outline-child';
      outline.append(link);
    });
    if (!headings.length) outline.closest('.page-outline').hidden = true;
  }
})();
