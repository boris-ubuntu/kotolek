class App {
    constructor() {
        this.balance = new BalanceComponent();
        this.chart = new ChartComponent();
        this.histogram = new HistogramComponent();
        this.graph = new GraphComponent();
        this.recent = new RecentComponent();
        this.modal = new ModalComponent();
        this.deleteModal = new DeleteModal();
        this.modal.setOnSuccess(() => this.refreshAll());
        document.getElementById('current-date').textContent = getCurrentDate();
        this.refreshAll();
        window.addEventListener('transaction-added', () => this.refreshAll());
        setInterval(() => this.refreshAll(), 30000);
        
        this.initExportImport();
        this.initTopExpenseClick();
        this.initInfoModal();
    }

    initTopExpenseClick() {
        const card = document.getElementById('top-expense-card');
        if (card) {
            card.addEventListener('click', () => this.balance.onTopClick());
        }
    }

    initInfoModal() {
        const overlay = document.getElementById('info-modal-overlay');
        const closeBtn = document.getElementById('info-modal-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => overlay.classList.add('hidden'));
        }
        if (overlay) {
            overlay.addEventListener('click', (e) => {
                if (e.target === overlay) overlay.classList.add('hidden');
            });
        }
    }

    showInfoModal(title, bodyHtml) {
        const overlay = document.getElementById('info-modal-overlay');
        const titleEl = document.getElementById('info-modal-title');
        const bodyEl = document.getElementById('info-modal-body');
        if (!overlay) return;
        if (titleEl) titleEl.textContent = title;
        if (bodyEl) bodyEl.innerHTML = bodyHtml;
        overlay.classList.remove('hidden');
    }
    
    initExportImport() {
        // Экспорт
        document.getElementById('export-btn').addEventListener('click', function() {
            window.location.href = '/api/transactions/export';
        });
        
        // Импорт - сразу загружаем файл
        document.getElementById('import-file').addEventListener('change', async function(e) {
            if (e.target.files.length === 0) return;
            
            const file = e.target.files[0];
            const formData = new FormData();
            formData.append('file', file);
            
            const importStatus = document.createElement('div');
            importStatus.style.cssText = 'position:fixed;bottom:100px;left:50%;transform:translateX(-50%);background:#2d3748;color:white;padding:12px 24px;border-radius:12px;z-index:9999;font-weight:600;box-shadow:0 4px 20px rgba(0,0,0,0.3);';
            importStatus.textContent = '⏳ Импорт...';
            document.body.appendChild(importStatus);
            
            try {
                const response = await fetch('/api/transactions/import', {
                    method: 'POST',
                    body: formData
                });
                
                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.detail || 'Ошибка импорта');
                }
                
                const result = await response.json();
                importStatus.textContent = '✅ ' + result.message;
                importStatus.style.background = '#48bb78';
                
                window.app.refreshAll();
                
                setTimeout(() => {
                    importStatus.remove();
                }, 3000);
                
            } catch (error) {
                importStatus.textContent = '❌ Ошибка: ' + error.message;
                importStatus.style.background = '#fc8181';
                
                setTimeout(() => {
                    importStatus.remove();
                }, 3000);
            }
            
            e.target.value = '';
        });
    }
    
    async refreshAll() {
        await Promise.all([
            this.balance.update(),
            this.chart.update(),
            this.histogram.update(),
            this.graph.update(),
            this.recent.update(),
        ]);
    }
}
document.addEventListener('DOMContentLoaded', function() {
    window.app = new App();
});
