"""Builds the inner pages (services, work, about, privacy, terms) from index.html's header and footer.

Run from the site root:  python tools/pages.py
The Home page (index.html) is written by hand; every other page takes its <header> and <footer>
from it, so the bar and the footer are identical everywhere. Edit the page bodies below, then run.
"""
import re, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
home = (ROOT / 'index.html').read_text(encoding='utf-8')
NAV = re.search(r'<header class="nav.*?</header>', home, re.S).group(0)
FOOTER = re.search(r'<footer class="footer closing.*?</footer>', home, re.S).group(0)
ROOT_VARS = re.search(r'<style>\n:root \{.*?\}\n</style>', home, re.S).group(0)

ARROW = '<svg class="m-arrow" viewBox="0 0 12 12" aria-hidden="true"><path class="m-arrow__stem" d="M1 6h8"/><path class="m-arrow__head" d="M4.5 2.5 8 6l-3.5 3.5"/></svg>'
CHECK = '<span class="ui-check__box"><svg viewBox="0 0 16 16"><path d="m4.5 8.2 2.3 2.3 4.7-5"/></svg></span>'


def head(title, desc, path, fragments=(), moments=(), diagram=False, css=''):
    frag = ''.join(f'<link rel="stylesheet" href="/assets/ui/{f}/fragment.css">\n' for f in fragments)
    mo = ''
    if moments:
        mo = ("<script>document.documentElement.classList.add('mo-js');setTimeout(()=>document.documentElement.classList.add('mo-safe'),2500)</script>\n"
              '<link rel="modulepreload" href="/assets/moments/moments.js">\n<link rel="modulepreload" href="/assets/moments/lib.js">\n'
              + ''.join(f'<link rel="modulepreload" href="/assets/moments/{m}/moment.js">\n' for m in moments))
    return f'''<!doctype html>
<html lang="en" data-type="software" data-radius="soft" data-ground="sky" data-buttons="solid" data-motion>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="https://aventoai.agency/share.jpg">
<meta property="og:url" content="https://aventoai.agency{path}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/images/favicon.png" type="image/png">
<meta name="theme-color" content="#ffffff">
<link rel="canonical" href="https://aventoai.agency{path}">
<meta name="site-kind" content="software">
<meta name="page-type" content="software">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Mona+Sans:wdth,wght@75..125,400..600&family=Geist+Mono:wght@400..500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/system.css">
<link rel="stylesheet" href="/assets/ui/cards.css">
<link rel="stylesheet" href="/assets/motion/motion.css">
<link rel="stylesheet" href="/assets/backgrounds/backgrounds.css">
<link rel="stylesheet" href="/assets/layout/layout.css">
<link rel="stylesheet" href="/assets/icons/icon.css">
{ROOT_VARS}
<link rel="stylesheet" href="/assets/ui/base.css">
{frag}{'<link rel="stylesheet" href="/assets/diagrams/diagram.css">' + chr(10) if diagram else ''}<link rel="stylesheet" href="/assets/site.css?v=8">
<script>document.documentElement.classList.add('m-enter');setTimeout(()=>document.documentElement.classList.add('m-enter-done'),700)</script>
<script src="/assets/backgrounds/backgrounds.js"></script>
{mo}<style>
  .panel > .frame__img, .frame > .frame__img {{ object-position: top center; }}
{css}</style>
</head>
<body>
'''


def nav(current):
    n = NAV.replace('<a class="nav__link" href="#faq">Questions</a>', '<a class="nav__link" href="/#faq">Questions</a>')
    if current:
        n = n.replace(f'<a class="nav__link" href="{current}">', f'<a class="nav__link" href="{current}" aria-current="page">', 1)
    return n


def footer(h2, line):
    f = FOOTER.replace('<a href="#faq">Questions</a>', '<a href="/#faq">Questions</a>')
    return f


TAIL = '''
<script type="module" src="/assets/system.js"></script>
<script type="module" src="/assets/motion/motion.js"></script>
<script type="module" src="/assets/layout/layout.js"></script>
<script type="module" src="/assets/diagrams/mount.js"></script>
</body>
</html>
'''


def checks(items):
    return '<ul class="checks2">' + ''.join(f'<li>{CHECK}<span>{i}</span></li>' for i in items) + '</ul>'


def shot(src, alt, url):
    host = url.split('//')[1].rstrip('/')
    return (f'<div class="shotwin"><div class="shot-bar"><span class="d-win__dots"><i></i><i></i><i></i></span><span>{host}</span></div>'
            f'<img class="shotwin__img" src="/images/shots/{src}.webp" alt="{alt}" loading="lazy" decoding="async" width="1440" height="900" data-source="client" data-subject="website"></div>')


def dg(spec):
    return f'<div class="dg" data-diagram><script type="application/json">{spec}</script></div>'


def hero(label, h1, lead, visual, second=('See our work', '/work/')):
    return f'''  <section class="hero hero--split" data-enter aria-labelledby="hero-h">
    <div class="wrap">
      <div class="hero-text grid hero-split">
        <div class="hero-copy span-5">
          <p class="hero-notice">{label}</p>
          <h1 id="hero-h">{h1}</h1>
          <p class="t-lead">{lead}</p>
          <div class="btn-row">
            <a class="btn btn--primary" href="/about/#contact">Book a free audit{ARROW}</a>
            <a class="btn btn--secondary" href="{second[1]}">{second[0]}</a>
          </div>
        </div>
        <div class="hero-visual span-7 start-6">{visual}</div>
      </div>
    </div>
  </section>
'''


SHARED_CSS = '''  .checks2 { list-style: none; margin: var(--s-6) 0 0; padding: 0; display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); column-gap: var(--s-5); }
  .checks2 li { display: flex; gap: 10px; align-items: flex-start; padding: 10px 0; border-bottom: 1px solid var(--line); font-size: 16px; line-height: 24px; }
  .checks2 .ui-check__box { flex: none; width: 20px; height: 20px; margin-top: 2px; border-radius: 6px; background: var(--ink); display: grid; place-items: center; }
  .checks2 .ui-check__box svg { width: 14px; height: 14px; fill: none; stroke: #fff; stroke-width: 1.8; stroke-linecap: round; stroke-linejoin: round; }
  .shotwin { border-radius: var(--r-lg); overflow: hidden; border: 1px solid var(--line); background: #fff; box-shadow: 0 24px 60px -30px rgb(10 10 11 / .35); }
  .shotwin .shot-bar { display: flex; align-items: center; gap: 12px; height: 36px; padding: 0 14px; border-bottom: 1px solid var(--line); font: 400 12px/1 var(--font-mono); color: var(--muted); }
  .shotwin .d-win__dots { display: flex; gap: 6px; } .shotwin .d-win__dots i { width: 9px; height: 9px; border-radius: 50%; background: #dcdfe2; }
  .shotwin__img { display: block; width: 100%; aspect-ratio: 16 / 10; object-fit: cover; }
  .hero-visual .panel { height: 100%; min-height: 440px; }
  .split-visual .panel { --p-h: 520px; }
  @media (max-width: 1023px) { .hero-visual .panel { min-height: 340px; } .split-visual .panel { --p-h: 420px; } }
  @media (max-width: 639px) { .hero-visual .shotwin__img { aspect-ratio: 2 / 1; } .checks2 { grid-template-columns: 1fr; } .checks2 li:nth-child(n+7) { display: none; } .hero-visual .panel { min-height: 260px; } .split-visual .panel { --p-h: 300px; } }
'''


def split(id_, label, h2, lead, items, visual, ground=''):
    g = f' {ground}' if ground else ''
    return f'''  <section class="section{g}" id="{id_}" aria-labelledby="{id_}-h">
    <div class="wrap">
      <div class="grid grid--top">
        <div class="span-6">
          <p class="t-label muted">{label}</p>
          <h2 id="{id_}-h">{h2}</h2>
          <p class="t-lead" style="margin-top:var(--s-5)">{lead}</p>
          {checks(items)}
        </div>
        <div class="split-visual span-6 start-7">{visual}</div>
      </div>
    </div>
  </section>
'''


def page(path, out, title, desc, current, body, close, fragments=(), moments=(), diagram=True, css=''):
    html = head(title, desc, path, fragments, moments, diagram, SHARED_CSS + css) + nav(current) + '\n\n<main id="top">\n' + body + '</main>\n\n' + footer(*close) + TAIL
    (ROOT / out).parent.mkdir(parents=True, exist_ok=True)
    (ROOT / out).write_text(html, encoding='utf-8')
    print('wrote', out)


# ---------------------------------------------------------------- SERVICES
CHAT = '''<div class="panel"><div class="stage stage--fade-b"><div class="at-rise fit" style="--fit-max:420px;--ax:max(24px, 50% - 210px);--ay:56px;--ay-sm:20px" data-ui-loop>
  <div class="ui ui-panel ui-chat" data-ui="chat">
    <div class="ui-head"><span class="ui-agent" aria-hidden="true"></span><div class="ui-title">Avento assistant · Website</div><span class="ui-chat__online">Online</span><span class="ui-spacer"></span></div>
    <div class="ui-chat__body">
      <div class="ui-chat__day">Today, 23:06</div>
      <div class="ui-msg ui-msg--me" data-chat-q><span class="ui-msg__text">Can I book a teeth cleaning this week?</span></div>
      <div class="ui-msg ui-msg--bot" data-chat-a>
        <span class="ui-agent ui-msg__av" aria-hidden="true"></span>
        <span class="ui-msg__col">
          <span class="ui-chat__typing" aria-hidden="true"><i></i><i></i><i></i></span>
          <span class="ui-chat__answer">Yes. Dr. Haddad has <b>Thursday at 9:30 or 14:00</b>. Shall I book one and send the details on WhatsApp?</span>
          <span class="ui-chat__srcs"><span class="ui-chat__src"><svg class="ui-icon" viewBox="0 0 16 16"><path d="M4 2.5h5l3 3v8H4z"/><path d="M9 2.5v3h3"/></svg>Clinic calendar</span></span>
        </span>
      </div>
    </div>
    <div class="ui-chat__input"><span class="ui-chat__ph">Write a message</span><span class="ui-chat__send" aria-hidden="true"><svg viewBox="0 0 16 16" width="14" height="14"><path d="M8 13V3.5M3.8 7.5 8 3.3l4.2 4.2" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/></svg></span></div>
  </div>
</div></div></div>'''

NOTIFY = '''<div class="panel"><div class="stage stage--fade-b"><div class="at-rise fit" style="--fit-max:400px;--ax:max(24px, 50% - 200px);--ay:64px;--ay-sm:24px">
  <div class="ui ui-notify" data-ui="notify">
    <ul class="ui-notify__list" data-notify-list>
      <li class="ui-note"><span class="ui-agent ui-note__av" aria-hidden="true"></span><span class="ui-note__text"><span class="ui-note__title">Payment gateway live<time>now</time></span><span class="ui-note__body">Card and Apple Pay on your store</span></span><span class="ui-btn ui-btn--sm ui-note__btn">Open</span></li>
      <li class="ui-note"><span class="ui-avatar ui-note__av" data-tone="5">GA</span><span class="ui-note__text"><span class="ui-note__title">Google Analytics connected<time>6m</time></span><span class="ui-note__body">Visits and enquiries now tracked</span></span></li>
      <li class="ui-note"><span class="ui-note__ico"><svg class="ui-icon" viewBox="0 0 16 16"><path d="m3.5 8.4 2.8 2.8 6.2-6.4"/></svg></span><span class="ui-note__text"><span class="ui-note__title">Domain and email set up<time>20m</time></span><span class="ui-note__body">hello@ works on your own domain</span></span></li>
      <li class="ui-note"><span class="ui-note__ico"><svg class="ui-icon" viewBox="0 0 16 16"><path d="m3.5 8.4 2.8 2.8 6.2-6.4"/></svg></span><span class="ui-note__text"><span class="ui-note__title">SEO setup finished<time>1h</time></span><span class="ui-note__body">Titles, sitemap and speed checked</span></span></li>
    </ul>
  </div>
</div></div></div>'''

HUB = dg('{"layout":"hub","alt":"Avento connects the website, WhatsApp, Instagram, HubSpot, Shopify, Stripe, OpenAI and Google Sheets into one system.","center":{"label":"Avento","icon":"ui:bot"},"spokes":[{"label":"WhatsApp","icon":"whatsapp"},{"label":"Instagram","icon":"instagram"},{"label":"HubSpot","icon":"hubspot"},{"label":"Shopify","icon":"shopify"},{"label":"Stripe","icon":"stripe"},{"label":"OpenAI","icon":"openai"},{"label":"Google Sheets","icon":"google-sheets"},{"label":"Slack","icon":"slack"}],"motion":{"cycle":3.4}}')

LANES = dg('{"layout":"lanes","size":"band","alt":"A website enquiry reaches the Avento assistant, which saves the lead to the CRM, sends a WhatsApp follow-up and notifies the sales agent at once.","input":{"label":"Website enquiry","icon":"ui:globe","sub":"Villa in Arabian Ranches"},"core":{"label":"Avento assistant","icon":"ui:bot"},"lanes":[{"label":"Lead saved","icon":"hubspot","done":true,"sub":"HubSpot · budget AED 4.2M"},{"label":"Follow-up sent","icon":"whatsapp","done":true,"sub":"Viewing options"},{"label":"Agent notified","icon":"slack","done":true,"sub":"Ready to call"}],"motion":{"cycle":3.2}}')

services_body = hero(
    'Services',
    'AI automation, websites and systems',
    'We combine AI, software development and digital strategy to help companies in Dubai work smarter and grow faster.',
    f'<div class="panel">{HUB}</div>',
    ('See the four services', '#ai-automation'),
)
services_body += split('ai-automation', '01 · AI Automation', 'AI automation that works while you sleep',
    'We connect your website, CRM, WhatsApp, email and business tools into workflows that qualify leads, answer customers and keep your team focused on closing.',
    ['AI Chatbots', 'WhatsApp Chatbots', 'Website Chatbots', 'Lead Qualification', 'Automated Follow-Ups', 'CRM Automation', 'Email Automation', 'Appointment Booking', 'Customer Support Automation', 'AI Assistants', 'Workflow Automation', 'API Automation'],
    CHAT)
services_body += f'''  <section class="section ground-inverse" id="use-case" data-moment="iris-opens" data-moment-opts='{{"from": "base"}}' aria-labelledby="use-case-h">
    <div class="wrap">
      <div class="section-head">
        <h2 id="use-case-h">A real estate enquiry, handled by automation. <span class="muted">It answers, collects the requirements, qualifies, saves the lead, follows up on WhatsApp and tells the agent.</span></h2>
      </div>
      <div class="frame fill" data-visual>{LANES}</div>
    </div>
  </section>
'''
services_body += split('web-development', '02 · Web Development', 'Websites engineered to convert',
    'Fast, accessible, conversion-led websites and stores, designed around your customer journey and built on modern, scalable technology.',
    ['Business Websites', 'Corporate Websites', 'Real Estate Websites', 'E-commerce Stores', 'Shopify Development', 'Landing Pages', 'Portfolio Websites', 'Web Applications', 'Website Redesign', 'Responsive Development', 'Website Maintenance', 'SEO-Friendly Development'],
    shot('restaurant', 'Restaurant website with menu and reservations, built by Avento AI', 'https://restaurant-website-zeta-rosy.vercel.app/'), 'ground-surface')
services_body += split('business-systems', '03 · Business Systems', 'Business systems for how you actually operate',
    'Dashboards, portals and internal tools that replace spreadsheets and manual processes with reliable software your whole team can use.',
    ['Custom CRM Systems', 'Admin Dashboards', 'Booking Platforms', 'Inventory Systems', 'Customer Portals', 'Employee Portals', 'Payment Systems', 'API Integrations', 'Internal Business Tools', 'Custom Web Applications'],
    shot('dashboard', 'Business dashboard with revenue, customers and orders, built by Avento AI', 'https://real-showcase.vercel.app/'))
services_body += split('digital-solutions', '04 · Digital Solutions', 'Everything else your business needs online',
    'Design, setup, tracking and ongoing support that make a launch successful and keep it performing.',
    ['UI/UX Design', 'Shopify Setup', 'E-commerce Setup', 'Payment Gateway Integration', 'Google Business Setup', 'Domain Setup', 'Professional Business Email', 'Google Analytics', 'Meta Pixel', 'SEO Setup', 'Website Maintenance', 'Technical Support'],
    NOTIFY, 'ground-surface')

page('/services/', 'services/index.html', 'Services: AI automation, websites and business systems | Avento AI',
     'AI chatbots, WhatsApp automation, conversion-focused websites, custom CRMs, dashboards and complete digital setup for businesses in Dubai.',
     '/services/', services_body, ('Not sure what your business needs?', 'Tell us the challenge and we recommend the right solution.'),
     fragments=('chat', 'notify'), moments=('iris-opens',),
     css='  .hero-visual .panel .dg { position: absolute; inset: 0; }\n  #use-case .frame { min-height: 0; }\n')


# ---------------------------------------------------------------- WORK
# (cat, image, name, kind, one line, tags, url)
PROJECTS = [
    ('systems ai', 'garage', 'Avento GarageOS', 'Business system · Car garages', 'Customers, vehicles, job cards, invoices and stock in one system, with AI reminders that bring customers back.', ['Business system', 'CRM', 'AI automation'], 'https://smart-garage-flow.vercel.app/'),
    ('web', 'realestate', 'Prime Property', 'Website · Real estate', 'A real estate platform that shows premium listings and turns visits into qualified leads.', ['Website', 'UI/UX', 'Lead generation'], 'https://luxury-real-estate-showcase-lemon.vercel.app/'),
    ('ai', 'ai-support', 'AI Customer Support', 'AI automation · Customer experience', 'An assistant that answers customers on WhatsApp and the website and collects leads.', ['AI chatbot', 'WhatsApp', 'CRM'], 'https://realsupport-ai.vercel.app/'),
    ('ecom uiux', 'ecommerce', 'Modern E-commerce Store', 'E-commerce · Retail and fashion', 'A Shopify store with a fast, responsive shopping experience and card payments.', ['Shopify', 'Payments', 'UI/UX'], 'https://fashion-ecommerce-store-eight.vercel.app/'),
    ('systems', 'dashboard', 'Business Dashboard', 'Business system · Operations', 'One dashboard for customers, analytics and daily operations.', ['Dashboard', 'API integrations'], 'https://real-showcase.vercel.app/'),
    ('web uiux', 'restaurant', 'Restaurant Website', 'UI/UX · Hospitality', 'Menu, reservations and location in one website that books tables.', ['Website', 'UI/UX', 'Bookings'], 'https://restaurant-website-zeta-rosy.vercel.app/'),
    ('web ai', 'dentist', 'Dental Clinic Website', 'Website · Healthcare', 'Online appointment booking, treatment pages and automatic follow-up for patient enquiries.', ['Website', 'Booking', 'Automation'], 'https://smile-book-pro.vercel.app/'),
]

ARROW_UR = '<svg class="ur" viewBox="0 0 12 12" aria-hidden="true"><path d="M3.5 8.5 8.5 3.5M4.5 3.5h4v4" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>'

tiles = ''
rows = ''
GRID_ORDER = PROJECTS[1:] + PROJECTS[:1]   # the newest (GarageOS) leads the hero, so in the grid it closes the set, across
for n, (cat, img, name, kind, line, tags, url) in enumerate(GRID_ORDER, 1):
    wide = ' wk-tile--wide' if n == len(GRID_ORDER) else ''
    tag_html = ''.join(f'<li>{t}</li>' for t in tags)
    tiles += (f'          <a class="wk-tile{wide}" data-cat="{cat}" href="{url}" target="_blank" rel="noopener">\n'
              f'            <span class="wk-tile__media"><img src="/images/shots/{img}.webp" alt="{name}, built by Avento AI" loading="{"eager" if n < 3 else "lazy"}" decoding="async" width="1440" height="900" data-source="client" data-subject="project"><span class="wk-tile__open">Open the live site {ARROW_UR}</span></span>\n'
              f'            <span class="wk-tile__meta"><span class="wk-tile__name">{name}</span><span class="wk-tile__kind">{kind}</span></span>\n'
              f'            <span class="wk-tile__line">{line}</span>\n'
              f'          </a>\n')
    rows += (f'          <a class="wk-row" data-cat="{cat}" data-preview="/images/shots/{img}.webp" href="{url}" target="_blank" rel="noopener">\n'
             f'            <span class="wk-row__n">{n:02d}</span>\n'
             f'            <span class="wk-row__name">{name}</span>\n'
             f'            <span class="wk-row__line">{line}</span>\n'
             f'            <ul class="wk-row__tags">{tag_html}</ul>\n'
             f'            <span class="wk-row__go">{ARROW_UR}</span>\n'
             f'          </a>\n')

INBOX = ('<div class="panel"><div class="stage stage--fade-b"><div class="at-rise fit" style="--fit-max:420px;--ax:max(24px, 50% - 210px);--ay:48px;--ay-sm:20px" data-ui-loop>\n'
         '  <div class="ui ui-panel ui-checks" data-ui="checklist">\n'
         '    <div class="ui-checks__head"><div class="ui-title">Leads inbox · Instagram DM</div><span class="ui-spacer"></span><div class="ui-meta" data-checks-count>2 of 6</div></div>\n'
         '    <div class="ui-checks__bar"><i data-checks-bar style="--k:0.33"></i></div>\n'
         '    <ul class="ui-checks__list">\n'
         + ''.join(f'      <li class="ui-check{done}">{CHECK}<span class="ui-check__label">{t}</span></li>\n' for done, t in [
             (' is-done', 'New enquiry: "What are your prices?"'), (' is-done', 'Qualified lead, score 92 of 100'),
             ('', 'Added to the CRM, owner assigned'), ('', 'WhatsApp follow-up delivered in 2 s'),
             ('', 'Appointment booked, tomorrow 11:00'), ('', 'Sales team notified')]) +
         '    </ul>\n  </div>\n</div></div></div>')

FILTERS = [('all', 'All work'), ('web', 'Websites'), ('ai', 'AI automation'), ('ecom', 'E-commerce'), ('systems', 'Business systems'), ('uiux', 'UI/UX')]
filter_html = ''.join(f'<button class="wk-chip" type="button" data-filter="{k}" aria-pressed="{"true" if k == "all" else "false"}">{t}<span class="wk-chip__n" data-count="{k}"></span></button>' for k, t in FILTERS)

work_body = f'''  <section class="hero hero--wk" data-enter aria-labelledby="hero-h">
    <div class="wrap">
      <div class="hero-text">
        <div class="wk-hero grid">
          <div class="span-8">
            <p class="hero-notice">Selected work · 2025 to 2026</p>
            <h1 id="hero-h">Websites, stores and AI systems <span class="muted">that are live today</span></h1>
          </div>
          <p class="t-lead span-4 wk-hero__lead">Seven projects for real estate, retail, hospitality, healthcare and garages. Open any of them and click around.</p>
        </div>
        <a class="wk-feature" href="https://smart-garage-flow.vercel.app/" target="_blank" rel="noopener" aria-label="Open Avento GarageOS, our newest system">
          <img src="/images/shots/garage.webp" alt="Avento GarageOS, a garage management system built by Avento AI" width="1440" height="900" fetchpriority="high" data-source="client" data-subject="project">
          <span class="wk-feature__tag">Newest · Avento GarageOS {ARROW_UR}</span>
        </a>
      </div>
    </div>
  </section>
  <section class="section wk" id="projects" aria-labelledby="projects-h">
    <div class="wrap">
      <div class="wk-bar">
        <h2 id="projects-h" class="wk-bar__title">All projects <span class="muted" data-total>7</span></h2>
        <div class="wk-chips" role="group" aria-label="Filter projects">{filter_html}</div>
        <div class="wk-view" role="group" aria-label="Display">
          <button type="button" class="wk-view__btn" data-view="grid" aria-pressed="true"><svg viewBox="0 0 16 16" aria-hidden="true"><rect x="2" y="2" width="5" height="5" rx="1"/><rect x="9" y="2" width="5" height="5" rx="1"/><rect x="2" y="9" width="5" height="5" rx="1"/><rect x="9" y="9" width="5" height="5" rx="1"/></svg>Grid</button>
          <button type="button" class="wk-view__btn" data-view="list" aria-pressed="false"><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M2 4h12M2 8h12M2 12h12"/></svg>List</button>
        </div>
      </div>
      <div class="wk-grid" data-panel="grid">
{tiles}      </div>
      <div class="wk-list" data-panel="list" hidden>
        <div class="wk-list__head" aria-hidden="true"><span>No.</span><span>Project</span><span>What we built</span><span>Services</span><span></span></div>
{rows}      </div>
      <img class="wk-float" alt="" aria-hidden="true" width="1440" height="900">
    </div>
  </section>
'''
work_body += split('social', 'Social media handling', 'Social media that turns followers into leads',
    'Beyond websites, we run and grow your business accounts end to end, so your pages bring in real enquiries, tracked from the first DM.',
    ['Content and page management', 'Daily posts, reels and stories', 'Audience growth strategy', 'Hashtag and local SEO', 'DM and comment handling', 'AI-assisted replies', 'Meta and Instagram ads', 'Leads sent to CRM or WhatsApp'],
    INBOX, 'ground-surface')

WORK_CSS = '''  /* hero: the headline and the newest project, big */
  .hero--wk .hero-text { display: flex; flex-direction: column; height: 100%; }
  .wk-hero { align-items: end; }
  .wk-hero h1 { font-size: clamp(40px, 5.6vw, 80px); line-height: 1.02; letter-spacing: -0.04em; max-width: 14ch; }
  .wk-hero h1 .muted { color: #a2a2a8; }
  .wk-hero__lead { margin: 0; }
  .wk-feature { position: relative; display: block; flex: 1; min-height: 0; margin-top: var(--s-6); border-radius: var(--r-lg); overflow: hidden; background: #0b1730; }
  .wk-feature img { width: 100%; height: 100%; object-fit: cover; object-position: top center; transition: transform 1s cubic-bezier(.22,1,.36,1); }
  .wk-feature:hover img { transform: scale(1.02); }
  .wk-feature__tag { position: absolute; left: 20px; bottom: 20px; display: inline-flex; align-items: center; gap: 8px; padding: 10px 16px; border-radius: 999px; background: #fff; color: var(--ink); font: 500 14px/1 var(--font-text); box-shadow: 0 10px 30px -12px rgb(0 0 0 / .4); }
  .ur { width: 12px; height: 12px; flex: none; transition: transform .35s cubic-bezier(.22,1,.36,1); }
  a:hover > .ur, a:hover .ur { transform: translate(2px, -2px); }

  /* the bar: title, filter chips, grid or list */
  .wk { height: auto !important; min-height: 100svh; }
  .wk-bar { display: grid; grid-template-columns: auto 1fr auto; align-items: center; gap: var(--s-5); padding-bottom: var(--s-5); border-bottom: 1px solid var(--line); }
  .wk-bar__title { margin: 0; font-size: 28px; letter-spacing: -0.02em; }
  .wk-chips { display: flex; flex-wrap: wrap; gap: 8px; }
  .wk-chip { display: inline-flex; align-items: center; gap: 6px; min-height: 40px; padding: 0 14px; border-radius: 999px; border: 1px solid var(--line); background: var(--bg); color: var(--ink); font: 500 14px/1 var(--font-text); cursor: pointer; transition: background-color .25s, color .25s, border-color .25s; }
  .wk-chip:hover { border-color: var(--ink); }
  .wk-chip[aria-pressed="true"] { background: var(--ink); border-color: var(--ink); color: #fff; }
  .wk-chip__n { font: 400 12px/1 var(--font-mono); opacity: .6; }
  .wk-view { display: inline-flex; padding: 4px; border-radius: 999px; background: var(--surface); }
  .wk-view__btn { display: inline-flex; align-items: center; gap: 6px; min-height: 36px; padding: 0 14px; border: 0; border-radius: 999px; background: transparent; color: var(--muted); font: 500 14px/1 var(--font-text); cursor: pointer; }
  .wk-view__btn svg { width: 14px; height: 14px; fill: none; stroke: currentColor; stroke-width: 1.5; }
  .wk-view__btn[aria-pressed="true"] { background: var(--bg); color: var(--ink); box-shadow: 0 1px 3px rgb(0 0 0 / .1); }

  /* grid view: the first project across, then two up, big pictures */
  .wk-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 56px 24px; padding-top: var(--s-7); }
  .wk-tile { display: flex; flex-direction: column; color: inherit; text-decoration: none; }
  .wk-tile--wide { grid-column: 1 / -1; }
  .wk-tile[hidden] { display: none; }
  .wk-tile__media { position: relative; display: block; aspect-ratio: 16 / 10; border-radius: var(--r-lg); overflow: hidden; background: var(--surface); border: 1px solid var(--line); }
  .wk-tile--wide .wk-tile__media { aspect-ratio: 21 / 9; }
  .wk-tile__media img { width: 100%; height: 100%; object-fit: cover; object-position: top center; transition: transform 1s cubic-bezier(.22,1,.36,1); }
  .wk-tile:hover .wk-tile__media img { transform: scale(1.03); }
  .wk-tile__open { position: absolute; right: 16px; bottom: 16px; display: inline-flex; align-items: center; gap: 8px; padding: 10px 14px; border-radius: 999px; background: #fff; color: var(--ink); font: 500 13px/1 var(--font-text);
                   opacity: 0; transform: translateY(8px); transition: opacity .3s, transform .45s cubic-bezier(.22,1,.36,1); box-shadow: 0 10px 30px -12px rgb(0 0 0 / .45); }
  .wk-tile:hover .wk-tile__open, .wk-tile:focus-visible .wk-tile__open { opacity: 1; transform: none; }
  .wk-tile__meta { display: flex; justify-content: space-between; align-items: baseline; gap: var(--s-4); margin-top: var(--s-5); }
  .wk-tile__name { font: 500 22px/1.2 var(--font-text); letter-spacing: -0.02em; }
  .wk-tile__kind { font: 400 13px/1.3 var(--font-mono); color: var(--muted); text-align: right; }
  .wk-tile__line { margin-top: 6px; font-size: 16px; line-height: 24px; color: var(--muted); max-width: 52ch; }

  /* list view: one row a project, the preview floats beside the pointer */
  .wk-list { padding-top: var(--s-5); }
  .wk-list__head, .wk-row { display: grid; grid-template-columns: 56px minmax(0, 3fr) minmax(0, 5fr) minmax(0, 3fr) 32px; gap: var(--s-5); align-items: center; }
  .wk-list__head { padding: 0 8px var(--s-3); font: 400 12px/1 var(--font-mono); color: var(--muted); text-transform: uppercase; letter-spacing: .04em; }
  .wk-row { padding: 26px 8px; border-top: 1px solid var(--line); color: inherit; text-decoration: none; transition: padding .35s cubic-bezier(.22,1,.36,1), background-color .35s; }
  .wk-row[hidden] { display: none; }
  .wk-row:hover, .wk-row:focus-visible { padding-left: 20px; background: var(--surface); }
  .wk-row__n { font: 400 13px/1 var(--font-mono); color: var(--muted); }
  .wk-row__name { font: 500 24px/1.15 var(--font-text); letter-spacing: -0.02em; }
  .wk-row:hover .wk-row__name { color: var(--accent); }
  .wk-row__line { color: var(--muted); font-size: 15px; line-height: 22px; }
  .wk-row__tags { list-style: none; margin: 0; padding: 0; display: flex; flex-wrap: wrap; gap: 6px; }
  .wk-row__tags li { padding: 5px 10px; border-radius: 999px; background: var(--surface); font-size: 13px; }
  .wk-row:hover .wk-row__tags li { background: var(--bg); }
  .wk-row__go { display: grid; place-items: center; width: 32px; height: 32px; border-radius: 50%; border: 1px solid var(--line); }
  .wk-row:hover .wk-row__go { background: var(--ink); color: #fff; border-color: var(--ink); }
  .wk-float { position: fixed; left: 0; top: 0; z-index: 30; width: 360px; height: auto; aspect-ratio: 16 / 10; object-fit: cover; object-position: top; border-radius: 14px; pointer-events: none;
              box-shadow: 0 30px 60px -20px rgb(10 10 11 / .45); opacity: 0; transform: translate3d(-9999px, 0, 0) scale(.92); transition: opacity .25s; }
  .wk-float.is-on { opacity: 1; }

  @media (max-width: 1023px) {
    .wk-bar { grid-template-columns: 1fr auto; }
    .wk-chips { grid-column: 1 / -1; grid-row: 2; }
    .wk-list__head, .wk-row { grid-template-columns: 40px minmax(0, 1fr) 32px; }
    .wk-row__line, .wk-row__tags, .wk-list__head span:nth-child(3), .wk-list__head span:nth-child(4) { display: none; }
  }
  @media (max-width: 639px) {
    .wk-hero h1 { font-size: 38px; }
    .wk-hero__lead { margin-top: var(--s-4); }
    .wk-feature { flex: 1; min-height: 240px; }
    .wk-feature__tag { left: 12px; bottom: 12px; font-size: 13px; }
    .wk-chips { overflow-x: auto; flex-wrap: nowrap; margin-inline: -24px; padding-inline: 24px; scrollbar-width: none; }
    .wk-chip { flex: none; min-height: 44px; }
    .wk-view__btn { min-height: 40px; }
    .wk-grid { grid-template-columns: 1fr; gap: 40px; }
    .wk-tile--wide .wk-tile__media { aspect-ratio: 16 / 10; }
    .wk-tile__meta { flex-direction: column; gap: 4px; }
    .wk-tile__kind { text-align: left; }
    .wk-tile__open { opacity: 1; transform: none; }
    .wk-row { padding: 20px 4px; } .wk-row__name { font-size: 19px; }
  }
  @media (prefers-reduced-motion: reduce) { .wk-tile__media img, .wk-feature img, .wk-row, .wk-float { transition: none; } }
'''

WORK_JS = '''<script>
(() => {
  const root = document.getElementById('projects');
  const items = [...root.querySelectorAll('[data-cat]')];
  const chips = [...root.querySelectorAll('.wk-chip')];
  // counts on the chips (projects per category, in the grid)
  const tiles = [...root.querySelectorAll('.wk-tile')];
  chips.forEach(c => {
    const k = c.dataset.filter;
    c.querySelector('[data-count]').textContent = k === 'all' ? tiles.length : tiles.filter(t => t.dataset.cat.split(' ').includes(k)).length;
  });
  const total = root.querySelector('[data-total]');
  chips.forEach(c => c.addEventListener('click', () => {
    chips.forEach(x => x.setAttribute('aria-pressed', String(x === c)));
    const k = c.dataset.filter;
    items.forEach(i => { i.hidden = !(k === 'all' || i.dataset.cat.split(' ').includes(k)); });
    // the first visible tile spans the row only when it is the full set
    tiles.forEach(t => t.classList.toggle('wk-tile--wide', k === 'all' && t === tiles[tiles.length - 1]));
    total.textContent = tiles.filter(t => !t.hidden).length;
  }));
  // grid or list
  const views = [...root.querySelectorAll('.wk-view__btn')];
  views.forEach(v => v.addEventListener('click', () => {
    views.forEach(x => x.setAttribute('aria-pressed', String(x === v)));
    root.querySelectorAll('[data-panel]').forEach(p => { p.hidden = p.dataset.panel !== v.dataset.view; });
  }));
  // list view: the project's screen follows the pointer (mouse only, not under reduced motion)
  const float = root.querySelector('.wk-float');
  const fine = matchMedia('(hover: hover) and (pointer: fine)').matches && !matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (!fine) return;
  let x = 0, y = 0, cx = 0, cy = 0, raf = 0, on = false;
  const tick = () => {
    cx += (x - cx) * 0.18; cy += (y - cy) * 0.18;
    float.style.transform = `translate3d(${cx + 28}px, ${cy - 110}px, 0) scale(${on ? 1 : .92})`;
    raf = on || Math.abs(x - cx) > .5 ? requestAnimationFrame(tick) : 0;
  };
  const hide = () => { on = false; float.classList.remove('is-on'); };
  addEventListener('scroll', hide, { passive: true });
  root.querySelector('.wk-list').addEventListener('pointerleave', hide);
  root.querySelectorAll('.wk-row').forEach(r => {
    r.addEventListener('pointerenter', e => {
      if (e.pointerType !== 'mouse') return;
      float.src = r.dataset.preview;
      if (!on) { cx = x = e.clientX; cy = y = e.clientY; }
      on = true; float.classList.add('is-on');
      if (!raf) raf = requestAnimationFrame(tick);
    });
    r.addEventListener('pointerleave', () => { on = false; float.classList.remove('is-on'); });
    r.addEventListener('pointermove', e => { x = e.clientX; y = e.clientY; if (!raf) raf = requestAnimationFrame(tick); });
  });
})();
</script>
'''

page('/work/', 'work/index.html', 'Our work: websites, stores and AI automation projects | Avento AI',
     'Websites, digital platforms and automation we have built for real estate, e-commerce, hospitality, healthcare and garages.',
     '/work/', work_body, ('Want results like these?', 'Tell us what you are building and we show you how we would approach it.'),
     fragments=('checklist',), diagram=False, css=WORK_CSS)
_w = (ROOT / 'work/index.html').read_text(encoding='utf-8')
(ROOT / 'work/index.html').write_text(_w.replace('</body>', WORK_JS + '</body>'), encoding='utf-8')


# ---------------------------------------------------------------- ABOUT
VALUES = [('ui:lightbulb', 'Innovation', 'We keep exploring modern technology and AI, and bring what works to your business.'),
          ('ui:shield-check', 'Quality', 'We build reliable, professional software that keeps running after launch.'),
          ('ui:message-square', 'Transparency', 'Clear communication through every project, from the first call to support.'),
          ('ui:trending-up', 'Growth', 'The goal is not just to deliver a project, but to help your business grow.')]
INDUSTRIES = [('ui:house', 'Real Estate'), ('ui:stethoscope', 'Clinics and Dental'), ('ui:utensils', 'Restaurants and Cafés'),
              ('ui:shopping-bag', 'E-commerce and Retail'), ('ui:briefcase', 'Professional Services'), ('ui:graduation-cap', 'Education and Coaching')]

def ic(id_):
    name = id_.split(':')[1]
    return f'<img class="ic" data-icon="{id_}" src="/assets/icons/ui-{name}.svg" alt="" width="24" height="24">'

AUDIT = '''<div class="panel"><div class="stage"><div class="at-rise fit" style="--fit-max:420px;--ax:max(24px, 50% - 210px);--ay:56px;--ay-sm:24px" data-ui-loop>
  <div class="ui ui-panel ui-checks" data-ui="checklist">
    <div class="ui-checks__head"><div class="ui-title">Growth audit · your-company.ae</div><span class="ui-spacer"></span><div class="ui-meta" data-checks-count>1 of 4</div></div>
    <div class="ui-checks__bar"><i data-checks-bar style="--k:0.25"></i></div>
    <ul class="ui-checks__list">
      <li class="ui-check is-done">''' + CHECK + '''<span class="ui-check__label">Speed, mobile and SEO health check</span></li>
      <li class="ui-check">''' + CHECK + '''<span class="ui-check__label">Where enquiries are being lost</span></li>
      <li class="ui-check">''' + CHECK + '''<span class="ui-check__label">2 to 3 automations that save the most hours</span></li>
      <li class="ui-check">''' + CHECK + '''<span class="ui-check__label">A roadmap with priority, effort and impact</span></li>
    </ul>
  </div>
</div></div></div>'''

about_body = hero('About us', 'A technology agency in Dubai',
    'Avento AI helps businesses use AI, software and modern digital solutions to improve how they operate and grow.',
    shot('ai-support', 'AI customer support system built by Avento AI', 'https://realsupport-ai.vercel.app/'), ('Get in touch', '#contact'))
about_body += '''  <section class="section" id="mission" data-moment="word-highlight" aria-labelledby="mission-h">
    <div class="wrap">
      <h2 id="mission-h" class="t-label muted">Our mission for business</h2>
      <p class="mo-wh__text">We make advanced technology accessible to businesses of every size, so they can move away from outdated manual work and build <strong>faster, smarter systems</strong> that scale with them.</p>
    </div>
  </section>
  <section class="section ground-surface" id="values" aria-labelledby="values-h">
    <div class="wrap">
      <div class="section-head"><h2 id="values-h">What we believe in business. <span class="muted">Four principles behind every project we take on.</span></h2></div>
      <div class="grid fill values">
''' + ''.join(f'        <article class="card m-nolift span-3"><span class="ic-tile">{ic(i)}</span><h3>{t}</h3><p>{d}</p></article>\n' for i, t, d in VALUES) + '''      </div>
    </div>
  </section>
  <section class="section" id="audit" aria-labelledby="audit-h">
    <div class="wrap">
      <div class="grid grid--top">
        <div class="span-5 stack-4">
          <p class="t-label muted">Free growth audit</p>
          <h2 id="audit-h">A free audit of your website and lead flow</h2>
          <p class="t-lead">Before you spend anything, we review what you have, show you where customers drop off and which parts can be automated. No obligation, no sales pressure.</p>
          <p>Delivered within 48 hours, usually the same day.</p>
          <p><a class="link" href="#contact">Request my free audit</a></p>
        </div>
        <div class="split-visual span-6 start-7">''' + AUDIT + '''</div>
      </div>
    </div>
  </section>
  <section class="section ground-surface" id="industries" aria-labelledby="industries-h">
    <div class="wrap">
      <div class="section-head"><h2 id="industries-h">Industries we work with. <span class="muted">We know how these businesses win customers, so we start with flows that work.</span></h2></div>
      <div class="grid industries">
''' + ''.join(f'        <div class="industry span-4"><span class="ic-tile">{ic(i)}</span><span>{t}</span></div>\n' for i, t in INDUSTRIES) + '''      </div>
      <p class="t-lead" style="margin-top:var(--s-7)">Not on the list? We have built systems for niche businesses too. Tell us what you do and we will map it out.</p>
    </div>
  </section>
  <section class="section" id="contact-form" aria-labelledby="contact-h">
    <div class="wrap">
      <div class="grid grid--top">
        <div class="span-5 stack-4">
          <p class="t-label muted">Contact</p>
          <h2 id="contact-h">Tell us about your business project</h2>
          <p class="t-lead">We reply with a clear recommendation and next steps, usually within one business day.</p>
          <ul class="contact-list">
            <li><span class="ic-tile">''' + ic('ui:mail') + '''</span><a class="link" href="mailto:hello@aventoai.agency">hello@aventoai.agency</a></li>
            <li><span class="ic-tile">''' + ic('ui:map-pin') + '''</span><span>Dubai, UAE</span></li>
            <li><span class="ic-tile"><img class="ic" data-icon="instagram" src="/assets/icons/instagram.svg" alt="" width="24" height="24"></span><a class="link" href="https://www.instagram.com/avento.ai_agency/" target="_blank" rel="noopener">@avento.ai_agency</a></li>
          </ul>
        </div>
        <form class="form span-6 start-7" action="mailto:hello@aventoai.agency" method="post" enctype="text/plain" data-endpoint="" novalidate>
          <div class="form-grid">
            <div class="field"><label for="f-name">Full name</label>
              <input id="f-name" name="name" type="text" autocomplete="name" required aria-describedby="f-name-err">
              <p class="field__error" id="f-name-err" hidden>Write your name so we know who to reply to.</p></div>
            <div class="field"><label for="f-company">Company name</label>
              <input id="f-company" name="company" type="text" autocomplete="organization"></div>
            <div class="field"><label for="f-email">Email</label>
              <input id="f-email" name="email" type="email" autocomplete="email" inputmode="email" required aria-describedby="f-email-err">
              <p class="field__error" id="f-email-err" hidden>Write an email address with an @, like name@company.ae.</p></div>
            <div class="field"><label for="f-phone">Phone or WhatsApp</label>
              <input id="f-phone" name="phone" type="tel" autocomplete="tel" inputmode="tel"></div>
            <div class="field"><label for="f-service">Service interested in</label>
              <select id="f-service" name="service" required aria-describedby="f-service-err">
                <option value="">Select a service</option><option>Free growth audit</option><option>AI Automation</option><option>Website Development</option><option>E-commerce</option><option>Business Systems</option><option>UI/UX Design</option><option>Other</option>
              </select>
              <p class="field__error" id="f-service-err" hidden>Pick the service closest to what you need.</p></div>
            <div class="field"><label for="f-budget">Budget range</label>
              <select id="f-budget" name="budget">
                <option value="">Select a range</option><option>Under AED 5,000</option><option>AED 5,000 to 10,000</option><option>AED 10,000 to 25,000</option><option>AED 25,000 to 50,000</option><option>AED 50,000+</option>
              </select></div>
            <div class="field field--full"><label for="f-message">Project description</label>
              <textarea id="f-message" name="message" rows="4" required aria-describedby="f-message-err"></textarea>
              <p class="field__error" id="f-message-err" hidden>Tell us in a sentence or two what you want to build.</p></div>
          </div>
          <div class="btn-row"><button class="btn btn--primary" type="submit">Send project request</button></div>
          <p class="form__status" role="status" data-form-status></p>
        </form>
      </div>
    </div>
  </section>
'''
page('/about/', 'about/index.html', 'About Avento AI: a technology agency in Dubai',
     'A Dubai-based technology agency helping businesses use AI, software and modern digital solutions to improve how they operate and grow.',
     '/about/', about_body, ('Book a free audit of your lead flow', 'Delivered within 48 hours, usually the same day.'),
     fragments=('checklist',), moments=('word-highlight',), diagram=False,
     css='''  .values .card h3 { margin-top: var(--s-6); }
  .values .card p { margin-top: var(--s-2); }
  .values .ic-tile, .industry .ic-tile, .contact-list .ic-tile { --tile: 44px; }
  .industries { row-gap: var(--s-4); margin-top: var(--s-2); }
  .industry { display: flex; align-items: center; gap: var(--s-4); padding: var(--s-5); border: 1px solid var(--line); border-radius: var(--r-lg); background: var(--bg); font: 500 18px/1.3 var(--font-text); }
  .contact-list { list-style: none; margin: var(--s-4) 0 0; padding: 0; display: grid; gap: var(--s-3); }
  .contact-list li { display: flex; align-items: center; gap: var(--s-4); }
  .form-grid { grid-column: 1 / -1; display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: var(--s-4) var(--s-5); }
  #contact .form > .btn-row, #contact .form > .form__status { grid-column: 1 / -1; }
  .field--full { grid-column: 1 / -1; }
  #contact .form { max-width: none; width: 100%; }
  .form-grid .field { min-width: 0; }
  .form-grid .field :is(input, select, textarea) { width: 100%; box-sizing: border-box; }
  #contact-form .form .btn-row { margin-top: var(--s-5); }
  @media (max-width: 639px) { .form-grid { grid-template-columns: 1fr; } #contact { --hm: 2; } .values .card p { display: none; } }
''')
# the old site's links all point to /about#contact: keep that address landing on the form
about = (ROOT / 'about/index.html').read_text(encoding='utf-8')
about = about.replace('id="contact-form"', 'id="contact"', 1).replace('<footer class="footer closing av-foot" id="contact"', '<footer class="footer closing av-foot" id="closing"')
about = about.replace('class="btn btn--primary" href="/about/#contact"', 'class="btn btn--primary" href="#contact"').replace('<li><a href="/about/#contact"><span class="av-foot__a">', '<li><a href="#contact"><span class="av-foot__a">')
(ROOT / 'about/index.html').write_text(about, encoding='utf-8')


# ---------------------------------------------------------------- LEGAL
def legal(path, out, title, h1, sections, close):
    body = f'''  <section class="hero hero--legal" data-enter aria-labelledby="hero-h">
    <div class="wrap"><div class="hero-text legal">
      <p class="hero-notice">Last updated: November 2026</p>
      <h1 id="hero-h">{h1}</h1>
{sections}
    </div></div>
  </section>
'''
    page(path, out, title, f'{h1} for the Avento AI website and services.', '', body, close, diagram=False,
         css='''  .hero--legal { height: auto !important; min-height: 100svh; padding-bottom: var(--s-9); }
  .legal { max-width: 760px; }
  .legal h2 { font-size: 24px; margin: var(--s-7) 0 var(--s-3); }
  .legal p, .legal li { font-size: 17px; line-height: 28px; margin: 0 0 var(--s-3); }
  .legal ul { padding-left: 20px; }
''')

legal('/privacy/', 'privacy/index.html', 'Privacy policy | Avento AI', 'Privacy policy', '''      <p>Avento AI Solutions ("Avento AI", "we") is based in Dubai, UAE. This policy explains what information we collect through aventoai.agency and how we use it.</p>
      <h2>Information we collect</h2>
      <ul><li>What you send us through the contact form or by email: your name, company, email, phone, the service you are interested in, your budget range and your project description.</li><li>Basic technical data such as browser, device and pages visited, when analytics are enabled on the site.</li></ul>
      <h2>How we use it</h2>
      <ul><li>To reply to your enquiry and prepare the proposals or audits you ask for.</li><li>To deliver and support the projects we work on together.</li><li>To improve our website and services.</li></ul>
      <p>We do not sell your personal information.</p>
      <h2>Sharing</h2>
      <p>We share information only with service providers that help us run our business, such as email and hosting providers, and only as needed to provide our services or where the law requires it.</p>
      <h2>Keeping it</h2>
      <p>We keep enquiry and project information only as long as needed for these purposes or as required by law.</p>
      <h2>Your rights</h2>
      <p>To access, correct or delete what we hold about you, email <a class="link" href="mailto:hello@aventoai.agency">hello@aventoai.agency</a>.</p>''',
      ('Questions about your data?', 'Email hello@aventoai.agency and we reply within one business day.'))

legal('/terms/', 'terms/index.html', 'Terms and conditions | Avento AI', 'Terms and conditions', '''      <p>These terms apply to your use of aventoai.agency, run by Avento AI Solutions in Dubai, UAE. By using this website you agree to them.</p>
      <h2>Use of the website</h2>
      <p>The content here is general information about our services. Do not copy or reuse it without our written permission.</p>
      <h2>Projects and services</h2>
      <p>Every project is covered by its own written proposal or agreement, which sets the scope, timeline, price and payment terms. Where it differs from these terms, the agreement applies.</p>
      <h2>Portfolio</h2>
      <p>The projects shown are examples of our work. Links to live demos are for reference and may change.</p>
      <h2>Other websites</h2>
      <p>This website links to other sites and platforms. We are not responsible for their content or privacy practices.</p>
      <h2>Liability</h2>
      <p>We work to keep this website accurate and available, but provide it as it is and are not liable for loss arising from its use.</p>
      <h2>Governing law</h2>
      <p>These terms are governed by the laws of the United Arab Emirates and the Emirate of Dubai.</p>''',
      ('Questions about these terms?', 'Email hello@aventoai.agency and we reply within one business day.'))
