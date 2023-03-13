from pydantic import BaseModel
from typing import List


class Component(BaseModel):
    name: str
    code_words: List[str]
    phrases: List[str]
