// Module: UI Rendering

export function renderFeed(requests, feedListId, onCardClick) {
    const feedList = document.getElementById(feedListId);
    if (!feedList) return;

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

        if (onCardClick) {
            card.addEventListener('click', () => onCardClick(req));
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

    const conditionsHtml = req.user.conditions.map(c => `<span class="health-badge">${c}</span>`).join('');

    const photoHtml = req.photo
        ? `<div class="info-group">
             <div class="info-label">Foto Inviata</div>
             <img src="${req.photo}" style="width: 100%; border-radius: 8px; margin-top: 5px; border: 1px solid #334155;">
           </div>`
        : '';

    const addressHtml = req.address
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
                <span style="color: var(--accent-${req.priority === 'high' ? 'red' : req.priority === 'medium' ? 'orange' : 'green'})">
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
            <div class="info-value"><strong>Gruppo Sanguigno:</strong> ${req.user.blood}</div>
        </div>

         <div class="info-group">
            <div class="info-label">Condizioni Mediche Note</div>
            <div class="info-value">${conditionsHtml}</div>
        </div>

        <div class="info-group">
            <div class="info-label">Coordinate GPS</div>
            <div class="info-value">Lat: ${req.location.lat}<br>Lng: ${req.location.lng}</div>
        </div>

        ${photoHtml}

        <div class="action-bar">
            <button id="btnContact" class="btn btn-secondary">Contatta</button>
            <button class="btn btn-secondary" onclick="window.open('/detail/${req.id}', '_blank')">Vedi Dettagli Completi</button>
        </div>
        
        <div style="margin-top: 10px;">
             <!-- Added primary action separately for spacing -->
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
