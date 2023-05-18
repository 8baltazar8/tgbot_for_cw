import re
from aiogram.filters import BaseFilter
from aiogram.types import Message


class Correct_category(BaseFilter):  # [1]
    def __init__(self): # [2]
        self.category = 1

    async def __call__(self, message: Message) -> bool:  # [3]
        if self.category and re.match(r"^[a-zA-Z]+$", message.text):
            return True
        else:
            return False


class Correct_meme_text(BaseFilter):  # [1]
    def __init__(self): # [2]
        pass

    async def __call__(self, message: Message) -> bool:  # [3]
        if len(message.text)<=60:
            return True
        else:
            return False
