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
            script.dataset.appName = appName; //Tags script for removal
            document.head.appendChild(script);
        });
    }

    async openApp(title, appPath) {
        this.modalTitle.textContent = title;
        this.currentApp = appPath;
        
        try {
            // Load the app content
            const response = await fetch(`/apps/${appPath}`);
            if(!response.ok) throw new Error('Failed to load ${appPath}');
            const appContent = await response.text();
            this.appContainer.innerHTML = appContent;
            
            console.log('Opening app: ${appPAth}');
            this.logCurrentScripts("Before script cleanup");

            this.cleanupPreviousApp();

            // Load app-specific JavaScript if it exists
            try {
                await this.loadAppScript(appPath);
                console.log(`Loaded ${appPath}.js successfully`);
            } catch (error) {
                console.log(`No specific JS file found for ${appPath}, continuing...`);
            }

            this.modal.style.display = 'block';

            this.logCurrentScripts("After script load");
            
            // Initialize app if function exists
            if (typeof window.initializeApp === "function") {
                try {
                    window.initializeApp();
                } catch (error) {
                    console.error('Error in initializeApp:', error);
                }
            }
        } catch (error) {
            console.error('Error loading app:', error);
            this.appContainer.innerHTML = '<p>Error loading application</p>';
        }
    }

    closeModal() {
        console.log('Closing modal for app: ${this.currentApp}');


        this.modal.style.display = 'none';
        this.appContainer.innerHTML = '';
        
        this.cleanupPreviousApp();

        this.logCurrentScripts("After modal Close");
    }
    cleanupPreviousApp() {
        console.log("Cleaning up previous app...");

        // Call app-specific cleanup function if available
        if (typeof window.cleanupApp === "function") {
            try {
                console.log("Executing cleanupApp...");
                window.cleanupApp();
            } catch (error) {
                console.error('Error in cleanupApp:', error);
            }
        }
        console.log("Removing dynamically added scripts...");
        document.querySelectorAll('script[data-app-name]').forEach(script => {
            console.log(`Removing script: ${script.src}`);
            script.remove();
        });

        // Remove lingering global variables & force garbage collection
        console.log("Removing global references: initializeApp and cleanupApp");
        window.initializeApp = undefined ;
        window.cleanupApp = undefined ;

    
    }
    logCurrentScripts(context) {
        console.log(`=== ${context} ===`);
        const scripts = document.querySelectorAll('script[data-app-name]');
        if (scripts.length === 0) {
            console.log("No dynamically loaded scripts found.");
        } else {
            scripts.forEach(script => console.log(`Loaded script: ${script.src}`));
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    window.appModal = new AppModal();
});