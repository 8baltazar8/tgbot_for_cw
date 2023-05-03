import asyncio
import logging
import io
import requests
import aiohttp
import asyncio
from PIL import Image
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.types import FSInputFile, BufferedInputFile
from settings import config


logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.bot_token.get_secret_value())

dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Hey! Sand me pic and I will generate meme for you!")

@dp.message(F.animation)
async def echo_gif(message: types.Message):
    await message.reply_animation(message.animation.file_id, caption="Only pics!")

@dp.message(F.photo)
async def download_photo(message: types.Message, bot: Bot):
    image_in_bytes_io = io.BytesIO()
    await bot.download(
        message.photo[-1],
        destination=image_in_bytes_io
    )

    async with aiohttp.ClientSession() as session:
        async with session.post('http://127.0.0.1:8000/meme_gen', data=image_in_bytes_io) as resp:
            print(resp.status)
            lol = await resp.read()

        await message.answer_photo(
                BufferedInputFile(
                    lol,
                    filename="image.jpg"
                ),
                caption="Your meme"
            )


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
