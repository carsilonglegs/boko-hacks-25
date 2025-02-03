class AppModal {
    constructor() {
        this.modal = document.getElementById('app-modal');
        this.modalTitle = document.getElementById('modal-title');
        this.appContainer = document.getElementById('app-container');
        this.closeBtn = document.querySelector('.close-modal');
        
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        this.closeBtn.addEventListener('click', () => this.closeModal());
        
        window.addEventListener('click', (e) => {
            if (e.target === this.modal) {
                this.closeModal();
            }
        });

        document.querySelectorAll('.app-card').forEach(card => {
            card.addEventListener('click', (e) => {
                e.preventDefault();
                const appTitle = card.querySelector('h3').textContent;
                const appPath = card.getAttribute('data-app');
                this.openApp(appTitle, appPath);
            });
        });
    }

    async openApp(title, appPath) {
        this.modalTitle.textContent = title;
        
        try {
            const response = await fetch(`/apps/${appPath}`);
            const appContent = await response.text();
            this.appContainer.innerHTML = appContent;
            this.modal.style.display = 'block';
            
            if (window.initializeApp) {
                window.initializeApp();
            }
        } catch (error) {
            console.error('Error loading app:', error);
            this.appContainer.innerHTML = '<p>Error loading application</p>';
        }
    }

    closeModal() {
        this.modal.style.display = 'none';
        this.appContainer.innerHTML = '';
    }
}

document.addEventListener('DOMContentLoaded', () => {
    window.appModal = new AppModal();
});