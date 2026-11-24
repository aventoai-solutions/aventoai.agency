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
{frag}{'<link rel="stylesheet" href="/assets/diagrams/diagram.css">' + chr(10) if diagram else ''}<link rel="stylesheet" href="/assets/site.css">
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
    f = re.sub(r'<h2 id="close-h">.*?</h2>', f'<h2 id="close-h">{h2}</h2>', f, 1, flags=re.S)
    f = re.sub(r'(<h2 id="close-h">.*?</h2>\s*<p>).*?(</p>)', lambda m: m.group(1) + line + m.group(2), f, count=1, flags=re.S)
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
  @media (max-width: 639px) { .checks2 { grid-template-columns: 1fr; } .checks2 li:nth-child(n+7) { display: none; } .hero-visual .panel { min-height: 260px; } .split-visual .panel { --p-h: 300px; } }
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
PROJECTS = [
    ('web', 'realestate', 'Prime Property', 'Web Development · Real Estate', 'A real estate platform built to showcase premium properties and generate qualified leads.', 'React · Next.js · CRM API', 'https://luxury-real-estate-showcase-lemon.vercel.app/'),
    ('ecom', 'ecommerce', 'Modern E-commerce Store', 'E-commerce · Retail and Fashion', 'A high-converting online store with a modern, responsive shopping experience.', 'Shopify · Stripe · Liquid', 'https://fashion-ecommerce-store-eight.vercel.app/'),
    ('ai', 'ai-support', 'AI Customer Support', 'AI Automation · Customer Experience', 'An AI support system that responds to customers and collects leads automatically.', 'OpenAI · Python · WhatsApp API', 'https://realsupport-ai.vercel.app/'),
    ('systems', 'dashboard', 'Business Dashboard', 'Business Systems · Operations', 'A custom dashboard for managing customers, analytics and daily operations.', 'React · Node.js · PostgreSQL', 'https://real-showcase.vercel.app/'),
    ('uiux web', 'restaurant', 'Restaurant Website', 'UI/UX · Hospitality', 'A restaurant website with menu display, reservations and location integration.', 'React · Maps API · Reservations', 'https://restaurant-website-zeta-rosy.vercel.app/'),
    ('web', 'dentist', 'Dental Clinic Website', 'Web Development · Healthcare and Dental', 'Online appointment booking, treatment pages and patient enquiry automation.', 'Next.js · Booking API · GA4', 'https://smile-book-pro.vercel.app/'),
    ('systems ai', 'garage', 'Avento GarageOS', 'Business Systems · Car Garages', 'Customers, vehicles, jobs, invoices, appointments and stock in one system, with AI reminders and follow-ups.', 'Next.js · React · PostgreSQL · AI', 'https://smart-garage-flow.vercel.app/'),
]

cards = ''
for cat, img, name, kind, line, stack, url in PROJECTS:
    cards += f'''        <a class="card card--row card--open span-4 proj" data-cat="{cat}" href="{url}" target="_blank" rel="noopener">
          <p class="t-label muted">{kind}</p>
          <h3>{name if name.endswith('Website') else name + ' website'}</h3>
          <p>{line}</p>
          <div class="panel"><img class="frame__img" src="/images/shots/{img}.webp" alt="{name}, built by Avento AI" loading="lazy" decoding="async" width="1440" height="900" data-source="client" data-subject="website"></div>
          <p class="proj__stack">{stack}</p>
        </a>
'''
cards = cards.replace('span-4 proj" data-cat="systems ai"', 'span-8 proj proj--wide" data-cat="systems ai"')
cards += '''        <a class="card card--row card--open span-4 proj proj--next" data-cat="web ai ecom systems uiux" href="/about/#contact">
          <p class="t-label muted">Your business · Dubai</p>
          <h3>Your project next</h3>
          <p>Tell us what you want to build. We reply with a clear plan, usually within one business day.</p>
          <div class="panel"><div class="next-tools" aria-hidden="true">
            <span class="ic-tile"><img class="ic" src="/assets/icons/whatsapp.svg" alt="" width="28" height="28"></span>
            <span class="ic-tile"><img class="ic" src="/assets/icons/shopify.svg" alt="" width="28" height="28"></span>
            <span class="ic-tile"><img class="ic" src="/assets/icons/openai.svg" alt="" width="28" height="28"></span>
            <span class="ic-tile"><img class="ic" src="/assets/icons/instagram.svg" alt="" width="28" height="28"></span>
            <span class="ic-tile"><img class="ic" src="/assets/icons/google-sheets.svg" alt="" width="28" height="28"></span>
            <span class="ic-tile"><img class="ic" src="/assets/icons/slack.svg" alt="" width="28" height="28"></span>
          </div></div>
          <p class="proj__stack">Start with a free audit</p>
        </a>
'''
cards = cards.replace('Avento GarageOS website', 'Avento GarageOS system').replace('AI Customer Support website', 'AI Customer Support system').replace('Business Dashboard website', 'Business Dashboard system').replace('Modern E-commerce Store website', 'Modern E-commerce Store')

INBOX = '''<div class="panel"><div class="stage stage--fade-b"><div class="at-rise fit" style="--fit-max:420px;--ax:max(24px, 50% - 210px);--ay:48px;--ay-sm:20px" data-ui-loop>
  <div class="ui ui-panel ui-checks" data-ui="checklist">
    <div class="ui-checks__head"><div class="ui-title">Leads inbox · Instagram DM</div><span class="ui-spacer"></span><div class="ui-meta" data-checks-count>2 of 6</div></div>
    <div class="ui-checks__bar"><i data-checks-bar style="--k:0.33"></i></div>
    <ul class="ui-checks__list">
      <li class="ui-check is-done">''' + CHECK + '''<span class="ui-check__label">New enquiry: "What are your prices?"</span></li>
      <li class="ui-check is-done">''' + CHECK + '''<span class="ui-check__label">Qualified lead, score 92 of 100</span></li>
      <li class="ui-check">''' + CHECK + '''<span class="ui-check__label">Added to the CRM, owner assigned</span></li>
      <li class="ui-check">''' + CHECK + '''<span class="ui-check__label">WhatsApp follow-up delivered in 2 s</span></li>
      <li class="ui-check">''' + CHECK + '''<span class="ui-check__label">Appointment booked, tomorrow 11:00</span></li>
      <li class="ui-check">''' + CHECK + '''<span class="ui-check__label">Sales team notified</span></li>
    </ul>
  </div>
</div></div></div>'''

work_body = hero('Our work', 'Websites, stores and AI systems we have built',
    'Explore the websites, digital platforms and automation we have created for real estate, retail, hospitality, healthcare and garages. Every project below is live.',
    shot('garage', 'Avento GarageOS, a garage management system built by Avento AI', 'https://smart-garage-flow.vercel.app/'), ('See all projects', '#projects'))
work_body += f'''  <section class="section" id="projects" style="--h: 2" aria-labelledby="projects-h">
    <div class="wrap">
      <div class="section-head">
        <h2 id="projects-h">Seven live projects</h2>
        <div class="filters" role="group" aria-label="Filter projects">
          <button class="filter" type="button" data-filter="all" aria-pressed="true">All</button>
          <button class="filter" type="button" data-filter="web" aria-pressed="false">Web</button>
          <button class="filter" type="button" data-filter="ai" aria-pressed="false">AI Automation</button>
          <button class="filter" type="button" data-filter="ecom" aria-pressed="false">E-commerce</button>
          <button class="filter" type="button" data-filter="systems" aria-pressed="false">Systems</button>
          <button class="filter" type="button" data-filter="uiux" aria-pressed="false">UI/UX</button>
        </div>
      </div>
      <div class="grid proj-grid">
{cards}      </div>
    </div>
  </section>
'''
work_body += split('social', 'Social media handling', 'Social media that turns followers into leads',
    'Beyond websites, we run and grow your business accounts end to end, so your pages bring in real enquiries, tracked from the first DM.',
    ['Content and page management', 'Daily posts, reels and stories', 'Audience growth strategy', 'Hashtag and local SEO', 'DM and comment handling', 'AI-assisted replies', 'Meta and Instagram ads', 'Leads sent to CRM or WhatsApp'],
    INBOX, 'ground-surface')

page('/work/', 'work/index.html', 'Our work: websites, stores and AI automation projects | Avento AI',
     'Websites, digital platforms and automation we have built for real estate, e-commerce, hospitality, healthcare and garages.',
     '/work/', work_body, ('Want results like these?', 'Tell us what you are building and we show you how we would approach it.'),
     fragments=('checklist',), diagram=False,
     css='''  #projects .panel { --p-h: 180px; }
  .proj .t-label { margin: 0 0 var(--s-2); }
  .proj__stack { margin-top: var(--s-4); font: 400 13px/1.3 var(--font-mono); color: var(--muted); }
  .proj.is-hidden { display: none; }
  .filters { display: flex; flex-direction: row; flex-wrap: wrap; gap: 8px; margin-top: var(--s-5); }
  .next-tools { position: absolute; inset: 0; display: flex; flex-wrap: wrap; align-content: center; justify-content: center; gap: 12px; padding: 24px; }
  .next-tools .ic-tile { --tile: 52px; }
  .filter { min-height: 44px; padding: 0 16px; border-radius: 999px; border: 1px solid var(--line); background: var(--bg); color: var(--ink); font: 500 14px/1 var(--font-text); cursor: pointer; }
  .filter[aria-pressed="true"] { background: var(--ink); color: var(--bg); border-color: var(--ink); }
  #projects .proj-grid { row-gap: var(--s-6); }
  #projects .card--row p:not(.t-label):not(.proj__stack) { display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
  @media (max-width: 1279px) { #projects { --h: auto !important; height: auto; min-height: 200svh; } }
  @media (max-width: 639px) {
    #projects { --hm: 2; }
    #projects .proj-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 20px 12px; }
    #projects .proj { grid-column: auto !important; }
    #projects .panel { --p-h: 104px; }
    #projects .proj p:not(.t-label), #projects .proj .t-label { display: none; }
    #projects .proj h3 { font-size: 15px; line-height: 20px; }
    .filters .filter { min-height: 44px; padding: 0 12px; font-size: 13px; }
  }
''')

# filter script: tiny, page-only (the kit has no filter part)
work = (ROOT / 'work/index.html').read_text(encoding='utf-8')
work = work.replace('</body>', '''<script>
document.querySelectorAll('.filter').forEach(b => b.addEventListener('click', () => {
  document.querySelectorAll('.filter').forEach(x => x.setAttribute('aria-pressed', String(x === b)));
  const f = b.dataset.filter;
  document.querySelectorAll('.proj').forEach(p => p.classList.toggle('is-hidden', f !== 'all' && !p.dataset.cat.split(' ').includes(f)));
}));
</script>
</body>''')
(ROOT / 'work/index.html').write_text(work, encoding='utf-8')


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
about = about.replace('id="contact-form"', 'id="contact"', 1).replace('<footer class="footer closing footer--statement" id="contact"', '<footer class="footer closing footer--statement" id="closing"')
about = about.replace('href="/about/#contact" class="btn', 'href="#contact" class="btn')
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
