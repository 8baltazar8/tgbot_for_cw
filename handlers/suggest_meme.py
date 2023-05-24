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
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from settings import config
from . import schemas
from .filters.correct_meme import Correct_category, Correct_meme_text
import pydantic
from pydantic_aiohttp import Client


router = Router()


@router.message(Command("suggest_a_meme"))
async def suggest_a_meme(message: types.Message, state: FSMContext):
    await message.answer("We would love to hear your text for the meme!\n\n"
                         "Please enter the general category of your meme now.\n"
                         "It should be one word in English (for example, 'cat' or 'Dog').\n\n"
                         "<b>Numbers and special characters are not allowed. Only letters...</b>")
    await state.set_state(schemas.Sug_meme.meme_category)



@router.message(schemas.Sug_meme.meme_category, F.text, Correct_category())
async def category_cor(message: Message, state: FSMContext):
    await state.update_data(category=message.text)
    await message.answer("The category is recorded!")
    await message.answer("Now enter your text for the meme.\n\n"
                         "You can type anything you want, but you only have <strong>60 characters...</strong>\n\n"
                         "<i>Unfunny memes will not be accepted</i>")
    await state.set_state(schemas.Sug_meme.meme_text_sug)



@router.message(schemas.Sug_meme.meme_category)
async def category_incorrectly(message: Message):
    await message.answer(
        "...it should be one word in English (for example, 'cat' or 'Dog').\n\n"
        "<b>Numbers and special characters are not allowed. Only letters...</b>"
        "\n\nPlease try again:",
    )


@router.message(schemas.Sug_meme.meme_text_sug, F.text, Correct_meme_text())
async def text_cor(message: Message, state: FSMContext):
    await state.update_data(meme_text=message.text)
    user_data = await state.get_data()
    await message.answer("Your meme has been successfully recorded!\n\n"
                         "<i>You better hope it's funny, or you'll be banned for life.........</i>")
    # print(schemas.Meme.parse_obj(user_data).json())
    requests.post('http://127.0.0.1:8000/post_meme', data=schemas.Meme.parse_obj(user_data).json())
    await state.clear()


@router.message(schemas.Sug_meme.meme_text_sug)
async def text_incorrectly(message: Message):
    await message.answer(
        "...You can type any text you want, but you only have <strong>60 characters...</strong>\n\n"
        "<i>Unfunny memes will not be accepted</i>",
    )


#GAVNO GAVNA
# @router.message(Command("random"))
# async def cmd_random(message: types.Message):
#     builder = InlineKeyboardBuilder()
#     builder.add(types.InlineKeyboardButton(
#         text="LALALA",
#         callback_data="random_value")
#     )
#     await message.answer(
#         "LOL",
#         reply_markup=builder.as_markup()
#     )


# @router.callback_query(Text("random_value"))
# async def send_random_value(callback: types.CallbackQuery):
#     await callback.message.answer("/suggest_a_meme")
#     await callback.answer("LOWLQPL{QLDPQWDQWKDKQWD}")
