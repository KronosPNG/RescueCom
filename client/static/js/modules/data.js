// Module: Data & State Management

const requests = [];

export function getRequests() {
    return requests;
}

export function addRequest(req) {
    requests.unshift(req);
    localStorage.setItem('rescuecom_requests', JSON.stringify(requests));
    return requests;
}

export function setRequests(newRequests) {
    requests.length = 0;
    requests.push(...newRequests);
    localStorage.setItem('rescuecom_requests', JSON.stringify(requests));
}

/**
 * Parses raw Emergency JSON (Python class structure) into Dashboard Request format
 */
export function parseEmergencyData(emergency) {
    // 1. Parse Position
    let lat = 0, lng = 0;
    if (emergency.position && typeof emergency.position === 'string') {
        [lat, lng] = emergency.position.split(',').map(Number);
    }

    // 2. Parse Details
    let details = {};
    try {
        details = JSON.parse(emergency.details_json || '{}');
    } catch (e) {
        console.error("Error parsing details_json", e);
        details = { gravity: 'medium', type: 'Segnalazione Generica' };
    }

    // 3. Photo
    const photoUrl = emergency.photo_b64
        ? `data:image/png;base64,${emergency.photo_b64}`
        : null;

    // 4. Construct Object
    return {
        id: `REQ-${emergency.id}`,
        time: new Date().toLocaleTimeString('it-IT', { hour: '2-digit', minute: '2-digit' }),
        type: details.type || 'Emergenza',
        desc: emergency.place_description || 'Nessuna descrizione luogo',
        priority: details.gravity || 'medium',
        location: { lat: lat, lng: lng },
        address: `${emergency.address}, ${emergency.street_number}, ${emergency.city}`,
        photo: photoUrl,
        user: {
            name: emergency.user_uuid ? `Utente ${emergency.user_uuid.substring(0, 8)}...` : 'Utente App',
            age: 'N/A',
            blood: 'N/A',
            conditions: ['Dati non disponibili']
        },
        originalData: emergency
    };
}
