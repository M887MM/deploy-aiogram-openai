import os
from dotenv import load_dotenv
import openai

load_dotenv()
openai.api_key = os.getenv('API_KEY')

async def create_response(text):
    res = await openai.chat.completions.create(
        model="gpt-5-nano-2025-08-07",
        messages=[
            {"role": "system", "content": (
                "Ты — опытный менеджер по продажам недвижимости. "
                "Отвечай **только на русском языке**. "
                "Твоя цель — помочь клиенту выбрать и приобрести квартиру. "
                "Общайся вежливо, уверенно и понятно. Задавай уточняющие вопросы, "
                "чтобы понять потребности клиента: бюджет, район, количество комнат, этаж, планировка и т.д. "
                "Предлагай подходящие варианты, подчеркивай их преимущества. "
                "Отвечай кратко, информативно. В конце разговора обязательно предложи записаться на просмотр квартиры или оставить контакт для связи."
            )},
            {"role": "user", "content": text}
        ]
    )
    return res.choices[0].message.content


