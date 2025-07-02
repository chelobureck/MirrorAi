#!/usr/bin/env python3
"""
Скрипт для добавления тестовых данных в базу данных SayDeck
"""
import asyncio
import os
import sys
from datetime import datetime

# Добавляем корневую папку в path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.base import get_session, engine, Base
from models.user import User
from models.presentation import Presentation
from utils.auth import get_password_hash
from sqlalchemy.ext.asyncio import AsyncSession

async def create_test_data():
    """Создает тестовые данные"""
    
    # Создаем таблицы
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with get_session().__anext__() as session:
        # Создаем тестового пользователя
        test_user = User(
            email="test@example.com",
            username="testuser",
            hashed_password=get_password_hash("testpassword123"),
            role="user",
            credits=100,
            is_email_verified=True
        )
        
        session.add(test_user)
        await session.commit()
        await session.refresh(test_user)
        
        # Создаем тестовые презентации
        test_presentations = [
            {
                "title": "Введение в искусственный интеллект",
                "content": {
                    "slides": [
                        {
                            "title": "Что такое ИИ?",
                            "content": "Искусственный интеллект - это технология, позволяющая машинам имитировать человеческий интеллект",
                            "type": "title"
                        },
                        {
                            "title": "Области применения",
                            "content": "• Медицина\n• Транспорт\n• Финансы\n• Образование",
                            "type": "content"
                        },
                        {
                            "title": "Перспективы развития",
                            "content": "ИИ будет играть все более важную роль в нашей жизни",
                            "type": "content"
                        }
                    ]
                },
                "user_id": test_user.id
            },
            {
                "title": "Основы веб-разработки",
                "content": {
                    "slides": [
                        {
                            "title": "HTML, CSS, JavaScript",
                            "content": "Основные технологии для создания веб-сайтов",
                            "type": "title"
                        },
                        {
                            "title": "Frontend vs Backend",
                            "content": "Frontend - пользовательский интерфейс\nBackend - серверная логика",
                            "type": "content"
                        }
                    ]
                },
                "user_id": test_user.id
            },
            {
                "title": "Python для начинающих",
                "content": {
                    "slides": [
                        {
                            "title": "Почему Python?",
                            "content": "Простой синтаксис, большое сообщество, множество библиотек",
                            "type": "title"
                        },
                        {
                            "title": "Основы синтаксиса",
                            "content": "print('Hello, World!')\nname = 'Python'\nif name == 'Python':\n    print('Это Python!')",
                            "type": "content"
                        }
                    ]
                },
                "user_id": test_user.id
            }
        ]
        
        for pres_data in test_presentations:
            presentation = Presentation(**pres_data)
            session.add(presentation)
        
        await session.commit()
        
        print("✅ Тестовые данные успешно созданы!")
        print(f"📧 Email: test@example.com")
        print(f"🔑 Password: testpassword123")
        print(f"👤 User ID: {test_user.id}")
        print(f"📊 Создано презентаций: {len(test_presentations)}")

async def main():
    """Главная функция"""
    try:
        await create_test_data()
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
