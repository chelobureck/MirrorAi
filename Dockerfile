# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта
COPY . .

# Устанавливаем зависимости
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Открываем порт
EXPOSE 8000

# Команда запуска uvicorn с поддержкой переменной PORT (по умолчанию 8000)
CMD [CMD-SHELL,python -c "import sys,urllib.request; \ resp=urllib.request.urlopen('http://localhost:8000/api/v1/health', timeout=5); \ sys.exit(0 if resp.status==200 else 1)"]
