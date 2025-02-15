class AppModal {
    constructor() {
        this.modal = document.getElementById('app-modal');
        this.modalTitle = document.getElementById('modal-title');
        this.appContainer = document.getElementById('app-container');
        this.closeBtn = document.querySelector('.close-modal');
        this.currentApp = null;
        
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

    async loadAppScript(appName) {
        return new Promise((resolve, reject) => {
            const script = document.createElement('script');
            script.src = `/static/js/${appName}.js`;
            script.onload = () => resolve();
            script.onerror = () => reject();
            document.head.appendChild(script);
        });
    }

    async openApp(title, appPath) {
        this.modalTitle.textContent = title;
        this.currentApp = appPath;
        
        try {
            // Load the app content
            const response = await fetch(`/apps/${appPath}`);
            const appContent = await response.text();
            this.appContainer.innerHTML = appContent;
            
            // Load app-specific JavaScript if it exists
            try {
                await this.loadAppScript(appPath);
                console.log(`Loaded ${appPath}.js successfully`);
            } catch (error) {
                console.log(`No specific JS file found for ${appPath}, continuing...`);
            }

            this.modal.style.display = 'block';
            
            // Initialize app if function exists
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
        this.currentApp = null;
        
        // Clean up any app-specific scripts
        const appScripts = document.querySelectorAll('script[src^="/static/js/"]');
        appScripts.forEach(script => {
            if (script.src.includes(this.currentApp)) {
                script.remove();
            }
        });
    }
}

document.addEventListener('DOMContentLoaded', () => {
    window.appModal = new AppModal();
});