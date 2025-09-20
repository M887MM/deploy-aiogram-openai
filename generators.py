import os
from dotenv import load_dotenv
from openai import AsyncOpenAI

# Загружаем переменные из .env
load_dotenv()

# Берём ключ из переменных окружения
OPENAI_API_KEY = os.getenv('API_KEY')
client = AsyncOpenAI(api_key=OPENAI_API_KEY)


async def create_response(text: str):
    response = await client.responses.create(
        model="gpt-5",
        input=text
    )
    return response.output_text
