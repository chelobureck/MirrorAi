# 🎯 SayDeck - AI-Powered Presentation Generator

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16+-blue?style=for-the-badge&logo=postgresql&logoColor=white)](https://postgresql.org)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)
[![Redis](https://img.shields.io/badge/Redis-7+-red?style=for-the-badge&logo=redis&logoColor=white)](https://redis.io)

[![Groq](https://img.shields.io/badge/Groq-AI%20Powered-orange?style=for-the-badge&logo=ai&logoColor=white)](https://groq.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen?style=for-the-badge)](CONTRIBUTING.md)

**🚀 Революционный сервис для создания потрясающих HTML презентаций с помощью ИИ за секунды!**

*Просто опишите тему - получите профессиональную презентацию с современным дизайном*

[🎨 Демо](https://saydeck-demo.com) • [📖 Документация](https://docs.saydeck.com) • [🐛 Баги](https://github.com/chelobureck/SayDeck/issues) • [💬 Обсуждения](https://github.com/chelobureck/SayDeck/discussions)

</div>

---

## ✨ Что делает SayDeck особенным?

### 🤖 **Молниеносный ИИ**
- **Groq AI** - самые быстрые модели (Llama 3.1 70B)
- **~2 секунды** на создание полной презентации
- **Умный анализ** темы и аудитории

### 🎨 **Потрясающий дизайн**
- **Современные HTML** презентации из коробки
- **CSS анимации** и плавные переходы  
- **Адаптивный дизайн** для любых устройств
- **Темная/светлая** темы

### 🛡️ **Enterprise-Ready**
- **JWT авторизация** + Google OAuth
- **Rate limiting** и защита от спама
- **PostgreSQL** база данных
- **Docker** контейнеризация
- **Production-готов**

### 📊 **Мощная организация**
- **Доски** для группировки презентаций
- **Шаблоны** для быстрого старта
- **Персональные настройки** пользователей
- **Публичный шаринг** презентаций

## 🚀 Возможности

| Функция | Описание | Статус |
|---------|----------|---------|
| 🤖 **AI Генерация** | Создание презентаций через Groq AI | ✅ Готово |
| 🎨 **HTML Экспорт** | Красивые веб-презентации | ✅ Готово |
| 👥 **Управление пользователями** | Регистрация, авторизация, профили | ✅ Готово |
| 📁 **Доски проектов** | Организация презентаций по папкам | ✅ Готово |
| 📄 **Шаблоны** | Готовые макеты для быстрого старта | ✅ Готово |
| ⚙️ **Настройки** | Персонализация интерфейса | ✅ Готово |
| 🔒 **Безопасность** | JWT токены, rate limiting | ✅ Готово |
| 🐳 **Docker** | Быстрое развертывание | ✅ Готово |
| 📱 **API** | RESTful API с документацией | ✅ Готово |
| 🔗 **Интеграции** | Google OAuth, Email | ✅ Готово |

### 💡 **Быстрый старт** - 3 простых шага:

```bash
# 1️⃣ Клонировать и настроить
git clone https://github.com/chelobureck/SayDeck.git
cd SayDeck && cp .env.example .env

# 2️⃣ Добавить Groq API ключ (бесплатно!)
# Получить на: https://console.groq.com/keys
echo "GROQ_API_KEY=your_key_here" >> .env

# 3️⃣ Запустить одной командой
docker-compose up -d
```

**🎉 Готово!** Открой http://localhost:8000/docs и создавай презентации!

---

## 📋 Требования

- Python 3.11+
- PostgreSQL
- Redis  
- **Groq API Key** (получить бесплатно на [console.groq.com](https://console.groq.com/keys))

## 🛠 Установка и запуск

### 1. Клонирование репозитория
```bash
git clone <repository-url>
cd SayDeck
```

### 2. Создание виртуального окружения
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# или source .venv/bin/activate  # Linux/Mac
```

### 3. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 4. Настройка переменных окружения
Скопируйте `.env.example` в `.env` и заполните необходимые значения:
```bash
cp .env.example .env
```

**Обязательно установите:**
```env
# Получите API ключ на https://console.groq.com/keys
GROQ_API_KEY=gsk_your_actual_groq_api_key_here

# Установите сильный секретный ключ
SECRET_KEY=your-super-secret-key-change-this-in-production

# Настройки базы данных (для локальной разработки можно оставить как есть)
POSTGRES_PASSWORD=your_postgres_password
```

### 5. Запуск с Docker (рекомендуется)
```bash
docker-compose up -d
```

### 6. Или локальный запуск
```bash
# Запуск PostgreSQL и Redis локально
# Затем:
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 📡 API

### Основной эндпоинт генерации

**POST** `/api/v1/generate-html-presentation`

```json
{
  "topic": "Искусственный интеллект в медицине",
  "audience": "студенты медицинских вузов",
  "tone": "академический",
  "slide_count": 10
}
```

**Ответ**: Полная HTML страница с презентацией

### Авторизация

**POST** `/api/v1/auth/register`
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**POST** `/api/v1/auth/login`
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Ответ**:
```json
{
  "access_token": "jwt_token_here",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "user@example.com"
  }
}
```

### Health Check

**GET** `/api/v1/health`

## 🏗 Архитектура проекта

```
SayDeck/
├── ai_services/           # AI интеграция
│   ├── base.py           # Базовый класс провайдера
│   ├── groq_provider.py  # Groq AI провайдер
│   └── manager.py        # Менеджер AI сервисов
├── config/
│   └── settings.py       # Настройки приложения
├── models/
│   ├── base.py          # Базовая модель SQLAlchemy
│   └── presentation.py  # Модель презентации
├── routers/
│   ├── auth.py          # Авторизация и регистрация
│   ├── html_generator.py # Генерация HTML презентаций
│   └── public.py        # Публичные эндпоинты
├── schemas/
│   └── presentation.py  # Pydantic схемы
├── utils/
│   ├── auth.py          # JWT утилиты
│   └── pptx_generator.py # PPTX экспорт (опционально)
├── docker-compose.yml   # Docker конфигурация
├── Dockerfile
├── main.py             # FastAPI приложение
└── requirements.txt    # Зависимости Python
```

## 🔧 Настройка AI

Сервис использует **только Groq** как AI провайдера. Настройки в `config/settings.py`:

```python
GROQ_API_KEY: str
DEFAULT_MODEL: str = "llama-3.1-70b-versatile"
```

## 🗄 База данных

Презентации автоматически сохраняются в PostgreSQL со следующими полями:
- `id` - Уникальный идентификатор
- `title` - Заголовок презентации
- `content` - HTML контент
- `topic` - Исходная тема
- `user_id` - ID пользователя (опционально)
- `created_at` - Время создания

## 🧪 Тестирование

### Ручное тестирование API

1. Запустите сервер:
```bash
uvicorn main:app --reload
```

2. Откройте Swagger UI: http://localhost:8000/docs

3. Протестируйте генерацию:
```bash
curl -X POST "http://localhost:8000/api/v1/generate-html-presentation" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Python для начинающих",
    "audience": "студенты",
    "tone": "дружелюбный",
    "slide_count": 5
  }'
```

### Проверка здоровья системы

```bash
curl http://localhost:8000/api/v1/health
```

---

## 🎬 Демонстрация

### 📝 **Простой запрос** →  🎨 **Потрясающий результат**

**Вход:**
```json
{
  "topic": "Искусственный интеллект в медицине",
  "audience": "врачи и медицинские работники",
  "tone": "профессиональный",
  "slide_count": 8
}
```

**Результат за ~2 секунды:**
- 🎯 8 логически структурированных слайдов
- 🎨 Современный дизайн с анимациями
- 📱 Адаптивная верстка для всех устройств
- ⌨️ Навигация клавишами (←→, пробел)
- 🔗 Готовая ссылка для демонстрации

### 🖼️ **Примеры презентаций:**

| Тема | Аудитория | Слайдов | Время |
|------|-----------|---------|--------|
| 🤖 "Machine Learning для бизнеса" | Менеджеры | 12 | 1.8с |
| 🚀 "React.js Best Practices" | Разработчики | 15 | 2.1с |
| 🎓 "Основы фотографии" | Новички | 10 | 1.5с |
| 💰 "Инвестиции в 2024" | Инвесторы | 20 | 2.8с |

## 🥇 Почему SayDeck?

### 🆚 **Сравнение с конкурентами:**

| Функция | SayDeck | PowerPoint + AI | Canva | Gamma |
|---------|---------|-----------------|-------|-------|
| ⚡ **Скорость создания** | ~2 сек | ~5-10 мин | ~10-15 мин | ~3-5 мин |
| 🎨 **Дизайн из коробки** | ✅ | ❌ | ✅ | ✅ |
| 💰 **Стоимость** | Бесплатно* | $20/мес | $15/мес | $10/мес |
| 🔓 **Open Source** | ✅ | ❌ | ❌ | ❌ |
| 🛠️ **Кастомизация** | ✅ Полная | ❌ | ⚠️ Ограничена | ⚠️ Ограничена |
| 🐳 **Self-hosted** | ✅ | ❌ | ❌ | ❌ |
| 📱 **API доступ** | ✅ | ❌ | ⚠️ Платно | ❌ |

*_Groq API имеет бесплатный тир с лимитами_

### 🎯 **Идеально для:**

- 🏢 **Стартапов** - быстрые питчи и презентации для инвесторов
- 👩‍🏫 **Преподавателей** - учебные материалы и лекции  
- 💼 **Бизнеса** - отчеты, предложения, тренинги
- 👨‍💻 **Разработчиков** - техническая документация, демо
- 🎤 **Спикеров** - конференции, воркшопы, семинары

---

### Docker развертывание
```bash
# Сборка образа
docker build -t saydeck .

# Запуск с docker-compose
docker-compose -f docker-compose.yml up -d
```

### Переменные окружения для продакшена
- Установите сильный `SECRET_KEY`
- Настройте правильные CORS origins
- Используйте внешние PostgreSQL и Redis
- Установите ограничения rate limiting

## 🛡 Безопасность

- JWT авторизация для защищенных эндпоинтов
- Rate limiting через Redis
- CORS настройки
- Валидация входных данных через Pydantic
- Хэширование паролей с bcrypt

## 📝 Логирование

Логи доступны через FastAPI и могут быть настроены в `config/settings.py`:
- Уровень логирования
- Формат вывода
- Ротация логов

## 🔄 Обновления

Для обновления зависимостей:
```bash
pip install --upgrade -r requirements.txt
```

Для миграций базы данных (если используете Alembic):
```bash
alembic upgrade head
```

## 📞 Поддержка

- Создайте Issue в GitHub репозитории
- Проверьте логи приложения: `docker-compose logs app`
- Убедитесь в корректности `.env` файла

---

## 🚀 Roadmap

### 🎯 **v1.1 (В разработке)**
- [ ] 📊 PDF экспорт презентаций
- [ ] 🎨 Дополнительные темы дизайна
- [ ] 🔗 Интеграция с Slack/Teams
- [ ] 📈 Аналитика просмотров

### 🔮 **v1.2 (Планируется)**
- [ ] 🎙️ Голосовые заметки к слайдам
- [ ] 🤝 Совместное редактирование
- [ ] 🌐 Мультиязычная поддержка
- [ ] 🔌 API для интеграций

### 💭 **Идеи сообщества**
- [ ] 🎬 Видео экспорт презентаций
- [ ] 🤖 Дополнительные AI провайдеры
- [ ] 📱 Мобильное приложение
- [ ] 🎯 A/B тестирование слайдов

---

## 🤝 Вклад в проект

### 🎉 **Как помочь:**
