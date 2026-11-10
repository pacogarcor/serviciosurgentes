#!/usr/bin/env python3
"""Generador de serviciosurgentes.es

Lee data/provincias.json, data/servicios.json y data/empresas.json y
genera index.html + provincias/<slug>.html + imágenes por defecto.

Para editar una empresa: cambia su entrada en data/empresas.json
(nombre, whatsapp, web, imagen) y vuelve a ejecutar:  python3 build.py
"""
import json, os, html, urllib.parse
from datetime import date

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = "serviciosurgentes.es"
DOMINIO = "https://serviciosurgentes.es"
WA_CONTACTO = "34600000000"  # WhatsApp del propietario del directorio (cámbialo)

def load(name):
    with open(os.path.join(ROOT, "data", name), encoding="utf-8") as f:
        return json.load(f)

PROVINCIAS = [dict(slug=s, nombre=n, comunidad=c) for s, n, c in load("provincias.json")]
SERVICIOS = load("servicios.json")

# ---------- iconos (SVG propios, trazo) ----------
ICONOS = {
 "cerrajeros": '<circle cx="22" cy="32" r="11"/><circle cx="22" cy="32" r="4"/><path d="M33 32h22M47 32v8M53 32v6"/>',
 "fontaneros": '<path d="M10 22h22v-8h10v8h6a8 8 0 0 1 8 8v4h-10v-2H10z"/><path d="M51 44c0 4-3 7-5 9-2-2-5-5-5-9 0-3 5-8 5-8s5 5 5 8z"/>',
 "electricistas": '<path d="M36 6 14 36h16l-4 22 24-32H34z"/>',
 "reformas": '<path d="M8 30 32 10l24 20"/><path d="M14 26v28h36V26"/><path d="M26 54V40h12v14"/><path d="M44 8v10"/>',
 "pintores": '<rect x="10" y="8" width="40" height="14" rx="3"/><path d="M50 15h4v12H32v8"/><rect x="28" y="35" width="8" height="21" rx="2"/>',
 "carpinteria": '<path d="M6 46 40 12l8 8-34 34H6z"/><path d="M34 18l8 8M12 40l4 4M18 34l4 4M24 28l4 4"/><path d="M44 52h14"/>',
 "aluminio": '<rect x="10" y="8" width="44" height="48" rx="2"/><rect x="16" y="14" width="14" height="36"/><rect x="34" y="14" width="14" height="36"/><path d="M28 30v4M36 30v4"/>',
 "cristaleros": '<rect x="10" y="10" width="44" height="44" rx="2"/><path d="M10 32h44M32 10v44M16 24l8-8M38 48l10-10"/>',
}

def icon(slug, size=28, cls="ico"):
    return (f'<svg class="{cls}" width="{size}" height="{size}" viewBox="0 0 64 64" fill="none" '
            f'stroke="currentColor" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round" '
            f'aria-hidden="true">{ICONOS[slug]}</svg>')

def imagen_defecto(serv):
    """SVG de marcador de posición para la imagen de la empresa."""
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 400">
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#1b1f1a"/><stop offset="1" stop-color="#0b0d0b"/></linearGradient>
<pattern id="p" width="24" height="24" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="24" height="24" fill="none"/><path d="M0 0v24" stroke="#d7ff3c" stroke-opacity=".06" stroke-width="10"/></pattern></defs>
<rect width="640" height="400" fill="url(#g)"/><rect width="640" height="400" fill="url(#p)"/>
<g transform="translate(256 90) scale(2)" fill="none" stroke="#d7ff3c" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round">{ICONOS[serv["slug"]]}</g>
<text x="320" y="300" text-anchor="middle" font-family="Anton, Impact, sans-serif" font-size="38" letter-spacing="2" fill="#f1f4ed">{serv["nombre"].upper()}</text>
<text x="320" y="340" text-anchor="middle" font-family="Arial, sans-serif" font-size="18" letter-spacing="4" fill="#8a9086">TU LOGO AQUÍ</text>
</svg>'''
    with open(os.path.join(ROOT, "img", "servicios", serv["slug"] + ".svg"), "w", encoding="utf-8") as f:
        f.write(svg)

# ---------- empresas ----------
def cargar_empresas():
    ruta = os.path.join(ROOT, "data", "empresas.json")
    datos = {}
    if os.path.exists(ruta):
        with open(ruta, encoding="utf-8") as f:
            datos = json.load(f)
    cambiado = False
    for p in PROVINCIAS:
        prov = datos.setdefault(p["slug"], {})
        for s in SERVICIOS:
            if s["slug"] not in prov:
                prov[s["slug"]] = {
                    "nombre": f"Tu empresa de {s['singular']} en {p['nombre']}",
                    "whatsapp": "",
                    "web": "",
                    "imagen": "",
                }
                cambiado = True
    if cambiado:
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)
    return datos

# ---------- plantilla ----------
e = html.escape

def menu_provincias(base):
    items = "".join(f'<li><a href="{base}provincias/{p["slug"]}.html">{e(p["nombre"])}</a></li>' for p in PROVINCIAS)
    return items

def cabecera(base, actual=""):
    return f'''<a class="skip" href="#contenido">Saltar al contenido</a>
<header class="top">
  <div class="wrap top__in">
    <a class="logo" href="{base}index.html" aria-label="{SITE} inicio">
      <span class="logo__mark">SU</span><span class="logo__txt">SERVICIOS<br><b>URGENTES</b></span>
    </a>
    <button class="burger" aria-label="Abrir menú" aria-expanded="false" aria-controls="nav"><span></span><span></span><span></span></button>
    <nav id="nav" class="nav">
      <div class="drop">
        <button class="drop__btn" aria-expanded="false" aria-haspopup="true">Provincias <span aria-hidden="true">▾</span></button>
        <div class="drop__panel" role="menu">
          <input class="drop__filter" type="search" placeholder="Filtrar provincia…" aria-label="Filtrar provincia">
          <ul class="drop__list">{menu_provincias(base)}</ul>
        </div>
      </div>
      <a href="{base}index.html#servicios">Servicios</a>
      <a href="{base}index.html#metodo">Método</a>
      <a class="btn btn--lime" href="https://wa.me/{WA_CONTACTO}?text={urllib.parse.quote('Hola, quiero anunciar mi empresa en ' + SITE)}" target="_blank" rel="noopener">Anúnciate ↗</a>
    </nav>
  </div>
</header>'''

def pie(base):
    return f'''<footer class="foot">
  <div class="wrap foot__in">
    <div>
      <a class="logo" href="{base}index.html"><span class="logo__mark">SU</span><span class="logo__txt">SERVICIOS<br><b>URGENTES</b></span></a>
      <p class="muted">Directorio de servicios urgentes por provincia. No prestamos los servicios: te ponemos en contacto directo con empresas locales.</p>
    </div>
    <div><h4>Servicios</h4><ul>{"".join(f"<li>{e(s['nombre'])}</li>" for s in SERVICIOS)}</ul></div>
    <div><h4>Directorio</h4><ul><li><a href="{base}index.html#provincias">Todas las provincias</a></li><li><a href="{base}index.html#metodo">Cómo funciona</a></li><li><a href="https://wa.me/{WA_CONTACTO}" target="_blank" rel="noopener">Contacto</a></li></ul></div>
  </div>
  <div class="wrap foot__legal"><span>© {date.today().year} {SITE}</span><span>Actualizado el {fecha_es(date.today())}</span></div>
</footer>
<script src="{base}js/main.js"></script>'''

MESES = ["enero","febrero","marzo","abril","mayo","junio","julio","agosto","septiembre","octubre","noviembre","diciembre"]
def fecha_es(d): return f"{d.day} de {MESES[d.month-1]} de {d.year}"

def head(title, desc, base, canonical):
    return f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{DOMINIO}{canonical}">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:type" content="website">
<link rel="icon" href="{base}img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Anton&family=Inter:wght@400;500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{base}css/estilos.css">
</head>
<body>'''

def marquee():
    t = " · ".join(s["nombre"].upper() for s in SERVICIOS) + " · "
    return f'<div class="marquee" aria-hidden="true"><div class="marquee__track"><span>{t*2}</span><span>{t*2}</span></div></div>'

# ---------- portada ----------
def portada():
    base = ""
    opciones = "".join(f'<option value="{e(p["nombre"])}" data-slug="{p["slug"]}"></option>' for p in PROVINCIAS)
    celdas = "".join(
        f'<a class="pcell" href="provincias/{p["slug"]}.html" data-name="{e(p["nombre"].lower())}">'
        f'<span class="pcell__n">{i+1:02d}</span><span class="pcell__name">{e(p["nombre"])}</span>'
        f'<span class="pcell__ca">{e(p["comunidad"])}</span><span class="pcell__go" aria-hidden="true">↗</span></a>'
        for i, p in enumerate(PROVINCIAS))
    servs = "".join(
        f'<div class="serv">{icon(s["slug"], 40)}<h3>{e(s["nombre"])}</h3><p>{e(s["desc"])}</p></div>' for s in SERVICIOS)
    faqs = [
        ("¿Qué es serviciosurgentes.es?", "Un directorio por provincia con una empresa de referencia para cada uno de los 8 servicios urgentes más demandados: cerrajería, fontanería, electricidad, reformas, pintura, carpintería, aluminio y cristalería."),
        ("¿Cómo contacto con una empresa?", "Entra en tu provincia y pulsa el botón de WhatsApp de la empresa para escribirle directamente, o visita su web. Sin formularios ni intermediarios."),
        ("¿Prestáis vosotros los servicios?", "No. Somos una plataforma de información. El presupuesto y el trabajo los acuerdas directamente con la empresa."),
        ("Tengo una empresa, ¿cómo aparezco?", "Cada provincia tiene una plaza por servicio. Escríbenos por WhatsApp desde el botón «Anúnciate» y te contamos la disponibilidad."),
    ]
    faq = "".join(f'<details class="faq__item"><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in faqs)
    total = len(PROVINCIAS)
    return head(f"Servicios urgentes en España: directorio por provincia | {SITE}",
                "Cerrajeros, fontaneros, electricistas, reformas, pintores, carpintería, aluminio y cristaleros en las 52 provincias. Contacto directo por WhatsApp.",
                base, "/") + cabecera(base) + f'''
<main id="contenido">
<section class="hero">
  <div class="wrap hero__in">
    <p class="tag">Directorio local · España</p>
    <h1>Servicios<br><span class="lime">urgentes</span><br><span class="outline">en España.</span></h1>
    <form class="search" id="buscador" autocomplete="off">
      <label for="q">Busca tu provincia</label>
      <div class="search__row">
        <input id="q" list="lista-provincias" placeholder="Madrid, Sevilla, Valencia…" required>
        <datalist id="lista-provincias">{opciones}</datalist>
        <button class="btn btn--lime" type="submit">Ver servicios</button>
      </div>
      <p class="search__err" role="alert" hidden>No encontramos esa provincia. Elige una de la lista.</p>
    </form>
    <div class="hero__lead">
      <p>Una urgencia no espera. Elige tu provincia y encontrarás <b>8 servicios urgentes</b> con su empresa local, su WhatsApp y su web para contactar al momento.</p>
      <a class="arrow" href="#provincias">Ver las {total} provincias ↓</a>
    </div>
    <ul class="stats"><li><b>{total}</b> provincias</li><li><b>8</b> servicios</li><li><b>{total*8}</b> empresas</li><li><b>24 h</b> contacto directo</li></ul>
  </div>
</section>
{marquee()}
<section class="sec" id="provincias">
  <div class="wrap">
    <div class="sec__head">
      <div><p class="tag">Cobertura nacional</p><h2>Elige tu<br>provincia</h2></div>
      <div class="sec__side">
        <p class="muted">Accede a la página de tu provincia y contacta directamente con la empresa de cada servicio.</p>
        <input class="filter" id="filtro" type="search" placeholder="Filtrar la lista…" aria-label="Filtrar provincias">
      </div>
    </div>
    <div class="pgrid" id="pgrid">{celdas}</div>
    <p class="muted empty" id="sin-resultados" hidden>Ninguna provincia coincide con la búsqueda.</p>
  </div>
</section>
<section class="sec sec--alt" id="servicios">
  <div class="wrap">
    <div class="sec__head"><div><p class="tag">Qué encontrarás</p><h2>8 servicios<br>en cada provincia</h2></div></div>
    <div class="servs">{servs}</div>
  </div>
</section>
<section class="sec" id="metodo">
  <div class="wrap">
    <div class="sec__head"><div><p class="tag">Método</p><h2>Rápido,<br>directo, local.</h2></div></div>
    <ol class="steps">
      <li><span>01</span><h3>Elige provincia</h3><p>Desde el menú o desde el cuadrante de provincias.</p></li>
      <li><span>02</span><h3>Elige servicio</h3><p>Ocho cajas, una por servicio, con su empresa local.</p></li>
      <li><span>03</span><h3>Escribe por WhatsApp</h3><p>Un toque y hablas directamente con la empresa.</p></li>
      <li><span>04</span><h3>Tú decides</h3><p>Visita su web, pide presupuesto y compara.</p></li>
    </ol>
  </div>
</section>
<section class="sec sec--alt" id="faq">
  <div class="wrap faq"><div><p class="tag">Dudas</p><h2>Preguntas<br>frecuentes</h2></div><div>{faq}</div></div>
</section>
</main>
''' + pie(base) + "\n</body>\n</html>\n"

# ---------- página de provincia ----------
def pagina_provincia(p, idx, empresas):
    base = "../"
    cajas = []
    for s in SERVICIOS:
        emp = empresas[p["slug"]][s["slug"]]
        nombre = emp.get("nombre") or f"Tu empresa de {s['singular']} en {p['nombre']}"
        img = emp.get("imagen") or f"img/servicios/{s['slug']}.svg"
        if not img.startswith(("http://", "https://", "/")):
            img = base + img
        msg = urllib.parse.quote(f"Hola, os contacto desde {SITE}. Necesito un servicio de {s['singular']} en {p['nombre']}.")
        wa = emp.get("whatsapp", "").replace("+", "").replace(" ", "")
        disponible = not wa and not emp.get("web")
        if wa:
            wa_link = f'<a class="btn btn--wa" href="https://wa.me/{wa}?text={msg}" target="_blank" rel="noopener">{WA_SVG} WhatsApp</a>'
        else:
            q = urllib.parse.quote(f"Hola, quiero la plaza de {s['nombre']} en {p['nombre']} en {SITE}")
            wa_link = f'<a class="btn btn--wa" href="https://wa.me/{WA_CONTACTO}?text={q}" target="_blank" rel="noopener">{WA_SVG} WhatsApp</a>'
        web = emp.get("web")
        web_link = (f'<a class="btn btn--ghost" href="{e(web)}" target="_blank" rel="noopener">Web ↗</a>' if web
                    else '<span class="btn btn--ghost is-off" aria-disabled="true">Web ↗</span>')
        badge = '<span class="card__badge">Plaza disponible</span>' if disponible else ''
        cajas.append(f'''<article class="card" id="{s["slug"]}">
  <div class="card__img"><img src="{e(img)}" alt="{e(nombre)}" loading="lazy" width="640" height="400">{badge}</div>
  <div class="card__body">
    <p class="card__serv">{icon(s["slug"], 20)} {e(s["nombre"])}</p>
    <h3>{e(nombre)}</h3>
    <p class="muted">{e(s["desc"])}</p>
    <div class="card__cta">{wa_link}{web_link}</div>
  </div>
</article>''')
    chips = "".join(f'<a class="chip" href="#{s["slug"]}">{icon(s["slug"], 16)}{e(s["nombre"])}</a>' for s in SERVICIOS)
    prev_p = PROVINCIAS[idx-1]; next_p = PROVINCIAS[(idx+1) % len(PROVINCIAS)]
    otras = "".join(f'<a href="{q["slug"]}.html">{e(q["nombre"])}</a>' for q in PROVINCIAS
                    if q["comunidad"] == p["comunidad"] and q["slug"] != p["slug"])
    otras_html = f'<div class="near"><h4>Otras provincias de {e(p["comunidad"])}</h4><div>{otras}</div></div>' if otras else ""
    return head(f"Servicios urgentes en {p['nombre']}: cerrajeros, fontaneros y más | {SITE}",
                f"Cerrajeros, fontaneros, electricistas, reformas, pintores, carpintería, aluminio y cristaleros en {p['nombre']}. Contacto directo por WhatsApp y web.",
                base, f"/provincias/{p['slug']}") + cabecera(base) + f'''
<main id="contenido">
<section class="phero">
  <div class="wrap">
    <nav class="crumbs" aria-label="Migas de pan"><a href="../index.html">Inicio</a> / <a href="../index.html#provincias">Provincias</a> / <span>{e(p["nombre"])}</span></nav>
    <p class="tag">{e(p["comunidad"])} · Guía local</p>
    <h1>Servicios urgentes<br><span class="lime">en {e(p["nombre"])}</span></h1>
    <p class="phero__lead">Estas son las empresas de referencia en {e(p["nombre"])} para los 8 servicios urgentes. Pulsa WhatsApp para escribirles directamente o visita su web.</p>
    <div class="chips">{chips}</div>
  </div>
</section>
{marquee()}
<section class="sec">
  <div class="wrap">
    <div class="cards">{"".join(cajas)}</div>
    <p class="note muted">Actualizado el {fecha_es(date.today())} · {SITE} es una plataforma de información: el presupuesto y el trabajo se acuerdan directamente con cada empresa.</p>
    {otras_html}
    <div class="pager">
      <a href="{prev_p["slug"]}.html">← {e(prev_p["nombre"])}</a>
      <a href="../index.html#provincias">Todas las provincias</a>
      <a href="{next_p["slug"]}.html">{e(next_p["nombre"])} →</a>
    </div>
  </div>
</section>
</main>
''' + pie(base) + "\n</body>\n</html>\n"

WA_SVG = '<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.2-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.8 11.9 11.9 0 0 0 4.6 4c1.7.7 2.3.8 3.2.7.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.2-1.2-.1-.1-.3-.2-.5-.3z"/></svg>'

def sitemap():
    urls = [f"{DOMINIO}/"] + [f"{DOMINIO}/provincias/{p['slug']}" for p in PROVINCIAS]
    body = "".join(f"<url><loc>{u}</loc><lastmod>{date.today().isoformat()}</lastmod></url>" for u in urls)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{body}</urlset>\n'

def main():
    for s in SERVICIOS:
        imagen_defecto(s)
    empresas = cargar_empresas()
    w = lambda rel, txt: open(os.path.join(ROOT, rel), "w", encoding="utf-8").write(txt)
    w("index.html", portada())
    for i, p in enumerate(PROVINCIAS):
        w(f"provincias/{p['slug']}.html", pagina_provincia(p, i, empresas))
    w("sitemap.xml", sitemap())
    w("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {DOMINIO}/sitemap.xml\n")
    print(f"Generadas {1 + len(PROVINCIAS)} páginas.")

if __name__ == "__main__":
    main()
