#!/bin/sh

# Используем готовый DATABASE_URL, если он задан (Render),
# иначе собираем из компонентов (локальный docker-compose)
if [ -z "${DATABASE_URL}" ]; then
    export DATABASE_URL="postgresql://${POSTGRES_USER:-kotolek}:${POSTGRES_PASSWORD:-kotolek}@${DB_HOST:-db}:${DB_PORT:-5432}/${POSTGRES_DB:-kotolek}"
fi

# Запускаем веб-сервер сразу в фоне, чтобы Render сразу увидел открытый порт
echo "🚀 Запуск сервера (порт из \$PORT)..."
python static_server.py &
SERVER_PID=$!

# Ждём готовности БД и создаём таблицы/категории (не блокирует порт).
# Передаём в psycopg2 весь DATABASE_URL, чтобы учитывался sslmode (Render требует SSL).
echo "⏳ Ожидание готовности базы данных..."
until python -c "import psycopg2, os; psycopg2.connect(os.getenv('DATABASE_URL')).close()" 2>/dev/null; do
    sleep 1
done
echo "✅ База данных доступна"

echo "🛠️ Инициализация таблиц и категорий..."
python init_db.py || echo "⚠️ init_db завершился с ошибкой, продолжаем"

if [ -f "/app/kotolek_export.csv" ]; then
    echo "📥 Импорт данных из kotolek_export.csv..."
    python import_csv.py || echo "⚠️ Импорт завершился с ошибкой, продолжаем"
else
    echo "ℹ️ Файл импорта kotolek_export.csv не найден, пропускаем импорт"
fi

echo "✅ Готово. Сервер работает."
wait $SERVER_PID