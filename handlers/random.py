from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from . import schemas
import requests

router = Router()


@router.message(Command(commands=["random"]))
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    meme = schemas.Random_meme.parse_obj(requests.get('https://memeinator-api.herokuapp.com/random_meme'))
    await message.answer(
        text=f"{meme.meme_text}",
        reply_markup=ReplyKeyboardRemove()
    )
