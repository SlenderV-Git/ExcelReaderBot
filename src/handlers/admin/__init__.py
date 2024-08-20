from aiogram import Router

from .manage_db import rt as manage_rt
from .see_info import rt as see_rt

from src.filters.admin_filter import IsAdmin

def get_admin_rt():
    rt = Router()
    '''rt.message.filter(IsAdmin())
    rt.callback_query.filter(IsAdmin())'''
    
    rt.include_router(manage_rt)
    rt.include_router(see_rt)
    
    return rt