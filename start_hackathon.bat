@echo off
echo ==========================================
echo       SayDeck Hackathon Quick Start
echo ==========================================
echo.

echo Останавливаем существующие контейнеры...
docker-compose down

echo.
echo Запускаем проект...
docker-compose up -d

echo.
echo Ожидаем запуск сервисов...
timeout /t 10 /nobreak > nul

echo.
echo Проверяем статус контейнеров:
docker ps

echo.
echo ==========================================
echo   Проект запущен!
echo   Web:   http://localhost:8000
echo   Docs:  http://localhost:8000/docs  
echo   Redis: localhost:6378
echo   DB:    localhost:5432
echo ==========================================
echo.

pause
