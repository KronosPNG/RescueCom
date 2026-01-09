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
    // 1. Parse Position (emposition: "lat,lng" OR position)
    let lat = 0, lng = 0;
    const posString = emergency.emposition || emergency.position || '0,0';
    if (typeof posString === 'string') {
        [lat, lng] = posString.split(',').map(n => parseFloat(n.trim()) || 0);
    }

    // 2. Parse Priority from emscore OR severity
    let priority = 'medium';
    // Handle both emscore (0-100) and severity (usually 1-3 or similar, assuming 1=Low, 3=High if int, or reusing 0-100 scale)
    // If severity is small int (1-5), map manually. If 0-100, treat as score.
    const rawScore = (emergency.emscore !== undefined) ? parseInt(emergency.emscore) : (emergency.severity !== undefined ? parseInt(emergency.severity) : 0);

    // Heuristic: if severity is small (<10), assume 1=Low, 2=Med, 3=High
    if (rawScore <= 5 && rawScore > 0) {
        if (rawScore >= 3) priority = 'high';
        else if (rawScore === 2) priority = 'medium';
        else priority = 'low';
    } else {
        // Standard 0-100 score
        if (rawScore >= 80) priority = 'high';
        else if (rawScore >= 40) priority = 'medium';
        else priority = 'low';
    }

    // 3. Photo (empicture OR photo_b64)
    const rawPhoto = emergency.empicture || emergency.photo_b64;
    const photoUrl = rawPhoto
        ? (rawPhoto.startsWith('http') ? rawPhoto : `data:image/png;base64,${rawPhoto}`)
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
    // Mappings: emtype -> emergency_type, emdescription -> description, bloodtype -> blood_type
    const type = emergency.emtype || emergency.emergency_type || 'Emergenza';
    const desc = emergency.emdescription || emergency.description || 'Nessuna descrizione';
    const blood = emergency.bloodtype || emergency.blood_type || 'N/A';
    const health = emergency.healthinfo || emergency.health_info_json || 'Nessuna info medica';

    return {
        id: `REQ-${emergency.id || emergency.emergency_id || Math.floor(Math.random() * 1000)}`,
        time: emergency.created_at ? new Date(emergency.created_at).toLocaleTimeString('it-IT', { hour: '2-digit', minute: '2-digit' }) : new Date().toLocaleTimeString('it-IT', { hour: '2-digit', minute: '2-digit' }),
        type: type,
        desc: desc,
        priority: priority,
        location: { lat: lat, lng: lng },
        address: emergency.address || 'Indirizzo non disponibile',
        photo: photoUrl,
        user: {
            name: `${emergency.name || ''} ${emergency.surname || ''}`.trim() || 'Utente Sconosciuto',
            age: age,
            blood: blood,
            conditions: health ? [health] : ['Nessuna info medica']
        },
        originalData: emergency
    };
}
