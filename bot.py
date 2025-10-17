import json
import aiohttp
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_URL = os.getenv("API_URL")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer(
        "Привет! Введи имя человека чтобы посмотреть его родословную."
    )

@dp.message()
async def handle_name(message: types.Message):
    name = message.text.strip()
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(API_URL.format(name=name)) as response:
                
                if response.status == 200:
                    data = await response.json()
                    formatted_json = json.dumps(data, ensure_ascii=False, indent=2)
                    await message.answer(f"Родословная {name}:\n```json\n{formatted_json}\n```", parse_mode='Markdown')
                
                elif response.status == 404:
                    await message.answer(f"Человека с именем '{name}' не существует.")
                
                else:
                    await message.answer("Ошибка сервера.")
    
    except Exception as e:
        await message.answer("Ошибка API.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())