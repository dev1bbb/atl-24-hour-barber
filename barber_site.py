#!/usr/bin/env python3
"""
Atlanta's 24 Hour Barber Shop - website launcher

Run this file with Python:   python barber_site.py

It does two things:
  1. Saves the website as index.html next to this script
     (that index.html is the file GitHub Pages needs).
  2. Starts a small web server and opens the site in your browser
     at http://localhost:8000 so you can preview it.

Press Ctrl+C in this window to stop the server.

Note: GitHub Pages cannot run Python. To put the site online,
upload the index.html this script creates, not this .py file.
"""

import http.server
import os
import socketserver
import threading
import webbrowser

PORT = 8000

HTML = r'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Atlanta’s 24 Hour Barber Shop | Haircuts, Fades &amp; Beard Trims Anytime in SW Atlanta</title>
<meta name="description" content="Atlanta’s 24 Hour Barber Shop at 2612 Steele Ave SW, Bldg 25 A. Haircuts, fades, beard trims and line-ups day or night. Book a chair or call 404-723-4711.">
<meta property="og:title" content="Atlanta’s 24 Hour Barber Shop">
<meta property="og:description" content="Haircuts, fades and beard work any hour in Southwest Atlanta. Book a chair or call 404-723-4711.">
<meta property="og:type" content="website">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>💈</text></svg>">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Big+Shoulders+Display:wght@600;800;900&family=Public+Sans:wght@400;500;700&display=swap" rel="stylesheet">

<!-- Structured data so Google shows the right hours, phone and address -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BarberShop",
  "name": "Atlanta’s 24 Hour Barber Shop",
  "telephone": "+1-404-723-4711",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "2612 Steele Ave SW, Bldg 25 A",
    "addressLocality": "Atlanta",
    "addressRegion": "GA",
    "postalCode": "30315",
    "addressCountry": "US"
  },
  "openingHoursSpecification": [{
    "@type": "OpeningHoursSpecification",
    "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
    "opens": "00:00",
    "closes": "23:59"
  }],
  "paymentAccepted": "Cash, Cash App"
}
</script>

<style>
  :root {
    --bg: #EDF1F7;
    --surface: #FFFFFF;
    --ink: #13203B;
    --muted: #4E5C77;
    --red: #B3122A;
    --blue: #1D4C9A;
    --line: #C7D0DF;
    --pole-white: #FFFFFF;
    --on-accent: #FFFFFF;
    --field: #F7F9FC;
    color-scheme: light;
  }
  @media (prefers-color-scheme: dark) {
    :root:not([data-theme="light"]) {
      --bg: #0C1630;
      --surface: #142142;
      --ink: #E9EFFA;
      --muted: #9DABC7;
      --red: #FF5A6C;
      --blue: #86AAF2;
      --line: #2A3B63;
      --pole-white: #DDE5F3;
      --on-accent: #0C1630;
      --field: #101B38;
      color-scheme: dark;
    }
  }
  :root[data-theme="dark"] {
    --bg: #0C1630;
    --surface: #142142;
    --ink: #E9EFFA;
    --muted: #9DABC7;
    --red: #FF5A6C;
    --blue: #86AAF2;
    --line: #2A3B63;
    --pole-white: #DDE5F3;
    --on-accent: #0C1630;
    --field: #101B38;
    color-scheme: dark;
  }

  *, *::before, *::after { box-sizing: border-box; }
  :root {
    padding-top: env(safe-area-inset-top, 0px);
    padding-bottom: env(safe-area-inset-bottom, 0px);
  }
  html { scroll-behavior: smooth; scroll-padding-top: calc(env(safe-area-inset-top, 0px) + 72px); }
  @media (prefers-reduced-motion: reduce) { html { scroll-behavior: auto; } }

  body {
    margin: 0;
    background: var(--bg);
    color: var(--ink);
    font-family: "Public Sans", "Segoe UI", system-ui, -apple-system, sans-serif;
    font-size: 1.0625rem;
    line-height: 1.6;
    -webkit-font-smoothing: antialiased;
  }
  img { max-width: 100%; }
  a { color: inherit; }
  :focus-visible { outline: 3px solid var(--blue); outline-offset: 3px; border-radius: 4px; }

  .display { font-family: "Big Shoulders Display", "Arial Narrow", Impact, sans-serif; letter-spacing: 0.005em; }
  .wrap { width: min(1120px, 100% - 2.5rem); margin-inline: auto; }

  /* The barber pole stripe: the shop's one visual signature */
  .pole {
    height: 10px;
    background: repeating-linear-gradient(-45deg,
      var(--red) 0 14px, var(--pole-white) 14px 28px,
      var(--blue) 28px 42px, var(--pole-white) 42px 56px);
  }

  .demo-note {
    background: var(--ink);
    color: var(--bg);
    font-size: 0.875rem;
    text-align: center;
    padding: 0.5rem 1rem;
  }

  /* Header */
  header {
    position: sticky;
    top: env(safe-area-inset-top, 0px);
    z-index: 20;
    background: var(--bg);
    border-bottom: 1px solid var(--line);
  }
  body::before {
    content: ""; position: fixed; inset: 0 0 auto;
    height: env(safe-area-inset-top, 0px); z-index: 30; background: var(--bg);
  }
  .bar { display: flex; align-items: center; justify-content: space-between; gap: 1rem; padding-block: 0.75rem; }
  .brand { text-decoration: none; font-weight: 800; font-size: 1.5rem; line-height: 1; }
  .brand span { display: block; font-family: "Public Sans", sans-serif; font-weight: 500; font-size: 0.8125rem; color: var(--muted); margin-top: 0.25rem; letter-spacing: 0; }
  nav { display: flex; align-items: center; gap: 1.5rem; }
  nav a.link { text-decoration: none; font-weight: 500; color: var(--muted); }
  nav a.link:hover { color: var(--ink); }
  @media (max-width: 760px) { nav a.link { display: none; } }

  .btn {
    display: inline-flex; align-items: center; justify-content: center; gap: 0.5rem;
    font: inherit; font-weight: 700; font-size: 1rem;
    padding: 0.8rem 1.35rem; border-radius: 999px;
    border: 2px solid var(--red); background: var(--red); color: var(--on-accent);
    text-decoration: none; cursor: pointer;
  }
  .btn:hover { filter: brightness(1.08); }
  .btn.ghost { background: transparent; color: var(--ink); border-color: var(--ink); }
  .btn.small { padding: 0.55rem 1rem; font-size: 0.9375rem; }

  /* Hero: live Atlanta clock */
  .hero { padding-block: clamp(3rem, 8vw, 6rem) clamp(3rem, 7vw, 5rem); }
  .now-label { font-weight: 500; color: var(--muted); margin: 0; }
  .clock {
    font-weight: 900; line-height: 0.82;
    font-size: clamp(6rem, 24vw, 17rem);
    margin: 0.25rem 0 0; font-variant-numeric: tabular-nums;
    display: flex; align-items: baseline; flex-wrap: wrap;
  }
  .clock .ampm { font-size: 0.3em; color: var(--red); margin-left: 0.2em; }
  .clock .colon { animation: blink 2s steps(1) infinite; }
  @keyframes blink { 50% { opacity: 0.25; } }
  @media (prefers-reduced-motion: reduce) { .clock .colon { animation: none; } }
  .hero h1 {
    font-family: "Big Shoulders Display", "Arial Narrow", Impact, sans-serif;
    font-weight: 800; font-size: clamp(2.25rem, 5.5vw, 3.75rem); line-height: 1;
    margin: 1.5rem 0 1rem; max-width: 18ch;
  }
  .status { font-size: 1.1875rem; max-width: 60ch; margin: 0 0 2rem; color: var(--muted); }
  .status strong { color: var(--ink); }
  .actions { display: flex; flex-wrap: wrap; gap: 0.75rem; }

  section { padding-block: clamp(3rem, 7vw, 5rem); border-top: 1px solid var(--line); }
  h2 { font-family: "Big Shoulders Display", "Arial Narrow", Impact, sans-serif; font-weight: 800; font-size: clamp(2rem, 4.5vw, 3rem); line-height: 1; margin: 0 0 0.75rem; }
  .lede { color: var(--muted); max-width: 60ch; margin: 0 0 2.25rem; }

  /* Price board */
  .split { display: grid; grid-template-columns: 1fr; gap: 3rem; }
  @media (min-width: 900px) { .split { grid-template-columns: 5fr 4fr; gap: 4rem; } }
  .prices { list-style: none; margin: 0; padding: 0; }
  .prices li { padding: 1rem 0; border-bottom: 1px dashed var(--line); }
  .prices .row { display: flex; align-items: baseline; gap: 0.75rem; }
  .prices .name { font-weight: 700; font-size: 1.125rem; }
  .prices .dots { flex: 1; border-bottom: 2px dotted var(--line); transform: translateY(-0.3em); min-width: 1rem; }
  .prices .price { font-family: "Big Shoulders Display", "Arial Narrow", sans-serif; font-weight: 800; font-size: 1.625rem; color: var(--red); font-variant-numeric: tabular-nums; }
  .prices .detail { margin: 0.15rem 0 0; color: var(--muted); font-size: 0.9375rem; }
  .fine { color: var(--muted); font-size: 0.875rem; margin-top: 1rem; }

  .vip {
    background: var(--ink); color: var(--bg);
    border-radius: 20px; padding: 2rem;
    position: relative; overflow: hidden; align-self: start;
  }
  .vip::before { content: ""; position: absolute; inset: 0 0 auto; height: 8px;
    background: repeating-linear-gradient(-45deg, var(--red) 0 10px, var(--pole-white) 10px 20px, var(--blue) 20px 30px, var(--pole-white) 30px 40px); }
  .vip h3 { font-family: "Big Shoulders Display", "Arial Narrow", sans-serif; font-weight: 800; font-size: 2rem; margin: 0.5rem 0 0.5rem; line-height: 1; }
  .vip p { margin: 0 0 1rem; opacity: 0.85; }
  .vip ul { margin: 0 0 1.5rem; padding-left: 1.2rem; }
  .vip li { margin-bottom: 0.4rem; }
  .vip .btn { background: var(--bg); color: var(--ink); border-color: var(--bg); }

  /* Barbers */
  .barbers { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 1.5rem; }
  .barber { border-left: 4px solid var(--blue); padding: 0.25rem 0 0.25rem 1.25rem; }
  .barber:nth-child(2) { border-left-color: var(--red); }
  .barber h3 { font-family: "Big Shoulders Display", "Arial Narrow", sans-serif; font-weight: 800; font-size: 2.25rem; margin: 0; line-height: 1; }
  .barber .role { font-weight: 700; margin: 0.35rem 0 0.5rem; }
  .barber p { margin: 0; color: var(--muted); }

  /* Booking */
  .book-grid { display: grid; grid-template-columns: 1fr; gap: 2.5rem; }
  @media (min-width: 900px) { .book-grid { grid-template-columns: 4fr 5fr; gap: 4rem; } }
  .steps { margin: 0; padding: 0; list-style: none; counter-reset: s; }
  .steps li { counter-increment: s; display: grid; grid-template-columns: 2.5rem 1fr; gap: 0.75rem; margin-bottom: 1.25rem; }
  .steps li::before { content: counter(s); font-family: "Big Shoulders Display", sans-serif; font-weight: 900; font-size: 2rem; line-height: 1; color: var(--red); }
  .steps strong { display: block; }
  .steps span { color: var(--muted); }

  form { background: var(--surface); border: 1px solid var(--line); border-radius: 20px; padding: clamp(1.25rem, 4vw, 2rem); }
  .fields { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
  .fields .full { grid-column: 1 / -1; }
  @media (max-width: 520px) { .fields { grid-template-columns: 1fr; } }
  label { display: block; font-weight: 700; font-size: 0.9375rem; margin-bottom: 0.35rem; }
  input, select, textarea {
    width: 100%; font: inherit; color: var(--ink); background: var(--field);
    border: 1.5px solid var(--line); border-radius: 10px; padding: 0.7rem 0.8rem;
  }
  input:focus, select:focus, textarea:focus { border-color: var(--blue); outline: none; box-shadow: 0 0 0 3px color-mix(in srgb, var(--blue) 30%, transparent); }
  textarea { resize: vertical; min-height: 5rem; }
  .err { color: var(--red); font-size: 0.875rem; margin: 0.75rem 0 0; min-height: 1.2em; }
  form .btn { width: 100%; margin-top: 0.5rem; }

  .confirm { display: none; background: var(--surface); border: 2px solid var(--blue); border-radius: 20px; padding: clamp(1.25rem, 4vw, 2rem); }
  .confirm.show { display: block; }
  .confirm h3 { font-family: "Big Shoulders Display", sans-serif; font-weight: 800; font-size: 2rem; margin: 0 0 0.5rem; line-height: 1; }
  .confirm pre { white-space: pre-wrap; font-family: inherit; background: var(--field); border-radius: 10px; padding: 1rem; margin: 1rem 0; border: 1px solid var(--line); }
  .confirm .actions { margin-top: 1rem; }
  .cash { margin-top: 1rem; padding-top: 1rem; border-top: 1px dashed var(--line); color: var(--muted); }
  .cash strong { color: var(--ink); }

  /* Visit */
  .visit { display: grid; grid-template-columns: 1fr; gap: 2rem; }
  @media (min-width: 900px) { .visit { grid-template-columns: 2fr 3fr; gap: 4rem; } }
  .addr { font-size: 1.25rem; font-weight: 700; line-height: 1.4; margin: 0 0 1rem; font-style: normal; }
  .find { background: var(--surface); border-left: 4px solid var(--red); padding: 1rem 1.25rem; border-radius: 0 12px 12px 0; margin: 1.5rem 0; }
  .find p { margin: 0; }
  .map { width: 100%; aspect-ratio: 4 / 3; border: 0; border-radius: 20px; background: var(--surface); }

  /* FAQ */
  details { border-bottom: 1px solid var(--line); padding: 1.1rem 0; max-width: 72ch; }
  summary { font-weight: 700; font-size: 1.125rem; cursor: pointer; list-style: none; display: flex; justify-content: space-between; gap: 1rem; }
  summary::-webkit-details-marker { display: none; }
  summary::after { content: "+"; font-family: "Big Shoulders Display", sans-serif; font-size: 1.75rem; line-height: 1; color: var(--red); }
  details[open] summary::after { content: "–"; }
  details p { color: var(--muted); margin: 0.75rem 0 0; }

  footer { border-top: 1px solid var(--line); padding-block: 2rem 3rem; color: var(--muted); font-size: 0.9375rem; }
  footer .wrap { display: flex; flex-wrap: wrap; justify-content: space-between; gap: 1rem; }

  /* Sticky call bar on phones */
  .mobile-bar { display: none; }
  @media (max-width: 760px) {
    .mobile-bar {
      display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem;
      position: fixed; left: 0; right: 0; bottom: 0; z-index: 25;
      padding: 0.6rem 0.75rem calc(0.6rem + env(safe-area-inset-bottom, 0px));
      background: var(--bg); border-top: 1px solid var(--line);
    }
    .mobile-bar .btn { width: 100%; }
    footer { padding-bottom: 6rem; }
    header .btn { display: none; }
  }
</style>
</head>
<body>

<div class="pole" aria-hidden="true"></div>
<div class="demo-note" id="demoNote" hidden>Preview site. Prices, barber schedules and the Cash App tag are placeholders until the shop confirms them.</div>

<header>
  <div class="wrap bar">
    <a class="brand display" href="#top">Atlanta’s 24 Hour Barber Shop<span>2612 Steele Ave SW, Bldg 25 A</span></a>
    <nav aria-label="Main">
      <a class="link" href="#prices">Prices</a>
      <a class="link" href="#barbers">Barbers</a>
      <a class="link" href="#visit">Find us</a>
      <a class="btn small" href="#book">Book a chair</a>
    </nav>
  </div>
</header>

<main id="top">
  <div class="wrap hero">
    <p class="now-label">Right now in Atlanta it’s</p>
    <p class="clock display" id="clock" aria-live="off">
      <span id="hh">12</span><span class="colon">:</span><span id="mm">00</span><span class="ampm" id="ampm">AM</span>
    </p>
    <h1>And we’re cutting.</h1>
    <p class="status" id="status"><strong>Open 24 hours, 7 days a week.</strong> Fades, line-ups and beard work whenever your schedule allows. Book ahead and your barber will be ready when you walk in.</p>
    <div class="actions">
      <a class="btn" href="#book">Book a chair</a>
      <a class="btn ghost" href="tel:+14047234711" data-phone-link>Call 404-723-4711</a>
    </div>
  </div>

  <section id="prices">
    <div class="wrap split">
      <div>
        <h2>Prices</h2>
        <p class="lede">The price you see is the price you pay. No surprise add-ons in the chair.</p>
        <ul class="prices">
          <li><div class="row"><span class="name">Haircut</span><span class="dots"></span><span class="price">$30</span></div><p class="detail">Classic or modern cut, finished and styled.</p></li>
          <li><div class="row"><span class="name">Taper or skin fade</span><span class="dots"></span><span class="price">$35</span></div><p class="detail">Clean blend, shaped to your head and growth pattern.</p></li>
          <li><div class="row"><span class="name">Haircut and beard</span><span class="dots"></span><span class="price">$45</span></div><p class="detail">Full cut plus beard shaping and detailing.</p></li>
          <li><div class="row"><span class="name">Beard trim and shape</span><span class="dots"></span><span class="price">$20</span></div><p class="detail">Trim, shape-up and razor detailing.</p></li>
          <li><div class="row"><span class="name">Razor line-up</span><span class="dots"></span><span class="price">$15</span></div><p class="detail">Edge-up between cuts to stay sharp.</p></li>
          <li><div class="row"><span class="name">Kids and teens cut</span><span class="dots"></span><span class="price">$25</span></div><p class="detail">Clean, age-appropriate cuts for younger clients.</p></li>
        </ul>
        <p class="fine">Cash and Cash App accepted.</p>
      </div>

      <aside class="vip" aria-labelledby="vip-title">
        <h3 id="vip-title">VIP membership</h3>
        <p>For regulars who want their spot held.</p>
        <ul>
          <li>Priority booking at any hour</li>
          <li>Members-only deals on cuts and beard work</li>
        </ul>
        <a class="btn" href="#book" data-vip>Ask about VIP</a>
      </aside>
    </div>
  </section>

  <section id="barbers">
    <div class="wrap">
      <h2>Your barbers</h2>
      <p class="lede">Pick your barber when you book, or let us match you with whoever is in the chair.</p>
      <div class="barbers">
        <article class="barber">
          <h3>Gerald</h3>
          <p class="role">Master barber</p>
          <p>Patient, precise cuts. Takes the time to get your fade and line-up exactly right.</p>
        </article>
        <article class="barber">
          <h3>Mellow</h3>
          <p class="role">Late-night barber</p>
          <p>Beard trims, touch-ups and full cuts for the after-10 PM crowd.</p>
        </article>
      </div>
    </div>
  </section>

  <section id="book">
    <div class="wrap book-grid">
      <div>
        <h2>Book a chair</h2>
        <p class="lede">Walk-ins are welcome, but late at night a booking guarantees a barber is ready for you.</p>
        <ol class="steps">
          <li><div><strong>Pick a service and time</strong><span>Any day, any hour.</span></div></li>
          <li><div><strong>Send the request</strong><span>It goes straight to the shop’s phone as a text.</span></div></li>
          <li><div><strong>Get your confirmation</strong><span>The shop texts back to lock in your spot.</span></div></li>
        </ol>
      </div>

      <div>
        <form id="bookForm" novalidate>
          <div class="fields">
            <div>
              <label for="fName">Your name</label>
              <input id="fName" name="name" autocomplete="name" required>
            </div>
            <div>
              <label for="fPhone">Your phone</label>
              <input id="fPhone" name="phone" type="tel" autocomplete="tel" inputmode="tel" required>
            </div>
            <div class="full">
              <label for="fService">Service</label>
              <select id="fService" name="service" required>
                <option value="">Choose a service</option>
                <option>Haircut</option>
                <option>Taper or skin fade</option>
                <option>Haircut and beard</option>
                <option>Beard trim and shape</option>
                <option>Razor line-up</option>
                <option>Kids and teens cut</option>
                <option>VIP membership question</option>
              </select>
            </div>
            <div>
              <label for="fDate">Date</label>
              <input id="fDate" name="date" type="date" required>
            </div>
            <div>
              <label for="fTime">Time</label>
              <input id="fTime" name="time" type="time" required>
            </div>
            <div class="full">
              <label for="fBarber">Barber</label>
              <select id="fBarber" name="barber">
                <option>No preference</option>
                <option>Gerald</option>
                <option>Mellow</option>
              </select>
            </div>
            <div class="full">
              <label for="fNotes">Anything we should know? (optional)</label>
              <textarea id="fNotes" name="notes" placeholder="Style you want, a photo you’ll bring, or if you’re running tight on time"></textarea>
            </div>
          </div>
          <p class="err" id="formErr" role="alert"></p>
          <button class="btn" type="submit">Send booking request</button>
        </form>

        <div class="confirm" id="confirm" tabindex="-1">
          <h3>Booking request ready</h3>
          <p>Tap “Text the shop” to send it. If you’re on a computer, call or copy the details instead.</p>
          <pre id="summary"></pre>
          <div class="actions">
            <a class="btn" id="smsLink" href="#">Text the shop</a>
            <a class="btn ghost" href="tel:+14047234711" data-phone-link>Call instead</a>
            <button class="btn ghost" type="button" id="copyBtn">Copy details</button>
            <button class="btn ghost" type="button" id="editBtn">Edit request</button>
          </div>
          <p class="cash" id="cashNote"></p>
        </div>
      </div>
    </div>
  </section>

  <section id="visit">
    <div class="wrap visit">
      <div>
        <h2>Find us</h2>
        <address class="addr">2612 Steele Ave SW<br>Building 25, Unit A<br>Atlanta, GA 30315</address>
        <div class="find">
          <p><strong>Several buildings share this address.</strong> Look for Building 25, then Unit A. Lost? Call and we’ll walk you in.</p>
        </div>
        <div class="actions">
          <a class="btn" href="https://www.google.com/maps/search/?api=1&query=2612+Steele+Ave+SW+Bldg+25+Atlanta+GA+30315" target="_blank" rel="noopener">Get directions</a>
          <a class="btn ghost" href="tel:+14047234711" data-phone-link>Call 404-723-4711</a>
        </div>
      </div>
      <iframe class="map" title="Map to Atlanta’s 24 Hour Barber Shop" loading="lazy" referrerpolicy="no-referrer-when-downgrade"
        src="https://www.google.com/maps?q=2612+Steele+Ave+SW,+Atlanta,+GA+30315&output=embed"></iframe>
    </div>
  </section>

  <section id="faq">
    <div class="wrap">
      <h2>Questions</h2>
      <details>
        <summary>Are you really open 24 hours?</summary>
        <p>Yes, every day. Late at night there may be one barber in the shop, so book ahead or call before you head over and we’ll make sure someone is ready for you.</p>
      </details>
      <details>
        <summary>Do you take walk-ins?</summary>
        <p>Yes. During busy hours a booking gets you in the chair faster.</p>
      </details>
      <details>
        <summary>How do I pay?</summary>
        <p>Cash or Cash App. Some bookings may ask for a small deposit through Cash App to hold a late-night spot.</p>
      </details>
      <details>
        <summary>Do you cut kids’ hair?</summary>
        <p>Yes, kids and teens are welcome any time.</p>
      </details>
      <details>
        <summary>How do I cancel or change a booking?</summary>
        <p>Text or call 404-723-4711 as early as you can so we can give the slot to someone else.</p>
      </details>
    </div>
  </section>
</main>

<footer>
  <div class="wrap">
    <span>© <span id="year"></span> Atlanta’s 24 Hour Barber Shop</span>
    <span>2612 Steele Ave SW, Bldg 25 A, Atlanta, GA 30315, <a href="tel:+14047234711" data-phone-link>404-723-4711</a></span>
  </div>
</footer>

<div class="mobile-bar">
  <a class="btn ghost" href="tel:+14047234711" data-phone-link>Call</a>
  <a class="btn" href="#book">Book a chair</a>
</div>

<script>
  /* ===== Edit these before going live ===== */
  const SHOP = {
    phoneDisplay: "404-723-4711",
    phoneE164: "+14047234711",
    cashtag: "",        // e.g. "$AtlCuts24". Leave empty to hide the Cash App line.
    depositAmount: "",  // e.g. "$10". Leave empty if no deposit is required.
    demo: true          // true shows the “Preview site” banner. Set to false once details are confirmed.
  };
  /* ======================================= */

  const tz = "America/New_York";

  // Demo banner
  if (SHOP.demo) document.getElementById("demoNote").hidden = false;
  document.getElementById("year").textContent = new Date().getFullYear();

  // Live Atlanta clock
  function atlParts(d = new Date()) {
    const parts = new Intl.DateTimeFormat("en-US", { timeZone: tz, hour: "numeric", minute: "2-digit", hour12: true }).formatToParts(d);
    const get = t => (parts.find(p => p.type === t) || {}).value;
    const hour24 = Number(new Intl.DateTimeFormat("en-US", { timeZone: tz, hour: "numeric", hourCycle: "h23" }).format(d));
    return { h: get("hour"), m: get("minute"), ampm: (get("dayPeriod") || "").toUpperCase(), hour24 };
  }
  function tick() {
    const t = atlParts();
    document.getElementById("hh").textContent = t.h;
    document.getElementById("mm").textContent = t.m;
    document.getElementById("ampm").textContent = t.ampm;
    const late = t.hour24 >= 22 || t.hour24 < 6;
    document.getElementById("status").innerHTML = late
      ? "<strong>Open now, all night.</strong> It’s late, so book or call ahead and your barber will be ready when you walk in."
      : "<strong>Open now, 24 hours a day, 7 days a week.</strong> Fades, line-ups and beard work whenever your schedule allows. Book ahead to skip the wait.";
    document.getElementById("clock").setAttribute("aria-label", `${t.h}:${t.m} ${t.ampm} in Atlanta`);
  }
  tick();
  setInterval(tick, 15000);

  // Default the date picker to today in Atlanta
  const todayAtl = new Intl.DateTimeFormat("en-CA", { timeZone: tz }).format(new Date());
  const dateEl = document.getElementById("fDate");
  dateEl.min = todayAtl;
  dateEl.value = todayAtl;

  // VIP button preselects the VIP option
  document.querySelector("[data-vip]").addEventListener("click", () => {
    document.getElementById("fService").value = "VIP membership question";
  });

  // Booking request → prefilled text message to the shop
  const form = document.getElementById("bookForm");
  const confirmBox = document.getElementById("confirm");
  const errEl = document.getElementById("formErr");

  function niceDate(iso) {
    const [y, m, d] = iso.split("-").map(Number);
    return new Date(y, m - 1, d).toLocaleDateString("en-US", { weekday: "long", month: "long", day: "numeric" });
  }
  function niceTime(hhmm) {
    const [h, m] = hhmm.split(":").map(Number);
    const ap = h >= 12 ? "PM" : "AM";
    return `${((h + 11) % 12) + 1}:${String(m).padStart(2, "0")} ${ap}`;
  }

  form.addEventListener("submit", e => {
    e.preventDefault();
    const f = Object.fromEntries(new FormData(form));
    const missing = [];
    if (!f.name.trim()) missing.push("your name");
    if (f.phone.replace(/\D/g, "").length < 10) missing.push("a 10-digit phone number");
    if (!f.service) missing.push("a service");
    if (!f.date) missing.push("a date");
    if (!f.time) missing.push("a time");
    if (missing.length) {
      errEl.textContent = "Add " + missing.join(", ") + " to send your request.";
      return;
    }
    errEl.textContent = "";

    const lines = [
      "Booking request – Atlanta’s 24 Hour Barber Shop",
      `Name: ${f.name.trim()}`,
      `Phone: ${f.phone.trim()}`,
      `Service: ${f.service}`,
      `When: ${niceDate(f.date)} at ${niceTime(f.time)}`,
      `Barber: ${f.barber}`
    ];
    if (f.notes.trim()) lines.push(`Notes: ${f.notes.trim()}`);
    const text = lines.join("\n");

    document.getElementById("summary").textContent = text;
    // "?&body=" works on both iPhone and Android
    document.getElementById("smsLink").href = `sms:${SHOP.phoneE164}?&body=${encodeURIComponent(text)}`;

    const cash = document.getElementById("cashNote");
    if (SHOP.cashtag) {
      cash.innerHTML = SHOP.depositAmount
        ? `To hold your spot, send a <strong>${SHOP.depositAmount}</strong> deposit to <strong>${SHOP.cashtag}</strong> on Cash App. It comes off your total.`
        : `Pay in the shop with cash or Cash App at <strong>${SHOP.cashtag}</strong>.`;
      cash.hidden = false;
    } else {
      cash.hidden = true;
    }

    form.style.display = "none";
    confirmBox.classList.add("show");
    confirmBox.focus();
  });

  document.getElementById("editBtn").addEventListener("click", () => {
    confirmBox.classList.remove("show");
    form.style.display = "";
    document.getElementById("fName").focus();
  });

  document.getElementById("copyBtn").addEventListener("click", async e => {
    const btn = e.currentTarget;
    try {
      await navigator.clipboard.writeText(document.getElementById("summary").textContent);
      btn.textContent = "Copied";
    } catch {
      btn.textContent = "Select the text above to copy";
    }
    setTimeout(() => (btn.textContent = "Copy details"), 2500);
  });
</script>
</body>
</html>
'''


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    os.chdir(here)

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(HTML)
    print("Saved index.html in:", here)

    handler = http.server.SimpleHTTPRequestHandler
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        url = f"http://localhost:{PORT}/"
        print("Website running at", url)
        print("Press Ctrl+C to stop.")
        threading.Timer(1.0, lambda: webbrowser.open(url)).start()
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nStopped.")


if __name__ == "__main__":
    main()
