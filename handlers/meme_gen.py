import asyncio
import logging
import io
import requests
import aiohttp
import asyncio
from keyboards.rate import make_row_keyboard
from aiogram import Bot, Dispatcher, types, F, Router
from aiogram.filters.command import Command
from aiogram.filters.text import Text
from aiogram.types import FSInputFile, BufferedInputFile, ReplyKeyboardRemove, Message, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from settings import config



router = Router()


@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Hey! Sand me pic and I will generate meme for you!")

@router.message(F.photo)
async def download_photo(message: types.Message, bot: Bot):
    image_in_bytes_io = io.BytesIO()
    await bot.download(
        message.photo[-1],
        destination=image_in_bytes_io
    )

    async with aiohttp.ClientSession() as session:
        async with session.post('http://127.0.0.1:8000/meme_gen', data=image_in_bytes_io) as resp:
            print(resp.status)
            id_to_rate = resp.headers['X-Meme-id']
            lol = await resp.read()

        await message.answer_photo(
                BufferedInputFile(
                    lol,
                    filename="image.jpg"
                ),
                caption="Your meme"
            )

@router.message(Command("test_rate"))
async def reply_builder(message: types.Message):
    await message.answer(
        "Rate from 1 to 10 how funny the meme is:",
        reply_markup=make_row_keyboard(),
    )


#class Chose_Rate(StatesGroup):
    #rate: State()






@router.message(F.animation)
async def echo_gif(message: types.Message):
    await message.reply_animation(message.animation.file_id, caption="Only pics!")#
