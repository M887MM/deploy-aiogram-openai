from aiogram import Router
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from generator import create_response

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