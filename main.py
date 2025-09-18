import asyncio
from aiogram import Bot, Dispatcher
from aiohttp import web
import os

from handlers import router

async def main():
    bot = Bot(token='5046427784:AAE6GJrPNBEZV5sfRbCftJXAjt7jhRSz8bY')
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)
app = web.Application()

if __name__ == '__main__':
    try:
        asyncio.run(main())
        web.run_app(app, host="0.0.0.0", port=int(os.getenv("PORT", 8080)))
    except KeyboardInterrupt:
        print('Exit')
