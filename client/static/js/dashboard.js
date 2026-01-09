import { getRequests, setRequests, parseEmergencyData } from './modules/data.js';
import { renderFeed } from './modules/ui.js';

// Configuration
const REFRESH_INTERVAL = 10000; // 10 seconds
// Note: Set up API polling here when backend is ready

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    init();
});

function init() {
    console.log('RescueCom Dashboard Initializing...');

    // Initial Render (will be empty usually)
    updateDashboard();

    // Siumulate initial API fetch
    fetchApiData();

    // Poll every 5 seconds
    setInterval(fetchApiData, REFRESH_INTERVAL);
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
