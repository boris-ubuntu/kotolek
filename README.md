# 🐱 Котолёк — Семейный бюджет

Веб-приложение для управления семейным бюджетом и контроля расходов.

**Версия:** 2.0.0  
**Статус:** ✅ Активно поддерживается

## 📱 Особенности

- 💰 **Семейный счёт** — баланс с 1-го числа текущего месяца
- 📊 **Круговая диаграмма** — группировка расходов по категориям с цветовой индикацией
- 📈 **График баланса** — ежедневное изменение баланса за месяц
- 📋 **Последние операции** — быстрый доступ к последним операциям
- ➕ **Добавление операций** — расходы и доходы с выбором категории
- 🗑️ **Удаление операций** — по клику с подтверждением
- 📥 **Импорт/экспорт CSV** — резервное копирование и перенос данных
- 📱 **Адаптивный дизайн** — отлично работает на всех устройствах

## 🏷️ Категории

| Группа | Категории | Цвет |
|--------|-----------|------|
| Еда | Продукты, Кафе | 🔴 Красный |
| Авто | Топливо, Мойка, Тех. обслуживание | 🟣 Фиолетовый |
| Товары | Товары, Дети, Одежда | 🔵 Синий |
| Мероприятия | Спорт, Культура, События | 🟢 Зелёный |
| Платежи | Интернет, Штрафы, ЖКХ, Общественный транспорт, Прочее | 🟠 Оранжевый |
| Доход | Доход | 🟡 Жёлтый |

## 🛠️ Технологии

### Backend
| Технология | Назначение |
|------------|------------|
| **Python 3.14+** | Язык программирования |
| **FastAPI** | Веб-фреймворк |
| **PostgreSQL 18** | База данных |
| **SQLAlchemy 2.x** | ORM |
| **Pydantic v2** | Валидация данных |
| **Uvicorn** | ASGI-сервер |

### Frontend
| Технология | Назначение |
|------------|------------|
| **HTML5 + CSS3** | Разметка и стили |
| **JavaScript (ES6+)** | Логика клиента |
| **Chart.js** | Визуализация данных |
| **LocalStorage** | Локальное кэширование |

## 🚀 Установка и запуск

### Требования
- Python 3.14+
- PostgreSQL 18+
- Git

### 1. Клонирование репозитория
```bash
git clone https://github.com/boris-ubuntu/kotolek.git
cd kotolek
```

### 2. Настройка базы данных PostgreSQL
```bash
sudo -u postgres psql
CREATE DATABASE kotolek;
CREATE USER kotolek_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE kotolek TO kotolek_user;
GRANT ALL ON SCHEMA public TO kotolek_user;
ALTER SCHEMA public OWNER TO kotolek_user;
\q
```

### 3. Настройка бэкенда
```bash
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
```

### 4. Запуск приложения
```bash
# Через uvicorn (рекомендуется)
./venv/bin/uvicorn app.main:app --reload

# Или через встроенный сервер
python3 static_server.py
```

Откройте в браузере: [http://localhost:8080](http://localhost:8080)  
Swagger-документация: [http://localhost:8080/docs](http://localhost:8080/docs)

### 5. Запуск в фоне
```bash
nohup python3 static_server.py > server.log 2>&1 &
```

## 📁 Структура проекта

```
kotolek/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── config.py          # Конфигурация (env)
│   │   ├── crud.py            # Бизнес-логика и работа с БД
│   │   ├── database.py        # Подключение к БД
│   │   ├── main.py            # Точка входа FastAPI
│   │   ├── models.py          # SQLAlchemy модели
│   │   ├── routers/
│   │   │   ├── __init__.py
│   │   │   ├── categories.py  # Эндпоинты категорий
│   │   │   └── transactions.py # Эндпоинты транзакций
│   │   └── schemas.py         # Pydantic схемы
│   ├── .env
│   ├── init_db.py
│   ├── insert_test_data.py    # Тестовые данные
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
│   │       ├── histogram.js
│   │       ├── modal.js
│   │       └── recent.js
│   ├── favicon.svg
│   ├── index.html
│   └── month-detail.html
├── .gitignore
├── README.md
└── LICENSE
```

## 📝 API Эндпоинты

| Метод | Эндпоинт | Описание |
|-------|----------|----------|
| **Категории** | | |
| `GET` | `/api/categories/` | Получить все категории |
| `GET` | `/api/categories/{id}` | Получить категорию по ID |
| **Транзакции** | | |
| `GET` | `/api/transactions/recent` | Последние операции (по умолчанию 5) |
| `GET` | `/api/transactions/by-month` | Операции за месяц (`?year=&month=`) |
| `GET` | `/api/transactions/balance` | Баланс за текущий месяц |
| `GET` | `/api/transactions/expenses-by-category` | Расходы по категориям (текущий месяц) |
| `GET` | `/api/transactions/daily-balance` | Ежедневный баланс за месяц |
| `GET` | `/api/transactions/monthly-expenses` | Расходы за последние 6 месяцев |
| `POST` | `/api/transactions/` | Создать операцию |
| `DELETE` | `/api/transactions/{id}` | Удалить операцию |
| `GET` | `/api/transactions/export` | Экспорт всех операций в CSV |
| `POST` | `/api/transactions/import` | Импорт операций из CSV |
| **Системные** | | |
| `GET` | `/` | Информация об API |
| `GET` | `/health` | Проверка работоспособности |

## 🔄 История изменений

### v2.0.0 (текущая)
- ✅ Исправлен баг: `crud.models.Category` → `models.Category` в categories.py
- ✅ Исправлен баг: дрейф месяцев в `get_monthly_expenses` (timedelta → calendar)
- ✅ Добавлена валидация существования категории при создании транзакции
- ✅ Оптимизация: устранено троекратное дублирование кода запросов
- ✅ Оптимизация: `get_balance` — 3 запроса объединены в 1
- ✅ Добавлена пагинация в `get_all_transactions` (skip/limit)
- ✅ Импорт/экспорт CSV с кодировкой UTF-8 BOM

### v1.0.0
- 🎉 Первый релиз: базовый функционал учёта расходов

## 📄 Лицензия

MIT License — см. файл [LICENSE](LICENSE)

## 👨‍💻 Автор

**Boris** ([@boris-ubuntu](https://github.com/boris-ubuntu))

## 🤝 Вклад в проект

Предложения и пул-реквесты приветствуются!  
По вопросам и багам — открывайте [Issue](https://github.com/boris-ubuntu/kotolek/issues).

---

⭐ Если проект полезен, поставьте звезду на GitHub!
