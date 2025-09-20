import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from handlers import router

load_dotenv()

async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token= os.getenv('TOKEN'))
    dp = Dispatcher()
    dp.include_router(router)  # Подключаем только один раз

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
