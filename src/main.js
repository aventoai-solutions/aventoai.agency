import Lenis from 'lenis';
import './style.css';

const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

// ---------- smooth scroll ----------
if (!reduced) {
  const lenis = new Lenis({ lerp: 0.1 });
  const raf = t => { lenis.raf(t); requestAnimationFrame(raf); };
  requestAnimationFrame(raf);
  document.querySelectorAll('a[href*="#"]').forEach(a => {
    a.addEventListener('click', e => {
      const url = new URL(a.href);
      if (url.pathname !== location.pathname || !url.hash) return;
      const el = document.querySelector(url.hash);
      if (!el) return;
      e.preventDefault();
      lenis.scrollTo(el, { offset: -90, duration: 1.2 });
      history.replaceState(null, '', url.hash);
    });
  });
  // arrive at #anchor from another page
  if (location.hash) {
    const el = document.querySelector(location.hash);
    if (el) setTimeout(() => lenis.scrollTo(el, { offset: -90, immediate: true }), 50);
  }
}

// ---------- header ----------
const header = document.querySelector('.site-header');
const onScroll = () => header?.classList.toggle('scrolled', window.scrollY > 8);
onScroll();
window.addEventListener('scroll', onScroll, { passive: true });

const page = document.body.dataset.page;
document.querySelectorAll(`.main-nav [data-nav="${page}"]`).forEach(a => {
  a.classList.add('active');
  a.setAttribute('aria-current', 'page');
});

const toggle = document.querySelector('.menu-toggle');
const menu = document.getElementById('mobile-menu');
toggle?.addEventListener('click', () => {
  const open = toggle.getAttribute('aria-expanded') === 'true';
  toggle.setAttribute('aria-expanded', String(!open));
  toggle.setAttribute('aria-label', open ? 'Open menu' : 'Close menu');
  menu.hidden = open;
});
menu?.querySelectorAll('a').forEach(a => a.addEventListener('click', () => {
  toggle.setAttribute('aria-expanded', 'false');
  menu.hidden = true;
}));

// ---------- reveal on scroll ----------
const io = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
  });
}, { rootMargin: '0px 0px -8% 0px', threshold: 0.12 });
document.querySelectorAll('.reveal, .process li').forEach(el => io.observe(el));

// ---------- step sequences (lead card, workflow, phone) ----------
function sequence(list, selector, interval = 1100, hold = 2600) {
  const items = [...list.querySelectorAll(selector)];
  if (!items.length) return;
  if (reduced) { items.forEach(i => i.classList.add('on')); return; }
  let i = 0, timer;
  const tick = () => {
    if (i === 0) items.forEach(x => x.classList.remove('on'));
    items[i].classList.add('on');
    i = (i + 1) % items.length;
    timer = setTimeout(tick, i === 0 ? hold : interval);
  };
  const vis = new IntersectionObserver(([e]) => {
    clearTimeout(timer);
    if (e.isIntersecting) { timer = setTimeout(tick, 400); }
  });
  vis.observe(list);
}
document.querySelectorAll('[data-sequence]').forEach(el =>
  sequence(el, el.dataset.sequence, Number(el.dataset.interval) || 1100),
);

// ---------- work filters ----------
const filters = document.querySelectorAll('.filter');
filters.forEach(btn => btn.addEventListener('click', () => {
  filters.forEach(b => { b.classList.toggle('active', b === btn); b.setAttribute('aria-pressed', String(b === btn)); });
  const f = btn.dataset.filter;
  document.querySelectorAll('.proj[data-cat]').forEach(p => {
    p.classList.toggle('hide', f !== 'all' && !p.dataset.cat.split(' ').includes(f));
  });
}));

// ---------- contact form ----------
// No server yet: the form opens the visitor's email app with everything filled in,
// addressed to hello@aventoai.agency. Swap for a form service (e.g. Formspree) later.
const form = document.getElementById('contact-form');
form?.addEventListener('submit', e => {
  e.preventDefault();
  if (!form.reportValidity()) return;
  const d = Object.fromEntries(new FormData(form));
  const body = [
    `Full Name: ${d.name}`,
    `Company Name: ${d.company || '-'}`,
    `Email: ${d.email}`,
    `Phone: ${d.phone || '-'}`,
    `Service Interested In: ${d.service || '-'}`,
    `Budget Range: ${d.budget || '-'}`,
    '',
    'Project Description:',
    d.message,
  ].join('\n');
  const subject = `Project request from ${d.name}${d.company ? ` (${d.company})` : ''}`;
  window.location.href = `mailto:hello@aventoai.agency?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
  const status = document.getElementById('form-status');
  if (status) status.textContent = 'Your email app should open with your request ready to send. If it does not, email hello@aventoai.agency directly.';
});
