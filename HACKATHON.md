# Hackathon Branch - bestcomp

## Изменения в этой ветке:

### ✅ Исправления:
- **Redis порт изменен** с 6379 на 6378 для избежания конфликтов
- **Docker-compose обновлен** для работы с несколькими Redis инстансами
- **Настройки окружения** обновлены для локальной разработки

### 📋 Задачи на хакатон:
- [ ] Добавить новые AI модели
- [ ] Улучшить генерацию презентаций
- [ ] Добавить новые форматы экспорта
- [ ] Оптимизировать производительность
- [ ] Добавить новые типы шаблонов

### 🚀 Как запустить:
```bash
# Остановить существующие контейнеры
docker-compose down

# Запустить проект
docker-compose up -d

# Проверить логи
docker-compose logs -f web
```

### 🔧 Полезные команды:
```bash
# Войти в контейнер приложения
docker-compose exec web bash

# Войти в PostgreSQL
docker-compose exec db psql -U say_deck_user -d say_deck

# Перезапустить только веб-сервис
docker-compose restart web

# Посмотреть все контейнеры
docker ps -a
```

### 📝 Заметки:
- Проект использует FastAPI + PostgreSQL + Redis + OpenAI
- Порты: Web:8000, DB:5432, Redis:6378
- Все настройки в .env файле
- API документация доступна на http://localhost:8000/docs

---
**Автор:** bestcomp  
**Дата:** $(date)  
**Ветка:** hackathon-bestcomp
