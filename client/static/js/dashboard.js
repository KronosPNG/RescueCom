import { initMap, renderMarkers, flyToLocation } from './modules/map.js';
import { getRequests, addRequest, setRequests, parseEmergencyData } from './modules/data.js';
import { renderFeed, highlightCard, updateStats, renderDetailPanel } from './modules/ui.js';

// Initial Mock Data
const initialData = [
    {
        id: 'REQ-1029',
        time: '10:42',
        type: 'Emergenza Medica',
        desc: 'Utente segnala dolore toracico acuto e difficoltà respiratorie. Possibile arresto cardiaco.',
        priority: 'high',
        location: { lat: 40.7824, lng: 14.7981 },
        address: 'Corso Vittorio Emanuele 123, Salerno',
        user: { name: 'Marco Rossi', age: 54, blood: 'A+', conditions: ['Ipertensione', 'Diabete Tipo 2'] }
    },
    {
        id: 'REQ-1028',
        time: '10:40',
        type: 'Emergenza Medica',
        desc: 'Utente segnala dolore toracico acuto e difficoltà respiratorie. Possibile arresto cardiaco.',
        priority: 'high',
        location: { lat: 40.6824, lng: 14.7681 },
        address: 'Via dei Principati 45, Salerno',
        user: { name: 'Giuseppe Verdi', age: 60, blood: 'A-', conditions: ['Ipertensione'] }
    },
    {
        id: 'REQ-1027',
        time: '10:35',
        type: 'Emergenza Medica',
        desc: 'Caduta accidentale, dolore alla gamba sinistra.',
        priority: 'medium',
        location: { lat: 40.6850, lng: 14.7700 },
        address: 'Via Roma 10, Salerno',
        user: { name: 'Maria Esposito', age: 72, blood: '0+', conditions: ['Osteoporosi'] }
    },
    {
        id: 'REQ-1026',
        time: '10:30',
        type: 'Incidente Stradale',
        desc: 'Tamponamento tra due veicoli, nessun ferito grave segnalato.',
        priority: 'medium',
        location: { lat: 40.6800, lng: 14.7600 },
        address: 'Piazza della Concordia, Salerno',
        user: { name: 'Antonio Russo', age: 35, blood: 'B+', conditions: ['Nessuna'] }
    },
    {
        id: 'REQ-1025',
        time: '10:25',
        type: 'Malore',
        desc: 'Svenimento in luogo pubblico, ripreso conoscenza.',
        priority: 'medium',
        location: { lat: 40.6780, lng: 14.7550 },
        address: 'Via Mercanti 8, Salerno',
        user: { name: 'Francesca Costa', age: 24, blood: 'AB-', conditions: ['Nessuna'] }
    },
    {
        id: 'REQ-1023',
        time: '10:38',
        type: 'Disperso',
        desc: 'Segnale GPS debole. Ultima posizione nota vicino al crinale nord. Gruppo di 3 persone.',
        priority: 'medium',
        location: { lat: 40.6950, lng: 14.7900 },
        address: 'Sentiero degli Dei, Agerola',
        user: { name: 'Giulia Bianchi', age: 29, blood: '0+', conditions: ['Nessuna'] }
    },
    {
        id: 'REQ-1022',
        time: '10:15',
        type: 'Richiesta Supporto',
        desc: 'Veicolo in panne, richiesta assistenza logistica. Nessuna urgenza medica immediata.',
        priority: 'low',
        location: { lat: 40.6700, lng: 14.7500 },
        address: 'SP 175 Litoranea, Pontecagnano',
        user: { name: 'Luca Verdi', age: 41, blood: 'B-', conditions: ['Asma allergica'] }
    },
    {
        id: 'REQ-1021',
        time: '09:55',
        type: 'Incidente',
        desc: 'Caduta da parete rocciosa, sospetta frattura arti inferiori. Cosciente.',
        priority: 'high',
        location: { lat: 40.7100, lng: 14.7200 },
        address: 'Monte Faito, Vico Equense',
        user: { name: 'Elena Neri', age: 33, blood: 'AB+', conditions: ['Nessuna'] }
    }
];

document.addEventListener('DOMContentLoaded', () => {
    // 1. Initialize Data
    setRequests(initialData);

    // 2. Initialize Map
    initMap('mapContainer', [40.6824, 14.7681]);

    // 3. Render Initial State
    updateUI();

    // 4. Setup Sorting
    setupSorting();
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
        // Revert to Time based (assuming IDs are somewhat chronological or just re-fetch original order if we stored it, 
        // but sorting by ID descending is a good proxy for time here as IDs are increasing)
        // actually existing 'requests' array is mutated. 
        // For simplicity, let's just sort by time string (descending) as a fallback
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

// Global functions for simulation
window.addEmergencyRequest = (rawEmergencyData) => {
    const newReq = parseEmergencyData(rawEmergencyData);
    addRequest(newReq);
    updateUI();

    // Auto-select the new request
    handleRequestSelect(newReq);

    if (newReq.priority === 'high') {
        console.log("High priority emergency received!");
    }
};

window.simulateBackendPush = () => {
    const mockPayload = {
        "id": Math.floor(Math.random() * 10000),
        "user_uuid": "550e8400-e29b-41d4-a716",
        "position": "41.117145,16.871871",
        "address": "Via Sparano da Bari",
        "city": "Bari",
        "street_number": 10,
        "place_description": "Vicino all'ingresso del negozio",
        "photo_b64": "",
        "resolved": false,
        "details_json": "{\"gravity\": \"high\", \"type\": \"Incidente Stradale\"}"
    };
    console.log("Simulating Backend Push...", mockPayload);
    window.addEmergencyRequest(mockPayload);
};
