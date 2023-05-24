from pydantic import BaseModel, ValidationError, validator, Field
from typing import Optional, List, IO, Text
from aiogram.fsm.state import State, StatesGroup

import re


class Meme(BaseModel):
    category: str
    meme_text: str


    @validator('category')
    def category_must_be_lowercasealpha(cls, category):
        assert re.match(r"^[a-zA-Z]+$", category), "Category should consist of lowercase letters, should be a word"
        return category.lower()


class Post_Meme(Meme):
    id: int
    meme_text: str
    category: str

    class Config:
        orm_mode = True


class Meme_by_category(BaseModel):
    memes: List[Post_Meme]
# ________________________________


class Meme_generated(BaseModel):
    id: int
    content: bytes


class User_rate(BaseModel):
    id: int
    grade: int


class Sug_meme(StatesGroup):
    meme_category = State()
    meme_text_sug = State()


class Sug_meme_404(StatesGroup):
    start_meme_sug = State()
