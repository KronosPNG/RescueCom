import { initMap, renderMarkers, flyToLocation } from './modules/map.js';
import { getRequests, addRequest, setRequests, parseEmergencyData } from './modules/data.js';
import { renderFeed, highlightCard, updateStats, renderDetailPanel } from './modules/ui.js';

// Initial Data - 3 Sample Requests for Visualization
const initialData = [
    {
        id: 'REQ-DEMO-1',
        time: '10:42',
        type: 'Emergenza Medica',
        desc: 'Sospetto arresto cardiaco in luogo pubblico.',
        priority: 'high',
        location: { lat: 40.6824, lng: 14.7681 }, // Salerno Centro
        address: 'Corso Vittorio Emanuele, Salerno',
        user: { name: 'Mario Rossi', age: 50, blood: 'A+', conditions: ['Ipertensione'] }
    },
    {
        id: 'REQ-DEMO-2',
        time: '10:30',
        type: 'Incendio',
        desc: 'Fumo nero visibile dal balcone al terzo piano.',
        priority: 'low',
        location: { lat: 40.6750, lng: 14.7700 }, // Zona Stazione
        address: 'Piazza della Concordia, Salerno',
        user: { name: 'Giuseppe Verdi', age: 35, blood: 'Unknown', conditions: [] }
    },
    {
        id: 'REQ-DEMO-3',
        time: '10:15',
        type: 'Incidente Stradale',
        desc: 'Tamponamento lieve, richiesta controllo medico.',
        priority: 'medium',
        location: { lat: 40.6800, lng: 14.7600 }, // Lungomare
        address: 'Lungomare Trieste, Salerno',
        user: { name: 'Anna Bianchi', age: 28, blood: '0+', conditions: ['Nessuna'] }
    }
];

document.addEventListener('DOMContentLoaded', () => {
    // 1. Initialize Map
    initMap('mapContainer', [40.6824, 14.7681]);

    // 2. Initialize Data
    setRequests(initialData);

    // 3. Render Initial State
    updateUI();

    // 3. Setup Sorting
    setupSorting();

    // 4. Check for existing data (e.g. from local storage or previous session)
    // const stored = localStorage.getItem('rescuecom_requests');
    // if (stored) setRequests(JSON.parse(stored));
    // updateUI();
});

let isSortedBySeverity = false;

function setupSorting() {
    const filterIcon = document.querySelector('.bi-filter-right');
    if (filterIcon) {
        filterIcon.addEventListener('click', toggleSort);
    }
}

function toggleSort() {
    isSortedBySeverity = !isSortedBySeverity;
    const requests = getRequests();

    const feedTitle = document.getElementById('feedTitle');

    if (isSortedBySeverity) {
        // Sort by Priority: High > Medium > Low
        const priorityMap = { 'high': 3, 'medium': 2, 'low': 1 };
        requests.sort((a, b) => {
            const pA = priorityMap[a.priority] || 0;
            const pB = priorityMap[b.priority] || 0;
            return pB - pA; // Descending order
        });
        // Visual feedback
        document.querySelector('.bi-filter-right').style.color = 'var(--accent-orange)';
        if (feedTitle) feedTitle.textContent = "Ordina per gravità";
    } else {
        // Revert to Time based
        requests.sort((a, b) => b.time.localeCompare(a.time));
        document.querySelector('.bi-filter-right').style.color = '';
        if (feedTitle) feedTitle.textContent = "Ordine temporale";
    }

    // Re-render
    renderFeed(requests, 'feedList', handleRequestSelect);
}

function updateUI() {
    const requests = getRequests();
    renderFeed(requests, 'feedList', handleRequestSelect);
    renderMarkers(requests, handleRequestSelect);
    updateStats(requests.length);
}

function handleRequestSelect(req) {
    highlightCard(req.id, 'feedList');
    renderDetailPanel(req, 'detailPanel', handleContact, handleDispatch);
    flyToLocation(req.location.lat, req.location.lng);
}

function handleContact(req) {
    console.log(`[Action] Contacting user: ${req.user.name} (REQ: ${req.id})`);
    alert(`📞 Call initiated to ${req.user.name}\nRequest ID: ${req.id}`);
}

function handleDispatch(req) {
    console.log(`[Action] Dispatching units to: ${req.address} (REQ: ${req.id})`);
    alert(`🚑 Rescue Team Dispatched!\nLocation: ${req.address}\nPriority: ${req.priority.toUpperCase()}`);
}

// Global entry point for Backend Pushes (WebSocket / SSE / HTTP Response)
window.addEmergencyRequest = (rawEmergencyData) => {
    console.log("📥 [Dashboard] Received Data:", rawEmergencyData);
    const newReq = parseEmergencyData(rawEmergencyData);
    addRequest(newReq);
    updateUI();

    // Optional: Auto-focus on high priority
    if (newReq.priority === 'high' || newReq.priority === 'critical') {
        handleRequestSelect(newReq);
    }
};
