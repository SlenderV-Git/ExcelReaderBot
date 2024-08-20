from io import BytesIO
from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, Command, StateFilter

from src.services.save_objects import convert_file_to_db
from src.state import DocumentTracker

rt = Router()

@rt.message(StateFilter(DocumentTracker.get_document), F.document)
async def document_process(message : Message, state : FSMContext):
    print(message.from_user, message.from_user.username)
    file = await message.bot.download(message.document.file_id, BytesIO())
    await state.clear()
    try:
        convert_file_to_db(file)
    except:
        await message.answer("Ошибка чтения файла")
    else:
        await message.answer("Файл успешно конвертирован в базу данных")
    