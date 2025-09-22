from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.types import Update
from aiogram import Router
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
import os
from dotenv import load_dotenv
from aiogram.enums import ChatAction
import asyncio
from openai import AsyncOpenAI
import httpx , openai
print("httpx version:", httpx.__version__)
print("openai version:", openai.__version__)

user_dialogs = {}
load_dotenv()

OPENAI_API_KEY = os.getenv("API_KEY")
openai.api_key = OPENAI_API_KEY


async def create_response(text: str):
    res = openai.chat.completions.create(
        model="gpt-5-nano-2025-08-07",
        messages=[{"role": "user" , "content": text}, { "role": "developer" , "content": "Ты — AI-менеджер по продаже квартир компании Dreamland в Узбекистане. Твоя задача — помогать клиентам подобрать квартиру. В начале общения уточняй у клиента его требования: количество комнат, площадь (кв.м), бюджет, этаж, дополнительные пожелания. Запоминай все ответы клиента. Когда клиент говорит «всё», «ищи», «найди» или аналогичное — фильтруй из базы только те квартиры, которые соответствуют условиям. Сохраняй ID подходящих квартир, чтобы потом передать их менеджеру. Отвечай просто и понятно, как настоящий агент по недвижимости."}],
    )
    return res.choices[0].message.content

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Привет! Я бот Dreamland. Расскажите, какую квартиру ищете? 🏠")


@router.message()
async def handle_message(message: Message):
    user_id = message.from_user.id

    # Инициализация списка
    if user_id not in user_dialogs:
        user_dialogs[user_id] = []

    # Если клиент отправил контакт
    if message.contact:
        phone = message.contact.phone_number
        dialog_text = "\n".join(user_dialogs[user_id])

        text_for_manager = (
            f"📞 Новый клиент!\n"
            f"Номер: {phone}\n\n"
            f"Диалог:\n{dialog_text}"
        )
        
        await bot.send_chat_action(message.chat.id, ChatAction.TYPING)

        await message.bot.send_message(GROUP_ID, text_for_manager)

        await message.answer("✅ Ваша заявка принята! С вами скоро свяжется менеджер.")

        # очистка истории
        user_dialogs[user_id] = []
        return

    # Если клиент отправил номер вручную
    if message.text and message.text.startswith("+"):
        phone = message.text
        dialog_text = "\n".join(user_dialogs[user_id])

        text_for_manager = (
            f"📞 Новый клиент!\n"
            f"Номер: {phone}\n\n"
            f"Диалог:\n{dialog_text}"
        )

        await message.bot.send_message(GROUP_ID, text_for_manager)
        user_dialogs[user_id] = []
        return

    # Если обычный текст → отправляем в GPT
    if message.text:
        user_dialogs[user_id].append(message.text)

        await message.bot.send_chat_action(message.chat.id, ChatAction.TYPING)
        await asyncio.sleep(1)

        try:
            response = await create_response(message.text)
            await message.answer(response)
        except Exception as e:
            await message.answer(f"Ошибка при генерации ответа: {e}")
bot = Bot(token=os.getenv('TOKEN'))
GROUP_ID = os.getenv('GROUP_ID')

dp = Dispatcher()
dp.include_router(router)
dp.bot_group_id = GROUP_ID

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
