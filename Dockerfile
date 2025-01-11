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
    build-essential \
    wget \
    git \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    && apt-get clean

# Создаем виртуальное окружение
RUN python3 -m venv /opt/venv

# Обновляем pip в виртуальном окружении
RUN /opt/venv/bin/pip install --upgrade pip

# Устанавливаем Cython перед установкой зависимостей
RUN /opt/venv/bin/pip install cython

# Копируем файлы requirements.txt в рабочую директорию
COPY requirements.txt .

# Выводим версию pip для диагностики
RUN /opt/venv/bin/pip --version

# Выводим содержимое requirements.txt для диагностики
RUN cat requirements.txt

# Устанавливаем зависимости из requirements.txt
RUN /opt/venv/bin/pip install -r requirements.txt --no-cache-dir

# Устанавливаем numpy, blis, thinc и spaCy с совместимыми версиями
RUN /opt/venv/bin/pip install numpy==1.21.0 blis==0.7.4 thinc==8.0.15 spacy==3.1.0 --no-cache-dir

# Копируем остальные файлы проекта в рабочую директорию
COPY . .

# Запускаем скрипт для загрузки модели spaCy
RUN /opt/venv/bin/python setup.py

# Устанавливаем переменные окружения
ENV PATH="/opt/venv/bin:$PATH"

# Указываем команду для запуска приложения
CMD ["python", "bot.py"]
