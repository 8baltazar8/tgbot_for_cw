from aiogram import Bot, Dispatcher, types, F, Router
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Hey! Sand me pic and I will generate meme for you!")


@router.message(F.animation)
async def echo_gif(message: types.Message):
    await message.reply_animation(message.animation.file_id, caption="Only pics!")


@router.message(F.video | F.audio | F.sticker)
async def echo_video(message: types.Message):
    await message.reply_animation("https://i.gifer.com/ICU.gif", caption="Only pics!")


@router.message(F.text)
async def echo_text(message: types.Message):
    await message.answer("Sand me pic and I will generate meme for you!\n\n"
                         "Or if you want to suggest your own text for a meme, use the /suggest_a_meme command",)
