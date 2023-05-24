import asyncio
import logging
import io
import requests
import aiohttp
import asyncio
import json
import base64
from keyboards.rate import make_row_keyboard
from keyboards.yes_no_sug_meme import yes_no_keys
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



@router.message(Command(commands=["cancel"]))
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Canceled",
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(F.photo)
async def download_photo(message: types.Message, bot: Bot, state: FSMContext):
    image_in_bytes_io = io.BytesIO()
    await bot.download(
        message.photo[-1],
        destination=image_in_bytes_io
    )
    raw_resp = requests.post('http://127.0.0.1:8000/meme_gen', data=image_in_bytes_io)
    resp = schemas.Meme_generated.parse_obj(raw_resp.json())
    if raw_resp.status_code == 404:
        await message.answer("404 wtf")

    if resp.id == 404:
        await message.answer_photo(
                BufferedInputFile(
                    base64.b64decode(resp.content),
                    filename="image.jpg"
                ),
                caption="<i>It seems that all the technical potential of mankind could not find a suitable text for your picture...</i>"
            )
        await message.answer(
            "Want to add text to images in this category?\n\n"
            "<i>We do not guarantee that the text you suggest will be used with this image next time.</i>",
            reply_markup=yes_no_keys(),
        )
        await state.set_state(schemas.Sug_meme_404.start_meme_sug)
    else:
        await message.answer_photo(
                BufferedInputFile(
                    base64.b64decode(resp.content),
                    filename="image.jpg"
                ),
                caption="Your meme"
            )
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



@router.message(schemas.Sug_meme_404.start_meme_sug, F.text == "Yes")
async def suggest_a_mem_404_yes(message: types.Message, state: FSMContext):
    await message.answer("We would love to hear your text for the meme!\n\n"
                         "Please enter the general category of your meme now.\n"
                         "It should be one word in English (for example, 'cat' or 'Dog').\n\n"
                         "<b>Numbers and special characters are not allowed. Only letters...</b>",
                         reply_markup=ReplyKeyboardRemove())
    await state.set_state(schemas.Sug_meme.meme_category)


@router.message(schemas.Sug_meme_404.start_meme_sug, F.text.lower() == "no")
async def suggest_a_mem_404_no(message: types.Message, state: FSMContext):
    await message.answer("Okay\n\n"
                         "<i>Have a nice day!</i>",
                         reply_markup=ReplyKeyboardRemove())
    await state.clear()
