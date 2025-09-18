from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message


router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Добро пожаловать!')


@router.message()
async def echo(message: Message):
    await message.send_copy(chat_id=message.from_user.id)