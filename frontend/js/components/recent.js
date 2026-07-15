class RecentComponent {
    constructor() {
        this.container = document.getElementById('recent-list');
        this.selectedId = null;
    }
    async update() {
        try {
            const transactions = await API.getRecentTransactions(5);
            console.log('Recent transactions:', transactions);
            this.render(transactions);
        } catch (error) {
            console.error('Failed to load recent transactions:', error);
            this.container.innerHTML = '<div class="loading">Ошибка загрузки</div>';
        }
    }
    render(transactions) {
        if (!transactions || transactions.length === 0) {
            this.container.innerHTML = '<div class="loading">Нет операций</div>';
            return;
        }
        var html = '';
        for (var i = 0; i < transactions.length; i++) {
            var txn = transactions[i];
            var isIncomeTxn = txn.is_income;
            var amountClass = isIncomeTxn ? 'income' : 'expense';
            var sign = isIncomeTxn ? '+' : '-';
            var groupName = getCategoryGroup(txn.category_name);
            var groupColor = getCategoryColorByGroup(groupName);
            var description = txn.description || 'Без описания';
            if (description.length > 25) {
                description = description.substring(0, 25) + '...';
            }
            html += '<div class="recent-item" data-id="' + txn.id + '" onclick="window.handleRecentClick(' + txn.id + ')">';
            html += '<div class="info">';
            html += '<span class="tag" style="background: ' + groupColor + '; width:12px; height:12px; border-radius:50%; display:inline-block; flex-shrink:0; min-width:12px; min-height:12px; border:1px solid rgba(0,0,0,0.1);"></span>';
            html += '<div class="details">';
            html += '<div class="category-name">' + groupName + '</div>';
            html += '<div class="description">' + description + '</div>';
            html += '</div>';
            html += '</div>';
            html += '<div class="right">';
            html += '<div class="amount ' + amountClass + '">' + sign + ' ' + formatCurrency(txn.amount) + '</div>';
            html += '<div class="date">' + formatDate(txn.date) + '</div>';
            html += '</div>';
            html += '</div>';
        }
        this.container.innerHTML = html;
    }
}

// Глобальная функция для обработки клика — открываем окно подтверждения удаления
window.handleRecentClick = function(id) {
    console.log('Clicked transaction id:', id);
    if (window.deleteModal) {
        window.deleteModal.open(id);
    } else {
        console.error('Delete modal not initialized');
    }
};
