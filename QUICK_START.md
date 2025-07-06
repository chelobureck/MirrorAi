# 🚀 SayDeck - Инструкция по запуску

## Быстрый старт (3 команды)

```bash
# 1. Клонирование
git clone <your-repository-url>
cd SayDeck

# 2. Настройка .env (добавьте свои API ключи)
cp .env.example .env
# Отредактируйте .env: GROQ_API_KEY, SECRET_KEY

# 3. Запуск
docker-compose up -d
```

**Готово!** API доступно по адресу: http://localhost:8000

## 📋 Проверка работы

1. **Health Check:**
   ```bash
   curl http://localhost:8000/api/v1/health
   ```

2. **Swagger UI:** http://localhost:8000/docs

3. **Тест генерации для гостя:**
   ```bash
   curl -X POST "http://localhost:8000/api/v1/generate-presentation" \
     -H "Content-Type: application/json" \
     -d '{"topic": "Тест", "slides_count": 3}'
   ```

4. **Автоматическое тестирование:**
   ```bash
   python test_tz_implementation.py
   ```

## ⚙️ Настройки

### Основные переменные в .env:
```env
SECRET_KEY=your-secret-key-256-bits
GROQ_API_KEY=your-groq-api-key
USE_POSTGRES=true
IMAGE_MICROSERVICE_URL=http://image-service:8080
```

### Структура проекта:
```
presentations/           # Файлы презентаций
├── user_<id>/          # Авторизованные пользователи  
└── guest_<session>/    # Гостевые сессии
    └── <presentation_id>/
        ├── raw.html    # Без картинок
        └── final.html  # С картинками
```

## 🔗 API Эндпоинты

| Метод | URL | Описание |
|-------|-----|----------|
| `POST` | `/api/v1/generate-presentation` | 🎯 Главный эндпоинт генерации |
| `GET` | `/api/v1/guest-credits` | 💰 Проверка кредитов гостя |
| `GET` | `/api/v1/health` | 🏥 Проверка работоспособности |
| `GET` | `/docs` | 📚 Swagger документация |

## 🐳 Docker команды

```bash
# Запуск
docker-compose up -d

# Логи
docker-compose logs -f app

# Остановка
docker-compose down

# Пересборка
docker-compose up -d --build
```

## 🔧 Разработка

```bash
# Локальный запуск без Docker
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
uvicorn main:app --reload
```

## 📊 Система кредитов

- **Гости:** 50 кредитов → -1 за генерацию → блокировка при 0
- **Пользователи:** Неограниченная генерация
- **Хранение:** Redis (быстро) + PostgreSQL (надежно)

---

**🎉 Готово к работе!** Все требования ТЗ реализованы.
