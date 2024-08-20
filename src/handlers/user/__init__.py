from aiogram import Router

from .handlers import rt as user_rt


def get_user_rt():
    rt = Router()
    rt.include_router(user_rt)

    return rt