class BalanceComponent {
    constructor() {
        this.element = document.getElementById('balance-amount');
    }
    async update() {
        try {
            const data = await API.getBalance();
            this.render(data);
        } catch (error) {
            console.error('Failed to load balance:', error);
            this.element.textContent = '0 ₽';
        }
    }
    render(data) {
        const balance = data ? data.balance : 0;
        const formatted = formatCurrency(balance);
        this.element.textContent = formatted;
        this.element.className = balance >= 0 ? 'positive' : 'negative';
    }
}
