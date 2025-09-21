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

**🚀 Revolutionary AI-powered service for creating stunning HTML presentations in seconds!**

*Simply describe your topic - get a professional presentation with modern design and relevant images*

[🌐 Live Demo](https://saydeck.onrender.com) | [📖 API Docs](https://saydeck.onrender.com/docs) | [🚀 Quick Start](#-quick-start)

</div>

---

## 🆕 Latest Features 

### 🎨 **Enhanced Presentation Generator**
- **Complete CRUD operations** - Create, Read, Update, Delete presentations
- **Advanced image integration** with Pexels API
- **Smart content analysis** for optimal image selection
- **Real-time HTML preview** generation

### 👥 **Guest Credits System**
- **50 free presentations** for unregistered users
- **Smart tracking** via Redis + PostgreSQL
- **Instant balance checking** and management

### 🖼️ **Image Microservice Integration**
- **Automatic search** for relevant images
- **HTML processing** with image insertion
- **Valid image URLs** in final presentations

### 💾 **Dual File Storage**
- **raw.html** - original presentation without images
- **final.html** - final version with images
- **Structured storage** `/presentations/<user_or_guest_id>/<presentation_id>/`

### ⚡ **Unified API Endpoints**
- **Main generation** - `/api/v1/generate-presentation`
- **Enhanced CRUD** - `/api/v1/enhanced/*`
- **Template system** - `/api/v1/templates/*`
- **User management** - `/api/v1/auth/*`

## ✨ Key Features

### 🤖 **Lightning-Fast AI**
- **Groq AI** - fastest models available (Llama 3.1 70B)
- **~2 seconds** for complete presentation generation
- **Smart topic analysis** and audience adaptation

### 🎨 **Modern Design**
- **Beautiful HTML presentations** out of the box
- **CSS animations** and smooth transitions  
- **Responsive design** for any device
- **Image integration** via microservice

### 🛡️ **Enterprise-Ready**
- **JWT authentication** + optional guest access
- **Rate limiting** and spam protection
- **PostgreSQL + Redis** for reliable data storage
- **Docker** containerization
- **Production-ready** deployment

### 📊 **Powerful Organization**
- **Boards** for grouping presentations
- **Templates** for quick start
- **User preferences** customization
- **Public sharing** capabilities

## 🚀 Features

| Feature | Description | Status |
|---------|-------------|---------|
| 🤖 **AI Generation** | Create presentations via Groq AI | ✅ Ready |
| 🖼️ **Smart Images** | Automatic image search (Pexels API) | 🆕 New |
| 🎨 **HTML Export** | Beautiful web presentations with images | ✅ Ready |
| 👥 **User Management** | Registration, authentication, profiles | ✅ Ready |
| 📁 **Project Boards** | Organize presentations in folders | ✅ Ready |
| 📄 **Templates** | Ready-made layouts for quick start | ✅ Ready |
| ⚙️ **Settings** | Interface personalization | ✅ Ready |
| 🔒 **Security** | JWT tokens, rate limiting | ✅ Ready |
| 🐳 **Docker** | Fast deployment | ✅ Ready |
| 📱 **API** | RESTful API with documentation | ✅ Ready |
| 🔗 **Integrations** | Google OAuth, Email | ✅ Ready |

### 💡 **Quick Start** - 3 simple steps:

```bash
# 1️⃣ Clone and setup
git clone https://github.com/chelobureck/SayDeck.git
cd SayDeck && cp .env.example .env

# 2️⃣ Add Groq API key (free!)
# Get it at: https://console.groq.com/keys
echo "GROQ_API_KEY=your_key_here" >> .env

# 3️⃣ Launch with one command
docker-compose up -d
```

**🎉 Done!** Open http://localhost:8000/docs and start creating presentations!

---

## 📋 Requirements

- Python 3.11+
- PostgreSQL
- Redis  
- **Groq API Key** (get free at [console.groq.com](https://console.groq.com/keys))

## 🛠 Installation & Setup

### 🐳 **Option 1: Docker (Recommended)**

```bash
# Clone repository
git clone https://github.com/chelobureck/SayDeck.git
cd SayDeck

# Setup environment
cp .env.example .env
# Edit .env file and add your API keys

# Launch with Docker
docker-compose up -d

# Check services
docker-compose ps
```

### 🐍 **Option 2: Local Development**

```bash
# Clone repository
git clone https://github.com/chelobureck/SayDeck.git
cd SayDeck

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# or source .venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env file

# Run database migrations
python -c "from models.base import init_db; init_db()"

# Start server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 🔧 **Environment Configuration**

Create `.env` file with the following settings:
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

## 📡 API Reference

### 🎯 **Основной эндпоинт генерации (NEW)**

**POST** `/api/v1/generate-presentation`

Единая точка входа для создания презентаций. Автоматически определяет статус пользователя (авторизованный или гость) и применяет соответствующую логику кредитов.

#### Запрос:
```json
{
  "topic": "Искусственный интеллект в медицине",
  "content": "Применение машинного обучения для диагностики заболеваний",
  "slides_count": 5,
  "language": "ru",
  "style": "modern"
}
```

#### Заголовки:
- `Authorization: Bearer <jwt_token>` (опционально, для авторизованных пользователей)
- `X-Guest-Session: <session_id>` (опционально, для отслеживания гостевой сессии)

#### Ответ для авторизованного пользователя:
```json
{
  "presentation_id": "uuid-presentation-id",
  "html": "<html>...</html>"
}
```

#### Ответ для гостя:
```json
{
  "presentation_id": "uuid-presentation-id", 
  "html": "<html>...</html>"
}
```

**Заголовки ответа для гостя:**
- `X-Guest-Session: <session_id>` - ID сессии для дальнейшего использования
- `X-Guest-Credits: <number>` - Оставшееся количество кредитов

#### Возможные ошибки:
- **403** - `{"error": "Not enough credits"}` - У гостя недостаточно кредитов
- **500** - `{"error": "Generation failed: <details>"}` - Ошибка генерации

### 👥 **Проверка кредитов гостя**

**GET** `/api/v1/guest-credits`

#### Заголовки:
- `X-Guest-Session: <session_id>` (обязательно)

#### Ответ:
```json
{
  "session_id": "guest-session-uuid",
  "credits": 45,
  "credits_used": 5
}
```

### 🔐 **Авторизация**

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

### ❤️ **Health Check**

**GET** `/api/v1/health`

**GET** `/` - Корневой эндпоинт

## 🏗 Архитектура проекта

```
SayDeck/
├── ai_services/           # AI интеграция
│   ├── base.py           # Базовый класс провайдера
│   ├── groq_provider.py  # Groq AI провайдер
│   └── manager.py        # Менеджер AI сервисов
├── config/
├── models/              # SQLAlchemy models
│   ├── base.py         # Base model
│   ├── presentation.py # Presentation model
│   ├── user.py        # User model
│   ├── board.py       # Board model
│   ├── template.py    # Template model
│   └── guest_session.py # 🆕 Guest session model
├── routers/             # FastAPI routers
│   ├── auth.py        # Authentication & registration
│   ├── main_generation.py # 🆕 Main generation endpoint
│   ├── enhanced_generator.py # 🆕 Enhanced generation with images
│   ├── presentations.py # Presentation management
│   ├── boards.py      # Board management
│   ├── templates.py   # Template management
│   └── public.py      # Public endpoints
├── schemas/             # Pydantic schemas
│   ├── presentation.py # Presentation schemas
│   ├── user.py       # User schemas
│   ├── board.py      # Board schemas
│   ├── template.py   # Template schemas
│   └── generation.py  # 🆕 Generation schemas
├── services/            # 🆕 Business logic
│   ├── guest_credits.py    # Guest credit management
│   ├── presentation_files.py # Presentation file storage
│   ├── template_service.py  # Template service
│   └── image_microservice.py # Image service integration
├── utils/
│   ├── auth.py        # JWT utilities + optional auth
│   ├── email.py       # Email utilities
│   └── pptx_generator.py # PowerPoint generation
├── presentations/       # 🆕 Presentation files directory
│   └── <user_or_guest_id>/
│       └── <presentation_id>/
│           ├── raw.html    # Original HTML without images
│           └── final.html  # Final HTML with images
├── docker-compose.yml   # Docker configuration
├── Dockerfile
├── main.py             # FastAPI application
└── requirements.txt    # Python dependencies
```

### 🆕 **Key Architecture Changes:**

1. **Service Layer** (`services/`) - Business logic extracted from routers
2. **Guest Sessions** - New model for tracking unregistered user credits
3. **File Storage** - Structured storage for raw/final HTML files
4. **Microservice Integration** - Client for external image service
5. **Optional Authentication** - Support for both authenticated users and guests
6. **Enhanced Generation** - Advanced presentation generation with images

## 🔧 AI Configuration

The service uses **Groq AI** as the primary provider. Configuration in `config/settings.py`:

```python
GROQ_API_KEY: str = "gsk_your_api_key_here"
DEFAULT_MODEL: str = "llama-3.1-70b-versatile"
```

## 🗄 Database

### Main Tables:

#### `presentations` - Presentations
- `id` - Unique identifier
- `title` - Presentation title
- `content` - HTML content
- `topic` - Original topic
- `user_id` - User ID (can be NULL for guests)
- `board_id` - Board ID for organization
- `created_at` - Creation time

#### `guest_sessions` - 🆕 Guest Sessions
- `id` - Unique identifier
- `session_id` - Guest session UUID
- `credits` - Number of credits (initial: 50)
- `ip_address` - Guest IP address
- `user_agent` - Browser User-Agent
- `is_active` - Session activity status
- `created_at` - Creation time
- `last_used_at` - Last usage time

#### `users` - Users
- `id` - Unique identifier
- `email` - Email address
- `hashed_password` - Hashed password
- `name` - User name
- `is_active` - Account activity
- `created_at` - Registration time

#### `boards` - Project Boards
- `id` - Unique identifier
- `name` - Board name
- `description` - Board description
- `user_id` - Owner ID
- `is_public` - Public visibility

#### `templates` - Presentation Templates
- `id` - Unique identifier
- `name` - Template name
- `description` - Template description
- `content` - Template HTML
- `is_public` - Public availability

### Guest Credit Storage:
- **Redis** - Primary storage (fast access)
- **PostgreSQL** - Backup storage (persistence)
- **TTL** - 7 days for automatic cleanup of inactive sessions

## 🧪 Testing

### Manual API Testing

1. **Start the server:**
```bash
uvicorn main:app --reload
```

2. **Open Swagger UI:** http://localhost:8000/docs

3. **Test the main endpoint:**

#### 👤 Guest Test (no authentication):
```bash
curl -X POST "http://localhost:8000/api/v1/generate-presentation" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Artificial Intelligence", 
    "content": "Machine learning fundamentals",
    "slides_count": 3,
    "language": "en"
  }'
```

#### 🔐 Authenticated User Test:
```bash
# First, login
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123"
  }'

# Then generate presentation
curl -X POST "http://localhost:8000/api/v1/generate-presentation" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <jwt_token>" \
  -d '{
    "topic": "Blockchain Technology",
    "slides_count": 6
  }'
```

#### 🎨 Enhanced Generation Test:
```bash
curl -X POST "http://localhost:8000/api/v1/enhanced/generate" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <jwt_token>" \
  -d '{
    "topic": "Data Science",
    "slides_count": 5,
    "include_images": true,
    "image_style": "professional"
  }'
```

## 🚀 Production Deployment

### � **Docker Production**

```bash
# 1. Clone and setup
git clone https://github.com/chelobureck/SayDeck.git
cd SayDeck

# 2. Setup production environment
cp .env.example .env
# Edit .env with production settings

# 3. Launch in production mode
docker-compose up -d

# 4. Check services
docker-compose ps
```

### � **Important Production Settings:**

```env
# Security
SECRET_KEY=your-super-strong-production-secret-key-256-bits
USE_POSTGRES=true

# Database
POSTGRES_PASSWORD=strong-production-password
POSTGRES_SERVER=your-postgres-host
POSTGRES_PORT=5432

# Redis
REDIS_HOST=your-redis-host
REDIS_PORT=6379

# AI Services
GROQ_API_KEY=your-production-groq-key
PEXELS_API_KEY=your-pexels-key

# Microservices
IMAGE_MICROSERVICE_URL=http://your-image-service:8080
IMAGE_MICROSERVICE_TIMEOUT=30
```

### � **Monitoring**

```bash
# Check container status
docker-compose ps

# Application logs
docker-compose logs -f app

# Database logs
docker-compose logs -f postgres

# Redis logs
docker-compose logs -f redis

# Resource monitoring
docker stats
```

## 💻 Development

### 🔧 **Development Setup**

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Code formatting
black . --check
isort . --check-only

# Type checking
mypy .

# Linting
flake8 .
```

### 🧪 **Testing**

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_generation.py

# Run with coverage
pytest --cov=. --cov-report=html

# Test specific endpoint
pytest tests/test_auth.py::test_login
```

### 📝 **API Documentation**

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 🤝 Contributing

We welcome contributions to SayDeck!

### � **How to Contribute:**

1. **Fork** the repository
2. Create a **feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit** your changes: `git commit -m 'Add amazing feature'`
4. **Push** to the branch: `git push origin feature/amazing-feature`
5. Open a **Pull Request**

### � **Bug Reports**

If you find a bug, please:
1. Check if there's already a similar issue
2. Create a new issue with detailed description
3. Include logs and screenshots

### 💡 **Feature Requests**

Have an idea for a new feature? Create an issue with the `enhancement` tag!

### 📋 **Development Guidelines**

- Follow PEP 8 style guide
- Write tests for new features
- Update documentation
- Use type hints
- Add docstrings

## � Performance

### ⚡ **Benchmarks**

- **AI Generation**: ~2-3 seconds (Groq AI)
- **Image Search**: ~1-2 seconds (Pexels API)
- **Database Operations**: <100ms (PostgreSQL)
- **Redis Operations**: <10ms
- **Concurrent Users**: 100+ (with proper scaling)

### 🔧 **Optimization Features**

- **Redis Caching** for guest credits
- **Async Processing** for all I/O operations
- **Connection Pooling** for PostgreSQL
- **Background Tasks** for image processing
- **Graceful Shutdown** for reliability

## 🔐 Security

- **JWT Authentication** with secure tokens
- **Password Hashing** with bcrypt
- **Rate Limiting** to prevent abuse
- **Input Validation** with Pydantic
- **CORS Configuration** for cross-origin requests
- **Environment Variables** for sensitive data

## 📈 Roadmap

### 🎯 **Upcoming Features**

- [ ] **PowerPoint Export** (.pptx format)
- [ ] **Real-time Collaboration** (WebSocket)
- [ ] **Advanced Templates** (industry-specific)
- [ ] **Presentation Analytics** (view tracking)
- [ ] **API Rate Limiting** (user-based)
- [ ] **Multi-language Support** (UI)
- [ ] **Mobile App** (React Native)

### � **Recent Updates**

- [x] **Enhanced Generation API** with CRUD operations
- [x] **Image Integration** via Pexels API
- [x] **Guest Credit System** with Redis
- [x] **Template Management** 
- [x] **Board Organization**
- [x] **Docker Support**
- [x] **Production Deployment**

## 🆘 Troubleshooting

### ❓ **Common Issues**

#### � **Database Connection Error**
```bash
# Check PostgreSQL status
docker-compose logs postgres

# Reset database
docker-compose down -v
docker-compose up -d
```

#### 🔴 **Redis Connection Error**
```bash
# Check Redis status
docker-compose logs redis

# Clear Redis cache
docker-compose exec redis redis-cli FLUSHALL
```

#### � **AI Generation Fails**
```bash
# Check Groq API key
echo $GROQ_API_KEY

# Test API connection
curl -H "Authorization: Bearer $GROQ_API_KEY" \
     https://api.groq.com/openai/v1/models
```

#### 🔴 **Image Service Error**
```bash
# Check Pexels API key
echo $PEXELS_API_KEY

# Test image search
curl -H "Authorization: $PEXELS_API_KEY" \
     "https://api.pexels.com/v1/search?query=business&per_page=1"
```

### � **Support**

- **GitHub Issues**: [Report a bug](https://github.com/chelobureck/SayDeck/issues)
- **Documentation**: [Complete API Guide](COMPLETE_API_GUIDE.md)
- **Quick Start**: [Frontend Guide](FRONTEND_QUICKSTART.md)

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## � Acknowledgments

- **[Groq](https://groq.com)** - Lightning-fast AI inference
- **[Pexels](https://pexels.com)** - High-quality stock photos
- **[FastAPI](https://fastapi.tiangolo.com)** - Modern Python web framework
- **[PostgreSQL](https://postgresql.org)** - Reliable database system
- **[Redis](https://redis.io)** - High-performance caching
- **[Docker](https://docker.com)** - Containerization platform

---

<div align="center">

**Made with ❤️ by the SayDeck Team**

[🌐 Website](https://saydeck.onrender.com) | [📧 Contact](mailto:adylbekoveldiyar2@gmail.com) | [🐙 GitHub](https://github.com/chelobureck/SayDeck)

</div>

---

<div align="center">

**Made with ❤️ by the SayDeck Team**

[🌐 Website](https://saydeck.onrender.com) | [� Contact](mailto:adylbekoveldiyar2@gmail.com) | [� GitHub](https://github.com/chelobureck/SayDeck)

</div>
