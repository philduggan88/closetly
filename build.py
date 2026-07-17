#!/usr/bin/env python3
"""Build the static public storefront (The Closet) from ../shop.html + ../data/closet.json.

Run from anywhere: python3 ~/closetly/mobile/build.py
Output: index.html, data.js, sw.js, photos/, fonts/ in this directory.
Publish flow: run this, then commit+push the mobile/ repo (see README).
"""
import hashlib
import json
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.dirname(HERE)

PUBLIC_PIECE_FIELDS = [
    "id", "name", "brand", "category", "size", "color", "condition",
    "photo", "status", "rent_price_cents", "sale_price_cents",
]


def must_replace(html, old, new):
    if old not in html:
        raise SystemExit("build.py: expected marker not found in shop.html: %r" % old[:60])
    return html.replace(old, new)


def build_data():
    with open(os.path.join(APP, "data", "closet.json"), encoding="utf-8") as f:
        state = json.load(f)
    pieces = []
    for p in state["pieces"]:
        if p.get("status") not in ("rent", "sell"):
            continue
        pub = {k: p.get(k) for k in PUBLIC_PIECE_FIELDS}
        # retail strikethrough on sale cards uses purchase price — only expose it there
        if p.get("status") == "sell":
            pub["purchase_price_cents"] = p.get("purchase_price_cents")
        pieces.append(pub)
    data = {"meta": {"contact": state["meta"]["contact"]}, "pieces": pieces}
    js = "window.CLOSET = " + json.dumps(data, ensure_ascii=False, indent=1) + ";\n"
    with open(os.path.join(HERE, "data.js"), "w", encoding="utf-8") as f:
        f.write(js)
    return data, js


def build_html():
    with open(os.path.join(APP, "shop.html"), encoding="utf-8") as f:
        html = f.read()

    html = must_replace(html, 'url("/fonts/', 'url("fonts/')
    html = must_replace(html, 'src="/photos/${p.photo}"', 'src="photos/${p.photo}"')
    html = must_replace(
        html,
        'Curated on <a href="/">closetly</a> ·',
        "Curated on closetly ·",
    )
    html = must_replace(
        html,
        """fetch("/api/closet").then(r => {
  if (!r.ok) throw new Error("failed to load: " + r.status);
  return r.json();
}).then(s => { state = s; render(); });""",
        """state = window.CLOSET;
render();
if ("serviceWorker" in navigator) navigator.serviceWorker.register("sw.js");""",
    )
    html = must_replace(
        html,
        "<title>The Closet — rent &amp; resale</title>",
        """<title>The Closet — rent &amp; resale</title>
<link rel="manifest" href="manifest.json">
<meta name="theme-color" content="#f4efe6">
<link rel="apple-touch-icon" href="icon-180.png">
<link rel="icon" type="image/png" href="icon-192.png">
<script src="data.js"></script>""",
    )
    with open(os.path.join(HERE, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    return html


def sync_assets(data):
    fonts_src = os.path.join(APP, "fonts")
    fonts_dst = os.path.join(HERE, "fonts")
    os.makedirs(fonts_dst, exist_ok=True)
    for f in os.listdir(fonts_src):
        if f.endswith(".woff2"):
            shutil.copy2(os.path.join(fonts_src, f), os.path.join(fonts_dst, f))

    photos_dst = os.path.join(HERE, "photos")
    os.makedirs(photos_dst, exist_ok=True)
    wanted = {p["photo"] for p in data["pieces"] if p.get("photo")}
    for f in wanted:
        shutil.copy2(os.path.join(APP, "data", "photos", f), os.path.join(photos_dst, f))
    for f in os.listdir(photos_dst):
        if f not in wanted:
            os.remove(os.path.join(photos_dst, f))
    return wanted


def build_sw(version_seed, photo_files):
    assets = ["./", "index.html", "data.js", "manifest.json",
              "fonts/playfair-display.woff2", "fonts/playfair-display-italic.woff2",
              "fonts/inter.woff2"] + sorted("photos/" + f for f in photo_files)
    version = hashlib.sha1(version_seed.encode("utf-8")).hexdigest()[:10]
    sw = """const CACHE = "closet-%s";
const ASSETS = %s;
self.addEventListener("install", e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(ASSETS)).then(() => self.skipWaiting()));
});
self.addEventListener("activate", e => {
  e.waitUntil(caches.keys().then(keys =>
    Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
  ).then(() => self.clients.claim()));
});
self.addEventListener("fetch", e => {
  e.respondWith(caches.match(e.request, {ignoreSearch: true}).then(hit => hit || fetch(e.request)));
});
""" % (version, json.dumps(assets))
    with open(os.path.join(HERE, "sw.js"), "w", encoding="utf-8") as f:
        f.write(sw)
    return version


def main():
    data, js = build_data()
    html = build_html()
    photos = sync_assets(data)
    version = build_sw(html + js, photos)
    print("built: %d pieces listed, %d photos, cache closet-%s" % (len(data["pieces"]), len(photos), version))


if __name__ == "__main__":
    main()
