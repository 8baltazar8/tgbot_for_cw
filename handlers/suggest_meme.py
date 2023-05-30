import requests
from aiogram import types, F, Router
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from . import schemas
from .filters.correct_meme import Correct_category, Correct_meme_text


router = Router()


@router.message(Command("suggest_a_meme"))
async def suggest_a_meme(message: types.Message, state: FSMContext):
    await state.clear()
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
    requests.post('https://memeinator-api.herokuapp.com/post_meme', data=schemas.Meme.parse_obj(user_data).json())
    await state.clear()


@router.message(schemas.Sug_meme.meme_text_sug)
async def text_incorrectly(message: Message):
    await message.answer(
        "...You can type any text you want, but you only have <strong>60 characters...</strong>\n\n"
        "<i>Unfunny memes will not be accepted</i>",
    )
