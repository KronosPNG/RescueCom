// Module: Map Logic (Leaflet)

let map;
let markers = [];

export function initMap(mapContainerId, initialCoords) {
    if (!document.getElementById(mapContainerId)) return;

    map = L.map(mapContainerId).setView(initialCoords, 13);

    // Add Standard OpenStreetMap Tile Layer
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        maxZoom: 19
    }).addTo(map);

    return map;
}

export function renderMarkers(requests, onMarkerClick) {
    if (!map) return;

    // Clear existing markers
    markers.forEach(m => map.removeLayer(m));
    markers = [];

    requests.forEach(req => {
        // Define simple colored circle markers
        const colorMap = {
            'high': 'red',
            'medium': 'orange',
            'low': 'green'
        };
        const color = colorMap[req.priority] || 'blue';

        const marker = L.circleMarker([req.location.lat, req.location.lng], {
            color: color,
            fillColor: color,
            fillOpacity: 0.7,
            radius: req.priority === 'high' ? 12 : 8,
            weight: 2
        }).addTo(map);

        marker.bindTooltip(`<b>${req.type}</b>`);

        if (onMarkerClick) {
            marker.on("click", () => onMarkerClick(req));
        }

        markers.push(marker);
    });
}

export function flyToLocation(lat, lng, zoom = 16) {
    if (!map) return;
    map.flyTo([lat, lng], zoom, {
        animate: true,
        duration: 1.5
    });
}
