"""Builds the SPLY/DMND static site into ./site (one HTML file per page)."""
import os
from html import escape as e

OUT = "site"
EMAIL = "hello@splydmnd.com"
BASE_HUE = 235

ROSTER = [
    dict(slug="dj-clean", name="DJ Clean", type="dj", genre="Open format", based="Los Angeles, CA",
         aka="The Sound of The People", origin="Washington, D.C.",
         sound="Open format: hip-hop, R&B, pop, house, dancehall, Afro-Caribbean, global sounds, classics and throwbacks",
         avail="Clubs, private events, weddings, corporate functions, festivals, brand activations, cultural spaces",
         sample=False, website="https://www.thesoundofthepeople.com",
         mixcloud="https://www.mixcloud.com/djclean/", instagram="https://www.instagram.com/djclean/",
         photo="images/dj-clean.jpg", pos="38% 30%",
         bio=["DJ Clean, known as \u201cThe Sound of The People,\u201d is a Los Angeles-based open-format DJ with over 20 years of experience bringing energy, style, and musical range to clubs, private events, corporate functions, festivals, brand activations, and cultural spaces.",
              "Originally from Washington, D.C., DJ Clean is prepared for any occasion, with the ability to move seamlessly through hip-hop, R&B, pop, house, dancehall, Afro-Caribbean rhythms, global sounds, classics, throwbacks, and feel-good party records. His versatility allows him to read any room and create the right atmosphere for everything from luxury private events and weddings to agency bookings, corporate clients, nightlife, and large-scale experiences.",
              "Whether behind the booth, on the mic, or curating the perfect soundtrack, DJ Clean brings professionalism, personality, and the musical range needed to make every event feel polished, intentional, and unforgettable."]),
    dict(slug="all-en1", name="All-En1", type="dj", genre="DJ · Producer", based="New York, NY",
         aka="Jordan Allen", role="DJ, producer, music lover",
         clients="Red Bull, Atlantic Records, Coca-Cola, Atlas Strategy Group",
         sample=False, email="all-en1@all-en1.com",
         instagram="https://www.instagram.com/all_en1/", twitter="https://x.com/all_en1",
         photo="images/all-en1.jpg", pos="50% 30%",
         bio=["Jordan “All-En1” Allen remembers exactly when he wanted to get into the music business. It was his 8th grade end-of-year trip, and he had stayed up way too late the night before recording the best new songs off the radio (yes, he came up in the era when that was the only way to make mixtapes). When he played the tape on the bus to Busch Gardens, everyone wanted a copy. That's when he knew he had an ear for music.",
              "His ear for music grew into a passion for sharing it with others. He soon learned to DJ and went on to host a successful college radio show at WNUR 89.3 at Northwestern University. His love of DJing and interest in the music industry eventually landed him in New York City as an intern, and then manager, at the legendary Violator Music Management, working for music mogul and visionary Chris Lighty.",
              "At Violator, Jordan honed his management and A&R skills on projects for Soulja Boy, Diggy Simmons and 50 Cent, and with corporate partners such as vitaminwater and Coca-Cola. That experience inspired him to start his own artist management and events company, FTM, where he put on shows and spun at parties in some of NYC’s most prominent venues."]),
    dict(slug="marisol-vega", name="Marisol Vega", type="dj", genre="House · Disco", based="Queens, NY",
         avail="Hotel lounges, dinner service, late nights",
         bio=["Marisol Vega builds slow-burn sets that start as dinner music and end as a dance floor.",
              "Her residencies in hotel lounges are known for soulful house, classic disco edits and long, smooth blends."]),
    dict(slug="knxx", name="KNXX", type="dj", genre="Techno", based="Bushwick, BK",
         avail="Club nights, warehouse parties",
         bio=["KNXX plays driving, hypnotic techno built for dark rooms and long sets.",
              "A fixture of the Brooklyn warehouse scene, comfortable opening, closing or playing all night."]),
    dict(slug="selector-dre", name="Selector Dre", type="dj", genre="Hip-hop · R&B", based="Harlem, NYC",
         avail="Private events, brand activations, parties",
         bio=["Selector Dre is a crowd-pleaser in the best sense: deep crates of hip-hop and R&B with tight, clean mixing.",
              "Booked often for private events and launches where the guest list is wide and everyone needs to dance."]),
    dict(slug="lux-ama", name="Lux Ama", type="artist", genre="Afro-house · Live", based="Brooklyn, NY",
         avail="Live sets, brand events, festivals",
         bio=["Lux Ama blends Afro-house production with live percussion and vocals for a set that feels like a performance.",
              "A strong fit for launches and activations that want a moment, not just a playlist."]),
    dict(slug="theo-grant", name="Theo Grant", type="artist", genre="Soul · Keys", based="Jersey City, NJ",
         avail="Dinner sets, private events, hospitality",
         bio=["Theo Grant performs live keys and soul covers with original arrangements.",
              "Ideal for dinners, cocktail hours and hotel programming that call for live music with warmth."]),
    dict(slug="nina-rue", name="Nina Rue", type="artist", genre="Alt R&B", based="Manhattan, NY",
         avail="Showcases, brand partnerships, live shows",
         bio=["Nina Rue writes moody, modern R&B and performs with a stripped-back live band.",
              "Represented for live opportunities and brand partnerships that suit her sound."]),
    dict(slug="okon", name="Okon", type="artist", genre="Afrobeats", based="The Bronx, NY",
         avail="Live shows, festivals, brand events",
         bio=["Okon brings high-energy Afrobeats with a live hype set that gets rooms moving.",
              "Available for shows, festival slots and brand events looking for a headline moment."]),
]
BY_SLUG = {a["slug"]: a for a in ROSTER}
for i, a in enumerate(ROSTER):
    a["hue"] = BASE_HUE + ((i * 29) % 70) - 35
    a["seed"] = i * 37 + len(a["name"]) * 11
    a["initials"] = "".join(p[0] for p in a["name"].replace("DJ ", "").split())[:2]

DATES = [
    ("Nov 07", "Sat", "okon", "Rooftop series", "Williamsburg, BK", "Residency"),
    ("Nov 14", "Sat", "marisol-vega", "Hotel lobby lounge", "Midtown, NYC", "Hospitality"),
    ("Nov 21", "Sat", "knxx", "Warehouse party", "Bushwick, BK", "Club night"),
    ("Dec 05", "Sat", "lux-ama", "Product launch", "SoHo, NYC", "Brand event"),
    ("Dec 12", "Sat", "selector-dre", "Holiday party", "DUMBO, BK", "Private"),
    ("Dec 19", "Sat", "nina-rue", "Rooftop series", "Williamsburg, BK", "Residency"),
]

SERVICES = [
    ("DJ Management &amp; Booking", "For DJs · For venues",
     "Career strategy, calendar building, negotiation and advancing. Venues get vetted DJs matched to the room and the crowd.",
     "Residencies · Club nights · Private events · Touring", "Book a DJ"),
    ("Artist Representation", "For artists",
     "A partner on positioning, partnerships and live opportunities, built on years of artist management experience.",
     "Strategy · Brand partnerships · Live", "Get represented"),
    ("Hospitality Management", "For hotels · Bars · Restaurants",
     "Music programming and nightlife direction for venues that want sound to be part of who they are, from brunch to last call.",
     "Programming · Residency planning · Venue nights", "Program a venue"),
    ("Event Curation", "For brands · Private clients",
     "Music-first events built from the lineup out: talent, flow, timing and room, planned by someone who reads crowds for a living.",
     "Brand events · Launches · Parties · Series", "Plan an event"),
    ("Experiential", "For brands · Collaborators",
     "Activations and one-off concepts where music is the hook. If the idea doesn't fit a category yet, we want to hear it.",
     "Activations · Pop-ups · Collaborations", "Pitch an idea"),
]

NAV = [("home", "Home", ""), ("roster", "Roster", "roster.html"), ("services", "Services", "services.html"),
       ("dates", "Dates", "dates.html"), ("about", "About", "about.html")]

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Big+Shoulders+Display:wght@600;800;900'
         '&family=Archivo:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">')


def nav(p, active):
    home = p or "./"
    cur = ' aria-current="page"'
    links = "".join(
        f'<li><a href="{(p + href) if href else home}"{cur if key == active else ""}>{label}</a></li>'
        for key, label, href in NAV)
    return f"""<header class="nav">
  <div class="wrap">
    <a class="mark" href="{home}">SPLY<span>/</span>DMND</a>
    <nav aria-label="Main"><ul>{links}</ul></nav>
    <div class="nav-right">
      <a class="btn solid book-btn" href="{p}book.html">Book now</a>
      <button class="menu-btn" id="menu-btn" type="button" aria-expanded="false" aria-controls="mobile-menu" aria-label="Open menu"><span></span><span></span><span></span></button>
    </div>
  </div>
</header>
<nav class="mobile-menu" id="mobile-menu" aria-label="Mobile" hidden>
  <ul>
    {links}
  </ul>
  <a class="btn solid" href="{p}book.html">Book now</a>
  <div class="label">{EMAIL}</div>
</nav>"""


def footer(p):
    links = "".join(f'<li><a href="{(p + href) if href else (p or "./")}">{label}</a></li>' for _, label, href in NAV)
    return f"""<footer>
  <div class="wrap">
    <div class="foot-top">
      <span class="mark">SPLY<span>/</span>DMND</span>
      <div class="foot-cols">
        <ul class="foot-links">{links}<li><a href="{p}book.html">Book now</a></li></ul>
        <ul class="foot-links">
          <li><a href="https://instagram.com" target="_blank" rel="noopener">Instagram</a></li>
          <li><a href="https://soundcloud.com" target="_blank" rel="noopener">SoundCloud</a></li>
          <li><a href="https://open.spotify.com" target="_blank" rel="noopener">Spotify</a></li>
          <li><a href="https://linkedin.com" target="_blank" rel="noopener">LinkedIn</a></li>
        </ul>
      </div>
    </div>
    <div class="foot-bot">
      <span class="label">DJ Management · Artist Representation · Hospitality · Events · Experiential</span>
      <span class="label">Brooklyn, NY · © 2026 SPLY/DMND</span>
    </div>
  </div>
</footer>"""


def page(path, title, desc, active, body, artifact=False):
    depth = path.count("/")
    p = "../" * depth
    full_title = "SPLY/DMND" if active == "home" else f"{title} · SPLY/DMND"
    head = (f'<title>{e(full_title)}</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n'
            f'<meta name="description" content="{e(desc)}">\n{FONTS}\n<link rel="stylesheet" href="{p}styles.css">')
    inner = f"{nav(p, active)}\n<main>\n{body}\n</main>\n{footer(p)}\n<script src=\"{p}script.js\"></script>"
    if artifact:
        return f"{head}\n{inner}\n"
    return (f'<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
            f'<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n{head}\n</head>\n'
            f"<body>\n{inner}\n</body>\n</html>\n")


def photo(a, p):
    if a.get("photo"):
        return (f'<img src="{p}{a["photo"]}" alt="{e(a["name"])}" loading="lazy" '
                f'style="object-position:{a.get("pos", "center")}">')
    return (f'<canvas data-hue="{a["hue"]}" data-seed="{a["seed"]}" aria-hidden="true"></canvas>'
            f'<span class="initials" aria-hidden="true">{a["initials"]}</span>')


def card(a, p):
    kind = "DJ" if a["type"] == "dj" else "Artist"
    meta = kind + (" · " + e(a["genre"]) if a.get("genre") else "")
    sample = '<span class="sample">Sample</span>' if a.get("sample", True) else ""
    return f"""<a class="card" href="{p}roster/{a['slug']}.html" data-type="{a['type']}">
  <div class="photo">{photo(a, p)}{sample}</div>
  <h3>{e(a['name'])}</h3>
  <div class="meta"><span>{meta}</span><span>View →</span></div>
</a>"""


def dates_table(rows, p, show_artist=True):
    head = "<th>Date</th>" + ("<th>Artist</th>" if show_artist else "") + "<th>Venue</th><th>City</th><th>Type</th>"
    trs = []
    for d, dow, slug, venue, city, kind in rows:
        a = BY_SLUG[slug]
        artist = f'<td class="artist"><a href="{p}roster/{slug}.html">{e(a["name"])}</a></td>' if show_artist else ""
        trs.append(f'<tr><td class="date">{d}<small>{dow}</small></td>{artist}<td>{venue}</td><td>{city}</td><td class="type">{kind}</td></tr>')
    return f'<div class="table-wrap"><table><thead><tr>{head}</tr></thead><tbody>{"".join(trs)}</tbody></table></div>'


def services_list(p, tags=True):
    items = []
    for name, who, desc, tg, cta in SERVICES:
        t = f'<div class="tags">{tg}</div>' if tags else ""
        items.append(f'<li class="svc"><div><h3>{name}</h3><span class="label for">{who}</span></div>'
                     f'<div><p>{desc}</p>{t}</div><a class="more" href="{p}book.html">{cta} →</a></li>')
    return f'<ul class="services">{"".join(items)}</ul>'


def page_head(kicker, title, text):
    return f"""<section class="page-head"><div class="wrap">
  <div class="label">{kicker}</div>
  <h1>{title}</h1>
  <p>{text}</p>
</div></section>"""


def cta_band(p):
    return f"""<section class="block book cta"><div class="wrap">
  <div><div class="label">Booking desk</div><h2>Book now</h2><p>Tell us the date, the room and the crowd.</p></div>
  <a class="btn" href="{p}book.html">Start an inquiry →</a>
</div></section>"""


def home():
    feat = BY_SLUG["dj-clean"]
    slides = f"""<section class="hero" aria-roledescription="carousel" aria-label="Featured">
  <div class="slides">
    <article class="slide slide-photo is-active" aria-label="Slide 1 of 3">
      <img class="slide-img" src="{feat['photo']}" alt="{feat['name']}">
      <div class="wrap slide-body">
        <div class="label">Featured DJ · The Sound of The People</div>
        <h1 class="slide-name">{feat['name']}</h1>
        <p class="slide-copy">Los Angeles-based, D.C.-raised open-format DJ with 20+ years of energy, style and range for clubs, private events, corporate functions and brand activations.</p>
        <div class="slide-actions"><a class="btn" href="roster/dj-clean.html">More info</a><a class="btn solid" href="book.html#dj-clean">Book now</a></div>
      </div>
    </article>
    <article class="slide" aria-label="Slide 2 of 3">
      <canvas data-hue="{BASE_HUE + 25}" data-seed="154" aria-hidden="true"></canvas>
      <div class="wrap slide-body">
        <div class="label">Hospitality</div>
        <h2 class="slide-name">Sound is <em>the room</em></h2>
        <p class="slide-copy">Music programming and residency planning for hotels, bars, restaurants and lounges.</p>
        <div class="slide-actions"><a class="btn" href="services.html">Our services</a><a class="btn solid" href="book.html">Talk to us</a></div>
      </div>
    </article>
    <article class="slide" aria-label="Slide 3 of 3">
      <canvas data-hue="{BASE_HUE - 25}" data-seed="207" aria-hidden="true"></canvas>
      <div class="wrap slide-body">
        <div class="label">Experiential</div>
        <h2 class="slide-name">Nights <em>people</em> remember</h2>
        <p class="slide-copy">Activations, launches and one-off concepts where the lineup leads and the room tells the story.</p>
        <div class="slide-actions"><a class="btn" href="services.html">See how</a><a class="btn solid" href="book.html">Start a project</a></div>
      </div>
    </article>
  </div>
  <div class="slide-controls"><div class="wrap">
    <div class="dots" role="group" aria-label="Choose slide">
      <button class="dot is-active" id="dot-0" aria-label="Show slide 1" aria-current="true"></button>
      <button class="dot" id="dot-1" aria-label="Show slide 2"></button>
      <button class="dot" id="dot-2" aria-label="Show slide 3"></button>
    </div>
    <span class="counter" id="counter">01 / 03</span>
  </div></div>
</section>"""
    cards = "".join(card(a, "") for a in ROSTER)
    body = f"""{slides}
<section class="block" id="services"><div class="wrap">
  <div class="head"><h2>Services</h2><p>One agency on both sides of the booth: we represent the talent, and we program the rooms that need them.</p></div>
  {services_list("")}
</div></section>
<section class="block roster-bg" id="roster"><div class="wrap">
  <div class="head">
    <h2>Roster</h2>
    <div class="tabs" role="group" aria-label="Filter roster">
      <button class="tab" id="tab-all" data-filter="all" aria-pressed="true">All</button>
      <button class="tab" id="tab-dj" data-filter="dj" aria-pressed="false">DJs</button>
      <button class="tab" id="tab-artist" data-filter="artist" aria-pressed="false">Artists</button>
    </div>
  </div>
  <div class="grid">{cards}</div>
</div></section>
<section class="block" id="dates"><div class="wrap">
  <div class="head"><h2>Upcoming</h2><p>Where the roster is playing next. <span class="sample">Sample dates</span></p></div>
  {dates_table(DATES[:5], "")}
</div></section>
{about_section()}
{book_section("h2")}"""
    return body


def roster_page():
    cards = "".join(card(a, "") for a in ROSTER)
    return f"""{page_head('Roster', 'Roster', 'DJs and artists represented by SPLY/DMND. Tap a name to see their profile and book them.')}
<section class="block roster-bg"><div class="wrap">
  <div class="head">
    <div class="tabs" role="group" aria-label="Filter roster">
      <button class="tab" id="tab-all" data-filter="all" aria-pressed="true">All</button>
      <button class="tab" id="tab-dj" data-filter="dj" aria-pressed="false">DJs</button>
      <button class="tab" id="tab-artist" data-filter="artist" aria-pressed="false">Artists</button>
    </div>
    <span class="sample">Sample roster</span>
  </div>
  <div class="grid">{cards}</div>
</div></section>
{cta_band("")}"""


def services_page():
    return f"""{page_head('Services', 'Services', 'One agency on both sides of the booth: we represent the talent, and we program the rooms that need them.')}
<section class="block"><div class="wrap">{services_list("")}</div></section>
<section class="block"><div class="wrap">
  <div class="split">
    <div><div class="label">For talent</div><h3>The <em>Supply</em></h3><p>DJs and artists who want a manager who has played the rooms they're trying to get into.</p></div>
    <div><div class="label">For venues &amp; brands</div><h3>The <em>Demand</em></h3><p>Venues, hotels and brands that need the right talent and a night that runs on time.</p></div>
  </div>
</div></section>
{cta_band("")}"""


def dates_page():
    return f"""{page_head('Dates', 'Upcoming', 'Where the roster is playing next. <span class="sample">Sample dates</span>')}
<section class="block"><div class="wrap">{dates_table(DATES, "")}</div></section>
{cta_band("")}"""


def about_page():
    return f"""{page_head('About', 'About', 'The agency behind the roster.')}
{about_section()}
{cta_band("")}"""


def about_section():
    return f"""<section class="block about" id="about"><div class="wrap">
  <div class="big23" aria-hidden="true">23</div>
  <div>
    <div class="label">About SPLY/DMND</div>
    <h2>Built from the booth out</h2>
    <p>SPLY/DMND grew out of 23 years of DJing and hands-on work in artist management and event curation. We understand a booking from every angle: what talent needs to do their best work, and what a venue or brand needs to see on the night.</p>
    <p>Supply is the talent. Demand is the room. We make the match.</p>
    <ul class="creds">
      <li><span>DJ</span><span>23 years, every room size</span></li>
      <li><span>Management</span><span>Artist management background</span></li>
      <li><span>Events</span><span>Music-first curation</span></li>
    </ul>
  </div>
</div></section>"""


def book_page():
    return book_section("h1")


def book_section(tag):
    opts = "".join(f'<option value="{a["slug"]}" data-type="{a["type"]}">{e(a["name"])}</option>' for a in ROSTER)
    return f"""<section class="block book" id="book"><div class="wrap">
  <div>
    <div class="label">Booking desk</div>
    <{tag}>Book now</{tag}>
    <p>Tell us the date, the room and the crowd. Fill in the form to build your inquiry, then paste it into an email.</p>
    <div class="contact">{EMAIL}</div>
  </div>
  <form id="inquiry-form" novalidate>
    <div class="row">
      <label for="f-name">Name<input id="f-name" name="name" value="Maya Ortiz"></label>
      <label for="f-org">Company or venue<input id="f-org" name="org" value="Rooftop bar, Williamsburg"></label>
    </div>
    <div class="row">
      <label for="f-type">I'm looking for
        <select id="f-type" name="type">
          <option selected>DJ booking</option><option>Artist booking</option><option>DJ management</option>
          <option>Artist representation</option><option>Hospitality / music programming</option>
          <option>Event curation</option><option>Experiential project</option>
        </select>
      </label>
      <label for="f-artist">Artist
        <select id="f-artist" name="artist"><option value="">No preference</option>{opts}</select>
      </label>
    </div>
    <label for="f-date">Date (if known)<input id="f-date" name="date" type="date" value="2026-12-12"></label>
    <label for="f-msg">Details<textarea id="f-msg" name="msg">Holiday party for about 200 guests. Looking for an open-format DJ from 8pm to 1am.</textarea></label>
    <div class="form-foot">
      <button class="btn solid" type="submit">Copy inquiry</button>
      <p class="status" id="f-status" role="status"></p>
    </div>
    <textarea id="f-out" aria-label="Your inquiry text" readonly hidden></textarea>
  </form>
</div></section>"""


def artist_page(a):
    p = "../"
    kind = "DJ" if a["type"] == "dj" else "Artist"
    rows = [r for r in DATES if r[2] == a["slug"]]
    dates = dates_table(rows, p, show_artist=False) if rows else '<p class="empty">No public dates right now. Book a private date below.</p>'
    others = [x for x in ROSTER if x["slug"] != a["slug"]]
    idx = ROSTER.index(a)
    others = (others[idx:] + others[:idx])[:4]
    more = "".join(card(x, p) for x in others)
    bio = "".join(f"<p>{e(t)}</p>" for t in a["bio"])
    badge = ' <span class="sample">Sample profile</span>' if a.get("sample", True) else ""
    photo_tag = "" if a.get("photo") else '<span class="sample">Photo</span>'
    facts = []
    for label, key in (("Also known as", "aka"), ("Role", "role"), ("Sound", "sound"), ("Based in", "based"), ("From", "origin"), ("Available for", "avail"), ("Notable clients", "clients")):
        if key == "sound" and not a.get("sound") and not a.get("role"):
            key = "genre"
        if a.get(key):
            facts.append(f"<li><span>{label}</span><span>{e(a[key])}</span></li>")
    if a.get("mixcloud"):
        facts.append(f'<li><span>Listen</span><span><a href="{a["mixcloud"]}" target="_blank" rel="noopener">Mixcloud</a></span></li>')
    if a.get("instagram"):
        handle = "@" + a["instagram"].rstrip("/").split("/")[-1]
        facts.append(f'<li><span>Instagram</span><span><a href="{a["instagram"]}" target="_blank" rel="noopener">{handle}</a></span></li>')
    if a.get("twitter"):
        handle = "@" + a["twitter"].rstrip("/").split("/")[-1]
        facts.append(f'<li><span>X / Twitter</span><span><a href="{a["twitter"]}" target="_blank" rel="noopener">{handle}</a></span></li>')
    if a.get("email"):
        facts.append(f'<li><span>Email</span><span><a href="mailto:{a["email"]}">{e(a["email"])}</a></span></li>')
    if a.get("website"):
        host = a["website"].split("//")[-1].strip("/")
        facts.append(f'<li><span>Website</span><span><a href="{a["website"]}" target="_blank" rel="noopener">{e(host)}</a></span></li>')
    elif a.get("sample", True):
        facts.append('<li><span>Listen</span><span><a href="https://soundcloud.com" target="_blank" rel="noopener">SoundCloud</a><a href="https://instagram.com" target="_blank" rel="noopener">Instagram</a></span></li>')
    facts = "".join(facts)
    return f"""<section class="profile"><div class="wrap">
  <div class="photo">{photo(a, p)}{photo_tag}</div>
  <div>
    <div class="label"><a href="{p}roster.html">Roster</a> / {kind}{badge}</div>
    <h1>{e(a['name'])}</h1>
    <div class="bio">{bio}</div>
    <ul class="facts">{facts}
    </ul>
    <div class="actions">
      <a class="btn solid" href="{p}book.html#{a['slug']}">Book {e(a['name'])}</a>
      <a class="btn" href="{p}roster.html">Back to roster</a>
    </div>
  </div>
</div></section>
<section class="block"><div class="wrap">
  <div class="head"><h2>Dates</h2></div>
  {dates}
</div></section>
<section class="block roster-bg"><div class="wrap">
  <div class="head"><h2>More roster</h2><a class="more" href="{p}roster.html">Full roster →</a></div>
  <div class="grid">{more}</div>
</div></section>"""


def write(path, html):
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full) or ".", exist_ok=True)
    with open(full, "w") as f:
        f.write(html)


PAGES = [
    ("index.html", "Home", "SPLY/DMND is a Brooklyn agency for DJ management and booking, artist representation, hospitality, events and experiential.", "home", home()),
    ("roster.html", "Roster", "DJs and artists represented by SPLY/DMND.", "roster", roster_page()),
    ("services.html", "Services", "DJ management, artist representation, hospitality, event curation and experiential.", "services", services_page()),
    ("dates.html", "Dates", "Upcoming dates for the SPLY/DMND roster.", "dates", dates_page()),
    ("about.html", "About", "About SPLY/DMND.", "about", about_page()),
    ("book.html", "Book now", "Book a DJ or artist from SPLY/DMND.", "book", book_page()),
]
for a in ROSTER:
    PAGES.append((f"roster/{a['slug']}.html", a["name"], f"{a['name']}: {a['genre']}. Book through SPLY/DMND.", "roster", artist_page(a)))

for path, title, desc, active, body in PAGES:
    write(path, page(path, title, desc, active, body))

# Optional preview copy of the home page without the document skeleton (used for Claude artifact previews)
if os.environ.get("ARTIFACT_PREVIEW"):
    os.makedirs("artifact", exist_ok=True)
    with open("artifact/index.html", "w") as f:
        f.write(page("index.html", "Home", PAGES[0][2], "home", PAGES[0][4], artifact=True))

print("\n".join(p[0] for p in PAGES))
