
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.types import Update
from aiogram import Router
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
import httpx , openai
print("httpx version:", httpx.__version__)
print("openai version:", openai.__version__)


load_dotenv()

OPENAI_API_KEY = os.getenv("API_KEY")
openai.api_key = OPENAI_API_KEY


async def create_response(text: str):
    res = openai.chat.completions.create(
        model="gpt-5-nano-2025-08-07",
        messages=[{"role": "user" , "content": text}],
    )
    return res.choices[0].message.content

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Добро пожаловать в гпт5!')


@router.message(StateFilter('generating'))
async def wait_response(message: Message):
    await message.answer('Ожидайте! Идёт генерация ответа...')


@router.message()
async def generate_answer(message: Message, state: FSMContext):
    await state.set_state('generating')

    try:
        response = await create_response(message.text)
    except Exception as e:
        await message.answer(f'Произошла ошибка: {e}')
    else:
        await message.answer(response)
    finally:
        await state.clear()

bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher()
dp.include_router(router)

async def handle(request):
    data = await request.json()
    update = Update.model_validate(data)
    await dp.feed_update(bot, update)
    return web.Response()

app = web.Application()
app.router.add_post("/webhook", handle)

async def on_startup(app):
    await bot.set_webhook(f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/webhook")

app.on_startup.append(on_startup)

if __name__ == "__main__":
    web.run_app(app, host="0.0.0.0", port=int(os.getenv("PORT", 8080)))
