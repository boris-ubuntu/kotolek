class BalanceComponent {
    constructor() {
        this.balanceEl = document.getElementById('balance-amount');
        this.incomeEl = document.getElementById('month-income');
        this.topEl = document.getElementById('top-expense-amount');
        this.trendEl = document.getElementById('expense-trend');
        this.topCardEl = document.getElementById('top-expense-card');
        this.topDetail = null;
    }
    async update() {
        try {
            const [balance, summary] = await Promise.all([
                API.getBalance(),
                API.getMonthSummary(),
            ]);
            this.renderBalance(balance);
            this.renderSummary(summary);
        } catch (error) {
            console.error('Failed to load balance:', error);
            if (this.balanceEl) this.balanceEl.textContent = '0 ₽';
            if (this.topEl) this.topEl.textContent = '0 ₽';
        }
    }
    renderBalance(data) {
        const balance = data ? data.balance : 0;
        if (this.balanceEl) {
            this.balanceEl.textContent = formatCurrency(balance);
            this.balanceEl.className = balance >= 0 ? 'positive' : 'negative';
        }
        if (this.incomeEl && data) {
            this.incomeEl.textContent = 'Доход за месяц: ' + formatCurrency(data.month_income);
        }
    }
    renderSummary(data) {
        if (!this.topEl) return;
        const top = data && data.top_expense ? data.top_expense : 0;
        this.topEl.textContent = formatCurrency(top);
        this.topDetail = (data && data.top_expense_detail) ? data.top_expense_detail : null;

        if (!this.trendEl) return;
        const pct = data ? data.change_pct : null;
        if (pct === null || pct === undefined) {
            this.trendEl.textContent = '';
            this.trendEl.className = 'expense-trend';
            return;
        }
        // Расходы ниже предыдущего месяца → зелёный треугольник ВНИЗ
        // Расходы выше → красный треугольник ВВЕРХ.
        // Показываем абсолютное значение разницы (без знака процента).
        const lower = pct < 0;
        const arrow = lower ? '▼' : '▲';
        const absPct = Math.abs(pct);
        this.trendEl.textContent = arrow + ' ' + absPct + '% к пр. месяцу';
        this.trendEl.className = 'expense-trend ' + (lower ? 'trend-down-good' : 'trend-up-bad');
    }
    onTopClick() {
        if (!this.topDetail) return;
        const d = this.topDetail;
        const dateStr = new Date(d.date).toLocaleDateString('ru-RU', { day: '2-digit', month: 'long', year: 'numeric' });
        const html =
            '<div style="display:flex;align-items:center;gap:10px;margin-bottom:14px;">' +
                '<span style="width:14px;height:14px;border-radius:50%;background:' + (d.category_color || '#f27362') + ';display:inline-block;"></span>' +
                '<span style="font-size:16px;font-weight:700;">' + (d.category_name || 'Расход') + '</span>' +
            '</div>' +
            '<div style="font-size:30px;font-weight:700;color:#f27362;margin-bottom:10px;">' + formatCurrency(d.amount) + '</div>' +
            (d.description ? '<div style="color:#cbd5e0;margin-bottom:8px;">' + escapeHtml(d.description) + '</div>' : '') +
            '<div style="color:#a0aec0;font-size:13px;">' + dateStr + '</div>';
        if (window.app && typeof window.app.showInfoModal === 'function') {
            window.app.showInfoModal('Топ расход за месяц', html);
        }
    }
}

function escapeHtml(str) {
    if (!str) return '';
    return String(str)
        .replace(/&/g, '&')
        .replace(/</g, '<')
        .replace(/>/g, '>')
        .replace(/"/g, '"');
}