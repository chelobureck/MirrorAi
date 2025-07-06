#!/usr/bin/env python3
"""
Простой скрипт для запуска сервера SayDeck
"""
import uvicorn
import sys
import os

if __name__ == "__main__":
    print("🚀 Запуск SayDeck сервера...")
    print(f"📁 Рабочая директория: {os.getcwd()}")
    print(f"🐍 Python: {sys.executable}")
    
    try:
        uvicorn.run(
            "main:app",
            host="127.0.0.1",
            port=8000,
            reload=True,
            log_level="info"
        )
    except Exception as e:
        print(f"❌ Ошибка запуска сервера: {e}")
        sys.exit(1)
