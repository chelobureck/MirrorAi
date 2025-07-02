# SayDeck API - AI-Powered Presentation Generator

## 📖 Описание проекта

SayDeck - это современный API для генерации презентаций с использованием искусственного интеллекта. Проект поддерживает множественные AI-провайдеры (OpenAI, Groq, Ollama) и предоставляет мощные возможности для создания презентаций из текста, аудио и других источников.

## 🏗️ Архитектура проекта

### Структура файлов и папок

```
SayDeck/
├── 📁 ai_services/           # AI провайдеры и менеджер
│   ├── __init__.py          # Экспорт основных классов
│   ├── base.py              # Базовый класс для всех AI провайдеров  
│   ├── groq_provider.py     # Groq Llama 3.1 провайдер
│   ├── manager.py           # Менеджер AI провайдеров
│   ├── ollama_provider.py   # Ollama локальный провайдер
│   └── openai_provider.py   # OpenAI GPT провайдер
│
├── 📁 config/               # Конфигурация приложения
│   ├── __init__.py          
│   └── settings.py          # Настройки через Pydantic Settings
│
├── 📁 models/               # SQLAlchemy модели базы данных
│   ├── __init__.py          
│   ├── base.py              # Базовая конфигурация БД и сессии
│   ├── board.py             # Модель досок/папок для организации
│   ├── presentation.py      # Модель презентаций
│   ├── template.py          # Модель шаблонов презентаций
│   ├── user.py              # Модель пользователей
│   └── userpreferences.py   # Модель настроек пользователей
│
├── 📁 routers/              # FastAPI роутеры (API endpoints)
│   ├── __init__.py          
│   ├── auth.py              # Аутентификация и авторизация
│   ├── boards.py            # CRUD операции с досками
│   ├── generate_v2.py       # 🚀 Основной роутер генерации AI
│   ├── preferences.py       # Управление настройками пользователей
│   ├── presentations.py     # CRUD операции с презентациями
│   └── templates.py         # Управление шаблонами
│
├── 📁 schemas/              # Pydantic схемы для валидации
│   ├── __init__.py          
│   ├── board.py             # Схемы для досок
│   ├── presentation.py      # Схемы для презентаций
│   ├── template.py          # Схемы для шаблонов
│   ├── user.py              # Схемы для пользователей
│   └── userpreferences.py   # Схемы для настроек
│
├── 📁 utils/                # Утилиты и вспомогательные функции
│   ├── __init__.py          
│   ├── auth.py              # JWT токены, хеширование паролей
│   └── openai_client.py     # Клиент для OpenAI (legacy)
│
├── 📁 uploads/              # Папка для загруженных файлов
│   └── .gitkeep             # Сохраняет папку в Git
│
├── 📁 .vscode/              # Настройки VS Code
│   └── tasks.json           # Task для запуска сервера
│
├── 📄 .dockerignore         # Исключения для Docker сборки
├── 📄 .env                  # Переменные окружения (не в Git!)
├── 📄 .gitignore            # Исключения для Git
├── 📄 docker-compose.yml    # 🐳 Оркестрация контейнеров
├── 📄 Dockerfile            # 🐳 Образ для приложения
├── 📄 main.py               # 🚀 Точка входа FastAPI приложения
├── 📄 requirements.txt      # Python зависимости
└── 📄 README.md             # Документация проекта
```

## 🔧 Детальное описание ключевых файлов

### 🚀 `main.py` - Точка входа приложения
```python
# Основной файл FastAPI приложения
# Содержит:
# - Настройка CORS
# - Регистрация всех роутеров с префиксом /api/v1
# - Startup события для инициализации БД и Redis
# - Health endpoint для мониторинга
```

### ⚙️ `config/settings.py` - Конфигурация
```python
# Pydantic Settings для управления конфигурацией
# Загружает из .env файла:
# - API ключи (OpenAI, Groq)
# - Настройки БД (PostgreSQL)
# - Настройки Redis
# - OAuth настройки
# - CORS настройки
```

### 🧠 `ai_services/` - AI провайдеры

#### `manager.py` - Менеджер AI провайдеров
```python
# Централизованное управление AI провайдерами
# Функции:
# - Автоматическое определение доступных провайдеров
# - Переключение между провайдерами
# - Единый интерфейс для генерации
# - Обработка ошибок и fallback
```

#### `groq_provider.py` - Groq Llama 3.1
```python
# Провайдер для Groq (быстрые open-source модели)
# Особенности:
# - Llama 3.1 70B и 8B модели  
# - Очень быстрая генерация
# - Бесплатный тир с лимитами
# - Structured JSON output
```

#### `openai_provider.py` - OpenAI GPT
```python
# Провайдер для OpenAI GPT-4/3.5
# Особенности:
# - Высочайшее качество генерации
# - Function calling support
# - Платный API
```

#### `ollama_provider.py` - Локальный Ollama
```python
# Провайдер для локальных моделей через Ollama
# Особенности:
# - Полностью приватные модели
# - Работает без интернета
# - Требует мощное железо
```

### 🌐 `routers/generate_v2.py` - Основной API генерации
```python
# Главный роутер для AI генерации
# Endpoints:
# - GET /providers - список доступных AI провайдеров
# - POST /text - генерация из текста  
# - POST /audio - генерация из аудио файла
# - POST /batch - пакетная генерация
# - POST /test/groq - тестирование Groq
# - POST /test/all - тестирование всех провайдеров
```

### 🗄️ `models/` - Модели базы данных

#### `user.py` - Пользователи
```python
# SQLAlchemy модель пользователей
# Поля:
# - email, username, hashed_password
# - role (admin, user)
# - credits (для ограничения использования)
# - email verification
# - связь с preferences
```

#### `presentation.py` - Презентации  
```python
# Модель сохраненных презентаций
# Поля:
# - title, content (JSON структура слайдов)
# - user_id, board_id (связи)
# - is_public, public_id (шаринг)
# - views_count, timestamps
```

#### `board.py` - Доски (папки)
```python
# Организация презентаций в папки
# Поля:
# - name, user_id
# - timestamps
```

### 📋 `schemas/` - Pydantic схемы
```python
# Валидация входящих/исходящих данных
# Каждая схема содержит:
# - Create/Update/Response варианты
# - Валидация полей
# - Автодокументация для Swagger
```

### 🔐 `utils/auth.py` - Аутентификация
```python
# JWT токены и безопасность
# Функции:
# - create_access_token()
# - verify_password() 
# - get_current_user()
# - hash_password()
```

### 🐳 `docker-compose.yml` - Развертывание
```yaml
# Полная инфраструктура в контейнерах:
# - web: FastAPI приложение 
# - db: PostgreSQL 17
# - redis: Redis 7 (rate limiting)
# 
# Особенности:
# - Health checks для БД
# - Volume mounting для live reload
# - Изолированная сеть
```

### 🐳 `Dockerfile` - Образ приложения
```dockerfile
# Мультистадийная сборка Python приложения
# - Python 3.11 slim образ
# - Установка системных зависимостей
# - Копирование и установка Python пакетов
# - Настройка рабочей директории
```

### 📄 `.env` - Переменные окружения
```bash
# Конфиденциальные настройки (НЕ в Git!)
# Содержит:
# - GROQ_API_KEY=gsk_xxx (рабочий ключ)
# - POSTGRES_* настройки БД
# - REDIS_* настройки
# - SECRET_KEY для JWT
# - OPENAI_API_KEY (опционально)
```

## 🚀 Как запустить проект

### Вариант 1: Локальная разработка
```bash
# 1. Активировать виртуальную среду
.venv\Scripts\activate

# 2. Запустить внешние сервисы
docker compose up -d db redis

# 3. Запустить API сервер
uvicorn main:app --reload
```

### Вариант 2: Полное развертывание
```bash
# Запуск всей инфраструктуры
docker compose up -d

# Проверка статуса
docker compose ps
```

## 🧪 Тестирование

### Проверка работоспособности
```bash
# Health check
curl http://localhost:8000/api/v1/health

# Список AI провайдеров  
curl http://localhost:8000/api/v1/generate/providers

# Тест Groq генерации
curl -X POST http://localhost:8000/api/v1/generate/test/groq \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Создай презентацию о блокчейне"}'
```

### Swagger UI
Интерактивная документация доступна по адресу:
- http://localhost:8000/docs

## 🎯 Ключевые особенности

### ✅ Множественные AI провайдеры
- **Groq**: Быстро и бесплатно (Llama 3.1)
- **OpenAI**: Максимальное качество (GPT-4)  
- **Ollama**: Локально и приватно

### ✅ Гибкая архитектура
- Легко добавлять новые AI провайдеры
- Модульная структура
- Асинхронное выполнение

### ✅ Production-ready
- Docker контейнеризация
- База данных PostgreSQL
- Redis для rate limiting
- JWT аутентификация
- Swagger документация

### ✅ Развитые возможности
- Генерация из текста и аудио
- Пакетная обработка  
- Организация в доски/папки
- Публичный шаринг презентаций
- Система шаблонов

## 🔧 Технологический стек

- **Backend**: FastAPI + Python 3.11
- **База данных**: PostgreSQL 17
- **Кеш**: Redis 7
- **AI провайдеры**: Groq, OpenAI, Ollama
- **Контейнеризация**: Docker + Docker Compose
- **ORM**: SQLAlchemy (async)
- **Валидация**: Pydantic v2
- **Аутентификация**: JWT
- **Документация**: OpenAPI/Swagger

## 📊 Статус проекта

✅ **Полностью рабочий проект**
- Все AI провайдеры протестированы
- База данных настроена
- Docker контейнеры работают
- API endpoints функционируют
- Документация актуальна

🎯 **Готов для:**
- Демонстрации коллегам
- Дальнейшей разработки
- Развертывания в продакшене
- Интеграции с фронтендом

---

*Проект создан для хакатона и готов к презентации команде. Все компоненты протестированы и задокументированы.*
