const CACHE = "closet-7040793d9b";
const ASSETS = ["./", "index.html", "data.js", "manifest.json", "fonts/playfair-display.woff2", "fonts/playfair-display-italic.woff2", "fonts/inter.woff2", "photos/jas-cny-floral.jpg", "photos/jas-fringe.jpg", "photos/jas-london-polka.jpg", "photos/jas-mermaid.jpg"];
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
