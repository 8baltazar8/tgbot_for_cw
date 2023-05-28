import asyncio
import logging
from aiogram import Bot, Dispatcher
from handlers import meme_gen, suggest_meme, top_base, bottom_base, random
from settings import config

logging.basicConfig(level=logging.INFO)


async def main():
    bot = Bot(token=config.bot_token.get_secret_value(), parse_mode="HTML")
    dp = Dispatcher()
    dp.include_routers(top_base.router)
    dp.include_routers(meme_gen.router)
    dp.include_routers(suggest_meme.router)
    dp.include_router(random.router)
    dp.include_routers(bottom_base.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
