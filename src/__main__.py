import asyncio
from aiogram import Bot, Dispatcher

from src.core.settings import get_settings
from src.handlers import get_root_rt

async def main():
    bot = Bot(token=get_settings().BOT_TOKEN)
    print(await bot.get_me())
    
    dp = Dispatcher()
    dp.include_router(get_root_rt())

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())