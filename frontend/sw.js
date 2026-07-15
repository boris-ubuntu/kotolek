// Service Worker для Котолёк — кеширует оболочку приложения,
// чтобы открывалось мгновенно и работало офлайн (как нативное приложение).
const CACHE = 'kotolek-v2';
const SHELL = [
  '/',
  '/index.html',
  '/css/style.css',
  '/js/utils.js',
  '/js/api.js',
  '/js/app.js',
  '/js/components/balance.js',
  '/js/components/chart.js',
  '/js/components/histogram.js',
  '/js/components/graph.js',
  '/js/components/recent.js',
  '/js/components/modal.js',
  '/js/components/delete-modal.js',
  '/manifest.webmanifest',
  '/icon-192.png',
  '/icon-512.png',
  '/icon-maskable-512.png',
  '/favicon.svg',
  'https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE).then((cache) => cache.addAll(SHELL)).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  const req = event.request;
  if (req.method !== 'GET') return;

  const url = new URL(req.url);

  // API — всегда пробуем сеть, при ошибке отдаём кеш (если есть)
  if (url.pathname.startsWith('/api/')) {
    event.respondWith(
      fetch(req).catch(() => caches.match(req))
    );
    return;
  }

  // Статика приложения — network-first: сначала пробуем сеть (чтобы
  // новые деплои применялись сразу), при сбое отдаём кеш (офлайн).
  event.respondWith(
    fetch(req).then((res) => {
      if (res && res.status === 200) {
        const copy = res.clone();
        caches.open(CACHE).then((cache) => cache.put(req, copy));
      }
      return res;
    }).catch(() => caches.match(req))
  );
});