from typing import Union, Dict, Any

from aiogram.filters import BaseFilter
from aiogram.types import Message
from loguru import logger

from utils.config import ADMIN_IDS


class IsAdmin(BaseFilter):
    """
    Filter that checks if the user is an admin
    """
    async def __call__(self, message: Message) -> bool:
        user_id = message.from_user.id
        is_admin = str(user_id) in ADMIN_IDS
        
        if is_admin:
            logger.info(f"User {user_id} is recognized as admin")
        else:
            logger.info(f"User {user_id} is not an admin. Available admin IDs: {ADMIN_IDS}")
        
        return is_admin
