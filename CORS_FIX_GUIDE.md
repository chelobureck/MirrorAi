# 🚀 Решение проблемы CORS и 500 ошибки

## 🐛 Найденные проблемы:

### 1. CORS Error
```
Access to XMLHttpRequest at 'https://saydeck.onrender.com/api/v1/boards/' 
from origin 'http://localhost:5173' has been blocked by CORS policy
```

**Причина**: Фронтенд на `localhost:5173` (Vite) пытается обратиться к production API, но CORS не настроен.

### 2. 500 Internal Server Error
```
POST https://saydeck.onrender.com/api/v1/boards/ net::ERR_FAILED 500
```

**Причина**: Ошибка на сервере при создании board.

---

## ✅ Исправления:

### 1. Обновлены CORS настройки
```javascript
// В main.py добавлено:
allow_origins=["*"],  // Разрешены все источники
allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
expose_headers=["*"],
```

### 2. Улучшена обработка ошибок в /boards
- Добавлено логирование
- Добавлен try/catch блок
- Добавлен rollback при ошибках
- Добавлен health check эндпоинт

### 3. Добавлен health check
```http
GET /api/v1/boards/health
```

---

## 🔧 Как исправить на Render.com:

### 1. Обновить код на GitHub
```bash
git add .
git commit -m "Fix CORS and boards 500 error - Add better error handling and logging"
git push origin main
```

### 2. Настроить Environment Variables на Render.com
```
SECRET_KEY=super-secure-production-key-saydeck-2025
USE_POSTGRES=true
POSTGRES_USER=your_render_postgres_user
POSTGRES_PASSWORD=your_render_postgres_password
POSTGRES_DB=your_render_postgres_db
POSTGRES_SERVER=your_render_postgres_host
POSTGRES_PORT=5432
REDIS_HOST=your_render_redis_host  
REDIS_PORT=6379
GROQ_API_KEY=your_groq_api_key
PEXELS_API_KEY=D4T0gagPy0PjrUCuqTIX3HkPBB2e3iFwELxxF9HjHRCaZ3GgSHQvPTnh
```

### 3. Проверить после deploy
```http
# Health check
GET https://saydeck.onrender.com/api/v1/health
GET https://saydeck.onrender.com/api/v1/boards/health

# Тест CORS (из браузера на localhost:5173)
fetch('https://saydeck.onrender.com/api/v1/boards/health')
  .then(r => r.json())
  .then(console.log)
```

---

## 🧪 Тестирование фронтенда:

### Обновите URL в фронтенде:
```javascript
// Вместо локального API используйте:
const API_BASE_URL = 'https://saydeck.onrender.com';

// Пример запроса:
const createBoard = async (boardData) => {
  const response = await fetch(`${API_BASE_URL}/api/v1/boards/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify(boardData)
  });
  
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to create board');
  }
  
  return response.json();
};
```

---

## 🔍 Диагностика:

### Если проблема остается:

1. **Проверить логи на Render.com**
2. **Проверить health endpoints**:
   - https://saydeck.onrender.com/api/v1/health
   - https://saydeck.onrender.com/api/v1/boards/health

3. **Проверить CORS в браузере**:
```javascript
// Откройте консоль на localhost:5173 и выполните:
fetch('https://saydeck.onrender.com/api/v1/health')
  .then(r => r.text())
  .then(console.log)
  .catch(console.error)
```

4. **Проверить Network tab** в DevTools при запросе

---

## 🚀 После исправления фронтенд должен работать!

Код исправлен и готов к deploy. Проблемы с CORS и 500 ошибкой должны быть решены.
