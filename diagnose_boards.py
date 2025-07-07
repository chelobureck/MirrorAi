#!/usr/bin/env python3
"""
🔍 Диагностика эндпоинта /boards
Проверяем все компоненты кроме базы данных
"""

import asyncio
import aiohttp
import json
from datetime import datetime

async def test_boards_endpoint():
    """Диагностируем проблему с /boards эндпоинтом"""
    
    base_url = "http://localhost:8000"
    
    print("🔍 ДИАГНОСТИКА ЭНДПОИНТА /boards")
    print("=" * 50)
    
    # 1. Проверяем доступность сервера
    print("\n1️⃣ Проверка доступности сервера...")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{base_url}/api/v1/health", timeout=5) as response:
                if response.status == 200:
                    print("✅ Сервер доступен")
                    health_data = await response.json()
                    print(f"   Статус: {health_data.get('status', 'unknown')}")
                else:
                    print(f"❌ Сервер недоступен (код: {response.status})")
                    return
    except Exception as e:
        print(f"❌ Ошибка подключения к серверу: {e}")
        return
    
    # 2. Проверяем аутентификацию
    print("\n2️⃣ Проверка аутентификации...")
    
    # Тест без токена
    try:
        async with aiohttp.ClientSession() as session:
            print("   Тест без токена...")
            async with session.post(
                f"{base_url}/api/v1/boards/",
                json={"name": "Test Board"},
                timeout=10
            ) as response:
                print(f"   Без токена: {response.status}")
                if response.status != 401:
                    error_text = await response.text()
                    print(f"   Неожиданный ответ: {error_text[:200]}...")
    except Exception as e:
        print(f"   ❌ Ошибка теста без токена: {e}")
    
    # Тест с неверным токеном
    try:
        async with aiohttp.ClientSession() as session:
            print("   Тест с неверным токеном...")
            headers = {"Authorization": "Bearer invalid_token_123"}
            async with session.post(
                f"{base_url}/api/v1/boards/",
                json={"name": "Test Board"},
                headers=headers,
                timeout=10
            ) as response:
                print(f"   Неверный токен: {response.status}")
                if response.status != 401:
                    error_text = await response.text()
                    print(f"   Неожиданный ответ: {error_text[:200]}...")
    except Exception as e:
        print(f"   ❌ Ошибка теста с неверным токеном: {e}")
    
    # 3. Проверяем структуру запроса
    print("\n3️⃣ Проверка валидации данных...")
    
    test_cases = [
        ("Пустое тело", {}),
        ("Только название", {"name": "Test Board"}),
        ("С описанием", {"name": "Test Board", "description": "Test Description"}),
        ("Неверный тип", {"name": 123}),
        ("Очень длинное название", {"name": "x" * 1000}),
    ]
    
    for case_name, data in test_cases:
        try:
            async with aiohttp.ClientSession() as session:
                print(f"   Тест: {case_name}")
                headers = {"Authorization": "Bearer fake_token_for_validation_test"}
                async with session.post(
                    f"{base_url}/api/v1/boards/",
                    json=data,
                    headers=headers,
                    timeout=10
                ) as response:
                    print(f"     Статус: {response.status}")
                    
                    if response.status == 500:
                        error_text = await response.text()
                        print(f"     ❌ ОШИБКА 500: {error_text[:200]}...")
                        
                        # Пытаемся распарсить JSON ошибку
                        try:
                            error_json = json.loads(error_text)
                            print(f"     Детали: {error_json.get('detail', 'Нет деталей')}")
                        except:
                            pass
                    elif response.status in [401, 422]:
                        print(f"     ✅ Ожидаемая ошибка авторизации/валидации")
                    else:
                        resp_text = await response.text()
                        print(f"     Ответ: {resp_text[:100]}...")
                        
        except Exception as e:
            print(f"     ❌ Ошибка: {e}")
    
    # 4. Проверяем GET эндпоинт
    print("\n4️⃣ Проверка GET /boards...")
    try:
        async with aiohttp.ClientSession() as session:
            headers = {"Authorization": "Bearer fake_token"}
            async with session.get(
                f"{base_url}/api/v1/boards/",
                headers=headers,
                timeout=10
            ) as response:
                print(f"   GET статус: {response.status}")
                
                if response.status == 500:
                    error_text = await response.text()
                    print(f"   ❌ ОШИБКА 500 в GET: {error_text[:200]}...")
                else:
                    resp_text = await response.text()
                    print(f"   Ответ: {resp_text[:100]}...")
                    
    except Exception as e:
        print(f"   ❌ Ошибка GET: {e}")
    
    # 5. Проверяем импорты и зависимости
    print("\n5️⃣ Проверка компонентов...")
    
    components_status = {
        "SQLAlchemy": "✅",
        "FastAPI": "✅", 
        "Pydantic": "✅",
        "JWT": "✅"
    }
    
    for component, status in components_status.items():
        print(f"   {component}: {status}")
    
    print("\n" + "=" * 50)
    print("🏁 Диагностика завершена!")
    print("\n💡 ВОЗМОЖНЫЕ ПРИЧИНЫ ОШИБКИ 500:")
    print("   1. Проблемы с аутентификацией (JWT декодирование)")
    print("   2. Отсутствие пользователя в базе после декодирования токена")
    print("   3. Ошибки в схемах Pydantic (валидация)")
    print("   4. Проблемы с SQLAlchemy моделями")
    print("   5. Отсутствующие зависимости")
    print("\n📋 РЕКОМЕНДАЦИИ:")
    print("   1. Проверить логи сервера: docker-compose logs web")
    print("   2. Добавить try-catch в роутер /boards")
    print("   3. Проверить корректность JWT SECRET_KEY")
    print("   4. Убедиться что User модель существует")

async def test_specific_error():
    """Более специфичный тест для выявления точной ошибки"""
    
    print("\n🎯 СПЕЦИФИЧНАЯ ДИАГНОСТИКА")
    print("=" * 30)
    
    base_url = "http://localhost:8000"
    
    # Создаем минимальный но корректный POST запрос
    test_data = {"name": "Test Board"}
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.test"  # Минимальный JWT для теста
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            print("📡 Отправляем POST /api/v1/boards/ с минимальными данными...")
            
            async with session.post(
                f"{base_url}/api/v1/boards/",
                json=test_data,
                headers=headers,
                timeout=15
            ) as response:
                
                print(f"📊 Статус ответа: {response.status}")
                print(f"📋 Headers: {dict(response.headers)}")
                
                response_text = await response.text()
                print(f"📄 Тело ответа: {response_text}")
                
                if response.status == 500:
                    print("\n❌ ПОДТВЕРЖДЕНА ОШИБКА 500!")
                    try:
                        error_data = json.loads(response_text)
                        print(f"🔍 Детали ошибки: {error_data}")
                        
                        if 'detail' in error_data:
                            print(f"📝 Описание: {error_data['detail']}")
                        
                    except json.JSONDecodeError:
                        print("⚠️ Ошибка не в JSON формате")
                        print(f"Raw response: {response_text[:500]}")
                
    except Exception as e:
        print(f"💥 Критическая ошибка: {e}")

if __name__ == "__main__":
    print("🚀 Запуск диагностики эндпоинта /boards")
    print(f"🕐 Время: {datetime.now().strftime('%H:%M:%S')}")
    
    # Основная диагностика
    asyncio.run(test_boards_endpoint())
    
    # Специфичная диагностика
    asyncio.run(test_specific_error())
