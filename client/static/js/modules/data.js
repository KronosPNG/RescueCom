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
    // 1. Parse Position (emposition: "lat,lng")
    let lat = 0, lng = 0;
    const posString = emergency.emposition || emergency.position || '0,0';
    if (typeof posString === 'string') {
        [lat, lng] = posString.split(',').map(n => parseFloat(n.trim()) || 0);
    }

    // 2. Parse Priority from emscore
    // Assuming emscore is a number 0-100 or similar. Adjust logic as needed.
    // Defaulting to medium if undefined.
    let priority = 'medium';
    const score = parseInt(emergency.emscore) || 0;
    if (score >= 80) priority = 'high';
    else if (score >= 40) priority = 'medium';
    else priority = 'low';

    // 3. Photo
    const photoUrl = emergency.empicture
        ? (emergency.empicture.startsWith('http') ? emergency.empicture : `data:image/png;base64,${emergency.empicture}`)
        : null;

    // 4. Calculate Age
    let age = 'N/A';
    if (emergency.birthday) {
        const birthDate = new Date(emergency.birthday);
        if (!isNaN(birthDate.getTime())) {
            const today = new Date();
            let calculatedAge = today.getFullYear() - birthDate.getFullYear();
            const m = today.getMonth() - birthDate.getMonth();
            if (m < 0 || (m === 0 && today.getDate() < birthDate.getDate())) {
                calculatedAge--;
            }
            age = calculatedAge.toString();
        }
    }

    // 5. Construct Object
    return {
        id: `REQ-${emergency.id || Math.floor(Math.random() * 1000)}`,
        time: new Date().toLocaleTimeString('it-IT', { hour: '2-digit', minute: '2-digit' }),
        type: emergency.emtype || 'Emergenza',
        desc: emergency.emdescription || 'Nessuna descrizione',
        priority: priority,
        location: { lat: lat, lng: lng },
        address: emergency.address || 'Indirizzo non disponibile', // Keep fallback if address isn't in new fields
        photo: photoUrl,
        user: {
            name: `${emergency.name || ''} ${emergency.surname || ''}`.trim() || 'Utente Sconosciuto',
            age: age,
            blood: emergency.bloodtype || 'N/A',
            conditions: emergency.healthinfo ? [emergency.healthinfo] : ['Nessuna info medica']
        },
        originalData: emergency
    };
}
