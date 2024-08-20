from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

def get_reply_kb():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Меню")]], resize_keyboard= True
    )