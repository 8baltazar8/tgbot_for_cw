from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import types


def make_row_keyboard(items: list[int] = list(range(1, 11))) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    for i in items:
        builder.add(types.KeyboardButton(text=str(i)))
    builder.adjust(5)
    return builder.as_markup(resize_keyboard=True)
