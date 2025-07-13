# Используем официальный образ Python
FROM python:3.10-slim

# Устанавливаем зависимости системы
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы requirements.txt и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы вашего проекта
COPY . .

# Устанавливаем переменные окружения для корректного выполнения бота
ENV PYTHONUNBUFFERED=1

# Команда для запуска вашего бота
CMD ["python", "main.py"]
