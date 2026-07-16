class DeleteModal {
    constructor() {
        this.overlay = document.getElementById('delete-modal-overlay');
        this.transactionId = null;
        this.init();
    }
    init() {
        document.getElementById('delete-confirm').addEventListener('click', () => this.confirm());
        document.getElementById('delete-cancel').addEventListener('click', () => this.close());
        this.overlay.addEventListener('click', (e) => {
            if (e.target === this.overlay) {
                this.close();
            }
        });
        // Сохраняем ссылку на глобальный объект
        window.deleteModal = this;
    }
    open(id) {
        console.log('Delete modal open for id:', id);
        this.transactionId = id;
        this.overlay.classList.remove('hidden');
    }
    close() {
        this.overlay.classList.add('hidden');
        this.transactionId = null;
    }
    async confirm() {
        if (!this.transactionId) {
            console.error('No transaction id');
            return;
        }
        try {
            console.log('Deleting transaction id:', this.transactionId);
            await API.request('/transactions/' + this.transactionId, {
                method: 'DELETE',
            });
            this.close();
            window.dispatchEvent(new Event('transaction-added'));
        } catch (error) {
            console.error('Ошибка удаления:', error);
            showError('Не удалось удалить операцию: ' + error.message);
        }
    }
}
