let map;
let markers = [];

// Mock Data with Real Coordinates (Salerno Area)
const requests = [
    {
        id: 'REQ-1024',
        time: '10:42',
        type: 'Emergenza Medica',
        desc: 'Utente segnala dolore toracico acuto e difficoltà respiratorie. Possibile arresto cardiaco.',
        priority: 'high',
        location: { lat: 40.6824, lng: 14.7681 }, // Salerno Centro
        user: {
            name: 'Marco Rossi',
            age: 54,
            blood: 'A+',
            conditions: ['Ipertensione', 'Diabete Tipo 2']
        }
    },
    {
        id: 'REQ-1023',
        time: '10:38',
        type: 'Disperso',
        desc: 'Segnale GPS debole. Ultima posizione nota vicino al crinale nord. Gruppo di 3 persone.',
        priority: 'medium',
        location: { lat: 40.6950, lng: 14.7900 }, // Zone collinari
        user: {
            name: 'Giulia Bianchi',
            age: 29,
            blood: '0+',
            conditions: ['Nessuna']
        }
    },
    {
        id: 'REQ-1022',
        time: '10:15',
        type: 'Richiesta Supporto',
        desc: 'Veicolo in panne, richiesta assistenza logistica. Nessuna urgenza medica immediata.',
        priority: 'low',
        location: { lat: 40.6700, lng: 14.7500 }, // Porto
        user: {
            name: 'Luca Verdi',
            age: 41,
            blood: 'B-',
            conditions: ['Asma allergica']
        }
    },
    {
        id: 'REQ-1021',
        time: '09:55',
        type: 'Incidente',
        desc: 'Caduta da parete rocciosa, sospetta frattura arti inferiori. Cosciente.',
        priority: 'high',
        location: { lat: 40.7100, lng: 14.7200 }, // Vietri sul Mare
        user: {
            name: 'Elena Neri',
            age: 33,
            blood: 'AB+',
            conditions: ['Nessuna']
        }
    }
];

function initMap() {
    // Stile "Dark Mode" per la mappa
    const darkMapStyle = [
        { elementType: "geometry", stylers: [{ color: "#242f3e" }] },
        { elementType: "labels.text.stroke", stylers: [{ color: "#242f3e" }] },
        { elementType: "labels.text.fill", stylers: [{ color: "#746855" }] },
        {
            featureType: "administrative.locality",
            elementType: "labels.text.fill",
            stylers: [{ color: "#d59563" }],
        },
        {
            featureType: "poi",
            elementType: "labels.text.fill",
            stylers: [{ color: "#d59563" }],
        },
        {
            featureType: "poi.park",
            elementType: "geometry",
            stylers: [{ color: "#263c3f" }],
        },
        {
            featureType: "poi.park",
            elementType: "labels.text.fill",
            stylers: [{ color: "#6b9a76" }],
        },
        {
            featureType: "road",
            elementType: "geometry",
            stylers: [{ color: "#38414e" }],
        },
        {
            featureType: "road",
            elementType: "geometry.stroke",
            stylers: [{ color: "#212a37" }],
        },
        {
            featureType: "road",
            elementType: "labels.text.fill",
            stylers: [{ color: "#9ca5b3" }],
        },
        {
            featureType: "road.highway",
            elementType: "geometry",
            stylers: [{ color: "#746855" }],
        },
        {
            featureType: "road.highway",
            elementType: "geometry.stroke",
            stylers: [{ color: "#1f2835" }],
        },
        {
            featureType: "road.highway",
            elementType: "labels.text.fill",
            stylers: [{ color: "#f3d19c" }],
        },
        {
            featureType: "transit",
            elementType: "geometry",
            stylers: [{ color: "#2f3948" }],
        },
        {
            featureType: "transit.station",
            elementType: "labels.text.fill",
            stylers: [{ color: "#d59563" }],
        },
        {
            featureType: "water",
            elementType: "geometry",
            stylers: [{ color: "#17263c" }],
        },
        {
            featureType: "water",
            elementType: "labels.text.fill",
            stylers: [{ color: "#515c6d" }],
        },
        {
            featureType: "water",
            elementType: "labels.text.stroke",
            stylers: [{ color: "#17263c" }],
        },
    ];

    map = new google.maps.Map(document.getElementById("mapContainer"), {
        center: { lat: 40.6824, lng: 14.7681 }, // Salerno
        zoom: 13,
        styles: darkMapStyle,
        disableDefaultUI: true, // Interfaccia pulita
        zoomControl: true,
    });

    renderMapMarkers();
}

function renderMapMarkers() {
    // Clear existing markers
    markers.forEach(m => m.setMap(null));
    markers = [];

    requests.forEach(req => {
        // Colore in base alla priorità
        let iconColor;
        switch (req.priority) {
            case 'high': iconColor = 'http://maps.google.com/mapfiles/ms/icons/red-dot.png'; break;
            case 'medium': iconColor = 'http://maps.google.com/mapfiles/ms/icons/orange-dot.png'; break;
            case 'low': iconColor = 'http://maps.google.com/mapfiles/ms/icons/green-dot.png'; break;
            default: iconColor = 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png';
        }

        const marker = new google.maps.Marker({
            position: req.location,
            map: map,
            title: req.type,
            icon: iconColor,
            animation: req.priority === 'high' ? google.maps.Animation.BOUNCE : null
        });

        marker.addListener("click", () => {
            selectRequest(req);
        });

        markers.push(marker);
    });
}

function selectRequest(req) {
    const detailPanel = document.getElementById('detailPanel');
    const feedList = document.getElementById('feedList');

    // Highlight active card
    const cards = feedList.querySelectorAll('.request-card');
    cards.forEach(c => {
        if (c.querySelector('.card-id').textContent === req.id) {
            c.style.backgroundColor = 'rgba(255, 255, 255, 0.15)';
        } else {
            c.style.backgroundColor = '';
        }
    });

    // Pan map to location
    map.panTo(req.location);
    if (map.getZoom() < 15) {
        map.setZoom(15);
    }

    // Render Details
    const conditionsHtml = req.user.conditions.map(c => `<span class="health-badge">${c}</span>`).join('');

    detailPanel.innerHTML = `
        <div class="detail-header">
            <div class="detail-title">${req.type}</div>
            <div class="detail-subtitle">${req.id} • ${req.time}</div>
        </div>

        <div class="info-group">
            <div class="info-label">Stato Emergenza</div>
            <div class="info-value">
                <span style="color: var(--accent-${req.priority === 'high' ? 'red' : req.priority === 'medium' ? 'orange' : 'green'})">
                    ${req.priority.toUpperCase()} PRIORITY
                </span>
            </div>
        </div>

        <div class="info-group">
            <div class="info-label">Descrizione</div>
            <div class="info-value" style="font-size: 0.95rem; line-height: 1.5;">${req.desc}</div>
        </div>

        <div class="info-group">
            <div class="info-label">Dati Paziente</div>
            <div class="info-value"><strong>Nome:</strong> ${req.user.name}</div>
            <div class="info-value"><strong>Età:</strong> ${req.user.age}</div>
            <div class="info-value"><strong>Gruppo Sanguigno:</strong> ${req.user.blood}</div>
        </div>

         <div class="info-group">
            <div class="info-label">Condizioni Mediche Note</div>
            <div class="info-value">${conditionsHtml}</div>
        </div>

        <div class="info-group">
            <div class="info-label">Posizione</div>
            <div class="info-value">Lat: ${req.location.lat}<br>Lng: ${req.location.lng}</div>
        </div>

        <div class="action-bar">
            <button class="btn btn-secondary" onclick="alert('Messaggio inviato a ${req.user.name}')">Contatta</button>
            <button class="btn btn-primary" onclick="alert('Squadra inviata per ${req.id}')">Invia Soccorsi</button>
        </div>
    `;
}

document.addEventListener('DOMContentLoaded', () => {
    const feedList = document.getElementById('feedList');
    const activeRequestsCount = document.getElementById('activeRequestsCount');

    // Update Header Status
    if (activeRequestsCount) {
        activeRequestsCount.textContent = requests.length;
    }

    // Render Request Cards
    feedList.innerHTML = '';
    requests.forEach(req => {
        const card = document.createElement('div');
        card.className = `request-card priority-${req.priority}`;
        card.innerHTML = `
            <div class="card-top">
                <span class="card-id">${req.id}</span>
                <span class="card-time">${req.time}</span>
            </div>
            <div class="card-title">${req.type}</div>
            <div class="card-preview">${req.desc}</div>
        `;
        card.addEventListener('click', () => selectRequest(req));
        feedList.appendChild(card);
    });
});

// Expose initMap to global scope for the Google Maps callback
window.initMap = initMap;
