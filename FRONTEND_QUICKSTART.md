# 🎯 SayDeck API - Quick Start для фронтенда

## 📋 Краткая справка

**API Base URL**: `http://localhost:8000`  
**Документация**: `http://localhost:8000/docs`  
**Полное руководство**: `COMPLETE_API_GUIDE.md`

---

## 🚀 Основные эндпоинты для фронта

### 1. Создание презентации с изображениями (ОСНОВНОЙ)
```http
POST /api/v1/enhanced/generate
Content-Type: application/json

{
  "topic": "Искусственный интеллект",
  "slides_count": 5,
  "audience": "студенты", 
  "include_images": true,
  "style": "professional"
}
```

### 2. Простая HTML презентация
```http
POST /api/v1/generate/
Authorization: Bearer TOKEN
Content-Type: application/json

{
  "text": "Создай презентацию о блокчейне"
}
```

### 3. Публичные шаблоны
```http
GET /api/v1/templates                    # Список шаблонов
GET /api/v1/templates/{id}               # Данные шаблона  
GET /api/v1/templates/{id}/viewer        # HTML просмотр
```

### 4. Поиск изображений
```http
GET /api/v1/enhanced/search-images?query=AI&style=professional
```

---

## ⚡ Быстрая интеграция

### JavaScript
```javascript
// Создание презентации
const response = await fetch('/api/v1/enhanced/generate', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    topic: "Тема презентации",
    slides_count: 5,
    include_images: true
  })
});

const presentation = await response.json();
console.log(presentation.slides); // Массив слайдов с изображениями
```

### React
```jsx
const [presentation, setPresentation] = useState(null);

const generatePresentation = async (topic) => {
  const response = await fetch('/api/v1/enhanced/generate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ 
      topic, 
      slides_count: 5,
      include_images: true 
    })
  });
  
  const result = await response.json();
  setPresentation(result);
};
```

---

## 🛠️ Структура ответа

### Enhanced Generate Response:
```json
{
  "title": "Название презентации",
  "slides": [
    {
      "title": "Заголовок слайда",
      "content": "Текст слайда",
      "image": {
        "url": "https://images.pexels.com/...",
        "alt": "Описание изображения",
        "photographer": "Автор"
      },
      "layout": "title-content-image"
    }
  ],
  "total_slides": 5,
  "generation_time": 3.2,
  "images_found": 4
}
```

---

## 🚨 Обработка ошибок

```javascript
try {
  const response = await fetch('/api/v1/enhanced/generate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail);
  }

  const result = await response.json();
  return result;
} catch (error) {
  console.error('Ошибка:', error.message);
  // Показать пользователю ошибку
}
```

---

## 📱 Примеры UI компонентов

### Форма создания
```jsx
function PresentationForm() {
  const [topic, setTopic] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      const result = await generatePresentation({
        topic,
        slides_count: 5,
        include_images: true
      });
      
      onPresentationCreated(result);
    } catch (error) {
      alert('Ошибка: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input 
        value={topic}
        onChange={(e) => setTopic(e.target.value)}
        placeholder="Тема презентации"
        required
      />
      <button type="submit" disabled={loading}>
        {loading ? 'Создание...' : 'Создать'}
      </button>
    </form>
  );
}
```

### Отображение слайдов
```jsx
function SlideViewer({ slides }) {
  return (
    <div className="slides-container">
      {slides.map((slide, index) => (
        <div key={index} className="slide">
          <h2>{slide.title}</h2>
          <div className="content">{slide.content}</div>
          {slide.image && (
            <img 
              src={slide.image.url} 
              alt={slide.image.alt}
              className="slide-image"
            />
          )}
        </div>
      ))}
    </div>
  );
}
```

---

## 🎨 CSS стили

```css
.slide {
  background: white;
  padding: 2rem;
  margin: 1rem 0;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.slide h2 {
  color: #333;
  margin-bottom: 1rem;
  border-bottom: 2px solid #4A90E2;
  padding-bottom: 0.5rem;
}

.slide-image {
  max-width: 100%;
  height: auto;
  border-radius: 4px;
  margin-top: 1rem;
}
```

---

## 📞 Нужна помощь?

1. **Полная документация**: `COMPLETE_API_GUIDE.md`
2. **API документация**: http://localhost:8000/docs  
3. **Health check**: http://localhost:8000/api/v1/health

**Основные проблемы и решения:**
- Ошибка 500 → Проверить запрос в `COMPLETE_API_GUIDE.md`
- Нет изображений → Проверить Pexels API ключ
- Медленно → Использовать `auto_enhance: false`

---

*Создано для команды фронтенда SayDeck • 07.07.2025*
