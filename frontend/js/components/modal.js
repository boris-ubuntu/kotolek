class ModalComponent {
    constructor() {
        this.overlay = document.getElementById('modal-overlay');
        this.form = document.getElementById('transaction-form');
        this.categorySelect = document.getElementById('category');
        this.typeSelect = document.getElementById('transaction-type');
        this.amountInput = document.getElementById('amount');
        this.descriptionInput = document.getElementById('description');
        this.closeBtn = document.getElementById('close-modal');
        this.addBtn = document.getElementById('add-btn');
        this.categories = [];
        this.onSuccess = null;
        this.init();
    }
    async init() {
        try {
            this.categories = await API.getCategories();
            console.log('✅ Категории загружены:', this.categories);
        } catch (error) {
            console.error('❌ Ошибка загрузки категорий:', error);
            this.categories = [
                {id: 1, name: 'Продукты', color: '#FF0000', is_income: false},
                {id: 2, name: 'Кафе', color: '#FF0000', is_income: false},
                {id: 3, name: 'Топливо', color: '#8B00FF', is_income: false},
                {id: 4, name: 'Мойка', color: '#8B00FF', is_income: false},
                {id: 5, name: 'Тех. обслуживание', color: '#8B00FF', is_income: false},
                {id: 6, name: 'Товары', color: '#00BFFF', is_income: false},
                {id: 7, name: 'Дети', color: '#00BFFF', is_income: false},
                {id: 8, name: 'Одежда', color: '#00BFFF', is_income: false},
                {id: 9, name: 'Спорт', color: '#00FF00', is_income: false},
                {id: 10, name: 'Культура', color: '#00FF00', is_income: false},
                {id: 11, name: 'События', color: '#00FF00', is_income: false},
                {id: 12, name: 'Интернет', color: '#FF8C00', is_income: false},
                {id: 13, name: 'Штрафы', color: '#FF8C00', is_income: false},
                {id: 14, name: 'ЖКХ', color: '#FF8C00', is_income: false},
                {id: 15, name: 'Общественный транспорт', color: '#FF8C00', is_income: false},
                {id: 16, name: 'Прочее', color: '#FF8C00', is_income: false},
                {id: 17, name: 'Доход', color: '#FFD700', is_income: true},
            ];
        }
        this.populateCategories();
        this.typeSelect.addEventListener('change', () => this.populateCategories());
        this.form.addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleSubmit(e);
        });
        this.closeBtn.addEventListener('click', () => this.close());
        this.addBtn.addEventListener('click', () => this.open());
        this.overlay.addEventListener('click', (e) => {
            if (e.target === this.overlay) {
                this.close();
            }
        });
    }
    populateCategories() {
        const type = this.typeSelect.value;
        const filtered = this.categories.filter(cat => {
            if (type === 'income') return cat.is_income === true;
            return cat.is_income === false;
        });
        this.categorySelect.innerHTML = '';
        for (let i = 0; i < filtered.length; i++) {
            const option = document.createElement('option');
            option.value = filtered[i].id;
            option.textContent = filtered[i].name;
            option.style.color = filtered[i].color;
            option.style.fontWeight = 'bold';
            this.categorySelect.appendChild(option);
        }
    }
    open() {
        this.overlay.classList.remove('hidden');
        this.amountInput.focus();
        this.amountInput.value = '';
        this.descriptionInput.value = '';
        this.populateCategories();
    }
    close() {
        this.overlay.classList.add('hidden');
        this.form.reset();
    }
    setOnSuccess(callback) {
        this.onSuccess = callback;
    }
    async handleSubmit(e) {
        e.preventDefault();
        const amount = parseFloat(this.amountInput.value);
        if (isNaN(amount) || amount <= 0) {
            showError('Введите корректную сумму');
            return;
        }
        const categoryId = parseInt(this.categorySelect.value);
        if (!categoryId) {
            showError('Выберите категорию');
            return;
        }
        const isIncome = this.typeSelect.value === 'income';
        const description = this.descriptionInput.value.trim();
        const data = {
            amount: amount,
            category_id: categoryId,
            is_income: isIncome,
            description: description || null,
        };
        const submitBtn = this.form.querySelector('button[type="submit"]');
        submitBtn.disabled = true;
        try {
            const result = await API.createTransaction(data);
            console.log('✅ Сохранено в БД:', result);
            this.close();
            if (this.onSuccess) {
                this.onSuccess();
            }
            window.dispatchEvent(new Event('transaction-added'));
        } catch (error) {
            console.error('❌ Ошибка:', error);
            showError('Ошибка: ' + error.message);
        } finally {
            submitBtn.disabled = false;
        }
    }
}
