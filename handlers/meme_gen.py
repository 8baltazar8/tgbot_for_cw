import asyncio
import logging
import io
import requests
import aiohttp
import asyncio
import json
import base64
from keyboards.rate import make_row_keyboard
from aiogram import Bot, Dispatcher, types, F, Router
from aiogram.filters.command import Command
from aiogram.filters.text import Text
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile, BufferedInputFile, ReplyKeyboardRemove, Message, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from settings import config
from . import schemas
import pydantic
from pydantic_aiohttp import Client


router = Router()


class Grade_meme(StatesGroup):
    meme_grade = State()


@router.message(Command("test_rate"))
async def reply_builder(message: types.Message):
    await message.answer(
        "Rate from 1 to 10 how funny the meme is:",
        reply_markup=make_row_keyboard(),
    )

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Hey! Sand me pic and I will generate meme for you!")

@router.message(F.photo)
async def download_photo(message: types.Message, bot: Bot, state: FSMContext):
    image_in_bytes_io = io.BytesIO()
    await bot.download(
        message.photo[-1],
        destination=image_in_bytes_io
    )

    resp = schemas.Meme_generated.parse_obj(requests.post('http://127.0.0.1:8000/meme_gen', data=image_in_bytes_io).json())
    await message.answer_photo(
                BufferedInputFile(
                    base64.b64decode(resp.content),
                    filename="image.jpg"
                ),
                caption="Your meme"
            )
    #await reply_builder("Your meme")
    await state.update_data(id=str(resp.id))
    await message.answer(
        "Rate from 1 to 10 how funny the meme is:",
        reply_markup=make_row_keyboard(),
    )
    await state.set_state(Grade_meme.meme_grade)

@router.message(Grade_meme.meme_grade, F.text.in_([str(x) for x in list(range(1, 11))]))
async def graded(message: Message, state: FSMContext):
    await state.update_data(grade=message.text.lower())
    user_data = await state.get_data()
    await message.answer(
        text="Thank you! Your opinion is important to us",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.clear()
    requests.put('http://127.0.0.1:8000/rate_meme', schemas.User_rate.parse_obj(user_data).json())
    #print(schemas.User_rate.parse_obj(user_data).json())


@router.message(Grade_meme.meme_grade)
async def graded_incorrectly(message: Message):
    await message.answer(
        "You have to rate the meme from 1 to 10 !\n\nPlease try again:",
        reply_markup=make_row_keyboard(),
    )

@router.message(F.animation)
async def echo_gif(message: types.Message):
    await message.reply_animation(message.animation.file_id, caption="Only pics!")
