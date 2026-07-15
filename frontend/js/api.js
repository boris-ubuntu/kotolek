class API {
    static TOKEN_KEY = 'kotolek_token';
    static onUnauthorized = null;

    static getToken() {
        return localStorage.getItem(API.TOKEN_KEY) || '';
    }

    static setToken(token) {
        if (token) {
            localStorage.setItem(API.TOKEN_KEY, token);
        } else {
            localStorage.removeItem(API.TOKEN_KEY);
        }
    }

    static async request(endpoint, options = {}) {
        const url = '/api' + endpoint;
        const headers = {
            'Content-Type': 'application/json',
            ...(options.headers || {}),
        };
        const token = API.getToken();
        if (token) {
            headers['Authorization'] = 'Bearer ' + token;
        }
        const config = {
            headers,
            ...options,
        };
        if (options.body) {
            config.body = JSON.stringify(options.body);
        }
        try {
            const response = await fetch(url, config);
            if (response.status === 401) {
                API.setToken('');
                if (typeof API.onUnauthorized === 'function') {
                    API.onUnauthorized();
                }
                throw new Error('Требуется авторизация');
            }
            if (!response.ok) {
                let detail = 'Ошибка сервера';
                try {
                    const data = await response.json();
                    detail = data.detail || JSON.stringify(data);
                } catch (e) {
                    // Тело ответа не JSON (например, HTML-страница ошибки) — берём текст
                    const text = await response.text();
                    detail = text ? text.slice(0, 200) : `HTTP ${response.status}`;
                }
                throw new Error(detail);
            }
            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    static async login(username, password) {
        const res = await fetch('/api/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password }),
        });
        if (!res.ok) {
            let detail = 'Неверный логин или пароль';
            try {
                const data = await res.json();
                detail = data.detail || detail;
            } catch (e) {}
            throw new Error(detail);
        }
        const data = await res.json();
        API.setToken(data.access_token);
        return data;
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
    static async getMonthSummary() {
        return this.request('/transactions/month-summary');
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
    static async deleteTransaction(id) {
        return this.request('/transactions/' + id, {
            method: 'DELETE',
        });
    }
}
