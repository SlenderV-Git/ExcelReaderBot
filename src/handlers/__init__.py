from aiogram import Router

from .admin import get_admin_rt
from .user import get_user_rt

def get_root_rt():
    rt = Router()
    
    rt.include_router(get_user_rt())
    rt.include_router(get_admin_rt())
    
    return rt