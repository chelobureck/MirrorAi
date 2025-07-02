# SayDeck API 🎯

> AI-Powered Presentation Generator with Multiple AI Providers

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg?style=for-the-badge&logo=python)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![PostgreSQL](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)

## 🚀 Quick Start

### Option 1: Docker Compose (Recommended)
```bash
# Clone repository
git clone <repository-url>
cd SayDeck

# Start all services
docker compose up -d

# Check status
docker compose ps
```

### Option 2: Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Start external services
docker compose up -d db redis

# Run API server
uvicorn main:app --reload
```

## 🌐 API Endpoints

- **Swagger UI**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/v1/health
- **AI Providers**: http://localhost:8000/api/v1/generate/providers

## 🧠 AI Providers

| Provider | Status | Models | Features |
|----------|--------|--------|----------|
| **Groq** | ✅ Active | Llama 3.1 70B/8B | Fast, Free tier |
| **OpenAI** | 🔑 API Key needed | GPT-4, GPT-3.5 | High quality |
| **Ollama** | 🏠 Local setup | Llama 3.1 8B | Private, Offline |

## 🧪 Test AI Generation

```bash
# Test Groq provider
curl -X POST "http://localhost:8000/api/v1/generate/test/groq" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Create a presentation about AI in healthcare"}'

# Test all providers
curl -X POST "http://localhost:8000/api/v1/generate/test/all" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Explain blockchain technology"}'
```

## ⚙️ Configuration

Copy `.env.example` to `.env` and configure:

```bash
# AI Providers
GROQ_API_KEY=your_groq_api_key
OPENAI_API_KEY=your_openai_api_key  # Optional

# Database
POSTGRES_USER=say_deck_user
POSTGRES_PASSWORD=your_password
POSTGRES_DB=say_deck
POSTGRES_SERVER=localhost  # or 'db' for Docker

# Redis
REDIS_HOST=localhost  # or 'redis' for Docker
REDIS_PORT=6379

# Security
SECRET_KEY=your-secret-key
```

## 📚 Documentation

- 📖 **[Complete Project Guide](PROJECT_GUIDE.md)** - Detailed explanation of every file
- 🌐 **[API Documentation](http://localhost:8000/docs)** - Interactive Swagger UI
- 🐳 **[Docker Setup](docker-compose.yml)** - Container orchestration

## 🏗️ Architecture

```
FastAPI Backend
├── 🧠 AI Services (Groq, OpenAI, Ollama)
├── 🗄️ PostgreSQL Database  
├── ⚡ Redis Cache
├── 🔐 JWT Authentication
└── 📊 RESTful API
```

## 🛠️ Tech Stack

- **Backend**: FastAPI + Python 3.11
- **Database**: PostgreSQL 17 + SQLAlchemy (async)
- **Cache**: Redis 7
- **AI**: Groq, OpenAI, Ollama APIs
- **Container**: Docker + Docker Compose
- **Auth**: JWT tokens
- **Validation**: Pydantic v2

## 📄 License

This project is licensed under the MIT License.

---

**Ready for hackathon presentation! 🎯**
