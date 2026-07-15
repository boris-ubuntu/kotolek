FROM python:3.12-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Backend
COPY backend/ /app/

# Frontend (для раздачи статики)
COPY frontend/ /frontend/

# Скрипт запуска (миграции + импорт + сервер)
COPY backend/start.sh /start.sh
RUN chmod +x /start.sh

EXPOSE 8080

CMD ["/start.sh"]