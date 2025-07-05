# 🤝 Contributing to SayDeck

<div align="center">

**Добро пожаловать в сообщество SayDeck!** 

*Мы рады каждому вкладу в развитие проекта*

</div>

---

## 🎯 Как внести вклад

### 🐛 **Нашли баг?**
1. Проверьте [существующие issues](https://github.com/chelobureck/SayDeck/issues)
2. Создайте новый issue с подробным описанием
3. Используйте шаблон bug report

### 💡 **Есть идея для улучшения?**
1. Обсудите в [GitHub Discussions](https://github.com/chelobureck/SayDeck/discussions)
2. Создайте feature request
3. Опишите пользу для проекта

### 🔧 **Хотите написать код?**

#### Шаг 1: Настройка окружения
```bash
# Форк репозитория
git clone https://github.com/YOUR_USERNAME/SayDeck.git
cd SayDeck

# Создание виртуального окружения
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# Установка зависимостей
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Если есть dev зависимости
```

#### Шаг 2: Создание ветки
```bash
git checkout -b feature/your-amazing-feature
# или
git checkout -b fix/bug-description
```

#### Шаг 3: Разработка
- Следуйте code style проекта
- Добавьте тесты для новой функциональности
- Обновите документацию при необходимости

#### Шаг 4: Тестирование
```bash
# Запуск тестов
pytest

# Проверка code style
flake8 .
black --check .

# Запуск сервера для тестирования
uvicorn main:app --reload
```

#### Шаг 5: Pull Request
```bash
git add .
git commit -m "feat: add amazing feature"
git push origin feature/your-amazing-feature
```

Создайте PR через GitHub с подробным описанием изменений.

---

## 📋 Code Style

### 🐍 **Python Code Style**
- Используем **Black** для форматирования
- Следуем **PEP 8**
- Максимальная длина строки: **88 символов**
- Используем **type hints** везде где возможно

```python
# ✅ Хорошо
async def create_presentation(
    topic: str, 
    audience: str = "general",
    slide_count: int = 10
) -> PresentationResponse:
    """Create a new presentation with AI."""
    pass

# ❌ Плохо  
def create_presentation(topic, audience="general", slide_count=10):
    pass
```

### 📝 **Commit Messages**
Используем [Conventional Commits](https://www.conventionalcommits.org/):

```bash
feat: add PDF export functionality
fix: resolve auth token expiration issue
docs: update API documentation
test: add unit tests for presentation service
refactor: optimize database queries
```

### 🧪 **Testing**
- Покрытие тестами > 80%
- Unit тесты для бизнес-логики
- Integration тесты для API endpoints
- Мокируем внешние зависимости

---

## 🎯 Области для вклада

### 🚀 **Высокий приоритет**
- [ ] PDF экспорт презентаций
- [ ] Дополнительные AI провайдеры (OpenAI, Claude)
- [ ] Улучшение производительности
- [ ] Мобильная адаптация

### 🔧 **Средний приоритет**  
- [ ] Новые темы дизайна
- [ ] Интеграции (Slack, Teams)
- [ ] Аналитика и метрики
- [ ] Кэширование

### 💡 **Идеи для новичков**
- [ ] Улучшение документации
- [ ] Добавление примеров
- [ ] Исправление мелких багов
- [ ] Перевод на другие языки

---

## 🏆 Recognition

Все участники будут упомянуты в:
- README.md файле
- Release notes
- Hall of Fame на сайте проекта

### 🎖️ **Уровни участия:**

| Уровень | Вклад | Награда |
|---------|--------|---------|
| 🥉 **Contributor** | 1-5 PR | Mention в README |
| 🥈 **Regular** | 5-15 PR | Badge + Blog post |
| 🥇 **Core** | 15+ PR | Maintainer права |

---

## 📞 Связь

- 💬 **Discord:** [SayDeck Community](https://discord.gg/saydeck)
- 📧 **Email:** contribute@saydeck.com
- 🐦 **Twitter:** [@SayDeckAI](https://twitter.com/saydeckai)

---

## 📜 License

Внося вклад в проект, вы соглашаетесь с [MIT License](LICENSE).

---

<div align="center">

**Спасибо за ваш вклад в развитие SayDeck!** 🙏

*Together we build amazing things* ✨

</div>
