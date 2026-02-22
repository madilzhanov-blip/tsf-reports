self.addEventListener('install', () => {
  console.log('Service Worker installed');
});

self.addEventListener('fetch', () => {});
self.addEventListener('install', event => {
  self.skipWaiting();
});

self.addEventListener('activate', event => {
  clients.claim();
});