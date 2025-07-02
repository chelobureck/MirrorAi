# SayDeck - Готовый проект для хакатона

## ✅ Что сделано:
- **Очищена структура проекта** - удалены лишние файлы
- **Обновлен requirements.txt** с актуальными зависимостями
- **Исправлен OpenAI клиент** для работы с новым API
- **Рефакторинг config/settings.py** - убраны дубли
- **Обновлен .gitignore** для игнорирования временных файлов
- **Создан .env** с чистыми настройками
- **Redis порт изменен** с 6379 на 6378 для избежания конфликтов

## 📁 Структура проекта:
```
├── main.py              # Основное приложение FastAPI
├── requirements.txt     # Зависимости Python
├── .env                # Переменные окружения
├── Dockerfile          # Docker конфигурация
├── docker-compose.yml  # Docker Compose
├── config/             # Настройки приложения
├── models/             # SQLAlchemy модели
├── routers/            # FastAPI роутеры
├── schemas/            # Pydantic схемы
├── utils/              # Утилиты (auth, openai_client)
├── uploads/            # Папка для загрузок
└── tests.py           # Базовые тесты
```

### 📋 Задачи на хакатон:
- [x] ✅ **API Endpoints реализованы**:
  - POST `/api/v1/auth/register` - Регистрация пользователя ✅
  - POST `/api/v1/auth/login` - Авторизация ✅
  - POST `/api/v1/generate/audio` - Генерация из аудио ✅
  - POST `/api/v1/generate/text` - Генерация из текста ✅
  - GET `/api/v1/presentations` - Список презентаций ✅
  - GET `/api/v1/presentations/{id}` - Получение по ID ✅

- [x] ✅ **Безопасность настроена**:
  - JWT аутентификация ✅
  - Rate limiting через Redis (5/мин аудио, 10/мин текст) ✅
  - CORS настройки ✅
  - Валидация входных данных ✅
  - Ограничение размера файлов ✅

- [x] ✅ **База данных и тестирование**:
  - PostgreSQL подключена и работает ✅
  - Тестовые данные созданы ✅
  - Тестовая HTML страница для проверки API ✅
  - Swagger документация доступна ✅

- [ ] Добавить новые AI модели (Groq, Llama)
- [ ] Улучшить генерацию презентаций
- [ ] Добавить новые форматы экспорта
- [ ] Оптимизировать производительность
- [ ] Добавить новые типы шаблонов

### 🚀 Как запустить:
```bash
# Остановить существующие контейнеры
docker-compose down

# Запустить проект
docker-compose up -d

# Проверить логи
docker-compose logs -f web
```

### 🔧 Полезные команды:
```bash
# Войти в контейнер приложения
docker-compose exec web bash

# Войти в PostgreSQL
docker-compose exec db psql -U say_deck_user -d say_deck

# Перезапустить только веб-сервис
docker-compose restart web

# Посмотреть все контейнеры
docker ps -a
```

### 📝 Заметки:
- Проект использует FastAPI + PostgreSQL + Redis + OpenAI
- Порты: Web:8000, DB:5432, Redis:6378
- Все настройки в .env файле
- API документация доступна на http://localhost:8000/docs

### 🧪 Тестирование:
- **Swagger UI**: http://localhost:8000/docs
- **Тестовая страница**: `test_page.html` (откройте в браузере)
- **Тестовые данные**: `create_test_data.py`
- **Тестовый пользователь**: 
  - Email: `testuser3@example.com`
  - Password: `password123`

### ✅ Проверенные функции:
- ✅ Регистрация нового пользователя
- ✅ Авторизация существующего пользователя
- ✅ JWT токены работают
- ✅ Rate limiting активен
- ✅ PostgreSQL подключение работает
- ✅ Redis кэширование работает
- ✅ CORS настроен правильно
- ✅ Swagger документация отображается

---
**Автор:** bestcomp  
**Дата:** July 3, 2025  
**Ветка:** hackathon-bestcomp
**Статус:** 🚀 Готов к хакатону!
