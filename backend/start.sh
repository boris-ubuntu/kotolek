#!/bin/sh
set -e

# Собираем DATABASE_URL из переменных окружения (как в app/config.py)
export DATABASE_URL="postgresql://${POSTGRES_USER:-kotolek}:${POSTGRES_PASSWORD:-kotolek}@${DB_HOST:-db}:${DB_PORT:-5432}/${POSTGRES_DB:-kotolek}"

echo "⏳ Ожидание готовности базы данных..."
until python -c "import psycopg2, os; from urllib.parse import urlparse; u=urlparse(os.getenv('DATABASE_URL')); psycopg2.connect(host=u.hostname, port=u.port, user=u.username, password=u.password, dbname=u.path[1:]).close()" 2>/dev/null; do
    sleep 1
done
echo "✅ База данных доступна"

echo "🛠️ Инициализация таблиц и категорий..."
python init_db.py

if [ -f "/app/kotolek_export.csv" ]; then
    echo "📥 Импорт данных из kotolek_export.csv..."
    python import_csv.py
else
    echo "ℹ️ Файл импорта kotolek_export.csv не найден, пропускаем импорт"
fi

echo "🚀 Запуск сервера на http://0.0.0.0:8080"
exec python static_server.py
