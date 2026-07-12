class API {
    static async request(endpoint, options = {}) {
        const url = '/api' + endpoint;
        const config = {
            headers: {
                'Content-Type': 'application/json',
            },
            ...options,
        };
        if (options.body) {
            config.body = JSON.stringify(options.body);
        }
        try {
            const response = await fetch(url, config);
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Ошибка сервера');
            }
            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }
    static async getCategories() {
        return this.request('/categories/');
    }
    static async createTransaction(data) {
        return this.request('/transactions/', {
            method: 'POST',
            body: data,
        });
    }
    static async getRecentTransactions(limit = 5) {
        return this.request('/transactions/recent?limit=' + limit);
    }
    static async getBalance() {
        return this.request('/transactions/balance');
    }
    static async getExpensesByCategory() {
        return this.request('/transactions/expenses-by-category');
    }
    static async getDailyBalance() {
        return this.request('/transactions/daily-balance');
    }
    static async getMonthlyExpenses() {
        return this.request('/transactions/monthly-expenses');
    }
    static async getTransactionsByMonth(year, month) {
        return this.request('/transactions/by-month?year=' + year + '&month=' + month);
    }
}
