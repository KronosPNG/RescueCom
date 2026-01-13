function jsonToHtml(jsonString) {
    if (!jsonString) return '';
    try {
        const data = JSON.parse(jsonString);
        return objectToList(data);
    } catch (e) {
        return '<p>Dati non disponibili</p>';
    }
}

function objectToList(obj) {
    let html = '<ul>';
    for (const [key, value] of Object.entries(obj)) {
        html += `<li><b>${key}</b>`;
        if (typeof value === 'object' && value !== null && !Array.isArray(value)) {
            html += objectToList(value);
        } else {
            html += `: ${value}`;
        }
        html += '</li>';
    }
    html += '</ul>';
    return html;
}

// Auto-rendering data-json
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('[data-json]').forEach(el => {
        el.innerHTML = jsonToHtml(el.getAttribute('data-json'));
    });
});
