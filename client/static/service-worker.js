const CACHE_NAME = 'rescuecom-v1';
const ASSETS_TO_CACHE = [
    '/',
    '/welcome',
    '/legal-info',
    '/static/css/style.css',
    '/static/css/welcome.css',
    '/static/css/bootstrap.min.css',
    '/static/css/bootstrap-icons.min.css',
    '/static/js/bootstrap.bundle.min.js',
    '/static/js/welcome.js',
    '/static/js/legal-info.js',
    '/static/img/logoDGPR.png',
    '/static/css/fonts/Inter-VariableFont_opsz,wght.ttf',
    '/static/css/fonts/bootstrap-icons.woff2'
    // Add other fonts or images as needed
];

// Install Event
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then((cache) => {
                console.log('Opened cache');
                return cache.addAll(ASSETS_TO_CACHE);
            })
    );
});

// Activate Event
self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cacheName) => {
                    if (cacheName !== CACHE_NAME) {
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
});

// Fetch Event
self.addEventListener('fetch', (event) => {
    event.respondWith(
        caches.match(event.request)
            .then((response) => {
                // Cache hit - return response
                if (response) {
                    return response;
                }
                return fetch(event.request);
            })
    );
});
