// Module: UI Rendering

export function renderFeed(requests, feedListId, onCardClick) {
    const feedList = document.getElementById(feedListId);
    if (!feedList) return;

    feedList.innerHTML = '';
    requests.forEach(req => {
        const card = document.createElement('details');
        card.className = `request-card priority-${req.priority}`;

        // Prepare Health Badges
        const conditionsHtml = (req.user.conditions && req.user.conditions.length > 0 && req.user.conditions[0] !== 'Nessuna info medica')
            ? req.user.conditions.map(c => `<span class="health-badge warning">${c}</span>`).join(' ')
            : '<span class="health-badge neutral">Nessuna patologia nota</span>';

        // Blood Badge
        const bloodHtml = req.user.blood !== 'N/A'
            ? `<span class="health-badge info">Gr. ${req.user.blood}</span>`
            : '';

        // Safely handle potential undefined location
        const lat = req.location?.lat?.toFixed(5) || 'N/A';
        const lng = req.location?.lng?.toFixed(5) || 'N/A';

        card.innerHTML = `
            <summary>
                <div class="summary-content">
                    <div class="summary-header">
                        <span class="card-id">${req.id}</span>
                        <span class="card-time">${req.time}</span>
                    </div>
                    <div class="card-title">${req.type}</div>
                    <div class="card-preview">${req.desc}</div>
                </div>
                <i class="bi bi-caret-down-fill" style="margin-left: 10px; color: #94a3b8;"></i>
            </summary>
            
            <div class="card-details">
                <div class="info-group">
                    <div class="info-label">Dati Paziente</div>
                    <div class="info-value">
                        <strong>${req.user.name}</strong> • ${req.user.age} anni ${bloodHtml}
                    </div>
                    <div style="margin-top: 8px;">${conditionsHtml}</div>
                </div>

                <div class="info-group">
                    <div class="info-label">Luogo & Descrizione</div>
                    <div class="info-value">${req.desc}</div>
                    <div class="info-value" style="margin-top: 4px; font-size: 0.85rem; color: #64748b;">
                        <i class="bi bi-geo-alt-fill"></i> ${req.address} <br>
                        <span style="font-family: monospace; opacity: 0.8;">GPS: ${lat}, ${lng}</span>
                    </div>
                </div>

                <div class="action-bar">
                     <button onclick="window.open('/detail/${req.originalData?.id || req.id.replace('REQ-', '')}', '_self')" 
                        class="btn-sm-primary">
                        <i class="bi bi-file-text"></i> Visualizza Dettagli
                     </button>
                </div>
            </div>
        `;

        if (onCardClick) {
            // Optional: keep click listener on summary if needed, but details handles expansion natively
            // card.querySelector('summary').addEventListener('click', (e) => onCardClick(req));
        }

        feedList.appendChild(card);
    });
}

export function highlightCard(reqId, feedListId) {
    const feedList = document.getElementById(feedListId);
    if (!feedList) return;

    const cards = feedList.querySelectorAll('.request-card');
    cards.forEach(c => {
        if (c.querySelector('.card-id').textContent === reqId) {
            c.style.backgroundColor = 'rgba(255, 255, 255, 0.15)';
            c.scrollIntoView({ behavior: 'smooth', block: 'center' });
        } else {
            c.style.backgroundColor = '';
        }
    });
}

export function updateStats(count) {
    const countEl = document.getElementById('activeRequestsCount');
    if (countEl) countEl.textContent = count;
}

export function renderDetailPanel(req, panelId, onContact, onDispatch) {
    const detailPanel = document.getElementById(panelId);
    if (!detailPanel || !req) return;

    // Conditions is array of strings
    const conditionsHtml = (req.user.conditions && req.user.conditions.length > 0 && req.user.conditions[0] !== 'Nessuna info medica')
        ? req.user.conditions.map(c => `<span class="health-badge" style="background: #ef444422; color: #f87171; padding: 2px 8px; border-radius: 4px; font-size: 0.8rem; border: 1px solid #ef444444;">${c}</span>`).join(' ')
        : '<span style="color: #94a3b8; font-style: italic;">Nessuna patologia nota</span>';

    // Blood type badge
    const bloodHtml = req.user.blood !== 'N/A'
        ? `<span class="blood-badge" style="background: #3b82f622; color: #60a5fa; padding: 2px 8px; border-radius: 4px; font-size: 0.8rem; border: 1px solid #3b82f644; margin-left: 5px;">${req.user.blood}</span>`
        : '<span style="color: #94a3b8;">N/A</span>';

    const photoHtml = req.photo
        ? `<div class="info-group">
             <div class="info-label">Foto Inviata</div>
             <img src="${req.photo}" style="width: 100%; border-radius: 8px; margin-top: 5px; border: 1px solid #334155; max-height: 200px; object-fit: cover;">
           </div>`
        : '';

    const addressHtml = (req.address && req.address !== 'Indirizzo non disponibile')
        ? `<div class="info-group">
            <div class="info-label">Indirizzo Rilevato</div>
            <div class="info-value"><i class="bi bi-geo-alt"></i> ${req.address}</div>
           </div>`
        : '';

    detailPanel.innerHTML = `
        <div class="detail-header">
            <div class="detail-title">${req.type}</div>
            <div class="detail-subtitle">${req.id} • ${req.time}</div>
        </div>

        <div class="info-group">
            <div class="info-label">Stato Emergenza</div>
            <div class="info-value">
                <span style="color: var(--accent-${req.priority === 'high' ? 'red' : req.priority === 'medium' ? 'orange' : 'green'}, ${req.priority === 'high' ? '#ef4444' : req.priority === 'medium' ? '#f97316' : '#22c55e'})">
                    ${req.priority.toUpperCase()} PRIORITY
                </span>
            </div>
        </div>

        <div class="info-group">
            <div class="info-label">Descrizione Luogo</div>
            <div class="info-value" style="font-size: 0.95rem; line-height: 1.5;">${req.desc}</div>
        </div>

        ${addressHtml}

        <div class="info-group">
            <div class="info-label">Dati Paziente</div>
            <div class="info-value"><strong>Nome:</strong> ${req.user.name}</div>
            <div class="info-value"><strong>Età:</strong> ${req.user.age}</div>
            <div class="info-value"><strong>Gruppo Sanguigno:</strong> ${bloodHtml}</div>
        </div>

         <div class="info-group">
            <div class="info-label">Condizioni Mediche Note</div>
            <div class="info-value">${conditionsHtml}</div>
        </div>

        <div class="info-group">
            <div class="info-label">Coordinate GPS</div>
            <div class="info-value">Lat: ${req.location.lat.toFixed(6)}<br>Lng: ${req.location.lng.toFixed(6)}</div>
        </div>

        ${photoHtml}

        <div class="action-bar">
            <button id="btnContact" class="btn btn-secondary">Contatta</button>
            <button class="btn btn-secondary" onclick="window.open('/detail/${req.id}', '_blank')">Vedi Dettagli Completi</button>
        </div>
        
        <div style="margin-top: 10px;">
             <button id="btnDispatch" class="btn btn-primary" style="width: 100%">Invia Soccorsi</button>
        </div>
    `;

    // Attach Event Listeners
    const btnContact = document.getElementById('btnContact');
    if (btnContact && onContact) {
        btnContact.addEventListener('click', () => onContact(req));
    }

    const btnDispatch = document.getElementById('btnDispatch');
    if (btnDispatch && onDispatch) {
        btnDispatch.addEventListener('click', () => onDispatch(req));
    }
}
