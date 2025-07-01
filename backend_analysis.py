#!/usr/bin/env python3
"""
Анализ проблем в бэкенде SayDeck
"""

import os
import sys
import importlib
from typing import List, Dict, Any

def analyze_imports():
    """Анализ импортов и зависимостей"""
    print("🔍 АНАЛИЗ ИМПОРТОВ И ЗАВИСИМОСТЕЙ")
    print("=" * 50)
    
    modules_to_check = [
        'main',
        'config.settings',
        'models.base',
        'models.user',
        'models.presentation',
        'models.board',
        'models.template',
        'models.userpreferences',
        'routers.auth',
        'routers.presentations',
        'routers.generate',
        'routers.boards',
        'routers.templates',
        'routers.preferences',
        'utils.auth',
        'utils.openai_client',
        'schemas.user',
        'schemas.presentation',
        'schemas.board',
        'schemas.template',
        'schemas.userpreferences'
    ]
    
    import_errors = []
    missing_modules = []
    
    for module in modules_to_check:
        try:
            importlib.import_module(module)
            print(f"✅ {module}")
        except ImportError as e:
            print(f"❌ {module}: {e}")
            import_errors.append((module, str(e)))
        except Exception as e:
            print(f"⚠️  {module}: {e}")
            missing_modules.append((module, str(e)))
    
    return import_errors, missing_modules

def analyze_configuration():
    """Анализ конфигурации"""
    print("\n🔧 АНАЛИЗ КОНФИГУРАЦИИ")
    print("=" * 50)
    
    issues = []
    
    # Проверка файла .env
    if not os.path.exists('.env'):
        print("❌ Файл .env не найден")
        issues.append("Отсутствует файл .env")
    else:
        print("✅ Файл .env найден")
    
    # Проверка переменных окружения
    required_env_vars = [
        'POSTGRES_USER',
        'POSTGRES_PASSWORD', 
        'POSTGRES_SERVER',
        'POSTGRES_PORT',
        'POSTGRES_DB',
        'REDIS_HOST',
        'OPENAI_API_KEY'
    ]
    
    for var in required_env_vars:
        if not os.getenv(var):
            print(f"❌ Переменная окружения {var} не установлена")
            issues.append(f"Отсутствует переменная окружения {var}")
        else:
            print(f"✅ {var} установлена")
    
    return issues

def analyze_database_models():
    """Анализ моделей базы данных"""
    print("\n🗄️  АНАЛИЗ МОДЕЛЕЙ БАЗЫ ДАННЫХ")
    print("=" * 50)
    
    issues = []
    
    try:
        from models.base import Base, engine
        from models.user import User
        from models.presentation import Presentation
        from models.board import Board
        from models.template import Template
        from models.userpreferences import UserPreferences
        
        print("✅ Все модели импортированы успешно")
        
        # Проверка связей между моделями
        if hasattr(User, 'presentations'):
            print("✅ Связь User -> Presentation")
        else:
            print("❌ Отсутствует связь User -> Presentation")
            issues.append("Отсутствует связь User -> Presentation")
        
        if hasattr(User, 'boards'):
            print("✅ Связь User -> Board")
        else:
            print("❌ Отсутствует связь User -> Board")
            issues.append("Отсутствует связь User -> Board")
        
        if hasattr(Presentation, 'user_id'):
            print("✅ Поле user_id в Presentation")
        else:
            print("❌ Отсутствует поле user_id в Presentation")
            issues.append("Отсутствует поле user_id в Presentation")
        
    except Exception as e:
        print(f"❌ Ошибка при анализе моделей: {e}")
        issues.append(f"Ошибка при анализе моделей: {e}")
    
    return issues

def analyze_routers():
    """Анализ роутеров"""
    print("\n🛣️  АНАЛИЗ РОУТЕРОВ")
    print("=" * 50)
    
    issues = []
    
    routers_to_check = [
        ('auth', 'routers.auth'),
        ('presentations', 'routers.presentations'),
        ('generate', 'routers.generate'),
        ('boards', 'routers.boards'),
        ('templates', 'routers.templates'),
        ('preferences', 'routers.preferences')
    ]
    
    for router_name, module_path in routers_to_check:
        try:
            module = importlib.import_module(module_path)
            if hasattr(module, 'router'):
                print(f"✅ {router_name}: router найден")
            else:
                print(f"❌ {router_name}: router не найден")
                issues.append(f"Router {router_name} не найден")
        except Exception as e:
            print(f"❌ {router_name}: {e}")
            issues.append(f"Ошибка в router {router_name}: {e}")
    
    return issues

def analyze_utils():
    """Анализ утилит"""
    print("\n🔧 АНАЛИЗ УТИЛИТ")
    print("=" * 50)
    
    issues = []
    
    # Проверка auth utils
    try:
        from utils.auth import (
            verify_password,
            get_password_hash,
            create_access_token,
            get_current_user
        )
        print("✅ Все функции auth импортированы")
    except Exception as e:
        print(f"❌ Ошибка в auth utils: {e}")
        issues.append(f"Ошибка в auth utils: {e}")
    
    # Проверка OpenAI utils
    try:
        from utils.openai_client import (
            transcribe_audio,
            generate_presentation_structure,
            generate_presentation_pptx
        )
        print("✅ Все функции OpenAI импортированы")
    except Exception as e:
        print(f"❌ Ошибка в OpenAI utils: {e}")
        issues.append(f"Ошибка в OpenAI utils: {e}")
    
    return issues

def analyze_schemas():
    """Анализ схем Pydantic"""
    print("\n📋 АНАЛИЗ СХЕМ PYDANTIC")
    print("=" * 50)
    
    issues = []
    
    schemas_to_check = [
        ('user', 'schemas.user'),
        ('presentation', 'schemas.presentation'),
        ('board', 'schemas.board'),
        ('template', 'schemas.template'),
        ('userpreferences', 'schemas.userpreferences')
    ]
    
    for schema_name, module_path in schemas_to_check:
        try:
            module = importlib.import_module(module_path)
            print(f"✅ {schema_name}: модуль загружен")
        except Exception as e:
            print(f"❌ {schema_name}: {e}")
            issues.append(f"Ошибка в схеме {schema_name}: {e}")
    
    return issues

def analyze_main_app():
    """Анализ главного приложения"""
    print("\n🚀 АНАЛИЗ ГЛАВНОГО ПРИЛОЖЕНИЯ")
    print("=" * 50)
    
    issues = []
    
    try:
        from main import app
        
        # Проверка middleware
        if hasattr(app, 'user_middleware_stack'):
            print("✅ Middleware настроены")
        else:
            print("❌ Middleware не настроены")
            issues.append("Middleware не настроены")
        
        # Проверка роутеров
        if hasattr(app, 'routes'):
            print(f"✅ Найдено {len(app.routes)} роутов")
        else:
            print("❌ Роуты не найдены")
            issues.append("Роуты не найдены")
        
        # Проверка событий
        if hasattr(app, 'router'):
            print("✅ Router настроен")
        else:
            print("❌ Router не настроен")
            issues.append("Router не настроен")
        
    except Exception as e:
        print(f"❌ Ошибка при анализе главного приложения: {e}")
        issues.append(f"Ошибка при анализе главного приложения: {e}")
    
    return issues

def analyze_security():
    """Анализ безопасности"""
    print("\n🔒 АНАЛИЗ БЕЗОПАСНОСТИ")
    print("=" * 50)
    
    issues = []
    
    # Проверка CORS
    try:
        from main import app
        from fastapi.middleware.cors import CORSMiddleware
        
        cors_configured = False
        for middleware in app.user_middleware_stack:
            if isinstance(middleware.cls, type) and middleware.cls == CORSMiddleware:
                cors_configured = True
                break
        
        if cors_configured:
            print("✅ CORS настроен")
        else:
            print("❌ CORS не настроен")
            issues.append("CORS не настроен")
    except Exception as e:
        print(f"❌ Ошибка при проверке CORS: {e}")
        issues.append(f"Ошибка при проверке CORS: {e}")
    
    # Проверка rate limiting
    try:
        from fastapi_limiter import FastAPILimiter
        print("✅ FastAPI Limiter импортирован")
    except ImportError:
        print("❌ FastAPI Limiter не установлен")
        issues.append("FastAPI Limiter не установлен")
    
    # Проверка JWT
    try:
        from jose import JWTError, jwt
        print("✅ JWT библиотека доступна")
    except ImportError:
        print("❌ JWT библиотека не установлена")
        issues.append("JWT библиотека не установлена")
    
    return issues

def generate_report():
    """Генерация отчета по анализу"""
    print("🔍 ПОЛНЫЙ АНАЛИЗ БЭКЕНДА SAYDECK")
    print("=" * 60)
    
    all_issues = []
    
    # Выполнение всех анализов
    import_errors, missing_modules = analyze_imports()
    config_issues = analyze_configuration()
    db_issues = analyze_database_models()
    router_issues = analyze_routers()
    utils_issues = analyze_utils()
    schema_issues = analyze_schemas()
    app_issues = analyze_main_app()
    security_issues = analyze_security()
    
    # Сбор всех проблем
    all_issues.extend(import_errors)
    all_issues.extend(missing_modules)
    all_issues.extend(config_issues)
    all_issues.extend(db_issues)
    all_issues.extend(router_issues)
    all_issues.extend(utils_issues)
    all_issues.extend(schema_issues)
    all_issues.extend(app_issues)
    all_issues.extend(security_issues)
    
    # Генерация отчета
    print("\n" + "=" * 60)
    print("📊 ИТОГОВЫЙ ОТЧЕТ")
    print("=" * 60)
    
    if not all_issues:
        print("🎉 КРИТИЧЕСКИХ ПРОБЛЕМ НЕ НАЙДЕНО!")
        print("✅ Бэкенд готов к работе")
    else:
        print(f"⚠️  НАЙДЕНО {len(all_issues)} ПРОБЛЕМ:")
        print()
        
        for i, issue in enumerate(all_issues, 1):
            if isinstance(issue, tuple):
                print(f"{i}. {issue[0]}: {issue[1]}")
            else:
                print(f"{i}. {issue}")
        
        print("\n🔧 РЕКОМЕНДАЦИИ ПО ИСПРАВЛЕНИЮ:")
        print("1. Установите все необходимые зависимости")
        print("2. Настройте переменные окружения в файле .env")
        print("3. Проверьте подключение к базе данных")
        print("4. Убедитесь, что Redis сервер запущен")
        print("5. Проверьте настройки OpenAI API")
    
    return all_issues

if __name__ == "__main__":
    generate_report() 