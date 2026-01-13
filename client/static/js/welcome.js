document.addEventListener('DOMContentLoaded', () => {

    const btnContinue = document.getElementById('btn-continue');
    const btnInfo = document.getElementById('btn-info');

    if (btnInfo) {
        btnInfo.addEventListener('click', (e) => {
            e.preventDefault();
            // Redirect to legal info
            window.location.href = '/legal-info';
        });
    }
});
