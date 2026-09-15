#!/usr/bin/env python3
"""Assembles the arya.wtf v2 preview: 8 static pages from shared chrome.
Preview files are flat (log.html, log-elux-headcount.html); the production
routes in sitemap/llms.txt use the final URL shape (/log/, /log/<slug>)."""
import json, os, datetime
OUT = os.path.dirname(os.path.abspath(__file__))
SITE = "https://arya.wtf"
TODAY = "2026-09-15"
IDENT = ("Founder of Elux Space, an AI-native design studio in Yogyakarta. "
         "I help owners decide what AI should automate, what it should assist, and what it should never touch.")
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Unbounded:wght@700;800&family=Archivo:wght@400;500;600&family=Space+Mono:wght@400;700&display=swap">')

SUN = '''<svg class="sunmark" viewBox="0 0 100 100" aria-hidden="true"><defs><linearGradient id="{id}g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFB347"/><stop offset=".6" stop-color="#F26A2E"/><stop offset="1" stop-color="#C0397A"/></linearGradient><mask id="{id}m"><circle cx="50" cy="50" r="50" fill="#fff"/><rect x="0" y="58" width="100" height="1.5" fill="#000"/><rect x="0" y="66" width="100" height="2.2" fill="#000"/><rect x="0" y="73" width="100" height="2.9" fill="#000"/><rect x="0" y="79" width="100" height="3.6" fill="#000"/><rect x="0" y="84" width="100" height="4.3" fill="#000"/><rect x="0" y="89" width="100" height="5" fill="#000"/></mask></defs><circle cx="50" cy="50" r="50" fill="url(#{id}g)" mask="url(#{id}m)"/></svg>'''

NAV = [("index.html","/","Home"),("about.html","/about","Record"),("method.html","/method","Method"),
       ("work.html","/work","Work"),("log.html","/log","Log"),("hire.html","/hire","Hire"),("now.html","/now","Now")]

def head(title, desc, path, jsonld, skeleton=False):
    canon = SITE + path
    og = SITE + "/img/og.jpg"
    core = (f'<title>{title}</title>'
            f'<meta name="description" content="{desc}">'
            f'<link rel="canonical" href="{canon}">'
            f'<meta property="og:type" content="website"><meta property="og:title" content="{title}"><meta property="og:description" content="{desc}">'
            f'<meta property="og:url" content="{canon}"><meta property="og:image" content="{og}"><meta property="og:site_name" content="arya.wtf">'
            f'<meta name="twitter:card" content="summary_large_image">'
            f'<link rel="stylesheet" href="styles.css">' + FONTS +
            f'<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>')
    if skeleton:
        return core
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
            + core + '</head><body>')

def mast(current):
    CUR = ' aria-current="page"'
    links = "".join(f'<a href="{f}"{CUR if f==current else ""}>{n}</a>' for f,_,n in NAV)
    return (f'<div class="grain" aria-hidden="true"></div><div class="page"><header class="mast">'
            f'<a class="brand" href="index.html" aria-label="arya.wtf, home">{SUN.format(id="b")}arya<em>.</em>wtf</a>'
            f'<nav aria-label="Primary">{links}</nav></header><main>')

def foot(skeleton=False):
    html = (f'</main><footer class="foot"><p class="ident"><b>Arya Pradana.</b> {IDENT}</p>'
            '<ul><li><a href="https://www.linkedin.com/in/aryapradana/" rel="me">linkedin.com/in/aryapradana</a></li>'
            '<li><a href="https://github.com/arya-wtf" rel="me">github.com/arya-wtf</a></li>'
            '<li><a href="https://elux.space">elux.space</a></li></ul>'
            '<p class="col">Set in Unbounded, Archivo and Space Mono. Looks like a 1979 airbrushed paperback cover on purpose. '
            'The portrait and plates were painted from a photograph of Arya; the halftone and grain are code. Nothing else moves.</p>'
            '<p class="edu">S1 Teknik Informatika, Institut Teknologi Sepuluh Nopember 2006–2011 · S2 Business, SBM Institut Teknologi Bandung 2016–2018 · Yogyakarta, Indonesia · Why? Think further.</p>'
            '</footer></div>')
    return html if skeleton else html + '</body></html>'

def sec_head(coord, h2, aside, hid):
    return f'<div class="sec-head"><span class="coord">{coord}</span><h2 id="{hid}">{h2}</h2><div class="aside">{aside}</div></div>'

PERSON = {"@type":"Person","@id":SITE+"/#person","name":"Arya Pradana","url":SITE+"/","image":SITE+"/img/hero.webp",
          "jobTitle":"Founder","description":IDENT,"worksFor":{"@id":"https://elux.space/#organization"},
          "alumniOf":[{"@type":"CollegeOrUniversity","name":"Institut Teknologi Sepuluh Nopember"},
                      {"@type":"CollegeOrUniversity","name":"Sekolah Bisnis dan Manajemen, Institut Teknologi Bandung"}],
          "homeLocation":{"@type":"Place","name":"Yogyakarta, Indonesia"},
          "knowsAbout":["AI adoption in small businesses","Design studio operations","UI/UX design","Software development"],
          "sameAs":["https://www.linkedin.com/in/aryapradana/","https://github.com/arya-wtf","https://elux.space"]}
ORG = {"@type":"Organization","@id":"https://elux.space/#organization","name":"Elux Space","url":"https://elux.space",
       "founder":{"@id":SITE+"/#person"},"foundingDate":"2022-02","location":{"@type":"Place","name":"Yogyakarta, Indonesia"}}
WEBSITE = {"@type":"WebSite","@id":SITE+"/#website","url":SITE+"/","name":"arya.wtf","publisher":{"@id":SITE+"/#person"},"inLanguage":"en"}
def graph(*extra): return {"@context":"https://schema.org","@graph":[PERSON,ORG,WEBSITE,*extra]}

pages = {}

# ---------------------------------------------------------------- HOME
pages["index.html"] = head("Arya Pradana", IDENT, "/", graph(
    {"@type":"ProfilePage","@id":SITE+"/#profilepage","url":SITE+"/","mainEntity":{"@id":SITE+"/#person"},"dateModified":TODAY}), skeleton=True) + mast("index.html") + f'''
<section class="hero g" aria-labelledby="h1" style="padding-top:calc(var(--b)*4)">
  <div class="floor" aria-hidden="true"></div>
  <figure class="art plate" style="margin:0;--ht-dir:left">
    <img src="img/hero.webp" width="1600" height="1066" alt="Arya Pradana in chrome headphones, painted as a 1979 paperback cover, a striped sun setting over a grid behind him." fetchpriority="high">
  </figure>
  <div class="copy">
    <p class="why rise">{SUN.format(id="h")} Why? Think further.</p>
    <h1 id="h1" class="rise">Building software companies since <em class="sun-text">2008</em>. The current one is four people doing what eighteen used&nbsp;to.</h1>
    <p class="ident rise"><b>{IDENT.split('. ')[0]}.</b> {IDENT.split('. ',1)[1]}</p>
    <div class="routes rise"><a class="btn sun" href="hire.html">Hire me</a><a class="btn" href="about.html">Read the record</a></div>
  </div>
</section>

<div class="strip" role="list" aria-label="At a glance">
  <div role="listitem"><div class="v" data-count="2008">2008</div><div class="k">First company, at university</div></div>
  <div role="listitem"><div class="v" data-count="5">5</div><div class="k">Companies built or run</div></div>
  <div role="listitem"><div class="v" data-count="50">50</div><div class="k">People at DOT, as COO</div></div>
  <div role="listitem"><div class="v">18 → 12 → <i>4</i></div><div class="k">Elux Space, 2023 → 2026</div></div>
  <div role="listitem"><div class="v">Jogja</div><div class="k">Yogyakarta, Indonesia</div></div>
</div>

<section class="g" aria-labelledby="h-method">
  <div class="sec">
    {sec_head("01 · Method", "Every piece of work gets one of three verdicts", "The whole practice<br>in one question", "h-method")}
    <div class="sec-body">
      <p class="lede span-7">Most owners ask <b>“what can AI do for us?”</b> That question has no edges, so the answer is always “everything,” and the project dies of scope. I ask a narrower one: for <em>this</em> piece of work, which pile does it belong in? <a href="method.html" style="color:var(--sun-1)">How the three verdicts work →</a></p>
    </div>
    <div class="verdicts">
      <div class="verdict" data-v="automate"><span class="tag">Verdict 1</span><h3>Automate</h3><p>Repetitive, well-defined, low-judgment. A human touching it adds cost, not quality.</p></div>
      <div class="verdict" data-v="assist"><span class="tag">Verdict 2</span><h3>Assist</h3><p>Judgment stays with a person; the machine drafts, checks and accelerates. Most real work lives here.</p></div>
      <div class="verdict" data-v="leave"><span class="tag">Verdict 3</span><h3>Leave alone</h3><p>The work <em>is</em> the relationship, the taste, or the accountability. Automating it removes the reason the client pays you.</p></div>
    </div>
  </div>
</section>

<section class="g" aria-labelledby="h-record">
  <div class="sec">
    {sec_head("02 · Record", "Eighteen years, two sides", "2008 → now", "h-record")}
    <div class="sec-body">
      <div class="span-6 prose">
        <p>Started a hosting and software company in the third year of university. Ran a fifty-person company as COO for five years — sales, funding, then admin, legal, finance and HR, then the business model. Left it in 2020. Built a video production house. Founded a design studio in 2022, grew it to eighteen, and then took it down to four on purpose — with revenue unchanged through the last step.</p>
        <p><a class="btn" href="about.html">The full record</a></p>
      </div>
      <div class="span-4" style="align-self:end">
        <div class="curve"><span>18</span><span class="arrow">→</span><span>12</span><span class="arrow">→</span><span class="four">4</span></div>
        <p class="curve-note">Elux Space headcount, 2023 → 2026.</p>
      </div>
    </div>
  </div>
</section>

<section class="g" aria-labelledby="h-log">
  <div class="sec">
    {sec_head("03 · Log", "Verdicts, with the numbers attached", "One a week, at most", "h-log")}
    <div class="list">
      <div class="row">
        <span class="id">2026-09</span>
        <a class="name" href="log-elux-headcount.html">The studio’s own headcount<small>Elux Space · own work</small></a>
        <p class="desc">Eighteen to twelve to four. What was automated, what was assisted, and what was left alone — and the part that wasn’t about tools at all.</p>
        <span class="meta"><span class="pill v-assist">Assist</span> <span class="pill draft">Draft</span></span>
      </div>
    </div>
    <div class="sec-body"><p class="lede span-7">Every entry follows the same eight fields, and the rule is simple: <b>no number, no entry.</b> <a href="log.html" style="color:var(--sun-1)">The log →</a></p></div>
  </div>
</section>

<section class="g" aria-labelledby="h-work">
  <div class="sec">
    {sec_head("04 · Work", "Built, shipped, still running", "Own builds + the studio", "h-work")}
    <div class="list">
      <div class="row"><span class="id">2026</span><a class="name" href="https://github.com/arya-wtf/arya-taste">arya-taste<small>Open source · skill</small></a><p class="desc">An anti-slop frontend method for coding agents. Twelve committed styles, six textures, eight bug classes that ship silently.</p><span class="meta">GitHub</span></div>
      <div class="row"><span class="id">2026</span><a class="name" href="https://github.com/arya-wtf/vimemory">vimemory<small>Open source · MCP</small></a><p class="desc">A Python memory MCP server, with a local variant and a remote Cloudflare Worker.</p><span class="meta">GitHub</span></div>
      <div class="row"><span class="id">2026</span><a class="name" href="https://github.com/arya-wtf/esflowsbeta">Esflows<small>Product · beta</small></a><p class="desc">Node-based AI image studio on Cloudflare. Next.js 16, React Flow.</p><span class="meta">GitHub</span></div>
    </div>
    <div class="sec-body"><p class="lede span-7"><a href="work.html" style="color:var(--sun-1)">All work, including the studio’s →</a></p></div>
  </div>
</section>

<section class="g" aria-labelledby="h-hire">
  <div class="sec">
    {sec_head("05 · Hire", "Two ways in", "One is me.<br>One is the studio.", "h-hire")}
    <div class="offers">
      <div class="offer me"><span class="kick">Hire me</span><div style="display:grid;gap:14px"><h3>An AI decision audit, for owners</h3><p>I go through your actual work and sort it into the three piles, with the reasoning written down so it survives me leaving the room.</p><p class="price">From <b>IDR 10,000,000</b></p></div><a class="btn sun" href="hire.html">How it works</a></div>
      <div class="offer team"><span class="kick">Hire the team</span><div style="display:grid;gap:14px"><h3>Product and UI/UX design, by Elux Space</h3><p>The four-person studio the record describes. Scope, quotes and the work itself live on the studio’s own site.</p><p class="price">Quoted per project</p></div><a class="btn" href="https://elux.space">elux.space</a></div>
    </div>
  </div>
</section>
''' + foot(skeleton=True)

# ---------------------------------------------------------------- ABOUT
pages["about.html"] = head("The Record — Arya Pradana", "Eighteen years of building software companies in Indonesia, from a university hosting business in 2008 to a four-person AI-native design studio in Yogyakarta.", "/about",
    graph({"@type":"ProfilePage","@id":SITE+"/about#profilepage","url":SITE+"/about","mainEntity":{"@id":SITE+"/#person"},"dateModified":TODAY},
          {"@type":"FAQPage","mainEntity":[
            {"@type":"Question","name":"Where is Arya Pradana based?","acceptedAnswer":{"@type":"Answer","text":"Yogyakarta, Indonesia. Elux Space is remote-first and based there."}},
            {"@type":"Question","name":"Which Arya Pradana is this?","acceptedAnswer":{"@type":"Answer","text":"The founder of Elux Space, a design studio in Yogyakarta; ITS Teknik Informatika 2006–2011; SBM ITB 2016–2018; former COO of DOT Indonesia. Several people share the name; this page is about this one."}},
            {"@type":"Question","name":"What did Arya Pradana do before Elux Space?","acceptedAnswer":{"@type":"Answer","text":"Founded IDOnesoft in 2008 while at university, was CEO of AyoWes! Web & Mobile Dev 2013–2015, COO of DOT Indonesia 2015–2020, and ran Incbuss Creative, a video production house, 2020–2024."}}]})) + mast("about.html") + f'''
<section class="phero g" aria-labelledby="h1">
  <figure class="plate" style="margin:0"><img src="img/about.webp" width="1200" height="675" alt="A road of light running toward a chrome city under a striped setting sun." loading="eager"></figure>
  <div class="head"><span class="kick sun">The record · 2008 → 2026</span><h1 id="h1">Eighteen years, two sides</h1>
    <p class="lede">A timeline, not a résumé. Every line has a year. <b>Side A</b> is building for other people’s companies. <b>Side B</b> is building smaller, on purpose.</p></div>
  <div class="side" style="grid-column:9/13">Side A · 2006 — 2020<br>Side B · 2020 — now</div>
</section>

<section class="g" aria-labelledby="h-a">
  <div class="sec">
    <div class="side">
      <div class="label" id="h-a">Side<br>A<small>2006 — 2020</small></div>
      <div class="tracks">
        <div class="track"><span class="yr">2006–2011</span><div class="who">Institut Teknologi Sepuluh Nopember<small>S1 · Teknik Informatika</small></div><p class="what">Informatics engineering, Surabaya.</p></div>
        <div class="track"><span class="yr">2008</span><div class="who">IDOnesoft<small>Founder</small></div><p class="what">Hosting and software development, started in the third year of university. <b>The first company.</b></p></div>
        <div class="track"><span class="yr">2013–2015</span><div class="who">AyoWes! Web &amp; Mobile Dev<small>CEO</small></div><p class="what">A web and mobile development studio.</p></div>
        <div class="track"><span class="yr">2015–2020</span><div class="who">DOT Indonesia<small>COO · ~50 people</small></div><p class="what">The role rotated as the company needed it. <b>First</b> sales and raising investment. <b>Then</b> admin, legal, finance and HR. <b>Then</b> the business model itself. Five years inside every function that breaks when you automate it carelessly.</p></div>
        <div class="track"><span class="yr">2016–2018</span><div class="who">SBM ITB<small>S2 · Business</small></div><p class="what">Business school, Bandung — taken while running operations at DOT.</p></div>
        <div class="track"><span class="yr">2020</span><div class="who">Left DOT<small>End of Side A</small></div><p class="what">There were three of us. One partner went into politics, and the company started being run for that. I didn’t want to run it that way, so I left.</p></div>
      </div>
    </div>
    <div class="side">
      <div class="label" id="h-b">Side<br>B<small>2020 — now</small></div>
      <div class="tracks">
        <div class="track"><span class="yr">2020–2024</span><div class="who">Incbuss Creative<small>Founder · video production</small></div><p class="what">Long-form video, produced and edited in-house. The creative turn. Passive since 2025.</p></div>
        <div class="track"><span class="yr">Feb 2022</span><div class="who">Elux Space<small>Founder · CEO</small></div><p class="what">A UI/UX and product design studio in Yogyakarta, remote-first from day one.</p></div>
        <div class="track"><span class="yr">2023–2024</span><div class="who">Eighteen people<small>Peak</small></div><p class="what">The studio at its largest.</p></div>
        <div class="track"><span class="yr">2025</span><div class="who">Twelve<small>Reduced</small></div><p class="what">The year before the rebuild.</p></div>
        <div class="track"><span class="yr now">2026</span><div class="who">Four<small>Now</small></div><p class="what"><b>Revenue unchanged from 2025.</b> Rebuilt around AI instead of hiring around it. The uncomfortable part: that took decisions about people, not just tools. <a href="log-elux-headcount.html" style="color:var(--sun-1)">The entry →</a></p></div>
      </div>
    </div>
    <div class="sec-body">
      <div class="span-4"><div class="curve"><span>18</span><span class="arrow">→</span><span>12</span><span class="arrow">→</span><span class="four">4</span></div><p class="curve-note">Headcount at Elux Space, 2023 → 2026. The revenue claim applies to the last step only.</p></div>
    </div>
  </div>
</section>

<section class="g" aria-labelledby="h-faq">
  <div class="sec">
    {sec_head("Disambiguation", "Which Arya Pradana is this?", "There are several", "h-faq")}
    <div class="faq">
      <details open><summary>Which Arya Pradana is this?</summary><div class="a">The founder of Elux Space, a design studio in Yogyakarta. ITS Teknik Informatika 2006–2011, SBM ITB 2016–2018, former COO of DOT Indonesia. Several people share the name — a film producer, a musician, and others in tech. This site is about this one.</div></details>
      <details><summary>Where is he based?</summary><div class="a">Yogyakarta, Indonesia. Not Malang, not Jakarta. Elux Space is remote-first and based there.</div></details>
      <details><summary>What did he do before Elux Space?</summary><div class="a">Founded IDOnesoft in 2008 while at university; CEO of AyoWes! Web &amp; Mobile Dev, 2013–2015; COO of DOT Indonesia, 2015–2020; founded Incbuss Creative, a video production house, 2020–2024.</div></details>
    </div>
  </div>
</section>
''' + foot()

# ---------------------------------------------------------------- METHOD
pages["method.html"] = head("Three Verdicts — what AI should automate, assist, or leave alone", "A method for owners deciding what AI should do in their business: sort every piece of work into automate, assist, or leave alone. By Arya Pradana.", "/method",
    graph({"@type":"Article","@id":SITE+"/method#article","headline":"Every piece of work gets one of three verdicts","author":{"@id":SITE+"/#person"},"datePublished":TODAY,"dateModified":TODAY,"url":SITE+"/method","inLanguage":"en"},
          {"@type":"FAQPage","mainEntity":[
            {"@type":"Question","name":"What is the difference between automate and assist?","acceptedAnswer":{"@type":"Answer","text":"Automate removes the person from the loop; assist keeps the person's judgment and uses the machine to draft, check and speed up. Most failed AI projects tried to automate work that should have been assisted."}},
            {"@type":"Question","name":"Why leave anything alone?","acceptedAnswer":{"@type":"Answer","text":"Because some work is the reason the client pays you — the relationship, the taste, the accountability. Automating it removes the value rather than the cost."}},
            {"@type":"Question","name":"Do you use AI to write the verdicts?","acceptedAnswer":{"@type":"Answer","text":"To draft, yes. The verdict itself — the decision and the refusal — is written by a person. Automate the work, never the voice."}}]})) + mast("method.html") + f'''
<section class="phero g" aria-labelledby="h1">
  <figure class="plate" style="margin:0"><img src="img/method.webp" width="1200" height="675" alt="Three chrome spheres of different sizes on a dark grid, the smallest cracked open with warm light inside." loading="eager"></figure>
  <div class="head"><span class="kick sun">The method</span><h1 id="h1">What should AI automate? Three verdicts.</h1>
    <p class="lede">Most owners ask <b>“what can AI do for us?”</b> That question has no edges, so the answer is always “everything,” and the project dies of scope. The narrower question is the useful one: for <em>this</em> piece of work, which pile does it belong in?</p></div>
  <div class="side" style="grid-column:9/13">One question,<br>asked on every task</div>
</section>

<section class="g" aria-labelledby="h-three">
  <div class="sec">
    {sec_head("01", "The three piles", "In order of how often<br>people get them wrong", "h-three")}
    <div class="verdicts">
      <div class="verdict" data-v="automate"><span class="tag">Verdict 1</span><h3>Automate</h3><p>Repetitive, well-defined, low-judgment. A human touching it adds cost, not quality. Build the pipeline and remove the person from the loop.</p>
        <ul><li>The input is structured or can be made structured</li><li>A wrong output is cheap to catch</li><li>Nobody’s name is on the result</li></ul></div>
      <div class="verdict" data-v="assist"><span class="tag">Verdict 2</span><h3>Assist</h3><p>Judgment stays with a person; the machine drafts, checks and accelerates. Most real work lives here — and most failed AI projects tried to push it into the first pile.</p>
        <ul><li>A person still signs off</li><li>The first draft is the expensive part</li><li>Speed matters more than perfection</li></ul></div>
      <div class="verdict" data-v="leave"><span class="tag">Verdict 3</span><h3>Leave alone</h3><p>The work <em>is</em> the relationship, the taste, or the accountability. Automating it removes the reason the client pays you. This pile is usually the one that saves the business.</p>
        <ul><li>The client is buying a person’s judgment</li><li>A mistake costs trust, not money</li><li>It’s the thing competitors can’t copy</li></ul></div>
    </div>
  </div>
</section>

<section class="g" aria-labelledby="h-why">
  <div class="sec">
    {sec_head("02", "Why the third pile matters most", "The uncomfortable part", "h-why")}
    <div class="sec-body">
      <div class="prose span-7">
        <p>Every tool vendor is paid to grow the first pile. Nobody is paid to grow the third. So in most small companies the pressure runs one way, and the work that made the company worth hiring gets automated first — because it’s visible, and because it looks expensive.</p>
        <p>The studio I run went from eighteen people to four with revenue unchanged through the last step. That wasn’t because we automated the most. It was because we were specific about what we <b>refused</b> to automate, and put the remaining people there.</p>
        <p>That’s why every verdict on this site has a field called <b>“what I refused to automate.”</b> A verdict without a refusal is a sales pitch.</p>
      </div>
    </div>
  </div>
</section>

<section class="g" aria-labelledby="h-fields">
  <div class="sec">
    {sec_head("03", "How a verdict is written", "Eight fields, no exceptions", "h-fields")}
    <dl class="fields">
      <div><dt>01</dt><dd>The work</dd></div><div><dt>02</dt><dd>Figure before</dd></div><div><dt>03</dt><dd>Verdict</dd></div><div><dt>04</dt><dd>What I refused to automate</dd></div>
      <div><dt>05</dt><dd>Result</dd></div><div><dt>06</dt><dd>The uncomfortable part</dd></div><div><dt>07</dt><dd>Tools</dd></div><div><dt>08</dt><dd>Date · revised</dd></div>
    </dl>
    <div class="sec-body"><p class="rule-line span-10">No number, <i>no entry.</i> No refusal named, <i>entry unfinished.</i></p></div>
  </div>
</section>

<section class="g" aria-labelledby="h-faq">
  <div class="sec">
    {sec_head("04", "Questions", "Asked often enough<br>to answer once", "h-faq")}
    <div class="faq">
      <details open><summary>What is the difference between automate and assist?</summary><div class="a">Automate removes the person from the loop. Assist keeps the person’s judgment and uses the machine to draft, check and speed up. Most failed AI projects tried to automate work that should have been assisted — the output looked fine until someone’s name was on it.</div></details>
      <details><summary>Why leave anything alone?</summary><div class="a">Because some work is the reason the client pays you — the relationship, the taste, the accountability. Automating it removes the value, not the cost. The third pile is where the business actually is.</div></details>
      <details><summary>Do you use AI to write the verdicts?</summary><div class="a">To draft, yes. The verdict itself — the decision and the refusal — is written by a person. Automate the work, never the voice.</div></details>
      <details><summary>Does this apply outside design studios?</summary><div class="a">The three piles do. The specific verdicts don’t transfer — a logistics company’s third pile looks nothing like a studio’s. That’s why an audit goes through <em>your</em> work, not a template.</div></details>
    </div>
  </div>
</section>
''' + foot()

# ---------------------------------------------------------------- WORK
WORK = [
 ("2026","arya-taste","Open source · agent skill","An anti-slop frontend method for coding agents. Twelve committed styles, six textures, eight bug classes that ship silently. Works across 70+ agents.","https://github.com/arya-wtf/arya-taste","GitHub"),
 ("2026","vimemory","Open source · MCP server","A Python memory MCP server, with a local variant and a remote Cloudflare Worker.","https://github.com/arya-wtf/vimemory","GitHub"),
 ("2026","Esflows","Product · beta","Node-based AI image studio on Cloudflare. Next.js 16, React Flow.","https://github.com/arya-wtf/esflowsbeta","GitHub"),
 ("2026","mrktelx","Internal tool","Sales commission and deal approval for a small studio.","https://github.com/arya-wtf/mrktelx","GitHub"),
 ("2025–","OpenClaw","Open source · infrastructure","AI infrastructure for a small team — each person gets their own agent, on a self-hosted server.","","In progress"),
 ("2025–","ERPS","Internal platform","The studio’s own ERP: project tracker, HR, money — folded into one Next.js monolith.","","Internal"),
]
rows = "".join(
    f'<div class="row"><span class="id">{y}</span>' + (f'<a class="name" href="{u}">{n}<small>{k}</small></a>' if u else f'<div class="name">{n}<small>{k}</small></div>') +
    f'<p class="desc">{d}</p><span class="meta">{m}</span></div>' for y,n,k,d,u,m in WORK)
pages["work.html"] = head("Work — Arya Pradana", "Software and tools built by Arya Pradana: open-source agent skills, MCP servers, an AI image studio, and the internal platform behind Elux Space.", "/work",
    graph({"@type":"CollectionPage","@id":SITE+"/work#collection","url":SITE+"/work","name":"Work","dateModified":TODAY,
           "mainEntity":{"@type":"ItemList","itemListElement":[{"@type":"ListItem","position":i+1,"item":{"@type":"SoftwareSourceCode","name":n,"description":d,**({"codeRepository":u} if u else {}),"author":{"@id":SITE+"/#person"}}} for i,(y,n,k,d,u,m) in enumerate(WORK)]}})) + mast("work.html") + f'''
<section class="phero g" aria-labelledby="h1">
  <figure class="plate" style="margin:0"><img src="img/work.webp" width="1200" height="675" alt="A hand-built radio dish on terraced hillside at dusk, tilted toward a striped orange sun." loading="eager"></figure>
  <div class="head"><span class="kick sun">Work</span><h1 id="h1">Built, shipped, still running</h1>
    <p class="lede">Two kinds of work. <b>Own builds</b> — tools I ship as a first-class output, not a side effect. And <b>the studio’s work</b>, which lives where the studio does.</p></div>
  <div class="side" style="grid-column:9/13">Small, fast, shipped</div>
</section>

<section class="g" aria-labelledby="h-own">
  <div class="sec">
    {sec_head("01", "Own builds", "Public unless marked", "h-own")}
    <div class="list">{rows}</div>
    <div class="sec-body"><p class="lede span-7">A long tail of landing pages, dashboards and single-file tools sits behind these on <a href="https://github.com/arya-wtf" style="color:var(--sun-1)">github.com/arya-wtf</a>.</p></div>
  </div>
</section>

<section class="g" aria-labelledby="h-studio">
  <div class="sec">
    {sec_head("02", "The studio’s work", "Elux Space", "h-studio")}
    <div class="sec-body">
      <div class="prose span-7">
        <p>Client projects, case studies and the team are on the studio’s own site. This page doesn’t duplicate them — one place for the work, one place for the person who runs it.</p>
        <p><a class="btn" href="https://elux.space">Client work on elux.space</a></p>
      </div>
    </div>
  </div>
</section>
''' + foot()

# ---------------------------------------------------------------- HIRE
pages["hire.html"] = head("Hire — AI decision audit for owners, from IDR 10,000,000", "Hire Arya Pradana for an AI decision audit — a sort of your actual work into automate, assist and leave alone — from IDR 10,000,000. Or hire the Elux Space team for product and UI/UX design.", "/hire",
    graph({"@type":"Service","@id":SITE+"/hire#audit","name":"AI decision audit","serviceType":"Consulting","provider":{"@id":SITE+"/#person"},"areaServed":"Indonesia","url":SITE+"/hire",
           "description":"A sort of an owner's actual work into three piles — automate, assist, leave alone — with the reasoning written down.",
           "offers":{"@type":"Offer","priceSpecification":{"@type":"PriceSpecification","price":"10000000","priceCurrency":"IDR","minPrice":"10000000"},"availability":"https://schema.org/InStock"}},
          {"@type":"FAQPage","mainEntity":[
            {"@type":"Question","name":"Who is the audit for?","acceptedAnswer":{"@type":"Answer","text":"Owners of small companies who are being sold AI and want a decision, not a demo."}},
            {"@type":"Question","name":"What do I get?","acceptedAnswer":{"@type":"Answer","text":"Your work sorted into automate, assist and leave alone, with the reasoning written down and the refusals named."}},
            {"@type":"Question","name":"Is this the same as hiring Elux Space?","acceptedAnswer":{"@type":"Answer","text":"No. The audit is Arya, alone. Elux Space is the four-person design studio, quoted per project on elux.space."}}]})) + mast("hire.html") + f'''
<section class="phero g" aria-labelledby="h1">
  <figure class="plate" style="margin:0"><img src="img/hire.webp" width="1200" height="675" alt="A tall signal beacon sending one orange beam into a cobalt night sky, two figures at its base." loading="eager"></figure>
  <div class="head"><span class="kick sun">Hire</span><h1 id="h1">Two ways in</h1>
    <p class="lede">One is me. One is the studio. They are priced differently, scoped differently, and they don’t compete — the audit decides <em>what</em> to build; the studio builds it.</p></div>
  <div class="side" style="grid-column:9/13">Audit · from IDR 10,000,000<br>Studio · per project</div>
</section>

<section class="g" aria-labelledby="h-offers">
  <div class="sec">
    <div class="offers">
      <div class="offer me"><span class="kick">Hire me</span>
        <div style="display:grid;gap:16px"><h3 id="h-offers">An AI decision audit, for owners</h3>
          <p>I go through your actual work — not a deck about it — and sort it into the three piles. You leave with:</p>
          <ul><li>Every recurring piece of work, with its verdict: automate, assist, or leave alone</li><li>The reasoning for each, written down so it survives me leaving the room</li><li>The refusals — the things I’d tell you <em>not</em> to automate, and why</li></ul>
          <p class="price">From <b>IDR 10,000,000</b></p></div>
        <a class="btn sun" href="https://www.linkedin.com/in/aryapradana/">Message me on LinkedIn</a></div>
      <div class="offer team"><span class="kick">Hire the team</span>
        <div style="display:grid;gap:16px"><h3>Product and UI/UX design, by Elux Space</h3>
          <p>The four-person studio the record describes. Design and build for products that have to ship. Scope, quotes and the work itself live on the studio’s own site.</p>
          <p class="price">Quoted per project</p></div>
        <a class="btn" href="https://elux.space">Go to elux.space</a></div>
    </div>
  </div>
</section>

<section class="g" aria-labelledby="h-faq">
  <div class="sec">
    {sec_head("Questions", "Before you message", "Short answers", "h-faq")}
    <div class="faq">
      <details open><summary>Who is the audit for?</summary><div class="a">Owners of small companies who are being sold AI and want a decision, not a demo. If you already know exactly what to build, you don’t need this — go to the studio.</div></details>
      <details><summary>What do I get?</summary><div class="a">Your work sorted into automate, assist and leave alone, with the reasoning written down and the refusals named. The format is the same eight fields every entry in <a href="log.html" style="color:var(--sun-1)">the log</a> uses, so you can see what you’re buying before you buy it.</div></details>
      <details><summary>Is this the same as hiring Elux Space?</summary><div class="a">No. The audit is me, alone. Elux Space is the four-person design studio, quoted per project on elux.space. The audit often ends with a list of things worth building; the studio is one of the places you could build them.</div></details>
    </div>
  </div>
</section>
''' + foot()

# ---------------------------------------------------------------- LOG INDEX
pages["log.html"] = head("The Log — verdicts, with the numbers attached", "Dated verdict entries by Arya Pradana: one real piece of work, sorted into automate, assist or leave alone, with the figure before, the result, and what was refused.", "/log",
    graph({"@type":"CollectionPage","@id":SITE+"/log#collection","url":SITE+"/log","name":"The Log","dateModified":TODAY,
           "mainEntity":{"@type":"ItemList","itemListElement":[{"@type":"ListItem","position":1,"url":SITE+"/log/elux-headcount"}]}})) + mast("log.html") + f'''
<section class="phero g" aria-labelledby="h1">
  <figure class="plate" style="margin:0"><img src="img/log.webp" width="1200" height="675" alt="A vintage line printer in a dark control room spooling a long ribbon of blank paper." loading="eager"></figure>
  <div class="head"><span class="kick sun">The log</span><h1 id="h1">Verdicts, with the numbers attached</h1>
    <p class="lede">Two kinds of unit. <b>Entries</b> are long: one real piece of work, sorted, with the figure before and after and the thing I refused to automate. <b>Notes</b> are a paragraph: something seen this week that changes a verdict, or should. Notes are allowed to be wrong. Entries are not.</p></div>
  <div class="side" style="grid-column:9/13">One entry a week, at most<br>Each on its own page</div>
</section>

<section class="g" aria-labelledby="h-entries">
  <div class="sec">
    {sec_head("Entries", "All entries", "Newest first", "h-entries")}
    <div class="list">
      <div class="row">
        <span class="id">2026-09-15</span>
        <a class="name" href="log-elux-headcount.html">The studio’s own headcount<small>Elux Space · own work</small></a>
        <p class="desc">Eighteen to twelve to four. What was automated, what was assisted, and what was left alone — and the part that wasn’t about tools at all.</p>
        <span class="meta"><span class="pill v-assist">Assist</span> <span class="pill draft">Draft</span></span>
      </div>
    </div>
    <div class="sec-body"><p class="lede span-7">Entry 01 — a teardown of a well-known Indonesian designer’s site — is written and awaiting publication clearance. It will appear here when it does.</p></div>
  </div>
</section>

<section class="g" aria-labelledby="h-fields">
  <div class="sec">
    {sec_head("Format", "Every entry, the same eight fields", "So they can be compared", "h-fields")}
    <dl class="fields">
      <div><dt>01</dt><dd>The work</dd></div><div><dt>02</dt><dd>Figure before</dd></div><div><dt>03</dt><dd>Verdict</dd></div><div><dt>04</dt><dd>What I refused to automate</dd></div>
      <div><dt>05</dt><dd>Result</dd></div><div><dt>06</dt><dd>The uncomfortable part</dd></div><div><dt>07</dt><dd>Tools</dd></div><div><dt>08</dt><dd>Date · revised</dd></div>
    </dl>
    <div class="sec-body"><p class="rule-line span-10">No number, <i>no entry.</i> No refusal named, <i>entry unfinished.</i></p></div>
  </div>
</section>
''' + foot()

# ---------------------------------------------------------------- LOG ENTRY (draft)
pages["log-elux-headcount.html"] = head("The studio’s own headcount — a verdict", "Elux Space went from eighteen people to twelve to four, with revenue unchanged through the last step. What was automated, what was assisted, what was left alone.", "/log/elux-headcount",
    graph({"@type":"Article","@id":SITE+"/log/elux-headcount#article","headline":"The studio’s own headcount","author":{"@id":SITE+"/#person"},"datePublished":TODAY,"dateModified":TODAY,"url":SITE+"/log/elux-headcount","inLanguage":"en","about":{"@id":"https://elux.space/#organization"},"isPartOf":{"@id":SITE+"/log#collection"}})) + mast("log.html") + f'''
<section class="g" aria-labelledby="h1" style="padding-top:calc(var(--b)*6)">
  <div class="sec">
    <div class="sec-body" style="grid-column:1/-1">
      <div class="span-10" style="display:grid;gap:16px">
        <p class="kick sun">Entry · 2026-09-15 · <span class="pill v-assist">Assist</span> <span class="pill draft">Draft — Arya to finish</span></p>
        <h1 id="h1" style="font-size:clamp(30px,4.4vw,60px);line-height:.98;text-transform:uppercase;letter-spacing:-.03em">The studio’s own headcount</h1>
        <p class="lede">Eighteen people in 2023–24. Twelve in 2025. Four in 2026, with revenue unchanged from 2025. This is the entry the whole site rests on, so it goes first — and it is the one with the most uncomfortable part.</p>
      </div>
    </div>
    <div class="entry">
      <dl class="spec">
        <div><dt>01 · The work</dt><dd>Running a UI/UX and product design studio, Yogyakarta</dd></div>
        <div><dt>02 · Figure before</dt><dd>18 people (2023–24) · 12 (2025)</dd></div>
        <div><dt>03 · Verdict</dt><dd>Assist — for most of the studio’s work. Automate for a narrow set. Leave alone for the part clients actually pay for.</dd></div>
        <div><dt>04 · Refused to automate</dt><dd>Client relationships. Design judgment. Who signs off.</dd></div>
        <div><dt>05 · Result</dt><dd>4 people in 2026. Revenue unchanged from 2025.</dd></div>
        <div><dt>06 · Uncomfortable part</dt><dd>The decisions were about people before they were about tools.</dd></div>
        <div><dt>07 · Tools</dt><dd>Claude, Claude Code, OpenClaw, a self-hosted server, ERPS</dd></div>
        <div><dt>08 · Date · revised</dt><dd>2026-09-15 · —</dd></div>
      </dl>
      <div class="body">
        <div class="prose">
          <div class="callout"><b>Draft.</b> The fields on the left are real. The body below is a structure for Arya to fill in his own words — what went into each pile, and why. Nothing here names a person.</div>
          <h2>What went into “automate”</h2>
          <p>The work where a person touching it added cost, not quality: the parts of production with structured input and a cheap way to catch a wrong output. <em>Arya: list them, with the before-and-after where there is a number.</em></p>
          <h2>What went into “assist”</h2>
          <p>Most of it. First drafts, checks, the parts where the expensive step was the blank page and the decision still needed a name on it. <em>Arya: which functions, and what the person still does.</em></p>
          <h2>What was left alone</h2>
          <p>Client relationships. Design judgment. Sign-off. The four people who remain sit here, because this is the pile clients pay for and the one a competitor can’t copy with the same tools.</p>
          <h2>The uncomfortable part</h2>
          <p>The number on this page is fourteen people who aren’t at the studio any more. The tooling made the smaller studio possible; it didn’t make the decisions. <em>Arya: say what you’re willing to say about that, and nothing about anyone in particular.</em></p>
        </div>
      </div>
    </div>
  </div>
</section>
''' + foot()

# ---------------------------------------------------------------- NOW
pages["now.html"] = head("Now — Arya Pradana", "What Arya Pradana is working on right now, dated. Updated when it changes.", "/now",
    graph({"@type":"WebPage","@id":SITE+"/now#page","url":SITE+"/now","name":"Now","dateModified":TODAY,"about":{"@id":SITE+"/#person"}})) + mast("now.html") + f'''
<section class="g" aria-labelledby="h1" style="padding-top:calc(var(--b)*6)">
  <div class="sec">
    <div class="sec-body" style="grid-column:1/-1">
      <div class="span-10" style="display:grid;gap:16px">
        <p class="kick sun">Now · updated {TODAY}</p>
        <h1 id="h1" style="font-size:clamp(30px,4.4vw,60px);line-height:.98;text-transform:uppercase;letter-spacing:-.03em">What I’m doing this quarter</h1>
        <p class="lede">A dated page, so nothing here pretends to be permanent.</p>
      </div>
    </div>
    <div class="list" style="grid-column:1/-1">
      <div class="row"><span class="id">Studio</span><div class="name">Elux Space at four people</div><p class="desc">Running the studio at its current size. Revenue unchanged from 2025. No hiring planned.</p><span class="meta">Ongoing</span></div>
      <div class="row"><span class="id">Audit</span><div class="name">AI decision audits, open</div><p class="desc">From IDR 10,000,000. Taking them one at a time. <a href="hire.html" style="color:var(--sun-1)">Details →</a></p><span class="meta">Open</span></div>
      <div class="row"><span class="id">Video</span><div class="name">A YouTube channel, in Bahasa Indonesia</div><p class="desc">Filming two a week, publishing one. It goes public when six are banked and I’d send three of them to a stranger.</p><span class="meta">In production</span></div>
      <div class="row"><span class="id">Site</span><div class="name">This site</div><p class="desc">Built in September 2026. The log starts with the studio’s own headcount; Entry 01 is written and awaiting clearance.</p><span class="meta">v2</span></div>
      <div class="row"><span class="id">Product</span><div class="name">Deferred</div><p class="desc">A product decision waits until early 2027, on signal from the channel and the audits — not on a date.</p><span class="meta">~Feb 2027</span></div>
    </div>
  </div>
</section>
''' + foot()

# ---------------------------------------------------------------- machine files
for name, html in pages.items():
    with open(os.path.join(OUT, name), "w") as f: f.write(html)

routes = ["/","/about","/method","/work","/log","/log/elux-headcount","/hire","/now"]
with open(os.path.join(OUT,"sitemap.xml"),"w") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' +
            "".join(f'<url><loc>{SITE}{r}</loc><lastmod>{TODAY}</lastmod></url>' for r in routes) + '</urlset>')
with open(os.path.join(OUT,"robots.txt"),"w") as f:
    f.write(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
with open(os.path.join(OUT,"llms.txt"),"w") as f:
    f.write(f"""# arya.wtf

> {IDENT}

Arya Pradana. Yogyakarta, Indonesia. Building software companies since 2008. Founder and CEO of Elux Space (Feb 2022–), a UI/UX and product design studio that went from 18 people (2023–24) to 12 (2025) to 4 (2026) with revenue unchanged from 2025. Former COO of DOT Indonesia (2015–2020, ~50 people). S1 Teknik Informatika, ITS (2006–2011). S2 Business, SBM ITB (2016–2018).

## Method
- [Three verdicts]({SITE}/method): every piece of work is sorted into automate, assist, or leave alone.

## Pages
- [The record]({SITE}/about): the 18-year timeline, Side A (2006–2020) and Side B (2020–now).
- [Work]({SITE}/work): own builds — arya-taste, vimemory, Esflows, mrktelx, OpenClaw, ERPS.
- [The log]({SITE}/log): dated verdict entries with eight fixed fields. Rule: no number, no entry.
- [Hire]({SITE}/hire): AI decision audit for owners, from IDR 10,000,000. Elux Space team quoted per project on https://elux.space.
- [Now]({SITE}/now): what he is doing this quarter, dated.

## Identity
- LinkedIn: https://www.linkedin.com/in/aryapradana/
- GitHub: https://github.com/arya-wtf
- Studio: https://elux.space
- Not the film producer, musician, or other people who share the name.
""")
print("built", len(pages), "pages")
