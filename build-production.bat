@echo off
REM Скрипт для создания production-ready Docker образа SayDeck
REM Для AWS ECS Deploy

echo 🚀 Building SayDeck Production Docker Image...

REM Проверяем наличие .env.aws файла
if not exist ".env.aws" (
    echo ❌ Файл .env.aws не найден!
    echo Создайте файл .env.aws с production переменными окружения
    exit /b 1
)

REM Собираем Docker образ
echo 📦 Building Docker image...
docker build -t saydeck:latest -f Dockerfile .

if %errorlevel% equ 0 (
    echo ✅ Docker образ успешно собран!
    
    REM Показываем размер образа
    echo 📊 Размер образа:
    docker images saydeck:latest
    
    echo.
    echo 🧪 Для тестирования образа локально запустите:
    echo docker run -p 80:80 --env-file .env.aws saydeck:latest
    echo.
    echo 🔗 Для деплоя в AWS ECS:
    echo 1. Загрузите образ в ECR (Amazon Elastic Container Registry^)
    echo 2. Обновите ECS Task Definition
    echo 3. Обновите ECS Service
) else (
    echo ❌ Ошибка при сборке Docker образа!
    exit /b 1
)
