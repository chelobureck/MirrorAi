#!/usr/bin/env python3
"""
🔍 Диагностика эндпоинта /boards
Тестирование POST запроса на создание доски
"""

import asyncio
import aiohttp
import json

async def test_boards_endpoint():
    """Тестируем POST /api/v1/boards"""
    
    base_url = "http://localhost:8000"
    
    print("🔍 Диагностика эндпоинта /boards")
    print("=" * 50)
    
    # Сначала проверим health check
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{base_url}/api/v1/health") as response:
                if response.status == 200:
                    print("✅ API сервер работает")
                else:
                    print(f"❌ API сервер недоступен: {response.status}")
                    return
    except Exception as e:
        print(f"❌ Не удается подключиться к серверу: {e}")
        return
    
    # Тест 1: POST без авторизации (должен вернуть 401)
    print("\n📝 Тест 1: POST /api/v1/boards без авторизации")
    try:
        async with aiohttp.ClientSession() as session:
            test_data = {
                "name": "Тестовая доска",
                "description": "Описание тестовой доски"
            }
            
            async with session.post(
                f"{base_url}/api/v1/boards/",
                json=test_data,
                headers={"Content-Type": "application/json"}
            ) as response:
                
                print(f"   Статус: {response.status}")
                text = await response.text()
                print(f"   Ответ: {text[:200]}...")
                
                if response.status == 401:
                    print("   ✅ Ожидаемый результат - требуется авторизация")
                elif response.status == 500:
                    print("   ❌ Ошибка 500 - проблема на сервере!")
                    try:
                        error_data = json.loads(text)
                        print(f"   🔍 Детали ошибки: {error_data.get('detail', 'Нет деталей')}")
                    except:
                        print(f"   🔍 Сырой ответ: {text}")
                else:
                    print(f"   ⚠️  Неожиданный статус: {response.status}")
                    
    except Exception as e:
        print(f"   💥 Ошибка запроса: {e}")
    
    # Тест 2: POST с фейковым токеном
    print("\n📝 Тест 2: POST /api/v1/boards с некорректным токеном")
    try:
        async with aiohttp.ClientSession() as session:
            test_data = {
                "name": "Тестовая доска",
                "description": "Описание тестовой доски"
            }
            
            async with session.post(
                f"{base_url}/api/v1/boards/",
                json=test_data,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": "Bearer fake_token_12345"
                }
            ) as response:
                
                print(f"   Статус: {response.status}")
                text = await response.text()
                print(f"   Ответ: {text[:200]}...")
                
                if response.status == 401:
                    print("   ✅ Ожидаемый результат - невалидный токен")
                elif response.status == 500:
                    print("   ❌ Ошибка 500 - проблема на сервере!")
                    try:
                        error_data = json.loads(text)
                        print(f"   🔍 Детали ошибки: {error_data.get('detail', 'Нет деталей')}")
                    except:
                        print(f"   🔍 Сырой ответ: {text}")
                        
    except Exception as e:
        print(f"   💥 Ошибка запроса: {e}")
    
    # Тест 3: Попробуем создать пользователя и получить токен
    print("\n📝 Тест 3: Создание пользователя и получение токена")
    
    test_user = {
        "email": "test_boards@example.com",
        "password": "testpass123",
        "username": "test_boards_user"
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            # Пытаемся зарегистрировать пользователя
            async with session.post(
                f"{base_url}/api/v1/auth/register",
                json=test_user,
                headers={"Content-Type": "application/json"}
            ) as response:
                
                print(f"   Регистрация - Статус: {response.status}")
                reg_text = await response.text()
                
                if response.status in [200, 201]:
                    print("   ✅ Пользователь создан")
                elif response.status == 400 and "already registered" in reg_text:
                    print("   ℹ️  Пользователь уже существует")
                else:
                    print(f"   ⚠️  Ответ регистрации: {reg_text[:200]}...")
            
            # Пытаемся войти
            login_data = {
                "email": test_user["email"],
                "password": test_user["password"]
            }
            
            async with session.post(
                f"{base_url}/api/v1/auth/login",
                json=login_data,
                headers={"Content-Type": "application/json"}
            ) as response:
                
                print(f"   Логин - Статус: {response.status}")
                login_text = await response.text()
                
                if response.status == 200:
                    try:
                        login_data = json.loads(login_text)
                        token = login_data.get("access_token")
                        
                        if token:
                            print("   ✅ Токен получен")
                            
                            # Тест 4: POST с валидным токеном
                            print("\n📝 Тест 4: POST /api/v1/boards с валидным токеном")
                            
                            board_data = {
                                "name": "Моя тестовая доска",
                                "description": "Создана для тестирования API"
                            }
                            
                            async with session.post(
                                f"{base_url}/api/v1/boards/",
                                json=board_data,
                                headers={
                                    "Content-Type": "application/json",
                                    "Authorization": f"Bearer {token}"
                                }
                            ) as response:
                                
                                print(f"   Статус: {response.status}")
                                board_text = await response.text()
                                
                                if response.status == 200:
                                    print("   ✅ Доска успешно создана!")
                                    try:
                                        board_result = json.loads(board_text)
                                        print(f"   📋 ID доски: {board_result.get('id')}")
                                        print(f"   📋 Название: {board_result.get('name')}")
                                    except:
                                        print(f"   📋 Ответ: {board_text}")
                                        
                                elif response.status == 500:
                                    print("   ❌ ОШИБКА 500 - Проблема найдена!")
                                    try:
                                        error_data = json.loads(board_text)
                                        print(f"   🔍 Детали: {error_data.get('detail', 'Нет деталей')}")
                                    except:
                                        print(f"   🔍 Сырая ошибка: {board_text}")
                                else:
                                    print(f"   ⚠️  Неожиданный ответ: {board_text[:200]}...")
                        else:
                            print("   ❌ Токен не найден в ответе")
                            
                    except json.JSONDecodeError:
                        print(f"   ❌ Не удается парсить ответ логина: {login_text[:200]}...")
                        
                else:
                    print(f"   ❌ Ошибка логина: {login_text[:200]}...")
                    
    except Exception as e:
        print(f"   💥 Ошибка теста с авторизацией: {e}")
    
    # Тест 5: Проверим доступность базы данных
    print("\n📝 Тест 5: Проверка подключения к базе данных")
    try:
        async with aiohttp.ClientSession() as session:
            # Попробуем любой эндпоинт, который использует БД
            async with session.get(f"{base_url}/api/v1/templates") as response:
                print(f"   Templates endpoint статус: {response.status}")
                if response.status == 200:
                    print("   ✅ База данных доступна")
                elif response.status == 500:
                    text = await response.text()
                    print("   ❌ Проблема с базой данных!")
                    print(f"   🔍 Ошибка: {text[:200]}...")
                    
    except Exception as e:
        print(f"   💥 Ошибка проверки БД: {e}")

if __name__ == "__main__":
    print("🧪 Диагностика эндпоинта /boards")
    print("Этот скрипт поможет найти причину ошибки 500")
    print()
    
    asyncio.run(test_boards_endpoint())
    
    print("\n" + "=" * 50)
    print("🏁 Диагностика завершена!")
    print()
    print("📋 Возможные причины ошибки 500:")
    print("1. Проблема с подключением к базе данных")
    print("2. Ошибка в модели Board или User")
    print("3. Проблема с системой аутентификации")
    print("4. Ошибка в зависимостях (get_session, get_current_user)")
    print("5. Проблема с миграциями таблиц")
