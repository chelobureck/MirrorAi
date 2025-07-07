# 📚 SayDeck API - Полное руководство для фронтенда

## 🎯 Общая информация

**Base URL**: `http://localhost:8000`  
**API Version**: v1  
**Префикс API**: `/api/v1`

SayDeck - это система для создания AI-презентаций с поддержкой изображений и шаблонов.

---

## 🔐 Аутентификация

### Получение токена
```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
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
Добавляйте заголовок ко всем защищенным запросам:
```http
Authorization: Bearer YOUR_ACCESS_TOKEN
```

---

## 🎨 Генерация презентаций

### 1. Базовая HTML презентация
```http
POST /api/v1/generate/
Authorization: Bearer YOUR_TOKEN
Content-Type: application/json

{
  "text": "Создай презентацию о машинном обучении"
}
```

**Ответ**: Готовый HTML для отображения в браузере

### 2. JSON презентация (для кастомной обработки)
```http
POST /api/v1/generate/json
Authorization: Bearer YOUR_TOKEN
Content-Type: application/json

{
  "text": "Создай презентацию о блокчейне"
}
```

**Ответ:**
```json
{
  "presentation_id": 123,
  "title": "Блокчейн технологии",
  "slides_count": 5,
  "content": {
    "title": "Блокчейн технологии",
    "slides": [
      {
        "title": "Введение в блокчейн",
        "content": "<p>Блокчейн - это...</p>",
        "type": "title"
      }
    ]
  },
  "created_at": "2025-07-07T12:00:00Z",
  "message": "Презентация успешно создана"
}
```

### 3. Расширенная генерация с изображениями ⭐
```http
POST /api/v1/enhanced/generate
Authorization: Bearer YOUR_TOKEN
Content-Type: application/json

{
  "topic": "Искусственный интеллект в медицине",
  "audience": "Врачи и медицинские работники",
  "style": "professional",
  "slides_count": 8,
  "language": "ru",
  "include_images": true,
  "image_style": "professional"
}
```

**Ответ:**
```json
{
  "presentation_id": 124,
  "title": "ИИ в медицине",
  "slides": [
    {
      "title": "Введение",
      "content": "<p>ИИ революционизирует медицину...</p>",
      "image": {
        "url": "https://images.pexels.com/photos/...",
        "alt": "Medical AI technology",
        "description": "AI technology in healthcare"
      }
    }
  ],
  "metadata": {
    "total_slides": 8,
    "images_added": 6,
    "generation_time": "3.2s"
  }
}
```

---

## 🖼️ Работа с изображениями

### Поиск изображений
```http
GET /api/v1/enhanced/search-images?query=artificial%20intelligence&count=5&style=professional
```

**Ответ:**
```json
{
  "images": [
    {
      "id": 123456,
      "url": "https://images.pexels.com/photos/123456/image.jpg",
      "alt": "Artificial Intelligence",
      "photographer": "John Smith",
      "width": 1920,
      "height": 1080
    }
  ],
  "query": "artificial intelligence",
  "count": 5,
  "total_found": 156
}
```

### Анализ контента для изображений
```http
POST /api/v1/enhanced/analyze-slide
Content-Type: application/json

{
  "content": "Машинное обучение в финансах помогает выявлять мошенничество"
}
```

**Ответ:**
```json
{
  "suggested_queries": [
    "machine learning finance",
    "fraud detection",
    "financial technology"
  ],
  "primary_query": "machine learning finance",
  "confidence": 0.85
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
      "created_at": "2025-07-07T12:00:00Z",
      "slides_count": 5,
      "has_images": true
    }
  ],
  "total": 15,
  "page": 1
}
```

### Получение конкретной презентации
```http
GET /api/v1/presentations/123
Authorization: Bearer YOUR_TOKEN
```

### Удаление презентации
```http
DELETE /api/v1/presentations/123
Authorization: Bearer YOUR_TOKEN
```

---

## 🎨 Система шаблонов (Публичные)

### Сохранить презентацию как шаблон
```http
POST /api/v1/templates/123/save
Authorization: Bearer YOUR_TOKEN
```

**Ответ:**
```json
{
  "templateId": "550e8400-e29b-41d4-a716-446655440000",
  "message": "Template created successfully"
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
    "createdAt": "2025-07-07T12:00:00Z"
  }
]
```

### Получить данные шаблона
```http
GET /api/v1/templates/550e8400-e29b-41d4-a716-446655440000
```

**Ответ:**
```json
{
  "templateId": "550e8400-e29b-41d4-a716-446655440000",
  "html": "<html>...полный HTML шаблона...</html>",
  "title": "Презентация о бизнесе"
}
```

### Просмотр шаблона (прямой HTML)
```http
GET /api/v1/templates/550e8400-e29b-41d4-a716-446655440000/viewer
```

**Ответ**: Прямой HTML контент для iframe или отдельной страницы

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
  "template_system": {
    "save_template": "/api/v1/templates/{presentation_id}/save (POST)",
    "get_template": "/api/v1/templates/{template_id} (GET)",
    "template_viewer": "/api/v1/templates/{template_id}/viewer (GET)"
  }
}
```

### Проверка расширенного сервиса
```http
GET /api/v1/enhanced/health
```

---

## 🎯 Примеры интеграции

### React/Next.js пример
```javascript
// Создание презентации с изображениями
const createPresentation = async (topic, audience) => {
  const response = await fetch('/api/v1/enhanced/generate', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${localStorage.getItem('token')}`
    },
    body: JSON.stringify({
      topic,
      audience,
      style: 'professional',
      include_images: true,
      slides_count: 6
    })
  });
  
  return await response.json();
};

// Отображение шаблона в iframe
const TemplateViewer = ({ templateId }) => (
  <iframe 
    src={`/api/v1/templates/${templateId}/viewer`}
    width="100%" 
    height="600px"
    frameBorder="0"
  />
);
```

### Vue.js пример
```javascript
// Композабл для работы с API
export const useSayDeckAPI = () => {
  const generatePresentation = async (data) => {
    const token = localStorage.getItem('authToken');
    
    const response = await $fetch('/api/v1/enhanced/generate', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`
      },
      body: data
    });
    
    return response;
  };
  
  return { generatePresentation };
};
```

---

## 🚨 Обработка ошибок

### Стандартные HTTP коды:
- **200**: Успех
- **400**: Неверный запрос  
- **401**: Не авторизован
- **404**: Не найдено
- **500**: Ошибка сервера

### Формат ошибок:
```json
{
  "detail": "Описание ошибки",
  "error_code": "VALIDATION_ERROR",
  "timestamp": "2025-07-07T12:00:00Z"
}
```

### Пример обработки:
```javascript
try {
  const response = await fetch('/api/v1/generate/', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ text: 'Topic' })
  });
  
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail);
  }
  
  const result = await response.json();
  // Обработка успешного результата
} catch (error) {
  console.error('Ошибка генерации:', error.message);
}
```

---

## 🔄 Rate Limiting

**Лимиты на пользователя:**
- Генерация HTML: 10 запросов/минуту
- Генерация JSON: 15 запросов/минуту  
- Поиск изображений: 30 запросов/минуту
- Шаблоны: без ограничений (публичные)

При превышении лимита API вернет `429 Too Many Requests`.

---

## 💡 Лучшие практики

### 1. Кэширование
- Кэшируйте результаты поиска изображений
- Сохраняйте токены в secure storage
- Используйте localStorage для временных данных

### 2. Оптимизация
- Группируйте запросы изображений
- Используйте debounce для поиска
- Показывайте прогресс загрузки

### 3. UX
- Показывайте превью перед генерацией
- Добавьте fallback для случаев без изображений  
- Используйте skeleton loading

### 4. Безопасность
- Всегда валидируйте токены
- Не храните токены в plain text
- Обновляйте токены при необходимости

---

## 🎉 Готово к использованию!

API полностью готов к интеграции. Все эндпоинты протестированы и работают стабильно.

**Поддержка**: Все вопросы по интеграции решайте с бэкенд-командой.

---

*Документация актуальна на: 07.07.2025*
