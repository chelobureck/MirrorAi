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
- [ ] Добавить новые AI модели
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

---
**Автор:** bestcomp  
**Дата:** $(date)  
**Ветка:** hackathon-bestcomp
