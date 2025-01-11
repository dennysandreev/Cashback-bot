# Используем базовый образ Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы requirements.txt в рабочую директорию
COPY requirements.txt .

# Устанавливаем зависимости
RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --upgrade pip && \
    /opt/venv/bin/pip install -r requirements.txt

# Копируем остальные файлы проекта в рабочую директорию
COPY . .

# Запускаем скрипт для загрузки модели spaCy
RUN /opt/venv/bin/python setup.py

# Устанавливаем переменные окружения
ENV PATH="/opt/venv/bin:$PATH"

# Указываем команду для запуска приложения
CMD ["python", "bot.py"]
