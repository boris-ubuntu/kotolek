# 🐱 Котолёк - Семейный бюджет

Веб-приложение для управления семейным бюджетом и контроля расходов.

## 📱 Особенности

- 💰 **Семейный счёт** - баланс с 1-го числа текущего месяца
- 📊 **Круговая диаграмма** - группировка расходов по категориям с цветовой индикацией
- 📈 **График баланса** - ежедневное изменение баланса за месяц
- 📋 **Последние операции** - быстрый доступ к 5 последним операциям
- ➕ **Добавление операций** - расходы и доходы с выбором категории
- 🗑️ **Удаление операций** - по клику с подтверждением
- 📱 **Адаптивный дизайн** - отлично работает на всех устройствах

## 🏷️ Категории

| Группа | Категории | Цвет |
|--------|-----------|------|
| Еда | Продукты, Кафе | 🔴 Красный |
| Авто | Топливо, Мойка, Тех. обслуживание | 🟣 Фиолетовый |
| Товары | Товары, Дети, Одежда | 🔵 Синий |
| Мероприятия | Спорт, Культура, События | 🟢 Зеленый |
| Платежи | Интернет, Штрафы, ЖКХ, Общественный транспорт, Прочее | 🟠 Оранжевый |
| Доход | Доход | 🟡 Желтый |

## 🛠️ Технологии

### Backend
- **Python 3.14+**
- **FastAPI** - веб-фреймворк
- **PostgreSQL 18** - база данных
- **SQLAlchemy** - ORM
- **Pydantic** - валидация данных

### Frontend
- **HTML5 + CSS3**
- **JavaScript (ES6+)**
- **Chart.js** - визуализация данных
- **LocalStorage** - локальное кэширование

## 🚀 Установка и запуск

### Требования
- Python 3.14+
- PostgreSQL 18+
- Git

### 1. Клонирование репозитория
```bash
git clone https://github.com/boris-ubuntu/kotolek.git
cd kotolek

2. Настройка базы данных PostgreSQL
bash

sudo -u postgres psql
CREATE DATABASE kotolek;
CREATE USER kotolek_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE kotolek TO kotolek_user;
GRANT ALL ON SCHEMA public TO kotolek_user;
ALTER SCHEMA public OWNER TO kotolek_user;
\q

3. Настройка бэкенда
bash

cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Создайте файл .env
echo "DATABASE_URL=postgresql://kotolek_user:your_password@localhost:5432/kotolek" > .env
echo "SECRET_KEY=your-secret-key" >> .env
echo "DEBUG=True" >> .env

# Инициализация базы данных
python init_db.py

4. Запуск приложения
bash

# Запуск сервера
python3 static_server.py

# Откройте в браузере:
# http://localhost:8080
# Или с телефона: http://ваш-ip:8080

5. Запуск в фоне
bash

nohup python3 static_server.py > server.log 2>&1 &

📁 Структура проекта
text

kotolek/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── crud.py
│   │   ├── database.py
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── routers/
│   │   │   ├── __init__.py
│   │   │   ├── categories.py
│   │   │   └── transactions.py
│   │   └── schemas.py
│   ├── .env
│   ├── init_db.py
│   ├── requirements.txt
│   └── static_server.py
├── frontend/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   ├── app.js
│   │   ├── api.js
│   │   ├── utils.js
│   │   └── components/
│   │       ├── balance.js
│   │       ├── chart.js
│   │       ├── delete-modal.js
│   │       ├── graph.js
│   │       ├── modal.js
│   │       └── recent.js
│   └── index.html
├── .gitignore
├── README.md
└── LICENSE

📝 API Эндпоинты
Метод	Эндпоинт	Описание
GET	/api/categories/	Получить все категории
POST	/api/transactions/	Создать операцию
GET	/api/transactions/recent	Получить последние операции
GET	/api/transactions/balance	Получить баланс за месяц
GET	/api/transactions/expenses-by-category	Расходы по категориям
GET	/api/transactions/daily-balance	Ежедневный баланс за месяц
DELETE	/api/transactions/{id}	Удалить операцию
📄 Лицензия

MIT License - см. файл LICENSE
👨‍💻 Автор

Boris (@boris-ubuntu)
⭐ Поддержка

Если вам понравился проект, поставьте ⭐ на GitHub!
