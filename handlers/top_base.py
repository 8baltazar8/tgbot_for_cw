from aiogram import types, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

router = Router()


@router.message(Command(commands=["cancel"]))
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Canceled",
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Hey! Send me pic and I will generate meme for you!\n\n"
                         "Or send me a picture with text and get a demotivator",)

@router.message(Command("help"))
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer("<b>This bot allows you to create memes.</b>\n\n\n"
                         "👾 Send me a picture and you'll get a meme with the most appropriate text according to the AI.\n\n"
                         "👾 Send a picture with a text - get a demotivator.\n\n"
                         "👾 You can also suggest your own texts for memes for the AI to use.\n\n"
                         "👾 You can also suggest your own texts for memes using the /suggest_a_meme command.\n\n"
                         "👾 The /cancel command cancels any action.\n\n\n"
                         "<b>Just follow the instructions</b>",)
