from aiogram import types, F, Router


router = Router()


@router.message(F.animation)
async def echo_gif(message: types.Message):
    await message.reply_animation(message.animation.file_id, caption="Only pics!")


@router.message(F.video | F.audio | F.sticker)
async def echo_video(message: types.Message):
    await message.reply_animation("https://i.gifer.com/ICU.gif", caption="Only pics!")


@router.message(F.text)
async def echo_text(message: types.Message):
    await message.answer("Send me pic and I will generate meme for you!\n\n"
                         "Or send me a picture with text and get a demotivator\n\n"
                         "If you want to suggest your own text for a meme, use the /suggest_a_meme command",)
