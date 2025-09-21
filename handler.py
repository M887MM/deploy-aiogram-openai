from aiogram import Router
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.fsm.context import FSMContext
from generator import create_response
import re

router = Router()

# ---------- клавиатура с кнопкой "Поделиться контактом" ----------
contact_button = KeyboardButton(text="Отправить контакт", request_contact=True)
keyboard = ReplyKeyboardMarkup(
    keyboard=[[contact_button]],
    resize_keyboard=True
)

# ---------- /start ----------
@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        'Добро пожаловать в гпт5! Отправь свой номер телефона или нажми кнопку ниже, чтобы поделиться контактом.',
        reply_markup=keyboard
    )

# ---------- обработка контакта через кнопку ----------
@router.message(lambda message: message.contact is not None)
async def contact_handler(message: Message):
    phone = message.contact.phone_number
    user_name = message.from_user.full_name
    await message.answer(f"Спасибо! Мы получили твой номер: {phone}")

    # отправка контакта в группу
    try:
        await message.bot.send_message(
            chat_id=message.bot.dp.bot_group_id,
            text=f"Новый контакт:\nПользователь: {user_name}\nНомер: {phone}"
        )
    except Exception as e:
        print(f"Ошибка отправки контакта в группу: {e}")

# ---------- обработка ручного ввода номера и GPT ----------
@router.message()
async def manual_phone_handler(message: Message, state: FSMContext):
    phone = message.text.strip()

    # проверка номера
    pattern = re.compile(r"^(?:\+?998)?(\d{9})$")
    match = pattern.match(phone)

    if match:
        formatted_phone = "+998" + match.group(1)
        await message.answer(f"Спасибо! Мы сохранили твой номер: {formatted_phone}")

        # отправка номера в группу
        try:
            await message.bot.send_message(
                chat_id=message.bot.dp.bot_group_id,
                text=f"Новый контакт:\nПользователь: {message.from_user.full_name}\nНомер: {formatted_phone}"
            )
        except Exception as e:
            print(f"Ошибка отправки контакта в группу: {e}")
    else:
        await message.chat.send_action(action="typing")
        # если это не номер, генерируем ответ через GPT
        await state.set_state('generating')
        try:
            response = await create_response(message.text)
            await message.answer(response)

            # отправляем текст диалога в группу
            try:
                await message.bot.send_message(
                    chat_id=message.bot.dp.bot_group_id,
                    text=f"Диалог пользователя {message.from_user.full_name}:\n{message.text}\nОтвет GPT:\n{response}"
                )
            except Exception as e:
                print(f"Ошибка отправки диалога в группу: {e}")

        except Exception as e:
            await message.answer(f'Произошла ошибка: {e}')
        finally:
            await state.clear()

# ---------- обработка генерации сообщений ----------
@router.message(StateFilter('generating'))
async def wait_response(message: Message):
    await message.answer('Ожидайте! Идёт генерация ответа...')