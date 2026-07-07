class App {
    constructor() {
        this.balance = new BalanceComponent();
        this.chart = new ChartComponent();
        this.graph = new GraphComponent();
        this.recent = new RecentComponent();
        this.modal = new ModalComponent();
        this.deleteModal = new DeleteModal();
        this.modal.setOnSuccess(() => this.refreshAll());
        document.getElementById('current-date').textContent = getCurrentDate();
        this.refreshAll();
        window.addEventListener('transaction-added', () => this.refreshAll());
        setInterval(() => this.refreshAll(), 30000);
    }
    async refreshAll() {
        await Promise.all([
            this.balance.update(),
            this.chart.update(),
            this.graph.update(),
            this.recent.update(),
        ]);
    }
}
document.addEventListener('DOMContentLoaded', () => {
    window.app = new App();
});
