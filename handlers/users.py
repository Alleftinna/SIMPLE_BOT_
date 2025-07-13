


from aiogram import Router, Bot
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

router_users = Router()

image_id = "AgACAgIAAxkBAAOVaHQjB5ZbiMXKiwqctevgbvlF-QQAAgv3MRs8dKBLNvr_enc5b90BAAMCAAN5AAM2BA"

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
    await bot.send_photo(message.chat.id, image_id, caption=welcome_text, reply_markup=keyboard)


# async def get_image_info(message: Message, bot: Bot, state: FSMContext, db=None):
#     """
#     Get image info
#     :param db: Database instance
#     :param state: FSM context
#     :param message: Message instance
#     :param bot: Bot instance
#     :return: None
#     """
    
#     image_id = message.photo[-1].file_id
#     image_info = await bot.get_file(image_id)
#     image_url = image_info.file_path
#     image_url = f"https://api.telegram.org/file/bot{bot.token}/{image_url}"
#     image_info = await bot.get_file(image_id)
#     image_url = image_info.file_path
#     image_url = f"https://api.telegram.org/file/bot{bot.token}/{image_url}"
    
#     await message.answer(image_id)







