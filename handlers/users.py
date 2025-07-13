


from aiogram import Router, Bot
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

router_users = Router()

# Remove the decorator since we register this function manually in register_routers.py
async def on_start(message: Message, bot: Bot, state: FSMContext, db=None):
    """
    Main start handler
    :param db: Database instance
    :param state: FSM context
    :param message: Message instance
    :param bot: Bot instance
    :return: None
    """
    # Add user to database
    user = message.from_user
    db.add_user(user.id, user.username, user.first_name, user.last_name)
    
    # Record button click
    db.record_button_click(user.id, "start")
    
    # Get welcome message and link from database
    welcome_text = db.get_welcome_message()
    welcome_link = db.get_welcome_link()
    welcome_link_text = db.get_welcome_link_text()
    
    # Create inline keyboard with link button
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=welcome_link_text, url=welcome_link)]
        ]
    )
    
    # Send welcome message with link button
    await message.answer(welcome_text, reply_markup=keyboard)


