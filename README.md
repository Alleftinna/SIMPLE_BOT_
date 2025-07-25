# Simple Telegram Bot

Простой Telegram бот с функциями приветствия, кнопкой-ссылкой и административной панелью.

## Функции

- Приветственное сообщение с кнопкой-ссылкой при команде /start
- Админ-панель для управления содержимым бота
- Сбор и отображение статистики по пользователям и действиям
- Хранение данных в SQLite

## Установка

1. Клонируйте репозиторий
2. Установите зависимости:
```bash
pip install -r requirements.txt
```
3. Создайте файл .env со следующим содержимым:
```
BOT_TOKEN=your_telegram_bot_token_here
ADMIN_IDS=123456789,987654321
```
Замените `your_telegram_bot_token_here` на токен вашего бота от @BotFather, а `123456789,987654321` на ID администраторов (через запятую).

## Запуск

```bash
python main.py
```

Или с использованием Docker:

```bash
docker compose up -d
```

## Команды

### Пользовательские команды
- `/start` - Запуск бота, показ приветственного сообщения с кнопкой-ссылкой

### Админ-команды
- `/admin` - Показать панель администратора
- `/stats_users` - Количество пользователей
- `/stats_buttons` - Статистика нажатий кнопок
- `/stats_chart` - Графическая статистика нажатий
- `/stats_daily` - Ежедневная статистика
- `/stats_active` - Активные пользователи
- `/set_welcome` - Изменить приветственное сообщение
- `/set_link` - Изменить ссылку
- `/set_link_text` - Изменить текст кнопки-ссылки
- `/view_welcome` - Просмотреть текущее приветствие 