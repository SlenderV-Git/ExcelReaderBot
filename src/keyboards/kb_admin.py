from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import Message

from src.core.settings import get_settings

from src.services.manager import list_id_managers
from src.cbdata import AdminMenuCallbackFactory, PaginationCallbackFacory

TEST = False

def get_start_kb(message : Message):
    builder = InlineKeyboardBuilder()
    if message.from_user.id in get_settings().ADMIN_ID or message.from_user.id in list_id_managers() or TEST:
        builder.button(
                text="Ввести ИНН",
                callback_data=AdminMenuCallbackFactory(action="send_inn")
            )
        builder.button(
                text="Поиск по имени продукта",
                callback_data=AdminMenuCallbackFactory(action="part_name")
            )
    if message.from_user.id in get_settings().ADMIN_ID or TEST:
        builder.button(
                text="Отправить документ",
                callback_data=AdminMenuCallbackFactory(action="send_doc")
            )
        builder.button(
            text="Добавить менеджера",
            callback_data=AdminMenuCallbackFactory(action="add_manager")
        )
        builder.button(
            text="Удалить менеджера",
            callback_data=AdminMenuCallbackFactory(action="delete_manager")
        )
        builder.button(
            text="Показать всех менеджеров",
            callback_data=AdminMenuCallbackFactory(action="list_manager")
        )
    return builder.adjust(1).as_markup()

def get_pagination_kb(type_product : str, data : str | int, pag_len : int, id : int | str, offset : int = 0):
    builder = InlineKeyboardBuilder()
    builder.button(
        text= "<",
        callback_data=PaginationCallbackFacory(type_pagination=type_product, data=data, offset=offset -1 if offset - 1 >= 0 else 0)
    )
    builder.button(
        text= "Выбрать",
        callback_data=PaginationCallbackFacory(type_pagination=f"{type_product}_select", data=id, offset=offset)
    )
    builder.button(
        text= ">",
        callback_data=PaginationCallbackFacory(type_pagination=type_product, data = data, offset=offset + 1 if offset + 1 <= pag_len else pag_len)
    )
    return builder.adjust(3).as_markup()