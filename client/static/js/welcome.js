document.addEventListener('DOMContentLoaded', () => {

    const btnContinue = document.getElementById('btn-continue');
    const btnInfo = document.getElementById('btn-info');

    if (btnContinue) {
        btnContinue.addEventListener('click', (e) => {
            e.preventDefault();
            // Logic to mark onboarding as done could go here (e.g., localStorage)
            // localStorage.setItem('onboarding_complete', 'true');

            // Redirect to home/dashboard
            window.location.href = '/';
        });
    }

    if (btnInfo) {
        btnInfo.addEventListener('click', (e) => {
            e.preventDefault();
            // Redirect to legal info
            window.location.href = '/legal-info';
        });
    }
});
