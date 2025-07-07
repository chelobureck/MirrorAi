#!/usr/bin/env python3
"""
🔧 Анализ возможных проблем с /boards эндпоинтом
Статический анализ кода без запуска сервера
"""

import os
import sys
import ast
import importlib.util

def check_file_exists(filepath, description):
    """Проверяет существование файла"""
    if os.path.exists(filepath):
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description} НЕ НАЙДЕН: {filepath}")
        return False

def check_python_syntax(filepath):
    """Проверяет синтаксис Python файла"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            source = f.read()
        ast.parse(source)
        print(f"✅ Синтаксис корректен: {os.path.basename(filepath)}")
        return True
    except SyntaxError as e:
        print(f"❌ Синтаксическая ошибка в {filepath}: {e}")
        return False
    except Exception as e:
        print(f"⚠️ Не удалось проверить {filepath}: {e}")
        return False

def analyze_imports(filepath):
    """Анализирует импорты в файле"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            source = f.read()
        
        tree = ast.parse(source)
        imports = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                for alias in node.names:
                    imports.append(f"{module}.{alias.name}")
        
        print(f"📦 Импорты в {os.path.basename(filepath)}:")
        for imp in imports[:10]:  # Показываем первые 10
            print(f"   - {imp}")
        if len(imports) > 10:
            print(f"   ... и еще {len(imports) - 10}")
            
        return imports
    except Exception as e:
        print(f"⚠️ Не удалось проанализировать импорты в {filepath}: {e}")
        return []

def check_model_relationships():
    """Проверяет связи в моделях"""
    print("\n🔗 ПРОВЕРКА СВЯЗЕЙ В МОДЕЛЯХ")
    print("=" * 30)
    
    # Проверим User модель
    user_model = "C:\\Users\\bestcomp\\SayDeck\\models\\user.py"
    if os.path.exists(user_model):
        try:
            with open(user_model, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if 'boards' in content and 'relationship' in content:
                print("✅ User модель имеет связь с boards")
            else:
                print("⚠️ User модель может не иметь связи с boards")
                print("   Это может вызывать проблемы с обратными связями")
                
        except Exception as e:
            print(f"❌ Ошибка чтения User модели: {e}")
    else:
        print("❌ User модель не найдена")

def check_schemas():
    """Проверяет схемы Pydantic"""
    print("\n📋 ПРОВЕРКА СХЕМ PYDANTIC")
    print("=" * 30)
    
    board_schema = "C:\\Users\\bestcomp\\SayDeck\\schemas\\board.py"
    if os.path.exists(board_schema):
        try:
            with open(board_schema, 'r', encoding='utf-8') as f:
                content = f.read()
            
            required_classes = ['BoardBase', 'BoardCreate', 'BoardResponse']
            for class_name in required_classes:
                if f"class {class_name}" in content:
                    print(f"✅ {class_name} найден")
                else:
                    print(f"❌ {class_name} НЕ НАЙДЕН")
                    
            # Проверим конфигурацию
            if 'from_attributes = True' in content or 'orm_mode = True' in content:
                print("✅ ORM конфигурация настроена")
            else:
                print("⚠️ ORM конфигурация может быть не настроена")
                
        except Exception as e:
            print(f"❌ Ошибка чтения схем: {e}")

def check_auth_dependencies():
    """Проверяет зависимости аутентификации"""
    print("\n🔐 ПРОВЕРКА АУТЕНТИФИКАЦИИ")
    print("=" * 30)
    
    auth_file = "C:\\Users\\bestcomp\\SayDeck\\utils\\auth.py"
    if os.path.exists(auth_file):
        try:
            with open(auth_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Проверяем ключевые функции
            functions_to_check = [
                'get_current_user',
                'create_access_token', 
                'verify_password'
            ]
            
            for func in functions_to_check:
                if f"def {func}" in content or f"async def {func}" in content:
                    print(f"✅ {func} найдена")
                else:
                    print(f"❌ {func} НЕ НАЙДЕНА")
            
            # Проверяем импорты
            critical_imports = ['jose', 'passlib', 'fastapi.security']
            for imp in critical_imports:
                if imp in content:
                    print(f"✅ Импорт {imp} найден")
                else:
                    print(f"⚠️ Импорт {imp} не найден")
                    
        except Exception as e:
            print(f"❌ Ошибка чтения auth.py: {e}")

def main():
    print("🔍 СТАТИЧЕСКИЙ АНАЛИЗ ПРОБЛЕМ С /boards")
    print("=" * 50)
    
    base_path = "C:\\Users\\bestcomp\\SayDeck"
    
    # 1. Проверяем существование ключевых файлов
    print("\n1️⃣ ПРОВЕРКА ФАЙЛОВ")
    print("-" * 20)
    
    key_files = {
        f"{base_path}\\routers\\boards.py": "Роутер boards",
        f"{base_path}\\models\\board.py": "Модель Board", 
        f"{base_path}\\models\\user.py": "Модель User",
        f"{base_path}\\schemas\\board.py": "Схемы Board",
        f"{base_path}\\utils\\auth.py": "Утилиты аутентификации",
        f"{base_path}\\config\\settings.py": "Настройки",
        f"{base_path}\\main.py": "Главный файл"
    }
    
    all_files_exist = True
    for filepath, description in key_files.items():
        if not check_file_exists(filepath, description):
            all_files_exist = False
    
    if not all_files_exist:
        print("\n❌ КРИТИЧНО: Не все необходимые файлы найдены!")
        return
    
    # 2. Проверяем синтаксис
    print("\n2️⃣ ПРОВЕРКА СИНТАКСИСА")
    print("-" * 20)
    
    for filepath in key_files.keys():
        check_python_syntax(filepath)
    
    # 3. Анализируем импорты
    print("\n3️⃣ АНАЛИЗ ИМПОРТОВ")
    print("-" * 20)
    
    analyze_imports(f"{base_path}\\routers\\boards.py")
    
    # 4. Специальные проверки
    check_model_relationships()
    check_schemas() 
    check_auth_dependencies()
    
    # 5. Проверяем возможные причины ошибки 500
    print("\n🎯 ВОЗМОЖНЫЕ ПРИЧИНЫ ОШИБКИ 500")
    print("=" * 40)
    
    potential_issues = [
        {
            "issue": "Проблемы с JWT токеном",
            "check": "SECRET_KEY в settings.py",
            "solution": "Убедиться что SECRET_KEY настроен правильно"
        },
        {
            "issue": "Отсутствует пользователь в БД",
            "check": "get_current_user возвращает None",
            "solution": "Проверить что пользователь существует после декодирования JWT"
        },
        {
            "issue": "Ошибки валидации Pydantic",
            "check": "BoardCreate схема",
            "solution": "Проверить соответствие полей в схеме и модели"
        },
        {
            "issue": "Проблемы с SQLAlchemy сессией",
            "check": "get_session dependency",
            "solution": "Проверить настройки базы данных"
        },
        {
            "issue": "Отсутствующие поля в модели",
            "check": "Board.description поле",
            "solution": "Убедиться что все поля схемы есть в модели"
        }
    ]
    
    for i, issue_info in enumerate(potential_issues, 1):
        print(f"{i}. {issue_info['issue']}")
        print(f"   Проверить: {issue_info['check']}")
        print(f"   Решение: {issue_info['solution']}")
        print()
    
    print("💡 РЕКОМЕНДАЦИИ ДЛЯ ИСПРАВЛЕНИЯ:")
    print("1. Добавить логирование в роутер (уже сделано)")
    print("2. Добавить try-catch блоки (уже сделано)")
    print("3. Проверить настройки JWT в config/settings.py")
    print("4. Убедиться что description поле есть в модели Board")
    print("5. Проверить что пользователь создан в базе данных")
    
    print(f"\n🏁 Анализ завершен!")

if __name__ == "__main__":
    main()
