from aiogram import Router, types, F, Bot
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart

# Подключаем роутер
router = Router()

# ID группы менеджеров
GROUP_ID = "GROUP_ID"  # замените на свой group_id

# Хранилище диалогов
user_dialogs = {}

# Функция кнопки для отправки номера
def get_contact_kb():
    kb = [[KeyboardButton(text="📞 Отправить номер", request_contact=True)]]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

# Старт
@router.message(CommandStart())
async def start(message: types.Message):
    await message.answer(
        "Привет! Нажмите кнопку, чтобы отправить номер телефона:",
        reply_markup=get_contact_kb()
    )

# Ловим обычные сообщения и сохраняем их в историю
@router.message(F.text)
async def save_message(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_dialogs:
        user_dialogs[user_id] = []
    user_dialogs[user_id].append(message.text)

# Ловим контакт
@router.message(F.contact)
async def process_contact(message: types.Message, bot: Bot):
    user_id = message.from_user.id
    phone = message.contact.phone_number
    name = message.from_user.full_name

    # Собираем диалог
    dialog = "\n".join(user_dialogs.get(user_id, [])) or "Диалог пуст"

    # Отправляем менеджерам
    text = (
        f"📞 Новый клиент!\n"
        f"Имя: {name}\n"
        f"Номер: {phone}\n\n"
        f"💬 Диалог:\n{dialog}"
    )
    await bot.send_message(GROUP_ID, text)

    # Подтверждаем клиенту
    await message.answer("Спасибо! Ваш номер и диалог переданы менеджеру ✅")

    # Чистим историю
    user_dialogs.pop(user_id, None)