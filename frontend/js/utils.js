function formatDate(dateStr) {
    const date = new Date(dateStr);
    return date.toLocaleDateString('ru-RU', { day: '2-digit', month: '2-digit', year: 'numeric' });
}
function formatTime(dateStr) {
    const date = new Date(dateStr);
    return date.toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' });
}
function formatDateTime(dateStr) {
    return formatDate(dateStr) + ' ' + formatTime(dateStr);
}
function formatCurrency(amount) {
    return new Intl.NumberFormat('ru-RU', {
        style: 'currency',
        currency: 'RUB',
        minimumFractionDigits: 0,
        maximumFractionDigits: 2
    }).format(amount);
}
function getCurrentDate() {
    const now = new Date();
    return now.toLocaleDateString('ru-RU', {
        day: '2-digit',
        month: 'long',
        year: 'numeric'
    });
}
function getToday() {
    const now = new Date();
    return now.toISOString().split('T')[0];
}
function isIncome(categoryName) {
    return categoryName === 'Доход';
}
function getCategoryColor(categoryName) {
    const colors = {
        'Продукты': '#5390d9',
        'Кафе': '#5390d9',
        'Топливо': '#56cfe1',
        'Мойка': '#56cfe1',
        'Тех. обслуживание': '#56cfe1',
        'Товары': '#5e60ce',
        'Дети': '#5e60ce',
        'Одежда': '#5e60ce',
        'Спорт': '#6930c3',
        'Культура': '#6930c3',
        'События': '#6930c3',
        'Интернет': '#2acbcb',
        'Штрафы': '#2acbcb',
        'ЖКХ': '#2acbcb',
        'Общественный транспорт': '#2acbcb',
        'Прочее': '#2acbcb',
        'Доход': '#4ea8de'
    };
    return colors[categoryName] || '#999999';
}
function getCategoryGroup(categoryName) {
    const groups = {
        'Продукты': 'Еда',
        'Кафе': 'Еда',
        'Топливо': 'Авто',
        'Мойка': 'Авто',
        'Тех. обслуживание': 'Авто',
        'Товары': 'Товары',
        'Дети': 'Товары',
        'Одежда': 'Товары',
        'Спорт': 'Мероприятия',
        'Культура': 'Мероприятия',
        'События': 'Мероприятия',
        'Интернет': 'Платежи',
        'Штрафы': 'Платежи',
        'ЖКХ': 'Платежи',
        'Общественный транспорт': 'Платежи',
        'Прочее': 'Платежи',
        'Доход': 'Доход'
    };
    return groups[categoryName] || categoryName;
}
function getCategoryColorByGroup(groupName) {
    const colors = {
        'Еда': '#5390d9',
        'Авто': '#56cfe1',
        'Товары': '#5e60ce',
        'Мероприятия': '#6930c3',
        'Платежи': '#2acbcb',
        'Доход': '#4ea8de'
    };
    return colors[groupName] || '#999999';
}
function showError(message) {
    alert('❌ Ошибка: ' + message);
}
function showSuccess(message) {
    alert('✅ ' + message);
}
