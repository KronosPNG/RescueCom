document.addEventListener('DOMContentLoaded', () => {
    renderJsonDetails();
});

function renderJsonDetails() {
    document.querySelectorAll('[data-json]').forEach(el => {
        try {
            if (el.dataset.rendered) return;

            const rawJson = el.dataset.json;
            if (!rawJson || rawJson === 'None' || rawJson === 'null') return;

            const data = JSON.parse(rawJson);
            if (!data || Object.keys(data).length === 0) return;

            const createList = (obj) => {
                const ul = document.createElement('ul');
                ul.style.marginTop = '5px';
                ul.style.paddingLeft = '20px';
                ul.style.listStyleType = 'none';

                for (const [key, value] of Object.entries(obj)) {
                    const li = document.createElement('li');
                    li.style.marginBottom = '2px';
                    li.innerHTML = `<strong style="color: #6c757d; font-size: 0.85em; text-transform: uppercase;">${key}:</strong> `;

                    if (typeof value === 'object' && value !== null) {
                        li.appendChild(createList(value));
                    } else {
                        li.innerHTML += `<span style="color: #212529;">${value}</span>`;
                    }
                    ul.appendChild(li);
                }
                return ul;
            };

            el.appendChild(createList(data));
            el.dataset.rendered = 'true';

        } catch (e) {
            console.warn('Error parsing JSON details for element:', el, e);
        }
    });
}
