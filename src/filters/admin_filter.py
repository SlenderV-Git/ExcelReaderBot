from typing import Any
from aiogram.filters import BaseFilter
from aiogram.types import Message
from src.services.manager import list_id_managers

from src.core.settings import get_settings

class IsAdmin(BaseFilter):
    async def __call__(self, message : Message) -> Any:
        return message.from_user.id in get_settings().ADMIN_ID or message.from_user.id in list_id_managers()