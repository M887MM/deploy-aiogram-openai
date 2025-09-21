import os
from dotenv import load_dotenv
import openai

load_dotenv()
openai.api_key = os.getenv('API_KEY')

async def create_response(text):
    system_text = (
        "Ты — опытный менеджер по продажам недвижимости.\n"
        "Ты должен отвечать только на русском языке, никогда не на украинском или любом другом языке.\n"
        "Твоя цель — помочь клиенту выбрать и приобрести квартиру.\n"
        "Общайся вежливо, уверенно и понятно.\n"
        "Задавай уточняющие вопросы, чтобы понять потребности клиента: бюджет, район, количество комнат, этаж, планировка и т.д.\n"
        "Предлагай подходящие варианты, подчеркивай их преимущества.\n"
        "Отвечай кратко, информативно. В конце разговора обязательно предложи записаться на просмотр квартиры или оставить контакт для связи."
    )

    res = await openai.chat.completions.create(
        model="gpt-5-nano-2025-08-07",
        messages=[
            {"role": "system", "content": system_text},
            {"role": "user", "content": text}
        ]
    )
    return res.choices[0].message.content



