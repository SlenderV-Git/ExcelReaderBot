from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart

from src.keyboards.kb_admin import get_start_kb
from src.dialogs.ru_dialogs import *
from src.keyboards.reply_kb import get_reply_kb

rt = Router()

@rt.message(CommandStart())
async def process_start(message : Message):
    print(message.from_user, message.from_user.username)
    await message.answer(START_REPLY, reply_markup=get_reply_kb())
    await message.answer(START, reply_markup= get_start_kb(message))
    
    
@rt.message(F.text == "Меню")
async def process_reply(message : Message):
    print(message.text)
    await message.answer(START, reply_markup= get_start_kb(message))
    