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
        'Продукты': '#FF0000',
        'Кафе': '#FF0000',
        'Топливо': '#8B00FF',
        'Мойка': '#8B00FF',
        'Тех. обслуживание': '#8B00FF',
        'Товары': '#00BFFF',
        'Дети': '#00BFFF',
        'Одежда': '#00BFFF',
        'Спорт': '#00FF00',
        'Культура': '#00FF00',
        'События': '#00FF00',
        'Интернет': '#FF8C00',
        'Штрафы': '#FF8C00',
        'ЖКХ': '#FF8C00',
        'Общественный транспорт': '#FF8C00',
        'Прочее': '#FF8C00',
        'Доход': '#FFD700'
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
        'Еда': '#FF0000',
        'Авто': '#8B00FF',
        'Товары': '#00BFFF',
        'Мероприятия': '#00FF00',
        'Платежи': '#FF8C00',
        'Доход': '#FFD700'
    };
    return colors[groupName] || '#999999';
}
function showError(message) {
    alert('❌ Ошибка: ' + message);
}
function showSuccess(message) {
    alert('✅ ' + message);
}
