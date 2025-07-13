import asyncio

from aiogram.client.default import DefaultBotProperties

from utils.config import TOKEN
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from loguru import logger
from handlers.register_routers import register_all_handlers
from handlers.users import router_users
from handlers.admin import router_admin
from db.database import Database


"""Настраиваем логи"""
logger.add('DEBUG.log', format="{time} {level} {message}", filter="my_module", level="ERROR")
logger.add('DEBUG.log', format="{time} {level} {message}", filter="my_module", level="INFO")
logger.add('DEBUG.log', format="{time} {level} {message}", filter="my_module", level="DEBUG")

# Initialize bot
bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


async def main() -> None:
    # Initialize database
    db = Database()
    
    dp = Dispatcher()
    
    # Register all handlers with database instance
    await register_all_handlers(db)
    
    # Include routers
    dp.include_router(router_users)
    dp.include_router(router_admin)
    
    logger.info("Bot started")
    try:
        await dp.start_polling(bot)
    finally:
        # Close database connection when bot stops
        db.close()
        logger.info("Bot stopped")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")
