# 🚀 SayDeck API - Полное руководство для фронтенда (v2.0)

## 📋 Содержание
- [Общая информация](#общая-информация)
- [Быстрый старт](#быстрый-старт)
- [Аутентификация](#аутентификация)
- [Генерация презентаций](#генерация-презентаций)
- [Работа с изображениями](#работа-с-изображениями)
- [Система шаблонов](#система-шаблонов)
- [Управление презентациями](#управление-презентациями)
- [Примеры интеграции](#примеры-интеграции)
- [Обработка ошибок](#обработка-ошибок)
- [Best Practices](#best-practices)

---

## 🎯 Общая информация

**Base URL**: `http://localhost:8000`  
**API Version**: v1  
**Документация**: `http://localhost:8000/docs`  
**Статус**: `http://localhost:8000/api/v1/health`

### Основные возможности
- ✅ Генерация HTML презентаций из текста
- ✅ Поиск и вставка изображений (Pexels API)
- ✅ Система публичных шаблонов
- ✅ Пользовательские презентации
- ✅ Экспорт в различные форматы
- ✅ Rate Limiting и безопасность

---

## 🏃‍♂️ Быстрый старт

### 1. Проверка доступности
```bash
curl http://localhost:8000/api/v1/health
```

### 2. Создание простой презентации
```javascript
const response = await fetch('/api/v1/enhanced/generate', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    topic: "Искусственный интеллект",
    slides_count: 5,
    include_images: true
  })
});

const presentation = await response.json();
console.log(presentation);
```

---

## 🔐 Аутентификация

### Регистрация пользователя
```http
POST /api/v1/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepass123",
  "name": "John Doe"
}
```

**Ответ:**
```json
{
  "message": "User created successfully",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "name": "John Doe"
  }
}
```

### Вход в систему
```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepass123"
}
```

**Ответ:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "name": "John Doe"
  }
}
```

### Использование токена
```http
Authorization: Bearer YOUR_ACCESS_TOKEN
```

---

## 🎨 Генерация презентаций

### 1. Базовая HTML генерация
```http
POST /api/v1/generate/
Authorization: Bearer YOUR_TOKEN
Content-Type: application/json

{
  "text": "Создай презентацию о машинном обучении для студентов"
}
```

**Ответ**: Готовый HTML код презентации

### 2. JSON генерация (для кастомной обработки)
```http
POST /api/v1/generate/json
Authorization: Bearer YOUR_TOKEN
Content-Type: application/json

{
  "text": "Блокчейн технологии в финтехе",
  "slides_count": 6
}
```

**Ответ:**
```json
{
  "presentation_id": 123,
  "title": "Блокчейн в финтехе",
  "slides_count": 6,
  "content": {
    "title": "Блокчейн технологии в финтехе",
    "slides": [
      {
        "title": "Введение",
        "content": "<p>Блокчейн революционизирует финансы...</p>",
        "type": "title"
      }
    ]
  },
  "created_at": "2025-07-07T14:00:00Z"
}
```

### 3. 🌟 Расширенная генерация с изображениями
```http
POST /api/v1/enhanced/generate
Content-Type: application/json

{
  "topic": "Квантовые вычисления",
  "slides_count": 8,
  "audience": "разработчики",
  "style": "professional",
  "language": "ru",
  "include_images": true,
  "image_style": "professional",
  "auto_enhance": true
}
```

**Ответ:**
```json
{
  "title": "Квантовые вычисления",
  "slides": [
    {
      "title": "Введение в квантовые вычисления",
      "content": "Квантовые компьютеры используют принципы квантовой механики...",
      "image": {
        "id": 123456,
        "url": "https://images.pexels.com/photos/123456/quantum.jpg",
        "photographer": "Alex Smith",
        "width": 1920,
        "height": 1080,
        "alt": "Quantum computing visualization"
      },
      "layout": "title-content-image"
    }
  ],
  "total_slides": 8,
  "generation_time": 4.2,
  "images_found": 7
}
```

### Параметры запроса Enhanced Generate:

| Параметр | Тип | По умолчанию | Описание |
|----------|-----|-------------|----------|
| `topic` | string | **обязательный** | Основная тема презентации |
| `slides_count` | integer | 5 | Количество слайдов (1-20) |
| `audience` | string | "general" | Целевая аудитория |
| `style` | string | "professional" | Стиль: professional, creative, minimal |
| `language` | string | "ru" | Язык презентации |
| `include_images` | boolean | true | Включать ли поиск изображений |
| `image_style` | string | "professional" | Стиль изображений |
| `auto_enhance` | boolean | true | Автоматические улучшения |

---

## 🖼️ Работа с изображениями

### Поиск изображений
```http
GET /api/v1/enhanced/search-images?query=artificial%20intelligence&count=10&style=professional
```

**Ответ:**
```json
{
  "query": "artificial intelligence",
  "enhanced_query": "artificial intelligence business professional",
  "count": 10,
  "images": [
    {
      "id": 123456,
      "url": "https://images.pexels.com/photos/123456/ai.jpg",
      "original_url": "https://images.pexels.com/photos/123456/ai.jpg",
      "photographer": "Tech Studio",
      "photographer_url": "https://pexels.com/@tech-studio",
      "width": 1920,
      "height": 1080,
      "alt": "Artificial Intelligence"
    }
  ]
}
```

### Анализ контента для изображений
```http
POST /api/v1/enhanced/analyze-slide
Content-Type: application/json

{
  "content": "Машинное обучение в медицине помогает диагностировать заболевания"
}
```

**Ответ:**
```json
{
  "original_content": "Машинное обучение в медицине...",
  "extracted_keywords": ["machine learning", "medicine", "diagnosis"],
  "suggested_image": {
    "id": 789012,
    "url": "https://images.pexels.com/photos/789012/medical-ai.jpg",
    "alt": "Medical AI Technology"
  }
}
```

---

## 📁 Управление презентациями

### Список презентаций пользователя
```http
GET /api/v1/presentations/
Authorization: Bearer YOUR_TOKEN
```

**Ответ:**
```json
{
  "presentations": [
    {
      "id": 123,
      "title": "Машинное обучение",
      "created_at": "2025-07-07T14:00:00Z",
      "slides_count": 5,
      "has_images": true,
      "preview_url": "/api/v1/presentations/123/preview"
    }
  ],
  "total": 15,
  "page": 1,
  "pages": 2
}
```

### Получение презентации
```http
GET /api/v1/presentations/123
Authorization: Bearer YOUR_TOKEN
```

### Удаление презентации
```http
DELETE /api/v1/presentations/123
Authorization: Bearer YOUR_TOKEN
```

**Ответ:**
```json
{
  "message": "Presentation deleted successfully"
}
```

---

## 🎨 Система шаблонов

### Сохранить презентацию как публичный шаблон
```http
POST /api/v1/templates/123/save
Authorization: Bearer YOUR_TOKEN
```

**Ответ:**
```json
{
  "templateId": "550e8400-e29b-41d4-a716-446655440000",
  "message": "Template created successfully",
  "public_url": "/api/v1/templates/550e8400-e29b-41d4-a716-446655440000"
}
```

### Список всех публичных шаблонов
```http
GET /api/v1/templates
```

**Ответ:**
```json
[
  {
    "templateId": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Презентация о бизнесе",
    "createdAt": "2025-07-07T14:00:00Z",
    "author": "John Doe",
    "views": 152,
    "preview_url": "/api/v1/templates/550e8400-e29b-41d4-a716-446655440000/viewer"
  }
]
```

### Получить данные шаблона (JSON)
```http
GET /api/v1/templates/550e8400-e29b-41d4-a716-446655440000
```

**Ответ:**
```json
{
  "templateId": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Презентация о бизнесе",
  "html": "<html>...полный HTML шаблона...</html>",
  "slides": [
    {
      "title": "Заголовок",
      "content": "Содержимое слайда..."
    }
  ],
  "metadata": {
    "created_at": "2025-07-07T14:00:00Z",
    "author": "John Doe",
    "views": 152
  }
}
```

### Просмотр шаблона (HTML страница)
```http
GET /api/v1/templates/550e8400-e29b-41d4-a716-446655440000/viewer
```

**Ответ**: Готовая HTML страница для просмотра

### Удалить шаблон (только владелец)
```http
DELETE /api/v1/templates/550e8400-e29b-41d4-a716-446655440000
Authorization: Bearer YOUR_TOKEN
```

---

## 🛠️ Служебные эндпоинты

### Проверка здоровья API
```http
GET /api/v1/health
```

**Ответ:**
```json
{
  "status": "healthy",
  "message": "SayDeck API v1 - AI Презентации с системой шаблонов",
  "endpoints": {
    "generate_html": "/api/v1/generate/ (POST)",
    "enhanced_generate": "/api/v1/enhanced/generate (POST)",
    "templates": "/api/v1/templates"
  },
  "features": [
    "Создание HTML презентаций из текста (Groq/OpenAI)",
    "Автоматический поиск и вставка изображений (Pexels API)",
    "Система публичных шаблонов презентаций"
  ]
}
```

### Проверка Enhanced сервиса
```http
GET /api/v1/enhanced/health
```

**Ответ:**
```json
{
  "status": "healthy",
  "services": {
    "pexels_api": "ok",
    "ai_services": "ok"
  },
  "cache_size": 150,
  "version": "1.0.0"
}
```

---

## 💻 Примеры интеграции

### React/Next.js
```javascript
// hooks/useSayDeck.js
import { useState, useCallback } from 'react';

export const useSayDeck = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const generatePresentation = useCallback(async (data) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch('/api/v1/enhanced/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify(data)
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Ошибка генерации');
      }

      const result = await response.json();
      return result;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const searchImages = useCallback(async (query, style = 'professional') => {
    try {
      const response = await fetch(
        `/api/v1/enhanced/search-images?query=${encodeURIComponent(query)}&style=${style}`
      );
      
      if (!response.ok) throw new Error('Ошибка поиска изображений');
      
      return await response.json();
    } catch (err) {
      setError(err.message);
      throw err;
    }
  }, []);

  return {
    generatePresentation,
    searchImages,
    loading,
    error
  };
};

// components/PresentationForm.jsx
import React, { useState } from 'react';
import { useSayDeck } from '../hooks/useSayDeck';

export const PresentationForm = () => {
  const { generatePresentation, loading, error } = useSayDeck();
  const [formData, setFormData] = useState({
    topic: '',
    slides_count: 5,
    audience: 'general',
    style: 'professional',
    include_images: true
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      const result = await generatePresentation(formData);
      console.log('Презентация создана:', result);
      // Обработка результата...
    } catch (err) {
      console.error('Ошибка:', err);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="presentation-form">
      <div className="form-group">
        <label htmlFor="topic">Тема презентации:</label>
        <input
          id="topic"
          type="text"
          value={formData.topic}
          onChange={(e) => setFormData({...formData, topic: e.target.value})}
          required
          placeholder="Например: Искусственный интеллект"
        />
      </div>

      <div className="form-group">
        <label htmlFor="slides_count">Количество слайдов:</label>
        <select
          id="slides_count"
          value={formData.slides_count}
          onChange={(e) => setFormData({...formData, slides_count: parseInt(e.target.value)})}
        >
          {[3,4,5,6,7,8,9,10].map(num => (
            <option key={num} value={num}>{num}</option>
          ))}
        </select>
      </div>

      <div className="form-group">
        <label htmlFor="audience">Аудитория:</label>
        <select
          id="audience"
          value={formData.audience}
          onChange={(e) => setFormData({...formData, audience: e.target.value})}
        >
          <option value="general">Общая</option>
          <option value="students">Студенты</option>
          <option value="professionals">Профессионалы</option>
          <option value="executives">Руководители</option>
        </select>
      </div>

      <div className="form-group">
        <label>
          <input
            type="checkbox"
            checked={formData.include_images}
            onChange={(e) => setFormData({...formData, include_images: e.target.checked})}
          />
          Включить изображения
        </label>
      </div>

      <button type="submit" disabled={loading} className="submit-btn">
        {loading ? 'Создание...' : 'Создать презентацию'}
      </button>

      {error && <div className="error-message">{error}</div>}
    </form>
  );
};

// components/TemplateViewer.jsx
export const TemplateViewer = ({ templateId, className }) => (
  <iframe 
    src={`/api/v1/templates/${templateId}/viewer`}
    className={`template-viewer ${className}`}
    width="100%" 
    height="600px"
    frameBorder="0"
    title="Template Preview"
  />
);
```

### Vue.js 3 Composition API
```javascript
// composables/useSayDeck.js
import { ref, reactive } from 'vue';

export function useSayDeck() {
  const loading = ref(false);
  const error = ref(null);

  const generatePresentation = async (data) => {
    loading.value = true;
    error.value = null;

    try {
      const response = await $fetch('/api/v1/enhanced/generate', {
        method: 'POST',
        body: data,
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('authToken')}`
        }
      });

      return response;
    } catch (err) {
      error.value = err.data?.detail || err.message;
      throw err;
    } finally {
      loading.value = false;
    }
  };

  const getTemplates = async () => {
    try {
      return await $fetch('/api/v1/templates');
    } catch (err) {
      error.value = err.data?.detail || err.message;
      throw err;
    }
  };

  return {
    generatePresentation,
    getTemplates,
    loading: readonly(loading),
    error: readonly(error)
  };
}

// components/PresentationGenerator.vue
<template>
  <div class="presentation-generator">
    <form @submit.prevent="handleSubmit" class="form">
      <div class="field">
        <label for="topic">Тема:</label>
        <input 
          id="topic"
          v-model="form.topic" 
          type="text" 
          required 
          placeholder="Введите тему презентации"
        />
      </div>

      <div class="field">
        <label for="slides">Слайдов:</label>
        <select id="slides" v-model="form.slides_count">
          <option v-for="n in 8" :key="n+2" :value="n+2">{{ n+2 }}</option>
        </select>
      </div>

      <div class="field">
        <label>
          <input type="checkbox" v-model="form.include_images" />
          Включить изображения
        </label>
      </div>

      <button type="submit" :disabled="loading" class="btn-primary">
        {{ loading ? 'Создание...' : 'Создать' }}
      </button>
    </form>

    <div v-if="error" class="error">{{ error }}</div>

    <div v-if="result" class="result">
      <h3>{{ result.title }}</h3>
      <p>Создано {{ result.total_slides }} слайдов</p>
      <p v-if="result.images_found">Найдено {{ result.images_found }} изображений</p>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue';
import { useSayDeck } from '../composables/useSayDeck';

const { generatePresentation, loading, error } = useSayDeck();

const form = reactive({
  topic: '',
  slides_count: 5,
  audience: 'general',
  style: 'professional',
  include_images: true
});

const result = ref(null);

const handleSubmit = async () => {
  try {
    result.value = await generatePresentation(form);
  } catch (err) {
    console.error('Ошибка создания презентации:', err);
  }
};
</script>
```

### Vanilla JavaScript / jQuery
```javascript
// utils/saydeck-api.js
class SayDeckAPI {
  constructor(baseURL = 'http://localhost:8000', token = null) {
    this.baseURL = baseURL;
    this.token = token;
  }

  setToken(token) {
    this.token = token;
    localStorage.setItem('saydeck_token', token);
  }

  getHeaders() {
    const headers = {
      'Content-Type': 'application/json'
    };
    
    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`;
    }
    
    return headers;
  }

  async generatePresentation(data) {
    const response = await fetch(`${this.baseURL}/api/v1/enhanced/generate`, {
      method: 'POST',
      headers: this.getHeaders(),
      body: JSON.stringify(data)
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Ошибка генерации');
    }

    return await response.json();
  }

  async getTemplates() {
    const response = await fetch(`${this.baseURL}/api/v1/templates`, {
      headers: this.getHeaders()
    });

    if (!response.ok) {
      throw new Error('Ошибка получения шаблонов');
    }

    return await response.json();
  }

  async searchImages(query, style = 'professional') {
    const url = `${this.baseURL}/api/v1/enhanced/search-images?query=${encodeURIComponent(query)}&style=${style}`;
    
    const response = await fetch(url, {
      headers: this.getHeaders()
    });

    if (!response.ok) {
      throw new Error('Ошибка поиска изображений');
    }

    return await response.json();
  }
}

// Использование
const api = new SayDeckAPI();

// Генерация презентации
document.getElementById('generate-btn').addEventListener('click', async () => {
  const topic = document.getElementById('topic').value;
  const slidesCount = parseInt(document.getElementById('slides').value);
  
  try {
    const result = await api.generatePresentation({
      topic: topic,
      slides_count: slidesCount,
      include_images: true,
      style: 'professional'
    });
    
    console.log('Презентация создана:', result);
    displayPresentation(result);
  } catch (error) {
    alert('Ошибка: ' + error.message);
  }
});

function displayPresentation(presentation) {
  const container = document.getElementById('presentation-container');
  
  let html = `<h2>${presentation.title}</h2>`;
  
  presentation.slides.forEach((slide, index) => {
    html += `
      <div class="slide">
        <h3>${index + 1}. ${slide.title}</h3>
        <div class="content">${slide.content}</div>
        ${slide.image ? `<img src="${slide.image.url}" alt="${slide.image.alt}" />` : ''}
      </div>
    `;
  });
  
  container.innerHTML = html;
}
```

---

## 🚨 Обработка ошибок

### Стандартные HTTP коды:
- **200** - Успех
- **400** - Неверный запрос (валидация)
- **401** - Не авторизован  
- **403** - Доступ запрещен
- **404** - Ресурс не найден
- **429** - Превышен лимит запросов
- **500** - Внутренняя ошибка сервера

### Формат ошибок:
```json
{
  "detail": "Описание ошибки",
  "error_code": "VALIDATION_ERROR",
  "timestamp": "2025-07-07T14:00:00Z",
  "path": "/api/v1/enhanced/generate"
}
```

### Примеры ошибок:

**400 - Валидация:**
```json
{
  "detail": "Topic is required and must be at least 3 characters long",
  "error_code": "VALIDATION_ERROR"
}
```

**401 - Авторизация:**
```json
{
  "detail": "Could not validate credentials",
  "error_code": "AUTHENTICATION_ERROR"
}
```

**429 - Rate Limit:**
```json
{
  "detail": "Rate limit exceeded. Try again in 60 seconds",
  "error_code": "RATE_LIMIT_EXCEEDED",
  "retry_after": 60
}
```

**500 - Сервер:**
```json
{
  "detail": "AI service temporarily unavailable",
  "error_code": "AI_SERVICE_ERROR",
  "fallback_available": true
}
```

### Рекомендуемая обработка:
```javascript
async function handleAPICall(apiCall) {
  try {
    const result = await apiCall();
    return { success: true, data: result };
  } catch (error) {
    if (error instanceof TypeError) {
      // Проблемы с сетью
      return { 
        success: false, 
        error: 'Проблемы с подключением к серверу' 
      };
    }

    const status = error.status || error.response?.status;
    
    switch (status) {
      case 400:
        return { 
          success: false, 
          error: 'Проверьте корректность данных', 
          details: error.message 
        };
      
      case 401:
        // Перенаправление на логин
        localStorage.removeItem('token');
        window.location.href = '/login';
        return { success: false, error: 'Требуется авторизация' };
      
      case 429:
        return { 
          success: false, 
          error: 'Слишком много запросов. Попробуйте позже', 
          retryAfter: error.retry_after 
        };
      
      case 500:
        return { 
          success: false, 
          error: 'Ошибка сервера. Мы работаем над исправлением' 
        };
      
      default:
        return { 
          success: false, 
          error: error.message || 'Неизвестная ошибка' 
        };
    }
  }
}

// Использование
const result = await handleAPICall(() => 
  api.generatePresentation({ topic: 'AI', slides_count: 5 })
);

if (result.success) {
  console.log('Успех:', result.data);
} else {
  console.error('Ошибка:', result.error);
  showUserError(result.error);
}
```

---

## 🔄 Rate Limiting

### Лимиты по эндпоинтам:
- **Генерация HTML**: 10 запросов/минуту на пользователя
- **Генерация Enhanced**: 5 запросов/минуту на пользователя  
- **Поиск изображений**: 30 запросов/минуту на пользователя
- **Публичные шаблоны**: Без ограничений
- **Авторизация**: 5 попыток/минуту на IP

### Заголовки ответа:
```http
X-RateLimit-Limit: 10
X-RateLimit-Remaining: 7
X-RateLimit-Reset: 1625657400
```

---

## 💡 Best Practices

### 1. Оптимизация производительности
```javascript
// Debounce для поиска
const debouncedSearch = debounce(async (query) => {
  const images = await api.searchImages(query);
  updateImageResults(images);
}, 300);

// Кэширование результатов
const cache = new Map();

async function getCachedTemplates() {
  if (cache.has('templates')) {
    return cache.get('templates');
  }
  
  const templates = await api.getTemplates();
  cache.set('templates', templates);
  
  // Очистка кэша через 5 минут
  setTimeout(() => cache.delete('templates'), 5 * 60 * 1000);
  
  return templates;
}

// Lazy loading для изображений
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const img = entry.target;
      img.src = img.dataset.src;
      observer.unobserve(img);
    }
  });
});

document.querySelectorAll('img[data-src]').forEach(img => {
  observer.observe(img);
});
```

### 2. UX улучшения
```javascript
// Показ прогресса генерации
async function generateWithProgress(data) {
  const progressBar = document.getElementById('progress');
  const statusText = document.getElementById('status');
  
  progressBar.style.width = '10%';
  statusText.textContent = 'Генерация контента...';
  
  try {
    const result = await api.generatePresentation(data);
    
    progressBar.style.width = '100%';
    statusText.textContent = 'Готово!';
    
    return result;
  } catch (error) {
    progressBar.style.width = '0%';
    statusText.textContent = 'Ошибка генерации';
    throw error;
  }
}

// Skeleton loading
function showSkeleton() {
  return `
    <div class="skeleton-slide">
      <div class="skeleton-title"></div>
      <div class="skeleton-content"></div>
      <div class="skeleton-image"></div>
    </div>
  `;
}

// Auto-save черновиков
let autoSaveTimeout;

function autoSaveDraft(formData) {
  clearTimeout(autoSaveTimeout);
  
  autoSaveTimeout = setTimeout(() => {
    localStorage.setItem('presentation_draft', JSON.stringify(formData));
    showAutoSaveIndicator();
  }, 2000);
}

// Восстановление черновика
function restoreDraft() {
  const draft = localStorage.getItem('presentation_draft');
  if (draft) {
    return JSON.parse(draft);
  }
  return null;
}
```

### 3. Безопасность
```javascript
// Валидация на клиенте
function validatePresentationData(data) {
  const errors = [];
  
  if (!data.topic || data.topic.length < 3) {
    errors.push('Тема должна содержать минимум 3 символа');
  }
  
  if (data.slides_count < 1 || data.slides_count > 20) {
    errors.push('Количество слайдов: от 1 до 20');
  }
  
  if (!['professional', 'creative', 'minimal'].includes(data.style)) {
    errors.push('Недопустимый стиль');
  }
  
  return errors;
}

// Sanitization HTML контента
function sanitizeHTML(html) {
  const temp = document.createElement('div');
  temp.textContent = html;
  return temp.innerHTML;
}

// Безопасное хранение токенов
class SecureStorage {
  static setToken(token) {
    if (typeof token !== 'string') {
      throw new Error('Token must be a string');
    }
    
    // В production используйте httpOnly cookies
    sessionStorage.setItem('auth_token', token);
  }
  
  static getToken() {
    return sessionStorage.getItem('auth_token');
  }
  
  static clearToken() {
    sessionStorage.removeItem('auth_token');
    localStorage.removeItem('user_data');
  }
}
```

### 4. Адаптивность и доступность
```css
/* Responsive дизайн */
.presentation-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 1rem;
}

@media (max-width: 768px) {
  .presentation-container {
    padding: 0.5rem;
  }
  
  .slide {
    margin: 1rem 0;
    padding: 1rem;
  }
  
  .slide img {
    max-width: 100%;
    height: auto;
  }
}

/* Accessibility */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

/* Focus states */
.btn:focus,
input:focus,
select:focus {
  outline: 2px solid #4A90E2;
  outline-offset: 2px;
}
```

```javascript
// Поддержка клавиатуры
document.addEventListener('keydown', (e) => {
  if (e.ctrlKey || e.metaKey) {
    switch (e.key) {
      case 's':
        e.preventDefault();
        saveDraft();
        break;
      case 'Enter':
        if (e.target.matches('.topic-input')) {
          e.preventDefault();
          generatePresentation();
        }
        break;
    }
  }
});

// Aria-live для уведомлений
function announceToScreenReader(message) {
  const announcer = document.getElementById('screen-reader-announcer');
  announcer.textContent = message;
}
```

---

## 🔧 Настройка окружения

### Environment Variables (.env)
```bash
# API Configuration
SECRET_KEY=your-super-secret-key-change-this-in-production
PROJECT_NAME=SayDeck
VERSION=1.0.0

# Database
USE_POSTGRES=false  # true для production
POSTGRES_USER=say_deck_user
POSTGRES_PASSWORD=saydeck123
POSTGRES_DB=say_deck
POSTGRES_SERVER=localhost
POSTGRES_PORT=5432

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379

# AI Services
GROQ_API_KEY=your_groq_api_key_here
OPENAI_API_KEY=your_openai_key

# Image Services
PEXELS_API_KEY=your_pexels_api_key_here

# Email (optional)
GMAIL_USER=your_email@gmail.com
GMAIL_APP_PASSWORD=your_app_password
```

### Docker Setup
```bash
# Запуск всех сервисов
docker-compose up -d

# Только база данных
docker-compose up -d db redis

# Просмотр логов
docker-compose logs -f web

# Остановка
docker-compose down
```

### Local Development
```bash
# Установка зависимостей
pip install -r requirements.txt

# Запуск сервера
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Или через скрипт
python run_server.py
```

---

## 📊 Мониторинг и метрики

### Health Check Endpoints
```javascript
// Полная проверка системы
async function checkSystemHealth() {
  const checks = await Promise.allSettled([
    fetch('/api/v1/health'),
    fetch('/api/v1/enhanced/health'),
    fetch('/api/v1/templates')
  ]);
  
  return {
    api: checks[0].status === 'fulfilled' && checks[0].value.ok,
    enhanced: checks[1].status === 'fulfilled' && checks[1].value.ok,
    templates: checks[2].status === 'fulfilled' && checks[2].value.ok
  };
}

// Мониторинг производительности
class PerformanceMonitor {
  static startTimer(operation) {
    return {
      operation,
      startTime: performance.now()
    };
  }
  
  static endTimer(timer) {
    const duration = performance.now() - timer.startTime;
    console.log(`${timer.operation}: ${duration.toFixed(2)}ms`);
    
    // Отправка метрик (опционально)
    if (duration > 5000) {
      console.warn(`Slow operation detected: ${timer.operation}`);
    }
    
    return duration;
  }
}

// Использование
const timer = PerformanceMonitor.startTimer('Generate Presentation');
const result = await api.generatePresentation(data);
PerformanceMonitor.endTimer(timer);
```

---

## 🎉 Готово к использованию!

SayDeck API предоставляет мощные возможности для создания AI-презентаций с изображениями. Все эндпоинты протестированы и готовы для интеграции.

### Быстрые ссылки:
- **API Документация**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/v1/health
- **Примеры шаблонов**: http://localhost:8000/api/v1/templates

### Поддержка:
- 📧 Email: tech@saydeck.ai
- 💬 Slack: #saydeck-api
- 📖 Wiki: [Internal Documentation]

---

**Документация актуальна на**: 07 июля 2025  
**Версия API**: 1.0.0  
**Последнее обновление**: Исправлены ошибки enhanced generator, добавлена fallback логика
