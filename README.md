# SayDeck

SayDeck - это веб-приложение, которое преобразует голосовой ввод в презентации с помощью OpenAI API.

## Возможности

- Регистрация и авторизация пользователей
- Загрузка аудио файлов и их транскрибация через Whisper API
- Генерация структуры презентации с помощью GPT-4
- Сохранение и управление презентациями
- Rate limiting и безопасность

## Требования

- Python 3.11+
- PostgreSQL 15+
- Redis 7+
- Docker и Docker Compose (опционально)

## Локальная установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/yourusername/saydeck.git
cd saydeck
```

2. Создайте файл `.env` в корневой директории:
```env
# Основные настройки
SECRET_KEY=your-secret-key
PROJECT_NAME=SayDeck
VERSION=1.0.0

# База данных
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your-password
POSTGRES_DB=saydeck

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379

# OpenAI
OPENAI_API_KEY=your-openai-api-key
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Запустите приложение:
```bash
uvicorn main:app --reload
```

## Запуск с Docker

1. Создайте файл `.env` (как описано выше)

2. Запустите с помощью Docker Compose:
```bash
docker-compose up --build
```

## Деплой на Render

1. Создайте новый Web Service на Render
2. Подключите ваш GitHub репозиторий
3. Настройте следующие переменные окружения:
   - `POSTGRES_USER`
   - `POSTGRES_PASSWORD`
   - `POSTGRES_DB`
   - `SECRET_KEY`
   - `OPENAI_API_KEY`
   - `REDIS_HOST`
   - `REDIS_PORT`

4. Настройте следующие параметры:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

5. Добавьте PostgreSQL и Redis как отдельные сервисы в Render

## API Endpoints

- `POST /api/v1/auth/register` - Регистрация пользователя
- `POST /api/v1/auth/login` - Авторизация
- `POST /api/v1/generate/audio` - Генерация презентации из аудио
- `POST /api/v1/generate/text` - Генерация презентации из текста
- `GET /api/v1/presentations` - Список презентаций
- `GET /api/v1/presentations/{id}` - Получение презентации по ID

## Безопасность

- JWT аутентификация
- Rate limiting через Redis
- CORS настройки
- Валидация входных данных
- Ограничение размера файлов

## Лицензия

MIT 