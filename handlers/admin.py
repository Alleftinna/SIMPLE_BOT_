from aiogram import Router, Bot, F
from aiogram.types import Message, FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
import os
import io
from datetime import datetime, timedelta

from utils.isadmin import IsAdmin
from utils.states import AdminSettings

router_admin = Router()

# Apply admin filter to all handlers in this router
router_admin.message.filter(IsAdmin())

# Список команд админ-панели для многократного использования
ADMIN_COMMANDS = [
    "/admin - Показать это меню",
    "/stats_users - Количество пользователей",
    "/stats_buttons - Статистика нажатий кнопок",
    "/stats_chart - Графическая статистика нажатий",
    "/stats_daily - Ежедневная статистика",
    "/stats_active - Активные пользователи",
    "/set_welcome - Изменить приветственное сообщение",
    "/set_link - Изменить ссылку",
    "/set_link_text - Изменить текст кнопки-ссылки",
    "/view_welcome - Просмотреть текущее приветствие"
]

async def send_admin_panel(message: Message):
    """
    Отправляет панель администратора
    """
    response = "📊 Панель администратора:\n\n" + "\n".join(ADMIN_COMMANDS)
    await message.answer(response)

# Удаляем все декораторы, так как они регистрируются в register_routers.py
async def admin_panel(message: Message):
    """
    Show admin panel with available commands
    """
    await send_admin_panel(message)

async def get_user_count(message: Message, bot: Bot, db=None):
    """
    Get the total number of users in the database
    :param message: Message instance
    :param bot: Bot instance
    :param db: Database instance
    :return: None
    """
    if db:
        user_count = db.get_user_count()
        await message.reply(f"Всего пользователей в базе: {user_count}")
    else:
        await message.reply("База данных не инициализирована.")
    
    # Показываем админ-панель
    await send_admin_panel(message)

async def get_button_stats(message: Message, bot: Bot, db=None):
    """
    Get statistics on button clicks
    :param message: Message instance
    :param bot: Bot instance
    :param db: Database instance
    :return: None
    """
    if not db:
        await message.reply("База данных не инициализирована.")
        await send_admin_panel(message)
        return
        
    stats = db.get_button_stats()
    if not stats:
        await message.reply("Нет данных о нажатиях кнопок.")
        await send_admin_panel(message)
        return
    
    result = "Статистика нажатий кнопок:\n\n"
    for button_name, count in stats:
        result += f"{button_name}: {count} раз\n"
    
    await message.reply(result)
    
    # Показываем админ-панель
    await send_admin_panel(message)

async def get_button_stats_chart(message: Message, bot: Bot, db=None):
    """
    Get statistics on button clicks as a text-based chart
    :param message: Message instance
    :param bot: Bot instance
    :param db: Database instance
    :return: None
    """
    if not db:
        await message.reply("База данных не инициализирована.")
        await send_admin_panel(message)
        return
        
    stats = db.get_button_stats()
    if not stats:
        await message.reply("Нет данных о нажатиях кнопок.")
        await send_admin_panel(message)
        return
    
    # Find the maximum count for scaling
    max_count = max([count for _, count in stats])
    
    # Create a text-based chart
    result = "📊 Статистика нажатий кнопок (график):\n\n"
    
    # Limit to top 10 buttons for readability
    top_stats = stats[:10]
    
    # Calculate the maximum width of button names for alignment
    max_name_width = max([len(button_name) for button_name, _ in top_stats])
    
    for button_name, count in top_stats:
        # Scale the bar to a maximum of 20 characters
        bar_length = int((count / max_count) * 20)
        bar = "█" * bar_length
        
        # Format with proper alignment
        result += f"{button_name.ljust(max_name_width)} | {bar} {count}\n"
    
    await message.reply(result)
    
    # Показываем админ-панель
    await send_admin_panel(message)

async def get_daily_stats(message: Message, bot: Bot, db=None):
    """
    Get daily statistics on button clicks for the last 7 days
    :param message: Message instance
    :param bot: Bot instance
    :param db: Database instance
    :return: None
    """
    if not db:
        await message.reply("База данных не инициализирована.")
        await send_admin_panel(message)
        return
    
    # Get daily stats for the last 7 days
    daily_stats = db.get_daily_stats()
    
    if not daily_stats:
        await message.reply("Нет данных о ежедневной активности.")
        await send_admin_panel(message)
        return
    
    result = "📅 Статистика активности за последние 7 дней:\n\n"
    
    for date_str, count in daily_stats:
        # Create a simple bar chart
        bar_length = int(count / 5) + 1  # Scale: 1 block per 5 clicks, minimum 1
        bar = "█" * min(bar_length, 20)  # Cap at 20 blocks
        
        result += f"{date_str}: {bar} {count}\n"
    
    await message.reply(result)
    
    # Показываем админ-панель
    await send_admin_panel(message)

async def get_active_users(message: Message, bot: Bot, db=None):
    """
    Get list of most active users
    :param message: Message instance
    :param bot: Bot instance
    :param db: Database instance
    :return: None
    """
    if not db:
        await message.reply("База данных не инициализирована.")
        await send_admin_panel(message)
        return
    
    active_users = db.get_most_active_users(limit=10)
    
    if not active_users:
        await message.reply("Нет данных об активных пользователях.")
        await send_admin_panel(message)
        return
    
    result = "👥 Самые активные пользователи:\n\n"
    
    for i, (user_id, username, first_name, last_name, click_count) in enumerate(active_users, 1):
        user_display = username or f"{first_name} {last_name}".strip() or f"ID: {user_id}"
        result += f"{i}. {user_display}: {click_count} действий\n"
    
    await message.reply(result)
    
    # Показываем админ-панель
    await send_admin_panel(message)

async def view_welcome(message: Message, bot: Bot, db=None):
    """
    View current welcome message and link
    """
    if not db:
        await message.reply("База данных не инициализирована.")
        await send_admin_panel(message)
        return
    
    welcome_text = db.get_welcome_message()
    welcome_link = db.get_welcome_link()
    welcome_link_text = db.get_welcome_link_text()
    
    # Create inline keyboard with link button to preview how it looks
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=welcome_link_text, url=welcome_link)]
        ]
    )
    
    info_text = (
        f"📋 Текущие настройки приветствия:\n\n"
        f"Текст сообщения:\n{welcome_text}\n\n"
        f"Текст кнопки: {welcome_link_text}\n"
        f"Ссылка: {welcome_link}\n\n"
        f"👇 Предварительный просмотр:"
    )
    
    await message.reply(info_text)
    await message.answer(welcome_text, reply_markup=keyboard)
    
    # Показываем админ-панель
    await send_admin_panel(message)

async def set_welcome_cmd(message: Message, state: FSMContext):
    """
    Set new welcome message
    """
    await message.reply("Пожалуйста, введите новый текст приветственного сообщения:")
    await state.set_state(AdminSettings.WAITING_FOR_WELCOME_TEXT)

async def set_link_cmd(message: Message, state: FSMContext):
    """
    Set new welcome link
    """
    await message.reply("Пожалуйста, введите новую ссылку (в формате https://example.com):")
    await state.set_state(AdminSettings.WAITING_FOR_WELCOME_LINK)

async def set_link_text_cmd(message: Message, state: FSMContext):
    """
    Set new link button text
    """
    await message.reply("Пожалуйста, введите новый текст для кнопки-ссылки:")
    await state.set_state(AdminSettings.WAITING_FOR_LINK_TEXT)

async def process_welcome_text(message: Message, state: FSMContext, db=None):
    """
    Process new welcome text
    """
    if not db:
        await message.reply("База данных не инициализирована.")
        await state.clear()
        await send_admin_panel(message)
        return
    
    new_text = message.text
    db.update_setting("welcome_text", new_text)
    
    await message.reply(f"✅ Текст приветствия успешно обновлен!\n\nНовый текст:\n{new_text}")
    await state.clear()
    
    # Показываем админ-панель
    await send_admin_panel(message)

async def process_welcome_link(message: Message, state: FSMContext, db=None):
    """
    Process new welcome link
    """
    if not db:
        await message.reply("База данных не инициализирована.")
        await state.clear()
        await send_admin_panel(message)
        return
    
    new_link = message.text
    
    # Simple validation for URL
    if not (new_link.startswith("http://") or new_link.startswith("https://")):
        await message.reply("❌ Ссылка должна начинаться с http:// или https://\nПожалуйста, попробуйте снова:")
        return
    
    db.update_setting("welcome_link", new_link)
    
    await message.reply(f"✅ Ссылка успешно обновлена!\n\nНовая ссылка: {new_link}")
    await state.clear()
    
    # Показываем админ-панель
    await send_admin_panel(message)

async def process_link_text(message: Message, state: FSMContext, db=None):
    """
    Process new link button text
    """
    if not db:
        await message.reply("База данных не инициализирована.")
        await state.clear()
        await send_admin_panel(message)
        return
    
    new_text = message.text
    db.update_setting("welcome_link_text", new_text)
    
    await message.reply(f"✅ Текст кнопки успешно обновлен!\n\nНовый текст: {new_text}")
    await state.clear()
    
    # Показываем админ-панель
    await send_admin_panel(message)
