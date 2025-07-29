# 📋 Объяснение переменных окружения SayDeck

## 🔧 Основные настройки (уже есть значения по умолчанию)

### `API_V1_STR` = "/api/v1"
- **Откуда:** встроено в код
- **Зачем:** префикс для всех API эндпоинтов
- **Пример:** GET /api/v1/health

### `BACKEND_CORS_ORIGINS`
- **Откуда:** настроено в settings.py по умолчанию
- **Зачем:** разрешенные домены для CORS (безопасность браузера)
- **По умолчанию:** localhost:3000, localhost:8000, etc.

## 🔒 Безопасность (ОБЯЗАТЕЛЬНО поменять для продакшена!)

### `SECRET_KEY`
- **Откуда:** ПРИДУМАЙТЕ СВОЙ! 
- **Зачем:** шифрование JWT токенов
- **Как получить:** любая длинная случайная строка
- **Пример:** `openssl rand -hex 32` или просто длинная фраза

### `ALGORITHM` = "HS256"
- **Откуда:** стандарт JWT
- **Зачем:** алгоритм шифрования токенов

### `ACCESS_TOKEN_EXPIRE_MINUTES` = 30
- **Откуда:** настройка FastAPI
- **Зачем:** время жизни JWT токенов в минутах

## 🤖 AI API ключи (ОБЯЗАТЕЛЬНО настроить!)

### `OPENAI_API_KEY`
- **Откуда:** https://platform.openai.com/api-keys
- **Зачем:** для работы с ChatGPT
- **Формат:** sk-proj-xxxxxxxxxxxx

### `GROQ_API_KEY`
- **Откуда:** https://console.groq.com/keys
- **Зачем:** альтернативный AI провайдер (быстрее OpenAI)
- **Формат:** gsk_xxxxxxxxxxxx

## 💾 База данных (работает без настройки)

### `USE_POSTGRES` = false
- **По умолчанию:** использует SQLite (файл saydeck.db)
- **Зачем:** переключение между SQLite и PostgreSQL

### Переменные PostgreSQL (только если USE_POSTGRES=true):
- `POSTGRES_USER` - имя пользователя БД
- `POSTGRES_PASSWORD` - пароль БД  
- `POSTGRES_DB` - название базы данных
- `POSTGRES_SERVER` - адрес сервера БД
- `POSTGRES_PORT` - порт БД (обычно 5432)

## ⚡ Redis (опционально, для rate limiting)

### `REDIS_HOST` = localhost
### `REDIS_PORT` = 6379
- **Зачем:** ограничение частоты запросов к API
- **Можно без него:** код работает без Redis

## 🎨 Дополнительные API (опционально)

### `PEXELS_API_KEY`
- **Откуда:** https://www.pexels.com/api/
- **Зачем:** поиск изображений для презентаций

### `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`
- **Откуда:** Google Cloud Console
- **Зачем:** авторизация через Google

## 📝 Минимальный .env для запуска:

```bash
# Только эти 2 переменные ОБЯЗАТЕЛЬНЫ:
SECRET_KEY=your-super-secret-random-string-here
OPENAI_API_KEY=sk-your-openai-key-here

# Все остальное работает по умолчанию!
```

## 🚀 Для быстрого старта используйте:
1. Скопируйте `.env.simple` в `.env`
2. Поменяйте `SECRET_KEY` на свой
3. Вставьте свой `OPENAI_API_KEY`
4. Запускайте!

## ⚠️ ВАЖНО:
- Все переменные с пустыми значениями ("") в settings.py имеют рабочие значения по умолчанию
- Проект запустится даже без .env файла
- Но GPT функции не будут работать без OPENAI_API_KEY
