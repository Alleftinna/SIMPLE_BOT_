from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from functools import partial

from handlers.users import router_users, on_start
from handlers.admin import router_admin, get_user_count, get_button_stats, get_button_stats_chart
from handlers.admin import get_daily_stats, get_active_users, view_welcome, admin_panel
from handlers.admin import process_welcome_text, process_welcome_link, process_link_text
from handlers.admin import set_welcome_cmd, set_link_cmd, set_link_text_cmd
from utils.isadmin import IsAdmin
from utils.states import AdminSettings


async def register_users(db):
    """Register user handlers with database access"""
    # Inject database instance into handler function
    router_users.message.register(
        partial(on_start, db=db),
        Command("start")
    )
    # router_users.message.register(
    #     partial(get_image_info, db=db),
    #     F.photo
    # )

async def register_admin_handlers(db):
    """Register all admin handlers with database access"""
    # Регистрируем команды без базы данных
    router_admin.message.register(admin_panel, Command("admin"))
    router_admin.message.register(set_welcome_cmd, Command("set_welcome"))
    router_admin.message.register(set_link_cmd, Command("set_link"))
    router_admin.message.register(set_link_text_cmd, Command("set_link_text"))
    
    # Регистрируем функции с базой данных
    # Regular command handlers
    admin_commands = {
        "stats_users": get_user_count,
        "stats_buttons": get_button_stats,
        "stats_chart": get_button_stats_chart,
        "stats_daily": get_daily_stats,
        "stats_active": get_active_users,
        "view_welcome": view_welcome
    }
    
    # Register all admin command handlers
    for cmd, handler_func in admin_commands.items():
        router_admin.message.register(
            partial(handler_func, db=db),
            Command(cmd)
        )
    
    # State handlers
    state_handlers = {
        AdminSettings.WAITING_FOR_WELCOME_TEXT: process_welcome_text,
        AdminSettings.WAITING_FOR_WELCOME_LINK: process_welcome_link,
        AdminSettings.WAITING_FOR_LINK_TEXT: process_link_text
    }
    
    # Register all state handlers
    for state, handler_func in state_handlers.items():
        router_admin.message.register(
            partial(handler_func, db=db),
            state
        )


async def register_all_handlers(db):
    """Register all handlers with database access"""
    # Register user handlers
    await register_users(db)
    
    # Register admin handlers
    await register_admin_handlers(db)


