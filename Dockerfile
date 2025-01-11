# Используем базовый образ Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем зависимости для создания виртуального окружения и компиляции пакетов
RUN apt-get update && apt-get install -y \
    python3-venv \
    gcc \
    libffi-dev \
    libssl-dev \
    make \
    && apt-get clean

# Копируем файлы requirements.txt в рабочую директорию
COPY requirements.txt .

# Создаем виртуальное окружение и устанавливаем зависимости
RUN python3 -m venv /opt/venv && \
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
