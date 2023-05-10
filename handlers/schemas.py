from pydantic import BaseModel, ValidationError, validator, Field
from typing import Optional, List, IO

import re


class Meme(BaseModel):
    meme_text: str
    category: str

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
