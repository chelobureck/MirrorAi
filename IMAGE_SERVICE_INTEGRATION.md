# 🖼️ SayDeck Image Service Integration Guide

<div align="center">

**🤝 Руководство интеграции микросервиса поиска изображений**

*Документация для интеграции Pexels Image Service в ваш проект*

</div>

---

## 📋 Обзор

Новый **Image Service** добавляет в SayDeck возможность автоматического поиска и вставки изображений в презентации через **Pexels API**. Сервис полностью асинхронный, с кэшированием и обработкой ошибок.

## 🏗️ Архитектура

```
ai_services/
├── image_service.py          # Основной сервис поиска изображений
└── manager.py               # AI менеджер (существующий)

routers/
├── enhanced_generator.py    # Новый роутер с изображениями
├── html_generator.py        # Оригинальный генератор (без изменений)
└── ...

config/
└── settings.py             # Добавлен PEXELS_API_KEY
```

## 🔧 Настройка

### 1. Переменные окружения

Добавлено в `.env`:
```env
# Image Search API Keys  
PEXELS_API_KEY=D4T0gagPy0PjrUCuqTIX3HkPBB2e3iFwELxxF9HjHRCaZ3GgSHQvPTnh
```

### 2. Зависимости

Добавлено в `requirements.txt`:
```txt
aiohttp>=3.9.0
```

## 🚀 API Endpoints

### Enhanced Generation

**POST** `/api/v1/enhanced/generate`

Создает презентацию с автоматическим поиском изображений:

```json
{
  "topic": "Machine Learning в бизнесе",
  "slides_count": 5,
  "audience": "business",
  "style": "professional", 
  "language": "ru",
  "include_images": true,
  "image_style": "professional",
  "auto_enhance": true
}
```

**Response:**
```json
{
  "title": "Machine Learning в бизнесе",
  "slides": [
    {
      "title": "Введение в ML",
      "content": "Содержимое слайда...",
      "image": {
        "id": 123456,
        "url": "https://images.pexels.com/...",
        "photographer": "John Doe",
        "alt": "Machine learning concept"
      },
      "layout": "title-content-image"
    }
  ],
  "total_slides": 5,
  "generation_time": 2.34,
  "images_found": 4
}
```

### Image Search

**GET** `/api/v1/enhanced/search-images`

Поиск изображений по запросу:

```
GET /api/v1/enhanced/search-images?query=artificial%20intelligence&count=10&style=professional
```

### Slide Analysis

**POST** `/api/v1/enhanced/analyze-slide`

Анализ содержимого слайда для подбора изображения:

```json
"Machine Learning алгоритмы для обработки больших данных"
```

### Health Check

**GET** `/api/v1/enhanced/health`

Проверка статуса сервисов:

```json
{
  "status": "healthy",
  "services": {
    "pexels_api": "ok",
    "ai_services": "ok"
  },
  "cache_size": 15
}
```

## 💻 Использование в коде

### 1. Прямое использование Image Service

```python
from ai_services.image_service import image_service

async def example_usage():
    async with image_service as service:
        # Поиск изображений
        images = await service.search_images("python programming", per_page=5)
        
        # Поиск для слайда
        slide_text = "Основы машинного обучения"
        image = await service.search_for_slide_content(slide_text)
        
        return images, image
```

### 2. Использование утилитарных функций

```python
from ai_services.image_service import search_images, get_image_for_slide

async def quick_example():
    # Быстрый поиск
    images = await search_images("business meeting", 3)
    
    # Поиск для слайда
    image = await get_image_for_slide("Презентация продукта клиентам")
    
    return images, image
```

## 🔄 Интеграция с вашим кодом

### Если у вас есть HTML генерация:

```python
async def enhance_html_with_images(html_content: str, topic: str):
    """Добавление изображений в существующий HTML"""
    from ai_services.image_service import get_image_for_slide
    
    # Поиск изображения для темы
    image = await get_image_for_slide(topic)
    
    if image:
        # Вставка изображения в HTML
        image_html = f'''
        <div class="slide-image">
            <img src="{image['url']}" alt="{image['alt']}" />
            <p class="image-credit">Фото: {image['photographer']}</p>
        </div>
        '''
        
        # Замена плейсхолдера или добавление в конец
        enhanced_html = html_content.replace(
            "{IMAGE_PLACEHOLDER}", 
            image_html
        )
        
        return enhanced_html
    
    return html_content
```

### Если у вас есть шаблоны слайдов:

```python
async def process_slide_template(slide_data: dict):
    """Обработка шаблона слайда с добавлением изображения"""
    from ai_services.image_service import get_image_for_slide
    
    # Извлекаем контент для поиска изображения
    search_content = f"{slide_data.get('title', '')} {slide_data.get('content', '')}"
    
    # Ищем изображение
    image = await get_image_for_slide(search_content)
    
    # Добавляем в данные слайда
    if image:
        slide_data['image'] = image
        slide_data['has_image'] = True
    else:
        slide_data['has_image'] = False
    
    return slide_data
```

## 🎯 Примеры шаблонов HTML

### Слайд с изображением

```html
<div class="slide">
    <h1>{{ slide.title }}</h1>
    
    {% if slide.image %}
    <div class="slide-content-with-image">
        <div class="text-content">
            {{ slide.content }}
        </div>
        <div class="image-content">
            <img src="{{ slide.image.url }}" alt="{{ slide.image.alt }}" />
            <p class="image-credit">
                Фото: {{ slide.image.photographer }} | Pexels
            </p>
        </div>
    </div>
    {% else %}
    <div class="slide-content">
        {{ slide.content }}
    </div>
    {% endif %}
</div>
```

### CSS стили

```css
.slide-content-with-image {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 30px;
    align-items: center;
}

.image-content img {
    width: 100%;
    height: auto;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.image-credit {
    font-size: 12px;
    color: #666;
    margin-top: 8px;
    text-align: center;
}
```

## ⚡ Производительность

### Кэширование

Сервис автоматически кэширует результаты поиска:

```python
# Первый запрос - идет к API
images = await search_images("machine learning")  # ~0.7s

# Второй запрос - из кэша  
images = await search_images("machine learning")  # ~0.001s
```

### Параллельная обработка

Для нескольких слайдов:

```python
async def process_multiple_slides(slides_data: list):
    """Параллельная обработка изображений для всех слайдов"""
    
    # Создаем задачи для всех слайдов
    tasks = []
    for slide in slides_data:
        task = get_image_for_slide(slide['content'])
        tasks.append(task)
    
    # Выполняем параллельно
    images = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Обрабатываем результаты
    for i, image in enumerate(images):
        if not isinstance(image, Exception) and image:
            slides_data[i]['image'] = image
    
    return slides_data
```

## 🛠️ Конфигурация

### Настройки поиска

```python
from ai_services.image_service import PexelsImageService

# Кастомная конфигурация
service = PexelsImageService(api_key="your_key")

# Поиск с параметрами
images = await service.search_images(
    query="business presentation",
    per_page=15,
    orientation="landscape",  # landscape, portrait, square
    size="large"             # large, medium, small
)
```

### Обработка ошибок

```python
async def safe_image_search(query: str):
    """Безопасный поиск с обработкой ошибок"""
    try:
        async with image_service as service:
            images = await service.search_images(query)
            return images
    except Exception as e:
        logger.error(f"Ошибка поиска изображений: {str(e)}")
        
        # Возвращаем плейсхолдер
        return [{
            "url": f"https://via.placeholder.com/800x600?text={query}",
            "alt": f"Placeholder for {query}",
            "photographer": "Placeholder"
        }]
```

## 🧪 Тестирование

### Запуск тестов

```bash
# Тест сервиса изображений
python test_image_service.py

# Тест API (нужен запущенный сервер)
python test_enhanced_api.py
```

### Unit тесты

```python
import pytest
from ai_services.image_service import search_images

@pytest.mark.asyncio
async def test_image_search():
    images = await search_images("technology", 3)
    assert len(images) <= 3
    assert all('url' in img for img in images)

@pytest.mark.asyncio  
async def test_slide_analysis():
    image = await get_image_for_slide("Machine Learning")
    assert image is None or 'url' in image
```

## 🔄 Миграция существующего кода

### 1. Обновление роутеров

```python
# Добавьте в существующий роутер
from ai_services.image_service import get_image_for_slide

@router.post("/generate-with-images")
async def generate_presentation_with_images(request: PresentationRequest):
    # Ваша существующая логика генерации
    presentation = await generate_presentation(request)
    
    # Добавление изображений
    for slide in presentation.slides:
        image = await get_image_for_slide(slide.content)
        if image:
            slide.image = image
    
    return presentation
```

### 2. Обновление HTML шаблонов

Добавьте поддержку изображений в существующие шаблоны:

```html
<!-- Ваш существующий слайд -->
<div class="slide">
    <h2>{{ slide.title }}</h2>
    <div class="content">{{ slide.content }}</div>
    
    <!-- Новое: условное отображение изображения -->
    {% if slide.image %}
    <div class="slide-image">
        <img src="{{ slide.image.url }}" alt="{{ slide.image.alt }}" />
    </div>
    {% endif %}
</div>
```

## 📞 Поддержка

### Логирование

Сервис использует стандартное Python логирование:

```python
import logging
logging.basicConfig(level=logging.INFO)

# Логи будут показывать:
# [INFO] Searching Pexels for: 'artificial intelligence'
# [INFO] ✅ Найдено 5 изображений для: artificial intelligence  
# [WARN] ⚠️ Превышен лимит запросов Pexels API
```

### Мониторинг

```python
# Проверка статуса через API
GET /api/v1/enhanced/health

# Или в коде
from ai_services.image_service import image_service

cache_size = len(image_service._cache)
api_available = image_service.api_key != "your_pexels_api_key"
```

### Fallback режим

Если Pexels API недоступен, сервис автоматически переключается на плейсхолдеры:

```python
# При отсутствии API ключа или ошибках API
# возвращаются красивые плейсхолдеры
image = {
    "url": "https://via.placeholder.com/800x600/4A90E2/FFFFFF?text=Your+Topic",
    "alt": "Placeholder image",
    "photographer": "Placeholder Service"
}
```

---

## 🤝 Совместная работа

Этот микросервис создан для **легкой интеграции** с вашей частью проекта. Все изменения обратно совместимы - существующий функционал работает без изменений.

**Ключевые точки интеграции:**
1. **API эндпоинты** - готовы к использованию
2. **Утилитарные функции** - для прямого использования в коде  
3. **HTML шаблоны** - примеры интеграции
4. **Обработка ошибок** - graceful fallback
5. **Кэширование** - оптимизация производительности

Микросервис полностью **автономен** и не влияет на существующую функциональность!
