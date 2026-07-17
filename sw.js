const CACHE = "closet-d49c3305b1";
const ASSETS = ["./", "index.html", "data.js", "manifest.json", "fonts/playfair-display.woff2", "fonts/playfair-display-italic.woff2", "fonts/inter.woff2", "photos/jas-cny-floral.jpg", "photos/jas-fringe.jpg", "photos/jas-london-polka.jpg", "photos/jas-mermaid.jpg", "photos/jas2-corset-gown.jpg", "photos/jas2-crochet-pants.jpg", "photos/jas2-dg-skirt.jpg", "photos/jas2-hibiscus-top.jpg", "photos/jas2-lace-mini.jpg", "photos/jas2-meshki-yellow.jpg", "photos/jas2-sandro-knit.jpg", "photos/jas2-silver-maxi.jpg"];
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
