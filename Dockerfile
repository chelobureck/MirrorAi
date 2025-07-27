FROM python:3.11-slim

# Создаем non-root пользователя для безопасности
RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

# Обновление pip
RUN pip install --upgrade pip

# Установка только необходимых системных зависимостей
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Копирование файлов зависимостей
COPY requirements.txt .

# Установка Python зависимостей без кеша
RUN pip install --no-cache-dir -r requirements.txt

# Копирование исходного кода (через .dockerignore исключаем ненужные файлы)
COPY . .

# Создание директорий и настройка прав
RUN mkdir -p uploads presentations && \
    chown -R appuser:appuser /app

# Переключаемся на non-root пользователя
USER appuser

# Открытие порта 80 для AWS ECS
EXPOSE 80

# Healthcheck для AWS ECS
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:80/health || exit 1

# Запуск приложения на порту 80
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
