import { getRequests, setRequests, parseEmergencyData } from './modules/data.js';
import { renderFeed } from './modules/ui.js';

// Configuration
const REFRESH_INTERVAL = 10000; // 10 seconds

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    init();
});

function init() {
    console.log('RescueCom Dashboard Initializing...');

    // Render JSON details for SSR pages
    renderJsonDetails();

    // Only run Client-Side Fetching if we are on the legacy CSR dashboard
    // We check if the feed containers exist
    if (document.getElementById('feed-grave')) {
        // Initial Render
        updateDashboard();
        // Siumulate initial API fetch
        fetchApiData();
        // Poll every 5 seconds
        setInterval(fetchApiData, REFRESH_INTERVAL);
    }
}

function renderJsonDetails() {
    document.querySelectorAll('[data-json]').forEach(el => {
        try {
            // Avoid double rendering if called multiple times
            if (el.dataset.rendered) return;

            const rawJson = el.dataset.json;
            if (!rawJson || rawJson === 'None' || rawJson === 'null') return;

            const data = JSON.parse(rawJson);
            if (!data || Object.keys(data).length === 0) return;

            const createList = (obj) => {
                const ul = document.createElement('ul');
                ul.style.marginTop = '5px';
                ul.style.paddingLeft = '20px';

                for (const [key, value] of Object.entries(obj)) {
                    const li = document.createElement('li');
                    li.style.marginBottom = '2px';
                    li.innerHTML = `<strong>${key}:</strong> `;

                    if (typeof value === 'object' && value !== null) {
                        li.appendChild(createList(value));
                    } else {
                        li.innerHTML += `<span style="color: #334155;">${value}</span>`;
                    }
                    ul.appendChild(li);
                }
                return ul;
            };

            el.appendChild(createList(data));
            el.dataset.rendered = 'true';

        } catch (e) {
            console.warn('Error parsing JSON details for element:', el, e);
        }
    });
}

// --- Real API Integration ---

async function fetchApiData() {
    console.log('Fetching data from API...');
    try {
        const response = await fetch('/api/requests');

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        // Process data
        const processed = data.map(d => parseEmergencyData(d));

        // Update State
        setRequests(processed);

        // Update UI
        updateDashboard();
        console.log('Dashboard updated with API data');

    } catch (error) {
        console.error('API Error:', error);
        // Optional: Show error state in UI
    }
}

// Export so other modules (like a WebSocket handler) can trigger updates
export function updateDashboard() {
    const allRequests = getRequests();

    // Filter by category
    const grave = allRequests.filter(r => r.priority === 'high');
    const moderato = allRequests.filter(r => r.priority === 'medium');
    const lieve = allRequests.filter(r => r.priority === 'low');

    // Render Feeds
    renderFeed(grave, 'feed-grave', onCardClick);
    if (grave.length === 0) showEmpty('feed-grave', 'Nessuna emergenza grave.');

    renderFeed(moderato, 'feed-moderato', onCardClick);
    if (moderato.length === 0) showEmpty('feed-moderato', 'Nessuna richiesta.');

    renderFeed(lieve, 'feed-lieve', onCardClick);
    if (lieve.length === 0) showEmpty('feed-lieve', 'Nessuna richiesta.');
}

function showEmpty(containerId, message) {
    const container = document.getElementById(containerId);
    if (container) {
        container.innerHTML = `<p style="color: #94a3b8; font-style: italic; padding: 10px;">${message}</p>`;
    }
}

function onCardClick(req) {
    console.log('Card clicked:', req.id);
    // Future: Open detail view or modal
}
