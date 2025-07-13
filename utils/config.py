from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())
import os
from loguru import logger

# Bot name: @XIII_HeadNeckCongress_Bot
TOKEN = os.environ.get('BOT_TOKEN')
ADMIN_IDS = os.environ.get('ADMIN_IDS', '').split(',')

# Логируем для отладки
logger.info(f"Loaded admin IDs: {ADMIN_IDS}")